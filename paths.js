"use strict";
/* ---------- Career paths: roadmap.sh-style roadmaps. Each path = phases → topic nodes (with resources) + a portfolio project per phase.
   Node state lives in P.nodes["pathId:nodeId"] = "doing" | "done" | "skip". ---------- */
const PATHS = {index:[], cache:{}, focusNode:null,
  async load(id){ if(this.cache[id]) return this.cache[id]; const d=await fetch(`data/paths/${id}.json`).then(r=>r.ok?r.json():null).catch(()=>null); if(d) this.cache[id]=d; return d; },
  loadAll(){ return this._all || (this._all=Promise.all(this.index.map(p=>this.load(p.id)))); },
  progress(p){ let done=0, total=0; (p.phases||[]).forEach(ph=>ph.nodes.forEach(n=>{ total++; if(P.nodes?.[p.id+":"+(n.id||n)]==="done") done++; })); return {done,total}; },
  current(){ let last=null; try{ last=localStorage.getItem("cl-lastpath"); }catch(e){}
    const scored=this.index.map(p=>({p, ...this.progress(p)})).filter(x=>x.done>0&&x.done<x.total).sort((a,b)=>b.done-a.done);
    const pick=scored.find(x=>x.p.id===last)||scored[0]||(last&&this.index.find(p=>p.id===last)?{p:this.index.find(p=>p.id===last),...this.progress(this.index.find(p=>p.id===last))}:null);
    return pick?{...pick.p, done:pick.done, total:pick.total}:null; }
};
EXTRA_LOADERS.push(async()=>{ const d=await fetch("data/paths/index.json").then(r=>r.ok?r.json():null).catch(()=>null); if(d) PATHS.index=d.paths; PATHS.cats=d?.cats||[]; });
SEARCH_SOURCES.push(()=>PATHS.index.map(p=>({t:p.title, sub:p.tagline, kind:"Career path", i:p.icon, kw:p.cat, r:{v:"path", id:p.id}})));
SEARCH_SOURCES.push(()=>Object.values(PATHS.cache).flatMap(p=>p.phases.flatMap(ph=>ph.nodes.map(n=>({t:n.t, sub:`${p.title} · ${ph.title}`, kind:"Topic", i:p.icon, kw:(n.topics||[]).join(" "), r:{v:"path", id:p.id, node:n.id}})))));

/* ---------- path finder quiz ---------- */
const QUIZ = [
  {q:"What sounds most fun to build?", a:[
    ["Things people see and tap: websites, apps, interfaces", {frontend:3, fullstack:2, ios:2, android:2, "ux-engineer":2}],
    ["The engines behind the scenes: APIs, databases, servers", {backend:3, fullstack:1, dba:2, architect:2, "data-engineer":1}],
    ["Software that learns from data or talks like a person", {"ai-engineer":3, "ml-engineer":3, "data-scientist":2}],
    ["Defending systems and keeping people's data safe", {cybersecurity:4, appsec:3}],
    ["Games, 3D worlds and graphics", {"game-dev":3, "xr-graphics":3}],
    ["Code that moves real hardware: robots, chips, devices", {embedded:3, robotics:3, systems:1}]]},
  {q:"Which kind of problem do you enjoy?", a:[
    ["Making something look and feel just right", {frontend:2, ios:2, android:2, "game-dev":1, "xr-graphics":1, "ux-engineer":2}],
    ["Logic puzzles and clever algorithms", {backend:1, systems:2, quantum:2, "ml-engineer":1, "game-dev":1, blockchain:1}],
    ["Finding the story hidden in numbers", {"data-scientist":2, "data-analyst":3, "data-engineer":1}],
    ["Automating chores and keeping systems running", {devops:3, sre:3, cloud:2, qa:2}],
    ["Spotting risks and making systems safer", {appsec:2, cybersecurity:2}]]},
  {q:"How do you feel about maths?", a:[
    ["Keep it light, please", {frontend:1, qa:1, devops:1, "data-analyst":1, fullstack:1, "ux-engineer":1}],
    ["Some is fine when it's useful", {backend:1, "data-engineer":1, appsec:1, "game-dev":1, cloud:1, blockchain:1}],
    ["Bring it on: linear algebra, probability, the works", {"ml-engineer":2, "ai-engineer":1, quantum:3, robotics:2, "xr-graphics":2, "data-scientist":2}]]},
  {q:"Where would you like to work?", a:[
    ["A startup, shipping fast and wearing many hats", {fullstack:2, "ai-engineer":2, frontend:1, ios:1, android:1}],
    ["Big systems at serious scale", {sre:2, systems:2, "ml-engineer":1, architect:2, "data-engineer":1, backend:1}],
    ["Anywhere: I want reliable, steady demand", {cybersecurity:2, cloud:2, dba:2, "data-analyst":1, qa:1, devops:1}],
    ["Close to the frontier of research", {quantum:2, "ml-engineer":2, robotics:2, blockchain:1, "xr-graphics":1}]]}
];
let quizState=null;
function quizHTML(){
  const s=quizState;
  if(s.i<QUIZ.length){ const q=QUIZ[s.i];
    return `<div class="row" style="justify-content:space-between"><span class="eyebrow">Question ${s.i+1} of ${QUIZ.length}</span><button class="btn ghost sm" id="qzx">${icon("x","sm")}Close</button></div><h2 class="h3" style="font-size:1.35rem">${esc(q.q)}</h2>
      <div class="opts">${q.a.map((a,k)=>`<button type="button" class="opt" data-qa="${k}"><span class="k">${"ABCDEF"[k]}</span><span>${esc(a[0])}</span></button>`).join("")}</div>`; }
  const top=Object.entries(s.score).sort((a,b)=>b[1]-a[1]).map(([id])=>PATHS.index.find(p=>p.id===id)).filter(Boolean).slice(0,3);
  return `<div class="row" style="justify-content:space-between"><span class="eyebrow">Your matches</span><button class="btn ghost sm" id="qzx">${icon("x","sm")}Close</button></div><h2 class="h3" style="font-size:1.35rem">Paths that fit how you think</h2>
    <div class="pgrid">${top.map(p=>pathCard(p)).join("")}</div><div class="row"><button class="btn ghost" id="qzr">${icon("refresh","sm")}Retake</button><span class="muted" style="font-size:.86rem">This is a starting point, not a verdict. The first phases of most paths overlap, so you can switch later at little cost.</span></div>`;
}
function bindQuiz(box){
  box.innerHTML=quizHTML();
  box.querySelectorAll("[data-qa]").forEach(b=>b.onclick=()=>{ const w=QUIZ[quizState.i].a[+b.dataset.qa][1]; Object.entries(w).forEach(([k,v])=>quizState.score[k]=(quizState.score[k]||0)+v); quizState.i++; bindQuiz(box); });
  box.querySelector("#qzx").onclick=()=>{ quizState=null; box.hidden=true; };
  box.querySelector("#qzr")?.addEventListener("click",()=>{ quizState={i:0,score:{}}; bindQuiz(box); });
}

let pathCat="all";
function viewPaths(el){
  if(!PATHS.index.length){ el.innerHTML=`<div class="empty">Career paths didn't load. Reload the page to try again.</div>`; return; }
  const cats=[...new Set(PATHS.index.map(p=>p.cat))];
  const totalNodes=PATHS.index.reduce((a,p)=>a+PATHS.progress(p).total,0);
  el.innerHTML=`<section class="head"><span class="eyebrow">Career paths · ${PATHS.index.length} roadmaps · ${totalNodes} topics</span><h1 class="h1">Choose your <span class="gt">destination</span></h1>
    <p class="lede">Every job in software, mapped. Each path is a phased curriculum: the topics to learn in order, free resources for each, a portfolio project per phase, and what interviews will ask. Click any topic to see details and track your progress.</p>
    <div class="row"><button class="btn grad" id="quiz">${icon("compass")}Not sure? Find your path</button><span class="muted" style="font-size:.9rem">Every path builds on the <button class="btn ghost sm" data-act="map">core curriculum</button></span></div></section>
  <section class="panel" id="quizbox" hidden></section>
  <div class="chips"><button type="button" class="chip" data-pc="all" aria-pressed="${pathCat==="all"}">All paths</button>${cats.map(c=>`<button type="button" class="chip" data-pc="${esc(c)}" aria-pressed="${pathCat===c}">${esc(c)}</button>`).join("")}</div>
  ${cats.filter(c=>pathCat==="all"||pathCat===c).map(c=>`<section style="display:grid;gap:14px"><h2 class="h2">${esc(c)}</h2><div class="pgrid">${PATHS.index.filter(p=>p.cat===c).map(p=>pathCard(p)).join("")}</div></section>`).join("")}`;
  el.querySelectorAll("[data-pc]").forEach(b=>b.onclick=()=>{ pathCat=b.dataset.pc; render(); });
  const qb=el.querySelector("#quizbox");
  el.querySelector("#quiz").onclick=()=>{ quizState={i:0,score:{}}; qb.hidden=false; bindQuiz(qb); qb.scrollIntoView({behavior:"smooth",block:"center"}); };
  if(quizState){ qb.hidden=false; bindQuiz(qb); }
}

const NODE_STATES=[["todo","To do"],["doing","In progress"],["done","Done"],["skip","Skip"]];
function nodeState(pid,nid){ return P.nodes?.[pid+":"+nid]||"todo"; }
function setNode(pid,nid,st){ P.nodes=P.nodes||{}; const k=pid+":"+nid; const was=P.nodes[k]; if(st==="todo") delete P.nodes[k]; else P.nodes[k]=st; if(st==="done"&&was!=="done") logActivity(1); save("p"); }

async function viewPath(el){
  const meta=PATHS.index.find(p=>p.id===route.id); if(!meta){ go({v:"paths"}); return; }
  try{ localStorage.setItem("cl-lastpath", meta.id); }catch(e){}
  el.innerHTML=`<div class="loading">Loading the ${esc(meta.title)} roadmap…</div>`;
  const p=await PATHS.load(meta.id); if(route.v!=="path"||route.id!==meta.id) return;
  if(!p){ el.innerHTML=`<div class="empty">This roadmap didn't load. Reload to try again.</div>`; return; }
  const draw=()=>{
    const pr=PATHS.progress(p), pct=Math.round(100*pr.done/Math.max(1,pr.total));
    const nextNode=p.phases.flatMap(ph=>ph.nodes).find(n=>!["done","skip"].includes(nodeState(p.id,n.id)));
    const coreMods=(p.core||[]).map(id=>D.modById[id]).filter(Boolean);
    el.innerHTML=`<nav class="crumbs"><button data-act="paths">Career paths</button><span>›</span><span>${esc(p.cat)}</span><span>›</span><span>${esc(p.title)}</span></nav>
    <section class="phero" style="--h:${esc(p.hue)}">
      <div class="row" style="gap:16px"><span class="pico" style="width:64px;height:64px;border-radius:18px">${icon(p.icon,"xl")}</span><div style="display:grid;gap:4px"><span class="eyebrow">${esc(p.cat)} · ${esc(p.duration)} · ${p.phases.length} phases</span><h1 class="h1">${esc(p.title)}</h1></div></div>
      <p class="lede">${esc(p.tagline)}</p>
      <div class="prose" style="max-width:80ch">${(p.about||[]).map(x=>`<p>${md(x)}</p>`).join("")}</div>
      <div style="display:grid;gap:6px;max-width:520px"><div class="row" style="justify-content:space-between"><span class="eyebrow">Your progress</span><span class="pill acc">${pr.done} / ${pr.total} topics · ${pct}%</span></div><div class="bar"><i style="width:${pct}%;background:var(--h)"></i></div></div>
      <div class="row">${nextNode?`<button class="btn grad" data-node="${esc(nextNode.id)}">${icon("play","sm")}${pr.done?"Continue":"Start"}: ${esc(nextNode.t)}</button>`:`<span class="pill ok">${icon("award","sm")}Path complete. Go build and apply.</span>`}<button class="btn ghost" id="jump">${icon("list","sm")}Jump to roadmap</button></div>
    </section>
    <div class="kv">
      <div><span class="eyebrow">What you'll do day to day</span><ul>${(p.day||[]).map(x=>`<li>${md(x)}</li>`).join("")}</ul></div>
      <div><span class="eyebrow">Tools of the trade</span><div class="tags">${(p.tools||[]).map(t=>`<span class="tag">${esc(t)}</span>`).join("")}</div></div>
      <div><span class="eyebrow">Job titles</span><ul>${(p.roles||[]).map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div>
      ${coreMods.length?`<div><span class="eyebrow">Core curriculum to take alongside</span><div style="display:grid;gap:6px">${coreMods.map(m=>`<button class="btn ghost sm" style="justify-content:flex-start;text-align:left" data-act="map" data-stage-go="${m.si}">${passed(m)?icon("checkc","sm"):icon("book","sm")}${esc(m.title)}</button>`).join("")}</div></div>`:""}
    </div>
    <section class="road" id="road" style="--h:${esc(p.hue)}">
      <div class="head" style="margin-bottom:22px"><span class="eyebrow">The roadmap</span><h2 class="h2">${p.phases.length} phases, in order</h2><p class="muted" style="margin:0">Tap a topic for what to learn and where. Mark it in progress, done, or skip it if you already know it.</p></div>
      ${p.phases.map((ph,k)=>{ const dn=ph.nodes.filter(n=>nodeState(p.id,n.id)==="done").length, all=dn===ph.nodes.length;
        return `<div class="phase ${all?"done":""}"><div class="rail"><span class="num">${all?icon("check"):k+1}</span></div><div class="body">
          <div style="display:grid;gap:4px"><span class="eyebrow">Phase ${k+1} · ${esc(ph.weeks||"")} · ${dn}/${ph.nodes.length}</span><h3>${esc(ph.title)}</h3>${ph.goal?`<p class="muted" style="margin:0">${md(ph.goal)}</p>`:""}</div>
          <div class="nodes">${ph.nodes.map(n=>{ const st=nodeState(p.id,n.id); return `<button type="button" class="node ${st} ${n.core?"core":""}" data-node="${esc(n.id)}"><span class="ck">${icon("check")}</span><span><b>${esc(n.t)}</b>${n.opt?`<span class="s">Optional</span>`:""}</span></button>`; }).join("")}</div>
          ${ph.project?`<div class="projbox"><span class="eyebrow" style="color:var(--h)">${icon("rocket","sm")} Portfolio project</span><b>${esc(ph.project.t)}</b><span class="muted" style="font-size:.92rem">${md(ph.project.d)}</span></div>`:""}
        </div></div>`; }).join("")}
    </section>
    <div class="grid2">
      ${(p.interview||[]).length?`<section class="panel"><h2 class="h3">${icon("brief")} Interview prep</h2><ul style="margin:0;padding-left:18px;display:grid;gap:6px">${p.interview.map(x=>`<li>${md(x)}</li>`).join("")}</ul><button class="btn ghost sm" style="justify-self:start" data-act="problems">${icon("braces","sm")}Practise problems</button></section>`:""}
      ${(p.certs||[]).length?`<section class="panel"><h2 class="h3">${icon("award")} Certifications worth knowing</h2><ul style="margin:0;padding-left:18px;display:grid;gap:6px">${p.certs.map(x=>`<li>${md(x)}</li>`).join("")}</ul><p class="muted" style="margin:0;font-size:.85rem">Optional. A strong portfolio usually matters more; certifications help most in security, cloud and some enterprise hiring.</p></section>`:""}
    </div>
    ${(p.related||[]).length?`<section style="display:grid;gap:14px"><h2 class="h2">Related paths</h2><div class="pgrid">${p.related.map(id=>PATHS.index.find(x=>x.id===id)).filter(Boolean).map(x=>pathCard(x)).join("")}</div></section>`:""}`;
    el.querySelector("#jump").onclick=()=>el.querySelector("#road").scrollIntoView({behavior:"smooth"});
    el.querySelectorAll("[data-node]").forEach(b=>b.onclick=()=>openNode(b.dataset.node));
  };
  const openNode=nid=>{
    const ph=p.phases.find(x=>x.nodes.some(n=>n.id===nid)); const n=ph?.nodes.find(x=>x.id===nid); if(!n) return;
    document.querySelector(".drawer-bg")?.remove(); document.querySelector(".drawer")?.remove();
    const bg=document.createElement("div"); bg.className="drawer-bg"; const dr=document.createElement("aside"); dr.className="drawer"; dr.setAttribute("role","dialog"); dr.setAttribute("aria-label",n.t); dr.style.setProperty("--h",p.hue);
    const mod=n.core?D.modById[n.core]:null;
    const paint=()=>{ const st=nodeState(p.id,n.id);
      dr.innerHTML=`<div class="row" style="justify-content:space-between"><span class="eyebrow">${esc(p.title)} · ${esc(ph.title)}</span><button class="iconbtn" id="dx" aria-label="Close">${icon("x")}</button></div>
        <h2 class="h2">${esc(n.t)}</h2>
        <div class="seg" role="group" aria-label="Status">${NODE_STATES.map(([k,t])=>`<button type="button" data-st="${k}" aria-pressed="${st===k}">${t}</button>`).join("")}</div>
        <div class="prose">${(Array.isArray(n.d)?n.d:[n.d]).map(x=>`<p>${md(x)}</p>`).join("")}</div>
        ${(n.topics||[]).length?`<div style="display:grid;gap:8px"><span class="eyebrow">Learn these</span><div class="tags">${n.topics.map(t=>`<span class="tag">${esc(t)}</span>`).join("")}</div></div>`:""}
        ${mod?`<div class="task"><span class="eyebrow" style="color:var(--accent)">${icon("map","sm")} In the core curriculum</span><span>Stage ${mod.si} · <b>${esc(mod.title)}</b>: ${esc(mod.summary)}</span><button class="btn primary sm" style="justify-self:start" data-act="map" data-stage-go="${mod.si}">Open module</button></div>`:""}
        ${(n.links||[]).length?`<div style="display:grid;gap:8px"><span class="eyebrow">Free resources</span><div class="links">${n.links.map(([t,u])=>`<a href="${esc(u)}" target="_blank" rel="noopener">${icon("ext","sm")}<span>${esc(t)}</span></a>`).join("")}</div></div>`:""}
        ${(()=>{ const all=ph.nodes, k=all.indexOf(n), nx=all[k+1]||p.phases[p.phases.indexOf(ph)+1]?.nodes[0]; return nx?`<button class="btn" id="dnext" style="justify-self:start">Next topic: ${esc(nx.t)} ${icon("arrow","sm")}</button>`:""; })()}`;
      dr.querySelector("#dx").onclick=close;
      dr.querySelectorAll("[data-st]").forEach(b=>b.onclick=()=>{ setNode(p.id,n.id,b.dataset.st); paint(); draw(); if(b.dataset.st==="done"){ const allDone=ph.nodes.every(x=>nodeState(p.id,x.id)==="done"); if(allDone) UI.confetti(120); } });
      dr.querySelector("#dnext")?.addEventListener("click",()=>{ const all=ph.nodes, k=all.indexOf(n), nx=all[k+1]||p.phases[p.phases.indexOf(ph)+1]?.nodes[0]; openNode(nx.id); });
      dr.querySelectorAll("[data-act]").forEach(b=>b.addEventListener("click",close));
    };
    const close=()=>{ bg.remove(); dr.remove(); document.removeEventListener("keydown",esck); };
    const esck=e=>{ if(e.key==="Escape") close(); };
    bg.onclick=close; document.addEventListener("keydown",esck);
    document.body.append(bg,dr); paint(); dr.querySelector("#dx").focus();
  };
  draw();
  if(route.node){ const nid=route.node; delete route.node; openNode(nid); }
}
VIEWS.paths=viewPaths; VIEWS.path=viewPath;
