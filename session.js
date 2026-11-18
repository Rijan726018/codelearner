"use strict";
/* ---------- focus sessions: a 50-minute timer with a break prompt, and a recap of what the session changed ----------
   The session lives in localStorage ("cl-focus"), so it survives reloads and new tabs on this device:
   {phase: "focus" | "break", start, end, began, snap}. snap is a snapshot of progress taken when the session began,
   and the recap is the difference between it and now. */
const FOCUS_MIN = 50, BREAK_MIN = 10, FKEY = "cl-focus";
const Focus = (() => {
  const read = () => { try{ return JSON.parse(localStorage.getItem(FKEY) || "null"); }catch(e){ return null; } };
  const write = s => { try{ s ? localStorage.setItem(FKEY, JSON.stringify(s)) : localStorage.removeItem(FKEY); }catch(e){} };
  let st = read(), timer = null, prompted = false;
  // what the recap compares against
  function snap(){
    return {xp: Game.stats().xp, secs: typeof Clock !== "undefined" ? Clock.stats().total : 0,
      solved: Object.keys(P.solved || {}), mastered: Object.keys(P.mastery || {}).filter(id => P.mastery[id]?.mastered),
      passes: typeof Mastery !== "undefined" ? Mastery.totalPasses() : 0, learned: Object.keys(P.learned || {}),
      debugged: Object.keys(P.debugged || {}), lessons: Object.keys(P.lessons || {}).length, steps: Object.keys(P.steps || {}).length,
      cards: Object.values(S.cards || {}).filter(c => c.b >= 1).length};
  }
  function start(min = FOCUS_MIN){ const now = Date.now(); st = {phase: "focus", start: now, end: now + min*60000, began: st?.began || now, snap: st?.snap || snap()}; prompted = false; write(st); tick(); UI.toast(`Focus session: ${min} minutes`, "Notifications stay on this page. You'll get a break prompt at the end.", "clock"); }
  function rest(min = BREAK_MIN){ const now = Date.now(); st = {...st, phase: "break", start: now, end: now + min*60000}; prompted = false; write(st); tick(); }
  function stop(){ st = null; write(null); pill()?.remove(); document.title = document.title.replace(/^\(\d+:\d\d\) /, ""); }
  const left = () => st ? Math.max(0, st.end - Date.now()) : 0;
  const mmss = ms => { const s = Math.ceil(ms/1000); return `${Math.floor(s/60)}:${String(s%60).padStart(2, "0")}`; };
  const pill = () => document.getElementById("focuspill");
  function tick(){
    clearInterval(timer); if(!st){ pill()?.remove(); return; }
    const draw = () => {
      if(!st){ clearInterval(timer); return; }
      let el = pill();
      if(!el){ el = document.createElement("div"); el.id = "focuspill"; el.setAttribute("role", "timer"); document.body.append(el);
        el.addEventListener("click", e => { const a = e.target.closest("[data-fx]")?.dataset.fx; if(a === "end") recap(true); else if(a === "skip") { if(st.phase === "break") start(); else prompt(); } }); }
      const ms = left(), f = st.phase === "focus";
      el.className = f ? "focus" : "break";
      el.innerHTML = `<span class="fp-dot"></span><b>${f ? "Focus" : "Break"} ${mmss(ms)}</b><button type="button" data-fx="skip" title="${f ? "Finish this block now" : "End the break and focus again"}">${f ? "Done" : "Back to work"}</button><button type="button" data-fx="end" title="End the session and see the recap">End</button>`;
      document.title = `(${mmss(ms)}) ` + document.title.replace(/^\(\d+:\d\d\) /, "");
      if(ms <= 0 && !prompted){ prompted = true; f ? prompt() : (UI.toast("Break's over", "Start the next 50 minutes when you're ready.", "clock", 8000), start()); }
    };
    draw(); timer = setInterval(draw, 1000);
  }
  function prompt(){ recap(false); }
  // the recap: shown when a focus block ends (with the break prompt) or when the session is ended
  async function recap(ending){
    if(!st) return;
    const s = st.snap, now = snap(), mins = Math.round((Date.now() - st.began) / 60000);
    const newSolved = now.solved.filter(id => !s.solved.includes(id)).map(id => PB.byId[id]).filter(Boolean);
    const newMastered = now.mastered.filter(id => !s.mastered.includes(id)).map(id => PB.byId[id]).filter(Boolean);
    const newDebug = now.debugged.filter(id => !s.debugged.includes(id)).length, learnedNew = now.learned.filter(id => !s.learned.includes(id));
    let cardsData = null; try{ cardsData = await loadConcepts(); }catch(e){}
    const names = ids => ids.map(id => cardsData?.cards?.[id]?.title?.split(":")[0]).filter(Boolean);
    const t = today(), dueTomorrow = (typeof Mastery !== "undefined" ? Object.values(P.mastery || {}).filter(r => r.due <= t + 1).length : 0),
      cardsTomorrow = Object.values(S.cards || {}).filter(c => c.d <= t + 1).length;
    const rows = [
      [`${fmtDur(now.secs - s.secs)}`, "practice measured", "clock"], [`+${(now.xp - s.xp).toLocaleString()}`, "XP earned", "zap"],
      [newSolved.length, `problem${newSolved.length === 1 ? "" : "s"} solved`, "braces"], [now.passes - s.passes, `review${now.passes - s.passes === 1 ? "" : "s"} passed from memory`, "refresh"],
      [newMastered.length, `problem${newMastered.length === 1 ? "" : "s"} newly mastered`, "star"], [newDebug, `bug${newDebug === 1 ? "" : "s"} fixed`, "bug"],
      [now.lessons - s.lessons, `lesson${now.lessons - s.lessons === 1 ? "" : "s"}`, "book"], [now.steps - s.steps, `bootcamp or project step${now.steps - s.steps === 1 ? "" : "s"}`, "cap"]
    ].filter((r, i) => i < 2 || +r[0] > 0);
    document.querySelectorAll(".drawer-bg,.drawer").forEach(x => x.remove());
    const bg = document.createElement("div"), dr = document.createElement("aside");
    bg.className = "drawer-bg"; dr.className = "drawer recap"; dr.setAttribute("role", "dialog"); dr.setAttribute("aria-label", "Session recap"); dr.tabIndex = -1;
    dr.innerHTML = `<div class="row" style="justify-content:space-between"><span class="eyebrow">${icon("clock","sm")} ${ending ? "Session recap" : `${FOCUS_MIN} minutes done`}</span><button class="iconbtn" id="dx" aria-label="Close">${icon("x")}</button></div>
      <h2 class="h2">${ending ? `${mins} minute${mins === 1 ? "" : "s"} well spent` : "Time for a break"}</h2>
      ${ending ? "" : `<p style="margin:0">Stand up, look at something far away, get some water. A ${BREAK_MIN}-minute break now makes the next block sharper. The recap below is what this session has done so far.</p>`}
      <div class="kpis">${rows.map(([v, l, i]) => `<div><b>${icon(i,"sm")} ${v}</b><span>${l}</span></div>`).join("")}</div>
      ${newSolved.length ? `<section class="xsec"><h3 class="h3">Solved</h3><div class="tags">${newSolved.map(p => `<span class="tag">${esc(p.title)}</span>`).join("")}</div></section>` : ""}
      ${newMastered.length ? `<section class="xsec"><h3 class="h3">Mastered</h3><div class="tags">${newMastered.map(p => `<span class="tag">${icon("star","sm")}${esc(p.title)}</span>`).join("")}</div></section>` : ""}
      ${learnedNew.length && names(learnedNew).length ? `<section class="xsec"><h3 class="h3">New concepts learned</h3><div class="tags">${names(learnedNew).map(n => `<span class="tag">${esc(n)}</span>`).join("")}</div></section>` : ""}
      <section class="xsec"><h3 class="h3">Tomorrow</h3><p style="margin:0">${dueTomorrow || cardsTomorrow ? `<b>${dueTomorrow}</b> problem review${dueTomorrow === 1 ? "" : "s"} and <b>${cardsTomorrow}</b> question card${cardsTomorrow === 1 ? "" : "s"} will be waiting. Start with them: they're what makes today stick.` : "Nothing is due tomorrow yet. Solve a problem or finish a lesson and it will come back for review."}</p></section>
      <div class="row">${ending ? `<button class="btn primary" id="rcnew">${icon("play","sm")}Start a new session</button><button class="btn ghost" id="rcdone">Done for now</button>`
        : `<button class="btn primary" id="rcbreak">${icon("clock","sm")}Start a ${BREAK_MIN}-minute break</button><button class="btn" id="rcmore">10 more minutes</button><button class="btn ghost" id="rcend">End the session</button>`}</div>`;
    const close = () => { bg.remove(); dr.remove(); document.removeEventListener("keydown", esck); };
    const esck = e => { if(e.key === "Escape") close(); };
    document.addEventListener("keydown", esck); bg.onclick = close; dr.querySelector("#dx").onclick = close;
    if(ending){ stop(); dr.querySelector("#rcnew").onclick = () => { close(); start(); }; dr.querySelector("#rcdone").onclick = close; }
    else { dr.querySelector("#rcbreak").onclick = () => { close(); rest(); }; dr.querySelector("#rcmore").onclick = () => { close(); start(10); }; dr.querySelector("#rcend").onclick = () => { close(); recap(true); }; }
    document.body.append(bg, dr); dr.focus();
  }
  if(st) setTimeout(tick, 0);
  return {start, rest, stop, recap, get state(){ return st; }, left};
})();
// the Today card and the menu entry
function focusCard(){
  const s = Focus.state;
  return `<section class="panel focuscard"><div class="row" style="justify-content:space-between"><span class="row" style="gap:8px;color:var(--accent)">${icon("clock")}<span class="eyebrow" style="color:inherit">Focus session</span></span>${s ? `<span class="pill acc">${s.phase === "focus" ? "Focusing" : "On a break"}</span>` : ""}</div>
    <p style="margin:0">${s ? "A session is running: the timer is in the corner. End it any time for a recap." : `${FOCUS_MIN} minutes on one thing, then a ${BREAK_MIN}-minute break. At the end you get a recap: what you solved and mastered, and what's due tomorrow.`}</p>
    <div class="row">${s ? `<button class="btn" data-focus="end">End and see the recap</button>` : `<button class="btn primary" data-focus="start">${icon("play","sm")}Start ${FOCUS_MIN} minutes</button>`}</div></section>`;
}
document.addEventListener("click", e => { const b = e.target.closest("[data-focus]"); if(!b) return; e.preventDefault();
  if(b.dataset.focus === "start"){ Focus.start(); if(route.v === "today") render(); } else { Focus.recap(true); } });
VIEWS.focus = el => { if(!Focus.state) Focus.start(); go({v:"today"}); };
SEARCH_SOURCES.push(() => [{t:"Focus session", sub:`${FOCUS_MIN}-minute timer with a break prompt and a recap`, kind:"Page", i:"clock", r:{v:"focus"}}]);
