"""Build data/problems.json from tools/problems_src.py.
Expected outputs are computed by running each Python reference solution; check_problems.mjs then
verifies both reference solutions through the real in-browser judge harness."""
import json, copy, os, sys
sys.path.insert(0, os.path.dirname(__file__))
sys.setrecursionlimit(10000)
import builtins
exec("class ListNode:\n def __init__(self, val=0, next=None):\n  self.val = val\n  self.next = next\nclass TreeNode:\n def __init__(self, val=0, left=None, right=None):\n  self.val = val\n  self.left = left\n  self.right = right", builtins.__dict__)
from problems_src import P, CATS
import problems_more  # noqa: F401 (adds more problems to P)

def to_list(a):
    d = ListNode(); c = d
    for v in a: c.next = ListNode(v); c = c.next
    return d.next
def from_list(n):
    o = []
    while n: o.append(n.val); n = n.next
    return o
def to_tree(a):
    if not a or a[0] is None: return None
    r = TreeNode(a[0]); q = [r]; i = 1
    while q and i < len(a):
        n = q.pop(0)
        if i < len(a) and a[i] is not None: n.left = TreeNode(a[i]); q.append(n.left)
        i += 1
        if i < len(a) and a[i] is not None: n.right = TreeNode(a[i]); q.append(n.right)
        i += 1
    return r
def from_tree(r):
    o = []; q = [r]
    while q:
        n = q.pop(0)
        if n is None: o.append(None); continue
        o.append(n.val); q.append(n.left); q.append(n.right)
    while o and o[-1] is None: o.pop()
    return o
def cin(v, t): return to_list(v) if t == "list" else to_tree(v) if t == "tree" else v
def cout(v, t):
    if t == "list": return from_list(v)
    if t == "tree": return from_tree(v)
    return json.loads(json.dumps(v))

out = []; ids = set()
for p in P:
    assert p["id"] not in ids, p["id"]; ids.add(p["id"])
    assert p["cat"] in {c["id"] for c in CATS}, p["id"]
    ns = {}
    exec(p["py"], ns)
    rec = {k: p[k] for k in ("id","title","difficulty","cat","tags","desc","constraints","hints","editorial","complexity") if k in p}
    rec["params"] = p.get("params", [])
    rec["starter"] = {}
    rec["solution"] = {"py": p["py"], "js": p["js"]}
    for k in ("cmp","inplace","types","kind","cls","jsmap"):
        if k in p: rec[k] = p[k]
    if p.get("kind") == "design":
        cls = ns[p["cls"]["py"]]
        def run(ops, args):
            res = []; obj = None
            for op, a in zip(ops, args):
                if op == p["cls"]["py"]: obj = cls(*a); res.append(None)
                else: res.append(json.loads(json.dumps(getattr(obj, op)(*a))))
            return res
        rec["tests"] = [{"ops": o, "args": a, "exp": run(o, a)} for o, a in p["tests_design"]]
        rec["examples"] = [{"ops": o, "args": a, "exp": run(o, a)} for o, a in p["design_examples"]]
        # starter code
        import re
        meths = re.findall(r"    def (\w+)\(self(?:, )?([^)]*)\)", p["py"])
        meths = [(m, a) for m, a in meths if m == "__init__" or not m.startswith("_")]
        rec["starter"]["py"] = f"class {p['cls']['py']}:\n" + "\n\n".join(f"    def {m}(self{', ' + a if a else ''}):\n        pass" for m, a in meths) + "\n"
        jm = [(p.get("jsmap", {}).get(m, m), a) for m, a in meths if m != "__init__"]
        init = [a for m, a in meths if m == "__init__"][0]
        rec["starter"]["js"] = f"class {p['cls']['js']} {{\n  constructor({init}) {{\n\n  }}\n" + "".join(f"\n  {m}({a}) {{\n\n  }}\n" for m, a in jm) + "}\n"
        rec["fnName"] = {"py": p["cls"]["py"], "js": p["cls"]["js"]}
    else:
        fn = ns[p["fn"]["py"]]; types = p.get("types", {}); ain = types.get("args", [])
        def run(args):
            a2 = [cin(copy.deepcopy(a), ain[i] if i < len(ain) else None) for i, a in enumerate(args)]
            got = fn(*a2)
            if p.get("inplace") is not None: got = a2[p["inplace"]]
            return cout(got, types.get("ret"))
        rec["fn"] = p["fn"]
        rec["tests"] = [{"args": a, "exp": run(a)} for a in p["tests"]]
        rec["examples"] = [{"args": a, "exp": run(a)} for a in p["examples"]]
        hasTypes = bool(types)
        doc_py = ""
        if hasTypes:
            doc_py = "# Definition for helper classes (already provided):\n# class ListNode:  val, next\n# class TreeNode:  val, left, right\n\n" if any(t in ("list","tree") for t in ain) else ""
        doc_js = "// Helper classes are already provided:\n// ListNode { val, next }   TreeNode { val, left, right }\n\n" if any(t in ("list","tree") for t in ain) else ""
        rec["starter"]["py"] = f"{doc_py}def {p['fn']['py']}({', '.join(p['params'])}):\n    # Write your solution here\n    pass\n"
        rec["starter"]["js"] = f"{doc_js}function {p['fn']['js']}({', '.join(p['params'])}) {{\n  // Write your solution here\n\n}}\n"
    out.append(rec)

order = {c["id"]: i for i, c in enumerate(CATS)}
diff = {"Easy":0,"Medium":1,"Hard":2}
out.sort(key=lambda r: (order[r["cat"]], diff[r["difficulty"]]))
json.dump({"categories": CATS, "problems": out}, open("data/problems.json","w"), separators=(",",":"))
from collections import Counter
print(len(out), "problems", dict(Counter(r["difficulty"] for r in out)), os.path.getsize("data/problems.json"), "bytes")
