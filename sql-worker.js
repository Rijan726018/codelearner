/* Runs learner SQL on SQLite (sql.js, WebAssembly) off the main thread. Every run starts from an empty in-memory database.
   Messages in:  {kind:"warm"} | {id, kind:"sql", code}
   Messages out: {type:"ready"} | {type:"fatal", error} | {id, type:"out", s:"o"|"e", text} | {id, type:"done", ms} */
let SQL = null, ready = null;

function boot() {
  if (!ready) ready = (async () => {
    importScripts("sqljs/sql-wasm.js");
    SQL = await initSqlJs({ locateFile: f => new URL("sqljs/" + f, self.location.href).href });
    postMessage({ type: "ready" });
  })();
  return ready;
}

function table(cols, rows) {
  const cells = rows.map(r => r.map(v => v === null ? "NULL" : v instanceof Uint8Array ? `<blob ${v.length} bytes>` : String(v)));
  const w = cols.map((c, i) => Math.max(c.length, ...cells.map(r => r[i].length)));
  const line = r => r.map((v, i) => v.padEnd(w[i])).join(" | ");
  return [line(cols), w.map(x => "-".repeat(x)).join("-+-"), ...cells.map(line), `(${rows.length} row${rows.length === 1 ? "" : "s"})`, ""].join("\n") + "\n";
}

self.onmessage = async (e) => {
  const { id, kind, code } = e.data;
  if (kind === "warm") { try { await boot(); } catch (err) { postMessage({ type: "fatal", error: String(err && err.message || err) }); } return; }
  const out = (s, text) => postMessage({ id, type: "out", s, text });
  try { await boot(); }
  catch (err) { out("e", "SQLite could not start in this browser: " + (err && err.message || err) + "\n"); postMessage({ id, type: "done", ms: 0 }); return; }
  const t0 = performance.now(); const db = new SQL.Database(); let stmt = null;
  try {
    for (stmt of db.iterateStatements(code)) {
      const sql = stmt.getSQL().trim(), cols = stmt.getColumnNames(), rows = [];
      while (stmt.step()) rows.push(stmt.get());
      const verb = (sql.replace(/^(--[^\n]*\n|\s)+/g, "").split(/\s+/)[0] || "").toUpperCase();
      if (cols.length) out("o", table(cols, rows));
      else if (["INSERT", "UPDATE", "DELETE"].includes(verb)) { const n = db.getRowsModified(); out("o", `${n} row${n === 1 ? "" : "s"} affected\n`); }
      stmt.free(); stmt = null;
    }
  } catch (err) {
    const where = stmt ? "\n  in: " + stmt.getSQL().trim().slice(0, 120) : "";
    out("e", "Error: " + (err && err.message || err) + where + "\n");
  } finally {
    try { stmt && stmt.free(); } catch (_) {}
    db.close();
  }
  postMessage({ id, type: "done", ms: Math.round(performance.now() - t0) });
};
