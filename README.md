# CodeLearner: The 10,000-Hour Map

A self-paced programming curriculum that takes you from your first line of code to world-class engineering, built on the learning-science evidence for retrieval practice, spacing, mastery learning and worked examples.

- **9 stages, 215 daily lessons, 1,171 questions**, from Base Camp (terminal, Git) through Python, algorithms, systems, full-stack, engineering craft and distributed systems, then a deep-specialty track, up to Summit.
- **Every lesson:** an objective, a short explanation, a diagram or step-through code trace, a worked example, a try-it task, an "explain it back" box and 3–4 check-yourself questions at three levels (Recall, Apply, Analyze).
- **Runnable code in the browser:** Python 3.12 (Pyodide), JavaScript (sandboxed worker) and SQL (SQLite via sql.js), in worked examples, a per-lesson scratchpad, after questions, and in a Playground.
- **Module exams** you need 80% to pass, mixing in questions from earlier modules, plus **Test out** to skip what you already know.
- **Spaced repetition:** every question you answer becomes a review card on a 1 → 3 → 7 → 14 → 30 → 60 → 120 day schedule.
- **Projects** with milestones for every module, a **level-based practice** mode, and a **Method** page summarising the research, with sources.

## Run it locally

No build step. Serve the folder over HTTP; web workers and WebAssembly don't run from `file://`.

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000. Progress saves in your browser's localStorage.

## Where it runs

The app was built to run as a private Claude artifact. There it saves progress and code drafts to your account and offers a hint-only AI tutor, through the artifact runtime's `db`, `user` and `sample` capabilities. Run anywhere else, for example locally or on GitHub Pages, it falls back to localStorage and hides the tutor.

To republish it as an artifact, remove the first three lines of `index.html` (doctype, charset and viewport), because the artifact host adds its own.

## Layout

| Path | What it is |
|---|---|
| `index.html` | Page shell and all styles |
| `app.js` | Views: Today, Map, Lesson, Exam, Review, Practice, Projects, Method; quiz engine; spaced repetition; persistence |
| `runner.js` | Code editor (CodeMirror 5), runners, drafts, Playground |
| `py-worker.js` | Runs Python in Pyodide off the main thread |
| `sql-worker.js` | Runs SQL in sql.js off the main thread |
| `data/s0.json` … `data/s8.json` | Stage content: modules, lessons, questions, projects, exams |
| `data/research.json` | Learning-science principles, protocol, review intervals, sources |
| `tools/SCHEMA.md` | Content schema the stage files follow |
| `tools/validate.py` | Schema checker: `python3 tools/validate.py data/s*.json` |
| `pyodide/` | Pyodide 0.26.4 runtime. The standard library is stored base64-encoded in `python_stdlib.b64.txt`, because artifact hosting doesn't serve `.zip` files. |
| `sqljs/` | sql.js 1.10.3 (SQLite compiled to WebAssembly) |

## Third-party code

- [Pyodide](https://github.com/pyodide/pyodide) 0.26.4, Mozilla Public License 2.0. Files in `pyodide/` are unmodified, apart from the base64 encoding of the standard library zip.
- [sql.js](https://github.com/sql-js/sql.js) 1.10.3, MIT License.
- [CodeMirror 5](https://codemirror.net/5/) 5.65.16, MIT License, loaded from cdnjs; its base CSS is inlined in `index.html`.
- Fonts: Bricolage Grotesque, IBM Plex Sans and JetBrains Mono from Google Fonts (SIL Open Font License).
