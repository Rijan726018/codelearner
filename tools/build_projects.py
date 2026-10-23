"""Build data/projects.json from tools/projects_src/*.py.
For SQL steps, expected rows come from running each solution on SQLite; for Python projects the demo output is
captured by running the finished program. Checks are verified by check_bootcamp.mjs (Python/JS) and in a browser (web/SQL)."""
import json, os, sys, sqlite3, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "projects_src"))
import _lib
for m in ["web", "python_projects", "more"]:
    if os.path.exists(os.path.join(HERE, "projects_src", m + ".py")): __import__(m)

def sql_rows(code):
    db = sqlite3.connect(":memory:"); cur = db.cursor(); last = None
    for stmt in code.split(";"):
        if not "\n".join(l for l in stmt.splitlines() if not l.strip().startswith("--")).strip(): continue
        cur.execute(stmt)
        if cur.description: last = ([d[0] for d in cur.description], [list(r) for r in cur.fetchall()])
    return last

mods = {m["id"] for s in range(9) for m in json.load(open(f"data/s{s}.json"))["modules"]}
ids, errs = set(), []
for p in _lib.PROJECTS:
    assert p["id"] not in ids, p["id"]; ids.add(p["id"])
    for c in p.get("core", []):
        if c not in mods: errs.append(f"{p['id']}: core {c} missing")
    for m in p["milestones"]:
        assert m["steps"], (p["id"], m["title"])
        for s in m["steps"]:
            assert s["id"] not in ids, s["id"]; ids.add(s["id"])
            assert s["tests"], s["id"]
            if s.get("core") and s["core"] not in mods: errs.append(f"{s['id']}: core {s['core']} missing")
            if p["lang"] == "sql":
                cols, rows = sql_rows(s["solution"])
                for t in s["tests"]:
                    if t.get("rows") is True: t["rows"] = rows
    if p["lang"] == "python" and p.get("demo_stdin") is not None:
        final = p["milestones"][-1]["steps"][-1]["solution"]
        echo = 'import builtins\n_cl_in = builtins.input\ndef _cl_echo(prompt=""):\n    value = _cl_in("")\n    print(f"{prompt}{value}")\n    return value\nbuiltins.input = _cl_echo\n'
        r = subprocess.run([sys.executable, "-c", echo + p.pop("demo_pre", "") + final], input="\n".join(p["demo_stdin"]) + "\n", capture_output=True, text=True, timeout=30)
        assert r.returncode == 0, (p["id"], r.stderr)
        p["demo"] = r.stdout.strip()
        p.pop("demo_stdin")
if errs: print("\n".join(errs)); sys.exit(1)
json.dump({"projects": _lib.PROJECTS}, open("data/projects.json", "w"), separators=(",", ":"), ensure_ascii=False)
print(len(_lib.PROJECTS), "projects,", sum(len(m["steps"]) for p in _lib.PROJECTS for m in p["milestones"]), "steps,", os.path.getsize("data/projects.json"), "bytes")
