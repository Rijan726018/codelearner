"use strict";
/* ---------- stage metadata (content lives in data/sN.json) ---------- */
const META = [
  {id:"s0", name:"Base Camp",            span:"Weeks 1–2",     hours:"~20 h",    goal:"Set up your tools and your habits."},
  {id:"s1", name:"Foundations",          span:"Months 1–3",    hours:"~200 h",   goal:"Write real programs in Python."},
  {id:"s2", name:"Algorithmic Thinking", span:"Months 3–6",    hours:"~450 h",   goal:"Solve problems you've never seen."},
  {id:"s3", name:"Under the Hood",       span:"Months 6–9",    hours:"~750 h",   goal:"Understand what the computer actually does."},
  {id:"s4", name:"Building Real Software",span:"Months 9–14",  hours:"~1,200 h", goal:"Ship applications people use."},
  {id:"s5", name:"Engineering Craft",    span:"Months 14–20",  hours:"~1,900 h", goal:"Write code others are glad to work with."},
  {id:"s6", name:"Systems at Scale",     span:"Months 20–30",  hours:"~3,000 h", goal:"Design systems that survive failure."},
  {id:"s7", name:"Deep Specialty",       span:"Years 2.5–4",   hours:"~5,000 h", goal:"Become one of the best in one area."},
  {id:"s8", name:"Summit",               span:"Year 4 →",      hours:"10,000 h+",goal:"Do work that moves the field forward."}
];
const LEVELS = {1:{name:"Recall", desc:"Facts and definitions, straight from memory."},
                2:{name:"Apply",  desc:"Use an idea on a new case: predict, compute, write."},
                3:{name:"Analyze",desc:"Debug, compare trade-offs, choose a design."}};
const PASS = 0.8;
let INTERVALS = [1,3,7,16,35,90,180];

/* ---------- state ---------- */
const D = {stages:[], research:null, q:{}, mods:[], lessons:{}, modById:{}};
const P0 = () => ({lessons:{}, notes:{}, ms:{}, exams:{}, log:{}, solved:{}, tried:{}, steps:{}, nodes:{}, badges:{}, xpSeen:null, time:{}, manual:[], goal:null, calib:{}});
const normP = d => { const z=P0(); Object.keys(z).forEach(k=>{ if(d && d[k]!=null) z[k]=d[k]; }); return z; };
let P = P0();   // progress doc: core lessons, notes, milestones, exams, activity log, problems, bootcamp steps, roadmap nodes, badges, practice time, confidence calibration
let S = {cards:{}};                                        // spaced-repetition doc
let route = {v:"home"};
const EXTRA_LOADERS = [];   // other modules push async loaders (problems, bootcamp, paths) that boot awaits
let mapStage = null;
let practiceStage = null;
const stores = {p:null, s:null}; const timers = {};

const $ = s => document.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const md = s => esc(s).replace(/`([^`]+)`/g,"<code>$1</code>").replace(/\*\*([^*]+)\*\*/g,"<b>$1</b>").replace(/(^|[\s(])\*([^\s*](?:[^*]*?[^\s*])?)\*(?=[\s.,;:!?)]|$)/g,"$1<em>$2</em>");
const shuffle = a => { a=[...a]; for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]} return a; };
const pick = (a,n) => shuffle(a).slice(0,n);
const dayNum = (d=new Date()) => Math.floor((d.getTime() - d.getTimezoneOffset()*60000)/86400000);
const today = () => dayNum();
const dayKey = n => new Date(n*86400000).toISOString().slice(0,10);
const fmtDay = n => new Date(n*86400000).toLocaleDateString(undefined,{timeZone:"UTC",month:"short",day:"numeric"});

/* ---------- persistence ---------- */
const LKEY = {p:"tenk2-progress", s:"tenk2-srs"};
function loadLocal(){ try{ const p=JSON.parse(localStorage.getItem(LKEY.p)||"null"); if(p) P=normP(p); const s=JSON.parse(localStorage.getItem(LKEY.s)||"null"); if(s) S={...S,...s}; }catch(e){} }
function setSync(t,ok){ const el=$("#sync"); el.textContent=t; el.classList.toggle("ok",!!ok); }
let gameT=null;
function save(which, quiet){
  const data = which==="p"?P:S;
  if(!quiet){ clearTimeout(gameT); gameT=setTimeout(()=>Game.sync(), 60); }
  try{ localStorage.setItem(LKEY[which], JSON.stringify(data)); }catch(e){}
  if(!stores[which]){ setSync("Saved in this browser"); return; }
  setSync("Saving…"); clearTimeout(timers[which]);
  timers[which] = setTimeout(async()=>{
    try{ await stores[which].set({...data, updated:new Date().toISOString()}); setSync("Saved to your account",true); }
    catch(e){ setSync("Saved in this browser only"); }
  }, 800);
}
function logActivity(n=1){ const k=dayKey(today()); P.log[k]=(P.log[k]||0)+n; }

/* ---------- account storage: the same doc interface ({get, set}) for the Claude runtime and for Google accounts ---------- */
const isObj = v => v && typeof v==="object" && !Array.isArray(v);
// Merge two copies of a progress doc so nothing done on either side is lost: maps are unioned, numbers keep the larger
// value (best scores, seconds practised, reps), lists of entries are unioned by id, and other values prefer the account copy.
function mergeDeep(a, b){
  if(Array.isArray(a) && Array.isArray(b)){ const seen=new Set(), out=[]; [...b, ...a].forEach(x=>{ const k=isObj(x)&&x.id!=null?x.id:JSON.stringify(x); if(!seen.has(k)){ seen.add(k); out.push(x); } }); return out; }
  if(isObj(a) && isObj(b)){ const out={...a}; Object.keys(b).forEach(k=>{ out[k] = k in a ? mergeDeep(a[k], b[k]) : b[k]; }); return out; }
  if(typeof a==="number" && typeof b==="number") return Math.max(a, b);
  if(b==null || b==="") return a;
  return b;
}
const ACCOUNT_HOOKS = [];   // other modules (the editor) attach their own docs: f(col) on connect, f(null) on disconnect
async function attachStores(col, label="Saved to your account"){
  stores.p=col.doc("v2progress"); stores.s=col.doc("v2srs"); Drafts.col=col; Drafts.cache={};
  setSync("Syncing…");
  const [sp,ss]=await Promise.all([stores.p.get(), stores.s.get()]);
  if(sp.exists) P=normP(mergeDeep(P, sp.data()||{}));
  if(ss.exists) S={cards:mergeDeep(S.cards||{}, (ss.data()||{}).cards||{})};
  await Promise.all([stores.p.set({...P, updated:new Date().toISOString()}), stores.s.set({...S, updated:new Date().toISOString()})]);
  try{ localStorage.setItem(LKEY.p,JSON.stringify(P)); localStorage.setItem(LKEY.s,JSON.stringify(S)); }catch(e){}
  for(const f of ACCOUNT_HOOKS){ try{ await f(col); }catch(e){} }
  setSync(label,true);
  Game.sync(true);
  if(!["lesson","exam","review","practice","problem","course","make","code"].includes(route.v)) render();
}
function detachStores(){ stores.p=stores.s=null; Drafts.col=null; Drafts.cache={}; ACCOUNT_HOOKS.forEach(f=>{ try{ f(null); }catch(e){} }); }

/* ---------- content indexing ---------- */
function indexContent(){
  D.q={}; D.mods=[]; D.lessons={}; D.modById={};
  D.stages.forEach((st,si)=>{
    if(!st) return;
    st.modules.forEach((m,mi)=>{
      m.sid=st.id; m.si=si; m.mi=mi; m.gi=D.mods.length; D.mods.push(m); D.modById[m.id]=m;
      m.lessons.forEach((l,li)=>{
        l.mid=m.id; l.li=li; D.lessons[l.id]=l;
        l.questions.forEach(q=>{ D.q[q.id]={...q, sid:st.id, mid:m.id, lid:l.id}; });
      });
      (m.exam||[]).forEach(q=>{ D.q[q.id]={...q, sid:st.id, mid:m.id, lid:null}; });
    });
  });
}
const passed = m => (P.exams[m.id]?.best ?? 0) >= PASS;
const isTrack = m => m.sid==="s7" && m.mi>=1;
const anyTrackPassed = () => D.mods.some(x=>isTrack(x)&&passed(x));
function isOpen(m){
  if(m.gi===0||passed(m)) return true;
  if(isTrack(m)){ const base=D.modById["s7m1"]; return !!base && passed(base); }
  const prev=D.mods[m.gi-1]; if(!prev) return true;
  if(isTrack(prev)) return anyTrackPassed();
  return passed(prev);
}
const lessonsDone = m => m.lessons.filter(l=>P.lessons[l.id]).length;
const msDone = m => (m.project?.milestones||[]).filter((_,i)=>P.ms[m.id+":"+i]).length;
function currentModule(){ const tp=anyTrackPassed(); return D.mods.find(m=>isOpen(m)&&!passed(m)&&!(tp&&isTrack(m))) || D.mods[D.mods.length-1]; }
function nextLesson(){ const m=currentModule(); if(!m) return null; return m.lessons.find(l=>!P.lessons[l.id]) || null; }
function stageStats(sid){
  const ms=D.mods.filter(m=>m.sid===sid); const L=ms.flatMap(m=>m.lessons);
  return {mods:ms.length, passed:ms.filter(passed).length, lessons:L.length, done:L.filter(l=>P.lessons[l.id]).length};
}
function dueCards(){ const t=today(); return Object.entries(S.cards).filter(([id,c])=>c.d<=t && D.q[id]).map(([id])=>id); }

/* ---------- spaced repetition (Leitner boxes on expanding intervals) ----------
   conf is how sure the learner said they were: "guess", "think" or "sure". A right answer that was a guess isn't
   knowledge yet, so the card stays in its box and comes back tomorrow. Every rated answer also feeds P.calib,
   which the profile turns into a calibration chart (how often "certain" is actually right). */
const CONF = [{k:"guess", label:"Guessing"}, {k:"think", label:"Fairly sure"}, {k:"sure", label:"Certain"}];
function srs(qid, correct, conf){
  const t=today(); const c=S.cards[qid]; const lucky = correct && conf==="guess";
  if(!c){ S.cards[qid] = {b:0, d:t+INTERVALS[0], l:correct?0:1}; }
  else if(lucky){ c.d=t+1; }
  else if(correct){ c.b=Math.min(c.b+1, INTERVALS.length-1); c.d=t+INTERVALS[c.b]; }
  else { c.b=0; c.d=t+1; c.l=(c.l||0)+1; }
  if(conf){ const k=P.calib[conf] || (P.calib[conf]={n:0, ok:0}); k.n++; if(correct) k.ok++; save("p", true); }
  logActivity(); save("s");
}

/* ---------- tooltip ---------- */
const tip=$("#tip");
document.addEventListener("pointerover",e=>{ const t=e.target.closest("[data-tip]"); if(!t){tip.hidden=true;return;} tip.textContent=t.dataset.tip; tip.hidden=false; });
document.addEventListener("pointermove",e=>{ if(tip.hidden) return; const x=Math.min(e.clientX+12, window.innerWidth-tip.offsetWidth-8); tip.style.left=x+"px"; tip.style.top=(e.clientY-34)+"px"; });

/* ---------- navigation ---------- */
const routeHash = r => "#/"+r.v+(r.id?"/"+encodeURIComponent(r.id):"");
function parseHash(){ const h=(location.hash||"").replace(/^#\/?/,""); if(!h) return null; const [v,id]=h.split("/"); return VIEWS[v]?{v, ...(id?{id:decodeURIComponent(id)}:{})}:null; }
function go(r){ route=r; tip.hidden=true; Palette.close?.();
  try{ if(location.hash!==routeHash(r)) history.pushState(null,"",routeHash(r)); }catch(e){}
  const swap=()=>{ render(); window.scrollTo({top:0}); };
  if(document.startViewTransition && !matchMedia("(prefers-reduced-motion: reduce)").matches) document.startViewTransition(swap); else swap(); }
window.addEventListener("popstate",()=>{ const r=parseHash(); route=r||{v:"home"}; render(); });
$("#tabs").addEventListener("click",e=>{ const b=e.target.closest("[data-v]"); if(b) go({v:b.dataset.v}); });
function updateBadge(){ const n=dueCards().length, bd=$("#duebadge"); if(!bd) return; bd.hidden=!n; bd.textContent=n; }
const TAB_OF = {lesson:"map", exam:"map", path:"paths", problem:"problems", course:"bootcamp", project:"build", make:"build"};
const currentTab = () => TAB_OF[route.v] || route.v;
function render(){
  UI.syncNav(currentTab());
  updateBadge();
  const v = VIEWS[route.v] || VIEWS.home; v($("#main"));
  document.title = (route.v==="home"?"CodeLearner · Learn to code, from zero to world-class":(document.querySelector("#main .h1, #main h1")?.textContent?.trim()||"CodeLearner")+" · CodeLearner");
}

/* ================= TODAY ================= */
function streak(){ let t=today(), n=0; if(!P.log[dayKey(t)]) t--; while(P.log[dayKey(t)]){ n++; t--; } return n; }
function viewToday(el){
  const due=dueCards().length, nl=nextLesson(), cm=currentModule();
  const wd=new Date().getDay(), deep=(wd===2||wd===4) && !!cm && lessonsDone(cm)>=2;
  const doneToday = P.log[dayKey(today())]||0;
  const lessonsTotal=Object.keys(D.lessons).length, lessonsN=Object.keys(P.lessons).filter(k=>D.lessons[k]).length;
  const examsN=D.mods.filter(passed).length;
  const projM = cm && cm.project ? cm : null;
  const nextMs = projM ? projM.project.milestones.findIndex((_,i)=>!P.ms[projM.id+":"+i]) : -1;
  const lessonsLeft = cm ? cm.lessons.length - lessonsDone(cm) : 0;
  const greeting = deep ? "Deep-work day. Reviews first, then put most of today into your project." : (wd===2||wd===4) ? "Long day: reviews, then two lessons back to back. Projects start once you have a couple of lessons in." : "Short session: reviews first, then one lesson.";
  const items=[];
  items.push(`<li class="${due?"":"done"}"><div><h4>${due?`Review ${due} card${due>1?"s":""}`:"Reviews: all caught up"}</h4><p>${due?`About ${Math.max(2,Math.round(due*0.6))} min. Mixed topics, so you practise choosing the right idea.`:"New cards appear here as you finish lessons and exams."}</p></div>${due?`<button class="btn primary" data-act="review">Start review</button>`:""}</li>`);
  if(nl && !deep) items.push(`<li><div><h4>Lesson: ${esc(nl.title)}</h4><p>${esc(D.modById[nl.mid].title)} · Day ${nl.li+1} of ${D.modById[nl.mid].lessons.length} · ~${nl.minutes||60} min</p></div><button class="btn primary" data-lesson="${nl.id}">Open lesson</button></li>`);
  if(cm && !nl && !passed(cm)) items.push(`<li><div><h4>Exam: ${esc(cm.title)}</h4><p>You finished every lesson in this module. Score ${PASS*100}% to unlock the next one.</p></div><button class="btn exam" data-exam="${cm.id}">Take exam</button></li>`);
  if(projM && nextMs>=0) items.push(`<li><div><h4>Project: ${esc(projM.project.title)}</h4><p>Next milestone: ${esc(projM.project.milestones[nextMs])}</p></div><button class="btn" data-act="projects">Open projects</button></li>`);
  if(nl && deep) items.push(`<li><div><h4>Then, if time is left: ${esc(nl.title)}</h4><p>Day ${nl.li+1} of ${esc(D.modById[nl.mid].title)}</p></div><button class="btn" data-lesson="${nl.id}">Open lesson</button></li>`);

  const g=Game.stats();
  const cont=[];
  if(nl) cont.push({i:"map", k:"Core curriculum", t:nl.title, s:`${D.modById[nl.mid].title} · day ${nl.li+1}`, a:`data-lesson="${nl.id}"`});
  const ns=BC.nextStep?.(); if(ns) cont.push({i:"cap", k:"Bootcamp", t:ns.step.title, s:`${ns.course.title} · step ${ns.idx+1} of ${ns.course.steps.length}`, a:`data-course="${ns.course.id}" data-step="${ns.idx}"`});
  const np=PJ.next?.(); if(np) cont.push({i:"rocket", k:"Build & Learn", t:np.project.title, s:`Step ${np.idx+1} of ${np.project.steps.length}: ${np.step.title}`, a:`data-project="${np.project.id}"`});
  const cp=PATHS.current?.(); if(cp) cont.push({i:cp.icon, k:"Career path", t:cp.title, s:`${cp.done} of ${cp.total} topics done`, a:`data-path="${cp.id}"`});
  const dp=PB.daily?.(); if(dp) cont.push({i:"braces", k:"Problem of the day", t:dp.title, s:`${dp.difficulty} · ${dp.tags.slice(0,2).join(", ")}${P.solved?.[dp.id]?" · solved ✓":""}`, a:`data-problem="${dp.id}"`});
  el.innerHTML = `
  <section class="head">
    <span class="eyebrow">${new Date().toLocaleDateString(undefined,{weekday:"long",month:"long",day:"numeric"})}</span>
    <h1 class="h1">${lessonsN?`Stage ${cm?cm.si:0}: <span class="gt">${esc(META[cm?cm.si:0].name)}</span>`:`Welcome, <span class="gt">${esc(Game.rank(g.level))}</span>`}</h1>
    <p class="lede">${greeting} ${lessonsN?"":"Already know some programming? Open Learn and test out of any module you can pass, so you only spend time on what's new to you."}</p>
  </section>
  <section class="panel glow" style="background:linear-gradient(135deg,var(--surface),var(--surface2))"><div class="lvcardx">${Game.ringSVG(g,128)}<div style="display:grid;gap:8px;min-width:0">
    <span class="eyebrow">${esc(Game.rank(g.level))}</span><b class="h2"><span class="gt">${g.xp.toLocaleString()}</span> XP</b>
    <div class="bar"><i style="width:${100*(g.xp-g.cur)/Math.max(1,g.next-g.cur)}%"></i></div>
    <span class="muted" style="font-size:.88rem">${(g.next-g.xp).toLocaleString()} XP to level ${g.level+1} · ${Object.keys(P.badges||{}).length} badges · <button class="btn ghost sm" data-act="profile">View profile</button></span></div></div></section>
  ${typeof clockCard==="function"?clockCard():""}
  <div class="stats">
    <div class="stat">${icon("flame")}<b>${streak()}</b><span>day streak</span></div>
    <div class="stat">${icon("refresh")}<b>${due}</b><span>reviews due</span></div>
    <div class="stat">${icon("book")}<b>${lessonsN}<small class="muted" style="font-size:.9rem"> / ${lessonsTotal}</small></b><span>lessons done</span></div>
    <div class="stat">${icon("braces")}<b>${g.solved}<small class="muted" style="font-size:.9rem"> / ${PB.list.length||0}</small></b><span>problems solved</span></div>
  </div>
  ${cont.length?`<section style="display:grid;gap:12px"><h2 class="h2">Pick up where you left off</h2><div class="cont">${cont.map(c=>`<button type="button" class="ccard glow" ${c.a}><span class="row" style="gap:8px;color:var(--accent)">${icon(c.i)}<span class="eyebrow" style="color:inherit">${esc(c.k)}</span></span><b>${esc(c.t)}</b><span>${esc(c.s)}</span></button>`).join("")}</div></section>`:""}
  <div class="grid2">
    <section class="panel" style="grid-column:1/-1">
      <div class="row" style="justify-content:space-between"><h2 class="h2">Today's session</h2><span class="pill ${doneToday?"ok":""}">${doneToday?`${doneToday} reps logged today`:"Nothing logged yet today"}</span></div>
      <ol class="plan">${items.join("")}</ol>
      ${cm?`<p class="muted" style="margin:0;font-size:.88rem">Current module: <b>${esc(cm.title)}</b>, ${lessonsDone(cm)}/${cm.lessons.length} lessons${lessonsLeft?"":" · exam ready"}.</p>`:""}
    </section>
    <section class="panel"><h2 class="h2">Practice days</h2>${heatmap()}</section>
    <section class="panel"><h2 class="h2">Reviews coming up</h2>${forecast()}</section>
    <section class="panel" style="grid-column:1/-1"><div class="row" style="justify-content:space-between"><h2 class="h2">Mastery by stage</h2><span class="legend"><i style="background:var(--accent)"></i> lessons done</span></div>${mastery()}</section>
  </div>`;
}
function heatmap(){
  const weeks=18, t=today(); let s0=t-(weeks*7-1); s0-=new Date(s0*86400000).getUTCDay();
  let cells="";
  for(let d=s0; d<=t; d++){
    const n=P.log[dayKey(d)]||0; const l=n===0?0:n<5?1:n<15?2:n<30?3:4;
    cells+=`<i data-l="${l}" class="${d===t?"today":""}" data-tip="${fmtDay(d)}: ${n} rep${n===1?"":"s"}"></i>`;
  }
  return `<div class="heat" role="img" aria-label="Practice activity over the last ${weeks} weeks">${cells}</div>
  <div class="legend">Less <i style="background:var(--sunk)"></i><i style="background:color-mix(in oklab,var(--accent) 30%,var(--sunk))"></i><i style="background:color-mix(in oklab,var(--accent) 55%,var(--sunk))"></i><i style="background:color-mix(in oklab,var(--accent) 78%,var(--sunk))"></i><i style="background:var(--accent)"></i> More · one rep = one question answered or lesson finished</div>`;
}
function forecast(){
  const t=today(), N=14, counts=Array(N).fill(0);
  Object.entries(S.cards).forEach(([id,c])=>{ if(!D.q[id]) return; const k=Math.max(0,c.d-t); if(k<N) counts[k]++; });
  const total=Object.keys(S.cards).length;
  if(!total) return `<div class="empty">Your review deck is empty. Every question you answer in a lesson or exam becomes a card that comes back on a schedule: ${INTERVALS.join(", ")} days.</div>`;
  const W=420,H=150,pad={l:26,b:22,t:8}, max=Math.max(4,...counts), step=Math.ceil(max/4), top=step*4;
  const bw=(W-pad.l)/N; const y=v=>pad.t+(H-pad.t-pad.b)*(1-v/top);
  let g=""; for(let v=0; v<=top; v+=step) g+=`<line class="grid" x1="${pad.l}" x2="${W}" y1="${y(v)}" y2="${y(v)}"/><text x="${pad.l-6}" y="${y(v)+3}" text-anchor="end">${v}</text>`;
  let bars=""; counts.forEach((c,i)=>{ const x=pad.l+i*bw+3, h=y(0)-y(c);
    const label=i===0?"Today (incl. overdue)":fmtDay(t+i);
    if(c) bars+=`<rect class="b ${i===0?"now":""}" x="${x}" y="${y(c)}" width="${bw-6}" height="${h}" rx="3"/>`;
    bars+=`<rect class="hit" x="${pad.l+i*bw}" y="${pad.t}" width="${bw}" height="${H-pad.t-pad.b}" data-tip="${label}: ${c} card${c===1?"":"s"}"/>`;
    if(i%2===0) bars+=`<text x="${pad.l+i*bw+bw/2}" y="${H-6}" text-anchor="middle">${i===0?"Today":"+"+i+"d"}</text>`; });
  return `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Cards due over the next 14 days">${g}${bars}</svg>
  <p class="muted" style="margin:0;font-size:.85rem">${total} cards in your deck. Today's bar (amber) includes anything overdue.</p>`;
}
function mastery(){
  return `<div class="mast">`+META.map((s,i)=>{ const st=stageStats(s.id); const p=st.lessons?Math.round(100*st.done/st.lessons):0;
    return `<div class="r"><span>${i}. ${esc(s.name)}</span><span class="t" data-tip="${st.done}/${st.lessons} lessons · ${st.passed}/${st.mods} exams passed"><i style="width:${p}%"></i></span><span class="n">${st.lessons?p+"%":"—"}</span></div>`; }).join("")+`</div>`;
}

/* ================= MAP ================= */
function viewMap(el){
  if(mapStage==null){ const cm=currentModule(); mapStage = cm?cm.si:0; }
  const st=D.stages[mapStage], meta=META[mapStage];
  const ladder = META.map((s,i)=>{ const ss=stageStats(s.id); const p=ss.lessons?Math.round(100*ss.done/ss.lessons):0; const first=D.mods.find(m=>m.sid===s.id); const locked=first&&!isOpen(first);
    return `<button type="button" data-stage="${i}" aria-current="${i===mapStage}" class="${locked?"lock":""}"><span class="k">STAGE ${i}${locked?" · LOCKED":""}</span><span class="nm">${esc(s.name)}</span><span class="t"><i style="width:${p}%"></i></span></button>`; }).join("");
  let body;
  if(!st) body = `<div class="empty">This stage's lessons aren't available yet. Reload the page later to check again.</div>`;
  else {
    const nl=nextLesson();
    body = `<div class="modules">`+st.modules.map(m=>{
      const open=isOpen(m), done=lessonsDone(m), ex=P.exams[m.id], pass=passed(m), mdn=msDone(m), mt=m.project?.milestones?.length||0;
      const days=m.lessons.map((l,i)=>`<button type="button" class="day ${P.lessons[l.id]?"done":""} ${nl&&nl.id===l.id?"next":""}" ${open?`data-lesson="${l.id}"`:`aria-disabled="true"`} title="${esc(l.title)}"><span class="dn">${P.lessons[l.id]?"✓":i+1}</span><span class="tt">${esc(l.title)}</span></button>`).join("");
      const examBtn = pass ? `<span class="pill ok">Passed · ${Math.round(ex.best*100)}%</span><button class="btn ghost" data-exam="${m.id}">Retake</button>`
        : done===m.lessons.length ? `<button class="btn exam" data-exam="${m.id}">Take exam</button>${ex?`<span class="pill">Best ${Math.round(ex.best*100)}%</span>`:""}`
        : `<button class="btn" data-exam="${m.id}" title="Pass the exam to skip this module">Test out</button>${ex?`<span class="pill">Best ${Math.round(ex.best*100)}%</span>`:""}`;
      return `<article class="mod ${open?"":"locked"}">
        <div><span class="eyebrow">${isTrack(m)?"Track · pick one":"Module "+(m.mi+1)} · ${done}/${m.lessons.length} lessons${open?"":isTrack(m)?" · opens when module 1 is passed":" · locked until the previous exam is passed"}</span><h3>${esc(m.title)}</h3><p>${esc(m.summary)}</p></div>
        <div class="side">${examBtn}</div>
        <div class="days">${days}</div>
        ${m.project?`<div class="proj"><span class="pill acc">Project</span><b>${esc(m.project.title)}</b><span class="minibar"><i style="width:${mt?100*mdn/mt:0}%"></i></span><span class="muted">${mdn}/${mt} milestones</span><button class="btn ghost" data-act="projects">Open</button></div>`:""}
      </article>`; }).join("")+`</div>`;
  }
  el.innerHTML = `<div class="ladder" role="tablist" aria-label="Stages">${ladder}</div>
    <section class="stagehead"><span class="eyebrow">Stage ${mapStage} of 8</span><h1 class="h1">${esc(meta.name)}</h1><p class="lede">${esc(meta.goal)} Each numbered tile is one day's lesson. Finish a module's lessons, then pass its exam at ${PASS*100}% to unlock the next. If you already know a module, use <b>Test out</b>.</p>
    <div class="facts"><span class="pill acc">${esc(meta.span)}</span><span class="pill acc">${esc(meta.hours)} cumulative</span>${st?`<span class="pill">${st.modules.length} modules · ${st.modules.reduce((a,m)=>a+m.lessons.length,0)} lessons</span>`:""}</div></section>
    ${body}`;
}

/* ================= LESSON =================
   The page follows what the learning research says works (Method page): guess first (pretesting), read, watch a short
   video then recall it (interpolated testing), study a worked example after predicting its output (PRIMM), confront the
   common misconceptions (refutation), produce something, explain it back, answer with a confidence rating, and only then
   compare against the key takeaways. */
function viewLesson(el){
  const l=D.lessons[route.id]; if(!l){ go({v:"map"}); return; }
  const m=D.modById[l.mid], meta=META[m.si];
  const idx=m.lessons.indexOf(l), next=m.lessons[idx+1], prev=m.lessons[idx-1];
  const exLang = l.example ? normLang(l.example.lang) : null;
  const tryLang = exLang || (l.example && ["c","go","rust","bash","ts","tsx"].includes(l.example.lang) ? null : ({s0:"python",s1:"python",s2:"python",s5:"python",s6:"python",s7:"python"})[m.sid] || null);
  const warm = P.lessons[l.id] ? null : (l.questions.find(q=>q.type==="mcq"&&q.level<=2) || l.questions[0]);
  const secs=[]; const sec=(id,title,html)=>secs.push({id,title,html});
  const note=(k,ph,max=600)=>`<textarea class="explain sm" data-note="${esc(k)}" maxlength="${max}" placeholder="${esc(ph)}">${esc(P.notes[k]||"")}</textarea>`;
  sec("learn","Learn",`<div class="prose">${(l.concept||[]).map(p=>`<p>${md(p)}</p>`).join("")}</div>
    ${(l.terms||[]).length?`<div class="terms"><span class="eyebrow">Key terms</span><dl>${l.terms.map(t=>`<div><dt>${md(t.t)}</dt><dd>${md(t.d)}</dd></div>`).join("")}</dl></div>`:""}`);
  sec("watch","Watch",`${videoBlock(l)}${l.video?`<div class="recall"><span class="eyebrow">After watching · from memory</span><p>Without rewinding, write the one idea from the video you most want to keep, or one thing it showed that the reading didn't.</p>${note(l.id+":v","The video's key idea, in my words…")}</div>`:""}`);
  if(l.visual) sec("see","See it",visual(l.visual));
  if(l.example) sec("example","Worked example",`${exLang?`<div class="predict"><span class="eyebrow">Predict first</span><p>Read the code and write what you expect it to print <b>before</b> you press Run. Then run it, compare, and change one thing to test your idea.</p>${note(l.id+":p","I expect it to print…",400)}</div><div id="ex-ed"></div>`:codeBlock(l.example.code)+(l.example.lang&&!["text","markdown","diff"].includes(l.example.lang)?`<p class="muted" style="margin:0;font-size:.85rem">${esc(String(l.example.lang).toUpperCase())} doesn't run in the browser. Predict what it does, then copy it into a file and run it in your terminal.</p>`:"")}<div class="prose"><p>${md(l.example.explain||"")}</p></div>`);
  if((l.mistakes||[]).length) sec("mistakes","Common mistakes",`<p class="muted" style="margin:0;font-size:.9rem">Beginners often believe these. Read the wrong idea, then why it's wrong.</p><div class="mist">${l.mistakes.map(x=>`<div class="mi"><div class="w"><span class="eyebrow">Myth</span><p>${md(x.wrong)}</p></div><div class="r"><span class="eyebrow">Actually</span><p>${md(x.right)}</p></div></div>`).join("")}</div>`);
  sec("try","Try it yourself",`<div class="tryit"><span class="eyebrow">${tryLang?"Write it below · no peeking":"In your editor · no peeking"}</span><div>${md(l.tryit)}</div></div>${tryLang?`<div id="try-ed"></div><p class="muted" style="margin:0;font-size:.85rem">Your code saves automatically. Stuck for 20 minutes? Ask the hint tutor; it can see this code.</p>`:""}`);
  sec("explain","Explain it back",`<p class="muted" style="margin:0;font-size:.9rem">Write two or three sentences as if teaching a friend. Gaps in your explanation are gaps in your understanding.</p>
    <textarea class="explain" id="note-${l.id}" maxlength="1500" placeholder="In my own words…">${esc(P.notes[l.id]||"")}</textarea>`);
  sec("check","Check yourself",`<p class="muted" style="margin:0;font-size:.9rem">Pick how sure you are when you check each answer. Lucky guesses come back tomorrow, and confident misses get flagged.</p><div id="lq"></div>`);
  if((l.takeaways||[]).length) sec("takeaways","Key takeaways",`<div class="tk" id="tk"><div class="tklock"><p>Write your explanation in step ${secs.findIndex(s=>s.id==="explain")+1} first. Comparing your own words with these is where it sticks.</p><button type="button" class="btn ghost sm" id="tkshow">Show them now</button></div><ul class="tklist">${l.takeaways.map(t=>`<li>${md(t)}</li>`).join("")}</ul></div>`);
  el.innerHTML = `
  <nav class="crumbs"><button data-act="map" data-stage-go="${m.si}">Stage ${m.si}: ${esc(meta.name)}</button><span>›</span><span>${esc(m.title)}</span><span>›</span><span>Day ${idx+1}</span></nav>
  <div class="lesson">
    <article>
      <header style="display:grid;gap:10px"><span class="eyebrow">Day ${idx+1} of ${m.lessons.length} · ~${l.minutes||60} min</span><h1 class="h1">${esc(l.title)}</h1>
      <div class="objective"><span class="eyebrow">Objective</span>${md(l.objective)}</div>
      ${l.why?`<p class="why"><b>Why it matters.</b> ${md(l.why)}</p>`:""}</header>
      ${warm?`<section class="sec warm" id="sec-warm"><h3>Warm-up · guess first</h3><p class="muted" style="margin:0;font-size:.9rem">Answer before you read. Guessing first makes the lesson stick better, even when the guess is wrong. It doesn't touch your review deck.</p><div id="wq"></div></section>`:""}
      ${secs.map((s,i)=>`<section class="sec" id="sec-${s.id}"><h3>${i+1} · ${esc(s.title)}</h3>${s.html}</section>`).join("")}
      <div class="row" id="lfoot" style="justify-content:space-between;border-top:1px solid var(--line);padding-top:18px">
        ${prev?`<button class="btn" data-lesson="${prev.id}">← ${esc(prev.title)}</button>`:"<span></span>"}
        <span class="row" id="lcomplete"></span>
      </div>
      ${l.resource?.url?`<p class="muted" style="margin:0;font-size:.9rem">Go deeper: <a href="${esc(l.resource.url)}" target="_blank" rel="noopener">${esc(l.resource.title||l.resource.url)}</a></p>`:""}
    </article>
    <aside><nav class="onpage" aria-label="On this page"><span class="eyebrow">On this page</span>${warm?`<button type="button" data-jump="warm"><span>0</span>Warm-up</button>`:""}${secs.map((s,i)=>`<button type="button" data-jump="${s.id}"><span>${i+1}</span>${esc(s.title)}</button>`).join("")}</nav>
      <span class="eyebrow">${esc(m.title)}</span><ul class="toc">${m.lessons.map((x,i)=>`<li class="${P.lessons[x.id]?"done":""}"><button data-lesson="${x.id}" aria-current="${x.id===l.id}"><span class="ck">${P.lessons[x.id]?"✓":i+1}</span><span>${esc(x.title)}</span></button></li>`).join("")}
      <li><button data-exam="${m.id}"><span class="ck">★</span><span>Module exam${passed(m)?" · passed":""}</span></button></li></ul>
      <section class="tutor" id="tutor" hidden><span class="eyebrow">Hint tutor</span><p class="muted" style="margin:0;font-size:.84rem">Stuck? Describe what you tried. You get a hint or a question back, never the full answer.</p><textarea id="tq" class="explain" style="min-height:70px" maxlength="1200" placeholder="I tried… and got…"></textarea><button class="btn" id="tbtn">Get a hint</button><div id="tout" class="tout"></div></section></aside>
  </div>`;
  bindVisuals(el); bindVideos(el);
  el.querySelector(".onpage").addEventListener("click",e=>{ const b=e.target.closest("[data-jump]"); if(b) document.getElementById("sec-"+b.dataset.jump)?.scrollIntoView({behavior:"smooth", block:"start"}); });
  if(exLang) mountEditor($("#ex-ed"), {lang:exLang, code:l.example.code, label:"Worked example"});
  lessonScratch = tryLang ? mountEditor($("#try-ed"), {lang:tryLang, code:STARTER[tryLang](l), draftKey:l.id, label:"Your scratchpad"}) : null;
  bindTutor(l, m);
  el.querySelectorAll("textarea[data-note]").forEach(t=>{ let tm; t.addEventListener("input",()=>{ clearTimeout(tm); tm=setTimeout(()=>{ P.notes[t.dataset.note]=t.value.slice(0,+t.maxLength||600); save("p",true); },900); }); });
  const tk=$("#tk"), openTk=()=>tk?.classList.add("open");
  if((P.notes[l.id]||"").trim().length>=40 || P.lessons[l.id]) openTk();
  $("#tkshow")?.addEventListener("click",openTk);
  const ta=$("#note-"+l.id); let nt; ta.addEventListener("input",()=>{ if(ta.value.trim().length>=40) openTk(); clearTimeout(nt); nt=setTimeout(()=>{ P.notes[l.id]=ta.value.slice(0,1500); save("p"); },900); });
  const showComplete = (ready)=>{
    const done=!!P.lessons[l.id];
    $("#lcomplete").innerHTML = done
      ? `<span class="pill ok">Completed</span>${next?`<button class="btn primary" data-lesson="${next.id}">Next: ${esc(next.title)} →</button>`:`<button class="btn exam" data-exam="${m.id}">Take the module exam →</button>`}`
      : `<button class="btn primary" id="completeBtn" ${ready?"":"disabled"} title="${ready?"":"Answer the questions first"}">Complete lesson</button>`;
    const cb=$("#completeBtn"); if(cb) cb.onclick=()=>{ P.lessons[l.id]=today(); logActivity(2); save("p"); showComplete(true); openTk(); const li=el.querySelector(`.toc [data-lesson="${l.id}"]`); if(li){ li.parentElement.classList.add("done"); li.querySelector(".ck").textContent="✓"; } updateBadge(); };
  };
  showComplete(!!P.lessons[l.id]);
  if(warm) quiz($("#wq"), [D.q[warm.id]], {mode:"pretest", confidence:false, finishLabel:"Start the lesson ↓", onFinish:()=>{
    $("#wq").innerHTML=`<p class="muted" style="margin:0">Keep that answer in mind. The lesson explains it, and the question comes back in step ${secs.findIndex(s=>s.id==="check")+1}.</p>`;
    document.getElementById("sec-learn")?.scrollIntoView({behavior:"smooth", block:"start"}); }});
  quiz($("#lq"), l.questions.map(q=>D.q[q.id]), {mode:"lesson", onAnswer:(q,ok,conf)=>srs(q.id,ok,conf), onFinish:()=>showComplete(true), compactResult:true});
}
/* Videos load only when played (a click-to-play facade): no YouTube requests or cookies until then, and the page stays fast. */
const ytSearch = l => "https://www.youtube.com/results?search_query="+encodeURIComponent(l.title+" explained");
function videoBlock(l){
  if(!l.video) return `<div class="vidnone"><p>No hand-picked video for this lesson yet. A short one helps: watch at most 10 minutes, then come back and do the steps below.</p><a class="btn ghost sm" href="${esc(ytSearch(l))}" target="_blank" rel="noopener">Search YouTube for “${esc(l.title)}”</a></div>`;
  const id=esc(l.video.id);
  return `<div class="vid" data-vid="${id}" data-title="${esc(l.video.title)}"><button type="button" class="vidplay" aria-label="Play video: ${esc(l.video.title)}"><img src="https://i.ytimg.com/vi/${id}/hqdefault.jpg" alt="" loading="lazy" referrerpolicy="no-referrer"><span class="pb" aria-hidden="true"></span></button></div>
    <p class="vidmeta"><span><b>${esc(l.video.title)}</b></span><span class="muted"><a href="https://www.youtube.com/watch?v=${id}" target="_blank" rel="noopener">Open on YouTube</a> · <a href="${esc(ytSearch(l))}" target="_blank" rel="noopener">Find another</a></span></p>
    <p class="muted" style="margin:0;font-size:.85rem">Watch actively: pause when a new idea appears and say it out loud. Long video? Watch the part that covers the objective and skip the rest.</p>`;
}
function bindVideos(root){
  root.querySelectorAll(".vid").forEach(v=>v.querySelector(".vidplay")?.addEventListener("click",()=>{
    const f=document.createElement("iframe");
    f.src=`https://www.youtube-nocookie.com/embed/${encodeURIComponent(v.dataset.vid)}?autoplay=1&rel=0`;
    f.title=v.dataset.title||"Video"; f.allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"; f.allowFullscreen=true; f.referrerPolicy="strict-origin-when-cross-origin";
    v.replaceChildren(f); v.classList.add("on");
  }));
}
function codeBlock(code, cur){ return `<pre class="code">${String(code||"").split("\n").map((ln,i)=>`<span class="l ${cur===i+1?"cur":""}">${esc(ln)||" "}</span>`).join("")}</pre>`; }
function visual(v){
  const h = v.title?`<h4>${esc(v.title)}</h4>`:"";
  if(v.type==="steps") return `<div class="vis">${h}<ol class="flow">${(v.steps||[]).map((s,i)=>`<li><span class="sn">${i+1}${i<v.steps.length-1?" →":""}</span><b>${md(s.label)}</b><span>${md(s.detail)}</span></li>`).join("")}</ol></div>`;
  if(v.type==="compare") return `<div class="vis">${h}<div class="cmp">${[v.left,v.right].map(c=>`<div><h5>${md(c?.title)}</h5><ul>${(c?.points||[]).map(p=>`<li>${md(p)}</li>`).join("")}</ul></div>`).join("")}</div></div>`;
  if(v.type==="table") return `<div class="vis">${h}<div class="tbl"><table><thead><tr>${(v.headers||[]).map(x=>`<th>${md(x)}</th>`).join("")}</tr></thead><tbody>${(v.rows||[]).map(r=>`<tr>${r.map(c=>`<td>${md(c)}</td>`).join("")}</tr>`).join("")}</tbody></table></div></div>`;
  if(v.type==="boxes") return `<div class="vis">${h}<div class="bx">${(v.items||[]).map(it=>`<div><b>${md(it.label)}</b><span>${md(it.detail)}</span></div>`).join("")}</div></div>`;
  if(v.type==="trace") return `<div class="vis">${h}<div class="trace" data-trace='${esc(JSON.stringify(v))}'></div></div>`;
  return "";
}
function bindVisuals(root){
  root.querySelectorAll("[data-trace]").forEach(box=>{
    const v=JSON.parse(box.dataset.trace); let i=-1;
    const draw=()=>{
      const s=v.steps[i]||{line:0,vars:{},out:""}, p=v.steps[i-1]||{vars:{}};
      const vars=Object.entries(s.vars||{});
      box.innerHTML = `<div>${codeBlock(v.code, s.line)}</div>
        <div class="side"><div class="box"><span class="eyebrow">Variables</span>${vars.length?`<div class="vars">${vars.map(([k,val])=>`<span class="${p.vars?.[k]!==val?"ch":""}">${esc(k)}</span><span class="${p.vars?.[k]!==val?"ch":""}">${esc(val)}</span>`).join("")}</div>`:`<span class="muted" style="font-size:.85rem">${i<0?"Press Step to run the first line.":"(none yet)"}</span>`}</div>
        <div class="box"><span class="eyebrow">Output</span><pre class="out">${esc(s.out||"")}</pre></div></div>
        <div class="ctl"><button class="btn" data-t="prev" ${i<0?"disabled":""}>◀ Back</button><button class="btn primary" data-t="next" ${i>=v.steps.length-1?"disabled":""}>Step ▶</button><button class="btn ghost" data-t="reset">Reset</button><span class="pos">${i<0?"not started":`step ${i+1} / ${v.steps.length} · line ${s.line}`}</span></div>`;
    };
    box.addEventListener("click",e=>{ const b=e.target.closest("[data-t]"); if(!b) return; const t=b.dataset.t;
      if(t==="next") i=Math.min(v.steps.length-1,i+1); else if(t==="prev") i=Math.max(-1,i-1); else i=-1; draw(); box.querySelector(`[data-t="${t}"]`)?.focus(); });
    draw();
  });
}


/* ---------- hint tutor (hints, never solutions: see Method → AI) ---------- */
let samplerP=null;
function bindTutor(l, m){
  samplerP = samplerP || (window.claude?.use?.("sample") ?? Promise.resolve(null));
  samplerP.then(sample=>{
    const box=document.getElementById("tutor"); if(!sample||!box||route.id!==l.id) return; box.hidden=false;
    const btn=box.querySelector("#tbtn"), out=box.querySelector("#tout"), tq=box.querySelector("#tq"); let ctl=null;
    btn.onclick=async()=>{
      const ask=tq.value.trim(); if(!ask){ tq.focus(); return; }
      ctl?.abort(); ctl=new AbortController(); btn.disabled=true; out.textContent="Thinking…";
      const prompt=`You are a programming tutor using the Socratic method. The learner is on a lesson in a self-study curriculum.
Lesson: "${l.title}" (module "${m.title}", stage "${META[m.si].name}").
Objective: ${l.objective}
Exercise they are doing: ${l.tryit}

Rules: NEVER give the full solution or write the complete code for them. Give ONE small hint, or ask ONE guiding question, or point to the exact concept or line to look at. You may show at most 2 lines of illustrative code that are not the answer. If they share code, point out where the problem is, not how to fix it entirely. Keep it under 90 words. Plain text, no markdown headings.

${lessonScratch&&lessonScratch.value.trim()?`Their current code in the lesson scratchpad:\n${lessonScratch.value.slice(0,3000)}\n\n`:""}Learner says: ${ask}`;
      try{ const r=await sample(prompt,{signal:ctl.signal, cache:false, modelTier:"quick", onText:({text})=>{ out.textContent=text; }}); out.textContent=r.text; }
      catch(e){ out.textContent = e?.code==="rate_limited" ? "Too many hints in a row. Wait a minute and try again." : e?.code==="not_granted" ? "The tutor needs permission to answer. Allow it from the artifact's Permissions menu." : "The tutor couldn't answer just now. Try again in a moment."; }
      finally{ btn.disabled=false; }
    };
  });
}

/* ================= QUIZ ENGINE ================= */
function norm(s){ return String(s??"").replace(/\r/g,"").split("\n").map(x=>x.replace(/\s+$/,"")).join("\n").trim(); }
// Each answer is checked with a confidence rating (CONF) unless opt.confidence is false, as in the lesson warm-up.
function quiz(el, qs, opt){
  qs=qs.filter(Boolean); let i=0; const res=[]; const rated = opt.confidence!==false;
  if(!qs.length){ el.innerHTML=`<div class="empty">No questions here yet.</div>`; opt.onFinish?.(1,[]); return; }
  const step=()=>{
    const q=qs[i]; let answered=false, choice=null, order=null;
    const dots=qs.map((_,k)=>`<i class="${k<res.length?(res[k].ok?"r":"w"):k===i?"cur":""}"></i>`).join("");
    let input="";
    const perm = q.type==="mcq" ? shuffle(q.options.map((_,k)=>k)) : null;
    if(q.type==="mcq") input=`<div class="opts">${perm.map((ok,k)=>`<button type="button" class="opt" data-o="${ok}" aria-pressed="false"><span class="k">${"ABCDEF"[k]}</span><span>${md(q.options[ok])}</span></button>`).join("")}</div>`;
    else if(q.type==="predict"){ const multi=String(q.answer).includes("\n"); input = multi?`<textarea class="pred" id="pred" rows="4" placeholder="Type the exact output"></textarea>`:`<input class="pred" id="pred" autocomplete="off" spellcheck="false" placeholder="Type the exact output, then press Enter">`; }
    else if(q.type==="parsons"){ order=shuffle(q.lines.map((_,k)=>k)); if(order.every((v,k)=>v===k)&&order.length>1) order.reverse(); input=`<ol class="pars" id="pars"></ol><p class="muted" style="margin:0;font-size:.82rem">Tap a line, then tap another to swap them, or use the arrows.</p>`; }
    el.innerHTML = `<div class="quiz">
      <div class="qhead"><span class="row"><span class="lv lv${q.level}">L${q.level} · ${LEVELS[q.level]?.name||""}</span><span class="eyebrow">Question ${i+1} of ${qs.length}</span></span><span class="dots">${dots}</span></div>
      <p class="qprompt">${md(q.prompt)}</p>
      ${q.code?codeBlock(q.code):""}
      ${input}
      <div id="fb"></div>
      <div class="row qact">${rated?`<div class="conf" role="group" aria-label="Check your answer: how sure are you?"><span class="cl">Check · how sure are you?</span>${CONF.map(c=>`<button type="button" class="btn sm${c.k==="sure"?" primary":""}" data-conf="${c.k}" ${q.type==="mcq"?"disabled":""}>${c.label}</button>`).join("")}</div>`:""}<button class="btn primary" id="qcheck" ${rated?"hidden":""} ${!rated&&q.type==="mcq"?"disabled":""}>Check</button><span class="muted" style="font-size:.82rem">${opt.mode==="exam"?"Answer from memory. No notes.":""}</span></div>
    </div>`;
    const check=el.querySelector("#qcheck"), confs=[...el.querySelectorAll("[data-conf]")];
    const ready=()=>{ check.disabled=false; confs.forEach(b=>b.disabled=false); };
    if(q.type==="mcq") el.querySelectorAll(".opt").forEach(b=>b.onclick=()=>{ if(answered) return; choice=+b.dataset.o; el.querySelectorAll(".opt").forEach(x=>x.setAttribute("aria-pressed", x===b)); ready(); });
    if(q.type==="predict"){ const inp=el.querySelector("#pred"); inp.focus({preventScroll:true}); inp.addEventListener("keydown",e=>{ if(e.key==="Enter"&&inp.tagName==="INPUT"){ e.preventDefault(); if(rated) confs[1].focus(); else check.click(); } }); }
    let sel=null;
    const drawP=()=>{ const ol=el.querySelector("#pars"); ol.innerHTML=order.map((k,pos)=>`<li data-p="${pos}" class="${sel===pos?"sel":""}"><pre>${esc(q.lines[k])}</pre><span class="mv"><button type="button" data-mv="-1" aria-label="Move up">↑</button><button type="button" data-mv="1" aria-label="Move down">↓</button></span></li>`).join(""); };
    if(q.type==="parsons"){ drawP(); el.querySelector("#pars").addEventListener("click",e=>{ if(answered) return; const li=e.target.closest("li"); if(!li) return; const pos=+li.dataset.p; const mv=e.target.closest("[data-mv]");
      if(mv){ const to=pos+(+mv.dataset.mv); if(to>=0&&to<order.length){ [order[pos],order[to]]=[order[to],order[pos]]; } sel=null; }
      else if(sel===null) sel=pos; else { [order[pos],order[sel]]=[order[sel],order[pos]]; sel=null; }
      drawP(); }); }
    confs.forEach(b=>b.onclick=()=>grade(b.dataset.conf));
    check.onclick=()=>{ if(answered){ i++; if(i<qs.length) step(); else finish(); return; } grade(null); };
    const grade=conf=>{
      if(answered) return;
      let ok=false, right="";
      if(q.type==="mcq"){ if(choice==null) return; ok=choice===q.answer; el.querySelectorAll(".opt").forEach(b=>{ const k=+b.dataset.o; b.disabled=true; if(k===q.answer) b.classList.add("right"); else if(k===choice) b.classList.add("wrong"); }); }
      else if(q.type==="predict"){ const inp=el.querySelector("#pred"); const v=norm(inp.value); if(!v){ inp.focus(); return; } ok=[q.answer,...(q.accept||[])].some(a=>norm(a)===v); inp.readOnly=true; right=`<pre>${esc(q.answer)}</pre>`; }
      else if(q.type==="parsons"){ ok=order.every((k,pos)=>q.lines[k]===q.lines[pos]); el.querySelector("#pars").classList.add(ok?"right":"wrong"); right=ok?"":`<pre>${esc(q.lines.join("\n"))}</pre>`; }
      answered=true; res.push({q,ok,conf}); opt.onAnswer?.(q,ok,conf);
      // Confident errors are the ones people correct best once they see why (the hypercorrection effect), so say so;
      // a lucky guess is flagged so it isn't mistaken for knowing.
      const note = ok ? (conf==="guess"?"Right, but you were guessing, so this one comes back tomorrow instead of moving up a box.":"")
        : conf==="sure" ? "You were certain and it was wrong. Misses like this are the easiest to fix for good, so read why before moving on."
        : conf==="guess" ? "A wrong guess still helps: now you know exactly what to look for." : "";
      confs.forEach(b=>{ b.disabled=true; b.classList.toggle("on", b.dataset.conf===conf); });
      el.querySelector(".conf")?.classList.add("done"); check.hidden=false;
      el.querySelector("#fb").innerHTML=`<div class="fb ${ok?"r":"w"}"><b>${ok?(conf==="guess"?"Correct, by a guess":"Correct"):"Not quite"}</b>${note?`<p class="cn">${note}</p>`:""}${!ok&&right?`<span class="eyebrow">Correct answer</span>${right}`:""}<p>${md(q.explain)}</p>${q.code&&qLang(q)?`<button type="button" class="btn ghost sm" data-runq style="justify-self:start">Run this code ▶</button>`:""}</div>`;
      const rq=el.querySelector("[data-runq]"); if(rq) rq.onclick=()=>runSnippet(rq, q.code, qLang(q));
      check.textContent = i<qs.length-1 ? "Next question →" : (opt.finishLabel || (opt.mode==="exam"?"See result":"Finish")); check.disabled=false; check.focus({preventScroll:true});
      el.querySelectorAll(".dots i")[i].className = ok?"r":"w";
    };
  };
  const finish=()=>{
    const sc=res.filter(r=>r.ok).length/res.length;
    if(opt.compactResult){ el.innerHTML=`<div class="quiz"><div class="row" style="justify-content:space-between"><b class="h2">${res.filter(r=>r.ok).length} / ${res.length} correct</b><button class="btn ghost" id="again">Try again</button></div><p class="muted" style="margin:0">Every question is now in your review deck and will come back on a spaced schedule. ${sc<1?"The ones you missed return tomorrow.":""}</p></div>`; el.querySelector("#again").onclick=()=>quiz(el, shuffle(qs), opt); }
    opt.onFinish?.(sc,res);
  };
  step();
}
function ring(p, pass){ const r=50,c=2*Math.PI*r; return `<svg class="ring" viewBox="0 0 120 120" role="img" aria-label="${Math.round(p*100)} percent"><circle cx="60" cy="60" r="${r}" fill="none" stroke="var(--sunk)" stroke-width="10"/><circle cx="60" cy="60" r="${r}" fill="none" stroke="${pass?"var(--ok)":"var(--bad)"}" stroke-width="10" stroke-linecap="round" stroke-dasharray="${c*p} ${c}" transform="rotate(-90 60 60)"/><text x="60" y="67" text-anchor="middle" style="font:700 22px var(--display);fill:var(--ink)">${Math.round(p*100)}%</text></svg>`; }
function resultList(res){ const wrong=res.filter(r=>!r.ok); if(!wrong.length) return ""; return `<div class="panel" style="width:100%"><span class="eyebrow">Review these</span>${wrong.map(r=>{const l=r.q.lid&&D.lessons[r.q.lid]; return `<div style="display:grid;gap:4px;border-top:1px solid var(--line);padding-top:10px"><span>${md(r.q.prompt)}</span><span class="muted" style="font-size:.88rem">${md(r.q.explain)}</span>${l?`<button class="btn ghost" style="justify-self:start" data-lesson="${l.id}">Re-read: ${esc(l.title)}</button>`:""}</div>`}).join("")}</div>`; }

/* ================= EXAM ================= */
function examQuestions(m){
  const own=(m.exam||[]).map(q=>D.q[q.id]);
  const fromLessons=pick(m.lessons.flatMap(l=>l.questions).filter(q=>q.level>=2).map(q=>D.q[q.id]), 4);
  const earlier=D.mods.slice(Math.max(0,m.gi-4), m.gi).flatMap(x=>x.exam||[]).map(q=>D.q[q.id]);
  return shuffle([...own, ...fromLessons, ...pick(earlier, earlier.length?2:0)]);
}
function viewExam(el){
  const m=D.modById[route.id]; if(!m){ go({v:"map"}); return; }
  const testOut = lessonsDone(m)<m.lessons.length && !passed(m);
  if(!route.started){
    el.innerHTML = `<nav class="crumbs"><button data-act="map" data-stage-go="${m.si}">Stage ${m.si}: ${esc(META[m.si].name)}</button><span>›</span><span>${esc(m.title)}</span></nav>
    <section class="panel" style="max-width:720px;gap:16px"><span class="eyebrow" style="color:var(--summit)">${testOut?"Test out":"Module exam"}</span><h1 class="h1">${esc(m.title)}</h1>
    <p class="lede">${testOut?`Pass at ${PASS*100}% and this module counts as done, so you can skip ahead. Fail and you'll know exactly which lessons to study.`:`Questions are mixed across the module, with a couple from earlier modules. Mixing topics feels harder and makes the skill stick. Pass at ${PASS*100}% to unlock the next module.`}</p>
    <div class="facts"><span class="pill exam">${examQuestions(m).length} questions</span><span class="pill">Mostly Apply & Analyze</span>${P.exams[m.id]?`<span class="pill">Best so far ${Math.round(P.exams[m.id].best*100)}%</span>`:""}</div>
    <div class="row"><button class="btn exam" id="go">Start exam</button><button class="btn ghost" data-act="map" data-stage-go="${m.si}">Not yet</button></div></section>`;
    $("#go").onclick=()=>{ route.started=true; render(); };
    return;
  }
  el.innerHTML = `<nav class="crumbs"><span>${esc(m.title)}</span><span>›</span><span>Exam</span></nav><div id="ex" style="max-width:820px"></div>`;
  quiz($("#ex"), examQuestions(m), {mode:"exam", onAnswer:(q,ok,conf)=>srs(q.id,ok,conf), onFinish:(sc,res)=>{
    const prev=P.exams[m.id]; P.exams[m.id]={best:Math.max(sc,prev?.best||0), last:today(), n:(prev?.n||0)+1}; logActivity(3); save("p");
    const pass=sc>=PASS; let nm=D.mods[m.gi+1]; if(pass) UI.confetti(); if(isTrack(m)) nm=D.mods.find(x=>x.sid==="s8");
    $("#ex").innerHTML=`<div class="result"><div class="row" style="gap:24px">${ring(sc,pass)}<div style="display:grid;gap:6px"><span class="eyebrow">${pass?"Passed":"Not yet"}</span><h2 class="h2">${pass?(nm?`Unlocked: ${esc(nm.title)}`:"You've passed the final module."):`You need ${PASS*100}%. Study the misses below, then retake.`}</h2><p class="muted" style="margin:0">${res.filter(r=>r.ok).length} of ${res.length} correct. Every question is now in your review deck.</p></div></div>
      <div class="row">${pass&&nm?`<button class="btn primary" data-act="map" data-stage-go="${nm.si}">Go to ${esc(nm.title)}</button>`:`<button class="btn exam" data-exam="${m.id}">Retake exam</button>`}<button class="btn ghost" data-act="map" data-stage-go="${m.si}">Back to map</button></div>
      ${resultList(res)}</div>`;
  }});
}

/* ================= REVIEW ================= */
function viewReview(el){
  const due=dueCards();
  if(!route.started){
    const total=Object.keys(S.cards).length, boxes=Array(INTERVALS.length).fill(0); Object.values(S.cards).forEach(c=>boxes[c.b]++);
    const mx=Math.max(1,...boxes);
    el.innerHTML = `<section style="display:grid;gap:10px"><span class="eyebrow">Spaced repetition</span><h1 class="h1">${due.length?`${due.length} card${due.length>1?"s":""} due`:"All caught up"}</h1>
      <p class="lede">Each card comes back just before you'd forget it. Get it right and the gap grows (${INTERVALS.join(" → ")} days). Miss it and it resets to tomorrow. Topics are shuffled together on purpose.</p></section>
      <div class="row">${due.length?`<button class="btn primary" id="go">Review ${Math.min(due.length,25)} now</button>`:`<button class="btn" data-act="map">Learn something new</button>`}<button class="btn ghost" data-act="practice">Practise by level instead</button></div>
      <section class="panel"><h2 class="h2">Your deck by box</h2>${total?`<div class="intervals">${boxes.map((n,k)=>`<div data-tip="Box ${k+1}: ${n} cards, next gap ${INTERVALS[k]} days"><span>${n}</span><i style="height:${8+100*n/mx}px"></i><span>${INTERVALS[k]}d</span></div>`).join("")}</div><p class="muted" style="margin:0;font-size:.85rem">${total} cards. Cards move right as you remember them for longer.</p>`:`<div class="empty">No cards yet. Finish a lesson's questions and they'll start appearing here.</div>`}</section>`;
    const g=$("#go"); if(g) g.onclick=()=>{ route.started=true; route.ids=shuffle(due).slice(0,25); render(); };
    return;
  }
  el.innerHTML=`<div id="rv" style="max-width:820px"></div>`;
  const qs=route.ids.map(id=>D.q[id]); const missed=[];
  quiz($("#rv"), qs, {mode:"review", onAnswer:(q,ok,conf)=>{ srs(q.id,ok,conf); if(!ok) missed.push(q); }, onFinish:(sc,res)=>{
    $("#rv").innerHTML=`<div class="result"><div class="row" style="gap:24px">${ring(sc,sc>=PASS)}<div style="display:grid;gap:6px"><span class="eyebrow">Review done</span><h2 class="h2">${res.filter(r=>r.ok).length} of ${res.length} remembered</h2><p class="muted" style="margin:0">${missed.length?`${missed.length} card${missed.length>1?"s":""} reset to tomorrow.`:"Every card moved to a longer interval."}</p></div></div>
    <div class="row">${dueCards().length?`<button class="btn primary" data-act="review">Keep going (${dueCards().length} left)</button>`:""}<button class="btn ghost" data-act="today">Back to today</button></div>${resultList(res)}</div>`;
  }});
}

/* ================= PRACTICE ================= */
function viewPractice(el){
  if(practiceStage==null){ const cm=currentModule(); practiceStage=cm?cm.si:0; }
  if(route.started){
    el.innerHTML=`<div id="pq" style="max-width:820px"></div>`;
    quiz($("#pq"), route.qs, {mode:"practice", onAnswer:(q,ok,conf)=>srs(q.id,ok,conf), onFinish:(sc,res)=>{
      $("#pq").innerHTML=`<div class="result"><div class="row" style="gap:24px">${ring(sc,sc>=PASS)}<div style="display:grid;gap:6px"><span class="eyebrow">Level ${route.level} · ${LEVELS[route.level].name}</span><h2 class="h2">${sc>=PASS?(route.level<3?"Strong. Try the next level up.":"Excellent analysis."):"Keep practising at this level."}</h2></div></div>
      <div class="row"><button class="btn primary" id="again">Another set</button>${sc>=PASS&&route.level<3?`<button class="btn" id="up">Level ${route.level+1}</button>`:""}<button class="btn ghost" data-act="practice">Change stage or level</button></div>${resultList(res)}</div>`;
      $("#again").onclick=()=>startPractice(route.level); const up=$("#up"); if(up) up.onclick=()=>startPractice(route.level+1);
    }});
    return;
  }
  const sid=META[practiceStage].id, pool=Object.values(D.q).filter(q=>q.sid===sid);
  const learned=new Set(Object.keys(P.lessons)); const scope=route.scope||"learned";
  const inScope=q=> scope==="all" || (q.lid?learned.has(q.lid):passed(D.modById[q.mid]));
  el.innerHTML=`<section style="display:grid;gap:10px"><span class="eyebrow">Level-based practice</span><h1 class="h1">Practice</h1><p class="lede">Pick a stage and a level. Ten mixed questions each time. Every answer feeds your review deck.</p></section>
    <section class="panel"><span class="eyebrow">Stage</span><div class="chips">${META.map((s,i)=>`<button type="button" class="chip" data-pstage="${i}" aria-pressed="${i===practiceStage}">${i}. ${esc(s.name)}</button>`).join("")}</div>
    <span class="eyebrow">Questions from</span><div class="chips"><button type="button" class="chip" data-scope="learned" aria-pressed="${scope==="learned"}">Lessons I've finished</button><button type="button" class="chip" data-scope="all" aria-pressed="${scope==="all"}">Whole stage (preview)</button></div></section>
    <div class="levels">${[1,2,3].map(lv=>{ const n=pool.filter(q=>q.level===lv&&inScope(q)).length; return `<button type="button" class="lvcard" data-level="${lv}" ${n?"":"disabled style='opacity:.5;cursor:default'"}><span class="lv lv${lv}" style="justify-self:start">Level ${lv}</span><b>${LEVELS[lv].name}</b><span>${LEVELS[lv].desc}</span><span class="n">${n} question${n===1?"":"s"} available</span></button>`; }).join("")}</div>
    ${scope==="learned"&&!pool.some(inScope)?`<div class="empty">Finish a lesson in this stage to unlock its questions, or switch to “Whole stage” to preview.</div>`:""}`;
  el.querySelectorAll("[data-pstage]").forEach(b=>b.onclick=()=>{ practiceStage=+b.dataset.pstage; render(); });
  el.querySelectorAll("[data-scope]").forEach(b=>b.onclick=()=>{ route.scope=b.dataset.scope; render(); });
  el.querySelectorAll("[data-level]").forEach(b=>b.onclick=()=>{ if(!b.disabled) startPractice(+b.dataset.level); });
  function startPractice(lv){ const qs=pick(pool.filter(q=>q.level===lv&&inScope(q)),10); if(!qs.length) return; go({v:"practice", started:true, level:lv, qs, scope}); }
}

/* ================= PROJECTS ================= */
function viewProjects(el){
  const cm=currentModule();
  const groups=META.map((s,i)=>{ const ms=D.mods.filter(m=>m.sid===s.id&&m.project); if(!ms.length) return "";
    return `<section style="display:grid;gap:14px"><h2 class="h2">Stage ${i}: ${esc(s.name)}</h2><div class="projs">${ms.map(m=>{ const n=msDone(m), t=m.project.milestones.length; const st=n===t?"ok":n?"acc":"";
      return `<article class="panel proj-card" ${cm&&cm.id===m.id?'style="border-color:var(--accent)"':""}><div class="row" style="justify-content:space-between"><span class="eyebrow">${esc(m.title)}</span><span class="pill ${st}">${n===t?"Done":n?`${n}/${t}`:"Not started"}</span></div>
        <h4>${esc(m.project.title)}</h4><p>${md(m.project.brief)}</p>
        <ul class="ms">${m.project.milestones.map((x,k)=>`<li><label><input type="checkbox" id="ms-${m.id}-${k}" data-ms="${m.id}:${k}" ${P.ms[m.id+":"+k]?"checked":""}><span>${md(x)}</span></label></li>`).join("")}</ul>
        ${m.project.stretch?`<p class="stretch"><b>Stretch:</b> ${md(m.project.stretch)}</p>`:""}</article>`; }).join("")}</div></section>`; }).join("");
  el.innerHTML=`<section style="display:grid;gap:10px"><span class="eyebrow">Learn by building</span><h1 class="h1">Projects</h1><p class="lede">Every module ends in a project that uses what you just learned. Do them on Tuesdays and Thursdays, your long days. Tick milestones as you go; push each one to GitHub.</p></section>${groups}`;
  el.querySelectorAll("[data-ms]").forEach(cb=>cb.onchange=()=>{ if(cb.checked){ P.ms[cb.dataset.ms]=today(); logActivity(); } else delete P.ms[cb.dataset.ms]; save("p");
    const card=cb.closest(".proj-card"), m=D.modById[cb.dataset.ms.split(":")[0]], n=msDone(m), t=m.project.milestones.length, pill=card.querySelector(".pill");
    pill.className="pill "+(n===t?"ok":n?"acc":""); pill.textContent=n===t?"Done":n?`${n}/${t}`:"Not started"; });
}

/* ================= METHOD ================= */
function viewMethod(el){
  const r=D.research;
  const fallback=`<div class="empty">The research summary didn't load. Reload to try again.</div>`;
  el.innerHTML = `<section style="display:grid;gap:10px"><span class="eyebrow">The science behind the plan</span><h1 class="h1">How to learn fastest</h1><p class="lede">${r?md(r.summary):""}</p></section>
  ${!r?fallback:`
  <section style="display:grid;gap:14px"><h2 class="h2">The protocol</h2><ol class="protocol">${(r.protocol||[]).map(s=>`<li><b>${md(s.step)}</b><span>${md(s.detail)}</span></li>`).join("")}</ol></section>
  <section style="display:grid;gap:14px"><h2 class="h2">How this app applies it</h2>
    <div class="tbl"><table><thead><tr><th>Feature</th><th>Principle</th><th>What it does</th></tr></thead><tbody>
      <tr><td>Daily lessons</td><td>Worked examples, small steps</td><td>One objective a day; see a solved example before you solve one yourself</td></tr>
      <tr><td>Warm-up question</td><td>Pretesting</td><td>You guess one question before reading; the attempt tells you what to look for</td></tr>
      <tr><td>Watch, then recall</td><td>Short videos, interpolated testing</td><td>A hand-picked short video, then you write its key idea without rewinding</td></tr>
      <tr><td>Predict first</td><td>PRIMM</td><td>You write the expected output before running the worked example, then change it and predict again</td></tr>
      <tr><td>Common mistakes</td><td>Refutation</td><td>Each classic misconception is stated, then corrected with the reason</td></tr>
      <tr><td>Check yourself</td><td>Retrieval practice</td><td>Every lesson ends with recall, apply and analyze questions</td></tr>
      <tr><td>How sure are you?</td><td>Metacognition, hypercorrection</td><td>Confident misses are flagged; lucky guesses come back tomorrow instead of moving up; your profile shows your calibration</td></tr>
      <tr><td>Explain it back</td><td>Self-explanation, generation</td><td>You write the idea in your own words, then compare with the key takeaways</td></tr>
      <tr><td>Review deck</td><td>Spacing</td><td>Every question returns on expanding intervals</td></tr>
      <tr><td>Module exams</td><td>Mastery learning, interleaving</td><td>${PASS*100}% to move on; mixed topics including earlier modules</td></tr>
      <tr><td>Test out</td><td>Expertise reversal</td><td>Skip what you already know; time goes to what's new</td></tr>
      <tr><td>Projects</td><td>Deliberate practice, transfer</td><td>Real builds at the edge of your ability, on your long days</td></tr>
    </tbody></table></div></section>
  <section style="display:grid;gap:14px"><h2 class="h2">The evidence</h2><div class="principles">${(r.principles||[]).map(p=>`<article class="panel pr"><div class="row" style="justify-content:space-between"><h4>${md(p.name)}</h4><span class="pill str-${esc(p.strength)}">${esc(p.strength)} evidence</span></div><p><b>${md(p.claim)}</b></p><p class="muted">${md(p.evidence)}</p><p class="ap">${md(p.howToApply)}</p><div class="src">${(p.sources||[]).map(s=>`<a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.label)}</a>`).join("")}</div></article>`).join("")}</div></section>
  ${r.ai?`<section class="panel"><h2 class="h2">Using AI while you learn</h2><p style="margin:0;max-width:70ch">${md(r.ai.guidance)}</p><div class="src">${(r.ai.sources||[]).map(s=>`<a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.label)}</a>`).join("")}</div></section>`:""}
  ${r.spacing?`<section class="panel"><h2 class="h2">Why these review intervals</h2><p style="margin:0;max-width:70ch">${md(r.spacing.rationale)}</p><div class="intervals">${INTERVALS.map(d=>`<div><i style="height:${10+Math.sqrt(d)*8}px"></i><span>${d}d</span></div>`).join("")}</div></section>`:""}
  ${(r.frameworks||[]).length?`<section style="display:grid;gap:14px"><h2 class="h2">Popular frameworks, rated</h2><div class="principles">${r.frameworks.map(f=>`<article class="panel pr"><h4>${md(f.name)}</h4><p>${md(f.note)}</p>${f.url?`<div class="src"><a href="${esc(f.url)}" target="_blank" rel="noopener">Source</a></div>`:""}</article>`).join("")}</div></section>`:""}
  ${(r.myths||[]).length?`<section style="display:grid;gap:14px"><h2 class="h2">Myths to ignore</h2><div class="principles">${r.myths.map(m=>`<article class="panel pr"><h4>${md(m.myth)}</h4><p>${md(m.reality)}</p><div class="src">${(m.sources||[]).map(s=>`<a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.label)}</a>`).join("")}</div></article>`).join("")}</div></section>`:""}`}
  <section class="panel"><h2 class="h2">Your week</h2><div class="tbl"><table><tbody>
    <tr><th>Mon · Wed · Fri</th><td>1–2 h: reviews first (10–15 min), then one lesson</td></tr>
    <tr><th>Tue · Thu</th><td>Long session: reviews, then the module project</td></tr>
    <tr><th>Sat</th><td>Level-3 practice set, or read real code for an hour</td></tr>
    <tr><th>Sun</th><td>Reviews only, plus plan next week</td></tr></tbody></table></div></section>`;
}

let lessonScratch=null;
const STARTER = {
  python: l=>`# ${l.title}: try it yourself\n# Write your solution here, then press Run.\n\n`,
  js: l=>`// ${l.title}: try it yourself\n// Write your solution here, then press Run.\n\n`,
  sql: l=>`-- ${l.title}: try it yourself\n-- Create a table, insert a few rows, then query them.\n\n`
};
function qLang(q){ const l=q.lid&&D.lessons[q.lid]; const base=l&&l.example?normLang(l.example.lang):null; const g=detectLang(q.code, base || (q.sid==="s4"?"js":["s3"].includes(q.sid)?null:"python")); return g&&RUNNABLE.has(g)?g:null; }
const VIEWS = {home:viewHome, profile:viewProfile, today:viewToday, map:viewMap, lesson:viewLesson, exam:viewExam, review:viewReview, practice:viewPractice, projects:viewProjects, method:viewMethod};

/* ---------- global clicks ---------- */
document.addEventListener("click",e=>{
  const t=e.target.closest("[data-lesson],[data-exam],[data-act],[data-stage],[data-path],[data-problem],[data-course],[data-project]"); if(!t || t.closest("#tabs,#moreMenu")) return;
  if(t.dataset.lesson){ go({v:"lesson", id:t.dataset.lesson}); return; }
  if(t.dataset.exam){ go({v:"exam", id:t.dataset.exam}); return; }
  if(t.dataset.path){ go({v:"path", id:t.dataset.path}); return; }
  if(t.dataset.problem){ go({v:"problem", id:t.dataset.problem}); return; }
  if(t.dataset.project){ go({v:"project", id:t.dataset.project}); return; }
  if(t.dataset.course){ go({v:"course", id:t.dataset.course, ...(t.dataset.step!=null?{step:+t.dataset.step}:{})}); return; }
  if(t.dataset.stage!=null && !t.dataset.act){ mapStage=+t.dataset.stage; render(); return; }
  if(t.dataset.act){ if(t.dataset.stageGo!=null) mapStage=+t.dataset.stageGo; else if(t.dataset.stage!=null) mapStage=+t.dataset.stage; go({v:t.dataset.act}); }
});
document.addEventListener("keydown",e=>{ if((e.key==="Enter"||e.key===" ") && e.target.matches?.('[role="button"][tabindex]')){ e.preventDefault(); e.target.dispatchEvent(new MouseEvent("click",{bubbles:true})); } });
const RESET=`<button type="button" id="reset">Clear all progress</button>`;
document.addEventListener("click",e=>{
  const t=e.target.closest("#reset,#rs-yes,#rs-no"); if(!t) return; const w=$("#resetwrap");
  if(t.id==="reset") w.innerHTML=`<span class="confirm">Erase all lessons, exams and your review deck? <button type="button" id="rs-yes">Yes, erase</button><button type="button" id="rs-no">Keep</button></span>`;
  else { if(t.id==="rs-yes"){ P=P0(); S={cards:{}}; Game.ready=false; save("p"); save("s"); go({v:"home"}); } w.innerHTML=RESET; }
});

/* ---------- boot ---------- */
(async function boot(){
  if(document.readyState==="loading") await new Promise(r=>document.addEventListener("DOMContentLoaded",r,{once:true}));
  loadLocal(); UI.buildNav();
  const files=META.map(s=>`data/${s.id}.json`).concat(["data/research.json"]);
  const [got]=await Promise.all([Promise.all(files.map(f=>fetch(f).then(r=>r.ok?r.json():null).catch(()=>null))), ...EXTRA_LOADERS.map(f=>f().catch(()=>null))]);
  D.stages=got.slice(0,META.length); D.research=got[META.length];
  if(D.research?.spacing?.intervalsDays?.length>=4) INTERVALS=D.research.spacing.intervalsDays.map(Number).filter(n=>n>0);
  indexContent();
  const legacy=(location.hash||"").slice(1);
  route = parseHash() || (VIEWS[legacy]&&!["lesson","exam"].includes(legacy)?{v:legacy}:null) || {v: Object.keys(P.lessons).length||Object.keys(P.solved).length||Object.keys(P.steps).length ? "today" : "home"};
  try{ history.replaceState(null,"",routeHash(route)); }catch(e){}
  Game.sync(true); render();
  try{
    if(window.claude?.use){
      const [db,user]=await Promise.all([window.claude.use("db"), window.claude.use("user")]);
      const uid=user?await user.id():null;
      if(db&&uid){ await attachStores(db.collection("data/users/"+uid)); return; }
    }
  }catch(e){ detachStores(); }
  if(typeof Account!=="undefined") Account.start(); else setSync("Saved in this browser");
})();
