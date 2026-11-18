// Every debug challenge must fail in the site's real judge (Pyodide for Python, a worker for JavaScript), and the
// reference solution must pass, so each challenge can be fixed back to green.
//   python3 -m http.server 8765  (from the repo root), then: node tools/check_debug.cjs
const { chromium } = require("playwright");
(async () => {
  const b = await chromium.launch(), p = await b.newPage();
  await p.route(/gstatic|googleapis/, r => r.abort());
  await p.goto("http://localhost:8765/#/problems"); await p.waitForFunction(() => PB.list.length > 0, null, { timeout: 30000 });
  const r = await p.evaluate(async () => {
    const d = await loadDebug(), bad = []; let n = 0;
    for (const [id, rec] of Object.entries(d.problems)) { const pb = PB.byId[id];
      for (const [k, c] of Object.entries(rec)) { const lang = k === "js" ? "js" : "python"; n++;
        const bug = await Judge.problem(pb, lang, c.code, pb.tests), ref = await Judge.problem(pb, lang, pb.solution[k], pb.tests);
        const fails = bug.res ? bug.res.filter(x => !x.ok).length : -1;
        if (bug.fatal || !bug.res || fails < 1 || fails !== c.fails) bad.push(`${id} ${k}: bug fails ${fails} (expected ${c.fails})${bug.fatal ? " fatal " + bug.fatal : ""}`);
        if (ref.status !== "Accepted") bad.push(`${id} ${k}: reference is ${ref.status}`); } }
    return { n, bad };
  });
  console.log(`${r.n} debug challenges checked in the browser judge`); r.bad.forEach(x => console.log("FAIL", x));
  await b.close(); process.exit(r.bad.length ? 1 : 0);
})();
