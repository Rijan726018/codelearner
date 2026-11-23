"use strict";
/* ---------- the Today page's launch area: a hero with one obvious next step and a live editor, a field of drifting
   syntax tokens behind it, a 60-second "what does this print?" puzzle, count-up stat tiles, and tilting cards.
   Colour stays reserved for code (the tokens and the editor use VS Code's palettes); everything else is the usual
   graphite. With prefers-reduced-motion, the tokens are drawn once and nothing moves. ---------- */
const Launch = (() => {
  const still = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const dark = () => { const t = document.documentElement.dataset.theme; return t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches; };

  // the single best thing to do right now
  function next(){
    const pd = typeof Mastery !== "undefined" ? Mastery.due() : [];
    if(pd.length) return {k:"Problem review", t:`Re-solve ${pd[0].title} from memory`, a:`data-review="${pd[0].id}"`, i:"refresh", cta:"Start the review"};
    const dc = dueCards().length;
    if(dc) return {k:"Reviews", t:`${dc} question card${dc>1?"s":""} waiting, about ${Math.max(2, Math.round(dc*0.6))} minutes`, a:`data-act="review"`, i:"refresh", cta:"Start reviewing"};
    const ns = BC.focusStep?.(), started = Object.keys(P.steps || {}).length, nl = nextLesson();
    if(ns && (ns.main || started)) return {k: ns.main ? "Your main course" : "Bootcamp", t:`${ns.course.title}: ${ns.step.title}`, a:`data-course="${ns.course.id}" data-step="${ns.idx}"`, i:"cap", cta: started ? "Continue coding" : "Start coding"};
    if(nl && Object.keys(P.lessons || {}).length) return {k:"Core curriculum", t:nl.title, a:`data-lesson="${nl.id}"`, i:"map", cta:"Open the lesson"};
    if(ns) return {k:"Bootcamp", t:`${ns.course.title}: ${ns.step.title}`, a:`data-course="${ns.course.id}" data-step="${ns.idx}"`, i:"cap", cta:"Write your first line"};
    const dp = PB.daily?.(); if(dp) return {k:"Problem of the day", t:dp.title, a:`data-problem="${dp.id}"`, i:"braces", cta:"Solve it"};
    return {k:"Editor", t:"A blank file and a Run button", a:`data-act="editor"`, i:"terminal", cta:"Open the editor"};
  }
  function greeting(){
    const h = new Date().getHours();
    return h < 5 ? "Late-night session?" : h < 12 ? "Good morning." : h < 18 ? "Good afternoon." : h < 22 ? "Good evening." : "One more before bed?";
  }

  function hero(g){
    const n = next(), st = streak(), probDue = typeof Mastery !== "undefined" ? Mastery.due().length : 0, due = dueCards().length + probDue;
    return `<section class="launch" id="launch">
      <canvas class="lfx" aria-hidden="true"></canvas><div class="lspot" aria-hidden="true"></div>
      <div class="lgrid">
        <div class="lcopy">
          <div class="row" style="gap:8px"><span class="eyebrow">${new Date().toLocaleDateString(undefined,{weekday:"long",month:"long",day:"numeric"})}</span>
            ${st ? `<span class="pill lflame">${icon("flame","sm")}${st}-day streak</span>` : `<span class="pill">${icon("flame","sm")}Start a streak today</span>`}</div>
          <h1 class="lh"><span class="lh1">${greeting()}</span><span class="lh2">Your next line of code<br>is waiting.</span></h1>
          <p class="lup"><span class="eyebrow">Up next · ${esc(n.k)}</span><b>${esc(n.t)}</b></p>
          <div class="row lcta"><button type="button" class="btn lgo" ${n.a}>${icon("play","sm")}<span>${esc(n.cta)}</span>${icon("arrow","sm")}</button>
            <button type="button" class="btn ghost" id="lpuzzle">${icon("zap","sm")}60-second puzzle</button>
            ${typeof Focus !== "undefined" && !Focus.state ? `<button type="button" class="btn ghost" data-focus="start">${icon("clock","sm")}Focus 50 min</button>` : ""}</div>
        </div>
        <div class="term lterm"><div class="tb"><i></i><i></i><i></i><span id="ltermf">hello.py</span></div><pre id="ltermp"></pre></div>
      </div></section>
    <div class="tstats">
      <div class="tstat rv lvl">${Game.ringSVG(g, 64)}<div><b data-count="${g.xp}">0</b><span>XP · level ${g.level} ${esc(Game.rank(g.level))}</span><div class="bar"><i style="width:${100*(g.xp-g.cur)/Math.max(1,g.next-g.cur)}%"></i></div></div></div>
      <div class="tstat rv ${st ? "hot" : ""}"><span class="ti">${icon("flame")}</span><b data-count="${st}">0</b><span>day streak</span></div>
      <div class="tstat rv"><span class="ti">${icon("refresh")}</span><b data-count="${due}">0</b><span>reviews due</span></div>
      <div class="tstat rv"><span class="ti">${icon("braces")}</span><b data-count="${g.solved}">0</b><span>problems solved</span></div>
      <div class="tstat rv"><span class="ti">${icon("clock")}</span><b>${typeof Clock !== "undefined" ? fmtHours(Clock.stats().total) : "0"}</b><span>hours practised</span></div>
    </div>`;
  }

  /* ---- drifting syntax tokens (VS Code Dark+ / Light+ colours), pushed aside by the cursor ---- */
  const TOK = [["def","k"],["for","c"],["if","c"],["return","c"],["=>","k"],["{ }","p"],["[ ]","p"],["( )","p"],["const","k"],["let","k"],["while","c"],["print()","f"],[".map()","f"],["len()","f"],
    ["&&","p"],["==","p"],["+=","p"],["import","c"],["class","k"],["async","k"],["await","c"],["0","n"],["1","n"],["42","n"],["true","k"],["None","k"],["\"hello\"","s"],["'world'","s"],["# todo","m"],["// why?","m"],["Map","t"],["Set","t"],["list","t"]];
  const PAL = {dark:{k:"#569cd6",c:"#c586c0",f:"#dcdcaa",s:"#ce9178",n:"#b5cea8",m:"#6a9955",t:"#4ec9b0",p:"#9cdcfe"}, light:{k:"#0000ff",c:"#af00db",f:"#795e26",s:"#a31515",n:"#098658",m:"#008000",t:"#267f99",p:"#001080"}};
  function field(cv, host){
    const ctx = cv.getContext("2d"); let W = 0, H = 0, dpr = 1, mx = -999, my = -999, raf = 0;
    const parts = [];
    const size = () => { const r = host.getBoundingClientRect(); dpr = Math.min(2, devicePixelRatio || 1); W = r.width; H = r.height; cv.width = W*dpr; cv.height = H*dpr; cv.style.width = W + "px"; cv.style.height = H + "px"; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
    size();
    const count = Math.round(Math.min(46, Math.max(18, W*H/14000)));
    for(let i = 0; i < count; i++){ const [t, c] = TOK[i % TOK.length];
      parts.push({t, c, x: Math.random()*W, y: Math.random()*H, z: .5 + Math.random()*.9, vy: -(.08 + Math.random()*.22), ph: Math.random()*6.28, ox: 0, oy: 0}); }
    const draw = time => {
      if(!cv.isConnected){ cancelAnimationFrame(raf); removeEventListener("resize", size); return; }
      const pal = PAL[dark() ? "dark" : "light"]; ctx.clearRect(0, 0, W, H);
      for(const p of parts){
        if(!still()){ p.y += p.vy * p.z; p.x += Math.sin(time/2400 + p.ph) * .12 * p.z; if(p.y < -20){ p.y = H + 20; p.x = Math.random()*W; } }
        const dx = p.x - mx, dy = p.y - my, d = Math.hypot(dx, dy), push = d < 150 ? (150 - d) / 150 : 0;
        p.ox += ((push ? dx / (d || 1) * push * 26 : 0) - p.ox) * .08; p.oy += ((push ? dy / (d || 1) * push * 26 : 0) - p.oy) * .08;
        ctx.globalAlpha = Math.min(.8, (dark() ? .16 : .1) * p.z + push * (dark() ? .55 : .4));
        ctx.font = `${Math.round(11 + 7*p.z)}px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`;
        ctx.fillStyle = pal[p.c]; ctx.fillText(p.t, p.x + p.ox, p.y + p.oy);
      }
      ctx.globalAlpha = 1;
      if(!still()) raf = requestAnimationFrame(draw);
    };
    host.addEventListener("pointermove", e => { const r = host.getBoundingClientRect(); mx = e.clientX - r.left; my = e.clientY - r.top;
      host.style.setProperty("--mx", mx + "px"); host.style.setProperty("--my", my + "px"); if(still()) draw(performance.now()); });
    host.addEventListener("pointerleave", () => { mx = my = -999; });
    addEventListener("resize", size);
    raf = requestAnimationFrame(draw);
  }

  /* ---- the 60-second puzzle: a verified concept example, "what does this print?" ---- */
  let lastCard = null;
  async function puzzle(host){
    const data = await loadConcepts(); if(!host.isConnected) return;
    if(!data){ host.remove(); return; }
    const L = pbLang === "js" ? "js" : "py", all = Object.values(data.cards).filter(c => c.id !== "big-o" && c[L + "_out"].length < 160);
    const fresh = all.filter(c => !P.learned?.[c.id] && c.id !== lastCard), pool = fresh.length ? fresh : all.filter(c => c.id !== lastCard);
    const c = pool[Math.floor(Math.random() * pool.length)]; lastCard = c.id;
    let solved = 0; try{ solved = +sessionStorage.getItem("cl-puz") || 0; }catch(e){}
    host.innerHTML = `<div class="sec-h"><span class="row" style="gap:8px">${icon("zap")}<span class="eyebrow">60-second puzzle · ${L === "js" ? "JavaScript" : "Python"}</span></span>${solved ? `<span class="pill ok">${solved} solved today</span>` : ""}</div>
      <h2 class="h3">${esc(c.title)}</h2>
      ${codeBlock(c[L], null, L === "js" ? "javascript" : "python")}
      <label for="pzin" class="muted" style="font-size:.9rem">What does this print? Trace it in your head, then type the output.</label>
      <textarea id="pzin" class="pred" rows="${Math.min(4, c[L + "_out"].split("\n").length)}" spellcheck="false" autocomplete="off" placeholder="Your answer"></textarea>
      <div class="row"><button type="button" class="btn primary" id="pzchk">${icon("check","sm")}Check</button><button type="button" class="btn ghost" id="pzshow">Show me</button><button type="button" class="btn ghost" id="pznext" style="margin-left:auto">${icon("shuffle","sm")}Another one</button></div>
      <div id="pzres" aria-live="polite"></div>`;
    const inp = host.querySelector("#pzin"), res = host.querySelector("#pzres"), out = c[L + "_out"];
    const done = ok => {
      P.learned = P.learned || {}; if(!P.learned[c.id]) { P.learned[c.id] = today(); save("p", true); }
      if(ok){ solved++; try{ sessionStorage.setItem("cl-puz", solved); }catch(e){} host.classList.remove("pzok"); void host.offsetWidth; host.classList.add("pzok"); if(!still()) UI.confetti(70); }
      res.innerHTML = `<div class="wfb ${ok ? "ok" : "no"}">${ok ? `<b>${icon("checkc","sm")} Exactly right.</b> ${solved > 1 ? `That's ${solved} today.` : "Your brain just ran code."}` : `<b>It prints:</b><pre class="cout">${esc(out)}</pre>`}<span class="muted" style="font-size:.88rem">${md(c.kid)}</span></div>`;
      host.querySelectorAll("#pzchk,#pzshow").forEach(b => b.disabled = true); inp.readOnly = true; host.querySelector("#pznext").focus();
    };
    host.querySelector("#pzchk").onclick = () => { if(!inp.value.trim()){ inp.focus(); return; } done(normOut(inp.value) === normOut(out)); };
    host.querySelector("#pzshow").onclick = () => done(false);
    host.querySelector("#pznext").onclick = () => puzzle(host);
    inp.addEventListener("keydown", e => { if(e.key === "Enter" && !e.shiftKey && c[L + "_out"].split("\n").length === 1){ e.preventDefault(); host.querySelector("#pzchk").click(); } });
  }

  // cards lean toward the cursor, with a soft light where it is
  function tilt(root){
    if(still() || !matchMedia("(hover: hover)").matches) return;
    root.querySelectorAll(".ccard, .tstat").forEach(c => {
      c.addEventListener("pointermove", e => { const r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        c.style.setProperty("--rx", ((.5 - y) * 6).toFixed(2) + "deg"); c.style.setProperty("--ry", ((x - .5) * 8).toFixed(2) + "deg");
        c.style.setProperty("--mx", (x*100).toFixed(1) + "%"); c.style.setProperty("--my", (y*100).toFixed(1) + "%"); c.classList.add("tilt"); });
      c.addEventListener("pointerleave", () => { c.style.setProperty("--rx", "0deg"); c.style.setProperty("--ry", "0deg"); c.classList.remove("tilt"); });
    });
  }

  function mount(el){
    const host = el.querySelector("#launch"); if(!host) return;
    field(host.querySelector(".lfx"), host);
    typeTerminal(host.querySelector("#ltermp"), host.querySelector("#ltermf"));
    host.querySelector("#lpuzzle").onclick = () => { const pz = el.querySelector("#tpuzzle"); pz?.scrollIntoView({behavior: still() ? "auto" : "smooth", block:"center"}); setTimeout(() => pz?.querySelector("#pzin")?.focus({preventScroll:true}), still() ? 0 : 450); };
    const pz = el.querySelector("#tpuzzle"); if(pz) puzzle(pz);
    tilt(el);
  }
  return {next, hero, mount};
})();
