"use strict";
/* ---------- practice clock: active time per day and section, plus time logged by hand, measured against 10,000 hours ----------
   Time counts only while the page is visible and you've typed, clicked or scrolled in the last two minutes (or code is running).
   P.time = {"YYYY-MM-DD": {learn, review, problems, bootcamp, build, editor}} in seconds; P.manual = [{id, day, min, cat, note}]. */
const CLOCK_CATS = {
  learn:{t:"Core lessons & exams", i:"map"}, review:{t:"Reviews", i:"refresh"}, problems:{t:"Problems", i:"braces"},
  bootcamp:{t:"Bootcamp", i:"cap"}, build:{t:"Build & Learn", i:"rocket"}, editor:{t:"Editor", i:"terminal"},
  offline:{t:"Logged by hand", i:"pen"}
};
const MANUAL_CATS = {coding:"Coding on my own", reading:"Reading or docs", course:"Another course or class", project:"Work or side project"};
const CLOCK_GOAL = 10000;
const CLOCK_MILESTONES = [[1,"First hour"],[10,"Ten hours"],[100,"A hundred hours"],[500,"Committed"],[1000,"A thousand hours"],[2500,"Serious practitioner"],[5000,"Halfway"],[10000,"Ten thousand hours"]];

const Clock = (() => {
  const IDLE = 120000, TICK = 5000, FLUSH = 60000;
  const VIEW_CAT = {map:"learn", lesson:"learn", exam:"learn", practice:"learn", projects:"learn", review:"review", problems:"problems", problem:"problems",
    bootcamp:"bootcamp", course:"bootcamp", build:"build", project:"build", make:"build", editor:"editor", code:"editor", playground:"editor"};
  let last = Date.now(), pending = {}, lastFlush = Date.now();
  const subs = new Set();
  const poke = () => { last = Date.now(); };
  ["keydown","pointerdown","pointermove","wheel","scroll","touchstart","input"].forEach(ev => addEventListener(ev, poke, {passive:true, capture:true}));
  const activeNow = () => document.visibilityState === "visible" && (Date.now() - last < IDLE || (typeof Runner !== "undefined" && Runner.busy));
  function flush(){
    lastFlush = Date.now();
    const cats = Object.keys(pending); if(!cats.length) return;
    const k = dayKey(today()); P.time = P.time || {}; const d = P.time[k] = P.time[k] || {};
    cats.forEach(c => { d[c] = (d[c]||0) + pending[c]; }); pending = {};
    save("p", true);
    if(Game.ready) Game.sync();   // unlocks the practice-hour badges
  }
  setInterval(() => {
    const cat = VIEW_CAT[route.v];
    if(cat && activeNow()){ pending[cat] = (pending[cat]||0) + TICK/1000; subs.forEach(f => { try{ f(); }catch(e){} }); }
    if(Date.now() - lastFlush >= FLUSH) flush();
  }, TICK);
  addEventListener("visibilitychange", () => { if(document.visibilityState === "hidden") flush(); });
  addEventListener("pagehide", flush);

  // per-day seconds, including what hasn't been flushed yet and manual entries
  function days(){
    const out = {};
    Object.entries(P.time || {}).forEach(([k, cats]) => { const d = out[k] = out[k] || {}; Object.entries(cats).forEach(([c, s]) => { d[c] = (d[c]||0) + (+s||0); }); });
    const tk = dayKey(today());
    Object.entries(pending).forEach(([c, s]) => { const d = out[tk] = out[tk] || {}; d[c] = (d[c]||0) + s; });
    (P.manual || []).forEach(m => { const d = out[m.day] = out[m.day] || {}; d.offline = (d.offline||0) + (+m.min||0)*60; });
    return out;
  }
  const sum = o => Object.values(o || {}).reduce((a, b) => a + b, 0);
  function stats(){
    const ds = days(), t = today(), tk = dayKey(t);
    const total = Object.values(ds).reduce((a, d) => a + sum(d), 0);
    const byCat = {}; Object.values(ds).forEach(d => Object.entries(d).forEach(([c, s]) => { byCat[c] = (byCat[c]||0) + s; }));
    const daySec = n => sum(ds[dayKey(n)]);
    let week = 0; const wd = (new Date(t*86400000).getUTCDay() + 6) % 7;   // Monday-based week
    for(let n = t - wd; n <= t; n++) week += daySec(n);
    let last30 = 0; for(let n = t - 29; n <= t; n++) last30 += daySec(n);
    const goalMin = P.goal || 60;
    let goalStreak = 0, n = t; if(daySec(n) < goalMin*60) n--;
    while(daySec(n) >= goalMin*60){ goalStreak++; n--; }
    // average over the last 30 days, or over the days since practice began if that's shorter
    const first = Object.keys(ds).filter(k => sum(ds[k]) > 0).sort()[0];
    const span = first ? Math.min(30, t - Math.round(Date.parse(first)/86400000) + 1) : 30;
    const perDay = last30 / Math.max(1, span), left = Math.max(0, CLOCK_GOAL*3600 - total);
    const finish = perDay > 0 ? new Date(Date.now() + left / perDay * 86400000) : null;
    return {total, hours: total/3600, today: daySec(t), week, last30, perDay, goalMin, goalStreak, finish, byCat, days: ds, todayKey: tk};
  }
  return {stats, flush, on(f){ subs.add(f); return () => subs.delete(f); }, get pending(){ return {...pending}; }};
})();

const fmtDur = s => { s = Math.round(s); if(s < 60) return s > 0 ? "<1 min" : "0 min"; const h = Math.floor(s/3600), m = Math.floor(s%3600/60); return h ? `${h} h${m ? ` ${m} min` : ""}` : `${m} min`; };
const fmtHours = s => { const h = s/3600; return h < 10 ? h.toFixed(1) : h < 1000 ? h.toFixed(0) : Math.round(h).toLocaleString(); };

/* ---------- the Today card ---------- */
function clockCard(){
  const c = Clock.stats(), pct = Math.min(100, 100*c.today/(c.goalMin*60));
  return `<section class="panel clockcard"><div class="row" style="justify-content:space-between"><span class="row" style="gap:8px;color:var(--accent)">${icon("clock")}<span class="eyebrow" style="color:inherit">Practice clock</span></span><button class="btn ghost sm" data-act="clock">Open the clock</button></div>
    <div class="clockrow"><div><b class="h2"><span class="gt" data-clock="total">${fmtHours(c.total)}</span> h</b><span class="muted"> of ${CLOCK_GOAL.toLocaleString()}</span></div>
      <div style="display:grid;gap:6px;min-width:0"><span class="muted" style="font-size:.88rem">Today: <b style="color:var(--ink)" data-clock="today">${fmtDur(c.today)}</b> of your ${fmtDur(c.goalMin*60)} goal</span><div class="bar"><i style="width:${pct}%"></i></div></div></div></section>`;
}
// keep the live numbers on screen ticking without a re-render
Clock.on(() => { const c = Clock.stats();
  document.querySelectorAll("[data-clock=total]").forEach(e => e.textContent = fmtHours(c.total));
  document.querySelectorAll("[data-clock=today]").forEach(e => e.textContent = fmtDur(c.today));
  document.querySelectorAll("[data-clock=hours]").forEach(e => e.textContent = (c.total/3600).toFixed(2)); });

/* ---------- the clock view ---------- */
function clockHeat(ds){
  const weeks = 53, t = today(); let s0 = t - (weeks*7-1); s0 -= (new Date(s0*86400000).getUTCDay() + 6) % 7;
  let cells = "";
  for(let d = s0; d <= t; d++){
    const s = Object.values(ds[dayKey(d)] || {}).reduce((a, b) => a + b, 0), m = s/60;
    const l = m === 0 ? 0 : m < 15 ? 1 : m < 45 ? 2 : m < 120 ? 3 : 4;
    cells += `<i data-l="${l}" class="${d===t?"today":""}" data-tip="${fmtDay(d)}: ${fmtDur(s)}"></i>`;
  }
  return `<div class="heat heat53" role="img" aria-label="Practice time over the last year">${cells}</div>
  <div class="legend">Less <i style="background:var(--sunk)"></i><i style="background:color-mix(in oklab,var(--accent) 30%,var(--sunk))"></i><i style="background:color-mix(in oklab,var(--accent) 55%,var(--sunk))"></i><i style="background:color-mix(in oklab,var(--accent) 78%,var(--sunk))"></i><i style="background:var(--accent)"></i> More · under 15 min, 45 min, 2 h, more</div>`;
}
function viewClock(el){
  Clock.flush();
  const c = Clock.stats(), pct = 100*c.total/(CLOCK_GOAL*3600);
  const next = CLOCK_MILESTONES.find(([h]) => c.hours < h) || CLOCK_MILESTONES[CLOCK_MILESTONES.length-1];
  const prev = [...CLOCK_MILESTONES].reverse().find(([h]) => c.hours >= h);
  const cats = Object.entries(CLOCK_CATS).map(([k, v]) => [k, v, c.byCat[k] || 0]).filter(x => x[2] > 0).sort((a, b) => b[2] - a[2]);
  const mx = Math.max(1, ...cats.map(x => x[2]));
  const yrs = c.finish ? (c.finish - Date.now())/31557600000 : null;
  const pace = c.total < 3600 ? "Your projection appears once you've practised for an hour. For scale: one hour a day reaches 10,000 hours in about 27 years, and three hours a day in about 9." :
    yrs <= 60 ? `At your recent pace of <b>${fmtDur(c.perDay)} a day</b>, you'll reach ${CLOCK_GOAL.toLocaleString()} hours around <b>${c.finish.getFullYear()}</b>, ${yrs < 1 ? "within a year" : `in about ${Math.round(yrs)} years`}. Three hours a day gets there in about 9 years: the pace of people who become world-class.`
    : `Your recent pace is <b>${fmtDur(c.perDay)} a day</b>. At that rate ${CLOCK_GOAL.toLocaleString()} hours is more than ${Math.floor(yrs/10)*10} years away, so build up gradually: one hour a day gets there in about 27 years, three hours in about 9.`;
  const recent = [...(P.manual || [])].sort((a, b) => b.day.localeCompare(a.day) || b.id.localeCompare(a.id)).slice(0, 8);
  const maxDay = dayKey(today());
  el.innerHTML = `<section class="head"><span class="eyebrow">The 10,000-hour clock</span><h1 class="h1">Practice clock</h1>
    <p class="lede">Mastery takes deliberate practice, and lots of it. This clock counts your active time on CodeLearner, section by section, and you can add practice you do anywhere else. Time only counts while the page is open and you've been active in the last two minutes, so leaving a tab open doesn't inflate it.</p></section>
  <section class="panel glow clockhero"><div class="clockbig"><b class="gt" data-clock="hours">${(c.total/3600).toFixed(2)}</b><span>hours of ${CLOCK_GOAL.toLocaleString()}</span></div>
    <div style="display:grid;gap:10px;min-width:0"><div class="bar big"><i style="width:${Math.max(pct, c.total ? 0.4 : 0)}%"></i></div>
      <span class="muted" style="font-size:.9rem">${pct.toFixed(pct < 1 ? 3 : 1)}% of the way${prev ? ` · reached <b style="color:var(--ink)">${esc(prev[1])}</b>` : ""} · next milestone: <b style="color:var(--ink)">${next[0].toLocaleString()} h, ${esc(next[1])}</b></span>
      <p class="muted" style="margin:0;font-size:.9rem">${pace}</p></div></section>
  <div class="stats">
    <div class="stat">${icon("clock")}<b data-clock="today">${fmtDur(c.today)}</b><span>today</span></div>
    <div class="stat">${icon("cal")}<b>${fmtDur(c.week)}</b><span>this week</span></div>
    <div class="stat">${icon("chart")}<b>${fmtDur(c.perDay)}</b><span>a day, recent average</span></div>
    <div class="stat">${icon("flame")}<b>${c.goalStreak}</b><span>days in a row at goal</span></div>
  </div>
  <div class="grid2">
    <section class="panel"><h2 class="h3">Daily goal</h2>
      <div class="lvcardx">${clockRing(c)}<div style="display:grid;gap:8px"><span class="muted">${fmtDur(c.today)} of ${fmtDur(c.goalMin*60)} today${c.today >= c.goalMin*60 ? " · goal met" : ""}</span>
        <div class="seg" role="group" aria-label="Daily goal">${[15,30,60,90,120,180].map(m => `<button type="button" data-goal="${m}" aria-pressed="${c.goalMin===m}">${m < 60 ? m+" min" : m/60+" h"}</button>`).join("")}</div></div></div></section>
    <section class="panel"><h2 class="h3">Where your hours go</h2>${cats.length ? `<div class="mast">${cats.map(([k, v, s]) => `<div class="r"><span>${esc(v.t)}</span><span class="t" data-tip="${fmtDur(s)}"><i style="width:${100*s/mx}%"></i></span><span class="n">${fmtHours(s)} h</span></div>`).join("")}</div>` : `<div class="empty">Nothing yet. Open a lesson, a problem or the editor and the clock starts on its own.</div>`}</section>
    <section class="panel" style="grid-column:1/-1"><h2 class="h3">The last year</h2>${clockHeat(c.days)}</section>
    <section class="panel"><h2 class="h3">Log practice from elsewhere</h2>
      <p class="muted" style="margin:0;font-size:.9rem">Coded in your own editor, read a book, took a class? Add it so the clock tells the whole story. Be honest: it's your number.</p>
      <form id="manual" class="mform">
        <label>Minutes<input class="field" id="m-min" type="number" min="5" max="720" step="5" value="30" required></label>
        <label>Date<input class="field" id="m-day" type="date" value="${maxDay}" max="${maxDay}" required></label>
        <label class="wide">What<select class="field" id="m-cat">${Object.entries(MANUAL_CATS).map(([k, t]) => `<option value="${k}">${esc(t)}</option>`).join("")}</select></label>
        <label class="wide">Note (optional)<input class="field" id="m-note" maxlength="80" placeholder="Read chapter 3 of Eloquent JavaScript"></label>
        <button class="btn primary">${icon("check","sm")}Add to my clock</button><span id="m-msg" class="muted" role="status" style="font-size:.88rem"></span>
      </form></section>
    <section class="panel"><h2 class="h3">Logged by hand</h2>${recent.length ? `<ul class="mlist">${recent.map(m => `<li><div><b>${fmtDur(m.min*60)} · ${esc(MANUAL_CATS[m.cat] || m.cat)}</b><span class="muted">${esc(m.day)}${m.note ? " · " + esc(m.note) : ""}</span></div><button type="button" class="btn ghost sm" data-delm="${esc(m.id)}" aria-label="Remove ${fmtDur(m.min*60)} on ${esc(m.day)}">Remove</button></li>`).join("")}</ul>` : `<div class="empty">Entries you add appear here.</div>`}</section>
  </div>`;
  el.querySelectorAll("[data-goal]").forEach(b => b.onclick = () => { P.goal = +b.dataset.goal; save("p", true); render(); });
  el.querySelector("#manual").onsubmit = e => {
    e.preventDefault();
    const min = Math.round(+el.querySelector("#m-min").value), day = el.querySelector("#m-day").value, msg = el.querySelector("#m-msg");
    if(!(min >= 1 && min <= 720)){ msg.textContent = "Enter between 1 and 720 minutes."; return; }
    if(!/^\d{4}-\d{2}-\d{2}$/.test(day) || day > maxDay){ msg.textContent = "Pick today or a past date."; return; }
    P.manual = P.manual || [];
    P.manual.push({id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6), day, min, cat: el.querySelector("#m-cat").value, note: el.querySelector("#m-note").value.trim().slice(0, 80)});
    save("p"); UI.toast(`Added ${fmtDur(min*60)}`, "Logged on your practice clock.", "clock", 2600); render();
  };
  el.querySelectorAll("[data-delm]").forEach(b => b.onclick = () => { P.manual = (P.manual || []).filter(m => m.id !== b.dataset.delm); save("p"); render(); });
}
function clockRing(c, size=110){
  const r = size/2 - 9, circ = 2*Math.PI*r, p = Math.min(1, c.today/(c.goalMin*60));
  return `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" role="img" aria-label="${Math.round(p*100)} percent of today's goal"><circle cx="${size/2}" cy="${size/2}" r="${r}" fill="none" stroke="var(--sunk)" stroke-width="10"/>
    <circle cx="${size/2}" cy="${size/2}" r="${r}" fill="none" stroke="var(--accent)" stroke-width="10" stroke-linecap="round" stroke-dasharray="${circ}" stroke-dashoffset="${circ*(1-p)}" transform="rotate(-90 ${size/2} ${size/2})"/>
    <text x="50%" y="50%" text-anchor="middle" dominant-baseline="central" style="font:800 20px var(--display);fill:var(--ink)">${Math.round(p*100)}%</text></svg>`;
}
VIEWS.clock = viewClock;
SEARCH_SOURCES.push(() => [{t:"Practice clock", sub:"Your hours toward 10,000, daily goal and time logged by hand", kind:"Page", i:"clock", r:{v:"clock"}}]);
