"use strict";
/* ---------- code runners: Python + SQL in a Pyodide worker, JavaScript in a throwaway worker ---------- */
const LANGNAME = {python:"Python 3.12", js:"JavaScript", sql:"SQL (SQLite)", html:"HTML & CSS", web:"HTML, CSS & JS"};
const RUNNABLE = new Set(["python","js","sql"]);
const normLang = l => ({py:"python", python:"python", javascript:"js", js:"js", node:"js", sql:"sql"})[String(l||"").toLowerCase()] || null;
function detectLang(code, fallback){
  const c=String(code||"");
  if(/#include\s*</.test(c) || /\bfn main\(|\bpackage main\b|\bfunc \w+\(/.test(c)) return null;
  if(/^\s*(interface|type)\s+\w+|\w\)?\s*:\s*(number|string|boolean|void|unknown|any|\w+\[\])\b|<(string|number|T)>|\bas const\b|\bReact\b|<\/?[A-Z]\w*[ >]/m.test(c)) return null;
  if(/^\s*(SELECT|CREATE TABLE|INSERT INTO|WITH)\b/im.test(c) && !/console\.log|print\(/.test(c)) return "sql";
  if(/console\.(log|error)|=>|\bconst |\blet |function\s*\w*\s*\(|===/.test(c)) return "js";
  if(/\bprint\(|\bdef |\bimport |:\s*$|\belif\b|f"/m.test(c)) return "python";
  return fallback || null;
}

const Runner = (() => {
  let seq=0, active=null; const subs=new Set();
  const note = () => subs.forEach(f=>{ try{ f(); }catch(e){} });
  // persistent workers: Python (Pyodide) and SQL (sql.js). Each is killed and rebuilt on timeout.
  const W = {python:{file:"py-worker.js", name:"Python", w:null, ready:false, failed:null},
             sql:{file:"sql-worker.js", name:"SQL", w:null, ready:false, failed:null}};
  function get(kind){
    const k=W[kind]; if(k.w) return k.w;
    try{ k.w=new Worker(k.file); }catch(e){ k.failed=String(e.message||e); note(); return null; }
    k.w.onmessage = e => { const m=e.data;
      if(m.type==="ready"){ k.ready=true; k.failed=null; note(); return; }
      if(m.type==="fatal"){ k.failed=m.error; note(); return; }
      if(!active || m.id!==active.id) return;
      if(m.type==="out") active.onOut(m.s, m.text);
      if(m.type==="rows") active.onRows?.(m);
      if(m.type==="done"){ const a=active; active=null; clearTimeout(a.timer); a.resolve({ms:m.ms}); note(); } };
    k.w.onerror = e => { e.preventDefault?.(); k.failed = e.message || ("the "+k.name+" worker failed to load");
      if(active && active.kind===kind){ active.onOut("e", k.name+" could not start: "+k.failed+"\n"); const a=active; active=null; clearTimeout(a.timer); a.resolve({ms:0}); } note(); };
    k.w.postMessage({kind:"warm"}); return k.w;
  }
  function kill(msg){ if(!active) return; const a=active; active=null; clearTimeout(a.timer); a.kill?.(); a.onOut("e", msg); a.resolve({ms:null, stopped:true}); note(); }
  function runIn(kind, code, stdin, onOut, limit, onRows, files){
    const k=W[kind], wk=get(kind); if(!wk){ onOut("e",k.name+" can't run in this browser.\n"); return Promise.resolve({ms:0}); }
    return new Promise(resolve=>{
      const id=++seq;
      active={id, kind, onOut, onRows, resolve, kill:()=>{ k.w.terminate(); k.w=null; k.ready=false; setTimeout(()=>get(kind), 50); }};
      active.timer=setTimeout(()=>kill(`\nStopped after ${limit/1000} s. Check for a loop that never ends.\n`), limit + (k.ready?0:25000));
      wk.postMessage({id, kind, code, stdin, json:!!onRows, files}); note();
    });
  }
  const JS_HARNESS = `const __post=(s,text)=>postMessage({type:"out",s,text});
const __fmt=(v,d=0,seen=new Set())=>{ if(v===null) return "null"; const t=typeof v;
  if(t==="undefined") return "undefined"; if(t==="string") return d?"'"+v.replace(/'/g,"\\\\'")+"'":v;
  if(t==="number"||t==="boolean") return Object.is(v,-0)?"-0":String(v); if(t==="bigint") return v+"n"; if(t==="symbol") return v.toString();
  if(t==="function") return v.name?(/^class\\s/.test(Function.prototype.toString.call(v))?"[class "+v.name+"]":"[Function: "+v.name+"]"):"[Function (anonymous)]";
  if(seen.has(v)) return "[Circular]"; if(d>2) return Array.isArray(v)?"[Array]":"[Object]"; seen.add(v); let r;
  if(Array.isArray(v)) r=v.length?"[ "+v.map(x=>__fmt(x,d+1,seen)).join(", ")+" ]":"[]";
  else if(v instanceof Map) r="Map("+v.size+") {"+(v.size?" "+[...v].map(([k,x])=>__fmt(k,d+1,seen)+" => "+__fmt(x,d+1,seen)).join(", ")+" ":"")+"}";
  else if(v instanceof Set) r="Set("+v.size+") {"+(v.size?" "+[...v].map(x=>__fmt(x,d+1,seen)).join(", ")+" ":"")+"}";
  else if(v instanceof Error) r=v.stack&&v.stack.includes(v.message)?v.name+": "+v.message:String(v);
  else if(v instanceof Date) r=v.toISOString(); else if(v instanceof Promise) r="Promise { <pending> }";
  else { const ks=Object.keys(v), c=v.constructor, nm=c&&c!==Object&&c.name?c.name+" ":"";
    r=ks.length?nm+"{ "+ks.map(k=>(/^[A-Za-z_$][\\w$]*$/.test(k)?k:"'"+k+"'")+": "+__fmt(v[k],d+1,seen)).join(", ")+" }":nm+"{}"; }
  seen.delete(v); return r; };
const __log=s=>(...a)=>__post(s,a.map(x=>typeof x==="string"?x:__fmt(x)).join(" ")+"\\n");
console.log=console.info=console.debug=__log("o"); console.warn=console.error=__log("e");
console.table=(x)=>__post("o",__fmt(x)+"\\n");
let __pending=0; const __st=setTimeout, __ct=clearTimeout, __live=new Set();
self.setTimeout=(f,ms,...a)=>{ __pending++; postMessage({type:"pending",n:__pending}); const id=__st(()=>{ __live.delete(id); __pending--; try{ typeof f==="function"&&f(...a); } finally { postMessage({type:"pending",n:__pending}); } },ms); __live.add(id); return id; };
self.clearTimeout=id=>{ if(__live.delete(id)){ __pending--; postMessage({type:"pending",n:__pending}); } __ct(id); };
const __si=setInterval, __ci=clearInterval, __ivs=new Set();
self.setInterval=(f,ms,...a)=>{ __pending++; postMessage({type:"pending",n:__pending}); const id=__si(f,ms,...a); __ivs.add(id); return id; };
self.clearInterval=id=>{ if(__ivs.delete(id)){ __pending--; postMessage({type:"pending",n:__pending}); } __ci(id); };
self.addEventListener("unhandledrejection",e=>{ e.preventDefault(); const r=e.reason; __post("e","Uncaught (in promise) "+(r&&r.name?r.name+": "+r.message:__fmt(r))+"\\n"); });
var process={env:new Proxy({NODE_ENV:"development"},{set:(t,k,v)=>(t[k]=String(v),true)}),argv:["node","main.js"],platform:"browser",version:"v20 (browser sandbox)",exit:(c=0)=>{ throw new Error("process.exit("+c+")"); },cwd:()=>"/",nextTick:(f,...a)=>queueMicrotask(()=>f(...a))};
class Buffer extends Uint8Array{
  static from(x,enc="utf8"){ if(typeof x!=="string") return new Buffer(x);
    if(enc==="base64"||enc==="base64url"){ let b=x.replace(/-/g,"+").replace(/_/g,"/"); while(b.length%4) b+="="; const bin=atob(b); return new Buffer([...bin].map(ch=>ch.charCodeAt(0))); }
    if(enc==="hex") return new Buffer((x.match(/../g)||[]).map(h=>parseInt(h,16)));
    return new Buffer(new TextEncoder().encode(x)); }
  static byteLength(x){ return new TextEncoder().encode(String(x)).length; }
  toString(enc="utf8"){ if(enc==="hex") return [...this].map(b=>b.toString(16).padStart(2,"0")).join("");
    if(enc==="base64"||enc==="base64url"){ let s=btoa(String.fromCharCode(...this)); return enc==="base64url"?s.replace(/\\+/g,"-").replace(/\\//g,"_").replace(/=+$/,""):s; }
    return new TextDecoder().decode(this); }
}
self.fetch=()=>Promise.reject(new TypeError("fetch is blocked in this sandbox. Run network code in your own terminal with node."));
`;
  const OFFSET = JS_HARNESS.split("\n").length; // user code starts on this line + 1
  function runJS(code, onOut, limit){
    return new Promise(resolve=>{
      const id=++seq; let wk, url, done=false, synced=false, pending=0, quiet;
      const finish=(extra)=>{ if(done) return; done=true; clearTimeout(quiet); clearTimeout(active?.timer); try{ wk.terminate(); }catch(e){} URL.revokeObjectURL(url); if(extra) onOut("e",extra); active=null; resolve({ms:Math.round(performance.now()-t0)}); note(); };
      const settle=()=>{ clearTimeout(quiet); if(synced&&pending<=0) quiet=setTimeout(()=>finish(),60); };
      const asyncWrap=/\bawait\b/.test(code);
      const body = asyncWrap ? `(async()=>{\n${code}\n})().catch(e=>__post("e","Uncaught "+(e&&e.name?e.name+": "+e.message:__fmt(e))+"\\n")).finally(()=>__st(()=>postMessage({type:"sync"}),0));` : `${code}\n;__st(()=>postMessage({type:"sync"}),0);`;
      const off = OFFSET + (asyncWrap?1:0) - 1;
      url=URL.createObjectURL(new Blob([JS_HARNESS+body],{type:"text/javascript"}));
      const t0=performance.now();
      try{ wk=new Worker(url); }catch(e){ onOut("e","JavaScript workers are blocked in this browser.\n"); resolve({ms:0}); return; }
      active={id, onOut, resolve, kill:()=>finish(), timer:setTimeout(()=>finish(`\nStopped after ${limit/1000} s. A loop, timer or interval was still running.\n`), limit)};
      wk.onmessage=e=>{ const m=e.data; if(m.type==="out"){ onOut(m.s,m.text); settle(); } else if(m.type==="sync"){ synced=true; settle(); } else if(m.type==="pending"){ pending=m.n; settle(); } };
      wk.onerror=e=>{ e.preventDefault(); const ln=e.lineno?Math.max(1,e.lineno-off):null; onOut("e",`${e.message||"Error"}${ln?` (line ${ln})`:""}\n`); finish(); };
      note();
    });
  }
  return {
    warm(lang){ get(lang==='sql'?'sql':'python'); },
    ready(lang){ return lang==='js' || W[lang==='sql'?'sql':'python'].ready; }, failed(lang){ return lang==='js'?null:W[lang==='sql'?'sql':'python'].failed; },
    get busy(){ return !!active; },
    on(f){ subs.add(f); return ()=>subs.delete(f); },
    stop(){ kill("\nStopped.\n"); },
    run(lang, code, stdin, onOut, opt={}){
      if(active) kill("\nStopped (a new run started).\n");
      if(lang==="js") return runJS(code, onOut, opt.limit||5000);
      return runIn(lang==="sql"?"sql":"python", code, stdin, onOut, opt.limit||10000, opt.onRows, opt.files);
    },
    JS_HARNESS
  };
})();

/* ---------- drafts (per-lesson scratch code) ---------- */
const Drafts = {
  col:null, cache:{}, timers:{},
  key:k=>"tenk2-code-"+k,
  async get(k){
    if(k in this.cache) return this.cache[k];
    let v=null; try{ v=localStorage.getItem(this.key(k)); }catch(e){}
    if(this.col){ try{ const s=await this.col.doc("code-"+k).get(); if(s.exists){ v=s.data()?.code ?? v; } }catch(e){} }
    this.cache[k]=v; return v;
  },
  set(k,v){
    this.cache[k]=v; try{ localStorage.setItem(this.key(k), v); }catch(e){}
    if(!this.col) return; clearTimeout(this.timers[k]);
    this.timers[k]=setTimeout(()=>{ this.col.doc("code-"+k).set({code:String(v).slice(0,60000), updated:new Date().toISOString()}).catch(()=>{}); }, 1200);
  }
};

/* ---------- editor widget ---------- */
const CM_MODE = {python:"python", js:"javascript", sql:"text/x-sqlite", html:"htmlmixed", web:"htmlmixed"};

/* ---------- VS Code look and feel for CodeMirror ----------
   CodeMirror's modes give the base colours. An overlay adds what VS Code's Dark+/Light+ themes colour on top:
   control-flow keywords (purple), function calls (yellow), class names after class/new (teal), self/cls, indent guides
   and brackets. Bracket pairs are coloured by nesting depth like VS Code's bracket-pair colorization: the depth at the
   start of every line is recomputed on each change (skipping strings and comments), and each rendered line colours its
   brackets from there. Also: auto-closing brackets, the active line, and Ln/Col for the status bar. */
const VS_CONTROL = {
  python: new Set("if elif else for while return import from as try except finally raise with yield break continue pass await assert del global nonlocal match case".split(" ")),
  js: new Set("if else for while do switch case default return break continue throw try catch finally import export from await yield".split(" ")),
};
const VS_EDITOR_FILE = {python: "main.py", js: "main.js", sql: "query.sql", html: "index.html", web: "index.html"};
const VS_LANG = {py: "python", js: "js", json: "js", sql: "sql", html: "web", css: "web", md: "", txt: "", csv: ""};
function vsFileIcon(name){
  const e = (String(name).match(/\.([a-z0-9]+)$/i) || [])[1]?.toLowerCase() || "";
  const [t, c] = ({py: ["py", "py"], js: ["JS", "js"], json: ["{}", "json"], html: ["<>", "html"], css: ["#", "css"], sql: ["db", "sql"], md: ["M↓", "md"], txt: ["≡", "txt"], csv: ["≡", "csv"]})[e] || ["·", "txt"];
  return `<i class="fi fi-${c}" aria-hidden="true">${t}</i>`;
}
function vsOverlay(lang, unit){
  const ctl = VS_CONTROL[lang] || new Set(), html = lang === "html" || lang === "web";
  return {token(stream){
    const before = stream.string.slice(0, stream.pos);
    if(/^\s*$/.test(before) && stream.pos % unit === 0 && stream.match(" ".repeat(unit), false) && /\S/.test(stream.string)){ stream.pos += unit; return "vsguide"; }
    if(/^\s*$/.test(before) && stream.eatSpace()) return null;
    if(!html && stream.match(/^[()[\]{}]/)) return "vsbr";
    const m = !html && stream.match(/^[A-Za-z_$][\w$]*/);
    if(m){ const w = m[0];
      if(ctl.has(w)) return "vsctl";
      if(lang === "python" && (w === "self" || w === "cls")) return "vsself";
      if(/\b(class|new|extends)\s+$/.test(before) && /^[A-Z]/.test(w)) return "vstype";
      if(/^\s*\(/.test(stream.string.slice(stream.pos)) && !/\b(def|function|class)\s+$/.test(before)) return "vsfn";
      return null; }
    stream.next(); return null;
  }};
}
function vsEnhance(cm, lang, onPos){
  const unit = cm.getOption("indentUnit"), html = lang === "html" || lang === "web";
  cm.setOption("styleActiveLine", true);
  // brackets only: CodeMirror can't pair a quote after a prefix (f"...", r"..."), so auto-closed quotes would double up
  cm.setOption("autoCloseBrackets", {pairs: "()[]{}", explode: "[]{}", override: true});   // override: the python mode would otherwise swap in its own quote-pairing config
  cm.addOverlay(vsOverlay(lang, unit));
  if(onPos){ const pos = () => { const c = cm.getCursor(), sel = cm.getSelection().length; onPos(`Ln ${c.line + 1}, Col ${c.ch + 1}${sel ? ` (${sel} selected)` : ""}`); }; cm.on("cursorActivity", pos); pos(); }
  if(html) return cm;
  let depth = [];
  const OPEN = "([{", CLOSE = ")]}";
  const recompute = () => {
    const next = [], n = cm.lineCount(); let d = 0;
    for(let i = 0; i < n; i++){ next.push(d);
      for(const tk of cm.getLineTokens(i, true)){ if(/string|comment/.test(tk.type || "")) continue;
        for(const ch of tk.string){ if(OPEN.includes(ch)) d++; else if(CLOSE.includes(ch)) d = Math.max(0, d - 1); } } }
    const stale = []; for(let i = 0; i < n; i++) if(depth[i] !== next[i]) stale.push(i);
    depth = next; return stale;
  };
  cm.on("renderLine", (c, line, el) => {
    let d = depth[line.lineNo()] || 0;
    el.querySelectorAll(".cm-vsbr").forEach(sp => {
      if(/cm-string|cm-comment/.test(sp.className)) return;
      const ch = sp.textContent;
      if(OPEN.includes(ch)){ sp.classList.add("vsb" + (d % 3)); d++; } else { d = Math.max(0, d - 1); sp.classList.add("vsb" + (d % 3)); }
    });
  });
  // a line whose starting depth changed must re-render; toggling a line class makes CodeMirror redraw just that line
  cm.on("change", () => { recompute().forEach(i => { const h = cm.getLineHandle(i); if(!h) return; const on = (h.wrapClass || "").includes("vsr"); on ? cm.removeLineClass(h, "wrap", "vsr") : cm.addLineClass(h, "wrap", "vsr"); }); });
  recompute(); cm.refresh();
  return cm;
}
// Static code samples get the same colours through CodeMirror's runMode (null until it loads).
function vsGuessMode(code){
  const c = String(code || "");
  if(/^\s*</.test(c)) return "htmlmixed";
  if(/\b(SELECT|INSERT|CREATE TABLE|UPDATE|DELETE FROM)\b/i.test(c) && !/\bdef |console\.|=>/.test(c)) return "text/x-sqlite";
  if(/\b(const|let|var|function)\b|=>|console\.|===|\bdocument\./.test(c)) return "javascript";
  return "python";
}
function vsHighlight(code, mode){
  if(!window.CodeMirror?.runMode) return null;
  mode = mode || vsGuessMode(code);
  const lang = mode === "python" ? "python" : mode === "javascript" ? "js" : "", ctl = VS_CONTROL[lang] || new Set();
  const lines = [[]];
  try{
    CodeMirror.runMode(String(code || ""), mode, (text, style) => {
      if(text === "\n"){ lines.push([]); return; }
      let cls = style ? style.split(/\s+/).map(x => "cm-" + x).join(" ") : "";
      if(lang && /^[A-Za-z_$][\w$]*$/.test(text)){
        if(ctl.has(text)) cls += " cm-vsctl"; else if(lang === "python" && (text === "self" || text === "cls")) cls += " cm-vsself";
      }
      lines[lines.length - 1].push(cls.trim() ? `<span class="${cls.trim()}">${esc(text)}</span>` : esc(text));
    });
  }catch(e){ return null; }
  // function calls: a plain or variable token directly followed by "("
  return lines.map(parts => parts.join("").replace(/(<span class="cm-(?:variable|property|builtin|variable-2)[^"]*">[^<]+<\/span>|\b[A-Za-z_$][\w$]*)(?=\()/g, m => m.startsWith("<span") ? m.replace('class="', 'class="cm-vsfn ') : `<span class="cm-vsfn">${m}</span>`));
}
function mountEditor(host, {lang, code, draftKey=null, resetTo=code, compact=false, label="", onRun=null, runLabel="Run ▶", onChange=null, tall=false, carried=0}){
  const isMac=/Mac|iPhone|iPad/.test(navigator.platform||""), kb=isMac?"⌘↵":"Ctrl+↵";
  host.classList.add("ed"); host.classList.toggle("tall", !!tall);
  const file=/\.[a-z0-9]+$/i.test(label)?label:VS_EDITOR_FILE[lang]||"main", crumb=label&&label!==file?label:"";
  host.innerHTML = `<div class="edbar"><span class="vstab" title="${esc(file)}">${vsFileIcon(file)}<span>${esc(file)}</span></span>${crumb?`<span class="vscrumb">${esc(crumb)}</span>`:""}<span class="edsp"></span>
    ${lang==="python"?`<button type="button" class="btn ghost sm" data-in aria-expanded="false">Input</button>`:""}
    <button type="button" class="btn ghost sm" data-reset title="Restore the original code">Reset</button>
    <button type="button" class="btn primary sm" data-run title="Run (${kb})">${esc(runLabel)}</button></div>
    <div class="edwrap"></div>
    <div class="edin" hidden><label class="eyebrow" for="">Input · one line per input() call</label><textarea rows="3" spellcheck="false" placeholder="Ada&#10;1815"></textarea></div>
    <div class="edout" hidden><div class="edouthead"><span class="vspanel">Output</span><span class="edms"></span></div><pre class="edpre" aria-live="polite"></pre></div>
    <div class="edfoot"><span class="edstat"></span><span class="edsp"></span><span class="edpos"></span><span>Spaces: ${lang==="python"?4:2}</span><span>UTF-8</span><span>${esc({python:"Python",js:"JavaScript",sql:"SQL",html:"HTML",web:"HTML"}[lang]||lang)}</span></div>`;
  const wrap=host.querySelector(".edwrap"), runB=host.querySelector("[data-run]"), out=host.querySelector(".edout"), pre=host.querySelector(".edpre"),
        ms=host.querySelector(".edms"), stat=host.querySelector(".edstat"), inBox=host.querySelector(".edin"), inTa=inBox.querySelector("textarea"), inB=host.querySelector("[data-in]");
  const uid="ed"+Math.random().toString(36).slice(2,8); inTa.id=uid+"-in"; inBox.querySelector("label").setAttribute("for",inTa.id);
  let cm=null, ta=null, markCarried=()=>{};
  const run=()=>onRun?onRun():doRun();
  if(window.CodeMirror){
    cm=CodeMirror(wrap,{value:code, mode:CM_MODE[lang], lineNumbers:true, indentUnit:lang==="python"?4:2, tabSize:4, matchBrackets:true, viewportMargin:Infinity, lineWrapping:false,
      extraKeys:{"Cmd-Enter":run,"Ctrl-Enter":run,
        Tab:c=>c.somethingSelected()?c.indentSelection("add"):c.replaceSelection(" ".repeat(c.getOption("indentUnit")),"end"),
        "Shift-Tab":c=>c.indentSelection("subtract"), Esc:c=>c.getInputField().blur()}});
    cm.getInputField().setAttribute("aria-label", (LANGNAME[lang]||"Code")+" editor. Press Escape, then Tab, to leave.");
    vsEnhance(cm, lang, t=>{ const p=host.querySelector(".edpos"); if(p) p.textContent=t; });
    // lines carried over from earlier steps start dimmed; a line brightens once you edit it. The cursor waits at the end.
    if(carried){
      cm.on("change",(c,ch)=>{ for(let l=ch.from.line; l<=ch.from.line+ch.text.length-1; l++){ const h=c.getLineHandle(l); if(h) c.removeLineClass(h,"text","vscarried"); } });
      markCarried=()=>{ const n=Math.min(carried, cm.lineCount()); for(let i=0;i<n;i++) if(cm.getLine(i).trim()) cm.addLineClass(i,"text","vscarried"); const last=cm.lastLine(); cm.setCursor({line:last, ch:cm.getLine(last).length}); };
      markCarried();
    }
  } else {
    ta=document.createElement("textarea"); ta.className="edta"; ta.value=code; ta.spellcheck=false; ta.setAttribute("aria-label","Code editor"); wrap.appendChild(ta);
    ta.addEventListener("keydown",e=>{ if(e.key==="Enter"&&(e.metaKey||e.ctrlKey)){ e.preventDefault(); run(); } else if(e.key==="Tab"&&!e.shiftKey){ e.preventDefault(); const s=ta.selectionStart; ta.setRangeText(" ".repeat(lang==="python"?4:2),s,ta.selectionEnd,"end"); } });
  }
  const getV=()=>cm?cm.getValue():ta.value, setV=v=>cm?cm.setValue(v):(ta.value=v);
  if(draftKey){ Drafts.get(draftKey).then(v=>{ if(v!=null && v!==getV()){ setV(v); onChange?.(v); } });
    const onCh=()=>Drafts.set(draftKey,getV()); cm?cm.on("change",onCh):ta.addEventListener("input",onCh); }
  if(onChange){ let t; const f=()=>{ clearTimeout(t); t=setTimeout(()=>onChange(getV()),250); }; cm?cm.on("change",f):ta.addEventListener("input",f); }
  const usesInput=()=>lang==="python"&&/\binput\s*\(/.test(getV());
  if(inB){ const toggle=(open)=>{ inBox.hidden=!open; inB.setAttribute("aria-expanded",open); }; inB.onclick=()=>toggle(inBox.hidden); if(usesInput()) toggle(true); }
  host.querySelector("[data-reset]").onclick=()=>{ setV(resetTo); markCarried(); out.hidden=true; if(draftKey) Drafts.set(draftKey,resetTo); onChange?.(resetTo); };
  const status=()=>{
    if(lang==="html"||lang==="web"){ stat.textContent=`The preview updates as you type · ${kb} checks your code`; return; }
    if(Runner.busy && host.dataset.running) { stat.textContent=!Runner.ready(lang)?`Starting ${lang==="sql"?"SQLite":"Python"} (the first run takes a few seconds)…`:"Running…"; return; }
    if(Runner.failed(lang)){ stat.textContent=(lang==="sql"?"SQLite":"Python")+" couldn't load here: "+Runner.failed(lang); return; }
    stat.textContent = !Runner.ready(lang) ? `Loading ${lang==="sql"?"SQLite":"Python"} in the background… you can start typing. ${kb} runs.` : `${kb} to run · Tab indents · Esc leaves the editor`;
  };
  const unsub=Runner.on(()=>{ if(!host.isConnected){ unsub(); return; } status(); if(!onRun) runB.textContent = host.dataset.running ? "Stop ■" : runLabel; });
  async function doRun(){
    if(host.dataset.running){ Runner.stop(); return; }
    document.querySelectorAll(".ed[data-running]").forEach(x=>delete x.dataset.running);
    host.dataset.running="1"; out.hidden=false; pre.textContent=""; ms.textContent=""; runB.textContent="Stop ■"; status();
    let n=0; const lines=inTa.value.replace(/\r/g,"").split("\n"); if(lines.length && lines[lines.length-1]==="") lines.pop();
    const res=await Runner.run(lang, getV(), lines, (s,text)=>{ n+=text.length; const sp=document.createElement("span"); if(s==="e") sp.className="err"; sp.textContent=text; pre.appendChild(sp); });
    delete host.dataset.running; runB.textContent="Run ▶";
    if(!n && !res.stopped){ const sp=document.createElement("span"); sp.className="muted"; sp.textContent=lang==="sql"?"(no rows returned)":"(no output: nothing was printed)"; pre.appendChild(sp); }
    ms.textContent = res.ms!=null ? `${res.ms} ms` : ""; status();
  }
  runB.onclick=run;
  status(); if(lang==="python"||lang==="sql") Runner.warm(lang);
  return {get value(){ return getV(); }, set value(v){ setV(v); }, run:doRun, refresh:()=>cm&&cm.refresh(), focus:()=>cm?cm.focus():ta.focus(), host};
}

/* ---------- run the code shown in a question, after answering ---------- */
function runSnippet(btn, code, lang){
  const box=document.createElement("div"); box.className="qrun"; btn.replaceWith(box);
  mountEditor(box, {lang, code, compact:true, label:"Edit it, run it again, see what changes"}).run();
}

/* ---------- playground view ---------- */
const PLAY_START = {
  python:`# Python playground: anything goes.\nnames = ["Ada", "Grace", "Linus"]\nfor i, name in enumerate(names, start=1):\n    print(f"{i}. {name} has {len(name)} letters")\n`,
  js:`// JavaScript playground\nconst nums = [3, 1, 4, 1, 5, 9, 2, 6];\nconst evens = nums.filter(n => n % 2 === 0);\nconsole.log("evens:", evens);\nconsole.log("sum:", nums.reduce((a, b) => a + b, 0));\n`,
  sql:`-- SQL playground (SQLite, in memory: every run starts empty)\nCREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, city TEXT);\nINSERT INTO users (name, city) VALUES ('Ada', 'London'), ('Grace', 'New York'), ('Linus', 'Helsinki');\n\nSELECT city, COUNT(*) AS people FROM users GROUP BY city ORDER BY city;\n`
};
let playLang="python";
function viewPlayground(el){
  el.innerHTML=`<section style="display:grid;gap:10px"><span class="eyebrow">Run code in your browser</span><h1 class="h1">Playground</h1>
    <p class="lede">A scratch editor for trying ideas between lessons. Python runs real CPython 3.12 compiled for the browser; SQL runs on SQLite; JavaScript runs in a sandboxed worker. Your code saves automatically. For C, Go, Rust and shell, use your own terminal.</p></section>
    <div class="chips">${Object.keys(PLAY_START).map(k=>`<button type="button" class="chip" data-pl="${k}" aria-pressed="${k===playLang}">${esc(LANGNAME[k])}</button>`).join("")}</div>
    <div id="play"></div>`;
  el.querySelectorAll("[data-pl]").forEach(b=>b.onclick=()=>{ playLang=b.dataset.pl; render(); });
  mountEditor($("#play"), {lang:playLang, code:PLAY_START[playLang], draftKey:"play-"+playLang});
}
VIEWS.playground = viewPlayground;
