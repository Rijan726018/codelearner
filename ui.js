"use strict";
/* ---------- UI kit: icons, theme, toasts, confetti, glow, reveal, nav, search palette, XP + badges, Home and Profile ---------- */
const ICONS = {
  home:'<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M9.5 21v-6h5v6"/>',
  dash:'<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>',
  map:'<path d="M9 4 3 6.5v13.5L9 17.5l6 2.5 6-2.5V4l-6 2.5z"/><path d="M9 4v13.5M15 6.5V20"/>',
  route:'<circle cx="6" cy="19" r="2.5"/><circle cx="18" cy="5" r="2.5"/><path d="M8.5 19H17a3.5 3.5 0 0 0 0-7H7a3.5 3.5 0 0 1 0-7h8.5"/>',
  braces:'<path d="M8 3H7a2 2 0 0 0-2 2v4l-2 3 2 3v4a2 2 0 0 0 2 2h1M16 3h1a2 2 0 0 1 2 2v4l2 3-2 3v4a2 2 0 0 1-2 2h-1"/>',
  cap:'<path d="M2 9 12 4l10 5-10 5z"/><path d="M6 11v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5"/><path d="M22 9v6"/>',
  refresh:'<path d="M21 12a9 9 0 1 1-2.64-6.36"/><path d="M21 3v6h-6"/>',
  target:'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
  rocket:'<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.2 2.2 0 0 0-2.9-.1z"/><path d="m12 15-3-3a22 22 0 0 1 2-4A12.9 12.9 0 0 1 22 2c0 2.7-.8 7.5-6 11a22.4 22.4 0 0 1-4 2z"/><path d="M9 12H4s.6-3 2-4c1.6-1.1 5 0 5 0M12 15v5s3-.6 4-2c1.1-1.6 0-5 0-5"/>',
  play:'<path d="M7 4v16l13-8z"/>',
  book:'<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2zM22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>',
  search:'<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
  flame:'<path d="M12 22c3.9 0 7-2.8 7-6.8 0-3.9-2.6-6.3-4.3-8.2-.3 1.9-1.4 3.2-2.9 3.5.4-3.4-1.2-6.3-3.8-8.5.2 3.8-5 6.8-5 13.2C3 19.2 7.6 22 12 22z"/>',
  zap:'<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
  trophy:'<path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M7 6H4v1a3 3 0 0 0 3 3M17 6h3v1a3 3 0 0 1-3 3"/>',
  sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  moon:'<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
  check:'<path d="M5 12.5 10 17l9-10"/>',
  lock:'<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
  star:'<path d="m12 3 2.8 5.8 6.2.9-4.5 4.4 1.1 6.2L12 17.4l-5.6 2.9 1.1-6.2L3 9.7l6.2-.9z"/>',
  arrow:'<path d="M5 12h14M13 6l6 6-6 6"/>',
  back:'<path d="M19 12H5M11 6l-6 6 6 6"/>',
  x:'<path d="M6 6l12 12M18 6 6 18"/>',
  chev:'<path d="m9 6 6 6-6 6"/>',
  user:'<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
  monitor:'<rect x="2.5" y="4" width="19" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>',
  server:'<rect x="3" y="3.5" width="18" height="7" rx="2"/><rect x="3" y="13.5" width="18" height="7" rx="2"/><path d="M7 7h.01M7 17h.01"/>',
  layers:'<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
  sparkles:'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="m19 15 .8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
  cpu:'<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
  chart:'<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/>',
  bars:'<path d="M3 21h18M7 17v-7M12 17V5M17 17v-4"/>',
  db:'<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
  flow:'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/><path d="M6.5 10v4a3 3 0 0 0 3 3H14"/>',
  shield:'<path d="M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
  cross:'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2"/><path d="M12 3v5M12 16v5M3 12h5M16 12h5"/>',
  bug:'<rect x="7" y="7" width="10" height="13" rx="5"/><path d="M12 11v9M7 13H3M21 13h-4M7 17l-3 2M17 17l3 2M7 9 4 7M17 9l3-2M9 7a3 3 0 0 1 6 0"/>',
  cloud:'<path d="M7 18a5 5 0 1 1 1-9.9A6 6 0 0 1 19.5 10 4 4 0 0 1 18 18z"/>',
  infinity:'<path d="M6.5 8.5C4.5 8.5 3 10.1 3 12s1.5 3.5 3.5 3.5c3.5 0 7.5-7 11-7 2 0 3.5 1.6 3.5 3.5s-1.5 3.5-3.5 3.5c-3.5 0-7.5-7-11-7z"/>',
  gauge:'<path d="m12 14 4-4"/><path d="M3.3 19a10 10 0 1 1 17.4 0"/>',
  phone:'<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M11 18h2"/>',
  android:'<path d="M4 18a8 8 0 0 1 16 0z"/><path d="M7.5 7.5 6 5M16.5 7.5 18 5M9 13.5h.01M15 13.5h.01"/>',
  game:'<rect x="2" y="7" width="20" height="11" rx="5"/><path d="M7 10.5v4M5 12.5h4M15.5 12h.01M18 14h.01"/>',
  board:'<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M11 9h4a2 2 0 0 0 2-2V3M7 21v-4a2 2 0 0 1 2-2h4"/><circle cx="9" cy="9" r="2"/><circle cx="15" cy="15" r="2"/>',
  chain:'<rect x="2" y="9" width="6" height="6" rx="1"/><rect x="9" y="9" width="6" height="6" rx="1"/><rect x="16" y="9" width="6" height="6" rx="1"/><path d="M8 12h1M15 12h1"/>',
  checkc:'<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
  building:'<path d="M3 21h18M5 21V8l7-5 7 5v13"/><path d="M9 21v-5h6v5M9 11h.01M15 11h.01"/>',
  binary:'<path d="M6 3v6M4 3h2M4 9h4M16 15v6M14 15h2M14 21h4"/><rect x="13" y="3" width="5" height="6" rx="2.5"/><rect x="3.5" y="15" width="5" height="6" rx="2.5"/>',
  cube:'<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
  robot:'<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 8V4M9 4h6M9 13h.01M15 13h.01M2 13v3M22 13v3M9 17h6"/>',
  atom:'<circle cx="12" cy="12" r="1.5"/><ellipse cx="12" cy="12" rx="10" ry="4"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(120 12 12)"/>',
  globe:'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
  eye:'<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
  key:'<circle cx="7.5" cy="15.5" r="4.5"/><path d="m10.7 12.3 8.8-8.8M16 7l3 3M19 4l2 2"/>',
  clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  list:'<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
  bulb:'<path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.3h6c0-1 .4-1.8 1-2.3A7 7 0 0 0 12 2z"/>',
  flag:'<path d="M4 22V4M4 4h13l-2 4 2 4H4"/>',
  mountain:'<path d="m3 20 6.5-11 4 6.5 2.5-4 5 8.5z"/>',
  ext:'<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
  grid:'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
  shuffle:'<path d="M16 3h5v5M4 20 21 3M21 16v5h-5M15 15l6 6M4 4l5 5"/>',
  award:'<circle cx="12" cy="9" r="6"/><path d="m8.5 14-1.5 8 5-3 5 3-1.5-8"/>',
  cal:'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
  brief:'<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
  compass:'<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
  code:'<path d="m8 7-5 5 5 5M16 7l5 5-5 5"/>',
  terminal:'<path d="m4 17 6-5-6-5M12 19h8"/>',
  palette:'<circle cx="13.5" cy="6.5" r="1"/><circle cx="17.5" cy="10.5" r="1"/><circle cx="8.5" cy="7.5" r="1"/><circle cx="6.5" cy="12.5" r="1"/><path d="M12 2a10 10 0 0 0 0 20c1 0 1.7-.8 1.7-1.7 0-.4-.2-.8-.4-1.1-.3-.3-.4-.7-.4-1.1 0-.9.8-1.7 1.7-1.7H17a5 5 0 0 0 5-5c0-5-4.5-9.4-10-9.4z"/>',
  download:'<path d="M12 3v12M7 10l5 5 5-5M4 21h16"/>',
  upload:'<path d="M12 21V9M7 14l5-5 5 5M4 3h16"/>',
  hash:'<path d="M4 9h16M4 15h16M10 3 8 21M16 3l-2 18"/>',
  heart:'<path d="M12 21s-8-5.2-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.8-8 11-8 11z"/>',
  wifi:'<path d="M2 8.8a15 15 0 0 1 20 0M5 12.6a10 10 0 0 1 14 0M8.5 16.4a5 5 0 0 1 7 0M12 20h.01"/>',
  pen:'<path d="M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
  users:'<circle cx="9" cy="8" r="4"/><path d="M2 21a7 7 0 0 1 14 0M16 3.1a4 4 0 0 1 0 7.8M22 21a7 7 0 0 0-4-6.3"/>',
  vr:'<path d="M3 8h18v8h-6l-1.5-2.5a1.7 1.7 0 0 0-3 0L9 16H3z"/>',
  menu:'<path d="M4 6h16M4 12h16M4 18h16"/>'
};
function icon(name, cls=""){ return `<svg class="ic ${cls}" viewBox="0 0 24 24" aria-hidden="true">${ICONS[name]||ICONS.star}</svg>`; }

const UI = {};
/* ---------- theme ---------- */
UI.theme = (()=>{ let t=null; try{ t=localStorage.getItem("cl-theme"); }catch(e){} return t; })();
UI.applyTheme = () => {
  const r=document.documentElement; if(UI.theme) r.dataset.theme=UI.theme; else delete r.dataset.theme;
  const dark = UI.theme ? UI.theme==="dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  const b=document.getElementById("themeBtn"); if(b){ b.innerHTML=icon(dark?"sun":"moon"); b.dataset.tip=dark?"Light theme":"Dark theme"; }
};
UI.toggleTheme = () => {
  const dark = UI.theme ? UI.theme==="dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  UI.theme = dark ? "light" : "dark"; try{ localStorage.setItem("cl-theme", UI.theme); }catch(e){}
  const swap=()=>UI.applyTheme(); document.startViewTransition ? document.startViewTransition(swap) : swap();
};

/* ---------- toasts + confetti ---------- */
UI.toast = (title, sub="", ic="zap", ms=3600) => {
  const host=document.getElementById("toasts"); if(!host) return;
  const t=document.createElement("div"); t.className="toast"; t.innerHTML=`<span class="ti">${icon(ic,"lg")}</span><div><b>${esc(title)}</b>${sub?`<span>${esc(sub)}</span>`:""}</div>`;
  host.appendChild(t); while(host.children.length>4) host.firstChild.remove();
  setTimeout(()=>{ t.classList.add("out"); setTimeout(()=>t.remove(),320); }, ms);
};
UI.confetti = (n=150) => {
  if(matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const c=document.getElementById("confetti"); if(!c) return; const x=c.getContext("2d"); const dpr=Math.min(2,devicePixelRatio||1);
  c.width=innerWidth*dpr; c.height=innerHeight*dpr; x.scale(dpr,dpr);
  const cols=["#8b7dff","#38d3f0","#a3e635","#ff5c93","#fbbf24","#ffffff"];
  const ps=Array.from({length:n},()=>({x:innerWidth/2+(Math.random()-.5)*innerWidth*.5, y:innerHeight*.35+(Math.random()-.5)*60, vx:(Math.random()-.5)*14, vy:-Math.random()*13-4,
    w:5+Math.random()*7, h:3+Math.random()*5, r:Math.random()*6, vr:(Math.random()-.5)*.4, c:cols[(Math.random()*cols.length)|0]}));
  const t0=performance.now();
  (function f(t){ x.clearRect(0,0,innerWidth,innerHeight); const age=(t-t0)/1000;
    ps.forEach(p=>{ p.vy+=.38; p.vx*=.99; p.x+=p.vx; p.y+=p.vy; p.r+=p.vr; x.save(); x.globalAlpha=Math.max(0,1-age/2.6); x.translate(p.x,p.y); x.rotate(p.r); x.fillStyle=p.c; x.fillRect(-p.w/2,-p.h/2,p.w,p.h); x.restore(); });
    if(age<2.7) requestAnimationFrame(f); else x.clearRect(0,0,innerWidth,innerHeight); })(t0);
};

/* ---------- pointer glow + scroll reveal + count-up ---------- */
document.addEventListener("pointermove", e => {
  const el=e.target.closest?.(".glow"); if(!el) return; const r=el.getBoundingClientRect();
  el.style.setProperty("--mx",(e.clientX-r.left)+"px"); el.style.setProperty("--my",(e.clientY-r.top)+"px");
}, {passive:true});
UI.io = ("IntersectionObserver" in window) ? new IntersectionObserver(es=>es.forEach(en=>{ if(en.isIntersecting){ en.target.classList.add("in"); UI.io.unobserve(en.target); if(en.target.dataset.count!=null) UI.countUp(en.target); } }),{rootMargin:"0px 0px -6% 0px"}) : null;
if(UI.io && !matchMedia("(prefers-reduced-motion: reduce)").matches) document.documentElement.classList.add("anim");
UI.countUp = el => { const to=+el.dataset.count; if(!(to>0)){ el.textContent=el.dataset.count; return; } const t0=performance.now(), d=1300;
  (function f(t){ const k=Math.min(1,(t-t0)/d), v=Math.round(to*(1-Math.pow(1-k,3))); el.textContent=v.toLocaleString(); if(k<1) requestAnimationFrame(f); })(t0); };
UI.scan = root => { (root||document).querySelectorAll(".rv:not(.in),[data-count]:not(.counted)").forEach(el=>{
  if(el.dataset.count!=null){ el.classList.add("counted"); if(!UI.io){ el.textContent=(+el.dataset.count).toLocaleString(); return; } }
  if(UI.io) UI.io.observe(el); else el.classList.add("in"); }); };
new MutationObserver(()=>UI.scan(document.getElementById("main"))).observe(document.getElementById("main"),{childList:true,subtree:true});

/* ---------- navigation ---------- */
const NAV = [
  {v:"today", t:"Today", i:"dash"}, {v:"map", t:"Learn", i:"map"},
  {v:"paths", t:"Paths", i:"route"}, {v:"problems", t:"Problems", i:"braces"}, {v:"bootcamp", t:"Bootcamp", i:"cap"}, {v:"build", t:"Build", i:"rocket"},
  {v:"review", t:"Review", i:"refresh", badge:true}
];
const NAV_MORE = [{v:"home", t:"Home", i:"home"}, {v:"practice", t:"Practice by level", i:"target"}, {v:"projects", t:"Projects", i:"rocket"}, {v:"playground", t:"Playground", i:"terminal"}, {v:"method", t:"The Method", i:"book"}, {v:"profile", t:"Profile & badges", i:"award"}];
UI.buildNav = () => {
  document.getElementById("tabs").innerHTML = NAV.map(n=>`<button type="button" data-v="${n.v}">${icon(n.i)}<span>${n.t}</span>${n.badge?`<span class="badge" id="duebadge" hidden>0</span>`:""}</button>`).join("");
  const r=document.querySelector(".top-r"); const m=document.createElement("div"); m.className="more";
  m.innerHTML=`<button type="button" class="iconbtn" id="moreBtn" aria-haspopup="true" aria-expanded="false" aria-label="More sections">${icon("grid")}</button><div class="menu" id="moreMenu" hidden>${NAV_MORE.map(n=>`<button type="button" data-v="${n.v}">${icon(n.i)}${n.t}</button>`).join("")}</div>`;
  r.insertBefore(m, document.getElementById("themeBtn"));
  const btn=m.querySelector("#moreBtn"), menu=m.querySelector("#moreMenu");
  btn.onclick=e=>{ e.stopPropagation(); menu.hidden=!menu.hidden; btn.setAttribute("aria-expanded",!menu.hidden); };
  menu.onclick=e=>{ const b=e.target.closest("[data-v]"); if(b){ menu.hidden=true; go({v:b.dataset.v}); } };
  document.addEventListener("click",e=>{ if(!menu.hidden && !m.contains(e.target)){ menu.hidden=true; btn.setAttribute("aria-expanded","false"); } });
  document.getElementById("themeBtn").onclick=UI.toggleTheme;
  document.getElementById("searchBtn").onclick=()=>Palette.open();
  UI.applyTheme(); matchMedia("(prefers-color-scheme: dark)").addEventListener?.("change",UI.applyTheme);
  UI.fitNav(); addEventListener("resize", UI.fitNav); document.fonts?.ready.then(UI.fitNav);
};
/* Icon-only tabs when the labels don't fit beside the logo and controls (desktop widths only; phones scroll the tab row). */
UI.fitNav = () => {
  const t=document.getElementById("tabs"), top=document.querySelector(".top-in"); if(!t||!top) return;
  t.classList.remove("compact"); top.classList.remove("tight");
  const over=()=>innerWidth>980 && t.scrollWidth>t.clientWidth+1;
  if(over()) top.classList.add("tight");   // first drop the "Search" label, then the tab labels
  if(over()) t.classList.add("compact");
};
UI.syncNav = tabV => {
  document.querySelectorAll("#tabs [data-v], #moreMenu [data-v]").forEach(b=>b.setAttribute("aria-current", b.dataset.v===tabV?"page":"false"));
  const g=Game.stats(); const sc=document.getElementById("streakChip"), xc=document.getElementById("xpChip");
  if(sc) sc.innerHTML=`${icon("flame","sm")}${g.streak}`;
  if(xc) xc.innerHTML=`<span class="lv">Lv ${g.level}</span>${g.xp.toLocaleString()} XP`;
  UI.fitNav();
};

/* ================= GAME: XP, levels, badges (all derived from progress, so nothing double-counts) ================= */
const XPV = {lesson:50, exam:200, milestone:25, card:5, Easy:30, Medium:60, Hard:100, step:15, node:20};
const RANKS = [[1,"Novice"],[3,"Apprentice"],[5,"Coder"],[8,"Developer"],[12,"Engineer"],[16,"Senior Engineer"],[20,"Staff Engineer"],[25,"Principal Engineer"],[30,"Legend"]];
const BADGES = [
  {id:"first-lesson", n:"First Steps", d:"Finish your first lesson", i:"flag", t:s=>s.lessons>=1},
  {id:"lessons-10", n:"Habit Builder", d:"Finish 10 lessons", i:"cal", t:s=>s.lessons>=10},
  {id:"lessons-50", n:"Half Century", d:"Finish 50 lessons", i:"book", t:s=>s.lessons>=50},
  {id:"lessons-all", n:"Cartographer", d:"Finish every core lesson", i:"map", t:s=>s.lessons>=s.lessonsTotal&&s.lessonsTotal>0},
  {id:"exam-1", n:"Gatekeeper", d:"Pass your first module exam", i:"lock", t:s=>s.exams>=1},
  {id:"exams-10", n:"Exam Machine", d:"Pass 10 module exams", i:"award", t:s=>s.exams>=10},
  {id:"summit", n:"Summit", d:"Pass every module exam", i:"mountain", t:s=>s.exams>=s.examsTotal&&s.examsTotal>0},
  {id:"streak-3", n:"On a Roll", d:"Practise 3 days in a row", i:"flame", t:s=>s.bestStreak>=3},
  {id:"streak-7", n:"Week Warrior", d:"Practise 7 days in a row", i:"flame", t:s=>s.bestStreak>=7},
  {id:"streak-30", n:"Unstoppable", d:"Practise 30 days in a row", i:"flame", t:s=>s.bestStreak>=30},
  {id:"solve-1", n:"Hello, Judge", d:"Get your first problem accepted", i:"braces", t:s=>s.solved>=1},
  {id:"solve-10", n:"Problem Solver", d:"Solve 10 problems", i:"target", t:s=>s.solved>=10},
  {id:"solve-30", n:"Algorithm Ace", d:"Solve 30 problems", i:"trophy", t:s=>s.solved>=30},
  {id:"hard-1", n:"Giant Slayer", d:"Solve a Hard problem", i:"zap", t:s=>s.hard>=1},
  {id:"step-1", n:"Bootcamper", d:"Pass your first bootcamp step", i:"cap", t:s=>s.steps>=1},
  {id:"course-1", n:"Graduate", d:"Finish a whole bootcamp course", i:"award", t:s=>s.courses>=1},
  {id:"courses-all", n:"Polyglot", d:"Finish every bootcamp course", i:"globe", t:s=>s.courses>=s.coursesTotal&&s.coursesTotal>0},
  {id:"build-1", n:"Builder", d:"Finish a guided Build & Learn project", i:"rocket", t:s=>s.built>=1},
  {id:"build-5", n:"Maker", d:"Finish 5 guided projects", i:"cube", t:s=>s.built>=5},
  {id:"node-1", n:"Pathfinder", d:"Check off your first career-path topic", i:"route", t:s=>s.nodes>=1},
  {id:"phase-1", n:"Phase Clear", d:"Complete a full phase of a career path", i:"layers", t:s=>s.phases>=1},
  {id:"path-1", n:"Job Ready", d:"Complete an entire career path", i:"brief", t:s=>s.paths>=1},
  {id:"cards-50", n:"Memory Palace", d:"Get 50 review cards past the first box", i:"refresh", t:s=>s.strongCards>=50},
  {id:"level-10", n:"Double Digits", d:"Reach level 10", i:"star", t:s=>s.level>=10}
];
const Game = {
  xpFor:n=>50*n*(n-1),
  levelOf(xp){ let n=1; while(this.xpFor(n+1)<=xp) n++; return n; },
  rank(l){ let r=RANKS[0][1]; RANKS.forEach(([n,t])=>{ if(l>=n) r=t; }); return r; },
  bestStreak(){ const days=Object.keys(P.log||{}).filter(k=>P.log[k]>0).sort(); let best=0, run=0, prev=null;
    days.forEach(k=>{ const n=Math.round(Date.parse(k)/86400000); run = prev!=null && n===prev+1 ? run+1 : 1; prev=n; best=Math.max(best,run); }); return best; },
  stats(){
    const lessons=Object.keys(P.lessons||{}).filter(k=>D.lessons[k]).length;
    const exams=D.mods.filter(m=>(P.exams[m.id]?.best??0)>=PASS).length;
    const ms=Object.keys(P.ms||{}).length;
    const cards=Object.values(S.cards||{}); const strongCards=cards.filter(c=>c.b>=1).length;
    const pb=PB.byId||{}; let solved=0, easy=0, medium=0, hard=0, pxp=0;
    Object.keys(P.solved||{}).forEach(id=>{ const p=pb[id]; if(!p) return; solved++; pxp+=XPV[p.difficulty]||0; if(p.difficulty==="Easy") easy++; else if(p.difficulty==="Medium") medium++; else hard++; });
    const steps=Object.keys(P.steps||{}).length;
    const built=PJ.list.filter(p=>p.steps.length&&p.steps.every(s=>P.steps?.[s.id])).length;
    const bc=BC.courses||[]; const courses=bc.filter(c=>c.steps.every(s=>P.steps?.[s.id])).length;
    const pidx=PATHS.index||[]; let phases=0, paths=0;
    pidx.forEach(p=>{ let all=true; (p.phases||[]).forEach(ph=>{ const ok=ph.nodes.length&&ph.nodes.every(n=>P.nodes?.[p.id+":"+n]==="done"); if(ok) phases++; else all=false; }); if(all&&p.phases?.length) paths++; });
    const nodes=Object.values(P.nodes||{}).filter(v=>v==="done").length;
    const parts={lessons:lessons*XPV.lesson, exams:exams*XPV.exam, projects:ms*XPV.milestone, reviews:strongCards*XPV.card, problems:pxp, bootcamp:steps*XPV.step, paths:nodes*XPV.node};
    const xp=Object.values(parts).reduce((a,b)=>a+b,0), level=this.levelOf(xp);
    return {lessons, lessonsTotal:Object.keys(D.lessons).length, exams, examsTotal:D.mods.length, ms, strongCards, solved, easy, medium, hard, steps, courses, coursesTotal:bc.length,
      nodes, phases, paths, built, projectsTotal:PJ.list.length, streak:streak(), bestStreak:Math.max(this.bestStreak(), streak()), xp, level, parts,
      next:this.xpFor(level+1), cur:this.xpFor(level)};
  },
  ready:false,
  sync(silent){
    const s=this.stats(); P.badges=P.badges||{}; let changed=false; const fresh=[];
    BADGES.forEach(b=>{ if(!P.badges[b.id] && b.t(s)){ P.badges[b.id]=today(); fresh.push(b); changed=true; } });
    const prevXp=P.xpSeen??s.xp, prevLv=this.levelOf(prevXp);
    if(P.xpSeen!==s.xp){ P.xpSeen=s.xp; changed=true; }
    if(!silent && this.ready){
      if(s.xp>prevXp) UI.toast(`+${s.xp-prevXp} XP`, `${s.xp.toLocaleString()} XP total · ${this.rank(s.level)}`, "zap", 2400);
      if(s.level>prevLv){ UI.toast(`Level ${s.level}!`, `You're now a ${this.rank(s.level)}.`, "star", 5000); UI.confetti(); }
      fresh.forEach((b,i)=>setTimeout(()=>{ UI.toast(`Badge unlocked: ${b.n}`, b.d, b.i, 5000); UI.confetti(90); }, 400+i*700));
    }
    this.ready=true;
    if(changed) save("p", true);
    UI.syncNav(currentTab());
  },
  ringSVG(s, size=120){ const r=size/2-9, c=2*Math.PI*r, p=Math.max(0,Math.min(1,(s.xp-s.cur)/Math.max(1,s.next-s.cur)));
    return `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" role="img" aria-label="Level ${s.level}, ${Math.round(p*100)} percent to next level"><defs><linearGradient id="lg${size}" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#8b7dff"/><stop offset=".55" stop-color="#38d3f0"/><stop offset="1" stop-color="#a3e635"/></linearGradient></defs>
    <circle cx="${size/2}" cy="${size/2}" r="${r}" fill="none" stroke="var(--sunk)" stroke-width="10"/><circle cx="${size/2}" cy="${size/2}" r="${r}" fill="none" stroke="url(#lg${size})" stroke-width="10" stroke-linecap="round" stroke-dasharray="${c*p} ${c}" transform="rotate(-90 ${size/2} ${size/2})"/>
    <text x="50%" y="${size/2-4}" text-anchor="middle" style="font:600 ${size/11}px var(--mono);fill:var(--muted)">LEVEL</text><text x="50%" y="${size/2+size/5.2}" text-anchor="middle" style="font:800 ${size/3.6}px var(--display);fill:var(--ink)">${s.level}</text></svg>`; }
};

/* ================= SEARCH PALETTE (Ctrl/Cmd + K) ================= */
const SEARCH_SOURCES = [];   // modules push () => [{t, sub, kind, i, r:route}]
SEARCH_SOURCES.push(()=>[...NAV, ...NAV_MORE].map(n=>({t:n.t, sub:"Go to section", kind:"Section", i:n.i, r:{v:n.v}})));
SEARCH_SOURCES.push(()=>D.mods.flatMap(m=>[{t:m.title, sub:`Stage ${m.si}: ${META[m.si].name} · module`, kind:"Module", i:"layers", r:{v:"map", stage:m.si}},
  ...m.lessons.map((l,i)=>({t:l.title, sub:`${m.title} · day ${i+1}`, kind:"Lesson", i:"book", r:{v:"lesson", id:l.id}}))]));
const Palette = {
  el:null, items:[], sel:0,
  open(){
    if(this.el) return; const all=SEARCH_SOURCES.flatMap(f=>{ try{ return f()||[]; }catch(e){ return []; } });
    this.all=all; PATHS.loadAll?.().then(()=>{ if(this.el){ this.all=SEARCH_SOURCES.flatMap(f=>{ try{ return f()||[]; }catch(e){ return []; } }); this.filter(); } });
    const bg=document.createElement("div"); bg.className="pal-bg"; bg.innerHTML=`<div class="pal" role="dialog" aria-label="Search"><div class="in">${icon("search")}<input id="palq" placeholder="Search lessons, problems, career paths, bootcamp steps…" autocomplete="off" spellcheck="false" aria-label="Search"><kbd>Esc</kbd></div><ul id="pall" role="listbox"></ul><div class="ft"><span>↑↓ to move</span><span>↵ to open</span><span>${all.length.toLocaleString()} items indexed</span></div></div>`;
    document.body.appendChild(bg); this.el=bg; const q=bg.querySelector("#palq"); q.focus();
    bg.addEventListener("click",e=>{ if(e.target===bg) this.close(); const b=e.target.closest("[data-k]"); if(b) this.pick(+b.dataset.k); });
    q.addEventListener("input",()=>{ this.sel=0; this.filter(); });
    q.addEventListener("keydown",e=>{ if(e.key==="ArrowDown"){ e.preventDefault(); this.move(1); } else if(e.key==="ArrowUp"){ e.preventDefault(); this.move(-1); } else if(e.key==="Enter"){ e.preventDefault(); this.pick(this.sel); } else if(e.key==="Escape") this.close(); });
    this.filter();
  },
  close(){ this.el?.remove(); this.el=null; },
  filter(){
    const q=(this.el.querySelector("#palq").value||"").toLowerCase().trim(), toks=q.split(/\s+/).filter(Boolean);
    let res;
    if(!toks.length) res=this.all.filter(x=>x.kind==="Section"||x.kind==="Career path"||x.kind==="Course").slice(0,40);
    else res=this.all.map(x=>{ const h=(x.t+" "+(x.sub||"")+" "+(x.kw||"")).toLowerCase(); if(!toks.every(t=>h.includes(t))) return null;
      const tl=x.t.toLowerCase(); let sc=0; if(tl===q) sc+=100; if(tl.startsWith(q)) sc+=50; if(tl.includes(q)) sc+=20; sc-=tl.length/40; sc+=({Section:6,"Career path":8,Course:5,Problem:4,Module:3,Lesson:2})[x.kind]||0; return {x,sc}; })
      .filter(Boolean).sort((a,b)=>b.sc-a.sc).slice(0,60).map(o=>o.x);
    this.items=res; this.sel=Math.min(this.sel,Math.max(0,res.length-1));
    const ul=this.el.querySelector("#pall");
    ul.innerHTML = res.length ? res.map((x,k)=>`<li><button type="button" data-k="${k}" role="option" aria-selected="${k===this.sel}"><span class="pi">${icon(x.i||"star","sm")}</span><span style="min-width:0"><span class="tt" style="display:block">${esc(x.t)}</span>${x.sub?`<span class="sub" style="display:block">${esc(x.sub)}</span>`:""}</span><span class="kd">${esc(x.kind)}</span></button></li>`).join("")
      : `<li class="empty" style="margin:10px">Nothing matches “${esc(q)}”. Try a topic like “recursion”, “sql” or “security”.</li>`;
  },
  move(d){ if(!this.items.length) return; this.sel=(this.sel+d+this.items.length)%this.items.length; this.el.querySelectorAll("[data-k]").forEach(b=>b.setAttribute("aria-selected", +b.dataset.k===this.sel)); this.el.querySelector(`[data-k="${this.sel}"]`)?.scrollIntoView({block:"nearest"}); },
  pick(k){ const x=this.items[k]; if(!x) return; this.close(); if(x.r.stage!=null) mapStage=x.r.stage; if(x.r.node){ PATHS.focusNode=x.r.node; } go({...x.r}); }
};
document.addEventListener("keydown",e=>{
  if((e.key==="k"||e.key==="K")&&(e.metaKey||e.ctrlKey)){ e.preventDefault(); Palette.el?Palette.close():Palette.open(); }
  else if(e.key==="/" && !/INPUT|TEXTAREA/.test(document.activeElement?.tagName||"") && !document.activeElement?.closest?.(".CodeMirror")){ e.preventDefault(); Palette.open(); }
});

/* ================= HOME (landing) ================= */
const TYPE_SNIPPETS = [
  {file:"hello.py", lines:[[["k","def "],["f","greet"],["","(name):"]],[["","    "],["k","return "],["s",'f"Hello, {name}! Ready to build?"']],[],[["f","print"],["","(greet("],["s",'"future engineer"'],["","))"]]], out:"Hello, future engineer! Ready to build?"},
  {file:"two_sum.js", lines:[[["k","function "],["f","twoSum"],["","(nums, target) {"]],[["","  "],["k","const "],["","seen = "],["k","new "],["f","Map"],["","();"]],[["","  "],["k","for "],["","("],["k","let "],["","i = "],["n","0"],["","; i < nums.length; i++) {"]],[["","    "],["k","const "],["","need = target - nums[i];"]],[["","    "],["k","if "],["","(seen.has(need)) "],["k","return "],["","[seen.get(need), i];"]],[["","    seen.set(nums[i], i);"]],[["","  }"]],[["","}"]],[["","console."],["f","log"],["","(twoSum(["],["n","2,7,11,15"],["","], "],["n","9"],["","));"]]], out:"[ 0, 1 ]"},
  {file:"query.sql", lines:[[["k","SELECT "],["","career, "],["f","COUNT"],["","(*) "],["k","AS "],["","learners"]],[["k","FROM "],["","codelearner.paths"]],[["k","GROUP BY "],["","career "],["k","ORDER BY "],["","learners "],["k","DESC"],["",";"]]], out:"AI Engineer      | ↑ fastest growing\nCybersecurity    | ↑ always hiring\nFull-Stack       | ↑ evergreen"}
];
function typeTerminal(pre, label){
  let si=0;
  const run = () => { if(!pre.isConnected) return; const sn=TYPE_SNIPPETS[si++%TYPE_SNIPPETS.length]; label.textContent=sn.file;
    const flat=[]; sn.lines.forEach((ln,li)=>{ ln.forEach(([c,t])=>[...t].forEach(ch=>flat.push([c,ch]))); flat.push(["","\n"]); });
    let k=0, html=""; const step=()=>{ if(!pre.isConnected) return;
      for(let j=0;j<2&&k<flat.length;j++,k++){ const [c,ch]=flat[k]; html+= c?`<span class="${c}">${esc(ch)}</span>`:esc(ch); }
      pre.innerHTML=html+`<span class="caret"></span>`;
      if(k<flat.length) setTimeout(step, 22+Math.random()*30);
      else setTimeout(()=>{ if(!pre.isConnected) return; pre.innerHTML=html+`\n<span class="c">$ run ${esc(sn.file)}</span>\n<span class="o">${esc(sn.out)}</span>\n<span class="caret"></span>`; setTimeout(run, 3200); }, 450); };
    step(); };
  if(matchMedia("(prefers-reduced-motion: reduce)").matches){ const sn=TYPE_SNIPPETS[0]; label.textContent=sn.file; pre.innerHTML=sn.lines.map(l=>l.map(([c,t])=>c?`<span class="${c}">${esc(t)}</span>`:esc(t)).join("")).join("\n")+`\n\n<span class="o">${esc(sn.out)}</span>`; return; }
  run();
}
function journeySVG(){
  const pts=META.map((s,i)=>{ const st=stageStats(s.id); return {i, s, p: st.lessons?st.done/st.lessons:0}; });
  return `<div class="journey rv"><svg viewBox="0 0 1000 400" role="img" aria-label="The nine-stage climb from Base Camp to Summit">
    <defs><linearGradient id="mtn" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="var(--accent)" stop-opacity=".35"/><stop offset="1" stop-color="var(--accent)" stop-opacity="0"/></linearGradient>
    <linearGradient id="mtn2" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="var(--accent-2)" stop-opacity=".22"/><stop offset="1" stop-color="var(--accent-2)" stop-opacity="0"/></linearGradient>
    <linearGradient id="trail" x1="0" x2="1"><stop offset="0" stop-color="#8b7dff"/><stop offset=".55" stop-color="#38d3f0"/><stop offset="1" stop-color="#a3e635"/></linearGradient></defs>
    <path d="M0 400 L120 300 L210 330 L330 210 L420 250 L560 120 L640 160 L780 40 L860 90 L1000 20 L1000 400Z" fill="url(#mtn2)"/>
    <path d="M0 400 L160 330 L260 350 L380 250 L470 280 L600 170 L690 200 L820 70 L900 110 L1000 60 L1000 400Z" fill="url(#mtn)"/>
    <path id="jtrail" d="M40 370 C140 360 170 320 230 318 S330 300 360 262 S450 240 500 222 S580 200 610 168 S700 150 730 122 S800 100 820 80 S900 52 950 34" fill="none" stroke="var(--line2)" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>
    <path d="M40 370 C140 360 170 320 230 318 S330 300 360 262 S450 240 500 222 S580 200 610 168 S700 150 730 122 S800 100 820 80 S900 52 950 34" fill="none" stroke="url(#trail)" stroke-width="4" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"><animate attributeName="stroke-dashoffset" from="100" to="0" dur="2.6s" fill="freeze" begin="0.3s"/></path>
    <g id="jpts">${pts.map(o=>`<g class="st" data-stage="${o.i}" data-act="map" tabindex="0" role="button" aria-label="Stage ${o.i}: ${esc(o.s.name)}"></g>`).join("")}</g>
    <g transform="translate(950 34)"><path d="M0 0 V-30 L22 -22 L0 -14" fill="var(--summit)" stroke="var(--summit)" stroke-width="2" stroke-linejoin="round"/></g>
  </svg></div>`;
}
function placeJourney(root){
  const path=root.querySelector("#jtrail"); if(!path||!path.getTotalLength) return; const L=path.getTotalLength();
  root.querySelectorAll("#jpts .st").forEach(g=>{ const i=+g.dataset.stage, pt=path.getPointAtLength(L*(0.02+0.96*i/8)); const st=stageStats(META[i].id), p=st.lessons?st.done/st.lessons:0;
    const up=i%2===0, ty=up?-22:34;
    g.innerHTML=`<circle cx="${pt.x}" cy="${pt.y}" r="15" fill="var(--bg)" opacity=".9"/><circle class="dot" cx="${pt.x}" cy="${pt.y}" r="8" fill="${p>=1?"var(--ok)":p>0?"var(--accent-2)":"var(--surface)"}" stroke="${p>0?"var(--accent-2)":"var(--line2)"}" stroke-width="3"/>
      <text class="k" x="${pt.x}" y="${pt.y+ty-14}" text-anchor="middle">STAGE ${i}</text><text x="${pt.x}" y="${pt.y+ty}" text-anchor="middle">${esc(META[i].name)}</text>`; });
}
function viewHome(el){
  const nL=Object.keys(D.lessons).length, nQ=Object.keys(D.q).length, nP=PB.list.length||0, nC=PATHS.index.length||0, nS=(BC.courses||[]).reduce((a,c)=>a+c.steps.length,0), nB=PJ.list.length;
  const g=Game.stats(); const started=g.xp>0;
  const firstCourse=BC.courses?.[0];
  const feats=[
    {i:"cap", t:"Bootcamp", d:"Never coded before? Start here. Bite-sized steps, a live editor and instant checks, freeCodeCamp-style. Build a web page, write Python and JavaScript, query a database.", v:"bootcamp", c:`${nS} interactive steps`},
    {i:"map", t:"The 10,000-Hour Map", d:"A 9-stage core curriculum from your first program to distributed systems. Daily lessons with visuals, runnable examples and spaced-repetition quizzes.", v:"map", c:`${nL} lessons · ${nQ.toLocaleString()} questions`},
    {i:"route", t:"Career Paths", d:"roadmap.sh-style roadmaps for every job in software: AI, security, cloud, games, mobile and more. Each one is a phased curriculum with projects.", v:"paths", c:`${nC} careers`},
    {i:"braces", t:"Problems", d:"LeetCode-style challenges judged right in your browser in Python or JavaScript, with hints, editorials and the patterns behind them.", v:"problems", c:`${nP} problems`},
    {i:"refresh", t:"Spaced review", d:"Every question you answer comes back right before you'd forget it, on a 1 → 3 → 7 → 16 → 35-day schedule. Memory that compounds.", v:"review", c:"Leitner system"},
    {i:"rocket", t:"Build & Learn", d:"Pick a real project (a to-do app, a game, a bank system, a database) and build it step by step, learning each concept the moment you need it.", v:"build", c:`${nB} guided projects`}
  ];
  const featured=(PATHS.index||[]).slice(0,8);
  el.innerHTML = `
  <section class="hero">
    <div class="orb" style="width:340px;height:340px;background:#8b7dff;left:-120px;top:-60px"></div>
    <div class="orb" style="width:300px;height:300px;background:#38d3f0;right:10%;top:40%;animation-delay:-5s"></div>
    <div style="display:grid;gap:22px;align-content:center">
      <span class="badge-line"><b>FREE</b> Everything runs in your browser. No sign-up, no paywall.</span>
      <h1>From your first line of code to <span class="gt">world-class engineer.</span></h1>
      <p class="lede">CodeLearner, the free coding school from CodeBay, is one place to learn programming end to end: an interactive bootcamp for total beginners, guided projects you build step by step, a 10,000-hour core curriculum, career roadmaps for every specialty and a problem judge to sharpen your skills. Built on the science of how people actually learn.</p>
      <div class="row" style="gap:12px">
        ${started?`<button class="btn grad lg" data-act="today">${icon("dash")}Continue learning</button>`:`<button class="btn grad lg" ${firstCourse?`data-course="${firstCourse.id}"`:`data-act="bootcamp"`}>${icon("play")}Start from zero</button>`}
        <button class="btn lg" data-act="paths">${icon("route")}Choose a career</button>
        <button class="btn lg ghost" data-act="problems">${icon("braces")}Solve problems</button>
      </div>
      <div class="row muted" style="font-size:.88rem;gap:18px">${["Python 3.12 in-browser","Auto-graded","Progress saved"].map(t=>`<span class="row" style="gap:6px">${icon("check","sm")}${t}</span>`).join("")}</div>
    </div>
    <div class="term rv"><div class="tb"><i></i><i></i><i></i><span id="termf">hello.py</span></div><pre id="termp"></pre></div>
  </section>
  <section class="counters">
    ${[[nL,"core lessons"],[nQ,"quiz questions"],[nP,"judged problems"],[nC,"career roadmaps"],[nS,"bootcamp steps"],[nB,"guided projects"]].map(([n,t])=>`<div class="counter rv"><b class="gt" data-count="${n}">0</b><span>${t}</span></div>`).join("")}
  </section>
  <section style="display:grid;gap:18px">
    <div class="sec-h rv"><div class="head"><span class="eyebrow">Everything in one place</span><h2 class="h2">Six ways to level up</h2></div><p class="lede" style="max-width:48ch">The structure of a university degree, the hands-on feel of a bootcamp and the practice volume of an interview grind.</p></div>
    <div class="feat">${feats.map(f=>`<button type="button" class="fcard glow rv" data-act="${f.v}"><span class="fi">${icon(f.i,"lg")}</span><h3>${f.t}</h3><p>${f.d}</p><span class="row" style="justify-content:space-between"><span class="pill acc">${f.c}</span><span class="go">Open ${icon("arrow","sm")}</span></span></button>`).join("")}</div>
  </section>
  <section style="display:grid;gap:18px">
    <div class="sec-h rv"><div class="head"><span class="eyebrow">The core curriculum</span><h2 class="h2">The climb: 9 stages, 10,000 hours</h2></div><button class="btn" data-act="map">Open the map ${icon("arrow","sm")}</button></div>
    ${journeySVG()}
    <div class="ladder">${META.map((s,i)=>`<button type="button" data-stage="${i}" data-act="map"><span class="k">STAGE ${i} · ${esc(s.span)}</span><span class="nm">${esc(s.name)}</span><span class="muted" style="font-size:.8rem">${esc(s.goal)}</span></button>`).join("")}</div>
  </section>
  ${featured.length?`<section style="display:grid;gap:18px">
    <div class="sec-h rv"><div class="head"><span class="eyebrow">Career paths</span><h2 class="h2">Pick where you want to end up</h2></div><button class="btn" data-act="paths">All ${nC} paths ${icon("arrow","sm")}</button></div>
    <div class="pgrid">${featured.map(p=>pathCard(p)).join("")}</div></section>`:""}
  <section style="display:grid;gap:18px">
    <div class="head rv"><span class="eyebrow">The method</span><h2 class="h2">How you become great, not just familiar</h2></div>
    <ol class="steps4">
      <li class="rv"><b>Learn one idea a day</b><span>A worked example first, then a visual, then you write the code yourself.</span></li>
      <li class="rv"><b>Retrieve it, don't reread it</b><span>Every lesson ends with recall, apply and analyze questions graded instantly.</span></li>
      <li class="rv"><b>Build real things</b><span>Each module ends in a project; each career path ends in a portfolio.</span></li>
      <li class="rv"><b>Review on a schedule</b><span>Spaced repetition brings each idea back just before you'd forget it.</span></li>
    </ol>
  </section>
  <section class="cta rv">
    <span class="eyebrow" style="color:#0a0b1a;opacity:.7">Your first hour</span>
    <h2>Write your first program in the next five minutes.</h2>
    <p>No installs. Open the bootcamp, type one line, press Run. That's the whole setup.</p>
    <div class="row"><button class="btn lg" ${firstCourse?`data-course="${firstCourse.id}"`:`data-act="bootcamp"`}>${icon("play")}Start the bootcamp</button><button class="btn lg" style="background:transparent;color:#0a0b1a;border-color:rgba(10,11,26,.35)" data-act="method">Why this works</button></div>
  </section>`;
  typeTerminal(el.querySelector("#termp"), el.querySelector("#termf"));
  placeJourney(el);
}
function pathCard(p){
  const done=(p.phases||[]).reduce((a,ph)=>a+ph.nodes.filter(n=>P.nodes?.[p.id+":"+n]==="done").length,0), tot=(p.phases||[]).reduce((a,ph)=>a+ph.nodes.length,0);
  return `<button type="button" class="pcard rv" style="--h:${esc(p.hue)}" data-path="${esc(p.id)}"><span class="row" style="justify-content:space-between;align-items:start"><span class="pico">${icon(p.icon,"lg")}</span>${done?`<span class="pill acc">${Math.round(100*done/Math.max(1,tot))}%</span>`:`<span class="pill">${esc(p.cat)}</span>`}</span>
    <h3>${esc(p.title)}</h3><p>${esc(p.tagline)}</p><span class="meta"><span>${p.phases.length} phases</span><span>·</span><span>${tot} topics</span><span>·</span><span>${esc(p.duration)}</span></span>${done?`<span class="bar"><i style="width:${100*done/Math.max(1,tot)}%"></i></span>`:""}</button>`;
}

/* ================= PROFILE ================= */
function viewProfile(el){
  const s=Game.stats(); const got=BADGES.filter(b=>P.badges?.[b.id]);
  const parts=[["Core lessons","lessons","book"],["Module exams","exams","lock"],["Projects","projects","rocket"],["Review cards","reviews","refresh"],["Problems","problems","braces"],["Bootcamp & projects","bootcamp","cap"],["Career paths","paths","route"]];
  const mx=Math.max(1,...Object.values(s.parts));
  el.innerHTML=`<section class="head"><span class="eyebrow">Your profile</span><h1 class="h1">${esc(Game.rank(s.level))}</h1><p class="lede">Every lesson, exam, problem and roadmap topic earns XP. Level up by learning, not by grinding: XP is recomputed from your real progress, so it always reflects what you've actually done.</p></section>
  <div class="grid2">
    <section class="panel"><div class="lvcardx">${Game.ringSVG(s,150)}<div style="display:grid;gap:8px"><b class="h2"><span class="gt">${s.xp.toLocaleString()}</span> XP</b><span class="muted">${(s.next-s.xp).toLocaleString()} XP to level ${s.level+1} · next rank: ${esc(Game.rank(RANKS.find(r=>r[0]>s.level)?.[0]||s.level))}</span><div class="bar"><i style="width:${100*(s.xp-s.cur)/Math.max(1,s.next-s.cur)}%"></i></div>
      <div class="row" style="gap:6px">${[["flame",`${s.streak}-day streak`],["award",`${got.length}/${BADGES.length} badges`],["braces",`${s.solved} solved`]].map(([i,t])=>`<span class="pill">${icon(i,"sm")}${t}</span>`).join("")}</div></div></div></section>
    <section class="panel"><h2 class="h3">Where your XP comes from</h2><div class="mast">${parts.map(([t,k])=>`<div class="r"><span>${t}</span><span class="t" data-tip="${s.parts[k].toLocaleString()} XP"><i style="width:${100*s.parts[k]/mx}%"></i></span><span class="n">${s.parts[k].toLocaleString()}</span></div>`).join("")}</div>
      <p class="muted" style="margin:0;font-size:.84rem">Lesson ${XPV.lesson} · exam ${XPV.exam} · milestone ${XPV.milestone} · card ${XPV.card} · Easy/Medium/Hard ${XPV.Easy}/${XPV.Medium}/${XPV.Hard} · step ${XPV.step} · roadmap topic ${XPV.node}</p></section>
  </div>
  <section style="display:grid;gap:14px"><div class="sec-h"><h2 class="h2">Badges</h2><span class="pill acc">${got.length} of ${BADGES.length} unlocked</span></div>
    <div class="badges">${BADGES.map(b=>`<div class="bdg ${P.badges?.[b.id]?"got":""}"><span class="md">${icon(b.i,"lg")}</span><b>${esc(b.n)}</b><span>${esc(b.d)}</span>${P.badges?.[b.id]?`<span class="pill ok">${fmtDay(P.badges[b.id])}</span>`:""}</div>`).join("")}</div></section>
  <section class="panel"><h2 class="h3">Ranks</h2><div class="row">${RANKS.map(([n,t])=>`<span class="pill ${s.level>=n?"acc":""}">Lv ${n}+ · ${t}</span>`).join("")}</div></section>
  <section class="panel"><h2 class="h3">Back up your progress</h2><p class="muted" style="margin:0">Progress lives in this browser${stores.p?" and your account":""}. Download a backup file, or restore one on another device.</p>
    <div class="row"><button class="btn" id="exp">${icon("download")}Download backup</button><label class="btn ghost" style="cursor:pointer">${icon("upload")}Restore from file<input type="file" id="imp" accept="application/json" hidden></label><span id="impmsg" class="muted" style="font-size:.88rem"></span></div></section>`;
  el.querySelector("#exp").onclick=()=>{ const a=document.createElement("a"); a.href=URL.createObjectURL(new Blob([JSON.stringify({app:"codelearner",v:3,P,S},null,1)],{type:"application/json"})); a.download=`codelearner-backup-${dayKey(today())}.json`; document.body.appendChild(a); a.click(); a.remove(); };
  el.querySelector("#imp").onchange=async e=>{ const f=e.target.files[0]; if(!f) return; try{ const d=JSON.parse(await f.text()); if(d.app!=="codelearner"||!d.P) throw 0; P=normP(d.P); S={cards:d.S?.cards||{}}; save("p"); save("s"); el.querySelector("#impmsg").textContent="Restored."; Game.sync(true); render(); }catch(err){ el.querySelector("#impmsg").textContent="That file isn't a CodeLearner backup."; } };
}
