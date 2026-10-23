// Verifies browser-only steps (HTML, web apps, SQL) for Bootcamp courses and Build projects using the real Judge:
// every solution must pass all its checks; every starter must fail at least one.
// Usage: python3 -m http.server 8765 &  then  NODE_PATH=$(npm root -g) node tools/check_in_browser.cjs [http://localhost:8765/]
const { chromium } = require('playwright');
(async () => {
  const url = process.argv[2] || 'http://localhost:8765/';
  const b = await chromium.launch(); const p = await b.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.route(/cdnjs|fonts\./, r => r.abort());
  await p.goto(url + '#/home'); await p.waitForFunction(() => typeof Judge !== 'undefined' && BC.courses.length && PJ.list.length, null, { timeout: 30000 });
  const out = await p.evaluate(async () => {
    const units = [...BC.courses.map(c => ['course', c]), ...PJ.list.map(x => ['project', x])].filter(([, u]) => ['html', 'web', 'sql'].includes(u.lang));
    const bad = []; let n = 0;
    for (const [kind, u] of units) for (const s of u.steps) {
      for (const [label, code] of [['solution', s.solution], ['starter', s.starter]]) {
        let r;
        if (u.lang === 'html') {
          const f = document.createElement('iframe'); f.setAttribute('sandbox', 'allow-same-origin'); f.style.width = '1024px'; document.body.appendChild(f);
          await new Promise(ok => { f.onload = ok; f.srcdoc = code; });
          r = await Judge.step(s, 'html', code, { doc: f.contentDocument, win: f.contentWindow }); f.remove();
        } else r = await Judge.step(s, u.lang, code);
        const all = r.checks.length && r.checks.every(x => x.ok);
        if (label === 'solution' && !all) bad.push(`FAIL ${kind} ${u.id}/${s.id}: ` + r.checks.filter(x => !x.ok).map(x => x.msg + (x.err ? ' [' + x.err + ']' : '')).join(' | ') + (r.stderr ? ' STDERR ' + r.stderr.slice(0, 200) : ''));
        if (label === 'starter' && all) bad.push(`STARTER PASSES ${kind} ${u.id}/${s.id}`);
      }
      n++;
    }
    return { n, bad };
  });
  console.log(`${out.n} browser steps checked`); out.bad.forEach(x => console.log(x));
  if (errs.length) console.log(`${errs.length} page errors (expected from starter code running in test frames)`);
  await b.close(); process.exit(out.bad.length ? 1 : 0);
})();
