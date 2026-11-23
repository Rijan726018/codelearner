"use strict";
/* ---------- Build anything: say what you want to build, and Claude designs a Build & Learn project at your level ----------
   The server (/api/build on codebay.org, in the codebay repo) asks Claude for the project. Before the learner sees it,
   this browser runs every step through the site's own judge: each step's solution must pass all its checks, and the
   code the step starts from must fail at least one (so every step asks for something). Steps that don't hold go back
   to Claude with what failed, up to two repair rounds; if a later step still fails, the project is cut before it.
   Builds are kept in this browser ("cl-ai-builds") and, when signed in, in the account doc "aibuilds". */
const AIB = (() => {
  const KEY = "cl-ai-builds", API = /(^|\.)codebay\.org$/.test(location.hostname) ? "/api/build" : "https://codebay.org/api/build";
  const read = () => { try{ return JSON.parse(localStorage.getItem(KEY) || "{}"); }catch(e){ return {}; } };
  let all = read(), doc = null;
  function persist(){ try{ localStorage.setItem(KEY, JSON.stringify(all)); }catch(e){} if(doc) doc.set({builds: all}).catch(() => {}); }
  // the stored record -> a project the step engine (bootcamp.js) already knows how to run
  function toProject(rec){
    const lang = rec.lang, steps = [];
    rec.milestones.forEach((m, mi) => m.steps.forEach(s => { const k = steps.length;
      steps.push({id: `${rec.id}-${k}`, title: s.title, concept: s.concept, example: s.example || null, task: s.task, hint: s.hint || null, solution: s.solution, ms: mi,
        starter: k === 0 ? (s.starter || "") : null,   // later steps continue from the previous step's solution
        tests: (s.checks || []).map(c => lang === "python" ? {py: c.code, msg: c.msg} : lang === "js" ? {js: c.code, msg: c.msg} : {js: c.code, do: c.action || "", msg: c.msg})}); }));
    const p = {id: rec.id, ai: true, title: rec.title, tagline: rec.tagline, desc: rec.summary, skills: rec.skills, level: rec.level, lang, hue: rec.hue, icon: "sparkles", art: "AI",
      milestones: rec.milestones.map(m => ({title: m.title, goal: m.goal})), steps, idea: rec.idea, made: rec.made, trimmed: rec.trimmed};
    linkSteps(p); return p;
  }
  const register = rec => { const p = toProject(rec); PJ.byId[p.id] = p; return p; };
  Object.values(all).forEach(register);
  if(typeof ACCOUNT_HOOKS !== "undefined") ACCOUNT_HOOKS.push(async col => {
    if(!col){ doc = null; return; }
    doc = col.doc("aibuilds");
    try{ const s = await doc.get(); if(s.exists) all = {...(s.data()?.builds || {}), ...all}; Object.values(all).forEach(register); await doc.set({builds: all}); }catch(e){}
  });

  // what the learner already knows, in a few lines Claude can pitch the course to
  async function profile(){
    const g = Game.stats(), bits = [`${g.lessons} core lessons, ${g.solved} problems solved, ${g.steps} bootcamp/project steps passed, ${g.built} guided projects built.`];
    try{ const d = await loadConcepts(); if(d){ const lv = Mastery.levels(d), name = id => d.cards[id].title.split(":")[0];
      const m = Object.keys(lv).filter(id => lv[id].lvl === 3).map(name), pr = Object.keys(lv).filter(id => lv[id].lvl === 2).map(name);
      if(m.length) bits.push(`Mastered: ${m.slice(0, 20).join(", ")}.`); if(pr.length) bits.push(`Practiced: ${pr.slice(0, 20).join(", ")}.`); } }catch(e){}
    return bits.join(" ");
  }
  function suggestLevel(){ const g = Game.stats(); return g.solved >= 40 || g.built >= 4 ? "Advanced" : g.solved >= 8 || g.steps >= 60 || g.lessons >= 20 ? "Intermediate" : "Beginner"; }

  async function call(body){
    const token = await Account.idToken(); if(!token) throw new Error("Sign in with Google to build with AI.");
    let r; try{ r = await fetch(API, {method: "POST", headers: {"content-type": "application/json", authorization: `Bearer ${token}`}, body: JSON.stringify(body)}); }
    catch(e){ throw new Error("Couldn't reach the build server. Check your connection and try again."); }
    let j = null; try{ j = JSON.parse((await r.text()).trim() || "{}"); }catch(e){}
    if(!j || j.error || !j.project) throw new Error(j?.error || `The build server answered with an error (${r.status}).`);
    return j.project;
  }
  // every step: the solution passes all checks, and the starting code fails at least one
  async function verify(p, onStep){
    const fails = [];
    for(let k = 0; k < p.steps.length; k++){ const s = p.steps[k]; onStep?.(k, p.steps.length);
      if(!s.tests.length){ fails.push({step: k + 1, title: s.title, problem: "The step has no checks."}); continue; }
      const sol = await Judge.step(s, p.lang, s.solution), bad = sol.checks.filter(c => !c.ok);
      if(bad.length){ fails.push({step: k + 1, title: s.title, problem: `On the step's own solution these checks were false: ${bad.map(c => JSON.stringify(c.msg)).join("; ")}.${sol.stderr?.trim() ? ` The program printed this error: ${sol.stderr.trim().slice(-600)}` : ""}`}); continue; }
      const st = await Judge.step(s, p.lang, s.starter || "");
      if(st.checks.every(c => c.ok)) fails.push({step: k + 1, title: s.title, problem: "Every check already passes on the code this step starts from, so the step asks for nothing. Make at least one check depend on this step's new code."});
    }
    return fails;
  }
  function trimTo(raw, n){   // keep the first n steps
    let left = n; const ms = [];
    for(const m of raw.milestones){ if(left <= 0) break; const steps = m.steps.slice(0, left); left -= steps.length; ms.push({...m, steps}); }
    return {...raw, milestones: ms};
  }
  const count = raw => raw.milestones.reduce((a, m) => a + m.steps.length, 0);
  async function create(input, stage){
    const base = {...input, profile: await profile()};
    stage("design");
    let raw = await call(base), round = 0;
    const id = "ai-" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), hue = `hsl(${Math.floor(Math.random()*360)} 60% 55%)`;
    while(true){
      if(!raw?.milestones?.length || !count(raw)) throw new Error("Claude's project came back empty. Try again.");
      const rec = {...raw, lang: input.lang, id, hue, idea: input.idea, made: today()};
      const p = toProject(rec);
      stage("verify", 0, p.steps.length);
      const fails = await verify(p, (k, n) => stage("verify", k + 1, n));
      if(!fails.length){ all[id] = rec; persist(); return register(rec); }
      if(round >= 2){
        const first = Math.min(...fails.map(f => f.step)) - 1;
        if(first >= 3){ const cut = {...trimTo(rec, first), trimmed: true}; all[id] = cut; persist(); return register(cut); }
        throw new Error("Claude's steps didn't pass CodeBay's checks, even after two fixes. Try again, or describe the idea a little differently.");
      }
      round++; stage("repair", fails.length, round);
      raw = await call({...base, project: raw, failures: fails});
    }
  }
  function remove(id){ delete all[id]; delete PJ.byId[id]; persist(); }
  return {create, remove, suggestLevel, list: () => Object.keys(all).map(id => PJ.byId[id]).filter(Boolean).sort((a, b) => b.made - a.made)};
})();

/* ---------- the panel on the Build & Learn page ---------- */
const AIB_EXAMPLES = ["A digital clock", "A dice roller", "A budget tracker", "A quiz about space", "Rock, paper, scissors", "A tip calculator"];
let aibState = {idea: "", lang: null, level: null, busy: false};
function aibPanel(){
  const s = aibState, lang = s.lang || (pbLang === "js" ? "js" : "python"), level = s.level || AIB.suggestLevel(), mine = AIB.list(), signed = !!Account?.user;
  return `<section class="panel aib" id="aib">
    <span class="eyebrow">${icon("sparkles","sm")} Build anything · with Claude</span>
    <h2 class="h2">What do you want to build?</h2>
    <p class="muted" style="margin:0">Describe it in a few words. Claude designs a step-by-step project for it at your level, and CodeBay runs every step's checks against a working solution before you see it.</p>
    <div class="aibin"><input id="aiidea" class="pred" maxlength="300" placeholder="A clock that shows the time in three cities" value="${esc(s.idea)}" ${s.busy ? "disabled" : ""}>
      <button type="button" class="btn grad" id="aigo" ${s.busy ? "disabled" : ""}>${icon("sparkles","sm")}${signed ? "Build my course" : "Sign in to build"}</button></div>
    <div class="chips aibex">${AIB_EXAMPLES.map(x => `<button type="button" class="chip" data-aiex="${esc(x)}">${esc(x)}</button>`).join("")}</div>
    <div class="row" style="gap:14px">
      <div class="seg" role="group" aria-label="Language">${[["python","Python"],["js","JavaScript"],["web","Web page"]].map(([k,t]) => `<button type="button" data-ailang="${k}" aria-pressed="${lang===k}">${t}</button>`).join("")}</div>
      <div class="seg" role="group" aria-label="Level">${LEVELS_B.map(l => `<button type="button" data-ailvl="${l}" aria-pressed="${level===l}">${l}${l === AIB.suggestLevel() ? " ·&nbsp;you" : ""}</button>`).join("")}</div>
    </div>
    <div id="aistat" aria-live="polite"></div>
    ${mine.length ? `<div class="aibmine"><span class="eyebrow">Your AI builds</span>${mine.map(p => { const d = courseDone(p); return `<div class="aibrow"><button type="button" class="rqi" data-make="${p.id}" data-step="${Math.max(0, BC.stepIndex(p))}"><span class="pill">${esc(LANGNAME[p.lang] || p.lang)}</span><b>${esc(p.title)}</b><span class="muted">${p.level} · ${d}/${p.steps.length} steps${d === p.steps.length ? " · built" : ""}</span>${icon("arrow","sm")}</button><button type="button" class="iconbtn" data-aidel="${p.id}" aria-label="Delete ${esc(p.title)}">${icon("x","sm")}</button></div>`; }).join("")}</div>` : ""}
  </section>`;
}
function wireAib(root){
  const box = root.querySelector("#aib"); if(!box) return;
  const inp = box.querySelector("#aiidea"), stat = box.querySelector("#aistat");
  inp.oninput = () => { aibState.idea = inp.value; };
  inp.onkeydown = e => { if(e.key === "Enter") box.querySelector("#aigo").click(); };
  box.querySelectorAll("[data-aiex]").forEach(b => b.onclick = () => { aibState.idea = inp.value = b.dataset.aiex; inp.focus(); });
  box.querySelectorAll("[data-ailang]").forEach(b => b.onclick = () => { aibState.lang = b.dataset.ailang; box.querySelectorAll("[data-ailang]").forEach(x => x.setAttribute("aria-pressed", x === b)); });
  box.querySelectorAll("[data-ailvl]").forEach(b => b.onclick = () => { aibState.level = b.dataset.ailvl; box.querySelectorAll("[data-ailvl]").forEach(x => x.setAttribute("aria-pressed", x === b)); });
  box.querySelectorAll("[data-aidel]").forEach(b => b.onclick = () => { if(confirm("Delete this AI build and its steps? Your XP from it stays.")){ AIB.remove(b.dataset.aidel); render(); } });
  const say = (html, kind = "") => { stat.innerHTML = `<div class="aibstat ${kind}">${html}</div>`; };
  box.querySelector("#aigo").onclick = async () => {
    if(!Account?.user){ Account.signIn?.(); return; }
    const idea = inp.value.trim(); if(idea.length < 3){ inp.focus(); return; }
    const lang = aibState.lang || (pbLang === "js" ? "js" : "python"), level = aibState.level || AIB.suggestLevel();
    aibState.busy = true; inp.disabled = true; box.querySelector("#aigo").disabled = true;
    const t0 = Date.now(); let tick = null;
    const stage = (k, a, b) => { clearInterval(tick);
      if(k === "design"){ const draw = () => say(`<span class="spin"></span><span><b>Claude is designing your project.</b> It usually takes one to three minutes. <span class="muted">${Math.round((Date.now()-t0)/1000)} s</span></span>`); draw(); tick = setInterval(draw, 1000); }
      else if(k === "verify") say(`<span class="spin"></span><span><b>Checking every step against its solution</b>${b ? ` · ${a} of ${b}` : ""}${lang === "python" && !Runner.ready("python") ? " (starting Python)" : ""}</span>`);
      else if(k === "repair"){ const draw = () => say(`<span class="spin"></span><span><b>${a} step${a > 1 ? "s" : ""} didn't pass, so Claude is fixing ${a > 1 ? "them" : "it"}</b> (round ${b} of 2). <span class="muted">${Math.round((Date.now()-t0)/1000)} s</span></span>`); draw(); tick = setInterval(draw, 1000); } };
    try{
      const p = await AIB.create({idea, lang, level}, stage); clearInterval(tick);
      aibState = {idea: "", lang: aibState.lang, level: aibState.level, busy: false};
      UI.toast(`${p.title} is ready`, `${p.steps.length} steps, every one checked${p.trimmed ? " (shortened to the steps that passed)" : ""}.`, "sparkles", 6000);
      go({v: "make", id: p.id, step: 0});
    }catch(e){ clearInterval(tick); aibState.busy = false; inp.disabled = false; box.querySelector("#aigo").disabled = false; say(`${icon("x","sm")}<span>${esc(e.message || String(e))}</span>`, "err"); }
  };
}
