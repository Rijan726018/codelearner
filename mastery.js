"use strict";
/* ---------- Mastery: a warm-up prediction before each new problem, a spaced review queue for solved problems, and a level
   for every concept (Learned → Practiced → Mastered).
   P.predict[problemId] = {ok, d, c}: the warm-up was answered (c = the concept card it used).
   P.learned[cardId]    = day the learner worked through that concept's warm-up.
   P.mastery[problemId] = {stage, due, last, passes:[days], mastered:day|null, helped:n}: the review schedule.
   A review is the same problem re-solved from a blank editor with different example numbers. Passing it on or after its
   due day without opening hints, the explanation or the editorial is what earns Mastered and lengthens the gap. ---------- */
const PR_GAPS = [1, 3, 7, 14, 30, 60];
const MLEVELS = [["new","New"],["learned","Learned"],["practiced","Practiced"],["mastered","Mastered"]];
XPV.review = 25;   // each review passed from memory

const Mastery = {
  helped: {},   // problem id -> true once help was opened during this review (this page visit)
  rec(id){ return P.mastery?.[id] || null; },
  // problems solved before reviews existed join the queue, due the day after they were solved
  seed(){
    Object.entries(P.solved || {}).forEach(([id, v]) => {
      if(!PB.byId[id] || P.mastery?.[id]) return;
      const d = typeof v === "number" ? v : v?.d ?? today();
      P.mastery = P.mastery || {}; P.mastery[id] = {stage: 0, due: d + 1, last: d, passes: [], mastered: null};
    });
  },
  firstSolve(id){ P.mastery = P.mastery || {}; if(!P.mastery[id]) P.mastery[id] = {stage: 0, due: today() + 1, last: today(), passes: [], mastered: null}; },
  isDue(id){ const r = this.rec(id); return !!r && r.due <= today(); },
  due(){ this.seed(); return Object.entries(P.mastery || {}).filter(([id, r]) => PB.byId[id] && r.due <= today()).sort((a, b) => a[1].due - b[1].due).map(([id]) => PB.byId[id]); },
  dueOn(t){ return Object.entries(P.mastery || {}).filter(([id, r]) => PB.byId[id] && r.due === t).length; },
  mastered(id){ return !!this.rec(id)?.mastered; },
  // a review submitted and accepted: from memory (pass) or with help (back to tomorrow)
  finish(id, helped){
    const r = this.rec(id), t = today(); if(!r || r.due > t) return {early: true};
    r.last = t;
    if(helped){ r.stage = 0; r.due = t + 1; r.helped = (r.helped || 0) + 1; return {pass: false, next: 1}; }
    const first = !r.mastered;
    r.passes = [...(r.passes || []), t]; if(first) r.mastered = t;
    r.stage = Math.min((r.stage || 0) + 1, PR_GAPS.length - 1); r.due = t + PR_GAPS[r.stage];   // 1 → 3 → 7 → 14 → 30 → 60 days
    return {pass: true, first, next: PR_GAPS[r.stage]};
  },
  passesBetween(a, b){ let n = 0; Object.values(P.mastery || {}).forEach(r => (r.passes || []).forEach(d => { if(d >= a && d <= b) n++; })); return n; },
  totalPasses(){ return this.passesBetween(-Infinity, Infinity); },
  // the examples a review shows: other test cases than the usual examples, picked afresh each day
  reviewExamples(p){
    const seen = new Set((p.examples || []).map(e => JSON.stringify(e))), pool = (p.tests || []).filter(t => !seen.has(JSON.stringify(t)) && JSON.stringify(t).length < 400);
    if(!pool.length) return p.examples || [];
    const start = (today() * 31 + p.n) % pool.length, out = [];
    for(let k = 0; k < Math.min(2, pool.length); k++) out.push(pool[(start + k) % pool.length]);
    return out;
  },
  // a level for every concept card, from the problems that use it
  levels(data){
    const out = {};
    Object.keys(data.cards).forEach(id => out[id] = {lvl: 0, probs: [], solved: 0, mastered: 0});
    Object.entries(data.byProblem).forEach(([pid, ids]) => { if(!PB.byId[pid]) return;
      ids.forEach(c => { const x = out[c]; if(!x) return; x.probs.push(pid); if(P.solved?.[pid]) x.solved++; if(this.mastered(pid)) x.mastered++; }); });
    // Mastered needs two different problems re-solved from memory (or the only one), so the idea transfers, not one answer
    Object.entries(out).forEach(([id, x]) => { x.need = Math.min(2, x.probs.length); x.lvl = x.need && x.mastered >= x.need ? 3 : x.solved ? 2 : P.learned?.[id] ? 1 : 0; });
    return out;
  }
};
const lvlPill = (l, sm) => `<span class="lvl l${l}${sm?" sm":""}"><span class="dots"><i></i><i></i><i></i></span>${MLEVELS[l][1]}</span>`;

/* ---------- warm-up: the big idea, a worked example, and "what does this print?" before any code ---------- */
const normOut = s => String(s || "").replace(/[‘’']/g, '"').replace(/[“”]/g, '"').split(/\r?\n/).map(l => l.trim().replace(/\s+/g, " ")).filter(Boolean).join("\n");
function pickWarmCard(data, p){
  const ids = data?.byProblem?.[p.id] || [], cards = ids.map(i => data.cards[i]).filter(c => c && c.id !== "big-o");
  return cards.find(c => c.kind === "pattern" && !P.learned?.[c.id]) || cards.find(c => !P.learned?.[c.id]) || cards.find(c => c.kind === "pattern") || cards[0] || null;
}
async function warmUp(host, p, lang, onDone){
  const data = await loadConcepts(); if(!host.isConnected) return;
  const c = pickWarmCard(data, p); if(!c){ onDone(); return; }
  const L = lang === "js" ? "js" : "py", code = c[L], out = c[L + "_out"], lvl = Mastery.levels(data)[c.id]?.lvl || 0;
  host.innerHTML = `<section class="panel warm" aria-labelledby="wmh">
    <div class="row" style="justify-content:space-between"><span class="eyebrow">${icon("bulb","sm")} Warm-up · about a minute</span>${lvlPill(lvl, true)}</div>
    <h2 class="h3" id="wmh">${c.kind==="pattern"?"The big idea":"A tool you'll need"}: ${esc(c.title)}</h2>
    <p class="wkid">${md(c.kid)}</p>
    <div class="prose">${c.how.map(x => `<p>${md(x)}</p>`).join("")}</div>
    <div class="cex"><span class="eyebrow">Worked example · ${L==="js"?"JavaScript":"Python"}</span>${codeBlock(code, null, L==="js"?"javascript":"python")}</div>
    <label class="wq" for="wans"><b>Before you write anything: what does this print?</b><span class="muted">Trace it line by line in your head, then type the output exactly as it would appear.</span></label>
    <textarea id="wans" class="pred" rows="${Math.min(6, out.split("\n").length + 1)}" spellcheck="false" autocomplete="off" placeholder="Your prediction"></textarea>
    <div class="row"><button type="button" class="btn primary" id="wchk">${icon("check","sm")}Check my prediction</button><button type="button" class="btn ghost" id="wshow">I'm not sure, show me</button><button type="button" class="btn ghost sm" id="wskip" style="margin-left:auto">Skip the warm-up</button></div>
    <div id="wres" aria-live="polite"></div></section>`;
  const ans = host.querySelector("#wans"), res = host.querySelector("#wres");
  const finish = ok => {
    P.predict = P.predict || {}; P.predict[p.id] = {ok, d: today(), c: c.id};
    P.learned = P.learned || {}; if(!P.learned[c.id]) P.learned[c.id] = today();
    save("p");
    res.innerHTML = `<div class="wfb ${ok?"ok":"no"}">${ok?`<b>${icon("checkc","sm")} Right.</b> You traced it correctly, so you understand how ${esc(c.title.toLowerCase())} behaves.`
        :`<b>${ans.value.trim()?"Not quite.":"Here's the answer."}</b> It prints:<pre class="cout">${esc(out)}</pre>Find the line where your trace and the real output part ways: that's the part to reread.`}
      <p class="cwatch">${icon("bug","sm")}<span><b>Watch out:</b> ${md(c.watch)}</span></p>
      <button type="button" class="btn grad" id="wgo">${icon("play","sm")}Now solve ${esc(p.title)}</button></div>`;
    host.querySelectorAll("#wchk,#wshow").forEach(b => b.disabled = true); ans.readOnly = true;
    res.querySelector("#wgo").onclick = () => { host.innerHTML = ""; onDone(); };
    res.querySelector("#wgo").focus();
  };
  host.querySelector("#wchk").onclick = () => { if(!ans.value.trim()){ ans.focus(); return; } finish(normOut(ans.value) === normOut(out)); };
  host.querySelector("#wshow").onclick = () => finish(false);
  host.querySelector("#wskip").onclick = () => { host.innerHTML = ""; onDone(); };
  ans.addEventListener("keydown", e => { if(e.key === "Enter" && (e.metaKey || e.ctrlKey)) host.querySelector("#wchk").click(); });
}

/* ---------- the review queue, as a panel for the Problems and Review pages ---------- */
function reviewQueueHTML(compact){
  const due = Mastery.due(), tomorrow = Mastery.dueOn(today() + 1);
  if(!due.length) return compact ? "" : `<section class="panel rq"><div class="sec-h"><h2 class="h3">${icon("refresh")} Problem reviews</h2><button type="button" class="btn ghost sm" data-act="concepts">${icon("layers","sm")}Your concepts</button></div>
    <p class="muted" style="margin:0">${Object.keys(P.mastery||{}).length?`Nothing due today.${tomorrow?` ${tomorrow} problem${tomorrow>1?"s":""} come${tomorrow>1?"":"s"} back tomorrow.`:""}`:"Solve a problem and it comes back tomorrow, then after 3 days, a week, two weeks and a month, each time from a blank editor."}</p></section>`;
  return `<section class="panel rq glow"><div class="sec-h"><h2 class="h3">${icon("refresh")} ${due.length} problem${due.length>1?"s":""} to re-solve from memory</h2><button type="button" class="btn ghost sm" data-act="concepts">${icon("layers","sm")}Your concepts</button></div>
    <p class="muted" style="margin:0">Blank editor, different example numbers, no hints. Pass without help and the problem is <b>Mastered</b>, and the next gap grows (${PR_GAPS.join(" → ")} days).</p>
    <div class="rqlist">${due.slice(0, compact ? 3 : 8).map(p => { const r = Mastery.rec(p.id); return `<button type="button" class="rqi" data-review="${p.id}"><span class="diff ${p.difficulty}">${p.difficulty}</span><b>${esc(p.title)}</b><span class="muted">${r.mastered?"Mastered · keep it":"Solved"} · ${r.due < today() ? `overdue ${today()-r.due} d` : "due today"}</span>${icon("arrow","sm")}</button>`; }).join("")}</div>
    ${due.length > (compact?3:8) ? `<span class="muted" style="font-size:.86rem">And ${due.length - (compact?3:8)} more. Do a few a day: they'll wait.</span>` : ""}</section>`;
}
document.addEventListener("click", e => { const b = e.target.closest("[data-review]"); if(b){ e.preventDefault(); go({v:"problem", id:b.dataset.review, review:1}); } });

/* ---------- Concepts: every idea card with its level, and the problems that use it ---------- */
let conceptFilter = "all";
async function viewConcepts(el){
  el.innerHTML = `<div class="loading">Loading your concepts…</div>`;
  const data = await loadConcepts(); if(route.v !== "concepts") return;
  if(!data || !PB.list.length){ el.innerHTML = `<div class="empty">The concepts didn't load. Reload the page to try again.</div>`; return; }
  const lv = Mastery.levels(data), cards = Object.values(data.cards), count = l => cards.filter(c => lv[c.id].lvl === l).length;
  const group = (kind, title, blurb) => { const cs = cards.filter(c => c.kind === kind && (conceptFilter === "all" || lv[c.id].lvl === +conceptFilter)).sort((a, b) => lv[b.id].lvl - lv[a.id].lvl || lv[b.id].probs.length - lv[a.id].probs.length);
    return cs.length ? `<section style="display:grid;gap:12px"><div class="sec-h"><h2 class="h2">${title}</h2><span class="muted" style="font-size:.9rem">${blurb}</span></div>
      <div class="cgrid">${cs.map(c => { const x = lv[c.id]; return `<button type="button" class="ctile l${x.lvl}" data-concept="${c.id}"><span class="row" style="justify-content:space-between;gap:8px"><b>${esc(c.title)}</b>${lvlPill(x.lvl, true)}</span><span class="muted">${md(c.kid)}</span>
        <span class="cmeter" aria-label="${x.mastered} mastered and ${x.solved} solved of ${x.probs.length} problems"><i style="width:${100*x.mastered/Math.max(1,x.probs.length)}%" class="m"></i><i style="width:${100*(x.solved-x.mastered)/Math.max(1,x.probs.length)}%"></i></span>
        <span class="muted" style="font:500 11px var(--mono)">${x.mastered} mastered · ${x.solved} solved · ${x.probs.length} problems</span></button>`; }).join("")}</div></section>` : ""; };
  el.innerHTML = `<section class="head"><span class="eyebrow">Mastery</span><h1 class="h1">Your <span class="gt">concepts</span></h1>
    <p class="lede">Every idea the problem set uses, and how well you know it. <b>Learned</b>: you worked through its warm-up. <b>Practiced</b>: you solved a problem that uses it. <b>Mastered</b>: you re-solved two different problems that use it later, from a blank editor, without any help.</p></section>
    <div class="kpis">${[3,2,1,0].map(l => `<div><b>${count(l)}</b><span>${MLEVELS[l][1].toLowerCase()}</span></div>`).join("")}<div><b>${Mastery.due().length}</b><span>reviews due today</span></div></div>
    ${reviewQueueHTML(true)}
    <div class="chips" role="group" aria-label="Show">${[["all","All"],["3","Mastered"],["2","Practiced"],["1","Learned"],["0","New"]].map(([k,t]) => `<button type="button" class="chip" data-cf="${k}" aria-pressed="${conceptFilter===k}">${t}</button>`).join("")}</div>
    ${group("pattern", "Big ideas", "The ways of thinking that crack problems")}${group("block", "Tools", "The pieces of Python and JavaScript you build solutions from")}`;
  el.querySelectorAll("[data-cf]").forEach(b => b.onclick = () => { conceptFilter = b.dataset.cf; render(); });
  el.querySelectorAll("[data-concept]").forEach(b => b.onclick = () => conceptDrawer(data, lv, b.dataset.concept));
}
function conceptDrawer(data, lv, id){
  document.querySelectorAll(".drawer-bg,.drawer").forEach(x => x.remove());
  const c = data.cards[id], x = lv[id], bg = document.createElement("div"), dr = document.createElement("aside");
  bg.className = "drawer-bg"; dr.className = "drawer explain"; dr.setAttribute("role", "dialog"); dr.setAttribute("aria-label", c.title); dr.tabIndex = -1;
  const st = pid => Mastery.mastered(pid) ? `<span class="pill ok">${icon("star","sm")}Mastered</span>` : Mastery.isDue(pid) ? `<span class="pill acc">Review due</span>` : P.solved?.[pid] ? `<span class="pill">Solved</span>` : "";
  const next = x.lvl === 3 ? "Mastered. Its problems keep coming back at growing gaps so it stays that way." : x.lvl === 2 ? `Practiced. ${x.mastered ? "One problem re-solved from memory; one more and this is mastered." : "When these problems come up for review, re-solve two of them without hints to master this."}` : x.lvl === 1 ? "Learned. Solve one of the problems below to practise it." : "New. Open any problem below: its warm-up starts with the big idea.";
  dr.innerHTML = `<div class="row" style="justify-content:space-between"><span class="eyebrow">${icon("layers","sm")} Concept</span><button class="iconbtn" id="dx" aria-label="Close">${icon("x")}</button></div>
    <h2 class="h2">${esc(c.title)}</h2><div class="row">${lvlPill(x.lvl)}<span class="muted" style="font-size:.9rem">${next}</span></div>
    ${conceptCard(c, pbLang === "js" ? "js" : "python", true)}
    <section class="xsec"><h3 class="h3">Problems that use it (${x.probs.length})</h3><div class="rqlist">${x.probs.map(pid => PB.byId[pid]).sort((a, b) => a.n - b.n).map(p => `<button type="button" class="rqi" data-problem="${p.id}"><span class="diff ${p.difficulty}">${p.difficulty}</span><b>${esc(p.title)}</b>${st(p.id)}${icon("arrow","sm")}</button>`).join("")}</div></section>`;
  const close = () => { bg.remove(); dr.remove(); document.removeEventListener("keydown", esck); };
  const esck = e => { if(e.key === "Escape") close(); };
  bg.onclick = close; document.addEventListener("keydown", esck); dr.querySelector("#dx").onclick = close;
  dr.querySelectorAll("[data-problem]").forEach(b => b.addEventListener("click", close));
  document.body.append(bg, dr); dr.focus();
}
VIEWS.concepts = viewConcepts;
SEARCH_SOURCES.push(() => [{t:"Your concepts", sub:"Mastery level of every idea, and problem reviews due", kind:"Page", i:"layers", r:{v:"concepts"}}]);

/* ---------- hint ladder: a nudge, then the idea behind it, then part of the code ----------
   P.helps[problemId] = {r, d}: the highest rung opened (1 nudge, 2 idea, 3 code, 4 editorial) and when. A first solve
   with no rung opened is a clean solve and earns a bonus of half the problem's XP; in a review, any rung means help. */
const RUNGS = [["A nudge","Just enough to get you moving."],["The idea behind it","The pattern this problem needs, explained."],["Part of the code","The opening of one solution. You write the rest."]];
const cleanBonus = p => Math.round((XPV[p?.difficulty] || 0) / 2);
const Help = {
  rung(id){ return P.helps?.[id]?.r || 0; },
  use(id, r){ P.helps = P.helps || {}; const h = P.helps[id]; if(!h || h.r < r){ P.helps[id] = {r, d: today()}; save("p", true); } Mastery.helped[id] = true; },
  clean(id){ return !this.rung(id); }
};
// the first ~40% of a reference solution's body, then a "your turn" line
function partialCode(src, lang){
  const lines = src.split("\n"), py = lang !== "js", isBody = (l, i) => i > 0 && l.trim() && !/^\s*[}\])]*;?\s*$/.test(l) && !/^\s*(#|\/\/)/.test(l);
  const body = lines.map((l, i) => ({l, i})).filter(x => isBody(x.l, x.i));
  if(body.length < 2) return lines.slice(0, 1).join("\n") + (py ? "\n    # ... the rest is yours" : "\n  // ... the rest is yours\n}");
  const cut = body[Math.max(0, Math.ceil(body.length * 0.4) - 1)].i, nextB = body.find(x => x.i > cut), ind = (nextB ? nextB.l : body[body.length - 1].l).match(/^\s*/)[0];
  return lines.slice(0, cut + 1).join("\n") + `\n${ind}${py ? "# ... the rest is yours" : "// ... the rest is yours"}`;
}
async function hintLadder(host, p, lang, onUse){
  const L = lang === "js" ? "js" : "py", data = await loadConcepts(); if(!host.isConnected) return;
  const big = (data?.byProblem?.[p.id] || []).map(i => data.cards[i]).find(c => c && c.kind === "pattern" && c.id !== "big-o");
  const draw = () => { const r = Help.rung(p.id);
    const body = k => k === 0 ? `<p>${md(p.hints[0] || "")}</p>`
      : k === 1 ? `${p.hints[1] ? `<p>${md(p.hints[1])}</p>` : ""}${big ? conceptCard(big, L === "js" ? "js" : "python", true) : ""}`
      : `<p class="muted" style="margin:0">The opening of one solution in ${L === "js" ? "JavaScript" : "Python"}. Finish it in your own words: don't just copy it.</p>${codeBlock(partialCode(p.solution[L], L), null, L === "js" ? "javascript" : "python")}`;
    host.innerHTML = `<div class="ladder">${r ? "" : `<p class="lnote">${icon("star","sm")} Solve it with no hints for a <b>clean-solve bonus of +${cleanBonus(p)} XP</b>. Hints never block you: open them in order, only as far as you need.</p>`}
      ${RUNGS.map(([t, s], k) => { const open = r > k, next = r === k;
        return `<div class="rung ${open ? "open" : next ? "next" : "locked"}"><div class="rh"><span class="rn">${k + 1}</span><span><b>${t}</b><small>${s}</small></span>${next ? `<button type="button" class="btn sm" data-rung="${k + 1}">Show ${t.toLowerCase()}</button>` : !open ? `<span class="muted" style="font-size:.8rem">after step ${k}</span>` : ""}</div>${open ? `<div class="rb prose">${body(k)}</div>` : ""}</div>`; }).join("")}
      ${r >= 3 ? `<p class="muted" style="margin:0;font-size:.88rem">Still stuck? The <b>Editorial</b> tab has the whole solution and why it works. Read it, close it, then write it again from memory.</p>` : ""}</div>`;
    host.querySelectorAll("[data-rung]").forEach(b => b.onclick = () => { Help.use(p.id, +b.dataset.rung); onUse?.(); draw(); });
  };
  draw();
}

/* ---------- debug challenges: a solved problem's reference solution with one bug planted (tools/build_debug.mjs) ----------
   P.debugged[problemId] = {d, lang, clean}. Unlocked once the problem is solved, so the code never spoils the problem. */
XPV.debug = 20;
let DEBUG_DATA = null, DEBUG_SYNC;   // DEBUG_SYNC: the loaded data, for pages that render synchronously
const loadDebug = () => DEBUG_DATA || (DEBUG_DATA = fetch("data/debug.json").then(r => r.ok ? r.json() : null).catch(() => null).then(d => (DEBUG_SYNC = d)));
const Debug = {
  get(data, id, L){ return data?.problems?.[id]?.[L] || null; },
  fixed(id){ return !!P.debugged?.[id]; },
  between(a, b){ return Object.values(P.debugged || {}).filter(v => v?.d >= a && v?.d <= b).length; },
  available(data, L){ return PB.list.filter(p => P.solved?.[p.id] && !this.fixed(p.id) && this.get(data, p.id, L)); }
};
async function debugPanel(host){
  const data = await loadDebug(); if(!host.isConnected) return;
  if(!data){ host.remove(); return; }
  const L = pbLang === "js" ? "js" : "py", av = Debug.available(data, L), total = Object.keys(data.problems).length, fixed = Object.keys(P.debugged || {}).length;
  host.innerHTML = `<div class="sec-h"><h2 class="h3">${icon("bug")} Debug challenges</h2><span class="muted" style="font-size:.86rem">${fixed} fixed · ${total} in all</span></div>
    <p class="muted" style="margin:0">Working code with one bug planted in it. Run it, read the failing test, find the line and fix it. Each one unlocks when you've solved that problem, so it never gives an answer away. <b>+${XPV.debug} XP</b> each.</p>
    ${av.length ? `<div class="rqlist">${av.slice(0, 4).map(p => `<button type="button" class="rqi" data-debug="${p.id}"><span class="diff ${p.difficulty}">${p.difficulty}</span><b>${esc(p.title)}</b><span class="muted">${esc(Debug.get(data, p.id, L).kind)}</span>${icon("arrow","sm")}</button>`).join("")}</div>${av.length > 4 ? `<span class="muted" style="font-size:.86rem">${av.length - 4} more ready.</span>` : ""}`
      : `<p style="margin:0">${fixed ? "You've fixed every challenge you've unlocked. Solve more problems to unlock more." : "Solve any problem to unlock its debug challenge."}</p>`}`;
}
document.addEventListener("click", e => { const b = e.target.closest("[data-debug]"); if(b){ e.preventDefault(); go({v:"problem", id:b.dataset.debug, debug:1}); } });
