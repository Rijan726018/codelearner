# CodeLearner

Learn to code from your first line to world-class engineering, in one place, entirely in the browser. CodeLearner is the free coding school that is part of [CodeBay](https://codebay.org/), and it is live at https://rijan726018.github.io/codelearner/. It combines five ways of learning:

| Section | Inspired by | What's in it |
|---|---|---|
| **Bootcamp** | freeCodeCamp | 17 step-by-step courses, 198 auto-checked steps, in five tracks. **Web foundations:** *Build Your First Web Page*, *CSS Layout Lab*, *Accessible HTML*, *JavaScript & the DOM*. **Python:** *Python from Zero*, *Python Strings & Text*, *Python Functions in Depth*, *Python Data & Objects*, *Python Errors & Testing*. **JavaScript:** *JavaScript from Zero*, *JavaScript Array Methods*, *Regular Expressions*, *Async JavaScript*. **Data & SQL:** *SQL from Zero*, *SQL Analytics*, *SQL Data Modeling*. **Computer science:** *Algorithms with Python* |
| **Build & Learn** | project tutorials | 19 guided projects, 148 checked steps grouped into milestones: pick a project (a to-do app, calculator, quiz game, expense tracker, focus timer, memory game, habit tracker, Hangman, text adventure, text analyzer, bank system, maze solver, tic-tac-toe AI, Markdown converter, shopping cart, library database, music streaming analytics and more), see the finished thing running, then build it one step at a time with the concept, an example, the task, checks, hints and links to the matching core lessons |
| **Learn: the 10,000-Hour Map** | university curricula | 9 stages, 215 daily lessons and 1,171 questions, from Base Camp to distributed systems, with module exams, test-outs and spaced repetition |
| **Career Paths** | roadmap.sh | 26 phased roadmaps (468 topics) for Frontend, Backend, Full-Stack, Design, AI, ML, Data Science/Engineering/Analysis, Security, DevOps, Cloud, SRE, iOS, Android, Games, Systems, Embedded, Robotics, Blockchain, Graphics/XR, Quantum, QA, Databases and Architecture, plus a path-finder quiz |
| **Problems** | LeetCode | 144 problems across 15 patterns, judged in the browser in Python or JavaScript against hidden tests, with hints, pattern guides and editorials |

Around them:
- **Editor**: your own multi-file projects in Python (with importable modules), JavaScript, SQL or HTML/CSS/JS with a live preview and console. It autosaves, downloads files, and any Build & Learn project can be copied in to keep building.
- **Practice clock**: counts active practice time per section and time you log by hand. It shows your hours toward 10,000, a daily goal, a year heatmap and a projected finish date.
- **Sign in with Google**: progress, review cards, practice hours and editor projects sync to your account (see [Accounts and cloud sync](#accounts-and-cloud-sync)).
- A dashboard with "continue" cards and a problem of the day, plus XP, levels, ranks and 28 badges.
- A Ctrl/⌘ K search across everything, light and dark themes, and backup/restore of progress.

## Run it locally

No build step. Serve the folder over HTTP; web workers and WebAssembly don't run from `file://`.

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000. Progress saves in your browser's localStorage. URLs are hash routes (`#/problem/two-sum`, `#/path/ai-engineer`), so the back button and deep links work.

## Where it runs

The app was built to run as a private Claude artifact. There it saves progress and code drafts to your account and offers a hint-only AI tutor, through the artifact runtime's `db`, `user` and `sample` capabilities. Run anywhere else, for example locally or on GitHub Pages, it falls back to localStorage and hides the tutor.

To republish it as an artifact, remove the first three lines of `index.html` (doctype, charset and viewport), because the artifact host adds its own.

## Accounts and cloud sync

"Sign in with Google" uses [Firebase](https://firebase.google.com/): Authentication for the Google sign-in, and Firestore for the data. Until `firebase-config.js` holds a config, the sign-in button is hidden and everything saves in the browser.

How it works:
- **Storage:** each person's data lives under `users/{uid}/docs/{docId}`. The docs are progress (`v2progress`), review cards (`v2srs`), code drafts, and one doc per editor project plus an index (`ws-index`). Each is stored as a JSON string.
- **Access:** `firestore.rules` lets a signed-in person read and write only their own documents.
- **Signing in:** progress from that browser is merged into the account, so nothing is lost. Maps are unioned, scores, reps and seconds keep the larger value, and editor projects keep the newest copy.
- **Signing out:** the browser's copy is cleared, so the next person starts fresh.

To switch it on (about 10 minutes, free on the Spark plan):

1. In the [Firebase console](https://console.firebase.google.com/), create a project. Google Analytics is optional.
2. Turn on Google sign-in: **Build → Authentication → Get started → Sign-in method → Google → Enable**, then choose a support email and save.
3. Allow the site's address: **Authentication → Settings → Authorized domains → Add domain**, and add `rijan726018.github.io`. `localhost` is already listed.
4. Create the database: **Build → Firestore Database → Create database**. Pick a location near your users and start in **production mode**.
5. Paste in the access rules: on **Firestore → Rules**, replace the contents with `firestore.rules` from this repository, then **Publish**.
6. Get the web config: **Project settings (gear) → General → Your apps → Web (`</>`)**. Register an app (no hosting needed) and copy the `firebaseConfig` values into `firebase-config.js` as `window.CL_FIREBASE = {...}`.
7. Commit and push. GitHub Pages redeploys, and the **Sign in** button appears in the header.

The web config values identify the project but aren't secrets; the rules decide who can read what.

## Layout

| Path | What it is |
|---|---|
| `index.html` | Page shell and the whole design system (CSS) |
| `ui.js` | Icons, theme, toasts, confetti, search palette, XP/levels/badges, Home and Profile views |
| `app.js` | Routing, persistence, Dashboard, Learn map, lessons, exams, review, practice, projects, method; quiz engine; spaced repetition |
| `runner.js` | Code editor widget (CodeMirror 5), runners and drafts |
| `clock.js` | Practice clock: active-time tracking, time logged by hand, the clock view and the Today card |
| `editor.js` | The Editor: multi-file projects, running and previews, autosave, and merging with the account |
| `cloud.js`, `firebase-config.js`, `firestore.rules` | Sign in with Google and cloud sync through Firebase |
| `judge.js` | Test harnesses for problems (Python and JavaScript) and checkers for bootcamp and project steps (stdout, source, DOM/CSS, SQL results, and web apps driven in a sandboxed frame) |
| `problems.js`, `bootcamp.js`, `paths.js` | The Problems, Bootcamp and Build & Learn, and Career Paths views |
| `py-worker.js`, `sql-worker.js` | Run Python (Pyodide) and SQL (sql.js) off the main thread |
| `data/s0.json` … `data/s8.json`, `data/research.json` | Core curriculum content and the learning-science summary |
| `data/problems.json`, `data/bootcamp.json`, `data/projects.json`, `data/paths/` | Generated content (see below) |
| `tools/` | Content sources, builders and validators |
| `pyodide/`, `sqljs/` | Pyodide 0.26.4 and sql.js 1.10.3 runtimes |

## Editing content

Problems, bootcamp courses, guided projects and career paths are written as Python source in `tools/` (`problems_src.py`, `problems_more*.py`, `bootcamp_src.py`, `bootcamp_more*.py`, `projects_src/`) and built into JSON. Every expected output is computed from reference solutions, and the checkers run every reference solution through the real judge code (and check that every step's starter code fails).

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
