from _lib import *

def T(js, msg, do=None, **k):
    d = dict(js=js, msg=msg, **k)
    if do: d["do"] = do
    return d

def add_todo(text):
    return f"_type('#new-todo', {text!r}); _submit('#todo-form');"

# =============================================================================================== TO-DO LIST
P = Page("My To-Dos")
S = []
BLANK = P.render()
P.body = ['  <h1>My To-Dos</h1>', '  <form id="todo-form">', '    <input id="new-todo" placeholder="What needs doing?" autocomplete="off">', '    <button>Add</button>', '  </form>', '  <ul id="list"></ul>']
S.append(step("td1", "The page skeleton",
  ["Every web app starts as HTML: the structure your JavaScript will bring to life later. A `<form>` groups an input with its button, and it gives you a single **submit** event whether people click **Add** or press Enter.",
   "Give each element you'll need from JavaScript an `id`. That's how the code will find it: `document.querySelector(\"#list\")`."],
  "Add an `<h1>` saying `My To-Dos`, a `<form id=\"todo-form\">` containing an `<input id=\"new-todo\">` and a `<button>Add</button>`, and an empty `<ul id=\"list\">` below the form.",
  P.render(),
  [T("_text('h1')==='My To-Dos'", "The `h1` says My To-Dos."), T("!!$('form#todo-form input#new-todo')", "The form `#todo-form` contains the input `#new-todo`."),
   T("!!$('#todo-form button')", "The form has a button."), T("!!$('ul#list')", "There's an empty `ul` with id `list`.")],
  starter=BLANK, hint="The input goes inside the form: `<form id=\"todo-form\"><input id=\"new-todo\"><button>Add</button></form>`.", core="s4m1", ref=("MDN: The form element", "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form")))
P.body = ['  <main class="app">'] + ['  ' + l for l in P.body] + ['  </main>']
P.css = ['    [hidden] { display: none !important; }',
         '    body { font-family: system-ui, sans-serif; background: #f4f1ff; margin: 0; padding: 40px 16px; }',
         '    .app { max-width: 480px; margin: 0 auto; background: white; padding: 24px; border-radius: 16px; }',
         '    #todo-form { display: flex; gap: 8px; }',
         '    #new-todo { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 8px; font: inherit; }',
         '    button { padding: 10px 14px; border: 0; border-radius: 8px; background: #5b45f0; color: white; font: inherit; cursor: pointer; }',
         '    #list { list-style: none; padding: 0; }',
         '    #list li { display: flex; align-items: center; gap: 10px; padding: 10px 0; border-bottom: 1px solid #eee; }']
S.append(step("td2", "Make it look like an app",
  ["Wrap everything in a `<main class=\"app\">` card and give it a `max-width`, so the app stays a comfortable width on big screens. `margin: 0 auto` centres it.",
   "`display: flex` on the form puts the input and button on one line, and `flex: 1` on the input lets it take all the leftover space."],
  "Wrap the page in `<main class=\"app\">`. In the `<style>`, give `.app` a `max-width`, a background and padding, and make `#todo-form` a flex row. Add `[hidden] { display: none !important; }` too: you'll need it later.",
  P.render(),
  [T("!!$('main.app #list')", "Everything is inside `main.app`."), T("getComputedStyle($('.app')).maxWidth!=='none'", "`.app` has a `max-width`."),
   T("getComputedStyle($('#todo-form')).display==='flex'", "`#todo-form` uses `display: flex`.")], core="s4m1", ref=("CSS-Tricks: A guide to Flexbox", "https://css-tricks.com/snippets/css/a-guide-to-flexbox/")))
P.js = ['    const form = document.querySelector("#todo-form");', '    const input = document.querySelector("#new-todo");', '',
        '    form.addEventListener("submit", (event) => {', '      event.preventDefault();', '      console.log(input.value);', '    });']
S.append(step("td3", "Listen for the form",
  ["JavaScript makes the page react. First, find the elements with `document.querySelector`, then **listen** for events with `addEventListener`.",
   "By default, submitting a form reloads the page, which would wipe your app. `event.preventDefault()` stops that. `console.log` prints to the console under the preview, which is your best debugging friend."],
  "Add a `<script>` at the end of `<body>`. Select the form and the input, listen for `submit`, call `event.preventDefault()`, and `console.log` the input's value. Type something and press Enter to see it in the console.",
  P.render(),
  [T("_logs().includes('Buy milk')", "Submitting the form logs what was typed.", do=add_todo("Buy milk")), dict(src="preventDefault\\(\\)", msg="You call `event.preventDefault()`.")],
  hint="`form.addEventListener(\"submit\", (event) => { event.preventDefault(); console.log(input.value); });`", ref=("MDN: addEventListener", "https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener")))
P.js = ['    const form = document.querySelector("#todo-form");', '    const input = document.querySelector("#new-todo");', '    const list = document.querySelector("#list");', '',
        '    function addTodo(text) {', '      const li = document.createElement("li");', '      li.textContent = text;', '      list.append(li);', '    }', '',
        '    form.addEventListener("submit", (event) => {', '      event.preventDefault();', '      addTodo(input.value);', '      input.value = "";', '    });']
S.append(step("td4", "Add items to the list",
  ["`document.createElement(\"li\")` makes a new element in memory; `list.append(li)` puts it on the page. Setting `textContent` (not `innerHTML`) is the safe way to show text people typed: it can never be treated as HTML.",
   "Put the work in a function, `addTodo(text)`, so the submit handler stays short and you can reuse it."],
  "Write `addTodo(text)` that creates an `li` with the text and appends it to `#list`. On submit, call it with the input's value, then clear the input.",
  P.render(),
  [T("$$('#list li').length===1 && _text('#list li').includes('Buy milk')", "Submitting adds an `li` with the text.", do=add_todo("Buy milk")),
   T("$('#new-todo').value===''", "The input is cleared after adding.", do=add_todo("Buy milk")),
   T("$$('#list li').length===2", "You can add more than one.", do=add_todo("A") + add_todo("B"))], core="s4m1", ref=("MDN: Document.createElement", "https://developer.mozilla.org/en-US/docs/Web/API/Document/createElement")))
P.sub_js('      addTodo(input.value);', '      const text = input.value.trim();\n      if (text === "") return;\n      addTodo(text);')
S.append(step("td5", "Ignore empty to-dos",
  ["Users press Enter by accident. `trim()` removes spaces from both ends of a string, so `\"   \".trim()` is `\"\"`.",
   "A **guard clause**, `if (text === \"\") return;`, exits early and keeps the happy path unindented."],
  "Trim the input. If the result is empty, do nothing; otherwise add the trimmed text.",
  P.render(),
  [T("$$('#list li').length===0", "Submitting only spaces adds nothing.", do=add_todo("    ")),
   T("_text('#list li')==='Tea'", "Text is trimmed before it's added.", do=add_todo("   Tea  "))]))
P.js = ['    const form = document.querySelector("#todo-form");', '    const input = document.querySelector("#new-todo");', '    const list = document.querySelector("#list");', '    let todos = [];', '',
        '    function render() {', '      list.innerHTML = "";', '      for (const todo of todos) {', '        const li = document.createElement("li");', '        const span = document.createElement("span");', '        span.textContent = todo.text;', '        li.append(span);', '        list.append(li);', '      }', '    }', '',
        '    function addTodo(text) {', '      todos.push({ id: Date.now() + Math.random(), text: text, done: false });', '      render();', '    }', '',
        '    form.addEventListener("submit", (event) => {', '      event.preventDefault();', '      const text = input.value.trim();', '      if (text === "") return;', '      addTodo(text);', '      input.value = "";', '    });']
S.append(step("td6", "Keep the data in an array",
  ["So far the page *is* the data. That gets messy once items can change. The fix every framework uses: keep the data in a JavaScript array (the **state**) and write one `render()` function that rebuilds the list from it.",
   "Each to-do becomes an object, `{ id, text, done }`. Changing the app is then always the same two moves: update the array, call `render()`."],
  "Add `let todos = [];`. Make `addTodo` push `{ id, text, done: false }` and call `render()`. Write `render()` to clear `#list` and add one `li` (containing a `span` with the text) per to-do.",
  P.render(),
  [T("Array.isArray(todos) && typeof render==='function'", "There's a `todos` array and a `render` function."),
   T("todos.length===2 && todos[1].text==='B' && todos[1].done===false", "Adding pushes `{ text, done: false }` objects.", do=add_todo("A") + add_todo("B")),
   T("$$('#list li span').length===2 && _text('#list li:last-child span')==='B'", "The list is rebuilt from the array, one `li` with a `span` per item.", do=add_todo("A") + add_todo("B"))],
  core="s4m2"))
P.css.append('    #list li.done span { text-decoration: line-through; color: #999; }')
P.sub_js('        const span = document.createElement("span");', '        if (todo.done) li.classList.add("done");\n        const box = document.createElement("input");\n        box.type = "checkbox";\n        box.checked = todo.done;\n        box.addEventListener("change", () => toggle(todo.id));\n        const span = document.createElement("span");')
P.sub_js('        li.append(span);', '        li.append(box, span);')
P.sub_js('    function addTodo(text) {', '    function toggle(id) {\n      const todo = todos.find(t => t.id === id);\n      todo.done = !todo.done;\n      render();\n    }\n\n    function addTodo(text) {')
S.append(step("td7", "Tick things off",
  ["Each item gets a checkbox. When it changes, flip that to-do's `done` flag and re-render. `array.find(t => t.id === id)` returns the first item matching a condition.",
   "Styling follows state: give the `li` the class `done` when the to-do is done, and let CSS draw the line through it."],
  "In `render`, add a checkbox before the text and the class `done` on finished items. Write `toggle(id)` to flip `done` and re-render. Add CSS that strikes through `li.done span`.",
  P.render(),
  [T("todos[0].done===true && $('#list li').classList.contains('done')", "Ticking the checkbox marks the to-do done.", do=add_todo("A") + "_click('#list li input[type=checkbox]');"),
   T("getComputedStyle($('#list li.done span')).textDecorationLine.includes('line-through')", "Done items are struck through.", do=add_todo("A") + "_click('#list li input[type=checkbox]');"),
   T("todos[0].done===false", "Ticking twice un-does it.", do=add_todo("A") + "_click('#list li input[type=checkbox]'); _click('#list li input[type=checkbox]');")],
  ref=("MDN: Array.prototype.find", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/find")))
P.sub_js('        li.append(box, span);', '        const del = document.createElement("button");\n        del.className = "delete";\n        del.textContent = "Delete";\n        del.addEventListener("click", () => removeTodo(todo.id));\n        li.append(box, span, del);')
P.sub_js('    function addTodo(text) {', '    function removeTodo(id) {\n      todos = todos.filter(t => t.id !== id);\n      render();\n    }\n\n    function addTodo(text) {')
P.css.append('    #list li span { flex: 1; }')
P.css.append('    .delete { background: transparent; color: #c62828; padding: 4px 8px; }')
S.append(step("td8", "Delete items",
  ["`array.filter(...)` returns a new array with only the items that pass the test. To delete, keep everything **except** the one with that id: `todos = todos.filter(t => t.id !== id)`.",
   "That's why `todos` is declared with `let`: you replace it with the filtered array."],
  "Add a `<button class=\"delete\">` to each item. Clicking it should remove that to-do (write `removeTodo(id)`) and re-render.",
  P.render(),
  [T("todos.length===1 && _text('#list li span')==='B'", "Deleting removes exactly that item.", do=add_todo("A") + add_todo("B") + "_click('#list li .delete');"),
   T("$$('#list li').length===0", "Deleting the last item empties the list.", do=add_todo("A") + "_click('.delete');")]))
P.sub_body('    <ul id="list"></ul>', '    <ul id="list"></ul>\n    <p id="count"></p>')
P.sub_js('    const list = document.querySelector("#list");', '    const list = document.querySelector("#list");\n    const count = document.querySelector("#count");')
P.sub_js('        list.append(li);\n      }\n    }', '        list.append(li);\n      }\n      const left = todos.filter(t => !t.done).length;\n      count.textContent = `${left} ${left === 1 ? "item" : "items"} left`;\n    }\n\n    render();')
S.append(step("td9", "Count what's left",
  ["A count of unfinished items is **derived state**: never store it, compute it inside `render()` from the array, so it can never be wrong.",
   "Grammar matters: `1 item left` but `2 items left`. A ternary `left === 1 ? \"item\" : \"items\"` handles it."],
  "Add `<p id=\"count\"></p>` under the list. In `render()`, show `N items left` (singular for 1). Call `render()` once when the page loads so it shows `0 items left` straight away.",
  P.render(),
  [T("_text('#count')==='0 items left'", "On load it shows `0 items left`."),
   T("_text('#count')==='2 items left'", "Two active items shows `2 items left`.", do=add_todo("A") + add_todo("B")),
   T("_text('#count')==='1 item left'", "Ticking one off shows `1 item left`.", do=add_todo("A") + add_todo("B") + "_click('#list li input[type=checkbox]');")]))
P.sub_body('    <p id="count"></p>', '    <div class="filters">\n      <button data-filter="all" class="active">All</button>\n      <button data-filter="active">Active</button>\n      <button data-filter="done">Done</button>\n    </div>\n    <p id="count"></p>')
P.css.append('    .filters { display: flex; gap: 6px; margin-top: 12px; }')
P.css.append('    .filters button { background: #eee; color: #333; }')
P.css.append('    .filters button.active { background: #5b45f0; color: white; }')
P.sub_js('    let todos = [];', '    let todos = [];\n    let filter = "all";')
P.sub_js('      for (const todo of todos) {', '      const shown = todos.filter(t => filter === "all" || (filter === "done" ? t.done : !t.done));\n      for (const todo of shown) {')
P.sub_js('      count.textContent = `${left} ${left === 1 ? "item" : "items"} left`;', '      count.textContent = `${left} ${left === 1 ? "item" : "items"} left`;\n      document.querySelectorAll("[data-filter]").forEach(b => b.classList.toggle("active", b.dataset.filter === filter));')
P.sub_js('\n    render();', '\n    document.querySelectorAll("[data-filter]").forEach(button => {\n      button.addEventListener("click", () => {\n        filter = button.dataset.filter;\n        render();\n      });\n    });\n\n    render();')
S.append(step("td10", "Filters: all, active, done",
  ["A filter is just one more piece of state: `let filter = \"all\"`. `render()` shows only the to-dos that match it.",
   "`data-` attributes carry information on elements: `<button data-filter=\"done\">` is read in JavaScript as `button.dataset.filter`. One loop can wire up all three buttons."],
  "Add three buttons with `data-filter=\"all\"`, `\"active\"` and `\"done\"`. Clicking one sets `filter` and re-renders; `render()` shows only matching items and gives the chosen button the class `active`.",
  P.render(),
  [T("$$('#list li').length===1 && _text('#list li span')==='B'", "Active shows only unfinished items.", do=add_todo("A") + add_todo("B") + "_click('#list li input[type=checkbox]'); _click('[data-filter=active]');"),
   T("$$('#list li').length===1 && _text('#list li span')==='A'", "Done shows only finished items.", do=add_todo("A") + add_todo("B") + "_click('#list li input[type=checkbox]'); _click('[data-filter=done]');"),
   T("$$('#list li').length===2", "All shows everything again.", do=add_todo("A") + add_todo("B") + "_click('#list li input[type=checkbox]'); _click('[data-filter=done]'); _click('[data-filter=all]');"),
   T("$('[data-filter=active]').classList.contains('active') && !$('[data-filter=all]').classList.contains('active')", "The chosen filter button is highlighted.", do="_click('[data-filter=active]');")],
  ref=("MDN: HTMLElement.dataset", "https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/dataset")))
P.sub_js('    function toggle(id) {', '    function save() {\n      localStorage.setItem("todos", JSON.stringify(todos));\n    }\n\n    function toggle(id) {')
P.sub_js('    function render() {\n      list.innerHTML = "";', '    function render() {\n      save();\n      list.innerHTML = "";')
S.append(step("td11", "Save to localStorage",
  ["Refresh the page and everything's gone. `localStorage` keeps strings in the browser between visits. Arrays aren't strings, so convert with `JSON.stringify(todos)` when saving.",
   "Since every change already goes through `render()`, saving there means you can never forget to save."],
  "Write `save()` that stores `JSON.stringify(todos)` under the key `\"todos\"`, and call it at the start of `render()`.",
  P.render(),
  [T("JSON.parse(localStorage.getItem('todos'))[0].text==='Milk'", "Adding a to-do saves it under the key `todos`.", do=add_todo("Milk")),
   T("JSON.parse(localStorage.getItem('todos'))[0].done===true", "Ticking it off is saved too.", do=add_todo("Milk") + "_click('#list li input[type=checkbox]');")],
  ref=("MDN: Window.localStorage", "https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage")))
P.sub_js('    let todos = [];', '    let todos = JSON.parse(localStorage.getItem("todos")) || [];')
SEED = {"todos": '[{"id":1,"text":"Saved earlier","done":false},{"id":2,"text":"Already done","done":true}]'}
S.append(step("td12", "Load saved to-dos",
  ["Saving is half the job. When the page loads, read the list back with `JSON.parse(localStorage.getItem(\"todos\"))`.",
   "The first time anyone visits there's nothing saved, so `getItem` returns `null`. `|| []` falls back to an empty list. Your app is finished: it remembers everything between visits."],
  "Start `todos` from localStorage instead of `[]`, falling back to an empty array when nothing is saved.",
  P.render(),
  [T("$$('#list li').length===2 && _text('#list li span')==='Saved earlier'", "Saved to-dos appear when the page loads.", storage=SEED),
   T("$('#list li:last-child').classList.contains('done') && _text('#count')==='1 item left'", "Saved state (done, count) comes back too.", storage=SEED),
   T("$$('#list li').length===0", "With nothing saved, the list starts empty.", storage={})],
  storage=SEED))
project(id="todo-app", title="To-Do List App", lang="web", level="Beginner", hours="1.5 h", hue="#38d3f0", icon="checkc", art="☑ ☐",
  tagline="The classic first app: add, tick off, filter and save your tasks.",
  desc=["You'll build a complete to-do app from an empty file: an HTML form, CSS that makes it look like an app, and JavaScript that handles adding, completing, deleting and filtering, with everything saved in the browser.",
        "Along the way you'll learn the pattern behind React, Vue and every other framework: keep your data in an array, and re-draw the page from it whenever it changes."],
  final="A to-do app that adds tasks with Enter, ticks them off, deletes them, filters by status, counts what's left and remembers everything after a refresh.",
  skills=["HTML forms", "CSS flexbox", "DOM selection", "events", "arrays of objects", "render-from-state", "localStorage", "JSON"],
  prereq="the **Build Your First Web Page** bootcamp course, or knowing what HTML tags and CSS rules are.", core=["s4m1", "s4m2"],
  stretch=["Double-click a to-do to edit its text.", "Add a **Clear completed** button.", "Add due dates and sort by them.", "Drag to reorder (the HTML Drag and Drop API)."],
  milestones=[milestone("The page", "Structure and style: a form and a list that look like an app.", S[0:2]),
              milestone("Adding to-dos", "Make the form actually add items, safely.", S[2:5]),
              milestone("Done and delete", "Move the data into an array and render from it.", S[5:9]),
              milestone("Filters and saving", "Filter by status and remember everything between visits.", S[9:12])])

# =============================================================================================== CALCULATOR
P = Page("Calculator")
S = []
BLANK = P.render()
DIG = lambda d: f"_click('[data-digit=\"{d}\"]');"
OP = lambda o: f"_click('[data-op=\"{o}\"]');"
def keys(seq):
    out = []
    for k in seq.split():
        if k in "+-*/": out.append(OP(k))
        elif k == "=": out.append("_click('#equals');")
        elif k == "C": out.append("_click('#clear');")
        else: out.extend(DIG(c) for c in k)
    return " ".join(out)
P.body = ['  <main class="calc">', '    <div id="display">0</div>', '    <div class="keys">', '      <button id="clear">C</button>', '      <button data-op="/">÷</button>', '      <button data-op="*">×</button>', '      <button data-op="-">−</button>',
          '      <button data-digit="7">7</button>', '      <button data-digit="8">8</button>', '      <button data-digit="9">9</button>', '      <button data-op="+">+</button>',
          '      <button data-digit="4">4</button>', '      <button data-digit="5">5</button>', '      <button data-digit="6">6</button>', '      <button id="equals">=</button>',
          '      <button data-digit="1">1</button>', '      <button data-digit="2">2</button>', '      <button data-digit="3">3</button>', '      <button data-digit="0">0</button>',
          '      <button data-digit=".">.</button>', '    </div>', '  </main>']
S.append(step("ca1", "Buttons and a display",
  ["A calculator is a display and a grid of buttons. Instead of giving every button its own id, label them with **data attributes**: `data-digit=\"7\"` for digits and `data-op=\"+\"` for operators. Then one piece of JavaScript can handle all of them.",
   "The symbols people see (÷, ×) can differ from the values your code uses (`/`, `*`)."],
  "Inside `<main class=\"calc\">`, add `<div id=\"display\">0</div>` and a `<div class=\"keys\">` holding buttons for the digits 0–9 and `.` (each with `data-digit`), the four operators (each with `data-op` set to `+`, `-`, `*` or `/`), `<button id=\"equals\">` and `<button id=\"clear\">`.",
  P.render(),
  [T("_text('#display')==='0'", "The display starts at 0."), T("$$('[data-digit]').length===11", "There are 11 digit buttons (0–9 and `.`)."),
   T("['+','-','*','/'].every(o=>$(`[data-op=\"${o}\"]`))", "There are buttons for `+ - * /`."), T("!!$('#equals') && !!$('#clear')", "There are `#equals` and `#clear` buttons.")],
  starter=BLANK, ref=("MDN: HTMLElement.dataset", "https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/dataset")))
P.css = ['    body { font-family: system-ui, sans-serif; background: #0e1330; min-height: 100vh; margin: 0; display: grid; place-items: center; }',
         '    .calc { width: 280px; background: #1d2440; padding: 16px; border-radius: 20px; }',
         '    #display { background: #0a0d1c; color: white; font-size: 2.2rem; text-align: right; padding: 12px 16px; border-radius: 12px; margin-bottom: 12px; overflow-x: auto; }',
         '    .keys { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }',
         '    .keys button { padding: 16px 0; font-size: 1.2rem; border: 0; border-radius: 12px; background: #2c3560; color: white; cursor: pointer; }',
         '    .keys button[data-op], #equals { background: #8b7dff; }',
         '    #clear { background: #ff5c86; }']
S.append(step("ca2", "A grid of keys",
  ["CSS Grid is made for keypads. `grid-template-columns: repeat(4, 1fr)` makes four equal columns, and the buttons flow into them row by row.",
   "`display: grid; place-items: center` on the `body` (with `min-height: 100vh`) centres the calculator on the screen."],
  "Style the calculator: make `.keys` a grid with **four** equal columns and a gap, give the display a large right-aligned font, and colour the operator buttons differently from the digits.",
  P.render(),
  [T("getComputedStyle($('.keys')).display==='grid'", "`.keys` is a grid."), T("getComputedStyle($('.keys')).gridTemplateColumns.split(' ').length===4", "The grid has four columns."),
   T("getComputedStyle($('#display')).textAlign==='right'", "The display is right-aligned.")], ref=("CSS-Tricks: A complete guide to CSS Grid", "https://css-tricks.com/snippets/css/complete-guide-grid/")))
P.js = ['    const display = document.querySelector("#display");', '    let current = "0";', '',
        '    function show() {', '      display.textContent = current;', '    }', '',
        '    function inputDigit(d) {', '      current = current === "0" ? d : current + d;', '      show();', '    }', '',
        '    document.querySelectorAll("[data-digit]").forEach(button => {', '      button.addEventListener("click", () => inputDigit(button.dataset.digit));', '    });']
S.append(step("ca3", "Type a number",
  ["Keep what's on the display in a variable, `let current = \"0\"`. It's a **string**, not a number, because you're building it up character by character: `\"1\"` then `\"12\"`.",
   "One loop wires every digit button: `document.querySelectorAll(\"[data-digit]\")` returns them all, and `button.dataset.digit` tells you which digit was clicked."],
  "Write `inputDigit(d)`: if `current` is `\"0\"`, replace it with `d`, otherwise append `d`; then update the display. Wire every `[data-digit]` button to call it.",
  P.render(),
  [T("_text('#display')==='12'", "Clicking 1 then 2 shows 12.", do=keys("12")), T("_text('#display')==='7'", "Clicking 7 replaces the starting 0.", do=keys("7")),
   T("_text('#display')==='305'", "Zeros in the middle work: 3, 0, 5 shows 305.", do=keys("305"))], core="s4m1"))
P.sub_js('    function inputDigit(d) {\n      current = current === "0" ? d : current + d;', '    function inputDigit(d) {\n      if (d === "." && current.includes(".")) return;\n      current = current === "0" && d !== "." ? d : current + d;')
P.sub_js('    document.querySelectorAll("[data-digit]")', '    function clearAll() {\n      current = "0";\n      show();\n    }\n\n    document.querySelector("#clear").addEventListener("click", clearAll);\n\n    document.querySelectorAll("[data-digit]")')
S.append(step("ca4", "Decimals and clear",
  ["Two edge cases make a calculator feel solid. A number can only have **one** decimal point, so ignore a second `.`. And pressing `.` on `0` should give `0.`, not `.`.",
   "Clear resets everything back to the starting state. Write it as a function, `clearAll()`, because you'll add more state to reset soon."],
  "Make `.` work: ignore it if `current` already contains one, and keep the leading 0 (`0.5`). Make `#clear` reset the display to `0`.",
  P.render(),
  [T("_text('#display')==='1.5'", "1 . . 5 shows 1.5 (the second dot is ignored).", do=keys("1..5")),
   T("_text('#display')==='0.5'", ". then 5 shows 0.5.", do=keys(".5")),
   T("_text('#display')==='0'", "Clear resets to 0.", do=keys("123 C"))]))
P.sub_js('    let current = "0";', '    let current = "0";\n    let previous = null;\n    let operator = null;\n    let fresh = false;')
P.sub_js('    function inputDigit(d) {', '    function inputDigit(d) {\n      if (fresh) {\n        current = "0";\n        fresh = false;\n      }')
P.sub_js('    function clearAll() {\n      current = "0";', '    function calculate(a, b, op) {\n      if (op === "+") return a + b;\n      if (op === "-") return a - b;\n      if (op === "*") return a * b;\n      if (op === "/") return a / b;\n    }\n\n    function chooseOperator(op) {\n      previous = current;\n      operator = op;\n      fresh = true;\n    }\n\n    function equals() {\n      if (operator === null) return;\n      current = String(calculate(Number(previous), Number(current), operator));\n      operator = null;\n      previous = null;\n      fresh = true;\n      show();\n    }\n\n    function clearAll() {\n      current = "0";\n      previous = null;\n      operator = null;\n      fresh = false;')
P.sub_js('    document.querySelector("#clear").addEventListener("click", clearAll);', '    document.querySelector("#clear").addEventListener("click", clearAll);\n    document.querySelector("#equals").addEventListener("click", equals);\n    document.querySelectorAll("[data-op]").forEach(button => {\n      button.addEventListener("click", () => chooseOperator(button.dataset.op));\n    });')
S.append(step("ca5", "Operators and equals",
  ["When you press `+`, the calculator has to **remember** the first number and the operator, then let you type a second number. That's three pieces of state: `previous`, `operator`, and a flag `fresh` meaning *the next digit starts a new number*.",
   "`=` turns the strings into numbers with `Number(...)`, does the maths in a small `calculate(a, b, op)` function, and shows the result."],
  "Add `previous`, `operator` and `fresh`. Clicking an operator stores the current number and the operator; the next digit starts a new number. `#equals` calculates and shows the result. Clear must reset all of it.",
  P.render(),
  [T("_text('#display')==='15'", "12 + 3 = shows 15.", do=keys("12 + 3 =")), T("_text('#display')==='-3'", "7 − 10 = shows −3.", do=keys("7 - 10 =")),
   T("_text('#display')==='8'", "2 × 4 = shows 8.", do=keys("2 * 4 =")), T("_text('#display')==='3'", "9 ÷ 3 = shows 3.", do=keys("9 / 3 =")),
   T("_text('#display')==='3'", "After + the next digit starts a new number.", do=keys("12 + 3"))], core="s1m3"))
P.sub_js('    function chooseOperator(op) {\n      previous = current;', '    function chooseOperator(op) {\n      if (operator !== null && !fresh) {\n        current = String(calculate(Number(previous), Number(current), operator));\n        show();\n      }\n      previous = current;')
S.append(step("ca6", "Chain calculations",
  ["Real calculators let you chain: `2 + 3 + 4 =` gives 9. When an operator is pressed while one is already waiting (and a second number has been typed), calculate the pending result first and show it.",
   "The `fresh` flag prevents a bug: pressing `+` twice in a row shouldn't calculate anything."],
  "Make `chooseOperator` calculate the pending operation first when there is one and a new number has been typed.",
  P.render(),
  [T("_text('#display')==='9'", "2 + 3 + 4 = shows 9.", do=keys("2 + 3 + 4 =")), T("_text('#display')==='5'", "After 2 + 3 + the display shows 5.", do=keys("2 + 3 +")),
   T("_text('#display')==='12'", "10 − 4 × 2 = works left to right: 12.", do=keys("10 - 4 * 2 =")), T("_text('#display')==='5'", "Pressing + twice doesn't break it: 2 + + 3 = shows 5.", do=keys("2 + + 3 ="))]))
P.sub_js('      if (op === "/") return a / b;\n    }', '      if (op === "/") return b === 0 ? NaN : a / b;\n    }\n\n    function format(n) {\n      return Number.isFinite(n) ? String(Number(n.toFixed(10))) : "Error";\n    }')
P.sub_js('        current = String(calculate(Number(previous), Number(current), operator));\n        show();', '        current = format(calculate(Number(previous), Number(current), operator));\n        show();')
P.sub_js('      current = String(calculate(Number(previous), Number(current), operator));\n      operator = null;', '      current = format(calculate(Number(previous), Number(current), operator));\n      operator = null;')
S.append(step("ca7", "Floating point and dividing by zero",
  ["Try `0.1 + 0.2`: JavaScript says `0.30000000000000004`. Computers store decimals in binary, which can't represent 0.1 exactly. The fix for display is rounding: `Number(n.toFixed(10))` gives `0.3`.",
   "Dividing by zero gives `Infinity` in JavaScript. A calculator should say `Error` instead. `Number.isFinite(n)` is false for `Infinity` and `NaN`."],
  "Write `format(n)` that returns `\"Error\"` for non-finite numbers and otherwise rounds to 10 decimal places. Make division by zero produce an error, and use `format` for every result.",
  P.render(),
  [T("_text('#display')==='0.3'", "0.1 + 0.2 = shows 0.3.", do=keys(".1 + .2 =")), T("_text('#display')==='Error'", "5 ÷ 0 = shows Error.", do=keys("5 / 0 =")),
   T("_text('#display')==='0.3333333333'", "1 ÷ 3 = is rounded to 10 places.", do=keys("1 / 3 ="))],
  ref=("MDN: Number.prototype.toFixed", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed")))
P.js += ['', '    document.addEventListener("keydown", (event) => {', '      const k = event.key;', '      if ("0123456789.".includes(k)) inputDigit(k);',
         '      else if ("+-*/".includes(k)) chooseOperator(k);', '      else if (k === "Enter" || k === "=") equals();', '      else if (k === "Escape" || k.toLowerCase() === "c") clearAll();', '    });']
S.append(step("ca8", "Keyboard support",
  ["Clicking every key gets old. Listen for `keydown` on the whole `document`: `event.key` is the character pressed (`\"7\"`, `\"+\"`, `\"Enter\"`, `\"Escape\"`).",
   "Because your logic lives in functions, the keyboard handler is just a router that calls the same functions the buttons do."],
  "Add a `keydown` listener on `document`: digits and `.` call `inputDigit`, `+ - * /` call `chooseOperator`, Enter or `=` calls `equals`, Escape or `c` clears.",
  P.render(),
  [T("_text('#display')==='9'", "Typing 7 + 2 Enter shows 9.", do="['7','+','2','Enter'].forEach(k=>_press(document,k));"),
   T("_text('#display')==='0'", "Escape clears.", do="['5','5','Escape'].forEach(k=>_press(document,k));")],
  ref=("MDN: KeyboardEvent.key", "https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/key")))
P.css.append('    .keys button.active { outline: 3px solid white; }')
P.sub_js('    function show() {\n      display.textContent = current;\n    }', '    function show() {\n      display.textContent = current;\n    }\n\n    function highlight() {\n      document.querySelectorAll("[data-op]").forEach(b => b.classList.toggle("active", b.dataset.op === operator));\n    }')
P.sub_js('      previous = current;\n      operator = op;\n      fresh = true;\n    }', '      previous = current;\n      operator = op;\n      fresh = true;\n      highlight();\n    }')
P.sub_js('      fresh = true;\n      show();\n    }', '      fresh = true;\n      show();\n      highlight();\n    }')
P.sub_js('      fresh = false;\n      show();\n    }', '      fresh = false;\n      show();\n      highlight();\n    }')
S.append(step("ca9", "Show the chosen operator",
  ["Small feedback makes interfaces feel trustworthy. While an operator is waiting, highlight its button so people know what will happen.",
   "`classList.toggle(\"active\", condition)` adds the class when the condition is true and removes it otherwise. That's perfect for syncing styles with state."],
  "Write `highlight()` that gives the `active` class to the operator button matching `operator` (and removes it from the rest). Call it whenever `operator` changes: choosing, equals and clear.",
  P.render(),
  [T("$('[data-op=\"+\"]').classList.contains('active') && $$('.keys .active').length===1", "Choosing + highlights only the + key.", do=keys("1 +")),
   T("$$('.keys .active').length===0", "Equals removes the highlight.", do=keys("1 + 2 =")),
   T("$$('.keys .active').length===0", "Clear removes the highlight.", do=keys("1 * C"))]))
project(id="calculator", title="Calculator", lang="web", level="Beginner", hours="1.5 h", hue="#8b7dff", icon="grid", art="7 8 9 ÷",
  tagline="A real calculator with chaining, decimals, keyboard support and no floating-point surprises.",
  desc=["You'll build a working calculator, the kind that's on every phone, from a grid of buttons to correct maths. It's a perfect first lesson in **state**: what the program has to remember between clicks.",
        "You'll also meet real-world edge cases that tutorials skip: double decimal points, chained operations, dividing by zero and why `0.1 + 0.2` isn't `0.3`."],
  final="A calculator with a CSS Grid keypad that adds, subtracts, multiplies and divides, chains operations, handles decimals and errors, highlights the waiting operator and works from the keyboard.",
  skills=["CSS Grid", "data attributes", "event delegation", "state variables", "functions", "floating point", "keyboard events"],
  prereq="the **Build Your First Web Page** bootcamp course.", core=["s4m1", "s1m3"],
  stretch=["Add `%` and `±` keys.", "Show the pending expression (like `12 +`) above the result.", "Keep a history of past calculations.", "Support backspace to delete the last digit."],
  milestones=[milestone("The keypad", "HTML buttons and a CSS Grid layout.", S[0:2]), milestone("Typing numbers", "Build numbers digit by digit, with decimals and clear.", S[2:4]),
              milestone("Doing maths", "Operators, equals, chaining and the edge cases.", S[4:7]), milestone("Polish", "Keyboard support and visual feedback.", S[7:9])])

# =============================================================================================== QUIZ GAME
P = Page("Code Quiz")
S = []
BLANK = P.render()
P.css = ['    [hidden] { display: none !important; }']
P.body = ['  <main class="quiz-app">', '    <section id="quiz">', '      <p id="progress"></p>', '      <h2 id="question"></h2>', '      <div id="options"></div>', '      <p id="score">Score: 0</p>', '      <button id="next" hidden>Next</button>', '    </section>',
          '    <section id="result" hidden>', '      <h2>Quiz complete</h2>', '      <p id="result-text"></p>', '      <button id="restart">Play again</button>', '    </section>', '  </main>']
S.append(step("qz1", "Two screens in one page",
  ["A quiz has two screens: the questions and the result. Rather than two pages, build both as `<section>`s and show one at a time with the `hidden` attribute.",
   "Leave the question and options empty. JavaScript will fill them in."],
  "Inside `<main class=\"quiz-app\">`, add `<section id=\"quiz\">` containing `p#progress`, `h2#question`, `div#options`, `<p id=\"score\">Score: 0</p>` and a hidden `button#next`. Then a hidden `<section id=\"result\">` with `p#result-text` and `button#restart`. Keep the `[hidden]` CSS rule.",
  P.render(),
  [T("!!$('#quiz #question') && !!$('#quiz #options') && !!$('#quiz #progress')", "The quiz section has `#progress`, `#question` and `#options`."),
   T("_text('#score')==='Score: 0'", "`#score` starts at `Score: 0`."), T("$('#next').hidden===true", "`#next` starts hidden."),
   T("$('#result').hidden===true && !!$('#result #result-text') && !!$('#result #restart')", "A hidden `#result` section has `#result-text` and `#restart`.")], starter=BLANK))
P.css += ['    body { font-family: system-ui, sans-serif; background: #0e1330; color: #e9ecff; margin: 0; padding: 40px 16px; }',
          '    .quiz-app { max-width: 560px; margin: 0 auto; background: #151b33; padding: 28px; border-radius: 18px; }',
          '    #progress { color: #8e97c0; font-size: .9rem; }',
          '    #options { display: grid; gap: 10px; margin: 18px 0; }',
          '    #options button { text-align: left; padding: 14px 16px; border-radius: 12px; border: 2px solid #2a3460; background: #0e1324; color: inherit; font: inherit; cursor: pointer; }',
          '    #options button.correct { border-color: #34d399; background: #0c2c22; }',
          '    #options button.wrong { border-color: #ff7a7a; background: #3a1418; }',
          '    #next, #restart { padding: 10px 18px; border: 0; border-radius: 10px; background: #8b7dff; color: #0a0b1a; font-weight: 600; cursor: pointer; }']
S.append(step("qz2", "Style the quiz",
  ["Answer buttons should be big, easy targets stacked in a column: `display: grid; gap: 10px` on `#options` does exactly that.",
   "Plan the feedback styles now: a `.correct` class (green) and a `.wrong` class (red) that JavaScript will add after an answer."],
  "Give the app a card style, make `#options` a grid column with a gap, and add `.correct` and `.wrong` styles for answer buttons with clearly different border colours.",
  P.render(),
  [T("getComputedStyle($('#options')).display==='grid'", "`#options` is a grid."),
   dict(src="\\.correct\\s*\\{", msg="There's a `.correct` style."), dict(src="\\.wrong\\s*\\{", msg="There's a `.wrong` style.")]))
QS = ['    const questions = [',
      '      { q: "Which keyword declares a variable that can\'t be reassigned?", options: ["let", "var", "const"], answer: 2 },',
      '      { q: "What does HTML stand for?", options: ["HyperText Markup Language", "High Tech Modern Language", "Home Tool Markup Language"], answer: 0 },',
      '      { q: "Which CSS property sets the text colour?", options: ["font-color", "color", "text-colour"], answer: 1 },',
      '      { q: "What is 7 % 3 in JavaScript?", options: ["1", "2", "0.33"], answer: 0 },',
      '      { q: "Which array method adds an item to the end?", options: ["shift", "pop", "push"], answer: 2 },',
      '    ];']
P.js = list(QS)
S.append(step("qz3", "Questions as data",
  ["Don't hard-code questions into HTML. Store them as **data**: an array of objects, each with the question text, its options and the index of the right answer.",
   "Data-driven code scales: adding a question becomes one line, with no new HTML or logic."],
  "In a `<script>`, create `const questions` with at least 3 objects shaped `{ q: \"...\", options: [\"...\", ...], answer: indexOfCorrectOption }`.",
  P.render(),
  [T("Array.isArray(questions) && questions.length>=3", "`questions` is an array of at least 3."),
   T("questions.every(x=>typeof x.q==='string' && Array.isArray(x.options) && x.options.length>=2)", "Each has a `q` string and at least two `options`."),
   T("questions.every(x=>Number.isInteger(x.answer) && x.answer>=0 && x.answer<x.options.length)", "Each `answer` is a valid index into its options.")], core="s1m4"))
P.js += ['', '    let index = 0;', '    let score = 0;', '    const questionEl = document.querySelector("#question");', '    const optionsEl = document.querySelector("#options");', '    const progressEl = document.querySelector("#progress");', '',
         '    function showQuestion() {', '      const item = questions[index];', '      questionEl.textContent = item.q;', '      progressEl.textContent = `Question ${index + 1} of ${questions.length}`;', '      optionsEl.innerHTML = "";',
         '      item.options.forEach((text, i) => {', '        const button = document.createElement("button");', '        button.textContent = text;', '        optionsEl.append(button);', '      });', '    }', '', '    showQuestion();']
S.append(step("qz4", "Show a question",
  ["The current question is just a number, `index`. `showQuestion()` reads `questions[index]` and paints it: the text, the progress line and one button per option.",
   "Clearing with `optionsEl.innerHTML = \"\"` first means the function can be called again for the next question without duplicating buttons."],
  "Add `let index = 0` and `let score = 0`. Write `showQuestion()` that fills `#question`, sets `#progress` to `Question 1 of N`, and creates a button for each option inside `#options`. Call it on load.",
  P.render(),
  [T("_text('#question')===questions[0].q", "The first question's text is shown."), T("$$('#options button').length===questions[0].options.length", "There's one button per option."),
   T("_text('#progress')===`Question 1 of ${questions.length}`", "Progress shows `Question 1 of N`.")]))
P.sub_js('    const progressEl = document.querySelector("#progress");', '    const progressEl = document.querySelector("#progress");\n    const scoreEl = document.querySelector("#score");\n    const nextBtn = document.querySelector("#next");')
P.sub_js('        button.textContent = text;', '        button.textContent = text;\n        button.addEventListener("click", () => choose(i));')
P.sub_js('    showQuestion();', '    function choose(i) {\n      const item = questions[index];\n      const buttons = optionsEl.querySelectorAll("button");\n      buttons.forEach((b, j) => {\n        b.disabled = true;\n        if (j === item.answer) b.classList.add("correct");\n      });\n      if (i === item.answer) score++;\n      else buttons[i].classList.add("wrong");\n      scoreEl.textContent = `Score: ${score}`;\n      nextBtn.hidden = false;\n    }\n\n    showQuestion();')
RIGHT = "$$('#options button')[questions[0].answer].click();"
WRONG = "$$('#options button')[(questions[0].answer+1)%questions[0].options.length].click();"
S.append(step("qz5", "Choose an answer",
  ["Each option button calls `choose(i)` with its own index. An **arrow function** inside `forEach` remembers the `i` it was created with: that's a **closure**.",
   "After an answer: lock all buttons (`disabled = true`), always reveal the correct one, mark a wrong pick red, update the score and show **Next**."],
  "Write `choose(i)`: disable every option, add `correct` to the right one, add `wrong` to the clicked one if it was wrong, add 1 to `score` for a right answer, update `#score`, and un-hide `#next`.",
  P.render(),
  [T("$$('#options button')[questions[0].answer].classList.contains('correct') && _text('#score')==='Score: 1'", "A right answer turns green and scores a point.", do=RIGHT),
   T("$$('#options .wrong').length===1 && $$('#options .correct').length===1 && _text('#score')==='Score: 0'", "A wrong answer turns red and the right one is revealed.", do=WRONG),
   T("$$('#options button').every(b=>b.disabled) && $('#next').hidden===false", "Answering locks the options and shows Next.", do=RIGHT)], core="s1m3"))
P.sub_js('    function choose(i) {', '    nextBtn.addEventListener("click", () => {\n      index++;\n      showQuestion();\n    });\n\n    function choose(i) {')
P.sub_js('        optionsEl.append(button);\n      });\n    }', '        optionsEl.append(button);\n      });\n      nextBtn.hidden = true;\n    }')
S.append(step("qz6", "Next question",
  ["**Next** moves `index` forward and calls `showQuestion()` again. Because `showQuestion` clears and rebuilds the options, nothing from the previous question leaks through.",
   "Hide **Next** again whenever a new question appears, so people have to answer before moving on."],
  "Make `#next` increase `index` and show the next question. `showQuestion()` should hide `#next`.",
  P.render(),
  [T("_text('#progress')===`Question 2 of ${questions.length}` && _text('#question')===questions[1].q", "Next shows question 2.", do=RIGHT + "_click('#next');"),
   T("$('#next').hidden===true && $$('#options button').every(b=>!b.disabled)", "The new question's options are fresh and Next is hidden.", do=RIGHT + "_click('#next');")]))
ALL_RIGHT = "for (let k = 0; k < questions.length; k++) { $$('#options button')[questions[k].answer].click(); _click('#next'); }"
P.sub_js('      index++;\n      showQuestion();', '      index++;\n      if (index < questions.length) showQuestion();\n      else showResult();')
P.sub_js('    function choose(i) {', '    function showResult() {\n      document.querySelector("#quiz").hidden = true;\n      document.querySelector("#result").hidden = false;\n      document.querySelector("#result-text").textContent = `You scored ${score} out of ${questions.length}.`;\n    }\n\n    function choose(i) {')
S.append(step("qz7", "The result screen",
  ["When `index` runs past the last question, swap screens: hide `#quiz`, un-hide `#result` and write the final score.",
   "Checking `index < questions.length` before showing a question is a **bounds check**: forget it and `questions[index]` is `undefined`, which crashes on `.q`."],
  "After the last question, **Next** should call `showResult()`, which hides `#quiz`, shows `#result` and sets `#result-text` to `You scored X out of N.`",
  P.render(),
  [T("$('#quiz').hidden && !$('#result').hidden", "After the last question the result screen replaces the quiz.", do=ALL_RIGHT),
   T("_text('#result-text')===`You scored ${questions.length} out of ${questions.length}.`", "It shows `You scored X out of N.`", do=ALL_RIGHT)]))
P.sub_body('      <p id="result-text"></p>', '      <p id="result-text"></p>\n      <p id="best"></p>')
P.sub_js('      document.querySelector("#result-text").textContent = `You scored ${score} out of ${questions.length}.`;', '      document.querySelector("#result-text").textContent = `You scored ${score} out of ${questions.length}.`;\n      const best = Math.max(score, Number(localStorage.getItem("bestScore")) || 0);\n      localStorage.setItem("bestScore", best);\n      document.querySelector("#best").textContent = `Best score: ${best}`;')
P.sub_js('    function choose(i) {', '    document.querySelector("#restart").addEventListener("click", () => {\n      index = 0;\n      score = 0;\n      scoreEl.textContent = "Score: 0";\n      document.querySelector("#result").hidden = true;\n      document.querySelector("#quiz").hidden = false;\n      showQuestion();\n    });\n\n    function choose(i) {')
S.append(step("qz8", "Play again and keep a best score",
  ["**Play again** resets the state (`index`, `score`), swaps the screens back and shows question 1.",
   "A best score that survives a refresh lives in `localStorage`. `Math.max(score, saved)` keeps the higher one; `Number(...) || 0` handles the first game, when nothing is saved."],
  "Add `<p id=\"best\"></p>` to the result screen. On the result, save the higher of this score and the saved `bestScore`, and show `Best score: N`. Make `#restart` reset everything and show question 1.",
  P.render(),
  [T("_text('#progress')===`Question 1 of ${questions.length}` && _text('#score')==='Score: 0' && !$('#quiz').hidden", "Play again starts over at question 1 with score 0.", do=ALL_RIGHT + "_click('#restart');"),
   T("localStorage.getItem('bestScore')===String(questions.length) && _text('#best')===`Best score: ${questions.length}`", "A perfect game saves and shows the best score.", do=ALL_RIGHT),
   T("_text('#best')==='Best score: 99'", "A higher saved best score is kept.", do=ALL_RIGHT, storage={"bestScore": "99"})]))
project(id="quiz-game", title="Quiz Game", lang="web", level="Intermediate", hours="2 h", hue="#ff5c93", icon="target", art="A B C ?",
  tagline="A multiple-choice quiz with instant feedback, scoring, a results screen and a saved best score.",
  desc=["You'll build a quiz app driven entirely by data: questions live in an array, and the same few functions handle any number of them. It's the shape of most real interactive apps.",
        "You'll practise closures, showing and hiding screens, guarding against out-of-range indexes and persisting a high score."],
  final="A quiz that shows one question at a time, marks answers right or wrong instantly, tracks the score, shows a result screen with your best score, and lets you play again.",
  skills=["data-driven UI", "arrays of objects", "closures", "show/hide screens", "state resets", "localStorage"],
  prereq="the **JavaScript from Zero** bootcamp course, or the To-Do List project.", core=["s4m1", "s1m4"],
  stretch=["Shuffle the questions (and the options) each game.", "Add a 15-second timer per question.", "Load questions from a JSON file with `fetch`.", "Add categories and let players choose one."],
  milestones=[milestone("Screens", "Build the quiz and result screens and style them.", S[0:2]), milestone("Questions", "Store questions as data and render one.", S[2:4]),
              milestone("Playing", "Answer, score and move through the quiz.", S[4:6]), milestone("Finishing", "Results, replay and a saved best score.", S[6:8])])
