"""Merge per-lesson extras into the stage files (data/sN.json).

- Videos come from tools/lesson_videos.tsv: lessonId <tab> YouTube id <tab> title. Lessons without a row get a
  "Search YouTube" link in the app instead.
- why / terms / mistakes / takeaways come from tools/lesson_extra/sN.py, which defines
  X = {lessonId: dict(why=str, terms=[(term, definition)], mistakes=[(wrong, right)], takeaways=[str])}.

Run from the repo root: python3 tools/merge_lessons.py
"""
import importlib.util, json, re, sys

VID = re.compile(r"^[A-Za-z0-9_-]{11}$")
videos = {}
for line in open("tools/lesson_videos.tsv", encoding="utf-8"):
    if line.startswith("#") or not line.strip():
        continue
    lid, vid, title = line.rstrip("\n").split("\t")
    assert VID.match(vid), f"{lid}: bad video id {vid}"
    videos[lid] = {"id": vid, "title": title}

errs, n = [], 0
for s in range(9):
    path = f"data/s{s}.json"
    d = json.load(open(path, encoding="utf-8"))
    try:
        spec = importlib.util.spec_from_file_location(f"x{s}", f"tools/lesson_extra/s{s}.py")
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); X = mod.X
    except FileNotFoundError:
        X = {}
    for m in d["modules"]:
        for l in m["lessons"]:
            lid = l["id"]
            for k in ("why", "terms", "mistakes", "takeaways", "video"):
                l.pop(k, None)
            if lid in videos:
                l["video"] = videos[lid]
            x = X.get(lid)
            if not x:
                errs.append(f"{lid}: no extra content"); continue
            l["why"] = x["why"]
            l["terms"] = [{"t": t, "d": dd} for t, dd in x["terms"]]
            l["mistakes"] = [{"wrong": w, "right": r} for w, r in x["mistakes"]]
            l["takeaways"] = list(x["takeaways"])
            if not (3 <= len(l["terms"]) <= 5): errs.append(f"{lid}: {len(l['terms'])} terms")
            if not (2 <= len(l["mistakes"]) <= 3): errs.append(f"{lid}: {len(l['mistakes'])} mistakes")
            if len(l["takeaways"]) != 3: errs.append(f"{lid}: {len(l['takeaways'])} takeaways")
            n += 1
    extra = set(X) - {l["id"] for m in d["modules"] for l in m["lessons"]}
    errs += [f"s{s}: unknown lesson {e}" for e in sorted(extra)]
    json.dump(d, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

print(f"{n} lessons enriched, {sum(1 for _ in videos)} videos")
for e in errs: print("  ", e)
sys.exit(1 if errs else 0)
