/* Runs learner Python in Pyodide, off the main thread.
   Messages in:  {kind:"warm"} | {id, kind:"python", code, stdin:[lines], files?:{"name.py": source}} (files are importable modules)
   Messages out: {type:"ready"} | {type:"fatal", error} | {id, type:"out", s:"o"|"e", text} | {id, type:"done", ms} */
let py = null, ready = null, cur = null;
const LIMIT = 100000; let sent = 0;

const HELPER = `
import sys, os, traceback, linecache, asyncio, importlib

__PROJ = "/home/pyodide/proj"
__loaded = set()

__tasks = []

def __tb(e):
    tb = e.__traceback__
    while tb is not None and tb.tb_frame.f_code.co_filename != "main.py":
        tb = tb.tb_next
    te = traceback.TracebackException(type(e), e, tb)
    te.stack = traceback.StackSummary.from_list([f for f in te.stack if f.filename == "main.py" or f.filename.startswith(__PROJ)])
    sys.stderr.write("".join(te.format()))

def __arun(main, *, debug=None):
    # Pyodide already runs an event loop, so asyncio.run schedules the coroutine; __drain awaits it.
    __tasks.append(asyncio.ensure_future(main))

async def __drain():
    while __tasks:
        t = __tasks.pop(0)
        try:
            await t
        except BaseException as e:
            __tb(e)
    sys.stdout.flush(); sys.stderr.flush()

def __setfiles(files):
    # Editor projects: write the other .py files where main.py can import them, and forget old copies of those modules.
    os.makedirs(__PROJ, exist_ok=True)
    sys.dont_write_bytecode = True
    for f in os.listdir(__PROJ):
        path = os.path.join(__PROJ, f)
        if os.path.isfile(path):
            os.remove(path)
    for name in list(__loaded) + [n[:-3] for n in files]:
        sys.modules.pop(name, None)
    __loaded.clear()
    for name, src in files.items():
        with open(os.path.join(__PROJ, name), "w") as fh:
            fh.write(src)
        __loaded.add(name[:-3])
    if __PROJ not in sys.path:
        sys.path.insert(0, __PROJ)
    importlib.invalidate_caches()

def __run(src, lines):
    it = iter(list(lines))
    def _input(prompt=""):
        try:
            v = next(it)
        except StopIteration:
            raise EOFError("input() ran out of lines. Open Input above the editor and type one line per input() call.") from None
        sys.stdout.write(str(prompt) + v + "\\n")
        return v
    linecache.cache["main.py"] = (len(src), None, src.splitlines(True), "main.py")
    g = {"__name__": "__main__", "__builtins__": __builtins__, "input": _input}
    _orig = asyncio.run
    asyncio.run = __arun
    try:
        exec(compile(src, "main.py", "exec"), g)
    except SystemExit:
        pass
    except BaseException as e:
        __tb(e)
    finally:
        asyncio.run = _orig
        sys.stdout.flush(); sys.stderr.flush()
`;

function stream(s) {
  const dec = new TextDecoder(); let buf = [];
  const flush = () => { if (!buf.length) return; const text = dec.decode(new Uint8Array(buf)); buf = [];
    if (sent >= LIMIT) return; sent += text.length;
    postMessage({ id: cur, type: "out", s, text: sent >= LIMIT ? text + "\n… output cut off at 100,000 characters\n" : text }); };
  return { raw: b => { buf.push(b); if (b === 10 || buf.length > 2048) flush(); }, flush };
}

function boot() {
  if (!ready) ready = (async () => {
    importScripts("pyodide/pyodide.js");
    // Artifacts don't serve .zip, so the standard library ships as base64 text and is unpacked into a blob URL.
    const b64 = await (await fetch("pyodide/python_stdlib.b64.txt")).text();
    const bin = atob(b64.replace(/\s+/g, "")), bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    const stdLibURL = URL.createObjectURL(new Blob([bytes], { type: "application/zip" }));
    py = await loadPyodide({ indexURL: new URL("pyodide/", self.location.href).href, stdLibURL });
    py.runPython(HELPER);
    postMessage({ type: "ready" });
  })();
  return ready;
}

self.onmessage = async (e) => {
  const { id, kind, code, stdin, files } = e.data;
  if (kind === "warm") { try { await boot(); } catch (err) { postMessage({ type: "fatal", error: String(err && err.message || err) }); } return; }
  cur = id; sent = 0;
  try { await boot(); }
  catch (err) { postMessage({ id, type: "out", s: "e", text: "Python could not start in this browser: " + (err && err.message || err) + "\n" }); postMessage({ id, type: "done", ms: 0 }); return; }
  const o = stream("o"), er = stream("e");
  py.setStdout({ raw: o.raw }); py.setStderr({ raw: er.raw });
  const t0 = performance.now();
  try {
    { const fs = py.toPy(files || {}); py.globals.get("__setfiles")(fs); fs.destroy();
      const lines = py.toPy(stdin || []); py.globals.get("__run")(code, lines); lines.destroy(); await py.runPythonAsync("await __drain()"); }
  } catch (err) { er.flush(); postMessage({ id, type: "out", s: "e", text: String(err && err.message || err) + "\n" }); }
  o.flush(); er.flush();
  postMessage({ id, type: "done", ms: Math.round(performance.now() - t0) });
};
