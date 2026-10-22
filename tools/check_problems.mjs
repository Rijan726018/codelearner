// Runs every reference solution (Python and JavaScript) through the real judge harness from judge.js.
// Usage: node tools/check_problems.mjs [problem-id]
import fs from "fs"; import vm from "vm"; import { execFileSync } from "child_process";
const src = fs.readFileSync(new URL("../judge.js", import.meta.url), "utf8");
const ctx = vm.createContext({ console, JSON, Math, performance });
vm.runInContext(src + "\n;this.__api={PY_PRELUDE,PY_HARNESS,JS_PRELUDE,JS_HARNESS_J,splitSentinel};", ctx);
const J = ctx.__api;
const data = JSON.parse(fs.readFileSync(new URL("../data/problems.json", import.meta.url), "utf8"));
const only = process.argv[2]; let bad = 0, n = 0;
for (const p of data.problems) {
  if (only && p.id !== only) continue; n++;
  for (const lang of ["py", "js"]) {
    for (const [label, code, wantAll] of [["solution", p.solution[lang], true], ["starter", p.starter[lang], false]]) {
      const spec = { fn: p.fn?.[lang], cls: p.cls?.[lang], kind: p.kind, cmp: p.cmp, inplace: p.inplace, types: p.types };
      let out = "", err = "";
      if (lang === "py") {
        const prog = J.PY_PRELUDE + code + J.PY_HARNESS(spec, p.tests);
        try { out = execFileSync("python3", ["-c", prog], { encoding: "utf8", timeout: 20000, maxBuffer: 1 << 26 }); } catch (e) { out = e.stdout || ""; err = e.stderr || String(e); }
      } else {
        const lines = [];
        const c2 = vm.createContext({ performance, JSON, Math, console, __post: (s, t) => lines.push(t) });
        c2.self = c2;
        try { vm.runInContext(J.JS_PRELUDE + code + "\n" + J.JS_HARNESS_J(spec, p.tests), c2, { timeout: 20000 }); } catch (e) { err = String(e); }
        out = lines.join("");
      }
      const { data: d } = J.splitSentinel(out);
      if (wantAll) {
        const fails = d?.res ? d.res.map((r, i) => r.ok ? null : i).filter(x => x !== null) : null;
        if (!d || d.fatal || fails.length) { bad++; console.log(`FAIL ${p.id} [${lang} ${label}]`, d?.fatal || "", fails ? `failed tests ${fails.join(",")}: got ${JSON.stringify(d.res[fails[0]].got ?? d.res[fails[0]].err).slice(0,200)} exp ${JSON.stringify(p.tests[fails[0]].exp).slice(0,200)}` : err.slice(0, 400)); }
      } else if (!d || (!d.res && !d.fatal)) { bad++; console.log(`STARTER BROKEN ${p.id} [${lang}]`, err.slice(0, 300)); }
      else if (d.res && d.res.every(r => r.ok)) { console.log(`STARTER PASSES?! ${p.id} [${lang}]`); }
    }
  }
}
console.log(`${n} problems checked, ${bad} failures`); process.exit(bad ? 1 : 0);
