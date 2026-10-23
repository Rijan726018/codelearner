# CodeLearner

Learn to code from your first line to world-class engineering, in one place, entirely in the browser. CodeLearner is the free coding school that is part of [CodeBay](https://codebay.org/), and it is live at https://rijan726018.github.io/codelearner/. It combines five ways of learning:

| Section | Inspired by | What's in it |
|---|---|---|
| **Bootcamp** | freeCodeCamp | 9 step-by-step courses, 120 auto-checked steps: *Build Your First Web Page* (HTML/CSS with live preview), *Python from Zero*, *JavaScript from Zero*, *SQL from Zero*, *CSS Layout Lab*, *JavaScript & the DOM*, *Python Data & Objects*, *SQL Analytics* (joins, CTEs, window functions) and *Algorithms with Python* |
| **Build & Learn** | project tutorials | 19 guided projects, 148 checked steps grouped into milestones: pick a project (a to-do app, calculator, quiz game, expense tracker, focus timer, memory game, habit tracker, Hangman, text adventure, text analyzer, bank system, maze solver, tic-tac-toe AI, Markdown converter, shopping cart, library database, music streaming analytics and more), see the finished thing running, then build it one step at a time with the concept, an example, the task, checks, hints and links to the matching core lessons |
| **Learn: the 10,000-Hour Map** | university curricula | 9 stages, 215 daily lessons and 1,171 questions, from Base Camp to distributed systems, with module exams, test-outs and spaced repetition |
| **Career Paths** | roadmap.sh | 26 phased roadmaps (468 topics) for Frontend, Backend, Full-Stack, Design, AI, ML, Data Science/Engineering/Analysis, Security, DevOps, Cloud, SRE, iOS, Android, Games, Systems, Embedded, Robotics, Blockchain, Graphics/XR, Quantum, QA, Databases and Architecture, plus a path-finder quiz |
| **Problems** | LeetCode | 144 problems across 15 patterns, judged in the browser in Python or JavaScript against hidden tests, with hints, pattern guides and editorials |

Around them: a dashboard with "continue" cards and a problem of the day, XP, levels, ranks and 24 badges, a Ctrl/⌘ K search across everything, light and dark themes, a playground, and backup/restore of progress.

## Run it locally

No build step. Serve the folder over HTTP; web workers and WebAssembly don't run from `file://`.

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000. Progress saves in your browser's localStorage. URLs are hash routes (`#/problem/two-sum`, `#/path/ai-engineer`), so the back button and deep links work.

## Where it runs

The app was built to run as a private Claude artifact. There it saves progress and code drafts to your account and offers a hint-only AI tutor, through the artifact runtime's `db`, `user` and `sample` capabilities. Run anywhere else, for example locally or on GitHub Pages, it falls back to localStorage and hides the tutor.

To republish it as an artifact, remove the first three lines of `index.html` (doctype, charset and viewport), because the artifact host adds its own.

## Layout

| Path | What it is |
|---|---|
| `index.html` | Page shell and the whole design system (CSS) |
| `ui.js` | Icons, theme, toasts, confetti, search palette, XP/levels/badges, Home and Profile views |
| `app.js` | Routing, persistence, Dashboard, Learn map, lessons, exams, review, practice, projects, method; quiz engine; spaced repetition |
| `runner.js` | Code editor (CodeMirror 5), runners, drafts, Playground |
| `judge.js` | Test harnesses for problems (Python and JavaScript) and checkers for bootcamp and project steps (stdout, source, DOM/CSS, SQL results, and web apps driven in a sandboxed frame) |
| `problems.js`, `bootcamp.js`, `paths.js` | The Problems, Bootcamp and Build & Learn, and Career Paths views |
| `py-worker.js`, `sql-worker.js` | Run Python (Pyodide) and SQL (sql.js) off the main thread |
| `data/s0.json` … `data/s8.json`, `data/research.json` | Core curriculum content and the learning-science summary |
| `data/problems.json`, `data/bootcamp.json`, `data/projects.json`, `data/paths/` | Generated content (see below) |
| `tools/` | Content sources, builders and validators |
| `pyodide/`, `sqljs/` | Pyodide 0.26.4 and sql.js 1.10.3 runtimes |

## Editing content

Problems, bootcamp courses, guided projects and career paths are written as Python source in `tools/` (`problems_src.py`, `problems_more*.py`, `bootcamp_src.py`, `bootcamp_more.py`, `projects_src/`) and built into JSON. Every expected output is computed from reference solutions, and the checkers run every reference solution through the real judge code (and check that every step's starter code fails).

```bash
python3 tools/build_problems.py && node tools/check_problems.mjs     # 144 problems × Python + JavaScript
python3 tools/build_bootcamp.py && python3 tools/build_projects.py
node tools/check_bootcamp.mjs                                         # Python/JS steps of courses and projects
python3 -m http.server 8765 & NODE_PATH=$(npm root -g) node tools/check_in_browser.cjs   # HTML, web-app and SQL steps, in Chromium
python3 tools/build_paths.py                                         # validates ids, icons, links and core-module references
python3 tools/validate.py data/s*.json                               # core curriculum schema
```

Core curriculum content follows `tools/SCHEMA.md`.

## Third-party code

- [Pyodide](https://github.com/pyodide/pyodide) 0.26.4, Mozilla Public License 2.0. Files in `pyodide/` are unmodified, apart from the base64 encoding of the standard library zip.
- [sql.js](https://github.com/sql-js/sql.js) 1.10.3, MIT License.
- [CodeMirror 5](https://codemirror.net/5/) 5.65.16, MIT License, loaded from cdnjs; its base CSS is inlined in `index.html`.
- Fonts: Bricolage Grotesque, IBM Plex Sans and JetBrains Mono from Google Fonts (SIL Open Font License).
