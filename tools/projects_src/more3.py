from _lib import *

def T(js, msg, do=None, **k):
    d = dict(js=js, msg=msg, **k)
    if do: d["do"] = do
    return d

def lines(block):
    return block.strip("\n").split("\n")

# =============================================================================================== FOCUS TIMER (web)
P = Page("Focus Timer")
S = []
BLANK = P.render()
P.body = ['  <h1>Focus Timer</h1>', '  <p id="time">25:00</p>', '  <button id="start">Start</button>', '  <button id="reset">Reset</button>']
S.append(step("pt1", "The timer's HTML",
  ["A **Pomodoro** timer splits work into 25-minute focus sessions with short breaks in between. It's a great first app with time in it: a display, two buttons and a bit of logic.",
   "Start with the HTML. The time is plain text in a `<p>` for now; JavaScript will keep it up to date."],
  "Add an `<h1>` saying `Focus Timer`, a `<p id=\"time\">25:00</p>`, and two buttons: `#start` (Start) and `#reset` (Reset).",
  P.render(), [T("_text('h1')==='Focus Timer'", "The `h1` says Focus Timer."), T("_text('#time')==='25:00'", "`#time` shows 25:00."),
               T("_text('#start')==='Start' && _text('#reset')==='Reset'", "There are Start and Reset buttons.")],
  starter=BLANK, core="s4m1"))
P.body = ['  <main class="timer">', '    <h1>Focus Timer</h1>', '    <p id="time">25:00</p>', '    <div class="controls">', '      <button id="start">Start</button>', '      <button id="reset">Reset</button>', '    </div>', '  </main>']
P.css = lines('''
    [hidden] { display: none !important; }
    body { font-family: system-ui, sans-serif; background: #1d1b3a; color: #f4f2ff; margin: 0; padding: 48px 16px; }
    .timer { max-width: 380px; margin: 0 auto; text-align: center; background: #2a2752; padding: 28px; border-radius: 24px; }
    #time { font-size: 72px; font-weight: 700; font-variant-numeric: tabular-nums; margin: 16px 0; }
    .controls { display: flex; gap: 10px; justify-content: center; }
    button { padding: 10px 18px; border: 0; border-radius: 999px; background: #f97316; color: #1d1b3a; font: inherit; font-weight: 600; cursor: pointer; }
    #reset { background: transparent; color: #f4f2ff; border: 1px solid #6b67a8; }''')
S.append(step("pt2", "Big, calm and centred",
  ["A timer is read from across the room, so the digits should be huge. `font-variant-numeric: tabular-nums` gives every digit the same width, so the time doesn't wobble as it counts down.",
   "Wrap everything in a `main.timer` card, centre the text, and put the buttons side by side with flexbox."],
  "Wrap the page in `<main class=\"timer\">` and the buttons in `<div class=\"controls\">`. Make `#time` at least 48px with tabular numbers, centre the card with a `max-width`, and lay the controls out with `display: flex`.",
  P.render(), [T("!!$('main.timer #time') && !!$('.controls #start')", "The timer and controls are inside `main.timer`."), T("parseFloat(getComputedStyle($('#time')).fontSize)>=48", "`#time` is at least 48px."),
               T("getComputedStyle($('#time')).fontVariantNumeric.includes('tabular-nums')", "The digits use `tabular-nums`."), T("getComputedStyle($('.controls')).display==='flex'", "The controls use flexbox.")]))
P.js = lines('''
    const timeEl = document.querySelector("#time");
    const startBtn = document.querySelector("#start");
    let remaining = 25 * 60;

    function format(seconds) {
      const m = Math.floor(seconds / 60);
      const s = seconds % 60;
      return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
    }

    function render() {
      timeEl.textContent = format(remaining);
    }

    render();''')
S.append(step("pt3", "Seconds in, minutes out",
  ["Keep time as one number: the seconds `remaining`. Everything on screen is computed from it, which is much simpler than juggling minutes and seconds separately.",
   "`Math.floor(seconds / 60)` gives the minutes and `seconds % 60` the leftover seconds. `String(5).padStart(2, \"0\")` is `\"05\"`."],
  "Add a `<script>`. Keep `let remaining = 25 * 60;`. Write `format(seconds)` returning `MM:SS`, and `render()` that shows `format(remaining)` in `#time`. Call `render()` once.",
  P.render(), [T("format(65)==='01:05' && format(0)==='00:00' && format(1500)==='25:00'", "`format` turns seconds into MM:SS."),
               T("remaining===1500 && _text('#time')==='25:00'", "It starts at 25:00."), T("_text('#time')==='01:01'", "`render()` shows whatever `remaining` holds.", do="remaining = 61; render();")],
  ref=("MDN: String.prototype.padStart", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/padStart")))
P.sub_js('    let remaining = 25 * 60;', '    let remaining = 25 * 60;\n    let timer = null;')
P.sub_js('    render();', '''    function tick() {
      remaining -= 1;
      if (remaining <= 0) {
        remaining = 0;
        stop();
      }
      render();
    }

    function start() {
      timer = setInterval(tick, 1000);
      startBtn.textContent = "Pause";
    }

    function stop() {
      clearInterval(timer);
      timer = null;
      startBtn.textContent = "Start";
    }

    startBtn.addEventListener("click", () => (timer ? stop() : start()));

    render();''')
S.append(step("pt4", "Tick, start and pause",
  ["`setInterval(tick, 1000)` calls `tick` every second and returns an id; `clearInterval(id)` stops it. Keep the id in `timer`: `null` means *not running*, which also tells the button what to do.",
   "`tick()` does one second of work. Keeping it a separate function means you can test it without waiting a whole second."],
  "Write `tick()` (one second less, stopping at 0), `start()` and `stop()`. The Start button starts the timer and becomes Pause; pressing Pause stops it and it says Start again.",
  P.render(), [T("_text('#time')==='24:59'", "`tick()` counts down one second.", do="tick();"),
               T("timer!==null && _text('#start')==='Pause'", "Start runs the timer and the button says Pause.", do="_click('#start');"),
               T("timer===null && _text('#start')==='Start'", "Pause stops it again.", do="_click('#start'); _click('#start');"),
               T("remaining===0 && _text('#time')==='00:00' && timer===null", "At zero the timer stops.", do="_click('#start'); remaining = 1; tick();")],
  ref=("MDN: setInterval", "https://developer.mozilla.org/en-US/docs/Web/API/setInterval")))
P.sub_js('    startBtn.addEventListener("click", () => (timer ? stop() : start()));', '''    startBtn.addEventListener("click", () => (timer ? stop() : start()));
    document.querySelector("#reset").addEventListener("click", () => {
      stop();
      remaining = 25 * 60;
      render();
    });''')
S.append(step("pt5", "Reset",
  ["Reset should always leave the app in a known state: stopped, with a full session. Reuse `stop()` instead of repeating its three lines."],
  "Clicking `#reset` stops the timer, puts `remaining` back to 25 minutes and re-renders.",
  P.render(), [T("_text('#time')==='25:00' && timer===null && _text('#start')==='Start'", "Reset stops the timer and shows 25:00.", do="_click('#start'); tick(); tick(); _click('#reset');"),
               T("remaining===1500", "`remaining` is back to 1500.", do="remaining = 7; _click('#reset');")]))
P.sub_body('    <h1>Focus Timer</h1>', '''    <h1>Focus Timer</h1>
    <div class="modes">
      <button data-mode="focus" class="active">Focus</button>
      <button data-mode="short">Short break</button>
      <button data-mode="long">Long break</button>
    </div>''')
P.css += lines('''
    .modes { display: flex; gap: 6px; justify-content: center; }
    .modes button { background: transparent; color: #c9c5f5; padding: 6px 12px; }
    .modes button.active { background: #3d3975; color: #fff; }''')
P.sub_js('    let remaining = 25 * 60;', '''    const LENGTHS = { focus: 25 * 60, short: 5 * 60, long: 15 * 60 };
    const modeButtons = document.querySelectorAll("[data-mode]");
    let mode = "focus";
    let remaining = LENGTHS.focus;''')
P.sub_js('      timeEl.textContent = format(remaining);', '      timeEl.textContent = format(remaining);\n      document.title = `${format(remaining)} · Focus Timer`;')
P.sub_js('''      stop();
      remaining = 25 * 60;
      render();
    });''', '''      stop();
      remaining = LENGTHS[mode];
      render();
    });

    function setMode(newMode) {
      stop();
      mode = newMode;
      remaining = LENGTHS[mode];
      for (const b of modeButtons) b.classList.toggle("active", b.dataset.mode === mode);
      render();
    }

    for (const b of modeButtons) b.addEventListener("click", () => setMode(b.dataset.mode));''')
S.append(step("pt6", "Focus, short break, long break",
  ["Three modes with three lengths is data, not three copies of code: `const LENGTHS = { focus: 1500, short: 300, long: 900 }` and one `setMode(mode)` that looks the length up.",
   "Show the time in the tab title too (`document.title`), so you can see it while working in another tab."],
  "Add three `data-mode` buttons (focus, short, long). Write `setMode(mode)` that stops the timer, sets `remaining` from `LENGTHS`, moves the `active` class and re-renders. Reset uses the current mode's length. Put the time in `document.title`.",
  P.render(), [T("_text('#time')==='05:00' && $('[data-mode=short]').classList.contains('active') && $$('.modes .active').length===1", "Short break shows 05:00 and is highlighted.", do="_click('[data-mode=short]');"),
               T("_text('#time')==='15:00' && mode==='long'", "Reset keeps the current mode's length.", do="_click('[data-mode=long]'); tick(); _click('#reset');"),
               T("document.title.startsWith('25:00')", "The tab title shows the time."), T("timer===null", "Changing mode stops the timer.", do="_click('#start'); _click('[data-mode=short]');")]))
P.sub_body('    </div>\n  </main>', '    </div>\n    <p id="sessions">Sessions today: 0</p>\n  </main>')
P.sub_js('    let mode = "focus";', '    const sessionsEl = document.querySelector("#sessions");\n    let mode = "focus";\n    let sessions = 0;')
P.sub_js('''      remaining -= 1;
      if (remaining <= 0) {
        remaining = 0;
        stop();
      }
      render();
    }''', '''      remaining -= 1;
      if (remaining <= 0) {
        finish();
        return;
      }
      render();
    }

    function finish() {
      if (mode === "focus") {
        sessions += 1;
        setMode("short");
      } else {
        setMode("focus");
      }
    }''')
P.sub_js('      document.title = `${format(remaining)} · Focus Timer`;', '      document.title = `${format(remaining)} · Focus Timer`;\n      sessionsEl.textContent = `Sessions today: ${sessions}`;')
S.append(step("pt7", "Count sessions and take breaks",
  ["When a focus session ends, count it and switch to a short break automatically; when a break ends, go back to focus. That logic belongs in one function, `finish()`, called by `tick()` at zero.",
   "`setMode` already stops the timer and re-renders, so `finish` is only a few lines."],
  "Add `<p id=\"sessions\">`. Keep `let sessions = 0;`. When the time runs out, `finish()` counts a finished focus session and switches to a short break, or switches a finished break back to focus. Show `Sessions today: N`.",
  P.render(), [T("sessions===1 && mode==='short' && _text('#time')==='05:00' && _text('#sessions')==='Sessions today: 1'", "Finishing a focus session counts it and starts a short break.", do="remaining = 1; tick();"),
               T("mode==='focus' && sessions===0 && _text('#time')==='25:00'", "Finishing a break goes back to focus without counting.", do="_click('[data-mode=short]'); remaining = 1; tick();"),
               T("_text('#sessions')==='Sessions today: 0'", "It starts at 0 sessions.")]))
P.sub_js('    let sessions = 0;', '''    const today = () => new Date().toISOString().slice(0, 10);

    function loadSessions() {
      try {
        const saved = JSON.parse(localStorage.getItem("focus-sessions"));
        return saved && saved.day === today() ? saved.count : 0;
      } catch {
        return 0;
      }
    }

    let sessions = loadSessions();''')
P.sub_js('        sessions += 1;\n', '        sessions += 1;\n        localStorage.setItem("focus-sessions", JSON.stringify({ day: today(), count: sessions }));\n')
S.append(step("pt8", "Remember today's sessions",
  ["Save the count together with the day it belongs to: `{ day: \"2026-10-23\", count: 3 }`. On load, use the count only if the day is today, so the number starts fresh every morning.",
   "`JSON.parse` throws on bad data, and `getItem` returns `null` when nothing is saved. `try`/`catch` and a `saved &&` check cover both."],
  "Save `{ day, count }` under `focus-sessions` each time a session finishes. On load, read it back: use the count if `day` is today, otherwise start at 0.",
  P.render(), [T("JSON.parse(localStorage.getItem('focus-sessions')).count===1 && JSON.parse(localStorage.getItem('focus-sessions')).day===new Date().toISOString().slice(0,10)", "Finishing a session saves today's count.", do="remaining = 1; tick();"),
               T("_text('#sessions')==='Sessions today: 4'", "Today's saved count is used.", do="localStorage.setItem('focus-sessions', JSON.stringify({ day: new Date().toISOString().slice(0, 10), count: 4 })); sessions = loadSessions(); render();"),
               T("_text('#sessions')==='Sessions today: 0'", "A count from another day is ignored.", storage={"focus-sessions": '{"day":"2000-01-01","count":5}'}),
               T("_text('#sessions')==='Sessions today: 0'", "Broken saved data doesn't crash the app.", storage={"focus-sessions": "{oops"})],
  ref=("MDN: Window.localStorage", "https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage")))
project(id="focus-timer", title="Focus Timer", lang="web", level="Beginner", hours="1.5 h", hue="#f97316", icon="clock", art="25:00",
  tagline="A Pomodoro timer with focus and break modes, a session count and a tab-title countdown.",
  desc=["Time is one of the first things apps have to handle. You'll build a focus timer you can actually use while studying: start, pause, reset, three modes and a count of today's sessions.",
        "Along the way you'll learn `setInterval`, how to keep state in one number and derive the display from it, and how to save data that expires each day."],
  final="A Pomodoro timer with Focus, Short break and Long break modes, start/pause and reset, automatic breaks, a live tab title and today's session count saved in the browser.",
  skills=["setInterval / clearInterval", "state and render", "string padding", "data-* attributes", "lookup objects", "localStorage with JSON", "try/catch"],
  prereq="**JavaScript & the DOM**, or the **Calculator** project.", core=["s4m1"],
  stretch=["Play a sound when a session ends (the Web Audio API or an `<audio>` element).", "Make every fourth break a long one.", "Let people change the lengths in a settings form.", "Show a circular progress ring with SVG."],
  milestones=[milestone("The display", "HTML, styles and seconds formatted as MM:SS.", S[0:3]), milestone("Time moves", "Tick, start, pause and reset.", S[3:5]),
              milestone("A real Pomodoro", "Modes, automatic breaks and saved sessions.", S[5:8])])

# =============================================================================================== MEMORY GAME (web)
P = Page("Memory")
S = []
BLANK = P.render()
PAIR = "const b = deck.findIndex((c, i) => i > 0 && c.symbol === deck[0].symbol); _click($$('.card')[0]); _click($$('.card')[b]);"
MISS = "const b = deck.findIndex(c => c.symbol !== deck[0].symbol); _click($$('.card')[0]); _click($$('.card')[b]);"
ALL = "for (const s of SYMBOLS) { const [a, b] = deck.map((c, i) => (c.symbol === s ? i : -1)).filter(i => i >= 0); _click($$('.card')[a]); _click($$('.card')[b]); }"
P.body = ['  <h1>Memory</h1>', '  <p id="status">Find all the pairs.</p>', '  <div id="board"></div>', '  <button id="restart">New game</button>']
S.append(step("mg1", "The game board",
  ["Memory (or *Concentration*) is a grid of face-down cards. Flip two: if they match, they stay up; if not, they flip back. Find every pair in as few moves as you can.",
   "The HTML only needs a place for messages, an empty board that JavaScript will fill with cards, and a restart button."],
  "Add an `<h1>` saying `Memory`, a `<p id=\"status\">`, an empty `<div id=\"board\">` and a `<button id=\"restart\">New game</button>`.",
  P.render(), [T("_text('h1')==='Memory'", "The `h1` says Memory."), T("!!$('#status') && !!$('#board') && $('#board').children.length===0", "There's a `#status` and an empty `#board`."),
               T("_text('#restart')==='New game'", "There's a New game button.")], starter=BLANK, core="s4m1"))
P.body = ['  <main class="game">', '    <h1>Memory</h1>', '    <p id="status">Find all the pairs.</p>', '    <div id="board"></div>', '    <button id="restart">New game</button>', '  </main>']
P.css = lines('''
    body { font-family: system-ui, sans-serif; background: #0f2f2a; color: #eafff8; margin: 0; padding: 32px 16px; }
    .game { max-width: 420px; margin: 0 auto; text-align: center; }
    #board { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 18px 0; }
    .card { aspect-ratio: 1; border: 0; border-radius: 14px; background: #1f6f5f; color: #eafff8; font-size: 30px; cursor: pointer; }
    .card.up { background: #f5fffb; }
    .card.matched { opacity: 0.55; cursor: default; }
    #restart { padding: 10px 18px; border: 0; border-radius: 999px; background: #34d399; color: #0f2f2a; font: inherit; font-weight: 600; cursor: pointer; }''')
S.append(step("mg2", "A grid of cards",
  ["CSS Grid lays out cards in rows and columns: `grid-template-columns: repeat(4, 1fr)` makes four equal columns, and `gap` spaces them.",
   "`aspect-ratio: 1` keeps each card square at any width. Style `.card.up` (face up) and `.card.matched` now, so they're ready when JavaScript adds those classes."],
  "Wrap the page in `<main class=\"game\">`. Make `#board` a 4-column grid with a gap, and style `.card`, `.card.up` and `.card.matched`.",
  P.render(), [T("getComputedStyle($('#board')).display==='grid'", "`#board` is a grid."), T("getComputedStyle($('#board')).gridTemplateColumns.split(' ').length===4", "It has 4 columns."),
               T("!!$('main.game #board')", "The board is inside `main.game`.")], ref=("MDN: CSS grid layout", "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout")))
P.js = lines('''
    const SYMBOLS = ["🍎", "🍋", "🍇", "🍒", "🥝", "🍑"];
    const board = document.querySelector("#board");
    const statusEl = document.querySelector("#status");
    let deck = [];

    function createDeck() {
      return SYMBOLS.flatMap(symbol => [symbol, symbol]).map((symbol, i) => ({ id: i, symbol, matched: false }));
    }

    function render() {
      board.innerHTML = "";
      deck.forEach((card, i) => {
        const button = document.createElement("button");
        button.className = "card";
        button.textContent = "?";
        button.setAttribute("aria-label", "Hidden card");
        board.append(button);
      });
    }

    deck = createDeck();
    render();''')
S.append(step("mg3", "Make the deck",
  ["Each card is an object: `{ id, symbol, matched }`. `flatMap(s => [s, s])` turns six symbols into twelve, two of each, in one line.",
   "`render()` rebuilds the board from `deck`. For now every card is face down: a `?`."],
  "Add a `<script>` with six `SYMBOLS`, `createDeck()` returning 12 card objects (each symbol twice), and `render()` that fills `#board` with a `button.card` showing `?` for each card.",
  P.render(), [T("createDeck().length===12 && SYMBOLS.every(s => createDeck().filter(c => c.symbol===s).length===2)", "The deck has every symbol exactly twice."),
               T("createDeck().every(c => c.matched===false) && new Set(createDeck().map(c => c.id)).size===12", "Cards start unmatched with unique ids."),
               T("$$('#board .card').length===12 && $$('#board .card').every(c => c.textContent==='?')", "The board shows 12 face-down cards.")],
  ref=("MDN: Array.prototype.flatMap", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/flatMap")))
P.sub_js('    function render() {', '''    function shuffle(items) {
      const a = [...items];
      for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }
      return a;
    }

    function render() {''')
P.sub_js('    deck = createDeck();', '    deck = shuffle(createDeck());')
S.append(step("mg4", "Shuffle fairly",
  ["The **Fisher–Yates shuffle** walks from the end of the array, swapping each item with a random one at or before it. Every order is equally likely, unlike the popular `sort(() => Math.random() - 0.5)`, which is biased.",
   "`[a[i], a[j]] = [a[j], a[i]]` swaps two items using destructuring. Copy the array first so `shuffle` doesn't change its input."],
  "Write `shuffle(items)` returning a shuffled copy using Fisher–Yates. Shuffle the deck before rendering.",
  P.render(), [T("JSON.stringify(shuffle([5,3,1,4,2]).sort())===JSON.stringify([1,2,3,4,5])", "Shuffling keeps every item."),
               T("(() => { const a = [1,2,3]; shuffle(a); return a.join()==='1,2,3'; })()", "The original array isn't changed."),
               T("new Set(Array.from({ length: 30 }, () => shuffle([1,2,3,4,5,6,7,8]).join())).size > 1", "Different shuffles give different orders."),
               dict(src="Math\\.random", msg="You use `Math.random`.")],
  ref=("Wikipedia: Fisher–Yates shuffle", "https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle")))
P.sub_js('    let deck = [];', '    let deck = [];\n    let flipped = [];')
P.sub_js('''        button.className = "card";
        button.textContent = "?";
        button.setAttribute("aria-label", "Hidden card");
        board.append(button);''', '''        const up = card.matched || flipped.includes(i);
        button.className = "card";
        if (up) button.classList.add("up");
        if (card.matched) button.classList.add("matched");
        button.textContent = up ? card.symbol : "?";
        button.setAttribute("aria-label", up ? card.symbol : "Hidden card");
        button.addEventListener("click", () => flip(i));
        board.append(button);''')
P.sub_js('    deck = shuffle(createDeck());', '''    function flip(i) {
      if (flipped.includes(i) || deck[i].matched) return;
      flipped.push(i);
      render();
    }

    deck = shuffle(createDeck());''')
S.append(step("mg5", "Flip a card",
  ["Keep the indexes of face-up cards in `flipped`. A card is shown if it's matched or in `flipped`; `render()` decides, so the screen always matches the data.",
   "Ignore clicks on a card that's already face up or matched: a **guard clause** at the top of `flip` does it."],
  "Add `let flipped = [];`. Clicking a card calls `flip(i)`, which adds its index (unless it's already up or matched) and re-renders. Face-up cards show their symbol and have the class `up`.",
  P.render(), [T("$$('.card')[0].classList.contains('up') && _text($$('.card')[0])===deck[0].symbol", "A clicked card turns face up and shows its symbol.", do="_click($$('.card')[0]);"),
               T("flipped.length===1", "Clicking the same card twice doesn't flip it twice.", do="_click($$('.card')[0]); _click($$('.card')[0]);"),
               T("$$('.card.up').length===0", "All cards start face down.")]))
P.sub_js('    let flipped = [];', '    let flipped = [];\n    let moves = 0;\n    let lock = false;')
P.sub_js('''      if (flipped.includes(i) || deck[i].matched) return;
      flipped.push(i);
      render();
    }''', '''      if (lock || flipped.includes(i) || deck[i].matched) return;
      flipped.push(i);
      if (flipped.length === 2) {
        moves += 1;
        const [a, b] = flipped;
        if (deck[a].symbol === deck[b].symbol) {
          deck[a].matched = true;
          deck[b].matched = true;
          flipped = [];
        } else {
          lock = true;
          setTimeout(() => {
            flipped = [];
            lock = false;
            render();
          }, 700);
        }
      }
      render();
    }''')
S.append(step("mg6", "Match or flip back",
  ["When a second card is turned, that's one move. If the symbols match, mark both `matched`. If not, leave them visible for a moment, then flip them back with `setTimeout`.",
   "While two wrong cards are showing, the board must ignore clicks, or a fast player could turn a third card. A `lock` flag does that."],
  "Count `moves`. On the second card, keep matching pairs face up (set `matched`), or lock the board and flip both back after 700 ms.",
  P.render(), [T("deck[0].matched && flipped.length===0 && moves===1", "A matching pair stays up and counts as one move.", do=PAIR),
               T("lock && $$('.card.up').length===2", "A wrong pair is shown and the board is locked.", do=MISS),
               T("!lock && $$('.card.up').length===0 && moves===1", "After a moment the wrong pair flips back.", do=MISS, wait=900),
               T("flipped.length===2", "A third card can't be turned while locked.", do=MISS + " _click($$('.card')[deck.findIndex((c, i) => i !== 0 && i !== b)]);")],
  ref=("MDN: setTimeout", "https://developer.mozilla.org/en-US/docs/Web/API/setTimeout")))
P.sub_js('''        board.append(button);
      });''', '''        board.append(button);
      });
      const won = deck.every(card => card.matched);
      statusEl.textContent = won ? `You won in ${moves} moves.` : `Moves: ${moves}`;''')
P.sub_js('''    deck = shuffle(createDeck());
    render();''', '''    function newGame() {
      deck = shuffle(createDeck());
      flipped = [];
      moves = 0;
      lock = false;
      render();
    }

    document.querySelector("#restart").addEventListener("click", newGame);
    newGame();''')
S.append(step("mg7", "Winning and restarting",
  ["The game is won when every card is matched: `deck.every(card => card.matched)`. Work it out inside `render()` and the status line is always right.",
   "A `newGame()` function that resets **all** the state (deck, flipped, moves, lock) is used both on load and by the restart button."],
  "Show `Moves: N` while playing and `You won in N moves.` once every pair is found. Write `newGame()` and call it on load and from `#restart`.",
  P.render(), [T("_text('#status')==='Moves: 0'", "The status starts at `Moves: 0`."), T("_text('#status')==='You won in 6 moves.'", "Finding every pair shows `You won in 6 moves.`", do=ALL),
               T("moves===0 && $$('.card.up').length===0 && _text('#status')==='Moves: 0'", "New game resets everything.", do=PAIR + " _click('#restart');")]))
P.sub_body('    <p id="status">Find all the pairs.</p>', '    <p id="status">Find all the pairs.</p>\n    <p id="best"></p>')
P.sub_js('    let lock = false;', '''    let lock = false;
    let best = Number(localStorage.getItem("memory-best")) || null;
    const bestEl = document.querySelector("#best");''')
P.sub_js('''      statusEl.textContent = won ? `You won in ${moves} moves.` : `Moves: ${moves}`;''', '''      statusEl.textContent = won ? `You won in ${moves} moves.` : `Moves: ${moves}`;
      bestEl.textContent = best ? `Best: ${best} moves` : "Best: none yet";''')
P.sub_js('''          deck[b].matched = true;
          flipped = [];''', '''          deck[b].matched = true;
          flipped = [];
          if (deck.every(card => card.matched) && (!best || moves < best)) {
            best = moves;
            localStorage.setItem("memory-best", String(best));
          }''')
S.append(step("mg8", "A best score to beat",
  ["Save the fewest moves with `localStorage`, so there's always a record to beat. `Number(null)` is `0`, and `0 || null` is `null`, which reads as *no best yet*.",
   "Only save when the game is won **and** the score beats the old one."],
  "Add `<p id=\"best\">`. Show `Best: N moves`, or `Best: none yet`. When a game is won with fewer moves than the best (or there's no best), save it under `memory-best`.",
  P.render(), [T("_text('#best')==='Best: none yet'", "With no saved score it shows `Best: none yet`.", storage={}),
               T("_text('#best')==='Best: 9 moves'", "A saved best is shown.", storage={"memory-best": "9"}),
               T("localStorage.getItem('memory-best')==='6' && _text('#best')==='Best: 6 moves'", "Beating it saves the new best.", do=ALL, storage={"memory-best": "9"}),
               T("localStorage.getItem('memory-best')==='4'", "A worse game doesn't overwrite the best.", do=ALL, storage={"memory-best": "4"})]))
project(id="memory-game", title="Memory Card Game", lang="web", level="Intermediate", hours="2 h", hue="#34d399", icon="game", art="🍎 ? ? 🍎",
  tagline="Flip cards, find pairs, beat your best: shuffling, game state and timing in the browser.",
  desc=["A complete little game you can play on your phone. You'll generate and shuffle a deck, flip cards, check pairs, lock the board while wrong guesses show, detect the win and keep a best score.",
        "It's a lesson in modelling state: everything on screen comes from a few variables and one `render()` function."],
  final="A 12-card memory game with a fair shuffle, flip animation states, a move counter, a locked board during mistakes, a win message, a New game button and a saved best score.",
  skills=["arrays of objects", "flatMap", "Fisher–Yates shuffle", "state and render", "setTimeout", "guard clauses", "CSS grid", "localStorage"],
  prereq="the **To-Do List App** project, or **JavaScript & the DOM**.", core=["s4m1", "s2m1"],
  stretch=["Add a timer and show it next to the moves.", "Offer 4×4 and 6×6 boards.", "Animate the flip with a CSS 3D transform.", "Make it playable with the keyboard (arrow keys and Enter)."],
  milestones=[milestone("The board", "HTML, a grid and a shuffled deck.", S[0:4]), milestone("Playing", "Flip cards and match pairs.", S[4:6]),
              milestone("The full game", "Winning, restarting and a best score.", S[6:8])])

# =============================================================================================== HABIT TRACKER (web)
P = Page("Habit Tracker")
S = []
BLANK = P.render()
def add_habit(name):
    return f"_type('#habit-name', {name!r}); _submit('#habit-form');"
DAY_TH = "".join(f"<th>{d}</th>" for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
P.body = ['  <h1>Habits</h1>', '  <form id="habit-form">', '    <input id="habit-name" placeholder="New habit" autocomplete="off">', '    <button>Add habit</button>', '  </form>',
          '  <table id="grid">', f'    <thead><tr><th>Habit</th>{DAY_TH}</tr></thead>', '    <tbody></tbody>', '  </table>']
S.append(step("ht1", "A form and a week",
  ["A habit tracker is a table: one row per habit, one column per day of the week, a tick in each cell you did it.",
   "The header row never changes, so write it in HTML. The rows depend on data, so JavaScript will build them."],
  "Add an `<h1>` saying `Habits`, a `form#habit-form` with `input#habit-name` and an Add habit button, and a `table#grid` whose header row is `Habit` then `Mon` to `Sun`, with an empty `tbody`.",
  P.render(), [T("_text('h1')==='Habits'", "The `h1` says Habits."), T("!!$('#habit-form #habit-name')", "The form has `#habit-name`."),
               T("$$('#grid thead th').map(th => th.textContent).join()==='Habit,Mon,Tue,Wed,Thu,Fri,Sat,Sun'", "The header is Habit, Mon … Sun."), T("$('#grid tbody').children.length===0", "The body starts empty.")],
  starter=BLANK, core="s4m1"))
P.body = ['  <main class="habits">'] + ['  ' + l for l in P.body] + ['  </main>']
P.css = lines('''
    [hidden] { display: none !important; }
    body { font-family: system-ui, sans-serif; background: #fdf6ec; color: #2b1d0e; margin: 0; padding: 32px 16px; }
    .habits { max-width: 720px; margin: 0 auto; background: white; padding: 24px; border-radius: 16px; }
    #habit-form { display: flex; gap: 8px; margin-bottom: 16px; }
    #habit-name { flex: 1; padding: 10px; border: 1px solid #d8c8b0; border-radius: 8px; font: inherit; }
    button { padding: 10px 14px; border: 0; border-radius: 8px; background: #c2410c; color: white; font: inherit; cursor: pointer; }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 8px 6px; border-bottom: 1px solid #f0e6d8; text-align: center; }
    th:first-child, td:first-child { text-align: left; }''')
S.append(step("ht2", "Make it tidy",
  ["`border-collapse: collapse` merges the double borders between table cells into single lines. Centre the tick boxes but keep the habit names left-aligned with `:first-child`.",
   "As in other projects, the form is a flex row and the input takes the spare space."],
  "Wrap the page in `<main class=\"habits\">` with a `max-width`. Make the form a flex row, the table full-width with collapsed borders, and add `[hidden] { display: none !important; }`.",
  P.render(), [T("!!$('main.habits #grid') && getComputedStyle($('.habits')).maxWidth!=='none'", "The page is a `main.habits` card with a max width."),
               T("getComputedStyle($('#habit-form')).display==='flex'", "The form is a flex row."), T("getComputedStyle($('#grid')).borderCollapse==='collapse'", "The table collapses its borders.")]))
P.js = lines('''
    const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    const tbody = document.querySelector("#grid tbody");
    let habits = [];

    function render() {
      tbody.innerHTML = "";
      habits.forEach((habit, h) => {
        const tr = document.createElement("tr");
        const name = document.createElement("td");
        name.textContent = habit.name;
        tr.append(name);
        habit.days.forEach((done, d) => {
          const td = document.createElement("td");
          const box = document.createElement("input");
          box.type = "checkbox";
          box.checked = done;
          box.setAttribute("aria-label", `${habit.name} on ${DAYS[d]}`);
          td.append(box);
          tr.append(td);
        });
        tbody.append(tr);
      });
    }

    function addHabit(name) {
      habits.push({ name, days: DAYS.map(() => false) });
      render();
    }''')
S.append(step("ht3", "Habits as data",
  ["Each habit is `{ name, days }`, where `days` is seven booleans, one per day. `DAYS.map(() => false)` makes a fresh array of seven `false`s.",
   "`render()` builds one row per habit: the name, then a checkbox per day. Give each checkbox an `aria-label` like `Read on Mon`, so screen readers can tell them apart."],
  "Add a `<script>` with `DAYS`, `let habits = [];`, `addHabit(name)` and `render()` that adds a row per habit: the name cell, then 7 checkboxes reflecting `days`.",
  P.render(), [T("$$('#grid tbody tr').length===1 && _text('#grid tbody td')==='Read' && $$('#grid tbody tr input[type=checkbox]').length===7", "`addHabit` adds a row with the name and 7 checkboxes.", do="addHabit('Read');"),
               T("habits[0].days.length===7 && habits[0].days.every(d => d===false)", "A new habit has seven unticked days.", do="addHabit('Read');"),
               T("$('#grid tbody input').getAttribute('aria-label')==='Read on Mon'", "Checkboxes have labels like `Read on Mon`.", do="addHabit('Read');")]))
P.sub_body('    </form>', '    </form>\n    <p id="msg" hidden></p>')
P.sub_js('    let habits = [];', '    const form = document.querySelector("#habit-form");\n    const input = document.querySelector("#habit-name");\n    const msg = document.querySelector("#msg");\n    let habits = [];')
P.js += lines('''

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const name = input.value.trim();
      msg.hidden = true;
      if (name === "") return;
      if (habits.some(h => h.name.toLowerCase() === name.toLowerCase())) {
        msg.textContent = "You already track that.";
        msg.hidden = false;
        return;
      }
      addHabit(name);
      input.value = "";
    });''')
S.append(step("ht4", "Add habits from the form",
  ["Clean the input before you trust it: trim spaces, ignore empty names, and refuse duplicates. `some()` answers *does any habit already have this name?*, compared in lowercase so `Read` and `read` count as the same.",
   "Show the reason in `#msg` instead of failing silently."],
  "On submit: trim the name, ignore it if empty, show `You already track that.` in `#msg` for a duplicate (any case), otherwise add it and clear the input.",
  P.render(), [T("habits.length===2 && _text('#grid tbody tr:last-child td')==='Run' && $('#habit-name').value===''", "Submitting adds the habit and clears the input.", do=add_habit("Read") + add_habit("  Run  ")),
               T("habits.length===0", "Empty names are ignored.", do=add_habit("   ")),
               T("habits.length===1 && !$('#msg').hidden && _text('#msg')==='You already track that.'", "Duplicates are refused with a message.", do=add_habit("Read") + add_habit("read")),
               T("$('#msg').hidden", "The message hides again on the next good add.", do=add_habit("Read") + add_habit("READ") + add_habit("Run"))]))
P.sub_body(f'<th>Sun</th></tr></thead>', '<th>Sun</th><th>Done</th></tr></thead>')
P.sub_js('          td.append(box);', '          box.addEventListener("change", () => toggle(h, d));\n          td.append(box);')
P.sub_js('        tbody.append(tr);', '''        const count = document.createElement("td");
        count.className = "count";
        count.textContent = `${habit.days.filter(Boolean).length}/7`;
        tr.append(count);
        tbody.append(tr);''')
P.sub_js('    function addHabit(name) {', '''    function toggle(h, d) {
      habits[h].days[d] = !habits[h].days[d];
      render();
    }

    function addHabit(name) {''')
S.append(step("ht5", "Tick off a day",
  ["When a checkbox changes, flip that day in the data and re-render. The checkbox's position gives you both indexes: habit `h` and day `d`.",
   "`days.filter(Boolean).length` counts the `true` values: a neat trick, since `Boolean(true)` is `true`."],
  "Add a `Done` header. Ticking a box calls `toggle(h, d)`, which flips that day and re-renders. Each row ends with a `td.count` showing `N/7`.",
  P.render(), [T("habits[0].days[0]===true && _text('#grid tbody .count')==='1/7'", "Ticking Monday records it and shows `1/7`.", do="addHabit('Read'); _click('#grid tbody input');"),
               T("habits[0].days[0]===false && _text('#grid tbody .count')==='0/7'", "Unticking undoes it.", do="addHabit('Read'); _click('#grid tbody input'); _click('#grid tbody input');"),
               T("$$('#grid thead th').pop().textContent==='Done'", "The header has a Done column.")]))
P.sub_body('<th>Done</th></tr></thead>', '<th>Done</th><th>Best streak</th></tr></thead>')
P.sub_js('        tr.append(count);', '''        tr.append(count);
        const streak = document.createElement("td");
        streak.className = "streak";
        streak.textContent = longestStreak(habit.days);
        tr.append(streak);''')
P.sub_js('    function toggle(h, d) {', '''    function longestStreak(days) {
      let best = 0;
      let run = 0;
      for (const done of days) {
        run = done ? run + 1 : 0;
        best = Math.max(best, run);
      }
      return best;
    }

    function toggle(h, d) {''')
S.append(step("ht6", "Best streak",
  ["A streak is days in a row. Walk the week keeping `run` (the current streak) and `best`: a ticked day adds one to `run`, an unticked one resets it to 0.",
   "It's the same pattern as *maximum consecutive ones*, a classic interview problem, so you're learning both at once."],
  "Write `longestStreak(days)` and show it in a `td.streak` on each row, under a new `Best streak` header.",
  P.render(), [T("longestStreak([true,true,false,true,true,true,false])===3 && longestStreak(Array(7).fill(false))===0 && longestStreak(Array(7).fill(true))===7", "`longestStreak` finds the longest run of ticks."),
               T("_text('#grid tbody .streak')==='2'", "The row shows the best streak.", do="addHabit('Read'); _click($$('#grid tbody input')[2]); _click($$('#grid tbody input')[3]); _click($$('#grid tbody input')[5]);")],
  hint="`run = done ? run + 1 : 0;` then `best = Math.max(best, run);`"))
P.sub_body('<th>Best streak</th></tr></thead>', '<th>Best streak</th><th></th></tr></thead>')
P.css.append('    .delete { background: transparent; color: #b91c1c; padding: 4px 8px; }')
P.sub_js('        tr.append(streak);', '''        tr.append(streak);
        const actions = document.createElement("td");
        const del = document.createElement("button");
        del.className = "delete";
        del.textContent = "Delete";
        del.setAttribute("aria-label", `Delete ${habit.name}`);
        del.addEventListener("click", () => removeHabit(h));
        actions.append(del);
        tr.append(actions);''')
P.sub_js('    function addHabit(name) {', '''    function removeHabit(h) {
      habits = habits.filter((_, i) => i !== h);
      render();
    }

    function addHabit(name) {''')
S.append(step("ht7", "Delete a habit",
  ["Habits change. `filter((_, i) => i !== h)` keeps every habit except the one at index `h`; the underscore is a common name for a parameter you don't use.",
   "Give each Delete button an `aria-label` naming its habit: a screen reader user hearing *Delete, Delete, Delete* wouldn't know which is which."],
  "Add a `button.delete` at the end of each row (with an empty header cell above). Clicking it removes that habit.",
  P.render(), [T("habits.length===1 && habits[0].name==='Run' && $$('#grid tbody tr').length===1", "Deleting removes exactly that habit.", do="addHabit('Read'); addHabit('Run'); _click('#grid tbody .delete');"),
               T("$('#grid tbody .delete').getAttribute('aria-label')==='Delete Read'", "The button is labelled with the habit's name.", do="addHabit('Read');")]))
P.sub_js('    let habits = [];', '''    function load() {
      try {
        const saved = JSON.parse(localStorage.getItem("habits"));
        return Array.isArray(saved) ? saved : [];
      } catch {
        return [];
      }
    }

    function save() {
      localStorage.setItem("habits", JSON.stringify(habits));
    }

    let habits = load();''')
P.sub_js('      tbody.innerHTML = "";', '      save();\n      tbody.innerHTML = "";')
P.js.append('')
P.js.append('    render();')
SAVED = '[{"name":"Run","days":[true,true,false,false,false,false,false]}]'
S.append(step("ht8", "Keep the week",
  ["Save the whole `habits` array as JSON every time it changes. Since every change ends in `render()`, saving at the start of `render()` covers them all in one line.",
   "On load, read it back, but don't trust it blindly: check it's really an array, and fall back to `[]` if the JSON is broken."],
  "Write `load()` and `save()` using the `habits` key. Start with `let habits = load();`, save on every render, and call `render()` once on page load.",
  P.render(), [T("_text('#grid tbody td')==='Run' && _text('#grid tbody .count')==='2/7' && _text('#grid tbody .streak')==='2'", "Saved habits are shown on load.", storage={"habits": SAVED}),
               T("JSON.parse(localStorage.getItem('habits'))[0].name==='Read' && JSON.parse(localStorage.getItem('habits'))[0].days[0]===true", "Changes are saved.", do=add_habit("Read") + "_click('#grid tbody input');", storage={}),
               T("habits.length===0 && $$('#grid tbody tr').length===0", "Broken saved data doesn't crash the app.", storage={"habits": "{oops"}),
               T("habits.length===0", "Saved data that isn't a list is ignored.", storage={"habits": '{"name":"Run"}'})]))
project(id="habit-tracker", title="Habit Tracker", lang="web", level="Intermediate", hours="1.5 h", hue="#c2410c", icon="cal", art="✓ ✓ · ✓",
  tagline="A weekly habit grid with ticks, totals, best streaks and everything saved between visits.",
  desc=["Build the kind of app people keep open all week: a grid of habits and days, ticked off as you go, with a count and a best streak for each.",
        "You'll practise the pattern behind most web apps (data in an array, one `render()` that builds the page from it) plus validation, tables and safe saving."],
  final="A habit tracker with a validated add form, a Mon–Sun checkbox grid, done counts, best streaks, delete buttons, accessible labels and data saved in the browser.",
  skills=["tables built from data", "arrays of objects", "array.map / filter / some", "validation", "streak algorithm", "accessibility labels", "localStorage with JSON"],
  prereq="the **To-Do List App** project.", core=["s4m1", "s1m4"],
  stretch=["Start a new week automatically each Monday, keeping last week's totals.", "Add a colour per habit.", "Show a summary row with the total ticks per day.", "Let people rename a habit by double-clicking it."],
  milestones=[milestone("The grid", "HTML, styles and habits as data.", S[0:3]), milestone("Tracking", "Add habits, tick days and see streaks.", S[3:6]),
              milestone("Finishing touches", "Delete and save.", S[6:8])])
