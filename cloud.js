"use strict";
/* ---------- accounts: "Sign in with Google" and cloud sync through Firebase ----------
   Configure the Firebase project in firebase-config.js. Each person's data lives in Firestore under users/{uid}/docs/{docId},
   and firestore.rules lets a signed-in person read and write only their own documents. Documents are stored as one JSON
   string ({json, updated}) so any shape of progress data is accepted. A page can also supply window.CL_CLOUD_PROVIDER
   (same interface as firebaseProvider below), which is how the tests run the whole flow without a real project.
   Leaderboard entries (rewards.js) live in boards/{all | w-YYYY-MM-DD}/entries/{uid}, only for people who opt in. */
const FIREBASE_SDK = "https://www.gstatic.com/firebasejs/10.12.2/";

function firebaseProvider(cfg){
  let sdk = null;
  const load = async () => sdk || (sdk = await Promise.all([import(FIREBASE_SDK + "firebase-app.js"), import(FIREBASE_SDK + "firebase-auth.js"), import(FIREBASE_SDK + "firebase-firestore.js")])
    .then(([app, auth, fs]) => { const a = app.initializeApp(cfg); return {auth, fs, au: auth.getAuth(a), db: fs.getFirestore(a)}; }));
  const toUser = u => u ? {uid: u.uid, name: u.displayName || u.email || "You", email: u.email || "", photo: u.photoURL || ""} : null;
  return {
    async init(onUser){ const {auth, au} = await load(); auth.onAuthStateChanged(au, u => onUser(toUser(u))); },
    async signIn(){
      const {auth, au} = await load(); const gp = new auth.GoogleAuthProvider(); gp.setCustomParameters({prompt: "select_account"});
      try{ await auth.signInWithPopup(au, gp); }
      catch(e){ if(["auth/popup-blocked", "auth/operation-not-supported-in-this-environment"].includes(e.code)) await auth.signInWithRedirect(au, gp); else throw e; }
    },
    async signOut(){ const {auth, au} = await load(); await auth.signOut(au); },
    collection(uid){
      return {doc: id => ({
        async get(){ const {fs, db} = await load(); const snap = await fs.getDoc(fs.doc(db, "users", uid, "docs", id)); const d = snap.exists() ? snap.data() : null;
          return {exists: !!d, data: () => d ? (typeof d.json === "string" ? JSON.parse(d.json) : d) : null}; },
        async set(obj){ const {fs, db} = await load(); await fs.setDoc(fs.doc(db, "users", uid, "docs", id), {json: JSON.stringify(obj), updated: fs.serverTimestamp()}); }
      })};
    },
    // leaderboards: boards/{name}/entries/{uid}, readable by any signed-in person, writable only by the owner (firestore.rules)
    board(name){
      const ref = (fs, db, uid) => fs.doc(db, "boards", name, "entries", uid);
      return {
        async put(uid, data){ const {fs, db} = await load(); await fs.setDoc(ref(fs, db, uid), {...data, updated: fs.serverTimestamp()}); },
        async remove(uid){ const {fs, db} = await load(); await fs.deleteDoc(ref(fs, db, uid)); },
        async top(field, n){ const {fs, db} = await load();
          const snap = await fs.getDocs(fs.query(fs.collection(db, "boards", name, "entries"), fs.orderBy(field, "desc"), fs.limit(n)));
          return snap.docs.map(d => ({uid: d.id, ...d.data()})); }
      };
    }
  };
}

const GOOGLE_G = `<svg class="gg" viewBox="0 0 48 48" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>`;

const Account = (() => {
  let provider = null, user = null, busy = false, error = "";
  const btn = () => document.getElementById("acctBtn"), menu = () => document.getElementById("acctMenu");
  function paint(){
    const b = btn(); if(!b) return;
    b.hidden = !provider;
    if(user){ b.innerHTML = user.photo ? `<img src="${esc(user.photo)}" alt="" referrerpolicy="no-referrer">` : `<span class="ini">${esc((user.name || "?").trim()[0] || "?").toUpperCase()}</span>`;
      b.setAttribute("aria-label", `Account: ${user.name}`); b.classList.add("in"); }
    else { b.innerHTML = `${GOOGLE_G}<span>Sign in</span>`; b.setAttribute("aria-label", "Sign in with Google"); b.classList.remove("in"); }
    const m = menu(); if(m && !m.hidden) fillMenu();
    if(route.v === "profile" || route.v === "editor") render();
  }
  function fillMenu(){
    const m = menu(); if(!m) return;
    m.innerHTML = user ? `<div class="who"><b>${esc(user.name)}</b><span>${esc(user.email)}</span></div>
      <p class="muted" style="margin:0;font-size:.84rem">Your progress, practice hours and editor projects are saved to this Google account.</p>
      <button type="button" class="btn sm" data-act="profile">${icon("user","sm")}Profile</button>
      <button type="button" class="btn ghost sm" id="acctOut">Sign out</button>`
      : signInBlock();
    m.querySelector("#acctOut")?.addEventListener("click", signOut);
    m.querySelector("[data-signin]")?.addEventListener("click", signIn);
  }
  function signInBlock(){
    return `<div style="display:grid;gap:10px"><b>Save your work to the cloud</b>
      <p class="muted" style="margin:0;font-size:.88rem">Sign in to keep your progress, practice hours and code in your account and pick up on any device. Anything you've done in this browser comes with you.</p>
      <button type="button" class="gbtn" data-signin>${GOOGLE_G}<span>${busy ? "Opening Google…" : "Sign in with Google"}</span></button>
      ${error ? `<p class="err" role="alert" style="margin:0;font-size:.86rem">${esc(error)}</p>` : ""}</div>`;
  }
  async function signIn(){
    if(!provider || busy) return; busy = true; error = ""; fillMenu();
    try{ await provider.signIn(); }
    catch(e){ console.warn("Sign-in failed:", e?.code || e); error = e?.code === "auth/popup-closed-by-user" || e?.code === "auth/cancelled-popup-request" ? "" : e?.code === "auth/unauthorized-domain" ? "Sign-in isn't enabled for this web address yet." : "Sign-in didn't finish. Please try again."; }
    busy = false; fillMenu();
  }
  async function signOut(){
    if(!provider) return;
    if(!confirm("Sign out? Your work stays safe in your account, and this browser's copy is cleared so the next person starts fresh.")) return;
    try{ Clock.flush(); await new Promise(r => setTimeout(r, 900)); await provider.signOut(); }catch(e){}
  }
  async function onUser(u){
    const was = user; user = u;
    if(u && (!was || was.uid !== u.uid)){
      paint();
      try{ await attachStores(provider.collection(u.uid)); }
      catch(e){ detachStores(); setSync("Couldn't reach your account · saved in this browser"); }
      UI.toast(`Signed in as ${u.name}`, "Your work now saves to your account.", "user", 3200);
    } else if(!u && was){
      try{ Object.keys(localStorage).filter(k => k.startsWith("tenk2-") || k.startsWith("cl-ws")).forEach(k => localStorage.removeItem(k)); }catch(e){}
      detachStores();
      P = P0(); S = {cards:{}}; Game.ready = false;
      setSync("Signed out · saved in this browser");
      Game.sync(true); go({v: "home"});
    } else if(!u) setSync("Saved in this browser");
    paint();
  }
  function mountButton(){
    const r = document.querySelector(".top-r"); if(!r || document.getElementById("acctBtn")) return;
    const w = document.createElement("div"); w.className = "acct";
    w.innerHTML = `<button type="button" class="acctbtn" id="acctBtn" aria-haspopup="true" aria-expanded="false" hidden></button><div class="acctmenu" id="acctMenu" hidden></div>`;
    r.insertBefore(w, document.getElementById("themeBtn"));
    const b = w.querySelector("#acctBtn"), m = w.querySelector("#acctMenu");
    b.onclick = e => { e.stopPropagation(); m.hidden = !m.hidden; b.setAttribute("aria-expanded", !m.hidden); if(!m.hidden) fillMenu(); };
    m.addEventListener("click", e => { if(e.target.closest("[data-act]")) m.hidden = true; });
    document.addEventListener("click", e => { if(!m.hidden && !w.contains(e.target)){ m.hidden = true; b.setAttribute("aria-expanded", "false"); } });
  }
  return {
    async start(){
      const cfg = window.CL_FIREBASE;
      provider = window.CL_CLOUD_PROVIDER || (cfg && cfg.apiKey && cfg.projectId ? firebaseProvider(cfg) : null);
      mountButton(); paint();
      if(!provider){ setSync("Saved in this browser"); return; }
      setSync("Checking your account…");
      try{ await provider.init(onUser); }
      catch(e){ provider = null; paint(); setSync("Saved in this browser"); }
    },
    get user(){ return user; }, get enabled(){ return !!provider; },
    board(name){ return provider?.board && user ? provider.board(name) : null; },
    signIn, signOut,
    panel(){   // for the profile page
      if(!provider) return "";
      return user ? `<section class="panel"><h2 class="h3">Your account</h2><div class="row" style="gap:12px">${user.photo ? `<img class="avatar" src="${esc(user.photo)}" alt="" referrerpolicy="no-referrer">` : ""}<div style="display:grid"><b>${esc(user.name)}</b><span class="muted" style="font-size:.88rem">${esc(user.email)}</span></div></div>
        <p class="muted" style="margin:0">Progress, practice hours, review cards and editor projects sync to this account automatically.</p><div class="row"><button class="btn ghost sm" id="pfOut">Sign out</button></div></section>`
        : `<section class="panel">${signInBlock()}</section>`;
    },
    wire(el){ el.querySelector("#pfOut")?.addEventListener("click", signOut); el.querySelector(".panel [data-signin]")?.addEventListener("click", async () => { await signIn(); }); }
  };
})();
