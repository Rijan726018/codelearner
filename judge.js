"use strict";
/* ---------- Judge: runs learner code against test cases, in the same sandboxes the editor uses.
   Problems: user code + a generated harness run as one program; the harness prints one sentinel line (char 30 + "JUDGE" + JSON).
   ListNode / TreeNode helpers are injected on a single prelude line, so error line numbers are shifted back by one. ---------- */
const SENT = String.fromCharCode(30) + "JUDGE";
const PY_PRELUDE = `import sys as _cl_s; _cl_s.stdout = getattr(_cl_s.stdout, "_cl_real", _cl_s.stdout); import builtins as _cl_b; exec("class ListNode:\\n def __init__(self, val=0, next=None):\\n  self.val = val\\n  self.next = next\\n def __repr__(self):\\n  return f'ListNode({self.val})'\\nclass TreeNode:\\n def __init__(self, val=0, left=None, right=None):\\n  self.val = val\\n  self.left = left\\n  self.right = right\\n def __repr__(self):\\n  return f'TreeNode({self.val})'", _cl_b.__dict__)\n`;
const JS_PRELUDE = `self.ListNode=class ListNode{constructor(val=0,next=null){this.val=val;this.next=next;}};self.TreeNode=class TreeNode{constructor(val=0,left=null,right=null){this.val=val;this.left=left;this.right=right;}};\n`;

// Bootcamp steps: tee stdout into a buffer (one prelude line) so checks can read it as _out; restores the real stream on the next run.
const STEP_PY_PRELUDE = `import sys as _cl_s; exec("class _ClTee:\\n def __init__(s, w):\\n  s._cl_real = w\\n  s.buf = []\\n def write(s, t):\\n  s.buf.append(t)\\n  return s._cl_real.write(t)\\n def flush(s):\\n  return s._cl_real.flush()\\n def __getattr__(s, k):\\n  return getattr(s._cl_real, k)", globals()); _cl_s.stdout = _ClTee(getattr(_cl_s.stdout, "_cl_real", _cl_s.stdout))\n`;
const PY_HARNESS = (spec, tests) => `

def _cl_judge():
    import json, time
    S = json.loads(${JSON.stringify(JSON.stringify(spec))})
    T = json.loads(${JSON.stringify(JSON.stringify(tests))})
    G = globals()
    def to_list(a):
        d = ListNode(); c = d
        for v in a:
            c.next = ListNode(v); c = c.next
        return d.next
    def from_list(n):
        out = []
        while n is not None and len(out) < 10001:
            out.append(n.val); n = n.next
        return out
    def to_tree(a):
        if not a or a[0] is None: return None
        root = TreeNode(a[0]); q = [root]; i = 1
        while q and i < len(a):
            node = q.pop(0)
            if i < len(a) and a[i] is not None:
                node.left = TreeNode(a[i]); q.append(node.left)
            i += 1
            if i < len(a) and a[i] is not None:
                node.right = TreeNode(a[i]); q.append(node.right)
            i += 1
        return root
    def from_tree(r):
        out = []; q = [r]
        while q and len(out) < 20001:
            n = q.pop(0)
            if n is None:
                out.append(None); continue
            out.append(n.val); q.append(n.left); q.append(n.right)
        while out and out[-1] is None: out.pop()
        return out
    def cin(v, t):
        if t == "list": return to_list(v)
        if t == "tree": return to_tree(v)
        return v
    def cout(v, t):
        if t == "list": return from_list(v)
        if t == "tree": return from_tree(v)
        if isinstance(v, (tuple, set, frozenset)): v = list(v)
        return json.loads(json.dumps(v, default=lambda o: list(o) if isinstance(o, (set, tuple, frozenset)) else repr(o)))
    def key(x): return json.dumps(x, sort_keys=True)
    def same(got, exp, mode):
        if mode == "float":
            try: return abs(float(got) - float(exp)) <= 1e-5 * max(1.0, abs(float(exp)))
            except Exception: return False
        if mode == "unordered" and isinstance(got, list) and isinstance(exp, list):
            return sorted(got, key=key) == sorted(exp, key=key)
        if mode == "deep" and isinstance(got, list) and isinstance(exp, list):
            norm = lambda L: sorted([sorted(x, key=key) if isinstance(x, list) else x for x in L], key=key)
            try: return norm(got) == norm(exp)
            except Exception: return False
        return got == exp
    res = []
    types = S.get("types") or {}
    ain = types.get("args") or []
    if S.get("kind") == "design":
        cls = G.get(S["cls"])
        if cls is None:
            print("\x1eJUDGE" + json.dumps({"fatal": "Define a class named " + S["cls"] + "."})); return
        for t in T:
            outs = []; obj = None; t0 = time.perf_counter()
            try:
                for op, a in zip(t["ops"], t["args"]):
                    if op == S["cls"]:
                        obj = cls(*a); outs.append(None)
                    else:
                        outs.append(cout(getattr(obj, op)(*a), None))
                ok = outs == t["exp"]
                res.append({"ok": ok, "got": outs, "ms": round((time.perf_counter() - t0) * 1000, 2)})
            except Exception as e:
                res.append({"ok": False, "err": type(e).__name__ + ": " + str(e), "got": outs})
        print("\x1eJUDGE" + json.dumps({"res": res})); return
    fn = G.get(S["fn"])
    if not callable(fn):
        print("\x1eJUDGE" + json.dumps({"fatal": "Define a function named " + S["fn"] + "."})); return
    for t in T:
        args = [cin(json.loads(json.dumps(a)), ain[i] if i < len(ain) else None) for i, a in enumerate(t["args"])]
        t0 = time.perf_counter()
        try:
            got = fn(*args)
            ms = round((time.perf_counter() - t0) * 1000, 2)
            if S.get("inplace") is not None: got = args[S["inplace"]]
            got = cout(got, types.get("ret"))
            res.append({"ok": same(got, t["exp"], S.get("cmp")), "got": got, "ms": ms})
        except RecursionError:
            res.append({"ok": False, "err": "RecursionError: maximum recursion depth exceeded (is your base case reachable?)"})
        except Exception as e:
            res.append({"ok": False, "err": type(e).__name__ + ": " + str(e)})
    print("\x1eJUDGE" + json.dumps({"res": res}))

_cl_judge()
`;

const JS_HARNESS_J = (spec, tests) => `
;(function(){
  const __S=${JSON.stringify(spec)}, __T=${JSON.stringify(tests)};
  const toList=a=>{ const d=new ListNode(); let c=d; for(const v of a){ c.next=new ListNode(v); c=c.next; } return d.next; };
  const fromList=n=>{ const o=[]; while(n&&o.length<10001){ o.push(n.val); n=n.next; } return o; };
  const toTree=a=>{ if(!a.length||a[0]===null) return null; const r=new TreeNode(a[0]); const q=[r]; let i=1;
    while(q.length&&i<a.length){ const n=q.shift(); if(i<a.length&&a[i]!==null){ n.left=new TreeNode(a[i]); q.push(n.left); } i++; if(i<a.length&&a[i]!==null){ n.right=new TreeNode(a[i]); q.push(n.right); } i++; } return r; };
  const fromTree=r=>{ const o=[]; const q=[r]; while(q.length&&o.length<20001){ const n=q.shift(); if(n===null||n===undefined){ o.push(null); continue; } o.push(n.val); q.push(n.left??null); q.push(n.right??null); } while(o.length&&o[o.length-1]===null) o.pop(); return o; };
  const cin=(v,t)=>t==="list"?toList(v):t==="tree"?toTree(v):v;
  const cout=(v,t)=>{ if(t==="list") return fromList(v); if(t==="tree") return fromTree(v); if(v instanceof Set) v=[...v]; if(v===undefined) return null; try{ return JSON.parse(JSON.stringify(v)); }catch(e){ return String(v); } };
  const key=x=>JSON.stringify(x);
  const same=(g,e,m)=>{ if(m==="float") return typeof g==="number"&&Math.abs(g-e)<=1e-5*Math.max(1,Math.abs(e));
    if(m==="unordered"&&Array.isArray(g)&&Array.isArray(e)) return key([...g].sort((a,b)=>key(a)<key(b)?-1:key(a)>key(b)?1:0))===key([...e].sort((a,b)=>key(a)<key(b)?-1:key(a)>key(b)?1:0));
    if(m==="deep"&&Array.isArray(g)&&Array.isArray(e)){ const srt=L=>L.map(x=>Array.isArray(x)?[...x].sort((a,b)=>key(a)<key(b)?-1:key(a)>key(b)?1:0):x).sort((a,b)=>key(a)<key(b)?-1:key(a)>key(b)?1:0); return key(srt(g))===key(srt(e)); }
    return key(g)===key(e); };
  const done=o=>__post("o","\x1eJUDGE"+JSON.stringify(o)+"\\n");
  const res=[], types=__S.types||{}, ain=types.args||[];
  if(__S.kind==="design"){
    const C=${spec.kind==="design"?`(typeof ${spec.cls}!=="undefined"?${spec.cls}:undefined)`:"undefined"};
    if(typeof C!=="function"){ done({fatal:"Define a class named "+__S.cls+"."}); return; }
    for(const t of __T){ const outs=[]; let obj=null; const t0=performance.now();
      try{ t.ops.forEach((op,i)=>{ if(op===__S.cls){ obj=new C(...t.args[i]); outs.push(null); } else outs.push(cout(obj[(__S.opmap||{})[op]||op](...t.args[i]),null)); });
        res.push({ok:key(outs)===key(t.exp), got:outs, ms:+(performance.now()-t0).toFixed(2)}); }
      catch(e){ res.push({ok:false, err:(e&&e.name?e.name+": "+e.message:String(e)), got:outs}); } }
    done({res}); return;
  }
  const F=${spec.fn?`(typeof ${spec.fn}!=="undefined"?${spec.fn}:undefined)`:"undefined"};
  if(typeof F!=="function"){ done({fatal:"Define a function named "+__S.fn+"."}); return; }
  for(const t of __T){ const args=JSON.parse(JSON.stringify(t.args)).map((a,i)=>cin(a,ain[i])); const t0=performance.now();
    try{ let got=F(...args); const ms=+(performance.now()-t0).toFixed(2); if(__S.inplace!=null) got=args[__S.inplace]; got=cout(got,types.ret); res.push({ok:same(got,t.exp,__S.cmp), got, ms}); }
    catch(e){ res.push({ok:false, err:(e instanceof RangeError?"RangeError: "+e.message+" (is your base case reachable?)":(e&&e.name?e.name+": "+e.message:String(e)))}); } }
  done({res});
})();
`;

function splitSentinel(out){
  const i=out.lastIndexOf(SENT); if(i<0) return {stdout:out, data:null};
  const j=out.indexOf("\n", i); const raw=out.slice(i+SENT.length, j<0?undefined:j);
  let data=null; try{ data=JSON.parse(raw); }catch(e){}
  return {stdout:out.slice(0,i)+(j<0?"":out.slice(j+1)), data};
}
const fixLines = (s, lang) => lang==="python" ? s.replace(/File "main\.py", line (\d+)/g,(m,n)=>`File "main.py", line ${Math.max(1,n-1)}`) : s.replace(/\(line (\d+)\)/g,(m,n)=>`(line ${Math.max(1,n-1)})`);

/* ---------- Web apps (HTML + CSS + JS): run in a sandboxed iframe (scripts on, opaque origin).
   A prelude adds an in-memory localStorage (opaque origins can't use the real one) and forwards console output and errors
   to the parent; for checks, a harness appended to the page drives it (click, type, submit) and posts back the results. ---------- */
const WEB = {
  handlers:{},
  token(){ return "w"+Math.random().toString(36).slice(2,10); },
  prelude(token, seed={}){
    return `<script>(function(){var T=${JSON.stringify(token)};
var m=new Map(Object.entries(${JSON.stringify(seed)}));
try{window.localStorage.getItem("__cl")}catch(e){var s={getItem:function(k){k=String(k);return m.has(k)?m.get(k):null},setItem:function(k,v){m.set(String(k),String(v))},removeItem:function(k){m.delete(String(k))},clear:function(){m.clear()},key:function(i){return Array.from(m.keys())[i]||null},get length(){return m.size}};
try{Object.defineProperty(window,"localStorage",{value:s,configurable:true})}catch(_){}}
window.__cl_logs=[];
var post=function(level,args){var text=Array.prototype.map.call(args,function(a){if(typeof a==="string")return a;try{return JSON.stringify(a)}catch(_){return String(a)}}).join(" ");window.__cl_logs.push(text);try{parent.postMessage({__cl:T,type:"log",level:level,text:Array.prototype.map.call(args,function(a){if(typeof a==="string")return a;try{return JSON.stringify(a)}catch(_){return String(a)}}).join(" ")},"*")}catch(_){}};
["log","info","warn","error"].forEach(function(k){var o=console[k];console[k]=function(){post(k,arguments);o&&o.apply(console,arguments)}});
window.addEventListener("error",function(e){post("error",[(e.message||"Error")+(e.lineno?" (line "+e.lineno+")":"")])});
window.addEventListener("unhandledrejection",function(e){post("error",["Uncaught (in promise) "+(e.reason&&e.reason.message||e.reason)])});
window.alert=function(x){post("info",["alert: "+x])};})();<\/script>`;
  },
  inject(code, head, tail=""){
    let out = /<head[^>]*>/i.test(code) ? code.replace(/<head[^>]*>/i, m=>m+head) : /<html[^>]*>/i.test(code) ? code.replace(/<html[^>]*>/i, m=>m+head) : head+code;
    if(tail){ const i=out.toLowerCase().lastIndexOf("</body>"); out = i>=0 ? out.slice(0,i)+tail+out.slice(i) : out+tail; }
    return out;
  },
  harness(token, tests){
    const body = tests.map((t,i)=> t.js ? `try{ R[${i}] = await (async()=>{ ${t.do||""}\n; await _wait(${t.wait??40}); return !!(${t.js}); })(); }catch(e){ R[${i}]=false; E[${i}]=String(e&&e.message||e); }` : "").join("\n");
    return `<script>window.addEventListener("load",function(){ setTimeout(async function(){ const R={}, E={};
const $=s=>document.querySelector(s), $$=s=>Array.from(document.querySelectorAll(s)), _wait=ms=>new Promise(r=>setTimeout(r,ms)), _el=s=>{ const e=typeof s==="string"?$(s):s; if(!e) throw new Error("No element matches "+s); return e; },
  _text=s=>((typeof s==="string"?$(s):s)?.textContent||"").replace(/\\s+/g," ").trim(),
  _click=s=>_el(s).click(), _type=(s,v)=>{ const e=_el(s); e.focus(); e.value=v; e.dispatchEvent(new Event("input",{bubbles:true})); e.dispatchEvent(new Event("change",{bubbles:true})); },
  _press=(s,key="Enter")=>{ const e=_el(s); e.dispatchEvent(new KeyboardEvent("keydown",{key,bubbles:true})); e.dispatchEvent(new KeyboardEvent("keyup",{key,bubbles:true})); },
  _submit=s=>_el(s).dispatchEvent(new Event("submit",{bubbles:true,cancelable:true})),
  _logs=()=>window.__cl_logs.join("\\n"), _visible=s=>{ const e=typeof s==="string"?$(s):s; if(!e) return false; const cs=getComputedStyle(e); return cs.display!=="none"&&cs.visibility!=="hidden"&&e.getClientRects().length>0; };
${body}
parent.postMessage({__cl:${JSON.stringify(token)},type:"result",R,E},"*"); }, 60); });<\/script>`;
  }
};
if(typeof addEventListener==="function") addEventListener("message", e=>{ const d=e.data; if(d && typeof d==="object" && d.__cl && WEB.handlers[d.__cl]) WEB.handlers[d.__cl](d); });

const Judge = {
  /* Run a problem's tests. lang: "python" | "js". Returns {status, res, stdout, stderr, ms, fatal} */
  async problem(p, lang, code, tests){
    const spec={fn:p.fn?.[lang==="python"?"py":"js"], cls:p.cls?.[lang==="python"?"py":"js"], kind:p.kind, cmp:p.cmp, inplace:p.inplace, types:p.types, opmap:lang==="js"?p.jsmap:undefined};
    const src = lang==="python" ? PY_PRELUDE + code + PY_HARNESS(spec, tests) : JS_PRELUDE + code + "\n" + JS_HARNESS_J(spec, tests);
    let out="", err=""; const t0=performance.now();
    const r = await Runner.run(lang, src, [], (s,text)=>{ if(s==="e") err+=text; else out+=text; }, {limit: lang==="python"?12000:6000});
    const {stdout, data} = splitSentinel(out);
    const base = {stdout, stderr:fixLines(err, lang), ms:Math.round(r.ms ?? (performance.now()-t0))};
    if(r.stopped || /Stopped after/.test(err)) return {...base, status:"Time Limit Exceeded"};
    if(!data) return {...base, status: /SyntaxError|IndentationError/.test(err) ? "Compile Error" : "Runtime Error"};
    if(data.fatal) return {...base, status:"Compile Error", fatal:data.fatal};
    const res=data.res; const fail=res.findIndex(x=>!x.ok);
    return {...base, res, status: fail<0 ? "Accepted" : res[fail].err ? "Runtime Error" : "Wrong Answer", firstFail:fail};
  },
  /* Run a bootcamp step: returns {checks:[{ok,msg}], stdout, stderr, rows} */
  async step(step, lang, code, ctx={}){
    const tests=step.tests||[]; const checks=[]; let stdout="", stderr="", rows=null;
    if(lang==="python"||lang==="js"){
      const exprs=tests.map((t,i)=>({i, e:t.py||t.js})).filter(x=>x.e);
      let harness="";
      if(lang==="python") harness = `\n\ndef _cl_step():\n    import json, sys\n    _src = ${JSON.stringify(code)}\n    G = dict(globals()); G["_src"] = _src\n    G["_out"] = "".join(getattr(sys.stdout, "buf", []))\n    def _raises(f, exc=Exception):\n        try:\n            f()\n        except exc:\n            return True\n        except Exception:\n            return False\n        return False\n    G["_raises"] = _raises\n    sys.stdout = getattr(sys.stdout, "_cl_real", sys.stdout)\n    R = {}\n${exprs.map(x=>`    try:\n        R[${x.i}] = bool(eval(${JSON.stringify(x.e)}, G))\n    except Exception as e:\n        R[${x.i}] = False\n`).join("")}    print("\x1eJUDGE" + json.dumps(R))\n_cl_step()\n`;
      if(lang==="js" && exprs.length) harness = `\n;(function(){ const R={}; const _src=${JSON.stringify(code)}; const _out=__cl_out.join("");\n${exprs.map(x=>`try{ R[${x.i}]=!!(${x.e}); }catch(e){ R[${x.i}]=false; }`).join("\n")}\n__post("o","\x1eJUDGE"+JSON.stringify(R)+"\\n"); })();\n`;
      let out="";
      const jsPre = `const __cl_out=[]; { const _l=console.log; console.log=(...a)=>{ __cl_out.push(a.map(x=>typeof x==="string"?x:JSON.stringify(x)).join(" ")+"\\n"); _l(...a); }; }\n`;
      const src = lang==="python" ? STEP_PY_PRELUDE + code + harness : jsPre.replace(/\n$/,"") + " " + code + "\n" + harness;
      const r = await Runner.run(lang, src, ctx.stdin||[], (s,text)=>{ if(s==="e") stderr+=text; else out+=text; }, {limit:8000});
      const sp=splitSentinel(out); stdout=sp.stdout; const R=sp.data||{};
      if(lang==="python") stderr=fixLines(stderr,"python");
      if(r.stopped) stderr += (stderr?"":"Your code took too long. Check for a loop that never ends.\n");
      tests.forEach((t,i)=>{ let ok;
        if(t.py||t.js) ok=!!R[i];
        else if(t.out!=null) ok=norm(stdout)===norm(t.out);
        else if(t.outHas!=null) ok=stdout.includes(t.outHas);
        else if(t.outRe!=null) ok=new RegExp(t.outRe,"m").test(stdout);
        else if(t.src!=null) ok=new RegExp(t.src,"m").test(code);
        else if(t.noErr) ok=!stderr.trim();
        else ok=false;
        checks.push({ok, msg:t.msg}); });
      if(stderr.trim()) checks.forEach(c=>{ if(!c.ok) c.hint="Your code raised an error. Read it in the output panel."; });
      return {checks, stdout, stderr};
    }
    if(lang==="sql"){
      const sets=[]; let out="";
      await Runner.run("sql", (step.seed||"")+"\n"+code, [], (s,text)=>{ if(s==="e") stderr+=text; else out+=text; }, {onRows:m=>sets.push({cols:m.cols, rows:m.rows})});
      rows = sets[sets.length-1]||null; stdout=out;
      tests.forEach(t=>{ let ok=false;
        if(t.src!=null) ok=new RegExp(t.src,"im").test(code);
        else if(t.rows){ if(rows){ const a=rows.rows.map(r=>JSON.stringify(r)), b=t.rows.map(r=>JSON.stringify(r)); ok = t.ordered ? JSON.stringify(a)===JSON.stringify(b) : JSON.stringify([...a].sort())===JSON.stringify([...b].sort()); } }
        else if(t.cols){ ok=!!rows && JSON.stringify(rows.cols.map(c=>c.toLowerCase()))===JSON.stringify(t.cols.map(c=>c.toLowerCase())); }
        else if(t.count!=null){ ok=!!rows && rows.rows.length===t.count; }
        checks.push({ok, msg:t.msg}); });
      return {checks, stdout, stderr, rows};
    }
    if(lang==="html"){
      const doc=ctx.doc, win=ctx.win;
      tests.forEach(t=>{ let ok=false;
        try{
          if(t.src!=null) ok=new RegExp(t.src,"im").test(code);
          else {
            const els=doc?[...doc.querySelectorAll(t.sel)]:[]; const el=els[0];
            if(t.count!=null) ok=els.length>=t.count;
            else if(t.exists===false) ok=!el;
            else if(t.nonempty) ok=!!el && norm(el.textContent).length>0;
            else if(t.text!=null) ok=!!el && norm(el.textContent).toLowerCase().includes(String(t.text).toLowerCase());
            else if(t.attr){ const v=el?.getAttribute(t.attr); ok = t.val==null ? v!=null : t.re ? new RegExp(t.val,"i").test(v||"") : (v||"").trim()===t.val; }
            else if(t.style){ const cs=el&&win?win.getComputedStyle(el):null; const v=cs?cs.getPropertyValue(t.style).trim():""; ok = t.re ? new RegExp(t.val,"i").test(v) : v===t.val; }
            else if(t.parent){ ok=!!el && !!el.parentElement?.closest(t.parent); }
            else ok=!!el;
          }
        }catch(e){ ok=false; }
        checks.push({ok, msg:t.msg}); });
      return {checks};
    }
    if(lang==="web"){
      // Each check gets a fresh copy of the page, so one check's clicks can't affect another's.
      const logs=[]; let timedOut=false;
      const runOne = t => new Promise(resolve=>{
        const token=WEB.token(), f=document.createElement("iframe");
        f.setAttribute("sandbox","allow-scripts"); f.setAttribute("aria-hidden","true"); f.tabIndex=-1;
        f.style.cssText="position:fixed;left:-10000px;top:0;width:1024px;height:768px;border:0;visibility:hidden";
        const done=r=>{ clearTimeout(timer); delete WEB.handlers[token]; f.remove(); resolve(r); };
        const timer=setTimeout(()=>{ timedOut=true; done(null); }, 8000);
        WEB.handlers[token]=d=>{ if(d.type==="log") logs.push(d); else if(d.type==="result") done(d); };
        document.body.appendChild(f); f.srcdoc=WEB.inject(code, WEB.prelude(token, t.storage||step.storage||{}), WEB.harness(token, [t]));
      });
      const results = await Promise.all(tests.map(t => t.src!=null ? Promise.resolve(null) : runOne(t)));
      const errs=[...new Set(logs.filter(l=>l.level==="error").map(l=>l.text))];
      tests.forEach((t,i)=>{ const ok = t.src!=null ? new RegExp(t.src,"m").test(code) : !!results[i]?.R?.[0];
        checks.push({ok, msg:t.msg, err:results[i]?.E?.[0]}); });
      checks.forEach(c=>{ if(c.ok) return; c.hint = timedOut ? "Your page didn't finish loading within 8 seconds. Look for a loop that never ends." : errs.length ? "Your page logged an error: "+errs[0] : c.err ? "While checking: "+c.err : ""; });
      return {checks, stdout:[...new Set(logs.filter(l=>l.level!=="error").map(l=>l.text))].join("\n"), stderr:errs.join("\n")};
    }
    return {checks:[]};
  }
};
