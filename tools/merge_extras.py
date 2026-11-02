"""Merge extras into the Build & Learn projects and the problems.

- Projects (data/projects.json): video from tools/project_videos.tsv, plus why / mistakes / takeaways from
  tools/project_extra.py.
- Problems (data/problems.json): a video per pattern (category) from tools/problem_videos.tsv, plus a key
  takeaway and common mistakes per problem from tools/problem_extra.py.

build_projects.py and build_problems.py call apply_projects / apply_problems before writing, so a rebuild keeps
these fields. Run this file directly to merge into the existing JSON without rebuilding:
    python3 tools/merge_extras.py
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VID = re.compile(r"^[A-Za-z0-9_-]{11}$")

def _videos(name):
    out = {}
    for line in open(os.path.join(HERE, name), encoding="utf-8"):
        if line.startswith("#") or not line.strip(): continue
        key, vid, title = line.rstrip("\n").split("\t")
        assert VID.match(vid), f"{name}: bad video id for {key}: {vid}"
        out[key] = {"id": vid, "title": title}
    return out

def _extra(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod.X

def apply_projects(projects):
    vids, X, errs = _videos("project_videos.tsv"), _extra("project_extra"), []
    for p in projects:
        for k in ("video", "why", "mistakes", "takeaways"): p.pop(k, None)
        if p["id"] in vids: p["video"] = vids[p["id"]]
        x = X.get(p["id"])
        if not x: errs.append(f"{p['id']}: no extras"); continue
        p["why"] = x["why"]; p["mistakes"] = [{"wrong": w, "right": r} for w, r in x["mistakes"]]; p["takeaways"] = list(x["takeaways"])
        if not 2 <= len(p["mistakes"]) <= 3: errs.append(f"{p['id']}: {len(p['mistakes'])} mistakes")
        if len(p["takeaways"]) != 3: errs.append(f"{p['id']}: {len(p['takeaways'])} takeaways")
    errs += [f"unknown project {k}" for k in set(X) - {p["id"] for p in projects}]
    return errs

def apply_problems(data):
    vids, X, errs = _videos("problem_videos.tsv"), _extra("problem_extra"), []
    for c in data["categories"]:
        c.pop("video", None)
        if c["id"] in vids: c["video"] = vids[c["id"]]
        else: errs.append(f"pattern {c['id']}: no video")
    for p in data["problems"]:
        p.pop("takeaway", None); p.pop("mistakes", None)
        x = X.get(p["id"])
        if not x: errs.append(f"{p['id']}: no extras"); continue
        p["takeaway"] = x[0]; p["mistakes"] = [{"wrong": w, "right": r} for w, r in x[1]]
        if not 1 <= len(p["mistakes"]) <= 3: errs.append(f"{p['id']}: {len(p['mistakes'])} mistakes")
    errs += [f"unknown problem {k}" for k in set(X) - {p["id"] for p in data["problems"]}]
    return errs

if __name__ == "__main__":
    os.chdir(os.path.dirname(HERE))
    pj = json.load(open("data/projects.json", encoding="utf-8")); e1 = apply_projects(pj["projects"])
    json.dump(pj, open("data/projects.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
    pb = json.load(open("data/problems.json", encoding="utf-8")); e2 = apply_problems(pb)
    json.dump(pb, open("data/problems.json", "w"), separators=(",", ":"))
    print(f"{len(pj['projects'])} projects ({sum('video' in p for p in pj['projects'])} with videos), "
          f"{len(pb['problems'])} problems, {sum('video' in c for c in pb['categories'])} pattern videos")
    for e in e1 + e2: print("  ", e)
    sys.exit(1 if e1 or e2 else 0)
