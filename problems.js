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
      <div class="grid2" style="align-items:start"><div class="prose">${cat.pattern.map(p=>`<p>${md(p)}</p>`).join("")}</div><div style="display:grid;gap:12px;min-width:0">${codeBlock(cat.template)}${cat.video?videoBlock({title:cat.name, video:cat.video, q:`${cat.name} coding interview pattern`}):""}</div></div></div>`:""}
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
  bindVideos(el);
}

function exampleHTML(p, ex, i){
  if(p.kind==="design") return `<div class="ex"><b>Example ${i+1}</b>\nCalls:  ${esc(fmtV(ex.ops))}\nArgs:   ${esc(fmtV(ex.args))}\nOutput: ${esc(fmtV(ex.exp))}</div>`;
  return `<div class="ex"><b>Example ${i+1}</b>\nInput:  ${esc(p.params.map((n,k)=>`${n} = ${fmtV(ex.args[k])}`).join(", "))}\nOutput: ${esc(fmtV(ex.exp))}</div>`;
}
function caseInput(p, t){ return p.kind==="design" ? `${fmtV(t.ops)}\n${fmtV(t.args)}` : p.params.map((n,k)=>`${n} = ${fmtV(t.args[k])}`).join("\n"); }

/* ---------- "Explain it simply": the problem in plain words, plus a card for every idea it uses ----------
   Cards and the problem → cards map come from data/concepts.json (tools/build_concepts.py, which runs every example). */
let PB_CONCEPTS = null;
const loadConcepts = () => PB_CONCEPTS || (PB_CONCEPTS = fetch("data/concepts.json").then(r => r.ok ? r.json() : null).catch(() => null));
function plainKind(v, p, name){
  const list = p.cat === "linked-list" && Array.isArray(v) && /^(head|list\d*|l\d|a|b)$/i.test(name || "head");
  const tree = p.cat === "trees" && Array.isArray(v) && /^(root|p|q|tree|subRoot|s|t)$/i.test(name || "root");
  if(list) return "a linked list (shown here as the list of its values, front to back)";
  if(tree) return "a binary tree (shown level by level, top to bottom; null means \"no child here\")";
  if(v === null) return "nothing: None in Python, null in JavaScript";
  if(typeof v === "boolean") return "true or false";
  if(typeof v === "number") return Number.isInteger(v) ? "a whole number" : "a number with decimals";
  if(typeof v === "string") return v.length === 1 ? "a single character" : "a piece of text (a string)";
  if(Array.isArray(v)){
    if(!v.length) return "a list (this one is empty)";
    if(v.every(Array.isArray)) return v.every(r => r.every(x => typeof x === "string")) ? "a grid of characters (a list of rows)" : v.length && v.every(r => r.length === 2) ? "a list of pairs" : "a grid (a list of rows, each row a list)";
    if(v.every(x => typeof x === "number")) return v.every(Number.isInteger) ? "a list of whole numbers" : "a list of numbers";
    if(v.every(x => typeof x === "string")) return v.every(x => x.length === 1) ? "a list of single characters" : "a list of strings";
    if(v.every(x => typeof x === "boolean")) return "a list of true/false values";
  }
  return "a value";
}
function plainWords(p){
  const ex = (p.examples || [])[0]; if(!ex) return "";
  const code = v => `<code>${esc(fmtV(v))}</code>`;
  if(p.kind === "design"){
    const cls = p.cls?.py || p.ops?.[0] || "the class";
    return `<p>This one is different: instead of one function, you build a small machine, a <b>class</b> called <code>${esc(cls)}</code>. The tests create one and then press its buttons (call its methods) one after another, checking every answer.</p>
      <div class="pw"><div><span class="eyebrow">The tests do this</span><ol>${ex.ops.map((op, i) => `<li><code>${esc(op)}(${esc(ex.args[i].map(fmtV).join(", "))})</code>${i === 0 ? " creates the object" : ex.exp[i] === null ? " (nothing to give back)" : ` should give back ${code(ex.exp[i])}`}</li>`).join("")}</ol></div></div>`;
  }
  const names = p.params || [];
  return `<div class="pw"><div><span class="eyebrow">You get</span><ul>${names.map((n, k) => `<li><code>${esc(n)}</code>: ${plainKind(ex.args[k], p, n)}, like ${code(ex.args[k])}</li>`).join("")}</ul></div>
    <div><span class="eyebrow">You give back</span><ul><li>${plainKind(ex.exp, p, names[0])}</li></ul></div></div>
    <p class="pwex">For example, when ${names.map((n, k) => `${esc(n)} is ${code(ex.args[k])}`).join(" and ")}, the right answer is ${code(ex.exp)}.${(p.examples || []).length > 1 ? ` The other example${p.examples.length > 2 ? "s" : ""} on the Description tab ${p.examples.length > 2 ? "are" : "is"} worth working through by hand too.` : ""}</p>`;
}
function conceptCard(c, lang, open){
  const code = c[lang === "js" ? "js" : "py"], out = c[lang === "js" ? "js_out" : "py_out"];
  return `<details class="ccard"${open ? " open" : ""}><summary><span class="ct">${esc(c.title)}</span><span class="ck">${md(c.kid)}</span></summary>
    <div class="cbody"><div class="prose">${c.how.map(x => `<p>${md(x)}</p>`).join("")}</div>
      <div class="cex"><span class="eyebrow">Try it · ${lang === "js" ? "JavaScript" : "Python"}</span>${codeBlock(code, null, lang === "js" ? "javascript" : "python")}<span class="eyebrow">It prints</span><pre class="cout">${esc(out)}</pre></div>
      <p class="cwatch">${icon("bug", "sm")}<span><b>Watch out:</b> ${md(c.watch)}</span></p></div></details>`;
}
async function explainProblem(p, toHints){
  document.querySelector(".drawer-bg")?.remove(); document.querySelector(".drawer")?.remove();
  const bg = document.createElement("div"); bg.className = "drawer-bg";
  const dr = document.createElement("aside"); dr.className = "drawer explain"; dr.setAttribute("role", "dialog"); dr.setAttribute("aria-label", `Explain ${p.title} simply`); dr.tabIndex = -1;
  document.body.append(bg, dr);
  const close = () => { bg.remove(); dr.remove(); document.removeEventListener("keydown", esck); document.getElementById("pexplain")?.focus(); };
  const esck = e => { if(e.key === "Escape") close(); };
  document.addEventListener("keydown", esck); bg.onclick = close;
  dr.innerHTML = `<span class="muted">Loading the explanations…</span>`;
  const data = await loadConcepts(); if(!dr.isConnected) return;
  let lang = pbLang === "js" ? "js" : "python";
  const paint = () => {
    const ids = data?.byProblem?.[p.id] || [], cards = ids.map(i => data.cards[i]).filter(Boolean);
    const big = cards.filter(c => c.kind === "pattern" && c.id !== "big-o"), tools = cards.filter(c => c.kind === "block"), bigo = cards.find(c => c.id === "big-o");
    dr.innerHTML = `<div class="row" style="justify-content:space-between"><span class="eyebrow">${icon("info", "sm")} Explain it simply</span><button class="iconbtn" id="dx" aria-label="Close">${icon("x")}</button></div>
      <h2 class="h2">${esc(p.title)}</h2>
      <div class="seg" role="group" aria-label="Language for examples"><button type="button" data-xl="python" aria-pressed="${lang === "python"}">Python</button><button type="button" data-xl="js" aria-pressed="${lang === "js"}">JavaScript</button></div>
      <section class="xsec"><h3 class="h3">What the problem wants, in plain words</h3>${plainWords(p)}</section>
      ${!data ? `<p class="muted">The idea cards didn't load. Check your connection and open this again.</p>` : ""}
      ${big.length ? `<section class="xsec"><h3 class="h3">The big idea</h3><p class="muted xnote">The way of thinking that cracks this problem. Open a card to read more.</p>${big.map((c, i) => conceptCard(c, lang, i === 0)).join("")}</section>` : ""}
      ${tools.length ? `<section class="xsec"><h3 class="h3">Tools the solution uses</h3><p class="muted xnote">Every piece of ${lang === "js" ? "JavaScript" : "Python"} a solution to this problem needs, in the order you'll meet them. Skip any you already know.</p>${tools.map(c => conceptCard(c, lang, false)).join("")}</section>` : ""}
      ${bigo ? `<section class="xsec"><h3 class="h3">How fast is fast enough?</h3>${p.complexity ? `<p style="margin:0">A good solution here is <b>${esc(p.complexity)}</b>${p.constraints?.length ? `, given the limits: <code>${esc(p.constraints[0])}</code>` : ""}.</p>` : ""}${conceptCard(bigo, lang, false)}</section>` : ""}
      <div class="row"><button class="btn primary" id="xhints">${icon("bulb", "sm")}Now try the hints</button><button class="btn ghost" id="xdone">Back to the problem</button></div>`;
    dr.querySelector("#dx").onclick = close; dr.querySelector("#xdone").onclick = close;
    dr.querySelector("#xhints").onclick = () => { close(); toHints?.(); };
    dr.querySelectorAll("[data-xl]").forEach(b => b.onclick = () => { lang = b.dataset.xl; const top = dr.scrollTop; paint(); dr.scrollTop = top; });
  };
  paint(); dr.focus();
}

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
      <button type="button" class="explainbtn" id="pexplain" aria-haspopup="dialog">${icon("info")}<span><b>Explain it simply</b><small>What the problem wants, and every idea you need for it, in plain words</small></span>${icon("arrow","sm")}</button>
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
      ${(p.mistakes||[]).length?`<details class="hint"><summary>${icon("bug","sm")}Common mistakes on this problem</summary><div class="mist" style="margin-top:8px">${p.mistakes.map(x=>`<div class="mi"><div class="w"><span class="eyebrow">Tempting</span><p>${md(x.wrong)}</p></div><div class="r"><span class="eyebrow">Instead</span><p>${md(x.right)}</p></div></div>`).join("")}</div></details>`:""}
      <details class="hint"><summary>${icon("layers","sm")}The ${esc(cat.name)} pattern</summary><div class="prose">${cat.pattern.map(x=>`<p>${md(x)}</p>`).join("")}${codeBlock(cat.template)}</div>${cat.video?`<div style="display:grid;gap:8px;margin-top:10px"><span class="eyebrow">Watch: the pattern</span>${videoBlock({title:cat.name, video:cat.video, q:`${cat.name} coding interview pattern`})}</div>`:""}</details>
      <p class="muted" style="margin:0;font-size:.86rem">Want to see someone talk through it? <a href="${esc(ytSearch({q:`${p.title} leetcode explained`}))}" target="_blank" rel="noopener">Search YouTube for a ${esc(p.title)} walkthrough</a>, ideally after you've tried it.</p></div>`;
    else { const show=P.solved?.[p.id]||route.reveal;
      box.innerHTML = show ? `${p.takeaway?`<div class="recall" style="margin-bottom:12px"><span class="eyebrow">Key takeaway</span><p>${md(p.takeaway)}</p></div>`:""}<div class="prose" style="gap:12px">${p.editorial.map(x=>`<p>${md(x)}</p>`).join("")}<p><b>Complexity:</b> ${md(p.complexity)}</p></div>
        <div class="seg" style="margin:12px 0 8px"><button type="button" data-sl="py" aria-pressed="${key==="py"}">Python</button><button type="button" data-sl="js" aria-pressed="${key==="js"}">JavaScript</button></div><div id="solcode">${codeBlock(p.solution[key])}</div>`
      : `<div class="empty" style="display:grid;gap:12px;justify-items:center">${icon("lock","xl")}<b>The editorial unlocks when you solve it.</b><span>Struggling productively is where the learning happens. Try the hints first. Still stuck after 20 minutes? Reading a solution is fine, then close it and write it again from memory tomorrow.</span><button class="btn" id="reveal">Reveal anyway</button></div>`;
      box.querySelector("#reveal")?.addEventListener("click",()=>{ route.reveal=true; drawTab(); });
      box.querySelectorAll("[data-sl]").forEach(b=>b.onclick=()=>{ box.querySelectorAll("[data-sl]").forEach(x=>x.setAttribute("aria-pressed",x===b)); box.querySelector("#solcode").innerHTML=codeBlock(p.solution[b.dataset.sl]); }); }
    el.querySelector("#patlink")?.addEventListener("click",()=>{ pbFilter.cat=p.cat; });
    bindVideos(box);
  };
  drawTab();
  el.querySelector("#pexplain").onclick=()=>explainProblem(p, ()=>{ tab=route.tab="hints"; el.querySelectorAll("[data-tab]").forEach(x=>x.setAttribute("aria-selected",x.dataset.tab==="hints")); drawTab(); });
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
