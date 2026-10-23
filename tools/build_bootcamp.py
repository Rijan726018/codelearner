"""Build data/bootcamp.json from tools/bootcamp_src.py. SQL expectations come from running each reference query on SQLite."""
import json, os, sys, sqlite3
sys.path.insert(0, os.path.dirname(__file__))
from bootcamp_src import C

def sql_rows(seed, ref):
    db = sqlite3.connect(":memory:"); db.executescript(seed); cur = db.cursor(); last = None
    for stmt in [x.strip() for x in ref.split(";") if x.strip()]:
        cur.execute(stmt)
        if cur.description: last = ([d[0] for d in cur.description], [list(r) for r in cur.fetchall()])
    return last

ids = set()
for c in C:
    for i, s in enumerate(c["steps"]):
        assert s["id"] not in ids, s["id"]; ids.add(s["id"])
        assert s["tests"], s["id"]
        if c["lang"] == "sql":
            cols, rows = sql_rows(c["seed"], s["ref"])
            for t in s["tests"]:
                if t.get("rows") is True:
                    t["rows"] = rows
                    if s.get("ordered"): t["ordered"] = True
            s.pop("ref"); s.pop("ordered", None)
json.dump({"courses": C}, open("data/bootcamp.json", "w"), separators=(",", ":"))
print(len(C), "courses,", sum(len(c["steps"]) for c in C), "steps,", os.path.getsize("data/bootcamp.json"), "bytes")
