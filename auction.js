"use strict";
/* ---------- Code Auction: list a cloud project, bid in US dollars, settle privately ----------
   Data lives in Firestore (cloud.js -> provider.auctions()); firestore.rules is the referee: bids must beat the last by $1,
   land before the end time and never come from the seller, and only the seller and the winner see the files and the deal.
   CodeBay does not move money yet. When a lot ends with a bid, the seller and the winner get a private thread to agree
   payment, and the seller releases the files once paid. The winner then copies them into their own projects.
   Amounts are whole cents. P.auction = {uid, name, bids:[lot ids]} keeps your public trading name (for that account) and the lots you bid on. */

const AUC = {
  DURATIONS: [[1, "1 day"], [3, "3 days"], [5, "5 days"], [7, "7 days"]],
  INC: 100,                // minimum raise, in cents (firestore.rules checks the same number)
  MAX: 10000000,           // $100,000 cap on any bid or starting price
  watch: null, timer: null,
};
const money = c => (c / 100).toLocaleString("en-US", {style: "currency", currency: "USD"});
const centsOf = v => { const n = Math.round(parseFloat(String(v).replace(/[$,\s]/g, "")) * 100); return Number.isFinite(n) ? n : NaN; };
function timeLeft(end, now = Date.now()){
  const s = Math.floor((end - now) / 1000); if(s <= 0) return "Ended";
  const d = Math.floor(s / 86400), h = Math.floor(s % 86400 / 3600), m = Math.floor(s % 3600 / 60);
  return d ? `${d} d ${h} h` : h ? `${h} h ${m} min` : m ? `${m} min ${s % 60} s` : `${s} s`;
}
const lotState = (a, now = Date.now()) => a.status === "cancelled" ? "cancelled" : now < a.endsAt ? "live" : a.bidCount ? "sold" : "unsold";
const nextBid = a => a.bidCount ? a.topBid + AUC.INC : a.startBid;
const auApi = () => (typeof Account !== "undefined" ? Account.auctions() : null);
const auUser = () => (typeof Account !== "undefined" ? Account.user : null);
const tradeName = () => (P.auction?.uid && P.auction.uid === auUser()?.uid ? P.auction.name || "" : "").trim();
function suggestName(){
  const u = auUser(); const g = u && !/@/.test(u.name || "") ? (u.name || "").split(/\s+/)[0] : "";
  return (tradeName() || P.board?.name || g || "").slice(0, 40);
}
function setTradeName(n){ P.auction = {...(P.auction || {}), uid: auUser()?.uid || "", name: n.trim().replace(/\s+/g, " ").slice(0, 40)}; save("p", true); }
function rememberBid(id){ const b = (P.auction?.bids || []).filter(x => x !== id); P.auction = {...(P.auction || {}), bids: [id, ...b].slice(0, 100)}; save("p", true); }
function stopLotWatch(){ try{ AUC.watch?.(); }catch(e){} AUC.watch = null; clearInterval(AUC.timer); AUC.timer = null; }
const AUC_LANG = {python: "Python", js: "JavaScript", web: "Web page", sql: "SQL"};

const auIntro = `CodeBay doesn't take payment yet. When a lot ends, the seller and the winner get a private thread to agree how to pay, and the seller releases the files once they've been paid. Only bid what you'll actually pay.`;

function auNeedsAccounts(el, title){
  el.innerHTML = `<section class="head"><span class="eyebrow">Code Auction</span><h1 class="h1">${esc(title)}</h1></section>
    <section class="panel"><p style="margin:0">The Code Auction runs on CodeBay accounts, and this copy of the site runs without them.</p></section>`;
}

/* ---------- browse ---------- */
function viewAuction(el){
  stopLotWatch();
  const api = auApi(); if(!api){ auNeedsAccounts(el, "Code Auction"); return; }
  const tab = ["ended", "mine", "bids"].includes(route.id) ? route.id : "live", u = auUser();
  const tabs = [["live", "Live"], ["ended", "Ended"], ["mine", "My listings"], ["bids", "My bids"]];
  el.innerHTML = `<section class="head"><span class="eyebrow">Code Auction</span><h1 class="h1">Code Auction</h1>
      <p class="lede">Put a project you built up for auction, or bid on one someone else made. Every lot is a real project from the seller's CodeBay editor, and bids are in US dollars.</p>
      <div class="row"><button class="btn primary lg" id="auSell">${icon("upload")}List a project</button>${u ? "" : `<button class="btn lg" id="auIn">${icon("user")}Sign in to bid</button>`}</div></section>
    <div class="aunote">${icon("shield", "sm")}<span>${esc(auIntro)}</span></div>
    <div class="chips" role="group" aria-label="Show">${tabs.map(([k, t]) => `<button type="button" class="chip" data-autab="${k}" aria-pressed="${tab === k}">${t}</button>`).join("")}</div>
    <div id="lots" class="lots" aria-live="polite"><div class="muted">Loading lots…</div></div>`;
  el.querySelector("#auSell").onclick = () => go({v: "sell"});
  el.querySelector("#auIn")?.addEventListener("click", () => Account.signIn());
  el.querySelectorAll("[data-autab]").forEach(b => b.onclick = () => go({v: "auction", ...(b.dataset.autab === "live" ? {} : {id: b.dataset.autab})}));
  const box = el.querySelector("#lots"), stamp = location.hash;
  (async () => {
    let rows = [], empty = "";
    try{
      if(tab === "live"){ rows = (await api.live()).filter(a => a.status !== "cancelled"); empty = "Nothing is up for auction right now. List a project and yours will be the first."; }
      else if(tab === "ended"){ rows = (await api.ended()).filter(a => a.status !== "cancelled"); empty = "No auctions have ended yet."; }
      else if(!u){ box.innerHTML = `<div class="panel"><p style="margin:0">Sign in to see ${tab === "mine" ? "the projects you've listed" : "the lots you've bid on"}.</p><div class="row"><button class="gbtn" data-signin>${GOOGLE_G}<span>Sign in with Google</span></button></div></div>`;
        box.querySelector("[data-signin]").onclick = () => Account.signIn(); return; }
      else if(tab === "mine"){ rows = (await api.bySeller(u.uid)).sort((a, b) => b.created - a.created); empty = "You haven't listed anything yet."; }
      else { const ids = (P.auction?.bids || []).slice(0, 30); rows = (await Promise.all(ids.map(id => api.get(id).catch(() => null)))).filter(Boolean); empty = "You haven't bid on anything yet."; }
    }catch(e){ console.warn("auction list", e); if(location.hash === stamp) box.innerHTML = `<div class="panel"><p class="err" style="margin:0">Couldn't load the auction. Check your connection and try again.</p></div>`; return; }
    if(location.hash !== stamp || !box.isConnected) return;
    box.innerHTML = rows.length ? rows.map(lotCard).join("") : `<div class="panel"><p class="muted" style="margin:0">${esc(empty)}</p></div>`;
    box.querySelectorAll("[data-lot]").forEach(b => b.onclick = () => go({v: "lot", id: b.dataset.lot}));
    tickCards(box);
  })();
}
function lotCard(a){
  const st = lotState(a), me = auUser()?.uid;
  const label = st === "live" ? (a.bidCount ? "Current bid" : "Starting bid") : st === "sold" ? "Sold for" : st === "cancelled" ? "Withdrawn" : "No bids";
  const tag = me && a.sellerUid === me ? `<span class="pill">Yours</span>` : me && a.topUid === me && a.bidCount ? `<span class="pill ok">${st === "live" ? "You're winning" : "You won"}</span>` : "";
  return `<button type="button" class="lot" data-lot="${esc(a.id)}">
    <span class="row" style="justify-content:space-between"><span class="eyebrow">${esc(AUC_LANG[a.lang] || a.lang)} · ${a.files?.length || 0} file${a.files?.length === 1 ? "" : "s"}</span>${tag}</span>
    <b class="lt">${esc(a.title)}</b>
    <span class="muted ls">by ${esc(a.sellerName)}</span>
    <span class="lp"><span><small>${label}</small><strong>${st === "cancelled" || st === "unsold" ? "–" : money(a.bidCount ? a.topBid : a.startBid)}</strong></span>
      <span style="text-align:right"><small>${a.bidCount} bid${a.bidCount === 1 ? "" : "s"}</small><strong class="tl" data-end="${a.endsAt}">${st === "live" ? timeLeft(a.endsAt) : "Ended"}</strong></span></span>
  </button>`;
}
function tickCards(root){
  clearInterval(AUC.timer);
  AUC.timer = setInterval(() => { if(!root.isConnected){ clearInterval(AUC.timer); return; } root.querySelectorAll(".tl[data-end]").forEach(t => { t.textContent = timeLeft(+t.dataset.end); }); }, 1000);
}

/* ---------- one lot ---------- */
function viewLot(el){
  stopLotWatch();
  const api = auApi(); if(!api){ auNeedsAccounts(el, "Code Auction"); return; }
  const id = route.id; if(!id){ go({v: "auction"}); return; }
  el.innerHTML = `<nav class="crumbs"><a href="#/auction" data-act="auction">Code Auction</a><span>›</span><span>Lot</span></nav><div class="muted">Loading the lot…</div>`;
  let lot = null, bids = [], msgs = null, vaultFiles = null, busy = false, flash = "";
  const paint = () => {
    if(route.v !== "lot" || route.id !== id) return stopLotWatch();
    if(!lot){ el.innerHTML = `<nav class="crumbs"><a href="#/auction" data-act="auction">Code Auction</a></nav><section class="panel"><p style="margin:0">This lot doesn't exist, or it was removed.</p></section>`; return; }
    const u = auUser(), st = lotState(lot), isSeller = u?.uid === lot.sellerUid, isTop = !!u && lot.bidCount > 0 && u.uid === lot.topUid;
    const party = isSeller || (isTop && st !== "live");
    el.innerHTML = `<nav class="crumbs"><a href="#/auction" data-act="auction">Code Auction</a><span>›</span><span>${esc(lot.title)}</span></nav>
    <div class="lotpage">
      <section class="panel" style="gap:18px">
        <span class="eyebrow">${esc(AUC_LANG[lot.lang] || lot.lang)} project · listed ${new Date(lot.created).toLocaleDateString()}</span>
        <h1 class="h2">${esc(lot.title)}</h1>
        <span class="muted">Sold by <b style="color:var(--ink)">${esc(lot.sellerName)}</b></span>
        ${lot.desc ? `<div class="audesc">${esc(lot.desc)}</div>` : `<p class="muted" style="margin:0">The seller didn't add a description.</p>`}
        <div><span class="eyebrow">What you get</span>
          <ul class="aufiles">${(lot.files || []).map(f => `<li><span>${icon("code", "sm")}${esc(f.n)}</span><span class="muted">${fmtBytes(f.b)}</span></li>`).join("")}</ul>
          <p class="muted" style="margin:6px 0 0;font-size:.88rem">The winner gets a copy of these files in their own CodeBay projects once the seller releases them. The seller keeps their copy.</p></div>
      </section>
      <aside class="panel aubox" style="gap:14px">
        ${priceBlock(lot, st)}
        ${flash ? `<div class="aumsg" role="status">${flash}</div>` : ""}
        ${actionBlock(lot, st, u, isSeller, isTop)}
        <div><span class="eyebrow">Bid history</span>${bids.length ? `<ol class="aubids">${bids.map(b => `<li><b>${money(b.amount)}</b><span>${esc(b.name)}</span><span class="muted">${b.at ? new Date(b.at).toLocaleString([], {month: "short", day: "numeric", hour: "numeric", minute: "2-digit"}) : ""}</span></li>`).join("")}</ol>` : `<p class="muted" style="margin:6px 0 0">No bids yet.</p>`}</div>
      </aside>
    </div>
    ${party && st === "sold" ? dealBlock(lot, isSeller, isTop) : ""}`;
    wire(u, st, isSeller, isTop);
  };
  const fmtBytes = b => b >= 1024 ? `${(b / 1024).toFixed(1)} KB` : `${b} B`;
  function priceBlock(a, st){
    const cur = a.bidCount ? a.topBid : a.startBid;
    const label = st === "live" ? (a.bidCount ? "Current bid" : "Starting bid") : st === "sold" ? "Sold for" : st === "cancelled" ? "Withdrawn by the seller" : "Ended with no bids";
    return `<div class="auprice"><small>${label}</small><strong>${st === "cancelled" || st === "unsold" ? money(a.startBid) : money(cur)}</strong>
      <span class="muted">${a.bidCount} bid${a.bidCount === 1 ? "" : "s"}${a.bidCount ? ` · top bidder ${esc(a.topName)}` : ""}</span></div>
      <div class="auclock"><small>${st === "live" ? "Time left" : "Ended"}</small><strong id="auLeft">${st === "live" ? timeLeft(a.endsAt) : new Date(a.endsAt).toLocaleString([], {dateStyle: "medium", timeStyle: "short"})}</strong>
      ${st === "live" ? `<span class="muted">Ends ${new Date(a.endsAt).toLocaleString([], {dateStyle: "medium", timeStyle: "short"})}</span>` : ""}</div>`;
  }
  function actionBlock(a, st, u, isSeller, isTop){
    if(st === "cancelled" || st === "unsold") return "";
    if(st === "sold") return isSeller ? `<p class="muted" style="margin:0">Your lot sold. Use the deal thread below to agree payment with ${esc(a.topName)}, then release the files.</p>`
      : isTop ? `<p style="margin:0"><b>You won this lot.</b> Use the deal thread below to pay the seller. They release the files once you've paid.</p>` : `<p class="muted" style="margin:0">This auction has ended.</p>`;
    if(!u) return `<button class="gbtn" data-signin>${GOOGLE_G}<span>Sign in with Google to bid</span></button>`;
    if(isSeller) return `<p class="muted" style="margin:0">This is your lot. You can't bid on it.</p>${a.bidCount ? "" : `<button class="btn ghost sm" id="auCancel">Withdraw this lot</button><span class="muted" style="font-size:.84rem">You can withdraw only until the first bid.</span>`}`;
    const min = nextBid(a);
    if(isTop) return `<p class="aumsg ok" style="margin:0">${icon("check", "sm")} You're the top bidder. If someone outbids you, you can bid again here.</p>`;
    return `<form id="auBid" class="aubid">
        ${tradeName() ? "" : `<label class="fl"><span>Your public name</span><input class="field" id="auName" maxlength="40" required value="${esc(suggestName())}" placeholder="Shown next to your bids"></label>`}
        <label class="fl"><span>Your bid (US dollars)</span><span class="aumoney"><span>$</span><input class="field" id="auAmt" inputmode="decimal" required value="${(min / 100).toFixed(2)}" aria-describedby="auMin"></span></label>
        <span class="muted" id="auMin" style="font-size:.84rem">Enter ${money(min)} or more.${a.bidCount ? " Each bid must beat the last by at least $1." : ""}</span>
        <label class="chk"><input type="checkbox" id="auOk" required><span>If I win, I'll pay this amount to the seller.</span></label>
        <button class="btn primary" ${busy ? "disabled" : ""}>${busy ? "Placing bid…" : "Place bid"}</button>
      </form>
      <p class="muted" style="margin:0;font-size:.84rem">${esc(auIntro)}</p>`;
  }
  function dealBlock(a, isSeller, isTop){
    const released = a.released;
    return `<section class="panel deal" style="gap:14px"><div class="row" style="justify-content:space-between"><h2 class="h3">Deal thread</h2><span class="pill">${released ? "Files released" : "Waiting for payment"}</span></div>
      <p class="muted" style="margin:0">Only you and ${esc(isSeller ? a.topName : a.sellerName)} can see this. Agree on how to pay here. CodeBay doesn't process payments, so never share passwords or card numbers.</p>
      <div class="aumsgs">${msgs == null ? `<span class="muted">Loading messages…</span>` : msgs.length ? msgs.map(m => `<div class="m ${m.uid === auUser()?.uid ? "me" : ""}"><b>${esc(m.name)}</b><span>${esc(m.text)}</span><small class="muted">${m.at ? new Date(m.at).toLocaleString([], {month: "short", day: "numeric", hour: "numeric", minute: "2-digit"}) : ""}</small></div>`).join("") : `<span class="muted">No messages yet. Say hello and agree how payment will work.</span>`}</div>
      <form id="auSend" class="row" style="align-items:stretch"><textarea class="field" id="auText" rows="2" maxlength="2000" required placeholder="Write a message" style="flex:1;min-width:0"></textarea><button class="btn">Send</button></form>
      ${isSeller && !released ? `<div class="row"><button class="btn primary" id="auRelease">${icon("key", "sm")}I've been paid: release the files</button><span class="muted" style="font-size:.84rem">This can't be undone.</span></div>` : ""}
      ${isTop && released ? `<div class="row"><button class="btn primary" id="auCopy">${icon("download", "sm")}Copy the files to my projects</button></div>` : ""}
      ${isTop && !released ? `<p class="muted" style="margin:0">The seller releases the files once they've been paid. You'll then be able to copy them into your projects from this page.</p>` : ""}
    </section>`;
  }
  function wire(u, st, isSeller, isTop){
    el.querySelector("[data-signin]")?.addEventListener("click", () => Account.signIn());
    el.querySelector("#auCancel")?.addEventListener("click", async () => {
      if(!confirm(`Withdraw "${lot.title}"? It stays visible as withdrawn and can't be reopened.`)) return;
      try{ await api.edit(id, {status: "cancelled"}); }catch(e){ flash = "Couldn't withdraw it. Someone may have just bid."; paint(); }
    });
    el.querySelector("#auBid")?.addEventListener("submit", async e => {
      e.preventDefault(); if(busy) return;
      const nameIn = el.querySelector("#auName");
      if(nameIn){ const n = nameIn.value.trim(); if(n.length < 2){ flash = "Pick a public name of at least 2 characters."; paint(); return; } setTradeName(n); }
      const amt = centsOf(el.querySelector("#auAmt").value), min = nextBid(lot);
      if(!(amt >= min)){ flash = `Your bid needs to be ${money(min)} or more.`; paint(); return; }
      if(amt > AUC.MAX){ flash = `Bids are capped at ${money(AUC.MAX)}.`; paint(); return; }
      if(amt >= min * 5 && amt >= 50000 && !confirm(`You're bidding ${money(amt)}, much more than the ${money(min)} needed. Continue?`)) return;
      busy = true; flash = ""; paint();
      try{ await api.bid({uid: u.uid, name: tradeName()}, id, amt); rememberBid(id); flash = `Bid placed: ${money(amt)}.`; bids = await api.bids(id).catch(() => bids); }
      catch(err){ console.warn("bid", err); flash = "That bid didn't go through. Someone may have bid first, or the auction just ended. The price above is up to date."; lot = await api.get(id).catch(() => lot); }
      busy = false; paint();
    });
    el.querySelector("#auSend")?.addEventListener("submit", async e => {
      e.preventDefault(); const t = el.querySelector("#auText").value.trim(); if(!t) return;
      try{ await api.send({uid: u.uid, name: isSeller ? lot.sellerName : lot.topName}, id, t); msgs = await api.messages(id); }
      catch(err){ flash = "Couldn't send that message. Try again."; }
      paint();
    });
    el.querySelector("#auRelease")?.addEventListener("click", async () => {
      if(!confirm(`Release the files to ${lot.topName}? Do this only once you've been paid. It can't be undone.`)) return;
      try{ await api.release(id); }catch(e){ flash = "Couldn't release the files. Try again."; paint(); }
    });
    el.querySelector("#auCopy")?.addEventListener("click", async () => {
      try{
        vaultFiles = vaultFiles || await api.vault(id);
        if(!vaultFiles || !Object.keys(vaultFiles).length) throw new Error("empty");
        const open = vaultFiles["main.py"] != null ? "main.py" : vaultFiles["main.js"] != null ? "main.js" : vaultFiles["index.html"] != null ? "index.html" : Object.keys(vaultFiles)[0];
        const ws = WS.create(lot.title.slice(0, 60), lot.lang, vaultFiles, open);
        UI.toast("Copied to your projects", `"${lot.title}" is now in your editor.`, "download", 3200);
        go({v: "code", id: ws.id});
      }catch(e){ console.warn("vault", e); flash = "Couldn't fetch the files. If the seller just released them, try again in a moment."; paint(); }
    });
    clearInterval(AUC.timer);
    if(st === "live") AUC.timer = setInterval(() => {
      const t = el.querySelector("#auLeft"); if(!t || route.v !== "lot" || route.id !== id){ clearInterval(AUC.timer); return; }
      if(Date.now() >= lot.endsAt){ clearInterval(AUC.timer); paint(); loadParty(); return; }
      t.textContent = timeLeft(lot.endsAt);
    }, 1000);
  }
  async function loadParty(){
    const u = auUser(); if(!lot || !u || lotState(lot) !== "sold") return;
    if(u.uid !== lot.sellerUid && u.uid !== lot.topUid) return;
    try{ msgs = await api.messages(id); }catch(e){ msgs = []; }
    paint();
  }
  (async () => {
    try{
      [lot, bids] = await Promise.all([api.get(id), api.bids(id).catch(() => [])]);
      paint(); loadParty();
      AUC.watch = await api.watch(id, async a => {
        if(route.v !== "lot" || route.id !== id) return stopLotWatch();
        const changed = !lot || !a || a.bidCount !== lot.bidCount || a.released !== lot.released || a.status !== lot.status;
        lot = a; if(changed && a){ bids = await api.bids(id).catch(() => bids); }
        if(!busy) paint();
      });
    }catch(e){ console.warn("lot", e); el.innerHTML = `<nav class="crumbs"><a href="#/auction" data-act="auction">Code Auction</a></nav><section class="panel"><p class="err" style="margin:0">Couldn't load this lot. Check your connection and try again.</p></section>`; }
  })();
}

/* ---------- list a project ---------- */
function viewSell(el){
  stopLotWatch();
  const api = auApi(); if(!api){ auNeedsAccounts(el, "List a project"); return; }
  const u = auUser();
  const head = `<nav class="crumbs"><a href="#/auction" data-act="auction">Code Auction</a><span>›</span><span>List a project</span></nav>
    <section class="head"><span class="eyebrow">Code Auction</span><h1 class="h1">List a project</h1>
    <p class="lede">Pick one of your cloud projects from the editor, set a starting price and an end time. When the auction ends, you and the winner agree payment in a private thread, and you release the files once you've been paid.</p></section>`;
  if(!u){ el.innerHTML = head + `<section class="panel"><p style="margin:0">Sign in first. Listings are tied to your CodeBay account, and the project has to be saved to it.</p><div class="row"><button class="gbtn" data-signin>${GOOGLE_G}<span>Sign in with Google</span></button></div></section>`;
    el.querySelector("[data-signin]").onclick = () => Account.signIn(); return; }
  const list = WS.list();
  if(!WS.cloud || !list.length){ el.innerHTML = head + `<section class="panel"><p style="margin:0">${WS.cloud ? "You don't have any projects yet. Build one in the editor, then come back to list it." : "Your projects are still syncing to your account. Give it a moment, then reload this page."}</p><div class="row"><button class="btn primary" data-act="editor">${icon("terminal", "sm")}Open the editor</button></div></section>`; return; }
  el.innerHTML = head + `<form class="panel sellform" id="sellForm" style="gap:18px">
      <fieldset class="fl"><legend>Project</legend><div class="wspick">${list.map((w, i) => `<label class="wsopt"><input type="radio" name="ws" value="${esc(w.id)}" ${i === 0 ? "checked" : ""}><span><b>${esc(w.name)}</b><small class="muted">${esc(AUC_LANG[w.lang] || w.lang)} · ${w.files} file${w.files === 1 ? "" : "s"} · edited ${ago(w.updated)}</small></span></label>`).join("")}</div></fieldset>
      <label class="fl"><span>Title</span><input class="field" id="slTitle" maxlength="80" minlength="3" required></label>
      <label class="fl"><span>Description</span><textarea class="field" id="slDesc" rows="6" maxlength="3000" placeholder="What does it do? What's it built with? What state is it in? Buyers only see the file names until they win."></textarea></label>
      <div class="grid2" style="gap:14px">
        <label class="fl"><span>Starting price (US dollars)</span><span class="aumoney"><span>$</span><input class="field" id="slStart" inputmode="decimal" required value="5.00"></span></label>
        <label class="fl"><span>Auction length</span><select class="field" id="slDur">${AUC.DURATIONS.map(([d, t]) => `<option value="${d}" ${d === 7 ? "selected" : ""}>${t}</option>`).join("")}</select></label>
      </div>
      <label class="fl"><span>Your public name</span><input class="field" id="slName" maxlength="40" required value="${esc(suggestName())}" placeholder="Shown on your listings and bids"></label>
      <div class="fl"><span>Included files</span><ul class="aufiles" id="slFiles"></ul></div>
      <label class="chk"><input type="checkbox" id="slOwn" required><span>I wrote this code, or I have the right to sell it, and it contains no passwords, keys or anyone's personal data.</span></label>
      <label class="chk"><input type="checkbox" id="slDeal" required><span>If it sells, I'll agree payment with the winner and release the files once paid. CodeBay doesn't handle the money.</span></label>
      <p class="err" id="slErr" role="alert" hidden></p>
      <div class="row"><button class="btn primary lg" id="slGo">${icon("upload")}List it for auction</button><button type="button" class="btn ghost lg" data-act="auction">Cancel</button></div>
    </form>`;
  const f = el.querySelector("#sellForm"), err = el.querySelector("#slErr");
  const pick = () => WS.get(f.querySelector("input[name=ws]:checked")?.value);
  const showFiles = () => { const ws = pick(); if(!ws) return;
    if(!f.dataset.touched) el.querySelector("#slTitle").value = ws.name.slice(0, 80);
    el.querySelector("#slFiles").innerHTML = Object.entries(ws.files).map(([n, t]) => `<li><span>${icon("code", "sm")}${esc(n)}</span><span class="muted">${new Blob([t]).size} B</span></li>`).join(""); };
  f.querySelectorAll("input[name=ws]").forEach(r => r.onchange = showFiles);
  el.querySelector("#slTitle").oninput = () => { f.dataset.touched = "1"; };
  showFiles();
  f.onsubmit = async e => {
    e.preventDefault(); err.hidden = true;
    const ws = pick(), title = el.querySelector("#slTitle").value.trim(), desc = el.querySelector("#slDesc").value.trim(), name = el.querySelector("#slName").value.trim();
    const start = centsOf(el.querySelector("#slStart").value), days = +el.querySelector("#slDur").value;
    const fail = m => { err.textContent = m; err.hidden = false; };
    if(!ws) return fail("Pick a project.");
    if(title.length < 3) return fail("Give it a title of at least 3 characters.");
    if(name.length < 2) return fail("Pick a public name of at least 2 characters.");
    if(!(start >= 100) || start > AUC.MAX) return fail(`The starting price has to be between $1.00 and ${money(AUC.MAX)}.`);
    const files = ws.files, meta = Object.entries(files).map(([n, t]) => ({n, b: new Blob([t]).size}));
    if(!meta.length) return fail("That project has no files.");
    if(JSON.stringify(files).length > 850000) return fail("That project is too large to list. Keep it under about 800 KB.");
    setTradeName(name);
    const btn = el.querySelector("#slGo"); btn.disabled = true; btn.textContent = "Listing…";
    try{
      const lotId = await api.create({uid: u.uid, name: tradeName()}, {title, desc, lang: ws.lang, files: meta, startBid: start, endsAt: Date.now() + days * 86400000}, files);
      UI.toast("Your project is listed", `"${title}" is up for auction for ${AUC.DURATIONS.find(x => x[0] === days)[1]}.`, "upload", 3200);
      go({v: "lot", id: lotId});
    }catch(ex){ console.warn("list", ex); btn.disabled = false; btn.innerHTML = `${icon("upload")}List it for auction`; fail("Couldn't list it. Check your connection and try again."); }
  };
}

VIEWS.auction = viewAuction; VIEWS.lot = viewLot; VIEWS.sell = viewSell;
