// Checks Python and JavaScript bootcamp steps with the real Judge.step: the solution must pass every check,
// and the starter (the previous step's solution) must fail at least one. HTML/SQL steps are checked in the browser test.
import fs from "fs"; import vm from "vm"; import { execFileSync } from "child_process";
const norm = s => String(s ?? "").replace(/\r/g, "").split("\n").map(x => x.replace(/\s+$/, "")).join("\n").trim();
const Runner = { async run(lang, src, stdin, onOut) {
  if (lang === "python") { try { onOut("o", execFileSync("python3", ["-c", src], { encoding: "utf8", timeout: 20000 })); } catch (e) { onOut("o", e.stdout || ""); onOut("e", e.stderr || String(e)); } return { ms: 0 }; }
  const c = vm.createContext({ JSON, Math, performance }); c.self = c;
  c.__post = (s, t) => onOut(s, t); c.console = { log: (...a) => onOut("o", a.map(x => typeof x === "string" ? x : JSON.stringify(x)).join(" ") + "\n") };
  try { vm.runInContext(src, c, { timeout: 10000 }); } catch (e) { onOut("e", String(e) + "\n"); } return { ms: 0 };
} };
const ctx = vm.createContext({ Runner, norm, JSON, Math, performance, console, RegExp }); 
vm.runInContext(fs.readFileSync(new URL("../judge.js", import.meta.url), "utf8") + "\n;this.Judge=Judge;", ctx);
const data = JSON.parse(fs.readFileSync(new URL("../data/bootcamp.json", import.meta.url), "utf8"));
let bad = 0, n = 0;
for (const c of data.courses) {
  if (!["python", "js"].includes(c.lang)) continue;
  for (let i = 0; i < c.steps.length; i++) {
    const s = c.steps[i], starter = s.starter ?? (i ? c.steps[i - 1].solution : ""); n++;
    const r = await ctx.Judge.step(s, c.lang, s.solution);
    const fails = r.checks.map((x, k) => x.ok ? null : x.msg).filter(Boolean);
    if (fails.length) { bad++; console.log(`FAIL ${c.id}/${s.id} solution:`, fails, r.stderr.slice(0, 300)); }
    const r2 = await ctx.Judge.step(s, c.lang, starter);
    if (r2.checks.every(x => x.ok)) { bad++; console.log(`STARTER PASSES ${c.id}/${s.id}`); }
  }
}
console.log(`${n} steps checked, ${bad} problems`); process.exit(bad ? 1 : 0);
