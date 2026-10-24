"use strict";
/* ---------- Bootcamp courses and Build projects share one step engine: instructions + starter code + automatic checks.
   A step's starter is the previous step's solution, so the learner builds one program from start to finish.
   Projects group their steps into milestones and add a live demo of the finished app. ---------- */
const BC = {courses:[], byId:{}, tracks:[],
  stepIndex(c){ return c.steps.findIndex(s=>!P.steps?.[s.id]); },
  nextStep(){ let best=null; for(const c of this.courses){ const done=c.steps.filter(s=>P.steps?.[s.id]).length; const i=this.stepIndex(c); if(done>0 && i>=0) return {course:c, idx:i, step:c.steps[i]}; if(!best && i>=0) best={course:c, idx:i, step:c.steps[i]}; } return best; }
};
const PJ = {list:[], byId:{},
  next(){ for(const p of this.list){ const d=courseDone(p), i=BC.stepIndex(p); if(d>0 && i>=0) return {project:p, idx:i, step:p.steps[i]}; } return null; }
};
const linkSteps = c => c.steps.forEach((s,i)=>{ s.starter = s.starter ?? (i ? c.steps[i-1].solution : ""); if(c.seed) s.seed=c.seed; });
EXTRA_LOADERS.push(async()=>{
  const d=await fetch("data/bootcamp.json").then(r=>r.ok?r.json():null).catch(()=>null); if(!d) return;
  BC.courses=d.courses; BC.tracks=d.tracks||[]; d.courses.forEach(c=>{ BC.byId[c.id]=c; linkSteps(c); });
});
EXTRA_LOADERS.push(async()=>{
  const d=await fetch("data/projects.json").then(r=>r.ok?r.json():null).catch(()=>null); if(!d) return;
  PJ.list=d.projects; PJ.tracks=d.tracks||[];
  d.projects.forEach(p=>{ PJ.byId[p.id]=p; p.steps=p.milestones.flatMap((m,mi)=>m.steps.map(s=>({...s, ms:mi}))); linkSteps(p); });
});
SEARCH_SOURCES.push(()=>BC.courses.flatMap(c=>[{t:c.title, sub:`${c.steps.length} steps · ${c.tagline}`, kind:"Course", i:c.icon, r:{v:"course", id:c.id}},
  ...c.steps.map((s,i)=>({t:s.title, sub:`${c.title} · step ${i+1}`, kind:"Step", i:"cap", r:{v:"course", id:c.id, step:i}}))]));
SEARCH_SOURCES.push(()=>PJ.list.flatMap(p=>[{t:p.title, sub:`${p.level} · ${LANGNAME[p.lang]||p.lang} · ${p.tagline}`, kind:"Project", i:p.icon, kw:p.skills.join(" "), r:{v:"project", id:p.id}},
  ...p.steps.map((s,i)=>({t:s.title, sub:`Build: ${p.title} · step ${i+1}`, kind:"Step", i:"rocket", r:{v:"make", id:p.id, step:i}}))]));

const courseDone = c => c.steps.filter(s=>P.steps?.[s.id]).length;
let bcTrack="all";
function viewBootcamp(el){
  if(!BC.courses.length){ el.innerHTML=`<div class="empty">The bootcamp didn't load. Reload the page to try again.</div>`; return; }
  const total=BC.courses.reduce((a,c)=>a+c.steps.length,0), done=BC.courses.reduce((a,c)=>a+courseDone(c),0), ns=BC.nextStep();
  el.innerHTML=`<section class="head"><span class="eyebrow">Zero experience required</span><h1 class="h1">The <span class="gt">Bootcamp</span></h1>
    <p class="lede">Learn by doing, one tiny step at a time. Each step explains one idea, asks you to write a few lines, and checks your code instantly. By the end of a course you'll have built something real, entirely in your browser.</p>
    <div class="row">${ns?`<button class="btn grad lg" data-course="${ns.course.id}" data-step="${ns.idx}">${icon("play")}${done?"Continue":"Start"}: ${esc(ns.course.title)}, step ${ns.idx+1}</button>`:`<span class="pill ok">Every course complete. You're a graduate.</span>`}<span class="pill acc">${done} / ${total} steps passed</span></div></section>
  <div class="chips" role="group" aria-label="Track">${[{id:"all",name:"All tracks"},...BC.tracks].map(t=>`<button type="button" class="chip" data-bct="${t.id}" aria-pressed="${bcTrack===t.id}">${t.icon?icon(t.icon,"sm"):""}${esc(t.name)}</button>`).join("")}</div>
  ${(BC.tracks.length?BC.tracks:[{id:"all",name:"Courses"}]).filter(t=>bcTrack==="all"||t.id===bcTrack).map(t=>{ const cs=BC.courses.filter(c=>t.id==="all"||c.track===t.id); if(!cs.length) return "";
    const td=cs.reduce((a,c)=>a+courseDone(c),0), tt=cs.reduce((a,c)=>a+c.steps.length,0);
    return `<section class="bctrack" style="display:grid;gap:14px"><div class="sec-h"><div class="head"><span class="eyebrow">${cs.length} course${cs.length===1?"":"s"} · ${td} / ${tt} steps</span><h2 class="h2">${esc(t.name)}</h2></div>${t.blurb?`<p class="lede" style="max-width:52ch;margin:0">${esc(t.blurb)}</p>`:""}</div>
    <div class="grid2">${cs.map(c=>{ const i=BC.courses.indexOf(c), d=courseDone(c), pct=Math.round(100*d/c.steps.length);
    return `<button type="button" class="course rv" style="--h:${esc(c.hue)}" data-course="${c.id}"><div class="art">${esc(c.art)}</div>
      <div class="row" style="justify-content:space-between"><span class="eyebrow">Course ${i+1} · ${esc(LANGNAME[c.lang]||c.lang)}${c.level?` · ${esc(c.level)}`:""}</span>${d===c.steps.length?`<span class="pill ok">${icon("award","sm")}Completed</span>`:d?`<span class="pill acc">${pct}%</span>`:`<span class="pill">${c.steps.length} steps · ~${esc(c.hours)}</span>`}</div>
      <h3 class="h3" style="font-size:1.35rem">${esc(c.title)}</h3><p class="muted" style="margin:0">${esc(c.desc)}</p>
      <div class="bar"><i style="width:${pct}%;background:var(--h)"></i></div>
      <span class="muted" style="font-size:.86rem">${icon("rocket","sm")} You'll build: <b style="color:var(--ink)">${esc(c.project)}</b></span></button>`; }).join("")}</div></section>`; }).join("")}
  <section class="panel"><h2 class="h3">How the bootcamp fits the rest of CodeLearner</h2>
    <div class="grid3">${[["cap","1. Bootcamp","Your first 10–20 hours: the syntax and the feeling of making things work."],["rocket","2. Build & Learn","Pick a real project and build it step by step, learning each idea at the moment you need it."],["map","3. Core curriculum","The 10,000-Hour Map: daily lessons, exams and spaced review, from Python basics to distributed systems."]].map(([i,t,d])=>`<div style="display:grid;gap:6px"><span class="row" style="gap:8px;color:var(--accent)">${icon(i)}<b style="color:var(--ink)">${t}</b></span><span class="muted" style="font-size:.92rem">${d}</span></div>`).join("")}</div></section>`;
  el.querySelectorAll("[data-bct]").forEach(b=>b.onclick=()=>{ bcTrack=b.dataset.bct; render(); });
}
function viewCourse(el){
  const c=BC.byId[route.id]; if(!c){ go({v:"bootcamp"}); return; }
  stepWorkspace(el, c, {crumbs:`<button data-act="bootcamp">Bootcamp</button><span>›</span><span>${esc(c.title)}</span>`, back:"bootcamp", backLabel:"Back to the Bootcamp", done:`You finished <b>${esc(c.title)}</b> and built ${esc(c.project)}. That's real code you wrote.`});
}

/* ---------- live preview for HTML (static, same-origin so checks can read styles) and web apps (scripts, sandboxed) ---------- */
function mountPreview(host, lang, storage){
  host.innerHTML=`<div class="preview"><div class="pbar">${icon("globe","sm")} Live preview${lang==="web"?`<span style="margin-left:auto" class="muted">sandboxed · storage resets each run</span>`:""}</div><iframe title="Live preview of your page" sandbox="${lang==="web"?"allow-scripts allow-forms":"allow-same-origin"}"></iframe>${lang==="web"?`<div class="console" aria-live="polite"><div class="chead"><span class="eyebrow">Console</span><button type="button" class="btn ghost sm" data-clr>Clear</button></div><pre></pre></div>`:""}</div>`;
  const pv=host.querySelector("iframe"), out=host.querySelector(".console pre");
  host.querySelector("[data-clr]")?.addEventListener("click",()=>{ out.textContent=""; });
  let last=null, token=null;
  return {frame:pv, show(code){
    if(code===last) return Promise.resolve(); last=code;
    if(lang!=="web") return new Promise(res=>{ pv.onload=()=>res(); pv.srcdoc=code; setTimeout(res,800); });
    if(token) delete WEB.handlers[token];
    token=WEB.token(); out.textContent="";
    WEB.handlers[token]=d=>{ if(d.type!=="log") return; const sp=document.createElement("span"); sp.className=d.level==="error"?"err":d.level==="warn"?"warn":""; sp.textContent=d.text+"\n"; out.appendChild(sp); out.scrollTop=out.scrollHeight; };
    pv.srcdoc=WEB.inject(code, WEB.prelude(token, storage||{}));
    return new Promise(res=>{ pv.onload=()=>res(); setTimeout(res,800); });
  }};
}

/* ---------- the shared step workspace ---------- */
function stepWorkspace(el, c, o){
  const firstOpen = BC.stepIndex(c);
  let i = route.step!=null ? route.step : (firstOpen<0 ? 0 : firstOpen);
  const maxOpen = firstOpen<0 ? c.steps.length-1 : firstOpen;
  if(i>maxOpen) i=maxOpen; route.step=i;
  const s=c.steps[i], passed=!!P.steps?.[s.id], last=i===c.steps.length-1;
  const lang=c.lang, ms=c.milestones?c.milestones[s.ms]:null;
  const stepBtn=(x,k)=>`<button type="button" data-goto="${k}" class="${P.steps?.[x.id]?"done":""}" aria-current="${k===i}" ${k>maxOpen?"disabled":""} data-tip="${esc(x.title)}">${k+1}</button>`;
  const stepper = c.milestones
    ? `<div class="msteps">${c.milestones.map((m,mi)=>{ const idx=c.steps.map((x,k)=>k).filter(k=>c.steps[k].ms===mi); const dn=idx.filter(k=>P.steps?.[c.steps[k].id]).length;
        return `<div class="mgroup ${mi===s.ms?"cur":""}"><span class="eyebrow">M${mi+1} · ${esc(m.title)} <span class="muted">${dn}/${idx.length}</span></span><div class="stepper">${idx.map(k=>stepBtn(c.steps[k],k)).join("")}</div></div>`; }).join("")}</div>`
    : `<div class="stepper" aria-label="Steps">${c.steps.map(stepBtn).join("")}</div>`;
  const mod=s.core?D.modById[s.core]:null;
  el.innerHTML=`<nav class="crumbs">${o.crumbs}<span>›</span><span>Step ${i+1} of ${c.steps.length}</span></nav>
  ${stepper}
  <div class="ws">
    <section class="panel desc" style="gap:16px">
      <span class="eyebrow" style="color:var(--accent)">${ms?`Milestone ${s.ms+1}: ${esc(ms.title)} · `:""}Step ${i+1}</span>
      <h1 class="h2">${esc(s.title)}</h1>
      ${ms&&c.steps.findIndex(x=>x.ms===s.ms)===i&&ms.goal?`<div class="objective"><span class="eyebrow">This milestone</span>${md(ms.goal)}</div>`:""}
      <div class="prose">${s.body.map(p=>`<p>${md(p)}</p>`).join("")}</div>
      ${s.example?`<div><span class="eyebrow">Example</span>${codeBlock(s.example)}</div>`:""}
      <div class="task"><span class="eyebrow" style="color:var(--accent)">${icon("target","sm")} Your task</span><div>${md(s.task)}</div></div>
      <div><span class="eyebrow">Checks</span><ul class="checks" id="checks" style="margin-top:8px">${(s.tests||[]).map(t=>`<li><span class="m">·</span><span>${md(t.msg)}</span></li>`).join("")}</ul></div>
      ${s.hint?`<details class="hint"><summary>${icon("bulb","sm")}Hint</summary><div>${md(s.hint)}</div></details>`:""}
      ${mod||s.ref?`<div class="links">${mod?`<a href="#/map" data-act="map" data-stage-go="${mod.si}">${icon("map","sm")}<span>Go deeper in the core curriculum: <b>${esc(mod.title)}</b></span></a>`:""}${s.ref?`<a href="${esc(s.ref[1])}" target="_blank" rel="noopener">${icon("ext","sm")}<span>${esc(s.ref[0])}</span></a>`:""}</div>`:""}
      <div id="sol"></div>
      <div id="stepres"></div>
    </section>
    <section style="display:grid;gap:14px;min-width:0">
      <div class="row" style="justify-content:space-between"><span class="pill ${passed?"ok":"acc"}">${passed?"Passed ✓":"In progress"}</span><button class="btn grad" id="check">${icon("check","sm")}Check your code</button></div>
      <div id="sed"></div>
      ${lang==="html"||lang==="web"?`<div id="pvh"></div>`:""}
      ${lang==="sql"?`<div class="panel" style="padding:14px"><span class="eyebrow">Tables available</span><div class="muted" style="font:12.5px/1.6 var(--mono);white-space:pre-wrap">${esc(c.schema||"Your own: you create them in the code.")}</div><div id="sqlres" class="sqlres"></div></div>`:""}
    </section>
  </div>`;
  el.querySelectorAll("[data-goto]").forEach(b=>b.onclick=()=>{ if(!b.disabled){ route.step=+b.dataset.goto; render(); window.scrollTo({top:0}); } });
  const pv = (lang==="html"||lang==="web") ? mountPreview(el.querySelector("#pvh"), lang, s.storage) : null;
  const visual = lang==="html"||lang==="web";
  const ed=mountEditor(el.querySelector("#sed"), {lang, code:s.starter, draftKey:`bc-${s.id}`, resetTo:s.starter, label:visual?"index.html":lang==="python"?"main.py":lang==="js"?"main.js":"query.sql",
    onRun: visual ? ()=>check() : null, runLabel: visual?"Check ▶":"Run ▶", onChange: visual ? v=>pv.show(v) : null, tall:true});
  if(visual) pv.show(s.starter);
  let fails=0;
  async function check(){
    const btn=el.querySelector("#check"); btn.disabled=true;
    const code=ed.value; let r;
    if(lang==="html"){ await pv.show(code); let doc=null, win=null; try{ doc=pv.frame.contentDocument; win=pv.frame.contentWindow; if(!doc||!doc.body) throw 0; }catch(e){ doc=new DOMParser().parseFromString(code,"text/html"); win=null; } r=await Judge.step(s,"html",code,{doc,win}); }
    else { el.querySelector("#stepres").innerHTML=`<div class="row muted">${icon("clock","sm")} ${lang==="web"?"Testing your app":"Running your code"}${lang==="python"&&!Runner.ready("python")?" (starting Python, the first run takes a few seconds)":""}…</div>`; r=await Judge.step(s,lang,code,{stdin:s.stdin}); if(lang==="web") pv.show(code); }
    btn.disabled=false;
    const lis=el.querySelectorAll("#checks li"); r.checks.forEach((x,k)=>{ const li=lis[k]; if(!li) return; li.className=x.ok?"p":"f"; li.querySelector(".m").textContent=x.ok?"✓":"✗"; });
    const ok=r.checks.length>0 && r.checks.every(x=>x.ok);
    if(lang==="sql"){ const box=el.querySelector("#sqlres"); box.innerHTML = r.rows ? `<table><thead><tr>${r.rows.cols.map(h=>`<th>${esc(h)}</th>`).join("")}</tr></thead><tbody>${r.rows.rows.slice(0,50).map(row=>`<tr>${row.map(v=>`<td>${esc(v===null?"NULL":v)}</td>`).join("")}</tr>`).join("")}</tbody></table><span class="muted" style="font:500 11px var(--mono)">${r.rows.rows.length} row${r.rows.rows.length===1?"":"s"}</span>` : r.stderr?`<pre class="edpre" style="color:var(--bad);padding:6px 0">${esc(r.stderr)}</pre>`:`<span class="muted">No rows returned yet. End with a SELECT.</span>`; }
    const outBox = (lang==="python"||lang==="js") ? `${r.stdout?.trim()?`<div><span class="eyebrow">Output</span><pre class="edpre" style="padding:6px 0">${esc(r.stdout.slice(0,3000))}</pre></div>`:""}${r.stderr?.trim()?`<div><span class="eyebrow">Error</span><pre class="edpre" style="padding:6px 0;color:var(--bad)">${esc(r.stderr.slice(0,3000))}</pre></div>`:""}` : "";
    if(ok){
      const first=!P.steps?.[s.id]; P.steps=P.steps||{}; if(first){ P.steps[s.id]=today(); logActivity(1); save("p"); }
      const allNow=c.steps.every(x=>P.steps?.[x.id]);
      const msDone = c.milestones && c.steps.filter(x=>x.ms===s.ms).every(x=>P.steps?.[x.id]) && (c.steps[i+1]?.ms!==s.ms);
      el.querySelector("#stepres").innerHTML=`<div class="fb r"><b>${allNow&&last?(c.milestones?"Project complete!":"Course complete!"):msDone?`Milestone ${s.ms+1} complete!`:"Step passed!"}</b><p>${first?`+${XPV.step} XP. `:""}${allNow&&last?o.done:msDone?`<b>${esc(ms.title)}</b> works. On to milestone ${s.ms+2}: ${esc(c.milestones[s.ms+1]?.title||"")}.`:"Nice work. Your code carries over to the next step."}</p>${outBox}
        <div class="row">${!last?`<button class="btn primary" data-goto2="${i+1}">Next step ${icon("arrow","sm")}</button>`:`<button class="btn primary" data-act="${o.back}">${esc(o.backLabel)}</button>${o.after||`<button class="btn" data-act="map">Continue to the core curriculum</button>`}`}</div></div>`;
      el.querySelector("[data-goto2]")?.addEventListener("click",()=>{ route.step=i+1; render(); window.scrollTo({top:0}); });
      if(first && allNow){ UI.confetti(220); } else if(first) UI.confetti(msDone?120:60);
      if(first){ const sb=el.querySelector(`[data-goto="${i}"]`); sb?.classList.add("done"); const nb=el.querySelector(`[data-goto="${i+1}"]`); if(nb) nb.disabled=false; }
    } else {
      fails++;
      const firstBad=r.checks.find(x=>!x.ok);
      el.querySelector("#stepres").innerHTML=`<div class="fb w"><b>Not yet</b><p>${firstBad?`Check: ${md(firstBad.msg)}`:"Something's off."} ${firstBad?.hint?esc(firstBad.hint):""}</p>${outBox}</div>`;
      if(fails>=2 && s.solution!=null && !el.querySelector("#showsol")) el.querySelector("#sol").innerHTML=`<button class="btn ghost sm" id="showsol">${icon("eye","sm")}Show a working solution</button>`;
      el.querySelector("#showsol")?.addEventListener("click",()=>{ el.querySelector("#sol").innerHTML=`<span class="eyebrow">One working solution</span>${codeBlock(s.solution)}<p class="muted" style="font-size:.85rem;margin:6px 0 0">Type it yourself rather than pasting. Your fingers learn too.</p>`; });
    }
    el.querySelector("#stepres").scrollIntoView({behavior:"smooth", block:"nearest"});
  }
  el.querySelector("#check").onclick=check;
}

/* ================= BUILD & LEARN ================= */
let buildFilter={lang:"all", level:"all"};
const LEVELS_B=["Beginner","Intermediate","Advanced"];
function projectCard(p){
  const d=courseDone(p), pct=Math.round(100*d/p.steps.length);
  return `<button type="button" class="course rv" style="--h:${esc(p.hue)}" data-project="${p.id}"><div class="art">${esc(p.art)}</div>
    <div class="row" style="justify-content:space-between"><span class="eyebrow">${esc(p.level)} · ${esc(LANGNAME[p.lang]||p.lang)}</span>${d===p.steps.length?`<span class="pill ok">${icon("award","sm")}Built</span>`:d?`<span class="pill acc">${pct}%</span>`:`<span class="pill">~${esc(p.hours)}</span>`}</div>
    <h3 class="h3" style="font-size:1.3rem">${esc(p.title)}</h3><p class="muted" style="margin:0">${esc(p.tagline)}</p>
    <div class="tags">${p.skills.slice(0,4).map(t=>`<span class="tag">${esc(t)}</span>`).join("")}</div>
    <div class="bar"><i style="width:${pct}%;background:var(--h)"></i></div>
    <span class="muted" style="font-size:.84rem">${p.milestones.length} milestones · ${p.steps.length} guided steps</span></button>`;
}
function viewBuild(el){
  if(!PJ.list.length){ el.innerHTML=`<div class="empty">The projects didn't load. Reload the page to try again.</div>`; return; }
  const f=buildFilter, langs=[...new Set(PJ.list.map(p=>p.lang))];
  const list=PJ.list.filter(p=>(f.lang==="all"||p.lang===f.lang)&&(f.level==="all"||p.level===f.level));
  const nx=PJ.next(), built=PJ.list.filter(p=>courseDone(p)===p.steps.length).length;
  el.innerHTML=`<section class="head"><span class="eyebrow">Build &amp; Learn · ${PJ.list.length} guided projects · ${PJ.list.reduce((a,p)=>a+p.steps.length,0)} steps</span><h1 class="h1">Pick a project. <span class="gt">Learn by building it.</span></h1>
    <p class="lede">Choose something you'd actually want to make. You get the full pathway: milestones, one small step at a time, the concept explained right when you need it, instant checks on your code, hints when you're stuck, and a working app at the end.</p>
    <div class="row">${nx?`<button class="btn grad lg" data-make="${nx.project.id}" data-step="${nx.idx}">${icon("play")}Continue ${esc(nx.project.title)}, step ${nx.idx+1}</button>`:""}<span class="pill acc">${built} of ${PJ.list.length} projects built</span></div></section>
  <section class="panel"><div class="grid3">${[["target","1. Choose","Pick a project by language and level. Each one lists the skills it teaches."],["layers","2. Build in milestones","Every milestone ends with something that works. Each step teaches one concept, then you write the code."],["checkc","3. Get unstuck","Checks tell you exactly what's missing. Hints, worked examples and a full solution are there when you need them."]].map(([i,t,d])=>`<div style="display:grid;gap:6px"><span class="row" style="gap:8px;color:var(--accent)">${icon(i)}<b style="color:var(--ink)">${t}</b></span><span class="muted" style="font-size:.92rem">${d}</span></div>`).join("")}</div></section>
  <div class="row" style="justify-content:space-between">
    <div class="chips" role="group" aria-label="Language"><button type="button" class="chip" data-bl="all" aria-pressed="${f.lang==="all"}">All languages</button>${langs.map(l=>`<button type="button" class="chip" data-bl="${l}" aria-pressed="${f.lang===l}">${esc(LANGNAME[l]||l)}</button>`).join("")}</div>
    <div class="seg" role="group" aria-label="Level">${["all",...LEVELS_B].map(l=>`<button type="button" data-blv="${l}" aria-pressed="${f.level===l}">${l==="all"?"Any level":l}</button>`).join("")}</div>
  </div>
  ${list.length?`<div class="grid3 pj">${list.map(projectCard).join("")}</div>`:`<div class="empty">No projects match those filters.</div>`}`;
  el.querySelectorAll("[data-bl]").forEach(b=>b.onclick=()=>{ f.lang=b.dataset.bl; render(); });
  el.querySelectorAll("[data-blv]").forEach(b=>b.onclick=()=>{ f.level=b.dataset.blv; render(); });
}
function viewProject(el){
  const p=PJ.byId[route.id]; if(!p){ go({v:"build"}); return; }
  const d=courseDone(p), nextI=BC.stepIndex(p), pct=Math.round(100*d/p.steps.length);
  const mods=(p.core||[]).map(id=>D.modById[id]).filter(Boolean);
  const visual=p.lang==="web"||p.lang==="html";
  el.innerHTML=`<nav class="crumbs"><button data-act="build">Build &amp; Learn</button><span>›</span><span>${esc(p.title)}</span></nav>
  <section class="phero" style="--h:${esc(p.hue)}">
    <div class="row" style="gap:16px"><span class="pico" style="width:64px;height:64px;border-radius:18px">${icon(p.icon,"xl")}</span><div style="display:grid;gap:4px"><span class="eyebrow">${esc(p.level)} · ${esc(LANGNAME[p.lang]||p.lang)} · ~${esc(p.hours)} · ${p.steps.length} steps</span><h1 class="h1">${esc(p.title)}</h1></div></div>
    <p class="lede">${esc(p.tagline)}</p>
    <div class="prose" style="max-width:80ch">${p.desc.map(x=>`<p>${md(x)}</p>`).join("")}</div>
    <div style="display:grid;gap:6px;max-width:520px"><div class="row" style="justify-content:space-between"><span class="eyebrow">Your progress</span><span class="pill acc">${d} / ${p.steps.length} steps · ${pct}%</span></div><div class="bar"><i style="width:${pct}%;background:var(--h)"></i></div></div>
    <div class="row">${nextI>=0?`<button class="btn grad lg" data-make="${p.id}" data-step="${nextI}">${icon("play")}${d?"Continue building":"Start building"}</button>`:`<span class="pill ok">${icon("award","sm")}Built. Now make it yours with the stretch goals below.</span><button class="btn" data-make="${p.id}" data-step="0">Revisit the steps</button>`}<button class="btn ghost" data-ws-from="${p.id}">${icon("terminal")}Open in the Editor</button></div>
  </section>
  <div class="grid2" style="align-items:start">
    <section class="panel"><h2 class="h3">${icon("eye")} What you'll build</h2><p style="margin:0">${md(p.final)}</p>
      ${visual?`<div id="demo"></div><p class="muted" style="margin:0;font-size:.85rem">This is the finished app, running live. Try it.</p>`:p.demo?`<div><span class="eyebrow">A sample run of the finished program</span><pre class="edpre" style="background:var(--code-bg);border:1px solid var(--line);border-radius:12px;padding:12px 14px">${esc(p.demo)}</pre></div>`:""}</section>
    <section class="panel"><h2 class="h3">${icon("bulb")} What you'll learn</h2><div class="tags">${p.skills.map(t=>`<span class="tag">${esc(t)}</span>`).join("")}</div>
      ${p.prereq?`<p class="muted" style="margin:0;font-size:.9rem"><b style="color:var(--ink)">Before you start:</b> ${md(p.prereq)}</p>`:""}
      ${mods.length?`<div style="display:grid;gap:6px"><span class="eyebrow">Matching core-curriculum modules</span>${mods.map(m=>`<button class="btn ghost sm" style="justify-content:flex-start;text-align:left" data-act="map" data-stage-go="${m.si}">${icon("book","sm")}${esc(m.title)}</button>`).join("")}</div>`:""}</section>
  </div>
  <section class="road" style="--h:${esc(p.hue)}">
    <div class="head" style="margin-bottom:22px"><span class="eyebrow">The pathway</span><h2 class="h2">${p.milestones.length} milestones, each ending in something that works</h2></div>
    ${p.milestones.map((m,mi)=>{ const idx=p.steps.map((x,k)=>k).filter(k=>p.steps[k].ms===mi), dn=idx.filter(k=>P.steps?.[p.steps[k].id]).length, all=dn===idx.length;
      return `<div class="phase ${all?"done":""}"><div class="rail"><span class="num">${all?icon("check"):mi+1}</span></div><div class="body">
        <div style="display:grid;gap:4px"><span class="eyebrow">Milestone ${mi+1} · ${dn}/${idx.length}</span><h3>${esc(m.title)}</h3><p class="muted" style="margin:0">${md(m.goal)}</p></div>
        <div class="nodes">${idx.map(k=>{ const x=p.steps[k], st=P.steps?.[x.id]?"done":""; const open=nextI<0||k<=nextI; return `<button type="button" class="node ${st}" ${open?`data-make="${p.id}" data-step="${k}"`:`aria-disabled="true" style="opacity:.6;cursor:default"`}><span class="ck">${icon("check")}</span><span><b>${k+1}. ${esc(x.title)}</b></span></button>`; }).join("")}</div>
      </div></div>`; }).join("")}
  </section>
  ${(p.stretch||[]).length?`<section class="panel"><h2 class="h3">${icon("rocket")} Stretch goals: make it yours</h2><ul style="margin:0;padding-left:18px;display:grid;gap:6px">${p.stretch.map(x=>`<li>${md(x)}</li>`).join("")}</ul>
    <p class="muted" style="margin:0;font-size:.9rem">${visual?"When you're happy with it, copy your code into an <code>index.html</code> file and publish it free on GitHub Pages or Netlify Drop.":"When you're happy with it, copy your code into a file on your computer, run it there, and push it to GitHub with a short README."}</p></section>`:""}
  <section style="display:grid;gap:14px"><h2 class="h2">More projects</h2><div class="grid3 pj">${PJ.list.filter(x=>x.id!==p.id).sort((a,b)=>(a.lang===p.lang?0:1)-(b.lang===p.lang?0:1)).slice(0,3).map(projectCard).join("")}</div></section>`;
  if(visual){ const pv=mountPreview(el.querySelector("#demo"), p.lang, p.steps[p.steps.length-1].storage); pv.show(p.steps[p.steps.length-1].solution); }
}
function viewMake(el){
  const p=PJ.byId[route.id]; if(!p){ go({v:"build"}); return; }
  stepWorkspace(el, p, {crumbs:`<button data-act="build">Build &amp; Learn</button><span>›</span><button data-project="${p.id}">${esc(p.title)}</button>`, back:"build", backLabel:"Pick your next project",
    after:`<button class="btn" data-project="${p.id}">See stretch goals</button><button class="btn" data-ws-from="${p.id}">${icon("terminal")}Keep building in the Editor</button>`, done:`You built <b>${esc(p.title)}</b> from an empty file. Open the project page for stretch goals and how to publish it.`});
}
document.addEventListener("click",e=>{ const t=e.target.closest("[data-make]"); if(!t||t.getAttribute("aria-disabled")==="true") return; go({v:"make", id:t.dataset.make, ...(t.dataset.step!=null?{step:+t.dataset.step}:{})}); });
VIEWS.bootcamp=viewBootcamp; VIEWS.course=viewCourse; VIEWS.build=viewBuild; VIEWS.project=viewProject; VIEWS.make=viewMake;
