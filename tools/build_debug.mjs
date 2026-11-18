// Build data/debug.json: one "debug challenge" per problem and language, a reference solution with a single realistic
// bug planted in it.  node tools/build_debug.mjs
//
// Every candidate bug (a flipped comparison, an off-by-one, a swapped and/or, a wrong starting value, min for max...)
// is run through the site's own judge harnesses (judge.js: PY_HARNESS with python3, JS_HARNESS_J in a Node sandbox)
// against the problem's full test set. A bug is kept only if the code still runs and gets a wrong answer on at least
// one test. Among those, the subtlest wins: fewest failing tests, wrong answers before crashes, some tests still passing.
// The reference solution itself must pass every test, so a challenge can always be fixed back to green.
import fs from "fs"; import vm from "vm"; import path from "path"; import { execFileSync } from "child_process"; import { fileURLToPath } from "url";
const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const J = (() => { const ctx = { addEventListener() {}, performance, console };
  vm.createContext(ctx); vm.runInContext(fs.readFileSync(path.join(ROOT, "judge.js"), "utf8") + "\n;globalThis.__J={PY_PRELUDE,PY_HARNESS,JS_PRELUDE,JS_HARNESS_J};", ctx); return ctx.__J; })();
const { problems } = JSON.parse(fs.readFileSync(path.join(ROOT, "data/problems.json"), "utf8"));
const SENT = "\x1eJUDGE";
const parse = out => { const i = out.lastIndexOf(SENT); if (i < 0) return null; const j = out.indexOf("\n", i); try { return JSON.parse(out.slice(i + SENT.length, j < 0 ? undefined : j)); } catch (e) { return null; } };
const spec = (p, py) => ({ fn: p.fn?.[py ? "py" : "js"], cls: p.cls?.[py ? "py" : "js"], kind: p.kind, cmp: p.cmp, inplace: p.inplace, types: p.types, opmap: py ? undefined : p.jsmap });

function runPy(p, code) {
  const src = J.PY_PRELUDE + code + J.PY_HARNESS(spec(p, true), p.tests);
  try { return parse(execFileSync("python3", ["-I", "-c", src], { timeout: 4000, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"], maxBuffer: 1 << 24 })); }
  catch (e) { return e.stdout ? parse(e.stdout) : null; }   // a timeout or a crash before the harness: not a usable bug
}
function runJs(p, code) {
  let out = ""; const ctx = { __post: (s, t) => { if (s === "o") out += t; }, performance, console: { log() {}, error() {}, warn() {} } }; ctx.self = ctx;
  try { vm.createContext(ctx); vm.runInContext(J.JS_PRELUDE + code + "\n" + J.JS_HARNESS_J(spec(p, false), p.tests), ctx, { timeout: 2000 }); }
  catch (e) { return null; }
  return parse(out);
}

// Each operator: a regex, a replacement, and the plain-words hint a learner gets as the first rung ("where to look").
const OPS = {
  py: [
    [/<=/g, "<", "a comparison"], [/(?<![<-])<(?![<=])/g, "<=", "a comparison"], [/>=/g, ">", "a comparison"], [/(?<![->])>(?![>=])/g, ">=", "a comparison"],
    [/==/g, "!=", "a condition"], [/!=/g, "==", "a condition"],
    [/ \+ 1\b/g, "", "an off-by-one"], [/ - 1\b/g, "", "an off-by-one"], [/(\w) \+= 1\b/g, "$1 += 2", "a step size"],
    [/\band\b/g, "or", "a condition"], [/\bor\b/g, "and", "a condition"], [/\bTrue\b/g, "False", "a true/false value"], [/\bFalse\b/g, "True", "a true/false value"],
    [/\bmin\(/g, "max(", "a min or max"], [/\bmax\(/g, "min(", "a min or max"],
    [/= 0$/gm, "= 1", "a starting value"], [/= 1$/gm, "= 0", "a starting value"], [/\[1:\]/g, "[2:]", "a slice"], [/\[:-1\]/g, "[:-2]", "a slice"],
    [/\[-1\]/g, "[0]", "an index"], [/\[0\]/g, "[-1]", "an index"]
  ],
  js: [
    [/<=/g, "<", "a comparison"], [/(?<![<-])<(?![<=])/g, "<=", "a comparison"], [/>=/g, ">", "a comparison"], [/(?<![=>-])>(?![>=])/g, ">=", "a comparison"],
    [/===/g, "!==", "a condition"], [/!==/g, "===", "a condition"],
    [/ \+ 1\b/g, "", "an off-by-one"], [/ - 1\b/g, "", "an off-by-one"], [/(\w)\+\+/g, "$1 += 2", "a step size"],
    [/&&/g, "||", "a condition"], [/\|\|/g, "&&", "a condition"], [/\btrue\b/g, "false", "a true/false value"], [/\bfalse\b/g, "true", "a true/false value"],
    [/Math\.min\(/g, "Math.max(", "a min or max"], [/Math\.max\(/g, "Math.min(", "a min or max"],
    [/= 0;/g, "= 1;", "a starting value"], [/= 1;/g, "= 0;", "a starting value"], [/\.slice\(1\)/g, ".slice(2)", "a slice"],
    [/\[0\]/g, "[1]", "an index"]
  ]
};
// one mutant per occurrence of each operator, skipping comment lines
function mutants(code, lang) {
  const out = [], lines = code.split("\n");
  lines.forEach((line, li) => {
    const t = line.trim(); if (!t || t.startsWith("#") || t.startsWith("//")) return;
    for (const [re, rep, kind] of OPS[lang]) {
      re.lastIndex = 0; let m;
      const r = new RegExp(re.source, re.flags.includes("g") ? re.flags : re.flags + "g");
      while ((m = r.exec(line))) {
        const nl = line.slice(0, m.index) + m[0].replace(new RegExp(re.source, re.flags.replace("g", "")), rep) + line.slice(m.index + m[0].length);
        if (nl !== line) out.push({ code: [...lines.slice(0, li), nl, ...lines.slice(li + 1)].join("\n"), line: li + 1, kind, was: line.trim(), now: nl.trim() });
        if (!m[0].length) r.lastIndex++;
      }
    }
  });
  return out;
}
const score = r => { const fails = r.res.filter(x => !x.ok), errs = fails.filter(x => x.err).length;
  return fails.length === 0 ? null : (fails.length === r.res.length ? 1000 : 0) + errs * 50 + fails.length; };

const out = {}, errors = []; let made = 0, tried = 0;
for (const p of problems) {
  const rec = {};
  for (const [lang, run] of [["py", runPy], ["js", runJs]]) {
    const ref = run(p, p.solution[lang]);
    if (!ref?.res || ref.res.some(x => !x.ok)) { errors.push(`${p.id} ${lang}: the reference solution doesn't pass its own tests`); continue; }
    let best = null;
    for (const m of mutants(p.solution[lang], lang)) {
      tried++; const r = run(p, m.code); if (!r?.res || r.fatal) continue;
      const s = score(r); if (s == null) continue;
      if (!best || s < best.s || (s === best.s && m.line > best.m.line)) best = { s, m, r };
    }
    if (!best) continue;
    const fails = best.r.res.filter(x => !x.ok).length;
    rec[lang] = { code: best.m.code, line: best.m.line, kind: best.m.kind, fails, total: best.r.res.length };
    made++;
  }
  if (Object.keys(rec).length) out[p.id] = rec;
}
if (errors.length) { console.error(errors.join("\n")); process.exit(1); }
fs.writeFileSync(path.join(ROOT, "data/debug.json"), JSON.stringify({ problems: out }));
const n = Object.keys(out).length;
console.log(`${made} debug challenges for ${n} of ${problems.length} problems (${tried} candidate bugs run through the judge)`);
