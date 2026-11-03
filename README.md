# CodeBay

Learn to code from your first line to world-class engineering, then auction the projects you build. Everything runs in the browser, and it is live at **https://codebay.org/**. (This site used to be called CodeLearner; the repository keeps that name. See [Hosting and the codebay.org address](#hosting-and-the-codebayorg-address).) It combines five ways of learning and a Code Auction:

| Section | Inspired by | What's in it |
|---|---|---|
| **Bootcamp** | freeCodeCamp | 17 step-by-step courses, 198 auto-checked steps, in five tracks. **Web foundations:** *Build Your First Web Page*, *CSS Layout Lab*, *Accessible HTML*, *JavaScript & the DOM*. **Python:** *Python from Zero*, *Python Strings & Text*, *Python Functions in Depth*, *Python Data & Objects*, *Python Errors & Testing*. **JavaScript:** *JavaScript from Zero*, *JavaScript Array Methods*, *Regular Expressions*, *Async JavaScript*. **Data & SQL:** *SQL from Zero*, *SQL Analytics*, *SQL Data Modeling*. **Computer science:** *Algorithms with Python* |
| **Build & Learn** | project tutorials | 19 guided projects, 148 checked steps grouped into milestones: pick a project (a to-do app, calculator, quiz game, expense tracker, focus timer, memory game, habit tracker, Hangman, text adventure, text analyzer, bank system, maze solver, tic-tac-toe AI, Markdown converter, shopping cart, library database, music streaming analytics and more), see the finished thing running, then build it one step at a time with the concept, an example, the task, checks, hints and links to the matching core lessons. Every project page also has a hand-picked video to watch first, why the project matters, its common mistakes and key takeaways |
| **Learn: the 10,000-Hour Map** | university curricula | 9 stages, 215 daily lessons and 1,171 questions, from Base Camp to distributed systems, with module exams, test-outs and spaced repetition. Each lesson runs in a research-backed order: a warm-up guess, the reading with key terms, a hand-picked short video followed by a recall prompt, a worked example you predict before running, common mistakes, a try-it task, explain it back, questions answered with a confidence rating, and key takeaways |
| **Career Paths** | roadmap.sh | 26 phased roadmaps (468 topics) for Frontend, Backend, Full-Stack, Design, AI, ML, Data Science/Engineering/Analysis, Security, DevOps, Cloud, SRE, iOS, Android, Games, Systems, Embedded, Robotics, Blockchain, Graphics/XR, Quantum, QA, Databases and Architecture, plus a path-finder quiz |
| **Problems** | LeetCode | 144 problems across 15 patterns, judged in the browser in Python or JavaScript against hidden tests, with hints, common mistakes for every problem, pattern guides with a video for each pattern, a key takeaway in each editorial, and a link to find a walkthrough |

Around them:
- **Code Auction**: list one of your cloud projects from the Editor, with a title, description, starting price and an end time (1 to 7 days). Others bid in US dollars; each bid must beat the last by at least $1, the seller can't bid on their own lot, and nobody can bid after the end. Buyers see the file names and sizes, not the code. CodeBay doesn't take payment yet: when a lot ends with a bid, the seller and the winner get a private deal thread to agree how to pay, and the seller releases the files once paid. The winner then copies them into their own projects. See [Code Auction](#code-auction).
- **Editor**: your own multi-file projects in Python (with importable modules), JavaScript, SQL or HTML/CSS/JS with a live preview and console. It autosaves, downloads files, and any Build & Learn project can be copied in to keep building.
- **Practice clock**: counts active practice time per section and time you log by hand. It shows your hours toward 10,000, a daily goal, a year heatmap and a projected finish date.
- **Sign in with Google**: progress, review cards, practice hours and editor projects sync to your account (see [Accounts and cloud sync](#accounts-and-cloud-sync)).
- **Confidence ratings**: every answer is checked with *Guessing*, *Fairly sure* or *Certain*. Confident misses are flagged, lucky guesses come back tomorrow instead of moving up a box, and your profile shows how often each rating is right. The Method page explains the research behind each lesson step, with sources.
- **Rewards**: coins for every lesson, exam, problem, step, project, course, career path, badge, level, practice day and streak milestone, worked out from real progress like XP so nothing pays twice. Three daily and three weekly challenges (the same for everyone on a given date) pay extra, with a bonus for clearing them all. Coins buy streak freezes (used automatically when you miss a day), accent colours and titles; nothing educational costs coins. An opt-in leaderboard ranks signed-in learners by progress: XP earned this week (the default), all-time XP, current streaks and coins earned, plus last week's final standings. It shows your exact rank among everyone, who you need to pass and by how much, who is chasing you, how far you've moved since yesterday, and your league for the week (Bronze, Silver, Gold, Platinum, Diamond, Legend). Each week's top three win 500 / 300 / 150 coins. Only a chosen display name and numbers are shown.
- A dashboard with "continue" cards, today's challenges and a problem of the day, plus XP, levels, ranks and 38 badges.
- A Ctrl/⌘ K search across everything, light and dark themes, and backup/restore of progress.

## Hosting and the codebay.org address

GitHub Pages builds and hosts the files (`.github/workflows/pages.yml`, on every push to `main`). People reach them at **codebay.org**:
- The codebay.org Vercel project (repository `Rijan726018/codebay`) has a `vercel.json` rewrite that fetches every path from the GitHub Pages copy. It's a rewrite, not a redirect, so the address bar stays on codebay.org.
- A short script at the top of `index.html` moves anyone who opens the old `rijan726018.github.io/codelearner` address to codebay.org. It first checks that `https://codebay.org/site.json` answers as this site, so it never sends people to a broken address.
- Browsers keep saved progress per address. The move carries this browser's `tenk2-*` and `cl-*` keys in the URL fragment, which is never sent to a server, and codebay.org writes them only where it has nothing of its own yet. Above about 1.5 MB it shows a notice instead, pointing to sign-in or Profile → backup.
- Signing in is per address too. After the move, people sign in once more on codebay.org, which only works once `codebay.org` is in Firebase's authorized domains (step 3 below).

Search engines get `<link rel="canonical" href="https://codebay.org/">`, Open Graph tags and `og-image.png` for link previews, a WebSite JSON-LD block, `robots.txt` and `sitemap.xml`.

To get into Google, add `codebay.org` as a **Domain** property in [Google Search Console](https://search.google.com/search-console), prove you own it with the TXT record it gives you (at your DNS provider; Vercel's **Domains → codebay.org → DNS Records** if Vercel runs the DNS), then submit `https://codebay.org/sitemap.xml` under **Sitemaps** and request indexing of the home page under **URL inspection**. Routes are hash URLs (`#/problems`), which search engines treat as the one home page.

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
- **Leaderboard:** people who join it get an entry in `boards/all/entries/{uid}` and `boards/w-YYYY-MM-DD/entries/{uid}` (the week starting Monday) holding a display name, title, XP, level, coins, streak and this week's XP. Any signed-in person can read the boards; only the owner can write or delete their entry, and the rules check every field's type and range. Leaving the board deletes the entries. Your rank comes from a Firestore count query and your neighbours from range queries on the same field, both covered by Firestore's automatic single-field indexes, so no extra index setup is needed.
- **Signing in:** progress from that browser is merged into the account, so nothing is lost. Maps are unioned, scores, reps and seconds keep the larger value, and editor projects keep the newest copy.
- **Signing out:** the browser's copy is cleared, so the next person starts fresh.

To switch it on (about 10 minutes, free on the Spark plan):

1. In the [Firebase console](https://console.firebase.google.com/), create a project. Google Analytics is optional.
2. Turn on Google sign-in: **Build → Authentication → Get started → Sign-in method → Google → Enable**, then choose a support email and save.
3. Allow the site's address: **Authentication → Settings → Authorized domains → Add domain**, and add `codebay.org` (and `www.codebay.org` if you use it) plus `rijan726018.github.io`. `localhost` is already listed.
4. Create the database: **Build → Firestore Database → Create database**. Pick a location near your users and start in **production mode**.
5. Paste in the access rules: on **Firestore → Rules**, replace the contents with `firestore.rules` from this repository, then **Publish**.
6. Get the web config: **Project settings (gear) → General → Your apps → Web (`</>`)**. Register an app (no hosting needed) and copy the `firebaseConfig` values into `firebase-config.js` as `window.CL_FIREBASE = {...}`.
7. Commit and push. GitHub Pages redeploys, and the **Sign in** button appears in the header.

The web config values identify the project but aren't secrets; the rules decide who can read what.

**Already set up before the leaderboard or the Code Auction existed?** Repeat step 5: paste the current `firestore.rules` into **Firestore → Rules** and **Publish**. Until then the leaderboard tab says it isn't switched on, and everything else, coins and challenges included, keeps working. Scores are reported by each person's browser, so a determined person could post a fake score; the rules only bound the numbers. Treat the board as friendly motivation, not a contest with prizes.

## Code Auction

Each lot is `auctions/{id}`, readable by anyone, with three subcollections:

| Path | Holds | Who can read | Who can write |
|---|---|---|---|
| `auctions/{id}` | title, description, language, file names and sizes, starting price, end time, top bid, top bidder, bid count, status, released | anyone | the seller creates it; bidders update only the top-bid fields; the seller can withdraw it before the first bid and release the files after the end |
| `bids/{n}` | bidder, public name, amount, time | anyone | the bidder, in the same write as the lot update, with `n` = the new bid count |
| `vault/files` | the project files as JSON | the seller; the winner once released | the seller, once, together with the lot |
| `deal/{msg}` | messages between seller and winner | those two, after the end | those two, after the end |

`firestore.rules` checks every bid: signed in, not the seller, not already the top bidder, before the end, at least the starting price for the first bid and at least $1 over the last one after that, and matched by a bid record with the same amount. Lots can't be deleted. `tools/test_auction_rules.mjs` runs 43 checks against the Firestore emulator.

The lists use single-field queries on `endsAt` and `sellerUid`, covered by Firestore's automatic indexes. Each person's public trading name and the lots they bid on live in their progress doc (`P.auction`).

Not built yet: payments (Stripe Connect with escrow would replace the deal thread), extending the end time when a bid lands in the last minutes, reporting a lot, and email notifications when you're outbid or win. Until payment is built in, a winner can fail to pay and a seller can fail to release. The deal thread and the bid history are the only record.

## Layout

| Path | What it is |
|---|---|
| `index.html` | Page shell and the whole design system (CSS): a black-and-white theme, with green and red kept only for passed and failed |
| `ui.js` | Icons, theme, toasts, confetti, search palette, XP/levels/badges, Home and Profile views |
| `app.js` | Routing, persistence, Dashboard, Learn map, lessons, exams, review, practice, projects, method; quiz engine; spaced repetition |
| `runner.js` | Code editor widget (CodeMirror 5), runners and drafts |
| `clock.js` | Practice clock: active-time tracking, time logged by hand, the clock view and the Today card |
| `editor.js` | The Editor: multi-file projects, running and previews, autosave, and merging with the account |
| `cloud.js`, `firebase-config.js`, `firestore.rules` | Sign in with Google and cloud sync through Firebase |
| `auction.js` | The Code Auction: browse lots, a lot page with live bids, list a project, the deal thread |
| `rewards.js` | Coins, daily and weekly challenges, streak freezes, the rewards shop and the leaderboard |
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
python3 tools/merge_lessons.py                                       # merges lesson videos and why/terms/mistakes/takeaways into data/sN.json
python3 tools/merge_extras.py                                        # merges project and pattern videos, project and problem mistakes and takeaways
python3 tools/validate.py data/s*.json                               # core curriculum schema
```

Core curriculum content follows `tools/SCHEMA.md`. Each lesson's videos are listed in `tools/lesson_videos.tsv` and its why/terms/mistakes/takeaways live in `tools/lesson_extra/sN.py`; edit those, then run `merge_lessons.py`. Projects and problems work the same way: `tools/project_videos.tsv`, `tools/project_extra.py`, `tools/problem_videos.tsv` (one video per pattern) and `tools/problem_extra.py`, merged by `merge_extras.py`; `build_projects.py` and `build_problems.py` apply them too, so a rebuild keeps them. Videos load only when played, from youtube-nocookie.com.

## Third-party code

- [Pyodide](https://github.com/pyodide/pyodide) 0.26.4, Mozilla Public License 2.0. Files in `pyodide/` are unmodified, apart from the base64 encoding of the standard library zip.
- [sql.js](https://github.com/sql-js/sql.js) 1.10.3, MIT License.
- [CodeMirror 5](https://codemirror.net/5/) 5.65.16, MIT License, loaded from cdnjs; its base CSS is inlined in `index.html`.
- Fonts: the system font (San Francisco on Apple devices), with Inter and JetBrains Mono from Google Fonts (SIL Open Font License) everywhere else.
