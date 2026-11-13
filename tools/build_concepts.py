"""Build data/concepts.json: the "Explain it simply" cards and which problems use which.

    python3 tools/build_concepts.py          (build_problems.py also runs it)

Every card's Python example is run with python3 and its JavaScript example with node, and the printed output must match
py_out / js_out exactly, so the cards can't teach something that isn't true. A problem gets a card when its reference
solution uses the idea, or one of its tags or its pattern names it. Fails if any example is wrong or a card is unused.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from problem_concepts import ALL, BLOCKS, PATTERNS  # noqa: E402

ROOT = os.path.dirname(HERE)
problems = json.load(open(os.path.join(ROOT, "data", "problems.json"), encoding="utf-8"))["problems"]
errors = []

# 1. every example prints exactly what its card says
for c in ALL:
    for lang, cmd in (("py", ["python3", "-I", "-c"]), ("js", ["node", "-e"])):
        try:
            got = subprocess.run(cmd + [c[lang]], capture_output=True, text=True, timeout=20)
            out = got.stdout.rstrip("\n")
            if got.returncode or out != c[lang + "_out"]:
                errors.append(f"{c['id']} {lang}: expected {c[lang + '_out']!r}, got {out!r} {got.stderr.strip()[-200:]}")
        except Exception as e:
            errors.append(f"{c['id']} {lang}: {e}")

# 2. which cards each problem needs: patterns first (the big idea), then building blocks, then Big-O
def uses(card, p):
    if card.get("always"):
        return True
    if set(card.get("tags", [])) & set(p.get("tags", [])) or p.get("cat") in card.get("cats", []):
        return True
    sol = p.get("solution", {})
    return bool((card.get("py_re") and re.search(card["py_re"], sol.get("py", ""), re.M))
                or (card.get("js_re") and re.search(card["js_re"], sol.get("js", ""), re.M)))

order = [c for c in PATTERNS if not c.get("always")] + BLOCKS + [c for c in PATTERNS if c.get("always")]
by_problem = {p["id"]: [c["id"] for c in order if uses(c, p)] for p in problems}
used = {i for ids in by_problem.values() for i in ids}
for c in ALL:
    if c["id"] not in used:
        errors.append(f"{c['id']}: no problem uses this card")

if errors:
    print("\n".join(errors)); sys.exit(1)

keep = ("id", "title", "kid", "how", "py", "py_out", "js", "js_out", "watch")
cards = {c["id"]: {k: c[k] for k in keep} | {"kind": "pattern" if c in PATTERNS else "block"} for c in ALL}
json.dump({"cards": cards, "byProblem": by_problem}, open(os.path.join(ROOT, "data", "concepts.json"), "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))
counts = [len(v) for v in by_problem.values()]
print(f"{len(cards)} concept cards, all {2 * len(cards)} examples verified; {len(by_problem)} problems, "
      f"{min(counts)}-{max(counts)} cards each (avg {sum(counts) / len(counts):.1f})")
