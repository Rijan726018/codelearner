"""Give each bootcamp step only the earlier code it needs.

Most Python and JavaScript courses build one program: each step's solution is the previous solution plus a few new
lines. Learners used to start every step with the whole program so far, so by step 9 the editor held 25 lines that had
nothing to do with the task, and every run printed all the old output again.

trim(course) rewrites those steps in place. For a step whose solution is "previous solution + new code", it keeps only
the earlier top-level statements that the new code and the step's checks depend on (a backwards liveness pass over the
previous program), and sets:
    starter  = those statements                      (what the learner starts with; carried = "some")
    solution = those statements + the new code       (what the checks are proven against)
A step that edits earlier code instead of appending to it (adding a method to a class, say) starts from the full
previous program, as before (carried = "all"). Steps listed in KEEP_FULL also keep the full program, because their checks look at earlier
output or source (for example "your program prints at least three lines").

tools/check_bootcamp.mjs proves every result: each solution passes all its checks and each starter fails one.
"""
from __future__ import annotations

import ast
import builtins
import re

# Steps whose checks read earlier output or source; check_bootcamp.mjs fails them when trimmed.
KEEP_FULL: set[str] = {
    "p2",   # "Your program prints at least three lines", starting with step 1's Hello, world!
}

PY_BUILTINS = set(dir(builtins)) | {"_out", "_src"}
JS_WORDS = set("""break case catch class const continue debugger default delete do else export extends false finally for
function if import in instanceof let new null of return super switch this throw true try typeof var void while with yield
async await undefined NaN Infinity console Math JSON Number String Boolean Array Object Map Set Date RegExp Error
TypeError RangeError Promise parseInt parseFloat isNaN isFinite Symbol BigInt structuredClone _out _src""".split())


# ---------- Python ----------
def _py_names(node, ctx):
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name) and isinstance(n.ctx, ctx)}


def _py_defs_uses(stmt):
    """Names a top-level statement (re)defines, and names it reads from the program around it."""
    if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        inner = _py_names(stmt, ast.Store)
        params = {a.arg for a in ast.walk(stmt) if isinstance(a, ast.arg)}
        uses = _py_names(stmt, ast.Load) - inner - params - {stmt.name} - PY_BUILTINS
        for d in getattr(stmt, "decorator_list", []):
            uses |= _py_names(d, ast.Load) - PY_BUILTINS
        return {stmt.name}, uses
    if isinstance(stmt, (ast.Import, ast.ImportFrom)):
        return {(a.asname or a.name).split(".")[0] for a in stmt.names}, set()
    defs = _py_names(stmt, ast.Store)
    uses = _py_names(stmt, ast.Load) - PY_BUILTINS
    # x.append(1), x[0] = 1, x.y = 2: these change x, so a later reader of x needs them
    for n in ast.walk(stmt):
        if isinstance(n, (ast.Attribute, ast.Subscript)) and isinstance(n.ctx, ast.Store):
            base = n.value
            while isinstance(base, (ast.Attribute, ast.Subscript)):
                base = base.value
            if isinstance(base, ast.Name):
                defs.add(base.id)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name):
            defs.add(n.func.value.id)
    if isinstance(stmt, ast.AugAssign) and isinstance(stmt.target, ast.Name):
        uses.add(stmt.target.id)
    # comprehension and lambda variables are local to them
    local = set()
    for n in ast.walk(stmt):
        if isinstance(n, ast.comprehension):
            local |= _py_names(n.target, ast.Store)
        if isinstance(n, ast.Lambda):
            local |= {a.arg for a in n.args.args}
    return defs - local, uses - local


def _py_trim(prev: str, needed: set[str]) -> str | None:
    try:
        tree = ast.parse(prev)
    except SyntaxError:
        return None
    lines = prev.split("\n")
    keep = []
    for stmt in reversed(tree.body):
        defs, uses = _py_defs_uses(stmt)
        if defs & needed:
            keep.append(stmt)
            needed = (needed - (defs - uses)) | uses
    keep.reverse()
    parts = []
    for stmt in keep:
        start = min([stmt.lineno] + [d.lineno for d in getattr(stmt, "decorator_list", [])])
        text = "\n".join(lines[start - 1:stmt.end_lineno])
        block = isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        if parts and (block or parts[-1][1]):
            parts.append(("", False))
        parts.append((text, block))
    return "\n".join(p for p, _ in parts)


def _py_needs(new_code: str, tests) -> set[str] | None:
    try:
        tree = ast.parse(new_code)
    except SyntaxError:
        return None
    needed = set()
    defined = set()
    for stmt in tree.body:
        defs, uses = _py_defs_uses(stmt)
        needed |= uses - defined
        defined |= defs - uses
    for t in tests:
        if t.get("py"):
            try:
                needed |= _py_names(ast.parse(t["py"], mode="eval"), ast.Load) - PY_BUILTINS
            except SyntaxError:
                return None
    return needed


# ---------- JavaScript (course code: one statement per line or block, semicolons, no tricky regexes) ----------
def _js_strip(code: str) -> str:
    """Blank out comments, plain strings and regex literals so identifiers inside them don't count; keep ${...}."""
    out, i, n = [], 0, len(code)
    while i < n:
        c = code[i]
        if code.startswith("//", i):
            j = code.find("\n", i); i = n if j < 0 else j; continue
        if code.startswith("/*", i):
            j = code.find("*/", i + 2); i = n if j < 0 else j + 2; continue
        if c in "'\"":
            j = i + 1
            while j < n and code[j] != c:
                j += 2 if code[j] == "\\" else 1
            out.append(" "); i = j + 1; continue
        if c == "`":
            j = i + 1
            while j < n and code[j] != "`":
                if code.startswith("${", j):
                    depth, k = 1, j + 2
                    while k < n and depth:
                        depth += {"{": 1, "}": -1}.get(code[k], 0); k += 1
                    out.append(" " + code[j + 2:k - 1] + " "); j = k; continue
                j += 2 if code[j] == "\\" else 1
            i = j + 1; continue
        if c == "/":
            prev = "".join(out).rstrip()[-1:]
            if prev in "(,=:[!&|?{};" or prev == "":
                j = i + 1
                while j < n and code[j] != "/":
                    if code[j] == "\n":
                        break
                    j += 2 if code[j] == "\\" else 1
                if j < n and code[j] == "/":
                    j += 1
                    while j < n and code[j].isalpha():
                        j += 1
                    out.append(" "); i = j; continue
        out.append(c); i += 1
    return "".join(out)


def _js_statements(code: str):
    """Split a program into top-level statements as (start_line, end_line) pairs (inclusive, 0-based)."""
    lines, stmts, start, depth = code.split("\n"), [], None, 0
    stripped = _js_strip(code).split("\n")
    for i, (raw, s) in enumerate(zip(lines, stripped)):
        if start is None:
            if not raw.strip() or raw.strip().startswith("//"):
                continue
            start = i
        depth += s.count("{") + s.count("(") + s.count("[") - s.count("}") - s.count(")") - s.count("]")
        nxt = next((l.strip() for l in lines[i + 1:] if l.strip()), "")
        if depth == 0 and (raw.rstrip().endswith(";") or raw.rstrip().endswith("}")) and not re.match(r"(else|catch|finally)\b", nxt):
            stmts.append((start, i)); start = None
    if start is not None:
        stmts.append((start, len(lines) - 1))
    return stmts


ID = r"[A-Za-z_$][\w$]*"


def _js_ids(s: str):
    s = re.sub(r"([{,]\s*)" + ID + r"\s*:(?!:)", r"\1", s)   # object keys ({ price: 4.5 }) aren't variables
    return {m.group(1) for m in re.finditer(r"(?<![\w$.])(" + ID + r")", s)} - JS_WORDS


def _js_defs_uses(text: str):
    s = _js_strip(text)
    head = s.lstrip()
    m = re.match(r"(?:async\s+)?(function\*?|class)\s+(" + ID + r")", head)
    if m:
        name = m.group(2)
        params = set()
        pm = re.match(r"(?:async\s+)?function\*?\s+" + ID + r"\s*\(([^)]*)\)", head)
        if pm:
            params = _js_ids(pm.group(1))
        local = {x.group(1) for x in re.finditer(r"\b(?:const|let|var)\s+(" + ID + r")", s)}
        local |= {i for x in re.finditer(r"\b(?:const|let|var)\s*[\[{]([^\]}]*)[\]}]", s) for i in _js_ids(x.group(1))}
        local |= {i for x in re.finditer(r"\(([^()]*)\)\s*=>|(" + ID + r")\s*=>", s) for i in _js_ids(x.group(0).split("=>")[0])}
        return {name}, _js_ids(s) - params - local - {name}
    defs = set()
    dm = re.match(r"(?:const|let|var)\s+(" + ID + r")", head)
    if dm:
        defs.add(dm.group(1))
    dm = re.match(r"(?:const|let|var)\s*[\[{]([^\]}]*)[\]}]", head)
    if dm:
        defs |= _js_ids(dm.group(1))
    defs |= {x.group(1) for x in re.finditer(r"(?<![\w$.])(" + ID + r")\s*(?:[-+*/%]?=(?![=>])|\+\+|--)", s)}
    defs |= {x.group(1) for x in re.finditer(r"(?<![\w$.])(" + ID + r")\s*\.\s*(?:push|pop|shift|unshift|splice|sort|reverse|fill|set|add|delete|clear)\s*\(", s)}
    defs |= {x.group(1) for x in re.finditer(r"(?<![\w$.])(" + ID + r")\s*(?:\[[^\]\n]*\]|\.\s*" + ID + r")+\s*[-+*/%]?=(?![=>])", s)}
    arrow_params = {i for x in re.finditer(r"\(([^()]*)\)\s*=>|(" + ID + r")\s*=>", s) for i in _js_ids(x.group(0).split("=>")[0])}
    block_locals = {x.group(1) for x in re.finditer(r"\b(?:const|let|var)\s+(" + ID + r")", s)} - defs
    uses = _js_ids(s) - arrow_params - block_locals
    if re.match(r"(?:const|let|var)\s", head):
        uses -= {d for d in defs if not re.search(r"(?<![\w$.])" + re.escape(d) + r"(?![\w$])", s[s.find("=") + 1:] if "=" in s else "")}
    return defs - arrow_params, uses


def _js_trim(prev: str, needed: set[str]) -> str:
    lines = prev.split("\n")
    stmts = _js_statements(prev)
    keep = []
    for a, b in reversed(stmts):
        text = "\n".join(lines[a:b + 1])
        defs, uses = _js_defs_uses(text)
        if defs & needed:
            keep.append((a, b, text))
            needed = (needed - (defs - uses)) | uses
    keep.reverse()
    parts = []
    for a, b, text in keep:
        block = b > a
        if parts and (block or parts[-1][1]):
            parts.append(("", False))
        parts.append((text, block))
    return "\n".join(p for p, _ in parts)


def _js_needs(new_code: str, tests) -> set[str]:
    needed, defined = set(), set()
    lines = new_code.split("\n")
    for a, b in _js_statements(new_code):
        defs, uses = _js_defs_uses("\n".join(lines[a:b + 1]))
        needed |= uses - defined
        defined |= defs - uses
    for t in tests:
        if t.get("js"):
            needed |= _js_ids(_js_strip(t["js"]))
    return needed


# ---------- the pass over a course ----------
def trim(course) -> dict:
    """Rewrite one course's steps in place. Returns counts for the build log."""
    lang = course.get("lang")
    stats = {"trimmed": 0, "full": 0, "fresh": 0}
    if lang not in ("python", "js"):
        return stats
    original = [s["solution"] for s in course["steps"]]
    for i, s in enumerate(course["steps"]):
        if i == 0 or "starter" in s:
            continue
        prev, sol = original[i - 1], original[i]
        if not sol.startswith(prev) or s["id"] in KEEP_FULL:
            s["starter"] = prev          # an edit step, or one whose checks need the earlier program
            s["carried"] = "all"
            stats["full"] += 1
            continue
        new = sol[len(prev):]
        needed = _py_needs(new, s["tests"]) if lang == "python" else _js_needs(new, s["tests"])
        ctx = (_py_trim(prev, needed) if lang == "python" else _js_trim(prev, needed)) if needed is not None else None
        if ctx is None:
            s["starter"] = prev
            s["carried"] = "all"
            stats["full"] += 1
            continue
        ctx = ctx.strip("\n")
        s["starter"] = ctx + "\n\n" if ctx else ""
        s["solution"] = s["starter"] + new.lstrip("\n")
        if ctx:
            s["carried"] = "some"   # the page says these lines come from earlier steps, and dims them
        stats["trimmed" if ctx else "fresh"] += 1
    return stats
