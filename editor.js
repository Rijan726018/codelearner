"use strict";
/* ---------- the Editor: your own multi-file projects, saved in the browser and (when signed in) to your account ----------
   A workspace is {id, name, lang, files:{name: text}, open, stdin, created, updated}. Locally: cl-ws-index and cl-ws-<id>.
   In the account: doc "ws-index" ({list:[{id, name, lang, updated, deleted?}]}) and one doc per workspace, "ws-<id>". */
const WS_LANGS = {
  python:{t:"Python", i:"code", ext:["py","txt","md","csv","json"], files:{"main.py":`# Your Python project. Press Run (Ctrl+Enter) to try it.\nfrom helpers import greet\n\nname = "world"\nprint(greet(name))\n`, "helpers.py":`def greet(name):\n    """Other files are modules: import them from main.py."""\n    return f"Hello, {name}!"\n`}, open:"main.py"},
  js:{t:"JavaScript", i:"braces", ext:["js","txt","md","json"], files:{"main.js":`// Your JavaScript project. Press Run (Ctrl+Enter) to try it.\nconst nums = [3, 1, 4, 1, 5, 9, 2, 6];\nconsole.log("sorted:", [...nums].sort((a, b) => a - b));\nconsole.log("total:", nums.reduce((a, b) => a + b, 0));\n`}, open:"main.js"},
  web:{t:"Web page (HTML, CSS & JS)", i:"globe", ext:["html","css","js","txt","md","json"], files:{
    "index.html":`<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="utf-8">\n  <title>My page</title>\n  <link rel="stylesheet" href="style.css">\n</head>\n<body>\n  <main>\n    <h1>Hello, web</h1>\n    <button id="btn">Click me</button>\n    <p id="out"></p>\n  </main>\n  <script src="script.js"></script>\n</body>\n</html>\n`,
    "style.css":`body {\n  font-family: system-ui, sans-serif;\n  margin: 0;\n  padding: 40px 16px;\n  background: #f5f3ff;\n}\n\nmain {\n  max-width: 560px;\n  margin: 0 auto;\n}\n`,
    "script.js":`let clicks = 0;\ndocument.querySelector("#btn").addEventListener("click", () => {\n  clicks += 1;\n  document.querySelector("#out").textContent = \`Clicked \${clicks} times\`;\n  console.log("click", clicks);\n});\n`}, open:"index.html"},
  sql:{t:"SQL (SQLite)", i:"db", ext:["sql","txt","md","csv"], files:{"query.sql":`-- Each run starts with an empty in-memory database: create, fill, then query.\nCREATE TABLE notes (id INTEGER PRIMARY KEY, title TEXT, words INTEGER);\nINSERT INTO notes (title, words) VALUES ('Ideas', 120), ('Todo', 45), ('Journal', 800);\n\nSELECT title, words FROM notes ORDER BY words DESC;\n`}, open:"query.sql"}
};
const WS_LIMIT = {files:30, bytes:400000};
const extOf = n => (n.match(/\.([a-z0-9]+)$/i)||[])[1]?.toLowerCase() || "";
const FILE_MODE = {py:"python", js:"javascript", json:"javascript", css:"css", html:"htmlmixed", sql:"text/x-sqlite"};
const ago = iso => { const s = Math.max(0, (Date.now() - Date.parse(iso))/1000); return s < 50 ? "just now" : s < 3600 ? `${Math.round(s/60)} min ago` : s < 86400 ? `${Math.round(s/3600)} h ago` : s < 86400*30 ? `${Math.round(s/86400)} days ago` : new Date(iso).toLocaleDateString(); };

const WS = (() => {
  let index = [], cache = {}, col = null, status = "local";
  const timers = {}, subs = new Set();
  const note = () => subs.forEach(f => { try{ f(status); }catch(e){} });
  const lget = k => { try{ return JSON.parse(localStorage.getItem(k) || "null"); }catch(e){ return null; } };
  const lset = (k, v) => { try{ localStorage.setItem(k, JSON.stringify(v)); return true; }catch(e){ return false; } };
  function loadLocal(){ index = lget("cl-ws-index") || []; cache = {}; }
  loadLocal();
  const live = () => index.filter(x => !x.deleted).sort((a, b) => b.updated.localeCompare(a.updated));
  const get = id => cache[id] || (cache[id] = lget("cl-ws-" + id));
  const entry = ws => ({id: ws.id, name: ws.name, lang: ws.lang, updated: ws.updated, files: Object.keys(ws.files).length});
  function putIndex(e){ index = index.filter(x => x.id !== e.id).concat([e]); lset("cl-ws-index", index); }
  function pushCloud(ws){
    if(!col) return;
    status = "saving"; note(); clearTimeout(timers[ws.id]);
    timers[ws.id] = setTimeout(async () => {
      try{
        if(ws.deleted) await col.doc("ws-" + ws.id).set({deleted: true, updated: ws.updated});
        else await col.doc("ws-" + ws.id).set(ws);
        await col.doc("ws-index").set({list: index});
        status = "cloud";
      }catch(e){ status = "error"; }
      note();
    }, 1500);
  }
  function save(ws){
    ws.updated = new Date().toISOString(); cache[ws.id] = ws;
    const ok = lset("cl-ws-" + ws.id, ws); putIndex(entry(ws));
    if(!col){ status = ok ? "local" : "full"; note(); }
    pushCloud(ws);
  }
  function create(name, lang, files, open){
    const L = WS_LANGS[lang] || WS_LANGS.python, now = new Date().toISOString();
    const ws = {id: Date.now().toString(36) + Math.random().toString(36).slice(2, 7), name: name || "Untitled project", lang, files: {...(files || L.files)}, open: open || Object.keys(files || L.files)[0] || L.open, stdin: "", created: now, updated: now};
    if(!files) ws.open = L.open;
    save(ws); return ws;
  }
  function remove(id){
    const e = index.find(x => x.id === id); if(!e) return;
    const t = {id, name: e.name, lang: e.lang, updated: new Date().toISOString(), deleted: true, files: 0};
    try{ localStorage.removeItem("cl-ws-" + id); }catch(err){}
    delete cache[id]; putIndex(t); pushCloud({id, deleted: true, updated: t.updated});
  }
  // Signing in merges this browser's projects with the account's, newest copy of each winning.
  async function attach(c){
    col = c;
    if(!c){ loadLocal(); status = "local"; note(); return; }
    status = "saving"; note();
    const snap = await c.doc("ws-index").get();
    const remote = (snap.exists && snap.data()?.list) || [];
    const byId = {}; [...remote.map(x => ({...x, _r: true})), ...index].forEach(x => { const o = byId[x.id]; if(!o || x.updated > o.updated) byId[x.id] = x; });
    const merged = Object.values(byId);
    for(const e of merged){
      const r = remote.find(x => x.id === e.id), l = index.find(x => x.id === e.id);
      if(e._r && !e.deleted && (!l || l.updated < e.updated)){ const d = await c.doc("ws-" + e.id).get(); if(d.exists && !d.data().deleted){ cache[e.id] = d.data(); lset("cl-ws-" + e.id, d.data()); } }
      else if(!e._r && (!r || r.updated < e.updated)){ if(e.deleted) await c.doc("ws-" + e.id).set({deleted: true, updated: e.updated}); else { const ws = get(e.id); if(ws) await c.doc("ws-" + e.id).set(ws); } }
      if(e.deleted){ try{ localStorage.removeItem("cl-ws-" + e.id); }catch(err){} delete cache[e.id]; }
      delete e._r;
    }
    index = merged; lset("cl-ws-index", index);
    await c.doc("ws-index").set({list: index});
    status = "cloud"; note();
  }
  return {list: live, get, save, create, remove, attach, on(f){ subs.add(f); return () => subs.delete(f); }, get status(){ return status; }, get cloud(){ return !!col; }};
})();
ACCOUNT_HOOKS.push(c => WS.attach(c));

const wsStatusText = s => ({local: "Saved in this browser", saving: "Saving…", cloud: "Saved to your account", error: "Couldn't reach your account · saved in this browser", full: "This browser's storage is full: download your files"})[s] || "";

/* ---------- combine a web project's files into one page for the preview ---------- */
function buildWebPage(files){
  const html = files["index.html"] ?? Object.entries(files).find(([n]) => extOf(n) === "html")?.[1] ?? "<!DOCTYPE html><p>Add an index.html file.</p>";
  return html
    .replace(/<link\b[^>]*href=["']([^"']+\.css)["'][^>]*>/gi, (m, href) => files[href] != null ? `<style>\n${files[href]}\n</style>` : m)
    .replace(/<script\b([^>]*)\bsrc=["']([^"']+\.js)["']([^>]*)>\s*<\/script>/gi, (m, a, src, b) => files[src] != null ? `<script${a}${b}>\n${files[src].replace(/<\/script/gi, "<\\/script")}\n</script>` : m);
}

/* ---------- a plain code editor: CodeMirror when it loaded, a textarea otherwise ---------- */
function codeArea(host, {value, file, onChange, onRun, onSave}){
  const keys = e => { if((e.metaKey || e.ctrlKey) && e.key === "Enter"){ e.preventDefault(); onRun(); } if((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "s"){ e.preventDefault(); onSave(); } };
  if(window.CodeMirror){
    const ext = extOf(file), cm = CodeMirror(host, {value, mode: FILE_MODE[ext] || null, lineNumbers: true, indentUnit: ext === "py" ? 4 : 2, tabSize: 4, matchBrackets: true, lineWrapping: ext === "md" || ext === "txt",
      extraKeys: {"Cmd-Enter": onRun, "Ctrl-Enter": onRun, "Cmd-S": onSave, "Ctrl-S": onSave, Tab: c => c.somethingSelected() ? c.indentSelection("add") : c.replaceSelection(" ".repeat(c.getOption("indentUnit")), "end"), "Shift-Tab": c => c.indentSelection("subtract"), Esc: c => c.getInputField().blur()}});
    cm.getInputField().setAttribute("aria-label", `Editing ${file}. Press Escape, then Tab, to leave the editor.`);
    cm.on("change", () => onChange(cm.getValue()));
    return {get value(){ return cm.getValue(); }, focus: () => cm.focus(), refresh: () => cm.refresh()};
  }
  const ta = document.createElement("textarea"); ta.className = "edta wsta"; ta.value = value; ta.spellcheck = false; ta.setAttribute("aria-label", `Editing ${file}`);
  ta.addEventListener("keydown", e => { keys(e); if(e.key === "Tab" && !e.shiftKey && !e.ctrlKey && !e.metaKey){ e.preventDefault(); ta.setRangeText(" ".repeat(extOf(file) === "py" ? 4 : 2), ta.selectionStart, ta.selectionEnd, "end"); onChange(ta.value); } });
  ta.addEventListener("input", () => onChange(ta.value));
  host.appendChild(ta);
  return {get value(){ return ta.value; }, focus: () => ta.focus(), refresh(){}};
}

/* ---------- the projects list ---------- */
let wsNewLang = "python";
function viewEditor(el){
  const list = WS.list(), signedIn = WS.cloud;
  const fromOpts = PJ.list.map(p => `<option value="${p.id}">${esc(p.title)} (${esc(LANGNAME[p.lang] || p.lang)})</option>`).join("");
  el.innerHTML = `<section class="head"><span class="eyebrow">Your code, your projects</span><h1 class="h1">Editor</h1>
    <p class="lede">A code editor for your own projects, with several files per project. Python, JavaScript, SQL and web pages all run right here, and your work saves as you type. ${signedIn ? "Everything syncs to your account, so it's on every device you sign in on." : "It saves in this browser."}</p></section>
  ${!signedIn && typeof Account !== "undefined" && Account.enabled ? `<section class="panel signbar"><div><b>Keep your code in the cloud</b><p class="muted" style="margin:0;font-size:.9rem">Sign in with Google and your projects, progress and practice hours follow you to any device.</p></div><button type="button" class="gbtn" data-signin>${GOOGLE_G}<span>Sign in with Google</span></button></section>` : ""}
  <div class="grid2">
    <section class="panel"><h2 class="h3">New project</h2>
      <form id="wsnew" class="mform"><label class="wide">Name<input class="field" id="wsname" maxlength="60" placeholder="My first app" required></label>
        <div class="wide"><div class="seg" role="group" aria-label="Language">${Object.entries(WS_LANGS).map(([k, L]) => `<button type="button" data-wl="${k}" aria-pressed="${wsNewLang === k}">${esc(L.t.replace(/ \(.*/, ""))}</button>`).join("")}</div></div>
        <button class="btn primary">${icon("plus","sm")}Create project</button></form></section>
    <section class="panel"><h2 class="h3">Start from a Build & Learn project</h2>
      <p class="muted" style="margin:0;font-size:.9rem">Copy your code from a guided project into a project of your own, then take it further with the stretch goals.</p>
      <div class="mform"><label class="wide">Project<select class="field" id="wsfrom">${fromOpts}</select></label><button type="button" class="btn" id="wsfromgo">${icon("rocket","sm")}Open in the Editor</button></div></section>
  </div>
  <section style="display:grid;gap:12px"><div class="sec-h"><h2 class="h2">Your projects</h2><span class="pill ${WS.status === "cloud" ? "ok" : ""}" id="wsstat">${esc(wsStatusText(WS.status))}</span></div>
    ${list.length ? `<div class="wsgrid">${list.map(w => `<div class="wscard"><button type="button" class="wsopen" data-ws="${w.id}"><span class="row" style="gap:8px;color:var(--accent)">${icon(WS_LANGS[w.lang]?.i || "code")}<span class="eyebrow" style="color:inherit">${esc(WS_LANGS[w.lang]?.t || w.lang)}</span></span><b>${esc(w.name)}</b><span class="muted">${w.files} file${w.files === 1 ? "" : "s"} · edited ${ago(w.updated)}</span></button><button type="button" class="btn ghost sm" data-wsdel="${w.id}" aria-label="Delete ${esc(w.name)}">Delete</button></div>`).join("")}</div>`
      : `<div class="empty">No projects yet. Create one above, or start from a Build & Learn project.</div>`}</section>`;
  el.querySelectorAll("[data-wl]").forEach(b => b.onclick = () => { wsNewLang = b.dataset.wl; el.querySelectorAll("[data-wl]").forEach(x => x.setAttribute("aria-pressed", x === b)); });
  el.querySelector("#wsnew").onsubmit = e => { e.preventDefault(); const ws = WS.create(el.querySelector("#wsname").value.trim().slice(0, 60), wsNewLang); go({v: "code", id: ws.id}); };
  el.querySelector("#wsfromgo").onclick = () => wsFromProject(el.querySelector("#wsfrom").value);
  el.querySelector("[data-signin]")?.addEventListener("click", () => Account.signIn());
  el.querySelectorAll("[data-wsdel]").forEach(b => b.onclick = () => { const w = list.find(x => x.id === b.dataset.wsdel); if(w && confirm(`Delete "${w.name}" and all its files? This can't be undone.`)){ WS.remove(w.id); render(); } });
}

/* Copy a guided project's latest code (your saved draft of the step you're on, or its starter) into a new workspace. */
async function wsFromProject(pid){
  const p = PJ.byId[pid]; if(!p) return;
  const i = p.steps.findIndex(s => !P.steps?.[s.id]), s = p.steps[i < 0 ? p.steps.length - 1 : i];
  const draft = await Drafts.get(`bc-${s.id}`);
  const code = draft ?? (i < 0 ? s.solution : s.starter);
  const map = {python: ["python", "main.py"], js: ["js", "main.js"], sql: ["sql", "query.sql"], web: ["web", "index.html"], html: ["web", "index.html"]}[p.lang] || ["python", "main.py"];
  const ws = WS.create(p.title, map[0], {[map[1]]: code, "NOTES.md": `# ${p.title}\n\nStarted from the Build & Learn project, at step ${(i < 0 ? p.steps.length : i + 1)} of ${p.steps.length}.\n\n## Stretch goals\n\n${(p.stretch || []).map(x => "- " + x).join("\n")}\n`}, map[1]);
  UI.toast("Copied into the Editor", `${p.title} is now one of your projects.`, "terminal", 3000);
  go({v: "code", id: ws.id});
}

/* ---------- one workspace ---------- */
function viewCode(el){
  const ws = WS.get(route.id); if(!ws || ws.deleted){ go({v: "editor"}); return; }
  const L = WS_LANGS[ws.lang] || WS_LANGS.python;
  if(!ws.files[ws.open]) ws.open = Object.keys(ws.files)[0];
  const isWeb = ws.lang === "web", runLang = ws.lang === "web" ? null : ws.lang;
  el.innerHTML = `<nav class="crumbs"><button data-act="editor">Editor</button><span>›</span><span>${esc(ws.name)}</span></nav>
  <section class="wshead"><input class="wsname" id="wsrename" value="${esc(ws.name)}" size="${Math.min(40, Math.max(6, ws.name.length + 1))}" maxlength="60" aria-label="Project name"><span class="pill acc">${esc(L.t)}</span><span class="sp"></span><span class="pill ${WS.status === "cloud" ? "ok" : ""}" id="wsstat">${esc(wsStatusText(WS.status))}</span></section>
  <div class="wslayout">
    <aside class="panel wsfiles"><div class="row" style="justify-content:space-between"><span class="eyebrow">Files</span><button type="button" class="btn ghost sm" id="wsadd" aria-label="New file">${icon("plus","sm")}New</button></div>
      <form id="wsaddf" hidden class="wsaddf"><input class="field" id="wsfname" placeholder="name.${L.ext[0]}" maxlength="40" aria-label="New file name"><button class="btn sm primary">Add</button></form>
      <p id="wsferr" class="err" role="alert" hidden style="margin:0;font-size:.82rem"></p>
      <ul class="wsflist">${Object.keys(ws.files).sort((a, b) => (a === L.open ? -1 : b === L.open ? 1 : a.localeCompare(b))).map(f => `<li><button type="button" data-f="${esc(f)}" aria-current="${f === ws.open}">${icon(extOf(f) === "md" || extOf(f) === "txt" ? "book" : "code","sm")}<span>${esc(f)}</span></button></li>`).join("")}</ul>
      <div class="wsfact"><button type="button" class="btn ghost sm" id="wsren">Rename</button><button type="button" class="btn ghost sm" id="wsdelf">Delete</button><button type="button" class="btn ghost sm" id="wsdl">${icon("download","sm")}Download</button></div>
      ${isWeb ? `<button type="button" class="btn ghost sm" id="wsdlweb">${icon("download","sm")}Download as one page</button>` : ""}</aside>
    <section class="wsmain"><div class="ed"><div class="edbar"><span class="pill">${esc(ws.open)}</span><span class="edsp"></span>
        ${ws.lang === "python" ? `<button type="button" class="btn ghost sm" id="wsin" aria-expanded="${!!ws.stdin}">Input</button>` : ""}
        <button type="button" class="btn primary sm" id="wsrun" title="Run (Ctrl+Enter)">${isWeb ? "Refresh preview ▶" : runLang && ws.lang === "python" ? "Run main.py ▶" : "Run ▶"}</button></div>
      <div class="edwrap" id="wsed"></div>
      <div class="edin" id="wsinbox" ${ws.stdin ? "" : "hidden"}><label class="eyebrow" for="wsstdin">Input · one line per input() call</label><textarea id="wsstdin" rows="3" spellcheck="false">${esc(ws.stdin || "")}</textarea></div>
      <div class="edfoot"><span class="edstat">Ctrl+Enter runs · Ctrl+S saves now · changes save automatically</span></div></div>
      <div id="wsout">${isWeb ? "" : `<div class="edout"><div class="edouthead"><span class="eyebrow">Output</span><span class="edms" id="wsms"></span></div><pre class="edpre" id="wspre" aria-live="polite"><span class="muted">Press Run to see the output here.</span></pre></div>`}</div></section>
  </div>`;
  const stat = () => { const s = el.querySelector("#wsstat"); if(s){ s.textContent = wsStatusText(WS.status); s.classList.toggle("ok", WS.status === "cloud"); } };
  const unsub = WS.on(() => { if(!el.contains(el.querySelector("#wsstat"))){ unsub(); return; } stat(); });
  let saveT = null;
  const persist = (now) => { clearTimeout(saveT); if(now) WS.save(ws); else saveT = setTimeout(() => WS.save(ws), 700); };
  let preview = null, autoT = null;
  const refreshWeb = () => { if(!preview) preview = mountPreview(el.querySelector("#wsout"), "web", {}); preview.show(buildWebPage(ws.files)); };
  const runNow = async () => {
    if(isWeb){ refreshWeb(); return; }
    const pre = el.querySelector("#wspre"), ms = el.querySelector("#wsms"), btn = el.querySelector("#wsrun");
    if(Runner.busy){ Runner.stop(); return; }
    const entry = ws.lang === "python" && ws.files["main.py"] != null ? "main.py" : ws.open;
    const code = ws.files[entry], files = {};
    if(ws.lang === "python") Object.entries(ws.files).forEach(([n, t]) => { if(n !== entry && extOf(n) === "py") files[n] = t; });
    pre.textContent = ""; ms.textContent = ""; btn.textContent = "Stop ■"; let n = 0;
    const lines = (el.querySelector("#wsstdin")?.value || "").replace(/\r/g, "").split("\n"); if(lines.length && lines[lines.length - 1] === "") lines.pop();
    const res = await Runner.run(runLang, code, lines, (s, text) => { n += text.length; const sp = document.createElement("span"); if(s === "e") sp.className = "err"; sp.textContent = text; pre.appendChild(sp); }, {files});
    btn.textContent = ws.lang === "python" ? "Run main.py ▶" : "Run ▶";
    if(!n && !res.stopped){ const sp = document.createElement("span"); sp.className = "muted"; sp.textContent = ws.lang === "sql" ? "(no rows returned)" : "(no output: nothing was printed)"; pre.appendChild(sp); }
    ms.textContent = res.ms != null ? `${res.ms} ms` : "";
  };
  const ed = codeArea(el.querySelector("#wsed"), {value: ws.files[ws.open], file: ws.open, onRun: runNow, onSave: () => persist(true),
    onChange: v => { ws.files[ws.open] = v; persist(); if(isWeb){ clearTimeout(autoT); autoT = setTimeout(refreshWeb, 600); } }});
  if(isWeb) refreshWeb(); else if(ws.lang === "python" || ws.lang === "sql") Runner.warm(ws.lang);
  el.querySelector("#wsrun").onclick = runNow;
  el.querySelector("#wsin")?.addEventListener("click", e => { const box = el.querySelector("#wsinbox"); box.hidden = !box.hidden; e.currentTarget.setAttribute("aria-expanded", !box.hidden); });
  el.querySelector("#wsstdin")?.addEventListener("input", e => { ws.stdin = e.target.value; persist(); });
  el.querySelector("#wsrename").addEventListener("change", e => { const v = e.target.value.trim().slice(0, 60); if(v){ ws.name = v; persist(true); render(); } else e.target.value = ws.name; });
  el.querySelectorAll("[data-f]").forEach(b => b.onclick = () => { persist(true); ws.open = b.dataset.f; render(); });
  const err = msg => { const p = el.querySelector("#wsferr"); p.textContent = msg; p.hidden = !msg; };
  const validName = (name, except) => {
    if(!/^[A-Za-z0-9_][A-Za-z0-9_.-]{0,38}\.[a-z0-9]+$/i.test(name)) return "Use letters, numbers, _ - . and an extension, like utils." + L.ext[0];
    if(!L.ext.includes(extOf(name))) return `This project can hold .${L.ext.join(", .")} files.`;
    if(name !== except && ws.files[name] != null) return "There's already a file with that name.";
    return "";
  };
  el.querySelector("#wsadd").onclick = () => { const f = el.querySelector("#wsaddf"); f.hidden = !f.hidden; if(!f.hidden) el.querySelector("#wsfname").focus(); };
  el.querySelector("#wsaddf").onsubmit = e => {
    e.preventDefault(); const name = el.querySelector("#wsfname").value.trim();
    const bad = validName(name) || (Object.keys(ws.files).length >= WS_LIMIT.files ? `A project can have up to ${WS_LIMIT.files} files.` : ""); if(bad){ err(bad); return; }
    ws.files[name] = ""; ws.open = name; persist(true); render();
  };
  el.querySelector("#wsren").onclick = () => {
    const name = (prompt("Rename the file to:", ws.open) || "").trim(); if(!name || name === ws.open) return;
    const bad = validName(name, ws.open); if(bad){ err(bad); return; }
    ws.files[name] = ws.files[ws.open]; delete ws.files[ws.open]; ws.open = name; persist(true); render();
  };
  el.querySelector("#wsdelf").onclick = () => {
    if(Object.keys(ws.files).length <= 1){ err("A project needs at least one file."); return; }
    if(!confirm(`Delete ${ws.open}?`)) return;
    delete ws.files[ws.open]; ws.open = Object.keys(ws.files)[0]; persist(true); render();
  };
  const download = (name, text, type) => { const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([text], {type: type || "text/plain"})); a.download = name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 1000); };
  el.querySelector("#wsdl").onclick = () => download(ws.open, ws.files[ws.open]);
  el.querySelector("#wsdlweb")?.addEventListener("click", () => download((ws.name.replace(/[^\w-]+/g, "-").toLowerCase() || "page") + ".html", buildWebPage(ws.files), "text/html"));
  const total = Object.values(ws.files).reduce((a, t) => a + t.length, 0);
  if(total > WS_LIMIT.bytes) err(`This project is ${Math.round(total/1000)} KB. Projects over ${WS_LIMIT.bytes/1000} KB may not sync, so download a copy.`);
  setTimeout(() => ed.refresh(), 0);
}

VIEWS.editor = viewEditor; VIEWS.code = viewCode; VIEWS.playground = viewEditor;
TAB_OF.code = "editor"; TAB_OF.playground = "editor";
document.addEventListener("click", e => {
  const w = e.target.closest("[data-ws]"); if(w){ go({v: "code", id: w.dataset.ws}); return; }
  const f = e.target.closest("[data-ws-from]"); if(f) wsFromProject(f.dataset.wsFrom);
});
SEARCH_SOURCES.push(() => [{t: "Editor", sub: "Your own multi-file projects, saved to your account", kind: "Page", i: "terminal", r: {v: "editor"}},
  ...WS.list().map(w => ({t: w.name, sub: `${WS_LANGS[w.lang]?.t || w.lang} · edited ${ago(w.updated)}`, kind: "Your project", i: "terminal", r: {v: "code", id: w.id}}))]);
