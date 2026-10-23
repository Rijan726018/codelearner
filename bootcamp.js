"use strict";
/* ---------- Bootcamp: freeCodeCamp-style step-by-step courses. Each step = instructions + starter code + automatic checks.
   A step's starter is the previous step's solution, so the learner builds one program from start to finish. ---------- */
const BC = {courses:[], byId:{},
  stepIndex(c){ return c.steps.findIndex(s=>!P.steps?.[s.id]); },
  nextStep(){ let best=null; for(const c of this.courses){ const done=c.steps.filter(s=>P.steps?.[s.id]).length; const i=this.stepIndex(c); if(done>0 && i>=0) return {course:c, idx:i, step:c.steps[i]}; if(!best && i>=0) best={course:c, idx:i, step:c.steps[i]}; } return best; }
};
EXTRA_LOADERS.push(async()=>{
  const d=await fetch("data/bootcamp.json").then(r=>r.ok?r.json():null).catch(()=>null); if(!d) return;
  BC.courses=d.courses; d.courses.forEach(c=>{ BC.byId[c.id]=c; c.steps.forEach((s,i)=>{ s.starter = s.starter ?? (i ? c.steps[i-1].solution : ""); if(c.seed) s.seed=c.seed; }); });
});
SEARCH_SOURCES.push(()=>BC.courses.flatMap(c=>[{t:c.title, sub:`${c.steps.length} steps · ${c.tagline}`, kind:"Course", i:c.icon, r:{v:"course", id:c.id}},
  ...c.steps.map((s,i)=>({t:s.title, sub:`${c.title} · step ${i+1}`, kind:"Step", i:"cap", r:{v:"course", id:c.id, step:i}}))]));

const courseDone = c => c.steps.filter(s=>P.steps?.[s.id]).length;
function viewBootcamp(el){
  if(!BC.courses.length){ el.innerHTML=`<div class="empty">The bootcamp didn't load. Reload the page to try again.</div>`; return; }
  const total=BC.courses.reduce((a,c)=>a+c.steps.length,0), done=BC.courses.reduce((a,c)=>a+courseDone(c),0), ns=BC.nextStep();
  el.innerHTML=`<section class="head"><span class="eyebrow">Zero experience required</span><h1 class="h1">The <span class="gt">Bootcamp</span></h1>
    <p class="lede">Learn by doing, one tiny step at a time. Each step explains one idea, asks you to write a few lines, and checks your code instantly. By the end of a course you'll have built something real, entirely in your browser.</p>
    <div class="row">${ns?`<button class="btn grad lg" data-course="${ns.course.id}" data-step="${ns.idx}">${icon("play")}${done?"Continue":"Start"}: ${esc(ns.course.title)}, step ${ns.idx+1}</button>`:`<span class="pill ok">Every course complete. You're a graduate.</span>`}<span class="pill acc">${done} / ${total} steps passed</span></div></section>
  <div class="grid2">${BC.courses.map((c,i)=>{ const d=courseDone(c), pct=Math.round(100*d/c.steps.length);
    return `<button type="button" class="course rv" style="--h:${esc(c.hue)}" data-course="${c.id}"><div class="art">${esc(c.art)}</div>
      <div class="row" style="justify-content:space-between"><span class="eyebrow">Course ${i+1} · ${esc(LANGNAME[c.lang]||c.lang)}</span>${d===c.steps.length?`<span class="pill ok">${icon("award","sm")}Completed</span>`:d?`<span class="pill acc">${pct}%</span>`:`<span class="pill">${c.steps.length} steps · ~${esc(c.hours)}</span>`}</div>
      <h3 class="h3" style="font-size:1.35rem">${esc(c.title)}</h3><p class="muted" style="margin:0">${esc(c.desc)}</p>
      <div class="bar"><i style="width:${pct}%;background:var(--h)"></i></div>
      <span class="muted" style="font-size:.86rem">${icon("rocket","sm")} You'll build: <b style="color:var(--ink)">${esc(c.project)}</b></span></button>`; }).join("")}</div>
  <section class="panel"><h2 class="h3">How the bootcamp fits the rest of CodeLearner</h2>
    <div class="grid3">${[["cap","1. Bootcamp","Your first 10–20 hours: the syntax and the feeling of making things work."],["map","2. Core curriculum","Then the 10,000-Hour Map: daily lessons, exams and spaced review, from Python basics to distributed systems."],["route","3. Career path","Pick a destination roadmap and work through its phases and portfolio projects."]].map(([i,t,d])=>`<div style="display:grid;gap:6px"><span class="row" style="gap:8px;color:var(--accent)">${icon(i)}<b style="color:var(--ink)">${t}</b></span><span class="muted" style="font-size:.92rem">${d}</span></div>`).join("")}</div></section>`;
}

function viewCourse(el){
  const c=BC.byId[route.id]; if(!c){ go({v:"bootcamp"}); return; }
  const firstOpen = BC.stepIndex(c);
  let i = route.step!=null ? route.step : (firstOpen<0 ? 0 : firstOpen);
  const maxOpen = firstOpen<0 ? c.steps.length-1 : firstOpen;
  if(i>maxOpen) i=maxOpen; route.step=i;
  const s=c.steps[i], passed=!!P.steps?.[s.id], last=i===c.steps.length-1;
  const lang=c.lang;
  el.innerHTML=`<nav class="crumbs"><button data-act="bootcamp">Bootcamp</button><span>›</span><span>${esc(c.title)}</span><span>›</span><span>Step ${i+1} of ${c.steps.length}</span></nav>
  <div class="stepper" aria-label="Steps">${c.steps.map((x,k)=>`<button type="button" data-goto="${k}" class="${P.steps?.[x.id]?"done":""}" aria-current="${k===i}" ${k>maxOpen?"disabled":""} data-tip="${esc(x.title)}">${k+1}</button>`).join("")}</div>
  <div class="ws">
    <section class="panel desc" style="gap:16px">
      <span class="eyebrow" style="color:var(--accent)">Step ${i+1} · ${esc(c.title)}</span>
      <h1 class="h2">${esc(s.title)}</h1>
      <div class="prose">${s.body.map(p=>`<p>${md(p)}</p>`).join("")}</div>
      ${s.example?`<div><span class="eyebrow">Example</span>${codeBlock(s.example)}</div>`:""}
      <div class="task"><span class="eyebrow" style="color:var(--accent)">${icon("target","sm")} Your task</span><div>${md(s.task)}</div></div>
      <div><span class="eyebrow">Checks</span><ul class="checks" id="checks" style="margin-top:8px">${(s.tests||[]).map(t=>`<li><span class="m">·</span><span>${md(t.msg)}</span></li>`).join("")}</ul></div>
      ${s.hint?`<details class="hint"><summary>${icon("bulb","sm")}Hint</summary><div>${md(s.hint)}</div></details>`:""}
      <div id="sol"></div>
      <div id="stepres"></div>
    </section>
    <section style="display:grid;gap:14px;min-width:0">
      <div class="row" style="justify-content:space-between"><span class="pill ${passed?"ok":"acc"}">${passed?"Passed ✓":"In progress"}</span><button class="btn grad" id="check">${icon("check","sm")}Check your code</button></div>
      <div id="sed"></div>
      ${lang==="html"?`<div class="preview"><div class="pbar">${icon("globe","sm")} Live preview</div><iframe id="pv" title="Live preview of your page" sandbox="allow-same-origin"></iframe></div>`:""}
      ${lang==="sql"?`<div class="panel" style="padding:14px"><span class="eyebrow">Tables available</span><div class="muted" style="font:12.5px/1.6 var(--mono)">${esc(c.schema||"")}</div><div id="sqlres" class="sqlres"></div></div>`:""}
    </section>
  </div>`;
  el.querySelectorAll("[data-goto]").forEach(b=>b.onclick=()=>{ if(!b.disabled){ route.step=+b.dataset.goto; render(); window.scrollTo({top:0}); } });
  const pv=el.querySelector("#pv");
  let lastHTML=null; const preview=code=>{ if(!pv||code===lastHTML) return Promise.resolve(); lastHTML=code; return new Promise(res=>{ pv.onload=()=>res(); pv.srcdoc=code; setTimeout(res,800); }); };
  const ed=mountEditor(el.querySelector("#sed"), {lang, code:s.starter, draftKey:`bc-${s.id}`, resetTo:s.starter, label:lang==="html"?"index.html":lang==="python"?"main.py":lang==="js"?"main.js":"query.sql",
    onRun: lang==="html" ? ()=>check() : null, runLabel: lang==="html"?"Check ▶":"Run ▶", onChange: lang==="html" ? v=>preview(v) : null, tall:true});
  if(lang==="html") preview(s.starter);
  let fails=0;
  async function check(){
    const btn=el.querySelector("#check"); btn.disabled=true;
    const code=ed.value; let r;
    if(lang==="html"){ await preview(code); let doc=null, win=null; try{ doc=pv.contentDocument; win=pv.contentWindow; if(!doc||!doc.body) throw 0; }catch(e){ doc=new DOMParser().parseFromString(code,"text/html"); win=null; } r=await Judge.step(s,"html",code,{doc,win}); }
    else { el.querySelector("#stepres").innerHTML=`<div class="row muted">${icon("clock","sm")} Running your code${lang==="python"&&!Runner.ready("python")?" (starting Python, the first run takes a few seconds)":""}…</div>`; r=await Judge.step(s,lang,code); }
    btn.disabled=false;
    const lis=el.querySelectorAll("#checks li"); r.checks.forEach((x,k)=>{ const li=lis[k]; if(!li) return; li.className=x.ok?"p":"f"; li.querySelector(".m").textContent=x.ok?"✓":"✗"; });
    const ok=r.checks.length>0 && r.checks.every(x=>x.ok);
    if(lang==="sql"){ const box=el.querySelector("#sqlres"); box.innerHTML = r.rows ? `<table><thead><tr>${r.rows.cols.map(h=>`<th>${esc(h)}</th>`).join("")}</tr></thead><tbody>${r.rows.rows.slice(0,50).map(row=>`<tr>${row.map(v=>`<td>${esc(v===null?"NULL":v)}</td>`).join("")}</tr>`).join("")}</tbody></table><span class="muted" style="font:500 11px var(--mono)">${r.rows.rows.length} row${r.rows.rows.length===1?"":"s"}</span>` : r.stderr?`<pre class="edpre" style="color:var(--bad);padding:6px 0">${esc(r.stderr)}</pre>`:`<span class="muted">No rows returned yet. End with a SELECT.</span>`; }
    const outBox = (lang==="python"||lang==="js") ? `${r.stdout?.trim()?`<div><span class="eyebrow">Output</span><pre class="edpre" style="padding:6px 0">${esc(r.stdout.slice(0,3000))}</pre></div>`:""}${r.stderr?.trim()?`<div><span class="eyebrow">Error</span><pre class="edpre" style="padding:6px 0;color:var(--bad)">${esc(r.stderr.slice(0,3000))}</pre></div>`:""}` : "";
    if(ok){
      const first=!P.steps?.[s.id]; P.steps=P.steps||{}; if(first){ P.steps[s.id]=today(); logActivity(1); save("p"); }
      const courseNow=c.steps.every(x=>P.steps?.[x.id]);
      el.querySelector("#stepres").innerHTML=`<div class="fb r"><b>${courseNow&&last?"Course complete!":"Step passed!"}</b><p>${first?`+${XPV.step} XP. `:""}${courseNow&&last?`You finished <b>${esc(c.title)}</b> and built ${esc(c.project)}. That's real code you wrote.`:"Nice work. Your code carries over to the next step."}</p>${outBox}
        <div class="row">${!last?`<button class="btn primary" data-goto2="${i+1}">Next step ${icon("arrow","sm")}</button>`:`<button class="btn primary" data-act="bootcamp">Back to the Bootcamp</button><button class="btn" data-act="map">Continue to the core curriculum</button>`}</div></div>`;
      el.querySelector("[data-goto2]")?.addEventListener("click",()=>{ route.step=i+1; render(); window.scrollTo({top:0}); });
      if(first && courseNow){ UI.confetti(220); } else if(first) UI.confetti(60);
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
VIEWS.bootcamp=viewBootcamp; VIEWS.course=viewCourse;
