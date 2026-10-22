"""Build data/paths/*.json and data/paths/index.json from tools/paths_src/*.py, validating references."""
import json, os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "paths_src"))
import _lib
for m in ["web", "ai_data", "security", "infra", "mobile_games", "systems", "specialist"]: __import__(m)
P = _lib.PATHS
mods = {m["id"] for s in range(9) for m in json.load(open(f"data/s{s}.json"))["modules"]}
icons = set(re.findall(r"^  (\w+):'", open("ui.js").read(), re.M))
ids = [p["id"] for p in P]; errs = []
assert len(ids) == len(set(ids)), "duplicate path ids"
for p in P:
    if p["icon"] not in icons: errs.append(f"{p['id']}: unknown icon {p['icon']}")
    for r in p.get("related", []):
        if r not in ids: errs.append(f"{p['id']}: related {r} missing")
    for c in p.get("core", []):
        if c not in mods: errs.append(f"{p['id']}: core {c} missing")
    seen = set()
    for ph in p["phases"]:
        for n in ph["nodes"]:
            if n["id"] in seen: errs.append(f"{p['id']}: duplicate node {n['id']}")
            seen.add(n["id"])
            if n.get("core") and n["core"] not in mods: errs.append(f"{p['id']}/{n['id']}: core {n['core']} missing")
            if not n["links"]: errs.append(f"{p['id']}/{n['id']}: no links")
            for t, u in n["links"]:
                if not u.startswith("https://"): errs.append(f"{p['id']}/{n['id']}: bad url {u}")
if errs: print("\n".join(errs)); sys.exit(1)
os.makedirs("data/paths", exist_ok=True)
for f in glob.glob("data/paths/*.json"): os.remove(f)
cats = []
for p in P:
    if p["cat"] not in cats: cats.append(p["cat"])
    json.dump(p, open(f"data/paths/{p['id']}.json", "w"), separators=(",", ":"), ensure_ascii=False)
idx = [{k: p[k] for k in ("id", "title", "icon", "hue", "cat", "tagline", "duration")} | {"phases": [{"t": ph["title"], "nodes": [n["id"] for n in ph["nodes"]]} for ph in p["phases"]]} for p in P]
json.dump({"cats": cats, "paths": idx}, open("data/paths/index.json", "w"), separators=(",", ":"), ensure_ascii=False)
nodes = sum(len(ph["nodes"]) for p in P for ph in p["phases"]); links = {u for p in P for ph in p["phases"] for n in ph["nodes"] for _, u in n["links"]}
print(f"{len(P)} paths, {nodes} topics, {len(links)} unique links, cats={cats}")
