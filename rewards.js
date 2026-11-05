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

/* ---------- leaderboard: boards/{all | w-YYYY-MM-DD}/entries/{uid} in Firestore, opt-in, name and numbers only ----------
   Ranked by progress: XP earned this week (lessons, exams, problems, steps, milestones since Monday) by default, plus
   all-time XP, current streaks and coins earned. Your exact rank comes from a count query, so it is right even outside
   the top 50, and the people just above and below you come from range queries on the same field. Weekly leagues are
   set by this week's XP, and last week's top three collect a coin prize the next time they open the board. */
const LEAGUES = [[0,"Bronze","#b86b2e"],[250,"Silver","#8e9bb0"],[750,"Gold","#d4a106"],[1500,"Platinum","#14b8c8"],[3000,"Diamond","#7c6cf0"],[6000,"Legend","#e2448f"]];
const PODIUM_PRIZE = [500, 300, 150], PRIZE_MIN_XP = 100;
const BOARD_MODES = [
  {id:"week",   t:"This week",    field:"weekXp", unit:"XP",    sub:"XP earned since Monday from lessons, exams, problems, steps and milestones. Resets every Monday."},
  {id:"all",    t:"All time",     field:"xp",     unit:"XP",    sub:"Total XP since you started."},
  {id:"streak", t:"Streaks",      field:"streak", unit:"days",  sub:"Current daily streaks. A streak that's been idle for more than a day drops off."},
  {id:"coins",  t:"Coins earned", field:"coins",  unit:"coins", sub:"Every coin earned, before anything spent in the shop."},
  {id:"last",   t:"Last week",    field:"weekXp", unit:"XP",    sub:"Final standings for last week. The top three collect a prize."}
];
const leagueOf = xp => { let i = 0; LEAGUES.forEach(([min], k) => { if(xp >= min) i = k; }); return {i, name: LEAGUES[i][1], col: LEAGUES[i][2], next: LEAGUES[i+1] || null}; };

const Board = (() => {
  let timer = null, lastSent = "", cache = {};
  const ws = () => Rewards.wkStart(today());
  const weekId = () => "w-" + dayKey(ws()), lastWeekId = () => "w-" + dayKey(ws() - 7);
  const can = () => typeof Account !== "undefined" && Account.user && Account.board;
  const boardOf = m => m.id === "week" ? weekId() : m.id === "last" ? lastWeekId() : "all";
  const entry = s => {
    const w = Rewards.between(ws(), today());
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
  const cached = async (k, f) => { if(cache[k] && Date.now() - cache[k].at < 60000) return cache[k].v; const v = await f(); cache[k] = {v, at: Date.now()}; return v; };
  const fresh = r => r.updated == null || Date.now() - r.updated < 2*86400000;   // a streak idle for 2 days is broken
  // everything one board view needs: the top rows, your rank among everyone, and your neighbours
  async function load(mode){
    const m = BOARD_MODES.find(x => x.id === mode) || BOARD_MODES[0], name = boardOf(m), me = Account.user.uid;
    return cached(name + ":" + m.field, async () => {
      const b = Account.board(name);
      let rows = await b.top(m.field, m.id === "streak" ? 100 : 50);
      if(m.id === "streak") rows = rows.filter(r => fresh(r) && r.streak > 0).slice(0, 50);
      const mine = rows.find(r => r.uid === me) || null;
      const myVal = mine ? +mine[m.field] || 0 : m.id === "last" ? null : +entry(Game.stats())[m.field] || 0;
      let rank = null, total = rows.length, above = null, below = null;
      if(m.id === "streak"){ const i = rows.findIndex(r => r.uid === me); rank = i >= 0 ? i + 1 : null; above = i > 0 ? rows[i-1] : null; below = i >= 0 ? rows[i+1] || null : null; }
      else if(myVal != null){
        const [rk, tot, nb] = await Promise.all([b.rank(m.field, myVal), b.count(), b.near(m.field, myVal)]);
        rank = rk; total = tot; above = nb.above; below = nb.below;
        if(above?.uid === me) above = null; if(below?.uid === me) below = null;
      }
      return {m, rows, rank, total, above, below, myVal};
    });
  }
  // last week's top three get a prize once, the next time they open the board
  async function claimPrize(){
    if(!can() || !P.board?.on) return null;
    const lw = lastWeekId(), key = "lb:" + lw; if(P.claimed?.[key] != null) return null;
    const rows = await cached(lw + ":podium", () => Account.board(lw).top("weekXp", 3));
    const i = rows.findIndex(r => r.uid === Account.user.uid);
    if(i < 0 || (+rows[i].weekXp || 0) < PRIZE_MIN_XP) return null;
    P.claimed[key] = PODIUM_PRIZE[i]; P.podium = P.podium || {}; P.podium[lw] = i + 1; save("p");
    return {place: i + 1, coins: PODIUM_PRIZE[i]};
  }
  // remember yesterday's rank per board so the page can show movement
  function movement(mode, rank){
    if(rank == null) return 0;
    const k = mode + ":" + (mode === "week" ? weekId() : mode === "last" ? lastWeekId() : "all"), t = today();
    P.board.seen = P.board.seen || {}; const s = P.board.seen[k];
    if(!s){ P.board.seen[k] = {r: rank, d: t, p: rank}; save("p", true); return 0; }
    if(s.d < t){ s.p = s.r; s.d = t; }
    if(s.r !== rank){ s.r = rank; save("p", true); }
    return s.p - rank;
  }
  async function join(name){
    P.board = {...(P.board || {}), on: true, name: name.trim().replace(/\s+/g, " ").slice(0, 24)}; save("p"); lastSent = ""; cache = {}; await publish();
  }
  async function leave(){
    const uidv = Account.user?.uid; P.board = {...(P.board || {}), on: false}; save("p"); lastSent = ""; cache = {};
    if(uidv){ try{ await Promise.all([Account.board("all").remove(uidv), Account.board(weekId()).remove(uidv)]); }catch(e){} }
  }
  const weekEndsIn = () => { const end = new Date((ws() + 7)*86400000); const local = new Date(end.getUTCFullYear(), end.getUTCMonth(), end.getUTCDate()); return Math.max(0, (local - new Date())/1000); };
  return {queue, publish, load, claimPrize, movement, join, leave, weekId, lastWeekId, can, weekEndsIn};
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
  const mode = BOARD_MODES.some(m => m.id === route.board) ? route.board : "week";
  const head = `<div class="chips" role="group" aria-label="Leaderboard">${BOARD_MODES.map(m=>`<button type="button" class="chip" data-bm="${m.id}" aria-pressed="${mode===m.id}">${m.t}</button>`).join("")}</div>`;
  const wire = () => body.querySelectorAll("[data-bm]").forEach(b => b.onclick = () => { route.board = b.dataset.bm; render(); });
  if(typeof Account === "undefined" || !Account.enabled){ body.innerHTML = `<section class="panel"><h2 class="h3">Leaderboard</h2><p class="muted" style="margin:0">The leaderboard needs accounts, and this copy of CodeBay runs without them. Everything else, including coins and challenges, works in this browser.</p></section>`; return; }
  if(!Account.user){ body.innerHTML = `<section class="panel"><h2 class="h3">Leaderboard</h2><p class="muted" style="margin:0">Sign in with Google to see who's making the most progress this week, and to race them.</p></section>${Account.panel()}`; Account.wire(body); return; }
  if(!P.board?.on){
    const first = (Account.user.name || "").trim().split(/\s+/)[0] || "Learner";
    body.innerHTML = `<section class="panel" style="max-width:640px"><h2 class="h3">${icon("trophy")} Join the leaderboard</h2>
      <p style="margin:0">Race other learners on progress: XP from lessons, exams, problems, steps and milestones, reset every Monday. Climb the leagues from Bronze to Legend, and finish in the top three to win ${PODIUM_PRIZE.join(" / ")} coins.</p>
      <p class="muted" style="margin:0">Other signed-in learners see only the name below, your title, level, XP, coins and streak. Your email address and photo are never shown. You can leave at any time, which removes your entry.</p>
      <label style="display:grid;gap:6px"><span class="eyebrow">Name on the board</span><input class="pred" id="lbname" maxlength="24" value="${esc(P.board?.name || first)}" autocomplete="nickname"></label>
      <div class="row"><button type="button" class="btn primary" id="lbjoin">Join as <span id="lbprev">${esc(P.board?.name || first)}</span></button></div></section>`;
    const inp = body.querySelector("#lbname"), prev = body.querySelector("#lbprev");
    inp.oninput = () => { prev.textContent = inp.value.trim() || "…"; };
    body.querySelector("#lbjoin").onclick = async () => { const n = inp.value.trim(); if(!n){ inp.focus(); return; } await Board.join(n); Game.sync(); render(); };
    return;
  }
  body.innerHTML = `${head}<section class="panel"><div class="loading" style="padding:12px 0">Loading the leaderboard…</div></section>`; wire();
  let d, prize = null, champs = null;
  try{
    await Board.publish(s);
    [d, prize] = await Promise.all([Board.load(mode), Board.claimPrize().catch(() => null)]);
    if(mode === "week") champs = await Board.load("last").catch(() => null);
  }catch(e){
    const denied = e?.code === "permission-denied";
    body.innerHTML = `${head}<section class="panel"><h2 class="h3">Leaderboard</h2><p class="muted" style="margin:0">${denied?"The leaderboard isn't switched on for this site yet: the site's Firestore rules need the leaderboard section (see the README). Your coins and challenges still work.":"The leaderboard didn't load. Check your connection, then open this tab again."}</p></section>`; wire(); return;
  }
  if(route.v !== "rewards" || (route.id||"challenges") !== "board" || (BOARD_MODES.some(m => m.id === route.board) ? route.board : "week") !== mode) return;
  if(prize){ UI.toast(prize.place === 1 ? "You won last week" : `You finished #${prize.place} last week`, `+${prize.coins} coins`, "trophy", 6000); UI.confetti(160); Game.sync(); }
  const {m, rows, rank, total, above, below, myVal} = d, me = Account.user.uid, unit = m.unit;
  const v = r => +r?.[m.field] || 0, u = n => unit === "days" && Math.abs(n) === 1 ? "day" : unit, fmt = n => `${(+n||0).toLocaleString()} ${u(+n||0)}`;
  const lg = r => leagueOf(+r?.weekXp || 0), chip = r => { const L = lg(r); return `<span class="lg" style="--lg:${L.col}">${L.name}</span>`; };
  const nm = r => `${esc(r?.name || "Learner")}`;
  const mv = Board.movement(mode, rank);
  const myLeague = leagueOf(mode === "last" ? (myVal || 0) : Rewards.between(Rewards.wkStart(today()), today()).xp);
  const lastWk = Rewards.between(Rewards.wkStart(today()) - 7, Rewards.wkStart(today()) - 1).xp, thisWk = Rewards.between(Rewards.wkStart(today()), today()).xp;

  // your standing: rank, movement, the person to catch and the person chasing you
  const standing = rank == null ? `<p class="muted" style="margin:0">${mode==="last"?"You weren't on last week's board.":mode==="streak"?"Start a streak to appear here: finish a lesson, a question, a step or a problem today.":"You'll appear here once your entry updates."}</p>` : `
    <div class="stand"><div class="rkbig"><span>#${rank}</span><small>of ${total.toLocaleString()}</small></div>
      <div style="display:grid;gap:6px;min-width:0">
        <div class="row" style="gap:8px">${mv>0?`<span class="pill ok">▲ ${mv} since yesterday</span>`:mv<0?`<span class="pill bad">▼ ${-mv} since yesterday</span>`:""}<span class="pill">${fmt(myVal)}</span>${mode==="week"||mode==="last"?`<span class="lg" style="--lg:${myLeague.col}">${myLeague.name} league</span>`:""}</div>
        ${above?`<span>${icon("target","sm")} <b>${fmt(v(above)-myVal+1)}</b> to pass <b>${nm(above)}</b> for #${rank-1}</span>`:rank===1?`<span>${icon("trophy","sm")} You're in first place. ${below?`<b>${nm(below)}</b> is ${fmt(myVal-v(below))} behind.`:""}</span>`:""}
        ${below&&rank!==1?`<span class="muted">${nm(below)} is ${fmt(myVal-v(below))} behind you.</span>`:""}
        ${mode==="week"?`<span class="muted">${thisWk.toLocaleString()} XP so far this week; ${lastWk.toLocaleString()} XP all of last week.${thisWk>lastWk&&lastWk>0?" Already ahead of last week.":""}</span>`:""}
      </div></div>
    ${mode==="week"&&myLeague.next?`<div style="display:grid;gap:4px"><div class="row" style="justify-content:space-between"><span class="muted" style="font-size:.85rem">${(myLeague.next[0]-thisWk).toLocaleString()} XP to ${myLeague.next[1]}</span><span class="muted" style="font-size:.85rem">${myLeague.name} → ${myLeague.next[1]}</span></div><div class="bar"><i style="width:${Math.min(100,100*(thisWk-LEAGUES[myLeague.i][0])/(myLeague.next[0]-LEAGUES[myLeague.i][0]))}%;background:${myLeague.next[2]}"></i></div></div>`:""}`;

  const podium = rows.slice(0, 3), rest = rows.slice(3);
  const pod = podium.length ? `<div class="podium">${[1,0,2].filter(i=>podium[i]).map(i=>{ const r=podium[i]; return `<div class="pd p${i+1} ${r.uid===me?"me":""}"><span class="av">${esc((r.name||"?").trim()[0]||"?").toUpperCase()}</span><b>${nm(r)}${r.uid===me?" (you)":""}</b>${r.title?`<span class="muted" style="font-size:.78rem">${esc(r.title)}</span>`:""}<span class="pv">${fmt(v(r))}</span>${(mode==="week"||mode==="last")?`<span class="muted" style="font-size:.78rem">${PODIUM_PRIZE[i]} coin prize</span>`:""}<div class="step"><span>${i+1}</span></div></div>`; }).join("")}</div>` : "";
  const row = (r, i) => `<li class="${r.uid===me?"me":""}"><span class="rk">${i+1}</span><span class="av">${esc((r.name||"?").trim()[0]||"?").toUpperCase()}</span><span class="nm"><b>${nm(r)}${r.uid===me?" (you)":""}</b><span class="muted">${r.title?esc(r.title)+" · ":""}Lv ${+r.level||1} · ${icon("flame","sm")}${+r.streak||0}</span></span>${chip(r)}<b class="val">${fmt(v(r))}</b></li>`;
  const meRow = rank != null && rank > rows.length ? `<li class="gap">⋯</li><li class="me"><span class="rk">${rank}</span><span class="av">${esc((P.board.name||"?")[0]).toUpperCase()}</span><span class="nm"><b>${esc(P.board.name)} (you)</b><span class="muted">Lv ${s.level} · ${icon("flame","sm")}${s.streak}</span></span><span class="lg" style="--lg:${myLeague.col}">${myLeague.name}</span><b class="val">${fmt(myVal)}</b></li>` : "";
  const champStrip = champs && champs.rows.length ? `<section class="panel"><div class="sec-h"><h2 class="h3">${icon("trophy")} Last week's winners</h2><button type="button" class="btn ghost sm" data-bm="last">Final standings</button></div>
    <div class="row" style="gap:8px">${champs.rows.slice(0,3).map((r,i)=>`<span class="pill ${i===0?"acc":""}">#${i+1} ${nm(r)} · ${fmt(v(r))}</span>`).join("")}</div></section>` : "";

  body.innerHTML = `${head}
    ${mode==="week"?`<div class="lbban">${icon("clock","sm")}<span>Week ends in <b>${(t=>{ const d=Math.floor(t/86400), h=Math.floor(t%86400/3600); return d?`${d} d ${h} h`:fmtDur(t); })(Board.weekEndsIn())}</b>. Top three win <b>${PODIUM_PRIZE.join(" / ")}</b> coins.</span></div>`:""}
    <section class="panel"><div class="sec-h"><h2 class="h3">Your standing</h2><span class="muted" style="font-size:.85rem">${esc(m.sub)}</span></div>${standing}</section>
    <section class="panel"><h2 class="h3">${m.t}${mode==="last"?` · week of ${esc(Board.lastWeekId().slice(2))}`:""}</h2>
      ${rows.length?`${pod}${rest.length||meRow?`<ol class="lb" start="4">${rest.map((r,k)=>row(r,k+3)).join("")}${meRow}</ol>`:""}`
        :`<p class="muted" style="margin:0">Nobody's on this board yet. ${mode==="last"?"Nobody finished last week with any progress.":"Finish a lesson or solve a problem and you'll be first."}</p>`}</section>
    ${mode==="week"?champStrip:""}
    <details class="panel"><summary><b>Leagues and prizes</b></summary><div style="display:grid;gap:8px;margin-top:10px">
      <p class="muted" style="margin:0">Your league is set by this week's XP and starts again every Monday.</p>
      <div class="row" style="gap:6px">${LEAGUES.map(([min,n,c])=>`<span class="lg" style="--lg:${c}">${n} · ${min.toLocaleString()}+ XP</span>`).join("")}</div>
      <p class="muted" style="margin:0">The top three of each week win ${PODIUM_PRIZE.join(", ")} coins (with at least ${PRIZE_MIN_XP} XP that week), collected the next time they open this board. Scores are sent by each learner's browser, so treat the board as friendly competition.</p></div></details>
    <section class="panel"><h2 class="h3">Your entry</h2><p class="muted" style="margin:0">Shown as <b style="color:var(--ink)">${esc(P.board.name)}</b>${Rewards.title()?`, ${esc(Rewards.title())}`:""}. Change the name or leave the board here.</p>
      <div class="row"><input class="pred" id="lbname" maxlength="24" value="${esc(P.board.name)}" style="max-width:260px"><button type="button" class="btn sm" id="lbren">Save the name</button><button type="button" class="btn ghost sm" id="lbleave">Leave the leaderboard</button></div></section>`;
  wire();
  body.querySelector("#lbren").onclick = async () => { const n = body.querySelector("#lbname").value.trim(); if(!n) return; await Board.join(n); render(); };
  body.querySelector("#lbleave").onclick = async () => { if(!confirm("Leave the leaderboard? Your entry is removed. Your coins and progress stay.")) return; await Board.leave(); render(); };
}
/* compact card for the Today page */
Rewards.todayCard = () => {
  const c = Rewards.challenges(), bal = Rewards.balance(), done = c.daily.filter(x => x.done).length;
  const seen = P.board?.on ? P.board.seen?.["week:" + Board.weekId()] : null;
  return `<section class="panel"><div class="sec-h"><h2 class="h3">${icon("target")} Today's challenges <span class="pill">${done} of ${c.daily.length} done</span></h2><button type="button" class="btn ghost sm" data-act="rewards">${COIN_SVG}${bal.toLocaleString()} coins</button></div>
    <div class="chals">${c.daily.map(x=>chalRow(x, true)).join("")}</div>
    ${seen?`<button type="button" class="btn ghost sm" data-lbgo style="justify-self:start">${icon("trophy","sm")}You were #${seen.r} on this week's leaderboard${seen.p>seen.r?`, up ${seen.p-seen.r}`:""}. See who's close.</button>`:""}</section>`;
};

/* ================= HOME: this week's leaderboard ================= */
// The landing page shows this week's race. Names are only ever shown to signed-in people, because that is what learners
// agreed to when they joined (and what firestore.rules allows); signed-out visitors see how it works and a way in.
function lbCountdown(){ const s = Board.weekEndsIn(), d = Math.floor(s/86400), h = Math.floor(s%86400/3600), m = Math.floor(s%3600/60); return d ? `${d} d ${h} h` : h ? `${h} h ${m} min` : `${m} min`; }
async function homeLeaderboard(host){
  if(!host || typeof Account === "undefined") return;
  // the home page renders before sign-in has been checked; wait for that (a few seconds at most)
  await Promise.race([Account.ready, new Promise(r => setTimeout(r, 6000))]);
  if(!host.isConnected) return;
  if(!Account.enabled){ host.remove(); return; }
  const u = Account.user, joined = !!(P.board?.on && P.board?.name);
  const intro = `<div class="lbh-l">
      <span class="eyebrow">Leaderboard · this week</span>
      <h2 class="h2">Who's putting in the work</h2>
      <p class="lede">Ranked by XP earned since Monday from lessons, exams, problems, bootcamp steps and projects. Everyone starts from zero each week.</p>
      <dl class="lbfacts"><div><dt>Resets in</dt><dd id="lbReset">${lbCountdown()}</dd></div><div><dt>Weekly prizes</dt><dd>${PODIUM_PRIZE.map(n=>n.toLocaleString()).join(" / ")} coins</dd></div></dl>
      <div class="lbleagues" aria-label="Leagues by XP this week">${LEAGUES.map(([min,n,c])=>`<span class="lg" style="--lg:${c}">${n} <small>${min.toLocaleString()}+</small></span>`).join("")}</div>
      <div class="row"><button class="btn primary" data-rwgo="board">${icon("trophy","sm")}${u && joined ? "Open the leaderboard" : u ? "Join the leaderboard" : "See the leaderboard"}</button></div>
    </div>`;
  const shell = right => { host.innerHTML = intro + `<div class="lbh-r panel">${right}</div>`;
    host.querySelectorAll("[data-rwgo]").forEach(b => b.onclick = () => go({v: "rewards", id: b.dataset.rwgo}));
    host.querySelector("[data-signin]")?.addEventListener("click", () => Account.signIn());
    const t = host.querySelector("#lbReset"); const iv = setInterval(() => { if(!t.isConnected){ clearInterval(iv); return; } t.textContent = lbCountdown(); }, 30000); };
  if(!u){ shell(`<div class="lbh-out"><b>See this week's standings</b><p class="muted" style="margin:0">Sign in to see who's leading, where you'd rank and how much XP it takes to pass the person above you.</p><button class="gbtn" data-signin>${GOOGLE_G}<span>Sign in with Google</span></button></div>`); return; }
  shell(`<span class="muted">Loading this week's standings…</span>`);
  let d;
  try{ d = await Board.load("week"); }
  catch(e){ console.warn("home leaderboard", e?.code || e); if(host.isConnected) shell(`<p class="muted" style="margin:0">The leaderboard couldn't load right now.</p>`); return; }
  if(!host.isConnected || route.v !== "home") return;
  const {rows, rank, total, above, myVal} = d, me = u.uid, top = rows.slice(0, 5);
  const xp = n => `${(+n||0).toLocaleString()} XP`, nm = r => esc(r?.name || "Learner");
  const chip = r => { const L = leagueOf(+r?.weekXp || 0); return `<span class="lg" style="--lg:${L.col}">${L.name}</span>`; };
  const line = (r, i, you) => `<li class="${you?"me":""}"><span class="rk">${i<3&&!you?`<span class="medal m${i+1}">${i+1}</span>`:i+1}</span><span class="av">${esc((r.name||"?").trim()[0]||"?").toUpperCase()}</span><span class="nm"><b>${nm(r)}${you?" (you)":""}</b><span class="muted">Lv ${+r.level||1} · ${icon("flame","sm")}${+r.streak||0}</span></span>${chip(r)}<b class="val">${xp(r.weekXp)}</b></li>`;
  const inTop = top.some(r => r.uid === me);
  const meLine = joined && !inTop && rank != null ? `<li class="gap">⋯</li>${line({name: P.board.name, level: Game.stats().level, streak: Game.stats().streak, weekXp: myVal}, rank - 1, true)}` : "";
  const status = joined
    ? (rank == null ? `You'll appear here once your entry updates.` : rank === 1 ? `${icon("trophy","sm")} You're in first place this week.` : `You're <b>#${rank}</b> of ${total.toLocaleString()}.${above ? ` <b>${xp((+above.weekXp||0) - myVal + 1)}</b> to pass ${nm(above)}.` : ""}`)
    : (rank != null && myVal > 0 ? `With your ${xp(myVal)} this week you'd be <b>#${rank}</b> of ${total.toLocaleString()}. Join to show up.` : `Earn XP this week and join to take a place.`);
  shell(top.length
    ? `<ol class="lb lbtop">${top.map((r, i) => line(r, i, r.uid === me)).join("")}${meLine}</ol><p class="lbstatus">${status}</p>`
    : `<p style="margin:0"><b>Nobody's on the board this week yet.</b></p><p class="muted" style="margin:0">The first learner to join this week takes first place.</p><p class="lbstatus">${status}</p>`);
}

VIEWS.rewards = viewRewards;
document.addEventListener("click", e => { if(e.target.closest("[data-lbgo]")){ route.board = "week"; go({v:"rewards", id:"board"}); } });
SEARCH_SOURCES.push(() => [{t:"Rewards", sub:"Coins, daily and weekly challenges", kind:"Page", i:"target", r:{v:"rewards"}},
  {t:"Leaderboard", sub:"This week's progress, all time, streaks, coins and last week's winners", kind:"Page", i:"trophy", r:{v:"rewards", id:"board"}},
  {t:"Rewards shop", sub:"Streak freezes, accent colours and titles", kind:"Page", i:"palette", r:{v:"rewards", id:"shop"}}]);
