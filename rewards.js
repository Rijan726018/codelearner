"use strict";
/* ================= REWARDS: coins, daily & weekly challenges, streak freezes, a shop and a leaderboard =================
   Coins are derived from real progress, like XP, so repeating something can't farm them: every lesson, exam, problem,
   step, project, course, path, badge, level, practice day and streak milestone pays once. Completed challenges are
   recorded in P.claimed ({key: coins}) and purchases in P.buys ([{id, item, price, day}]), so the balance is
   earned minus spent and merges cleanly across devices (maps are unioned, lists are unioned by id).
   Challenges are computed from the day each piece of progress was recorded (P.lessons[id] = day number,
   P.solved[id].d, P.steps[id], P.ms[k], P.exams[m].last, P.qa[dayKey], practice-clock seconds). */
const COINV = {lesson:10, exam:50, milestone:10, Easy:15, Medium:30, Hard:60, step:5, node:5, project:100, course:100, path:250, badge:25, day:5};
const STREAK_BONUS = [[3,20],[7,60],[14,150],[30,400],[60,800],[100,1500]];
const levelCoins = lv => 5*(lv-1)*(lv+2);   // reaching level L pays 10 × L coins, summed over every level reached
const DAY_BONUS = 50, WEEK_BONUS = 250;     // for finishing all of a day's or a week's challenges

const DAILY = [
  {id:"lesson",   t:"Finish a core lesson",                         i:"book",    goal:1,  coins:30, v:d=>d.lessons, go:()=>({v:"map"})},
  {id:"lessons2", t:"Finish 2 core lessons",                        i:"book",    goal:2,  coins:60, v:d=>d.lessons, go:()=>({v:"map"})},
  {id:"solve",    t:"Get a problem accepted",                       i:"braces",  goal:1,  coins:40, v:d=>d.solved,  go:()=>({v:"problems"})},
  {id:"pod",      t:"Solve the problem of the day",                 i:"target",  goal:1,  coins:50, v:d=>d.pod,     go:()=>{ const p=PB.daily?.(); return p?{v:"problem", id:p.id}:{v:"problems"}; }},
  {id:"steps",    t:"Pass 3 bootcamp or Build steps",               i:"cap",     goal:3,  coins:30, v:d=>d.steps,   go:()=>({v:"bootcamp"})},
  {id:"answers",  t:"Answer 10 questions in lessons or reviews",    i:"refresh", goal:10, coins:25, v:d=>d.qa,      go:()=>({v:"review"})},
  {id:"sure",     t:"Get 5 answers right that you marked Certain",  i:"award",   goal:5,  coins:30, v:d=>d.sure,    go:()=>({v:"review"})},
  {id:"time",     t:"Practise for 30 minutes",                      i:"clock",   goal:30, coins:30, v:d=>Math.floor(d.sec/60), unit:"min", go:()=>({v:"clock"})},
  {id:"ms",       t:"Check off a project milestone",                i:"rocket",  goal:1,  coins:25, v:d=>d.ms,      go:()=>({v:"projects"})}
];
const WEEKLY = [
  {id:"days",    t:"Practise on 5 different days",     i:"flame",  goal:5,    coins:150, v:w=>w.days, fixed:true, go:()=>({v:"today"})},
  {id:"lessons", t:"Finish 5 core lessons",            i:"book",   goal:5,    coins:150, v:w=>w.lessons, go:()=>({v:"map"})},
  {id:"solve",   t:"Solve 5 problems",                 i:"braces", goal:5,    coins:200, v:w=>w.solved,  go:()=>({v:"problems"})},
  {id:"hours",   t:"Practise for 5 hours",             i:"clock",  goal:300,  coins:200, v:w=>Math.floor(w.sec/60), unit:"min", go:()=>({v:"clock"})},
  {id:"exam",    t:"Pass a module exam",               i:"lock",   goal:1,    coins:150, v:w=>w.exams,   go:()=>({v:"map"})},
  {id:"steps",   t:"Pass 15 bootcamp or Build steps",  i:"cap",    goal:15,   coins:150, v:w=>w.steps,   go:()=>({v:"bootcamp"})},
  {id:"xp",      t:"Earn 1,000 XP",                    i:"zap",    goal:1000, coins:200, v:w=>w.xp,      go:()=>({v:"today"})}
];
const SHOP = [
  {id:"freeze", kind:"freeze", t:"Streak freeze", d:"Covers one missed day so your streak survives. Used automatically the day after you miss. You can hold 3.", price:150, i:"shield", max:3},
  {id:"accent-ocean",  kind:"accent", v:"ocean",  t:"Ocean accent",  d:"Blue buttons, links and highlights.",   price:300, sw:"#0284c7"},
  {id:"accent-forest", kind:"accent", v:"forest", t:"Forest accent", d:"Green buttons, links and highlights.",  price:300, sw:"#059669"},
  {id:"accent-sunset", kind:"accent", v:"sunset", t:"Sunset accent", d:"Orange buttons, links and highlights.", price:300, sw:"#ea580c"},
  {id:"accent-rose",   kind:"accent", v:"rose",   t:"Rose accent",   d:"Pink buttons, links and highlights.",   price:300, sw:"#db2777"},
  {id:"accent-gold",   kind:"accent", v:"gold",   t:"Gold accent",   d:"Gold buttons, links and highlights. Needs level 10.", price:600, sw:"#ca8a04", minLevel:10},
  {id:"title-bug",     kind:"title", v:"Bug Hunter",      t:"Title: Bug Hunter",      d:"Shown on your profile and the leaderboard.", price:200, i:"bug"},
  {id:"title-owl",     kind:"title", v:"Night Owl",       t:"Title: Night Owl",       d:"Shown on your profile and the leaderboard.", price:200, i:"moon"},
  {id:"title-bird",    kind:"title", v:"Early Bird",      t:"Title: Early Bird",      d:"Shown on your profile and the leaderboard.", price:200, i:"sun"},
  {id:"title-crusher", kind:"title", v:"Problem Crusher", t:"Title: Problem Crusher", d:"Needs 25 solved problems.", price:400, i:"braces", need:s=>s.solved>=25, needT:"Solve 25 problems"},
  {id:"title-wizard",  kind:"title", v:"Code Wizard",     t:"Title: Code Wizard",     d:"Needs level 10.", price:600, i:"sparkles", minLevel:10},
  {id:"title-grand",   kind:"title", v:"Grandmaster",     t:"Title: Grandmaster",     d:"Needs level 20.", price:1500, i:"trophy", minLevel:20}
];
const COIN_SVG = `<svg class="coin" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.5"/><circle cx="12" cy="12" r="6.5"/><path d="M12 8.5v7M10 10.2h3.1a1.4 1.4 0 0 1 0 2.8h-2.2a1.4 1.4 0 0 0 0 2.8H14"/></svg>`;

const Rewards = (() => {
  const wkStart = t => t - (new Date(t*86400000).getUTCDay() + 6) % 7;     // Monday
  const dayOf = v => typeof v === "number" ? v : v && typeof v === "object" && typeof v.d === "number" ? v.d : null;
  const hash = s => { let h = 2166136261; for(const c of s){ h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; };
  const seeded = seed => () => { seed = (seed + 0x6D2B79F5) | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const uid = () => Math.random().toString(36).slice(2, 10) + Date.now().toString(36);

  // progress recorded between day numbers a and b, inclusive
  function between(a, b){
    const inR = v => { const d = dayOf(v); return d != null && d >= a && d <= b; };
    const pb = PB.byId || {}; let solved = 0, sxp = 0;
    Object.entries(P.solved || {}).forEach(([id, v]) => { if(inR(v)){ solved++; sxp += XPV[pb[id]?.difficulty] || 0; } });
    const lessons = Object.entries(P.lessons || {}).filter(([k, v]) => D.lessons[k] && inR(v)).length;
    const steps = Object.values(P.steps || {}).filter(inR).length, ms = Object.values(P.ms || {}).filter(inR).length;
    const exams = D.mods.filter(m => { const e = P.exams[m.id]; return e && e.best >= PASS && e.last >= a && e.last <= b; }).length;
    const per = typeof Clock !== "undefined" ? Clock.stats().days : {};
    let days = 0, sec = 0, qa = 0, sure = 0;
    for(let t = a; t <= b; t++){ const k = dayKey(t);
      if(P.log?.[k] > 0) days++;
      sec += Object.values(per[k] || {}).reduce((x, y) => x + y, 0);
      qa += P.qa?.[k]?.n || 0; sure += P.qa?.[k]?.sure || 0; }
    const pod = PB.daily?.(); const podDone = pod && inR(P.solved?.[pod.id]) ? 1 : 0;
    return {lessons, solved, steps, ms, exams, days, sec, qa, sure, pod: podDone, xp: lessons*XPV.lesson + sxp + steps*XPV.step + ms*XPV.milestone + exams*XPV.exam};
  }
  // three daily challenges and three weekly ones, the same for everyone on a given date
  function pickDaily(t){
    const rnd = seeded(hash("d" + dayKey(t))), pool = [...DAILY], out = [];
    while(out.length < 3 && pool.length){ const c = pool.splice(Math.floor(rnd()*pool.length), 1)[0];
      if((c.id === "lesson" && out.some(x => x.id === "lessons2")) || (c.id === "lessons2" && out.some(x => x.id === "lesson"))) continue;
      if(c.id === "pod" && !PB.daily?.()) continue;
      out.push(c); }
    return out;
  }
  function pickWeekly(ws){
    const rnd = seeded(hash("w" + dayKey(ws))), pool = WEEKLY.filter(c => !c.fixed), out = WEEKLY.filter(c => c.fixed);
    while(out.length < 3 && pool.length) out.push(pool.splice(Math.floor(rnd()*pool.length), 1)[0]);
    return out;
  }
  function challenges(){
    const t = today(), ws = wkStart(t), d = between(t, t), w = between(ws, t);
    const mk = (c, data, key) => { const have = Math.max(0, c.v(data) || 0); return {...c, have, done: have >= c.goal, key, claimed: P.claimed?.[key] != null}; };
    const daily = pickDaily(t).map(c => mk(c, d, `d:${dayKey(t)}:${c.id}`));
    const weekly = pickWeekly(ws).map(c => mk(c, w, `w:${dayKey(ws)}:${c.id}`));
    return {daily, weekly, dayKey: `d:${dayKey(t)}:all`, weekKey: `w:${dayKey(ws)}:all`, week: w, ws};
  }

  /* ---------- coins ---------- */
  function parts(s){
    const days = Object.keys(P.log || {}).filter(k => P.log[k] > 0).length;
    return {
      lessons: s.lessons*COINV.lesson, exams: s.exams*COINV.exam, problems: s.easy*COINV.Easy + s.medium*COINV.Medium + s.hard*COINV.Hard,
      steps: s.steps*COINV.step, projects: s.ms*COINV.milestone + s.built*COINV.project, courses: s.courses*COINV.course,
      paths: s.nodes*COINV.node + s.paths*COINV.path, badges: Object.keys(P.badges || {}).length*COINV.badge,
      levels: levelCoins(s.level), days: days*COINV.day, streaks: STREAK_BONUS.filter(([n]) => s.bestStreak >= n).reduce((a, [, c]) => a + c, 0),
      challenges: Object.values(P.claimed || {}).reduce((a, c) => a + (+c || 0), 0)
    };
  }
  const earned = s => Object.values(parts(s)).reduce((a, b) => a + b, 0);
  const spent = () => (P.buys || []).reduce((a, b) => a + (+b.price || 0), 0);
  const balance = s => earned(s || Game.stats()) - spent();
  const owns = item => (P.buys || []).some(b => b.item === item);
  const freezesLeft = () => (P.buys || []).filter(b => b.item === "freeze" && !Object.values(P.frozen || {}).includes(b.id)).length;

  // a gap of missed days ending yesterday is covered by freezes bought on or before each missed day
  function autoFreeze(){
    const t = today(), active = n => P.log?.[dayKey(n)] > 0 || !!P.frozen?.[dayKey(n)];
    let g = 0; while(g < 7 && !active(t - 1 - g)) g++;
    if(!g || g >= 7 || !active(t - 1 - g)) return 0;
    const free = (P.buys || []).filter(b => b.item === "freeze" && !Object.values(P.frozen || {}).includes(b.id)).sort((x, y) => x.day - y.day);
    const plan = [];
    for(let i = g; i >= 1; i--){ const day = t - i, b = free.find(f => f.day <= day && !plan.some(p => p.b === f)); if(!b) return 0; plan.push({day, b}); }
    P.frozen = P.frozen || {}; plan.forEach(({day, b}) => { P.frozen[dayKey(day)] = b.id; });
    return plan.length;
  }

  // claim finished challenges; returns toasts to show
  function claim(){
    const ev = [], c = challenges(); P.claimed = P.claimed || {};
    const used = autoFreeze(); if(used) ev.push({t: used > 1 ? `${used} streak freezes used` : "Streak freeze used", s: `Your ${streak()}-day streak is safe.`, i: "shield"});
    [...c.daily, ...c.weekly].forEach(x => { if(x.done && !x.claimed){ P.claimed[x.key] = x.coins; ev.push({t: `Challenge done: ${x.t}`, s: `+${x.coins} coins`, i: "target", big: true}); } });
    if(c.daily.length && c.daily.every(x => P.claimed[x.key] != null) && P.claimed[c.dayKey] == null){ P.claimed[c.dayKey] = DAY_BONUS; ev.push({t: "All of today's challenges done", s: `+${DAY_BONUS} bonus coins`, i: "star", big: true}); }
    if(c.weekly.every(x => P.claimed[x.key] != null) && P.claimed[c.weekKey] == null){ P.claimed[c.weekKey] = WEEK_BONUS; ev.push({t: "Weekly challenges cleared", s: `+${WEEK_BONUS} bonus coins`, i: "trophy", big: true}); }
    return ev;
  }
  // after badges are settled: how many coins appeared since last time, and publish to the leaderboard
  function settle(s){
    const e = earned(s), prev = P.coinSeen ?? e, gained = Math.max(0, e - prev);
    const changed = P.coinSeen !== e; P.coinSeen = e;
    look(); Board.queue(s);
    return {gained, changed};
  }
  function look(){
    const a = P.equip?.accent && owns("accent-" + P.equip.accent) ? P.equip.accent : "";
    if(a) document.documentElement.dataset.accent = a; else delete document.documentElement.dataset.accent;
  }
  function buy(id){
    const it = SHOP.find(x => x.id === id); if(!it) return;
    const s = Game.stats();
    if(balance(s) < it.price || (it.minLevel && s.level < it.minLevel) || (it.need && !it.need(s))) return;
    if(it.kind === "freeze" ? freezesLeft() >= it.max : owns(it.id)) return;
    P.buys = P.buys || []; P.buys.push({id: uid(), item: it.id, price: it.price, day: today()});
    if(it.kind !== "freeze") equip(it, true);
    save("p"); UI.toast(`Bought: ${it.t}`, `${balance().toLocaleString()} coins left`, it.i || "palette", 3200); render();
  }
  function equip(it, quiet){
    P.equip = P.equip || {}; const k = it.kind;
    P.equip[k] = P.equip[k] === it.v && !quiet ? "" : it.v;
    if(!quiet){ save("p"); render(); }
  }
  const title = () => { const v = P.equip?.title; return v && SHOP.some(x => x.kind === "title" && x.v === v && owns(x.id)) ? v : ""; };
  return {challenges, between, parts, earned, spent, balance, owns, freezesLeft, claim, settle, buy, equip, title, look, wkStart};
})();

/* ---------- leaderboard: boards/{all | w-YYYY-MM-DD}/entries/{uid} in Firestore, opt-in, name and numbers only ---------- */
const Board = (() => {
  let timer = null, lastSent = "", cache = {};
  const weekId = () => "w-" + dayKey(Rewards.wkStart(today()));
  const can = () => typeof Account !== "undefined" && Account.user && Account.board;
  const entry = s => {
    const w = Rewards.between(Rewards.wkStart(today()), today());
    return {name: (P.board?.name || "").slice(0, 24), title: Rewards.title(), xp: s.xp, level: s.level, coins: Rewards.earned(s), streak: s.streak, weekXp: w.xp};
  };
  function queue(s){
    if(!can() || !P.board?.on || !P.board?.name) return;
    clearTimeout(timer); timer = setTimeout(() => publish(s), 4000);
  }
  async function publish(s){
    if(!can() || !P.board?.on) return;
    const e = entry(s || Game.stats()), key = JSON.stringify([weekId(), e]); if(key === lastSent) return;
    try{ const uidv = Account.user.uid; await Promise.all([Account.board("all").put(uidv, e), Account.board(weekId()).put(uidv, e)]); lastSent = key; cache = {}; }
    catch(err){ console.warn("Leaderboard update failed:", err?.code || err); }
  }
  async function top(which){
    const name = which === "week" ? weekId() : "all", field = which === "week" ? "weekXp" : "xp";
    if(cache[name] && Date.now() - cache[name].at < 60000) return cache[name].rows;
    const rows = await Account.board(name).top(field, 50); cache[name] = {rows, at: Date.now()}; return rows;
  }
  async function join(name){
    P.board = {on: true, name: name.trim().replace(/\s+/g, " ").slice(0, 24)}; save("p"); lastSent = ""; await publish(); cache = {};
  }
  async function leave(){
    const uidv = Account.user?.uid; P.board = {on: false, name: P.board?.name || ""}; save("p"); lastSent = ""; cache = {};
    if(uidv){ try{ await Promise.all([Account.board("all").remove(uidv), Account.board(weekId()).remove(uidv)]); }catch(e){} }
  }
  return {queue, publish, top, join, leave, weekId, can};
})();

/* ================= REWARDS PAGE ================= */
const RW_TABS = [["challenges","Challenges","target"],["board","Leaderboard","trophy"],["shop","Shop","palette"],["earn","How coins work","list"]];
function chalRow(c, compact){
  const pct = Math.min(100, 100*c.have/c.goal), fmt = n => c.unit === "min" ? fmtDur(n*60) : n.toLocaleString();
  return `<div class="chal ${c.done?"done":""}"><span class="ci">${icon(c.done?"check":c.i)}</span><div class="cb"><b>${esc(c.t)}</b><span class="bar"><i style="width:${pct}%"></i></span><span class="cm">${fmt(Math.min(c.have, c.goal))} / ${fmt(c.goal)}</span></div>
    <span class="cr">${c.done?`<span class="pill ok">+${c.coins}</span>`:`<span class="coins">${COIN_SVG}${c.coins}</span>${compact?"":`<button type="button" class="btn sm" data-cgo="${esc(c.key)}">Go</button>`}`}</span></div>`;
}
function untilMidnight(){ const n = new Date(), m = new Date(n); m.setHours(24, 0, 0, 0); return fmtDur((m - n)/1000); }
function viewRewards(el){
  const tab = RW_TABS.some(t => t[0] === route.id) ? route.id : "challenges";
  const s = Game.stats(), bal = Rewards.balance(s), c = Rewards.challenges();
  el.innerHTML = `<section class="head"><span class="eyebrow">Rewards</span><h1 class="h1 coinh">${COIN_SVG}<span class="gt">${bal.toLocaleString()}</span> coins</h1>
    <p class="lede">Coins come from real progress: every lesson, problem, step, project, badge, level and practice day pays once, and challenges pay extra. Spend them on streak freezes and new looks, and compare your week on the leaderboard.</p>
    <div class="row" style="gap:6px">${[["flame",`${s.streak}-day streak`],["shield",`${Rewards.freezesLeft()} streak freeze${Rewards.freezesLeft()===1?"":"s"}`],["star",`Level ${s.level} · ${Game.rank(s.level)}`],["award",`${Object.keys(P.badges||{}).length} badges`]].map(([i,t])=>`<span class="pill">${icon(i,"sm")}${t}</span>`).join("")}${Rewards.title()?`<span class="pill acc">${esc(Rewards.title())}</span>`:""}</div></section>
  <div class="chips" role="tablist" aria-label="Rewards sections">${RW_TABS.map(([id,t,i])=>`<button type="button" class="chip" role="tab" data-rtab="${id}" aria-selected="${tab===id}" aria-pressed="${tab===id}">${icon(i,"sm")}${t}</button>`).join("")}</div>
  <div id="rwbody"></div>`;
  el.querySelectorAll("[data-rtab]").forEach(b => b.onclick = () => go({v:"rewards", id:b.dataset.rtab}));
  const body = el.querySelector("#rwbody");
  if(tab === "challenges") rwChallenges(body, s, c);
  else if(tab === "shop") rwShop(body, s, bal);
  else if(tab === "earn") rwEarn(body, s);
  else rwBoard(body, s);
}
function rwChallenges(body, s, c){
  const next = STREAK_BONUS.find(([n]) => s.bestStreak < n);
  const dAll = c.daily.every(x => x.done), wAll = c.weekly.every(x => x.done);
  body.innerHTML = `<div class="grid2">
    <section class="panel"><div class="sec-h"><h2 class="h3">Today</h2><span class="muted" style="font-size:.85rem">New ones in ${untilMidnight()}</span></div>
      <div class="chals">${c.daily.map(x=>chalRow(x)).join("")}</div>
      <p class="muted" style="margin:0;font-size:.85rem">${dAll?`All three done. +${DAY_BONUS} bonus coins collected.`:`Finish all three for +${DAY_BONUS} bonus coins.`}</p></section>
    <section class="panel"><div class="sec-h"><h2 class="h3">This week</h2><span class="muted" style="font-size:.85rem">Resets Monday</span></div>
      <div class="chals">${c.weekly.map(x=>chalRow(x)).join("")}</div>
      <p class="muted" style="margin:0;font-size:.85rem">${wAll?`Week cleared. +${WEEK_BONUS} bonus coins collected.`:`Clear all three for +${WEEK_BONUS} bonus coins.`}</p></section>
  </div>
  <section class="panel"><h2 class="h3">${icon("flame")} Streak</h2>
    <div class="row" style="gap:18px;align-items:center"><b class="score" style="font-size:2.6rem">${s.streak}</b><div style="display:grid;gap:4px"><span>day${s.streak===1?"":"s"} in a row · best ${s.bestStreak}</span>
      <span class="muted" style="font-size:.9rem">${next?`Reach a ${next[0]}-day streak for +${next[1]} coins.`:"You've collected every streak bonus."} A day counts when you finish something: a lesson, a question, a step or a problem.</span>
      <span class="muted" style="font-size:.9rem">${Rewards.freezesLeft()?`You hold ${Rewards.freezesLeft()} streak freeze${Rewards.freezesLeft()===1?"":"s"}. If you miss a day, one is used automatically.`:`No streak freezes. <button type="button" class="btn ghost sm" data-rtab2="shop">Buy one for 150 coins</button>`}</span></div></div></section>`;
  body.querySelectorAll("[data-cgo]").forEach(b => b.onclick = () => { const x = [...c.daily, ...c.weekly].find(y => y.key === b.dataset.cgo); if(x) go(x.go()); });
  body.querySelector("[data-rtab2]")?.addEventListener("click", () => go({v:"rewards", id:"shop"}));
}
function rwShop(body, s, bal){
  const card = it => {
    const freeze = it.kind === "freeze", own = !freeze && Rewards.owns(it.id), on = own && P.equip?.[it.kind] === it.v;
    const locked = (it.minLevel && s.level < it.minLevel) ? `Needs level ${it.minLevel}` : (it.need && !it.need(s)) ? it.needT : "";
    const full = freeze && Rewards.freezesLeft() >= it.max, short = it.price - bal;
    const btn = own ? `<button type="button" class="btn sm ${on?"":"primary"}" data-equip="${it.id}">${on?(it.kind==="accent"?"Use the default accent":"Remove the title"):(it.kind==="accent"?"Use this accent":"Show this title")}</button>`
      : locked ? `<span class="pill">${icon("lock","sm")}${esc(locked)}</span>`
      : full ? `<span class="pill">You hold ${it.max} of ${it.max}</span>`
      : short > 0 ? `<span class="pill">${short.toLocaleString()} more coins needed</span>`
      : `<button type="button" class="btn primary sm" data-buy="${it.id}">Buy for ${it.price.toLocaleString()} coins</button>`;
    return `<article class="shopc ${own?"own":""} ${on?"on":""}"><span class="sv" ${it.sw?`style="--sw:${it.sw}"`:""}>${it.sw?"":icon(it.i||"star")}</span>
      <div style="display:grid;gap:4px"><b>${esc(it.t)}</b><span class="muted" style="font-size:.86rem">${esc(it.d)}</span>${freeze?`<span class="muted" style="font-size:.82rem">You hold ${Rewards.freezesLeft()} of ${it.max}</span>`:""}</div>
      <div class="row" style="justify-content:space-between;align-items:center"><span class="coins">${COIN_SVG}${it.price.toLocaleString()}</span>${btn}</div></article>`;
  };
  body.innerHTML = `<p class="muted" style="margin:0">You have <b style="color:var(--ink)">${bal.toLocaleString()} coins</b>. Everything here is for fun and streak protection; no lesson, problem or hint ever costs coins.</p>
    <section style="display:grid;gap:12px"><h2 class="h3">Keep your streak</h2><div class="shop">${SHOP.filter(x=>x.kind==="freeze").map(card).join("")}</div></section>
    <section style="display:grid;gap:12px"><h2 class="h3">Accent colours</h2><div class="shop">${SHOP.filter(x=>x.kind==="accent").map(card).join("")}</div></section>
    <section style="display:grid;gap:12px"><h2 class="h3">Titles</h2><div class="shop">${SHOP.filter(x=>x.kind==="title").map(card).join("")}</div></section>`;
  body.querySelectorAll("[data-buy]").forEach(b => b.onclick = () => Rewards.buy(b.dataset.buy));
  body.querySelectorAll("[data-equip]").forEach(b => b.onclick = () => Rewards.equip(SHOP.find(x => x.id === b.dataset.equip)));
}
function rwEarn(body, s){
  const p = Rewards.parts(s), rows = [["lessons","Core lessons",`${COINV.lesson} each`],["exams","Module exams passed",`${COINV.exam} each`],["problems","Problems solved",`${COINV.Easy} / ${COINV.Medium} / ${COINV.Hard} for Easy / Medium / Hard`],
    ["steps","Bootcamp and Build steps",`${COINV.step} each`],["projects","Project milestones and finished Build projects",`${COINV.milestone} per milestone, ${COINV.project} per project`],["courses","Bootcamp courses finished",`${COINV.course} each`],
    ["paths","Career-path topics and whole paths",`${COINV.node} per topic, ${COINV.path} per path`],["badges","Badges",`${COINV.badge} each`],["levels","Levels reached","10 × the level, for every level"],
    ["days","Days you practised",`${COINV.day} per day`],["streaks","Streak milestones",STREAK_BONUS.map(([n,c])=>`${n} days: ${c}`).join(", ")],["challenges","Daily and weekly challenges",`as listed, plus ${DAY_BONUS} for a full day and ${WEEK_BONUS} for a full week`]];
  body.innerHTML = `<section class="panel"><h2 class="h3">Where your coins came from</h2><div class="tbl"><table><thead><tr><th>Source</th><th>Rate</th><th style="text-align:right">You earned</th></tr></thead><tbody>
    ${rows.map(([k,t,r])=>`<tr><td>${t}</td><td class="muted">${r}</td><td style="text-align:right">${p[k].toLocaleString()}</td></tr>`).join("")}
    <tr><td><b>Earned</b></td><td></td><td style="text-align:right"><b>${Rewards.earned(s).toLocaleString()}</b></td></tr>
    <tr><td>Spent in the shop</td><td></td><td style="text-align:right">−${Rewards.spent().toLocaleString()}</td></tr>
    <tr><td><b>Balance</b></td><td></td><td style="text-align:right"><b>${Rewards.balance(s).toLocaleString()}</b></td></tr></tbody></table></div>
    <p class="muted" style="margin:0;font-size:.88rem">Coins are worked out from what you've actually done, the same way XP is, so redoing a lesson or re-solving a problem doesn't pay twice. They're kept with the rest of your progress and sync to your account when you sign in.</p></section>`;
}
async function rwBoard(body, s){
  const mode = route.board === "all" ? "all" : "week";
  const head = `<div class="chips" role="group" aria-label="Leaderboard period"><button type="button" class="chip" data-bm="week" aria-pressed="${mode==="week"}">This week</button><button type="button" class="chip" data-bm="all" aria-pressed="${mode==="all"}">All time</button></div>`;
  const wire = () => body.querySelectorAll("[data-bm]").forEach(b => b.onclick = () => { route.board = b.dataset.bm; render(); });
  if(typeof Account === "undefined" || !Account.enabled){ body.innerHTML = `<section class="panel"><h2 class="h3">Leaderboard</h2><p class="muted" style="margin:0">The leaderboard needs accounts, and this copy of CodeLearner runs without them. Everything else, including coins and challenges, works in this browser.</p></section>`; return; }
  if(!Account.user){ body.innerHTML = `<section class="panel"><h2 class="h3">Leaderboard</h2><p class="muted" style="margin:0">Sign in with Google to see who's practising most this week and to add yourself.</p></section>${Account.panel()}`; Account.wire(body); return; }
  if(!P.board?.on){
    const first = (Account.user.name || "").trim().split(/\s+/)[0] || "Learner";
    body.innerHTML = `<section class="panel" style="max-width:640px"><h2 class="h3">Join the leaderboard</h2>
      <p class="muted" style="margin:0">Other signed-in learners will see only the name below, your title, level, XP, coins and streak. Your email address and photo are never shown. You can leave at any time, which removes your entry.</p>
      <label style="display:grid;gap:6px"><span class="eyebrow">Name on the board</span><input class="pred" id="lbname" maxlength="24" value="${esc(P.board?.name || first)}" autocomplete="nickname"></label>
      <div class="row"><button type="button" class="btn primary" id="lbjoin">Join as <span id="lbprev">${esc(P.board?.name || first)}</span></button></div><p class="err" id="lberr" role="alert" style="margin:0" hidden></p></section>`;
    const inp = body.querySelector("#lbname"), prev = body.querySelector("#lbprev");
    inp.oninput = () => { prev.textContent = inp.value.trim() || "…"; };
    body.querySelector("#lbjoin").onclick = async () => { const n = inp.value.trim(); if(!n){ inp.focus(); return; } await Board.join(n); Game.sync(); render(); };
    return;
  }
  body.innerHTML = `${head}<section class="panel"><div class="loading" style="padding:12px 0">Loading the leaderboard…</div></section>`; wire();
  let rows;
  try{ await Board.publish(s); rows = await Board.top(mode); }
  catch(e){
    const denied = e?.code === "permission-denied";
    body.innerHTML = `${head}<section class="panel"><h2 class="h3">Leaderboard</h2><p class="muted" style="margin:0">${denied?"The leaderboard isn't switched on for this site yet: the site's Firestore rules need the leaderboard section (see the README). Your coins and challenges still work.":"The leaderboard didn't load. Check your connection, then open this tab again."}</p></section>`; wire(); return;
  }
  if(route.v !== "rewards" || (route.id||"challenges") !== "board") return;
  const me = Account.user.uid, mine = rows.findIndex(r => r.uid === me);
  const val = r => mode === "week" ? r.weekXp : r.xp;
  const medal = i => i < 3 ? `<span class="medal m${i+1}">${i+1}</span>` : `<span class="rk">${i+1}</span>`;
  body.innerHTML = `${head}<section class="panel"><div class="sec-h"><h2 class="h3">${mode==="week"?"This week":"All time"}</h2><span class="muted" style="font-size:.85rem">${mode==="week"?"XP from lessons, exams, problems, steps and milestones since Monday":"Total XP"}</span></div>
    ${rows.length?`<ol class="lb">${rows.map((r,i)=>`<li class="${r.uid===me?"me":""}">${medal(i)}<span class="av">${esc((r.name||"?").trim()[0]||"?").toUpperCase()}</span><span class="nm"><b>${esc(r.name||"Learner")}${r.uid===me?" (you)":""}</b>${r.title?`<span class="muted">${esc(r.title)}</span>`:""}</span><span class="lvl muted">Lv ${+r.level||1} · ${icon("flame","sm")}${+r.streak||0}</span><b class="val">${(+val(r)||0).toLocaleString()} XP</b></li>`).join("")}</ol>`
      :`<p class="muted" style="margin:0">Nobody's on the ${mode==="week"?"weekly ":""}board yet. Finish a lesson or solve a problem and you'll be first.</p>`}
    ${rows.length && mine<0?`<p class="muted" style="margin:0;font-size:.88rem">You're not in the top ${rows.length} yet. Weekly XP comes from lessons, exams, problems, steps and milestones.</p>`:""}</section>
    <section class="panel"><h2 class="h3">Your entry</h2><p class="muted" style="margin:0">Shown as <b style="color:var(--ink)">${esc(P.board.name)}</b>${Rewards.title()?`, ${esc(Rewards.title())}`:""}. Change the name or leave the board here.</p>
      <div class="row"><input class="pred" id="lbname" maxlength="24" value="${esc(P.board.name)}" style="max-width:260px"><button type="button" class="btn sm" id="lbren">Save the name</button><button type="button" class="btn ghost sm" id="lbleave">Leave the leaderboard</button></div></section>`;
  wire();
  body.querySelector("#lbren").onclick = async () => { const n = body.querySelector("#lbname").value.trim(); if(!n) return; await Board.join(n); render(); };
  body.querySelector("#lbleave").onclick = async () => { if(!confirm("Leave the leaderboard? Your entry is removed. Your coins and progress stay.")) return; await Board.leave(); render(); };
}
/* compact card for the Today page */
Rewards.todayCard = () => {
  const c = Rewards.challenges(), bal = Rewards.balance(), done = c.daily.filter(x => x.done).length;
  return `<section class="panel"><div class="sec-h"><h2 class="h3">${icon("target")} Today's challenges <span class="pill">${done} of ${c.daily.length} done</span></h2><button type="button" class="btn ghost sm" data-act="rewards">${COIN_SVG}${bal.toLocaleString()} coins</button></div>
    <div class="chals">${c.daily.map(x=>chalRow(x, true)).join("")}</div></section>`;
};

VIEWS.rewards = viewRewards;
SEARCH_SOURCES.push(() => [{t:"Rewards", sub:"Coins, daily and weekly challenges", kind:"Page", i:"target", r:{v:"rewards"}},
  {t:"Leaderboard", sub:"This week and all time", kind:"Page", i:"trophy", r:{v:"rewards", id:"board"}},
  {t:"Rewards shop", sub:"Streak freezes, accent colours and titles", kind:"Page", i:"palette", r:{v:"rewards", id:"shop"}}]);
