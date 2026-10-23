"use strict";
/* ---------- Problems: a LeetCode-style problem set judged in the browser (Python via Pyodide, JavaScript in a worker) ---------- */
const PB = {list:[], byId:{}, cats:[], catById:{},
  daily(){ if(!this.list.length) return null; const pool=this.list.filter(p=>p.difficulty!=="Hard"); return pool[(today()*7919)%pool.length]; }};
EXTRA_LOADERS.push(async()=>{
  const d=await fetch("data/problems.json").then(r=>r.ok?r.json():null).catch(()=>null); if(!d) return;
  PB.list=d.problems; PB.cats=d.categories; d.problems.forEach((p,i)=>{ p.n=i+1; PB.byId[p.id]=p; }); d.categories.forEach(c=>PB.catById[c.id]=c);
});
SEARCH_SOURCES.push(()=>PB.list.map(p=>({t:p.title, sub:`${p.difficulty} · ${p.tags.join(", ")}`, kind:"Problem", i:"braces", kw:PB.catById[p.cat]?.name, r:{v:"problem", id:p.id}})));
SEARCH_SOURCES.push(()=>PB.cats.map(c=>({t:c.name+" pattern", sub:c.blurb, kind:"Pattern", i:c.icon, r:{v:"problems", cat:c.id}})));

let pbFilter={cat:"all", diff:"all", status:"all", q:""};
let pbLang=(()=>{ try{ return localStorage.getItem("cl-lang")||"python"; }catch(e){ return "python"; } })();
const fmtV = v => JSON.stringify(v);
const pStatus = id => P.solved?.[id] ? "solved" : P.tried?.[id] ? "tried" : "todo";

function diffRing(s){
  const tot={Easy:0,Medium:0,Hard:0}, got={Easy:0,Medium:0,Hard:0};
  PB.list.forEach(p=>{ tot[p.difficulty]++; if(P.solved?.[p.id]) got[p.difficulty]++; });
  const all=PB.list.length, solved=got.Easy+got.Medium+got.Hard, r=54, c=2*Math.PI*r;
  let off=0; const seg=(n,col)=>{ const len=c*n/Math.max(1,all); const s=`<circle cx="70" cy="70" r="${r}" fill="none" stroke="${col}" stroke-width="10" stroke-dasharray="${len} ${c}" stroke-dashoffset="${-off}" transform="rotate(-90 70 70)" stroke-linecap="butt"/>`; off+=len; return s; };
  return `<div class="ring-stats"><svg width="140" height="140" viewBox="0 0 140 140" role="img" aria-label="${solved} of ${all} solved"><circle cx="70" cy="70" r="${r}" fill="none" stroke="var(--sunk)" stroke-width="10"/>${seg(got.Easy,"var(--easy)")}${seg(got.Medium,"var(--med)")}${seg(got.Hard,"var(--hard)")}
    <text x="70" y="68" text-anchor="middle" style="font:800 30px var(--display);fill:var(--ink)">${solved}</text><text x="70" y="88" text-anchor="middle" style="font:600 11px var(--mono);fill:var(--muted)">/ ${all} SOLVED</text></svg>
    <div class="dbars">${["Easy","Medium","Hard"].map(d=>`<div class="r" style="color:var(--${d==="Easy"?"easy":d==="Medium"?"med":"hard"})"><span>${d}</span><span class="bar"><i style="width:${100*got[d]/Math.max(1,tot[d])}%"></i></span><span style="color:var(--muted)">${got[d]}/${tot[d]}</span></div>`).join("")}</div></div>`;
}

function viewProblems(el){
  if(!PB.list.length){ el.innerHTML=`<div class="empty">The problem set didn't load. Reload the page to try again.</div>`; return; }
  if(route.cat){ pbFilter.cat=route.cat; delete route.cat; }
  const f=pbFilter, dp=PB.daily();
  const match=p=>(f.cat==="all"||p.cat===f.cat)&&(f.diff==="all"||p.difficulty===f.diff)&&(f.status==="all"||pStatus(p.id)===f.status)
    &&(!f.q||(p.title+" "+p.tags.join(" ")).toLowerCase().includes(f.q.toLowerCase()));
  const cat=PB.catById[f.cat];
  el.innerHTML=`<section class="head"><span class="eyebrow">Problem set · judged in your browser</span><h1 class="h1">Sharpen your <span class="gt">problem solving</span></h1>
    <p class="lede">${PB.list.length} hand-picked problems across the ${PB.cats.length} patterns that cover most coding interviews. Write Python or JavaScript, run the examples, then submit against hidden tests. Every problem has hints and a full editorial.</p></section>
  <div class="grid2">
    <section class="panel">${diffRing()}</section>
    <section class="panel glow" style="background:linear-gradient(135deg,var(--surface),var(--surface2))"><div class="row" style="justify-content:space-between"><span class="eyebrow" style="color:var(--hot)">${icon("cal","sm")} Problem of the day</span><span class="diff ${dp.difficulty}">${dp.difficulty}</span></div>
      <h2 class="h2">${esc(dp.title)}</h2><p class="muted" style="margin:0">${esc(PB.catById[dp.cat].name)} · ${dp.tags.map(esc).join(", ")}</p>
      <div class="row"><button class="btn grad" data-problem="${dp.id}">${P.solved?.[dp.id]?"Solved ✓ · open again":"Solve it now"} ${icon("arrow","sm")}</button><button class="btn ghost" id="rand">${icon("shuffle")}Random unsolved</button></div></section>
  </div>
  <section style="display:grid;gap:12px">
    <div class="chips" role="group" aria-label="Pattern"><button type="button" class="chip" data-cat="all" aria-pressed="${f.cat==="all"}">All patterns</button>${PB.cats.map(c=>{ const n=PB.list.filter(p=>p.cat===c.id), s=n.filter(p=>P.solved?.[p.id]).length; return `<button type="button" class="chip" data-cat="${c.id}" aria-pressed="${f.cat===c.id}">${esc(c.name)} <span class="muted" style="font:500 11px var(--mono)">${s}/${n.length}</span></button>`; }).join("")}</div>
    ${cat?`<div class="panel pattern"><div class="row" style="justify-content:space-between"><h2 class="h3">${icon(cat.icon)} ${esc(cat.name)}: the pattern</h2><span class="pill acc">${esc(cat.blurb)}</span></div>
      <div class="grid2" style="align-items:start"><div class="prose">${cat.pattern.map(p=>`<p>${md(p)}</p>`).join("")}</div>${codeBlock(cat.template)}</div></div>`:""}
    <div class="row" style="justify-content:space-between">
      <input class="search" id="pq" placeholder="Search problems or tags…" value="${esc(f.q)}" aria-label="Search problems">
      <div class="row"><div class="seg" role="group" aria-label="Difficulty">${["all","Easy","Medium","Hard"].map(d=>`<button type="button" data-diff="${d}" aria-pressed="${f.diff===d}">${d==="all"?"Any":d}</button>`).join("")}</div>
      <div class="seg" role="group" aria-label="Status">${[["all","All"],["todo","To do"],["tried","Attempted"],["solved","Solved"]].map(([k,t])=>`<button type="button" data-st="${k}" aria-pressed="${f.status===k}">${t}</button>`).join("")}</div></div>
    </div>
    <div class="ptable" id="plist"></div>
  </section>`;
  const drawList=()=>{ const rows=PB.list.filter(match);
    el.querySelector("#plist").innerHTML = rows.length ? rows.map(p=>{ const st=pStatus(p.id); return `<button type="button" class="prow" data-problem="${p.id}"><span class="st ${st==="tried"?"tried":""}" aria-label="${st}">${st==="solved"?icon("checkc"):st==="tried"?icon("clock"):`<span class="muted" style="font:600 12px var(--mono)">${p.n}</span>`}</span><span class="t">${esc(p.title)}</span><span class="tg">${esc(p.tags.slice(0,2).join(" · "))}</span><span class="diff ${p.difficulty}">${p.difficulty}</span></button>`; }).join("")
      : `<div class="empty" style="margin:14px">No problems match those filters.</div>`; };
  drawList();
  el.querySelectorAll("[data-cat]").forEach(b=>b.onclick=()=>{ f.cat=b.dataset.cat; render(); });
  el.querySelectorAll("[data-diff]").forEach(b=>b.onclick=()=>{ f.diff=b.dataset.diff; el.querySelectorAll("[data-diff]").forEach(x=>x.setAttribute("aria-pressed",x===b)); drawList(); });
  el.querySelectorAll("[data-st]").forEach(b=>b.onclick=()=>{ f.status=b.dataset.st; el.querySelectorAll("[data-st]").forEach(x=>x.setAttribute("aria-pressed",x===b)); drawList(); });
  el.querySelector("#pq").oninput=e=>{ f.q=e.target.value; drawList(); };
  el.querySelector("#rand").onclick=()=>{ const pool=PB.list.filter(p=>!P.solved?.[p.id]); const p=(pool.length?pool:PB.list)[Math.floor(Math.random()*(pool.length||PB.list.length))]; go({v:"problem", id:p.id}); };
}

function exampleHTML(p, ex, i){
  if(p.kind==="design") return `<div class="ex"><b>Example ${i+1}</b>\nCalls:  ${esc(fmtV(ex.ops))}\nArgs:   ${esc(fmtV(ex.args))}\nOutput: ${esc(fmtV(ex.exp))}</div>`;
  return `<div class="ex"><b>Example ${i+1}</b>\nInput:  ${esc(p.params.map((n,k)=>`${n} = ${fmtV(ex.args[k])}`).join(", "))}\nOutput: ${esc(fmtV(ex.exp))}</div>`;
}
function caseInput(p, t){ return p.kind==="design" ? `${fmtV(t.ops)}\n${fmtV(t.args)}` : p.params.map((n,k)=>`${n} = ${fmtV(t.args[k])}`).join("\n"); }

function viewProblem(el){
  const p=PB.byId[route.id]; if(!p){ go({v:"problems"}); return; }
  const idx=PB.list.indexOf(p), prev=PB.list[idx-1], next=PB.list[idx+1], cat=PB.catById[p.cat];
  const L = pbLang==="js" ? "js" : "python", key = L==="python"?"py":"js";
  let tab = route.tab || "desc";
  el.innerHTML=`<nav class="crumbs"><button data-act="problems">Problems</button><span>›</span><span>${esc(cat.name)}</span><span>›</span><span>${p.n}. ${esc(p.title)}</span></nav>
  <div class="ws">
    <section class="panel desc">
      <div class="row" style="justify-content:space-between"><span class="diff ${p.difficulty}">${p.difficulty}</span>${P.solved?.[p.id]?`<span class="pill ok">${icon("check","sm")}Solved in ${P.solved[p.id].lang==="js"?"JavaScript":"Python"}</span>`:P.tried?.[p.id]?`<span class="pill exam">Attempted</span>`:""}</div>
      <h1 class="h2">${p.n}. ${esc(p.title)}</h1>
      <div class="tags">${p.tags.map(t=>`<span class="tag">${esc(t)}</span>`).join("")}</div>
      <div class="tabs2" role="tablist">${[["desc","Description","book"],["hints","Hints","bulb"],["ed","Editorial","star"]].map(([k,t,i])=>`<button type="button" role="tab" data-tab="${k}" aria-selected="${tab===k}">${icon(i,"sm")}${t}</button>`).join("")}</div>
      <div id="ptab"></div>
      <div class="row" style="justify-content:space-between;border-top:1px solid var(--line);padding-top:12px">${prev?`<button class="btn ghost sm" data-problem="${prev.id}">${icon("back","sm")} Previous</button>`:"<span></span>"}${next?`<button class="btn ghost sm" data-problem="${next.id}">Next ${icon("arrow","sm")}</button>`:""}</div>
    </section>
    <section style="display:grid;gap:14px;min-width:0">
      <div class="row" style="justify-content:space-between"><div class="seg" role="group" aria-label="Language"><button type="button" data-lang="python" aria-pressed="${L==="python"}">Python 3</button><button type="button" data-lang="js" aria-pressed="${L==="js"}">JavaScript</button></div>
        <div class="row"><button class="btn" id="prun">${icon("play","sm")}Run examples</button><button class="btn grad" id="psub">${icon("zap","sm")}Submit</button></div></div>
      <div id="ped"></div>
      <div id="pres"></div>
    </section>
  </div>`;
  const drawTab=()=>{ const box=el.querySelector("#ptab");
    if(tab==="desc") box.innerHTML=`<div class="prose" style="gap:14px">${p.desc.map(x=>`<p>${md(x)}</p>`).join("")}</div>
      <div style="display:grid;gap:10px;margin-top:6px">${(p.examples||[]).map((ex,i)=>exampleHTML(p,ex,i)).join("")}</div>
      <div style="margin-top:6px"><span class="eyebrow">Constraints</span><ul style="margin:8px 0 0;padding-left:18px;font:13px/1.7 var(--mono)">${p.constraints.map(c=>`<li>${esc(c)}</li>`).join("")}</ul></div>
      <p class="muted" style="font-size:.86rem;margin:10px 0 0">Pattern: <button class="btn ghost sm" data-act="problems" id="patlink">${esc(cat.name)}</button></p>`;
    else if(tab==="hints") box.innerHTML=`<div style="display:grid;gap:10px">${p.hints.map((h,i)=>`<details class="hint"><summary>${icon("bulb","sm")}Hint ${i+1}</summary><div>${md(h)}</div></details>`).join("")}
      <details class="hint"><summary>${icon("layers","sm")}The ${esc(cat.name)} pattern</summary><div class="prose">${cat.pattern.map(x=>`<p>${md(x)}</p>`).join("")}${codeBlock(cat.template)}</div></details></div>`;
    else { const show=P.solved?.[p.id]||route.reveal;
      box.innerHTML = show ? `<div class="prose" style="gap:12px">${p.editorial.map(x=>`<p>${md(x)}</p>`).join("")}<p><b>Complexity:</b> ${md(p.complexity)}</p></div>
        <div class="seg" style="margin:12px 0 8px"><button type="button" data-sl="py" aria-pressed="${key==="py"}">Python</button><button type="button" data-sl="js" aria-pressed="${key==="js"}">JavaScript</button></div><div id="solcode">${codeBlock(p.solution[key])}</div>`
      : `<div class="empty" style="display:grid;gap:12px;justify-items:center">${icon("lock","xl")}<b>The editorial unlocks when you solve it.</b><span>Struggling productively is where the learning happens. Try the hints first. Still stuck after 20 minutes? Reading a solution is fine, then close it and write it again from memory tomorrow.</span><button class="btn" id="reveal">Reveal anyway</button></div>`;
      box.querySelector("#reveal")?.addEventListener("click",()=>{ route.reveal=true; drawTab(); });
      box.querySelectorAll("[data-sl]").forEach(b=>b.onclick=()=>{ box.querySelectorAll("[data-sl]").forEach(x=>x.setAttribute("aria-pressed",x===b)); box.querySelector("#solcode").innerHTML=codeBlock(p.solution[b.dataset.sl]); }); }
    el.querySelector("#patlink")?.addEventListener("click",()=>{ pbFilter.cat=p.cat; });
  };
  drawTab();
  el.querySelectorAll("[data-tab]").forEach(b=>b.onclick=()=>{ tab=route.tab=b.dataset.tab; el.querySelectorAll("[data-tab]").forEach(x=>x.setAttribute("aria-selected",x===b)); drawTab(); });
  const ed=mountEditor(el.querySelector("#ped"), {lang:L, code:p.starter[key], draftKey:`pb-${p.id}-${key}`, label:`${p.kind==="design"?p.cls[key]:p.fn[key]}()`, onRun:()=>judge(false), runLabel:"Run ▶", tall:true});
  el.querySelectorAll("[data-lang]").forEach(b=>b.onclick=()=>{ pbLang=b.dataset.lang; try{ localStorage.setItem("cl-lang",pbLang); }catch(e){} render(); });
  const res=el.querySelector("#pres"), runB=el.querySelector("#prun"), subB=el.querySelector("#psub");
  async function judge(full){
    if(Runner.busy) return;
    const tests = full ? p.tests : p.examples;
    runB.disabled=subB.disabled=true;
    res.innerHTML=`<div class="panel"><div class="row">${icon("clock")}<b>${full?"Judging against all tests":"Running examples"}…</b><span class="muted" style="font-size:.88rem">${L==="python"&&!Runner.ready("python")?"Starting Python (first run takes a few seconds)":""}</span></div></div>`;
    const r=await Judge.problem(p, L, ed.value, tests);
    runB.disabled=subB.disabled=false;
    if(full){ P.tried=P.tried||{}; P.tried[p.id]=1; }
    const ac=r.status==="Accepted", first=!P.solved?.[p.id];
    if(full && ac){ P.solved=P.solved||{}; if(first){ P.solved[p.id]={d:today(), lang:L==="js"?"js":"py"}; logActivity(3); } }
    if(full){ logActivity(1); save("p"); }
    const passed=r.res?r.res.filter(x=>x.ok).length:0;
    const showCases = !full ? (r.res||[]).map((x,i)=>({x,t:tests[i],i})) : (r.res&&!ac ? [{x:r.res[r.firstFail], t:tests[r.firstFail], i:r.firstFail}] : []);
    res.innerHTML=`<div class="panel">
      <div class="verdict ${ac?"ac":"wa"}">${icon(ac?"checkc":"x","lg")}<span>${full?r.status:(ac?"All examples pass":r.status)}</span><span style="margin-left:auto;font:500 13px var(--mono)">${r.res?`${passed} / ${r.res.length} passed`:""}${r.ms!=null?` · ${r.ms} ms`:""}</span></div>
      ${r.fatal?`<p style="margin:0">${esc(r.fatal)} Keep the name from the starter code.</p>`:""}
      ${full&&ac?`<p style="margin:0">${first?`Accepted on your first solve: <b>+${XPV[p.difficulty]} XP</b>. `:""}All ${r.res.length} tests passed, including the hidden ones. Read the editorial to compare approaches${next?", or move on":""}.</p><div class="row"><button class="btn" data-tab-go="ed">${icon("star","sm")}Read the editorial</button>${next?`<button class="btn primary" data-problem="${next.id}">Next problem ${icon("arrow","sm")}</button>`:""}</div>`:""}
      ${!full&&ac?`<p class="muted" style="margin:0">Examples pass. Now <b>Submit</b> to run the hidden tests, which include edge cases and larger inputs.</p>`:""}
      ${showCases.length?`<div class="tests">${showCases.map(({x,t,i})=>`<div class="tcase ${x.ok?"p":"f"}"><div class="hd">${x.ok?`<span class="ok">✓</span>`:`<span class="no">✗</span>`}${full?`Failing test ${i+1} of ${tests.length}`:`Example ${i+1}`}${x.ms!=null?`<span class="muted" style="margin-left:auto;font:500 11px var(--mono)">${x.ms} ms</span>`:""}</div>
        <span class="muted">Input</span><span style="white-space:pre-wrap">${esc(caseInput(p,t))}</span><span class="muted">Expected</span><span>${esc(fmtV(t.exp))}</span>${x.err?`<span class="muted">Error</span><span style="color:var(--bad)">${esc(x.err)}</span>`:`<span class="muted">Your output</span><span>${esc(fmtV(x.got))}</span>`}</div>`).join("")}</div>`:""}
      ${r.stdout.trim()?`<div><span class="eyebrow">Your prints (stdout)</span><pre class="edpre" style="padding:6px 0">${esc(r.stdout.slice(0,4000))}</pre></div>`:""}
      ${r.stderr.trim()?`<div><span class="eyebrow">Error</span><pre class="edpre" style="padding:6px 0;color:var(--bad)">${esc(r.stderr.slice(0,4000))}</pre></div>`:""}
      ${r.status==="Time Limit Exceeded"?`<p style="margin:0">Your code ran too long. Look for an infinite loop, or an approach slower than the constraints allow. Check the hints for the intended complexity.</p>`:""}
    </div>`;
    res.querySelector("[data-tab-go]")?.addEventListener("click",()=>{ tab=route.tab="ed"; el.querySelectorAll("[data-tab]").forEach(x=>x.setAttribute("aria-selected",x.dataset.tab==="ed")); drawTab(); el.querySelector(".desc").scrollIntoView({behavior:"smooth"}); });
    if(full && ac && first) UI.confetti();
    res.scrollIntoView({behavior:"smooth", block:"nearest"});
  }
  runB.onclick=()=>judge(false); subB.onclick=()=>judge(true);
}
VIEWS.problems=viewProblems; VIEWS.problem=viewProblem;
