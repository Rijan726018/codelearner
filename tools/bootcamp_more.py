"""More Bootcamp courses, appended to bootcamp_src.C. Same format as tools/bootcamp_src.py; `web` steps use the
checks described in tools/projects_src/_lib.py."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "projects_src"))
from _lib import Page
from bootcamp_src import C


def chain(store):
    """Returns a helper that appends a step whose solution is the previous solution plus `add_code`."""
    def add(id, title, body, task, add_code, tests, hint=None, example=None, ref=None):
        prev = store[-1]["solution"] if store else ""
        s = dict(id=id, title=title, body=body, task=task, solution=prev + add_code, tests=tests)
        if hint: s["hint"] = hint
        if example: s["example"] = example
        if ref: s["ref"] = ref
        store.append(s)
    return add


def T(js, msg, do=None, **k):
    d = dict(js=js, msg=msg, **k)
    if do: d["do"] = do
    return d


# =====================================================================================================  JS & THE DOM
P = Page("Tip Calculator")
BLANK = P.render()
D = []
def dom(id, title, body, task, tests, **k):
    D.append(dict(id=id, title=title, body=body, task=task, solution=P.render(), tests=tests, **k))

P.body = ['  <h1>Tip Calculator</h1>',
          '  <label>Bill <input id="bill" type="number" min="0" step="0.01" placeholder="0.00"></label>',
          '  <label>People <input id="people" type="number" min="1" value="1"></label>',
          '  <p>Tip: <output id="tip-amount">-</output></p>',
          '  <p>Each person pays: <output id="per-person">-</output></p>']
dom("d1", "The calculator's HTML",
 ["JavaScript changes pages that already exist, so every DOM project starts with HTML. This course builds a tip calculator: type a bill, pick a tip, split it between friends.",
  "Give every element your code will touch an `id`. `<output>` is an element made for showing a calculated result; until the code runs it shows a dash."],
 "Add an `<h1>` saying `Tip Calculator`, a number `<input id=\"bill\">`, a number `<input id=\"people\" value=\"1\">`, and two outputs: `<output id=\"tip-amount\">` and `<output id=\"per-person\">`, each containing `-`.",
 [T("_text('h1')==='Tip Calculator'", "The `h1` says Tip Calculator."), T("$('#bill')&&$('#bill').type==='number'", "There's a number input `#bill`."),
  T("$('#people')&&$('#people').value==='1'", "There's an input `#people` starting at 1."), T("!!$('#tip-amount')&&!!$('#per-person')", "There are elements `#tip-amount` and `#per-person`.")],
 starter=BLANK, hint="`<input id=\"people\" type=\"number\" min=\"1\" value=\"1\">` — wrapping each input in a `<label>` makes the text clickable.",
 ref=("MDN: The output element", "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/output"))

P.body = ['  <main class="calc">'] + ['  ' + l for l in P.body] + ['  </main>']
P.css = ['    [hidden] { display: none !important; }',
         '    body { font-family: system-ui, sans-serif; background: #e8f6f3; margin: 0; padding: 40px 16px; }',
         '    .calc { max-width: 360px; margin: 0 auto; background: white; padding: 24px; border-radius: 16px; }',
         '    label { display: block; margin: 12px 0; }',
         '    input { display: block; width: 100%; box-sizing: border-box; padding: 10px; font: inherit; }',
         '    output { font-weight: bold; }']
dom("d2", "Style it as a card",
 ["Wrap the calculator in `<main class=\"calc\">` and give it a `max-width`, so it stays a sensible size on a wide screen.",
  "`display: block` on the labels and inputs stacks them vertically; `box-sizing: border-box` makes `width: 100%` include the padding, so inputs never overflow the card."],
 "Wrap everything in `<main class=\"calc\">`. Give `.calc` a `max-width`, a white background, padding and a `border-radius`. Make `input` elements `display: block` with `width: 100%`.",
 [T("!!$('main.calc #bill')", "Everything is inside `main.calc`."), T("getComputedStyle($('.calc')).maxWidth!=='none'", "`.calc` has a `max-width`."),
  T("getComputedStyle($('.calc')).borderTopLeftRadius!=='0px'", "`.calc` has rounded corners."), T("getComputedStyle($('#bill')).display==='block'", "Inputs are `display: block`.")])

P.js = ['    const bill = document.querySelector("#bill");',
        '    const people = document.querySelector("#people");',
        '    const tipAmount = document.querySelector("#tip-amount");',
        '    const perPerson = document.querySelector("#per-person");',
        '',
        '    tipAmount.textContent = "$0.00";',
        '    perPerson.textContent = "$0.00";']
dom("d3", "Find elements, change text",
 ["The **DOM** (Document Object Model) is the browser's live version of your HTML. `document.querySelector(\"#bill\")` returns the first element matching a CSS selector, and you keep it in a `const` to use later.",
  "Setting `element.textContent` replaces the text inside it. That's the simplest way JavaScript changes a page."],
 "Add a `<script>` at the end of `<body>`. Select `#bill`, `#people`, `#tip-amount` and `#per-person` into constants, then set both outputs' text to `$0.00`.",
 [T("_text('#tip-amount')==='$0.00'&&_text('#per-person')==='$0.00'", "Both outputs show `$0.00` once the page loads."), dict(src="querySelector", msg="You used `document.querySelector`.")],
 hint="`const tipAmount = document.querySelector(\"#tip-amount\");` then `tipAmount.textContent = \"$0.00\";`",
 ref=("MDN: Document.querySelector", "https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector"))

P.js += ['', '    function update() {', '      console.log(bill.value);', '    }', '', '    bill.addEventListener("input", update);']
dom("d4", "React to typing",
 ["`addEventListener(\"input\", update)` runs your function every time the value changes, keystroke by keystroke. Pass the function itself (`update`), not the result of calling it (`update()`).",
  "An input's `.value` is always a **string**, even for `type=\"number\"`. You'll convert it next."],
 "Write a function `update()` that logs `bill.value`, and register it for the `input` event on `bill`. Type in the bill box and watch the console.",
 [T("_logs().includes('42')", "Typing in `#bill` logs its value.", do="_type('#bill','42');"), dict(src="addEventListener\\(\\s*[\"']input", msg="You listen for the `input` event.")],
 hint="`bill.addEventListener(\"input\", update);`")

P.sub_js('      console.log(bill.value);', '      const amount = Number(bill.value);\n      const tip = amount * 0.15;\n      tipAmount.textContent = "$" + tip.toFixed(2);')
dom("d5", "Do the maths",
 ["`Number(\"12.4\")` turns text into a number you can calculate with. An empty box gives `Number(\"\")`, which is `0`: handy here.",
  "Money needs exactly two decimals. `tip.toFixed(2)` returns a string like `\"1.86\"`."],
 "In `update()`, convert the bill to a number, work out a 15% tip, and show it in `#tip-amount` as `$` plus the amount with two decimals.",
 [T("_text('#tip-amount')==='$15.00'", "A bill of 100 shows a tip of `$15.00`.", do="_type('#bill','100');"),
  T("_text('#tip-amount')==='$1.86'", "A bill of 12.40 shows `$1.86`.", do="_type('#bill','12.40');")],
 example='const n = Number("19.5");   // 19.5\n(n * 0.2).toFixed(2);       // "3.90"')

P.sub_js('      tipAmount.textContent = "$" + tip.toFixed(2);', '      const count = Number(people.value);\n      tipAmount.textContent = "$" + tip.toFixed(2);\n      perPerson.textContent = "$" + ((amount + tip) / count).toFixed(2);')
P.sub_js('    bill.addEventListener("input", update);', '    bill.addEventListener("input", update);\n    people.addEventListener("input", update);')
dom("d6", "Split the bill",
 ["Each person pays an equal share of the bill **plus** the tip. One `update()` can serve several inputs: register it on `people` too, so changing either box recalculates."],
 "Show `(bill + tip) / people` in `#per-person`, with two decimals. Make typing in `#people` update the result as well.",
 [T("_text('#per-person')==='$28.75'", "A bill of 100 split 4 ways shows `$28.75`.", do="_type('#bill','100'); _type('#people','4');"),
  T("_text('#per-person')==='$57.50'", "Changing people recalculates.", do="_type('#people','4'); _type('#bill','100'); _type('#people','2');")])

P.sub_body('    <label>People', '    <div class="tips">\n      <button data-tip="10">10%</button>\n      <button data-tip="15" class="active">15%</button>\n      <button data-tip="20">20%</button>\n    </div>\n    <label>People')
P.css += ['    .tips { display: flex; gap: 8px; }',
          '    .tips button { flex: 1; padding: 10px; border: 0; border-radius: 8px; background: #d5eee9; font: inherit; cursor: pointer; }',
          '    .tips button.active { background: #0f766e; color: white; }']
P.sub_js('    function update() {', '    let tipPercent = 15;\n    const tipButtons = document.querySelectorAll(".tips button");\n\n    function update() {')
P.sub_js('      const tip = amount * 0.15;', '      const tip = amount * tipPercent / 100;')
P.js += ['', '    for (const button of tipButtons) {', '      button.addEventListener("click", () => {', '        tipPercent = Number(button.dataset.tip);',
         '        for (const b of tipButtons) b.classList.remove("active");', '        button.classList.add("active");', '        update();', '      });', '    }']
dom("d7", "Tip buttons",
 ["`data-*` attributes store your own information on an element. `<button data-tip=\"20\">` is read in JavaScript as `button.dataset.tip` (a string, so convert it).",
  "`querySelectorAll` returns every match. Loop over them to add a click listener to each. `classList.add` and `classList.remove` switch the highlighted button."],
 "Add three buttons in a `<div class=\"tips\">` with `data-tip` 10, 15 and 20 (15 has the class `active`). Keep the percentage in `let tipPercent = 15;`. Clicking a button sets it, moves the `active` class, and recalculates.",
 [T("_text('#tip-amount')==='$10.00'", "Choosing 20% on a bill of 50 shows `$10.00`.", do="_click('[data-tip=\"20\"]'); _type('#bill','50');"),
  T("_text('#tip-amount')==='$5.00'", "Clicking after typing recalculates straight away.", do="_type('#bill','50'); _click('[data-tip=\"10\"]');"),
  T("$('[data-tip=\"20\"]').classList.contains('active')&&$$('.tips .active').length===1", "Only the clicked button has the class `active`.", do="_click('[data-tip=\"20\"]');")],
 ref=("MDN: Using data attributes", "https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes"))

P.sub_body('    <p>Tip:', '    <p id="error" hidden>Enter at least 1 person.</p>\n    <p>Tip:')
P.css.append('    #error { color: #b91c1c; }')
P.sub_js('    const perPerson = document.querySelector("#per-person");', '    const perPerson = document.querySelector("#per-person");\n    const error = document.querySelector("#error");')
P.sub_js('      const count = Number(people.value);', '      const count = Number(people.value);\n      error.hidden = count >= 1;\n      if (count < 1) {\n        perPerson.textContent = "-";\n        return;\n      }')
dom("d8", "Guard against bad input",
 ["Dividing by 0 people gives `Infinity`, which is not a price. Check input before using it, show a helpful message, and stop early with `return`.",
  "The `hidden` attribute hides an element; in JavaScript `element.hidden = true` or `false` toggles it. (Your CSS rule `[hidden] { display: none !important; }` makes sure nothing overrides it.)"],
 "Add `<p id=\"error\" hidden>Enter at least 1 person.</p>`. In `update()`, show the error and set `#per-person` to `-` when people is less than 1; hide the error otherwise.",
 [T("!$('#error').hidden&&_text('#per-person')==='-'", "0 people shows the error and no per-person amount.", do="_type('#bill','100'); _type('#people','0');"),
  T("$('#error').hidden&&_text('#per-person')==='$57.50'", "Fixing the input hides the error again.", do="_type('#bill','100'); _type('#people','0'); _type('#people','2');"),
  T("$('#error').hidden", "The error is hidden when the page loads.")])

P.sub_body('  </main>', '    <button id="reset">Reset</button>\n  </main>')
P.css.append('    #reset { margin-top: 12px; width: 100%; padding: 10px; border: 1px solid #0f766e; border-radius: 8px; background: white; color: #0f766e; font: inherit; cursor: pointer; }')
P.sub_js('    for (const button of tipButtons) {', '''    function setTip(percent) {
      tipPercent = percent;
      for (const b of tipButtons) b.classList.toggle("active", Number(b.dataset.tip) === percent);
      update();
    }

    for (const button of tipButtons) {''')
P.sub_js('''        tipPercent = Number(button.dataset.tip);
        for (const b of tipButtons) b.classList.remove("active");
        button.classList.add("active");
        update();''', '        setTip(Number(button.dataset.tip));')
P.js += ['', '    document.querySelector("#reset").addEventListener("click", () => {', '      bill.value = "";', '      people.value = "1";', '      setTip(15);', '    });']
dom("d9", "Reset, and a small refactor",
 ["Reset needs to choose a tip button too, and that code already lives in the click handler. Move it into a function `setTip(percent)` and call it from both places: one source of truth.",
  "`classList.toggle(\"active\", condition)` adds the class when the condition is true and removes it otherwise, which replaces the remove-all-then-add dance."],
 "Write `setTip(percent)` and use it in the tip buttons. Add `<button id=\"reset\">Reset</button>`: clicking it empties the bill, sets people back to 1 and the tip back to 15%.",
 [T("$('#bill').value===''&&$('#people').value==='1'&&_text('#tip-amount')==='$0.00'", "Reset clears the bill and people, and the outputs.", do="_type('#bill','80'); _type('#people','3'); _click('#reset');"),
  T("$('[data-tip=\"15\"]').classList.contains('active')&&tipPercent===15", "Reset selects 15% again.", do="_click('[data-tip=\"20\"]'); _click('#reset');"),
  T("typeof setTip==='function'", "There's a `setTip` function.")])

P.sub_js('    let tipPercent = 15;', '    let tipPercent = 15;\n    const saved = Number(localStorage.getItem("tip"));')
P.sub_js('      tipPercent = percent;', '      tipPercent = percent;\n      localStorage.setItem("tip", String(percent));')
P.js += ['', '    setTip(saved || 15);']
dom("d10", "Remember the favourite tip",
 ["`localStorage` keeps small strings in the browser, even after the tab closes. `localStorage.setItem(\"tip\", \"20\")` saves; `localStorage.getItem(\"tip\")` reads it back, or gives `null` if nothing was saved.",
  "`Number(null)` is `0`, and `0 || 15` is `15`, so `saved || 15` gives a sensible default for first-time visitors. You built a complete, interactive app."],
 "Save the tip percentage in `localStorage` whenever `setTip` runs. When the page loads, read it back and call `setTip` with it, or with 15 if nothing was saved.",
 [T("localStorage.getItem('tip')==='20'", "Choosing 20% saves it.", do="_click('[data-tip=\"20\"]');"),
  T("$('[data-tip=\"10\"]').classList.contains('active')&&_text('#tip-amount')==='$10.00'", "A saved 10% is selected when the page loads.", do="_type('#bill','100');", storage={"tip": "10"}),
  T("$('[data-tip=\"15\"]').classList.contains('active')", "With nothing saved, 15% is selected.", storage={})],
 ref=("MDN: Window.localStorage", "https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage"))

C.append(dict(id="js-dom", title="JavaScript & the DOM", lang="web", hue="#2dd4bf", icon="monitor", art="DOM", hours="2 h",
 tagline="Make web pages react to people.",
 desc="Select elements, listen for typing and clicks, update the page and remember settings, by building a tip calculator that splits the bill. Take JavaScript from Zero first.",
 project="a tip calculator that splits the bill", steps=D))

# =====================================================================================================  PYTHON DATA & OOP
OO = []
oo = chain(OO)
oo("o1", "A list of dictionaries",
 ["Real data is usually a **list of records**. In Python each record is a dictionary, so a whole table is a list of dicts.",
  "This course builds a small library system. Start with the books."],
 "Create `books`: a list of 4 dictionaries, each with the keys `title`, `author` and `year`. Use these: *Dune* (Frank Herbert, 1965), *Emma* (Jane Austen, 1815), *Persuasion* (Jane Austen, 1817), *Neuromancer* (William Gibson, 1984). Print how many books there are.",
 'books = [\n    {"title": "Dune", "author": "Frank Herbert", "year": 1965},\n    {"title": "Emma", "author": "Jane Austen", "year": 1815},\n    {"title": "Persuasion", "author": "Jane Austen", "year": 1817},\n    {"title": "Neuromancer", "author": "William Gibson", "year": 1984},\n]\nprint(len(books))\n',
 [dict(py='len(books) == 4 and all({"title", "author", "year"} <= set(b) for b in books)', msg="`books` has 4 dicts with title, author and year."),
  dict(py='sorted(b["title"] for b in books) == ["Dune", "Emma", "Neuromancer", "Persuasion"]', msg="The titles match the four books."), dict(outHas="4", msg="It prints 4.")],
 example='people = [{"name": "Ada", "age": 36}, {"name": "Alan", "age": 41}]')
oo("o2", "List comprehensions",
 ["A **comprehension** builds a list in one line: `[expression for item in items]`. Add `if condition` at the end to filter.",
  "It reads like English: *the title, for each book in books, if it was published before 1900*."],
 "Make `titles`, a list of every title, and `classics`, the titles of books published before 1900. Print both.",
 '\ntitles = [b["title"] for b in books]\nclassics = [b["title"] for b in books if b["year"] < 1900]\nprint(titles)\nprint(classics)\n',
 [dict(py='titles == [b["title"] for b in books]', msg="`titles` lists every title in order."), dict(py='classics == ["Emma", "Persuasion"]', msg="`classics` is Emma and Persuasion."),
  dict(src="\\[.+for .+ in .+\\]", msg="You used a list comprehension.")])
oo("o3", "Sorting with a key",
 ["`sorted(items, key=...)` sorts by whatever the key function returns. `lambda b: b[\"year\"]` is a tiny unnamed function returning a book's year.",
  "Add `reverse=True` for largest first. `sorted` returns a new list; the original is untouched."],
 "Make `by_year`: the books sorted oldest first. Print the title of the newest book (the last one).",
 '\nby_year = sorted(books, key=lambda b: b["year"])\nprint(by_year[-1]["title"])\n',
 [dict(py='[b["year"] for b in by_year] == [1815, 1817, 1965, 1984]', msg="`by_year` is sorted by year."), dict(py='_out.splitlines()[-1] == "Neuromancer"', msg="It prints Neuromancer last."),
  dict(py='books[0]["title"] == "Dune"', msg="`books` keeps its original order.")])
oo("o4", "Sets for unique values",
 ["A **set** holds each value at most once and checks membership instantly. `{expression for item in items}` is a set comprehension.",
  "Sets have no order, so sort them when you print."],
 "Make `authors`, a set of every author. Print them sorted, joined with `, `.",
 '\nauthors = {b["author"] for b in books}\nprint(", ".join(sorted(authors)))\n',
 [dict(py='authors == {"Frank Herbert", "Jane Austen", "William Gibson"}', msg="`authors` is a set of the three authors."), dict(outHas="Frank Herbert, Jane Austen, William Gibson", msg="It prints the sorted authors.")])
oo("o5", "Counting with a dictionary",
 ["To count things, use a dict from thing to count. `counts.get(key, 0)` returns 0 for a key you haven't seen yet, so you can always add 1.",
  "This is the most common dictionary pattern there is. (`collections.Counter` does it for you once you know how it works.)"],
 "Build `per_author`: a dict from author to how many of their books are in the list. Print it.",
 '\nper_author = {}\nfor b in books:\n    per_author[b["author"]] = per_author.get(b["author"], 0) + 1\nprint(per_author)\n',
 [dict(py='per_author == {"Frank Herbert": 1, "Jane Austen": 2, "William Gibson": 1}', msg="`per_author` counts 2 for Jane Austen and 1 for the others.")])
oo("o6", "Tuples and unpacking",
 ["A **tuple** is a fixed group of values, like `(\"Dune\", 1965)`. Python can unpack it into names: `title, year = pair`.",
  "Loops unpack too: `for title, year in pairs:`. `enumerate` gives you `(index, item)` tuples, which is why `for i, x in enumerate(items)` works."],
 "Make `pairs`, a list of `(title, year)` tuples. Loop over it with `enumerate`, starting at 1, and print lines like `1. Dune (1965)`.",
 '\npairs = [(b["title"], b["year"]) for b in books]\nfor i, (title, year) in enumerate(pairs, start=1):\n    print(f"{i}. {title} ({year})")\n',
 [dict(py='pairs[0] == ("Dune", 1965) and len(pairs) == 4', msg="`pairs` holds `(title, year)` tuples."), dict(outHas="1. Dune (1965)", msg="It prints `1. Dune (1965)`."), dict(outHas="4. Neuromancer (1984)", msg="It prints `4. Neuromancer (1984)`.")])
oo("o7", "Your first class",
 ["Dicts are great for plain data. When data comes with **behaviour** (a book can be checked out), a **class** keeps them together.",
  "`__init__` runs when you create an object. `self` is the object being built; `self.title = title` stores a value on it. `Book(\"Dune\", \"Frank Herbert\", 1965)` creates one."],
 "Write `class Book` whose `__init__` takes `title`, `author` and `year`, stores them, and sets `self.available = True`. Create `dune = Book(\"Dune\", \"Frank Herbert\", 1965)` and print its title.",
 '\n\nclass Book:\n    def __init__(self, title, author, year):\n        self.title = title\n        self.author = author\n        self.year = year\n        self.available = True\n\n\ndune = Book("Dune", "Frank Herbert", 1965)\nprint(dune.title)\n',
 [dict(py='Book("A", "B", 2000).year == 2000 and Book("A", "B", 2000).author == "B"', msg="`Book` stores title, author and year."), dict(py='dune.available is True', msg="New books are available."),
  dict(py='_out.splitlines()[-1] == "Dune"', msg="It prints Dune.")],
 example='class Dog:\n    def __init__(self, name):\n        self.name = name\n\nrex = Dog("Rex")\nprint(rex.name)')
oo("o8", "Methods",
 ["A **method** is a function inside a class. Its first parameter is always `self`, so it can read and change the object.",
  "Methods can refuse: `check_out` returns `False` if the book is already out, rather than pretending it worked."],
 "Add `check_out(self)`: if the book is available, mark it unavailable and return `True`; otherwise return `False`. Add `give_back(self)`, which makes it available again. Check `dune` out twice and print both results.",
 '',
 [dict(py='(lambda b: (b.check_out(), b.available, b.check_out(), b.give_back(), b.available))(Book("A", "B", 1)) == (True, False, False, None, True)', msg="`check_out` works once, fails the second time, and `give_back` returns it."),
  dict(outHas="True\nFalse", msg="Checking out `dune` twice prints True then False.")],
 hint="Methods go inside the class, indented like `__init__`. Print the results after the class: `print(dune.check_out())` twice.")
OO[-1]["solution"] = OO[-1]["solution"].replace('        self.available = True\n\n\ndune', '        self.available = True\n\n    def check_out(self):\n        if not self.available:\n            return False\n        self.available = False\n        return True\n\n    def give_back(self):\n        self.available = True\n\n\ndune') + 'print(dune.check_out())\nprint(dune.check_out())\n'
oo("o9", "Readable objects with __str__",
 ["Printing an object shows something like `<__main__.Book object at 0x7f…>`. Define `__str__` to return friendlier text; `print` and `str()` use it.",
  "Methods with double underscores (*dunder* methods) hook into Python's built-in behaviour."],
 "Add `__str__` returning text like `Dune by Frank Herbert (1965)`. Print `dune`.",
 'print(dune)\n',
 [dict(py='str(Book("Emma", "Jane Austen", 1815)) == "Emma by Jane Austen (1815)"', msg="`str(book)` gives `Title by Author (Year)`."), dict(outHas="Dune by Frank Herbert (1965)", msg="Printing `dune` shows the friendly text.")])
OO[-1]["solution"] = OO[-1]["solution"].replace('    def give_back(self):\n        self.available = True\n', '    def give_back(self):\n        self.available = True\n\n    def __str__(self):\n        return f"{self.title} by {self.author} ({self.year})"\n')
oo("o10", "A class that holds objects",
 ["Objects can contain other objects. A `Library` keeps a list of `Book`s and offers operations on the whole collection.",
  "Turning the dicts from the start into objects is a one-line comprehension: `Book(b[\"title\"], b[\"author\"], b[\"year\"])` for each `b`."],
 "Write `class Library` with `self.books = []`, an `add(book)` method and `by_author(author)` returning a list of that author's books. Create `library`, add a `Book` for every dict in `books`, and print how many Jane Austen books it has.",
 '\n\nclass Library:\n    def __init__(self):\n        self.books = []\n\n    def add(self, book):\n        self.books.append(book)\n\n    def by_author(self, author):\n        return [b for b in self.books if b.author == author]\n\n\nlibrary = Library()\nfor b in books:\n    library.add(Book(b["title"], b["author"], b["year"]))\nprint(len(library.by_author("Jane Austen")))\n',
 [dict(py='len(library.books) == 4 and all(isinstance(b, Book) for b in library.books)', msg="`library` holds four `Book` objects."),
  dict(py='[b.title for b in library.by_author("Jane Austen")] == ["Emma", "Persuasion"]', msg="`by_author` returns that author's books."), dict(py='library.by_author("Nobody") == []', msg="An unknown author gives an empty list.")])
oo("o11", "Raising errors",
 ["When asked for something impossible, a method should **raise** an exception instead of returning a confusing value. `raise ValueError(\"No book called X\")` stops the function and reports what went wrong.",
  "The caller can handle it with `try:` / `except ValueError:`. Errors you raise on purpose are a feature, not a failure."],
 "Add `Library.check_out(title)`: find the book with that title and call its `check_out()`, returning the result. If there is no such book, raise `ValueError`. Then use `try`/`except` to check out `\"Missing\"` and print `Not found`.",
 '',
 [dict(py='_raises(lambda: Library().check_out("X"), ValueError)', msg="An unknown title raises `ValueError`."),
  dict(py='(lambda L: (L.add(Book("A", "B", 1)), L.check_out("A"), L.check_out("A"))[1:])(Library()) == (True, False)', msg="Checking out a known title works once."),
  dict(outHas="Not found", msg="Your `try`/`except` prints Not found.")],
 hint="Loop over `self.books`; return as soon as a title matches. After the loop, `raise ValueError(f\"No book called {title}\")`.")
OO[-1]["solution"] = OO[-1]["solution"].replace('        return [b for b in self.books if b.author == author]\n', '        return [b for b in self.books if b.author == author]\n\n    def check_out(self, title):\n        for b in self.books:\n            if b.title == title:\n                return b.check_out()\n        raise ValueError(f"No book called {title}")\n') + 'try:\n    library.check_out("Missing")\nexcept ValueError:\n    print("Not found")\n'
oo("o12", "Inheritance",
 ["A class can **inherit** from another: `class EBook(Book):` gets every method of `Book`, and can change (override) some of them.",
  "`super().__init__(...)` runs the parent's `__init__`, so you only write what's new. An e-book never runs out, so its `check_out` always succeeds."],
 "Write `class EBook(Book)` whose `__init__` also takes `size_mb` and calls `super().__init__`. Override `check_out` to always return `True` and `__str__` to add ` [ebook]` to the end. Add an e-book of *Snow Crash* (Neal Stephenson, 1992, 2.5 MB) to the library and print it.",
 '\n\nclass EBook(Book):\n    def __init__(self, title, author, year, size_mb):\n        super().__init__(title, author, year)\n        self.size_mb = size_mb\n\n    def check_out(self):\n        return True\n\n    def __str__(self):\n        return super().__str__() + " [ebook]"\n\n\nsnow = EBook("Snow Crash", "Neal Stephenson", 1992, 2.5)\nlibrary.add(snow)\nprint(snow)\n',
 [dict(py='issubclass(EBook, Book) and EBook("A", "B", 1, 3).size_mb == 3', msg="`EBook` inherits from `Book` and stores `size_mb`."),
  dict(py='(lambda e: (e.check_out(), e.check_out()))(EBook("A", "B", 1, 1)) == (True, True)', msg="An e-book can always be checked out."),
  dict(outHas="Snow Crash by Neal Stephenson (1992) [ebook]", msg="Printing it shows ` [ebook]` at the end."), dict(src="super\\(\\)", msg="You used `super()`.")])
oo("o13", "The library report",
 ["Time to put it together. Every piece is something you built: objects with `__str__`, a method that filters, sorting with a key.",
  "You now know the data structures and the object model that most Python code is built from."],
 "Add `Library.available()` returning the books that are available. Then print `Available:` followed by each available book on its own line, sorted by year.",
 '',
 [dict(py='[b.title for b in library.available()] == [b.title for b in library.books if b.available]', msg="`available()` returns the available books."),
  dict(outRe="Available:\\nEmma by Jane Austen \\(1815\\)\\nPersuasion by Jane Austen \\(1817\\)\\nDune by Frank Herbert \\(1965\\)\\nNeuromancer", msg="It prints the available books, oldest first."),
  dict(py='"Snow Crash" in _out.splitlines()[-1]', msg="The e-book is listed last.")])
OO[-1]["solution"] = OO[-1]["solution"].replace('        raise ValueError(f"No book called {title}")\n', '        raise ValueError(f"No book called {title}")\n\n    def available(self):\n        return [b for b in self.books if b.available]\n') + '\nprint("Available:")\nfor book in sorted(library.available(), key=lambda b: b.year):\n    print(book)\n'

C.append(dict(id="python-oop", title="Python Data & Objects", lang="python", hue="#60a5fa", icon="cube", art="cls", hours="2.5 h",
 tagline="Comprehensions, dictionaries, classes and inheritance.",
 desc="The next step after Python from Zero. Shape real data with comprehensions, sets and dictionaries, then model it with classes, methods, exceptions and inheritance while building a small library system.",
 project="a library system with books and e-books", steps=OO))

# =====================================================================================================  SQL ANALYTICS
SHOP = """CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
INSERT INTO customers VALUES (1,'Amara','Lagos'),(2,'Ben','Leeds'),(3,'Chen','Taipei'),(4,'Dana','Leeds'),(5,'Emil','Oslo'),(6,'Farah','Lagos');
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL);
INSERT INTO products VALUES (1,'Notebook','Stationery',4.5),(2,'Fountain pen','Stationery',32.0),(3,'Desk lamp','Home',45.0),(4,'Mug','Home',9.0),(5,'Headphones','Tech',120.0),(6,'USB cable','Tech',8.0),(7,'Backpack','Bags',60.0);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(id), order_date TEXT);
INSERT INTO orders VALUES (1,1,'2024-01-05'),(2,2,'2024-01-12'),(3,1,'2024-02-02'),(4,3,'2024-02-14'),(5,4,'2024-02-20'),(6,2,'2024-03-03'),(7,5,'2024-03-09'),(8,1,'2024-03-28'),(9,3,'2024-04-11'),(10,4,'2024-04-15');
CREATE TABLE order_items (order_id INTEGER REFERENCES orders(id), product_id INTEGER REFERENCES products(id), qty INTEGER);
INSERT INTO order_items VALUES (1,1,3),(1,4,1),(2,5,1),(3,2,1),(3,1,2),(4,3,1),(4,6,2),(5,7,1),(6,4,4),(6,6,2),(7,5,1),(7,2,1),(8,3,1),(9,1,10),(10,7,1),(10,5,1);
"""
SA = []
def sa(id, title, body, task, ref, tests, hint=None, example=None, ordered=False):
    SA.append(dict(id=id, title=title, body=body, task=task, solution=ref, ref=ref, ordered=ordered, starter="-- Write your query below\n", tests=tests,
                   **({"hint": hint} if hint else {}), **({"example": example} if example else {})))
ROWS = lambda msg: dict(rows=True, msg=msg)
sa("a1", "Join two tables",
 ["Data is split across tables so nothing is stored twice: an order holds a `customer_id`, not the customer's name. A **JOIN** puts them back together.",
  "`FROM orders o JOIN customers c ON o.customer_id = c.id` pairs each order with its customer. `o` and `c` are short **aliases**."],
 "Select each order's `id`, its `order_date` and the customer's `name`.",
 "SELECT o.id, o.order_date, c.name FROM orders o JOIN customers c ON o.customer_id = c.id;",
 [dict(src="JOIN", msg="You used `JOIN`."), ROWS("Every order is listed with its customer's name.")])
sa("a2", "LEFT JOIN: find what's missing",
 ["A plain `JOIN` drops rows with no match. `LEFT JOIN` keeps every row from the left table and fills the right side with `NULL` when nothing matches.",
  "So `WHERE o.id IS NULL` after a `LEFT JOIN` finds customers who never ordered. (Use `IS NULL`, never `= NULL`.)"],
 "Select the `name` of every customer who has never placed an order.",
 "SELECT c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.id WHERE o.id IS NULL;",
 [dict(src="LEFT\\s+JOIN", msg="You used `LEFT JOIN`."), ROWS("You find the one customer with no orders.")])
sa("a3", "Three tables and a calculation",
 ["Joins chain: orders → order_items → products. Each `JOIN … ON …` adds one table.",
  "Columns can be calculated: `oi.qty * p.price AS line_total` names the result."],
 "For every row in `order_items`, select the `order_id`, the product `name` and `line_total` (quantity times price).",
 "SELECT oi.order_id, p.name, oi.qty * p.price AS line_total FROM order_items oi JOIN products p ON p.id = oi.product_id;",
 [dict(cols=["order_id", "name", "line_total"], msg="The columns are `order_id`, `name` and `line_total`."), ROWS("Every line has the right total.")])
sa("a4", "Revenue by category",
 ["`GROUP BY` folds rows into one per group, and aggregate functions like `SUM` work across each group.",
  "Combine it with joins and you can answer business questions: which category earns most?"],
 "Select each product `category` and its total `revenue` (sum of quantity × price), highest revenue first.",
 "SELECT p.category, SUM(oi.qty * p.price) AS revenue FROM order_items oi JOIN products p ON p.id = oi.product_id GROUP BY p.category ORDER BY revenue DESC;",
 [dict(src="GROUP\\s+BY", msg="You used `GROUP BY`."), ROWS("Each category's revenue is correct, highest first.")], ordered=True)
sa("a5", "HAVING filters groups",
 ["`WHERE` filters rows *before* grouping. `HAVING` filters groups *after*, so it can use aggregates: `HAVING SUM(...) > 100`."],
 "Select the `name` and `total` spent by every customer who spent **more than 150** in all.",
 "SELECT c.name, SUM(oi.qty * p.price) AS total FROM customers c JOIN orders o ON o.customer_id = c.id JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id GROUP BY c.id HAVING total > 150;",
 [dict(src="HAVING", msg="You used `HAVING`."), ROWS("You get exactly the customers who spent over 150.")],
 hint="Join customers → orders → order_items → products, group by customer, then `HAVING SUM(oi.qty * p.price) > 150`.")
sa("a6", "CASE: label your data",
 ["`CASE WHEN condition THEN value … ELSE value END` is SQL's if/else. It creates a new column from rules.",
  "Conditions are checked in order, and the first match wins."],
 "Select every product's `name`, `price` and a `band`: `budget` under 10, `mid` under 50, otherwise `premium`.",
 "SELECT name, price, CASE WHEN price < 10 THEN 'budget' WHEN price < 50 THEN 'mid' ELSE 'premium' END AS band FROM products;",
 [dict(src="CASE[\\s\\S]*END", msg="You used `CASE … END`."), ROWS("Every product has the right band.")])
sa("a7", "Grouping by month",
 ["Dates here are text like `2024-02-14`. SQLite's `strftime('%Y-%m', order_date)` cuts them down to the month, `2024-02`, which you can group by.",
  "Other databases have `DATE_TRUNC` or `EXTRACT`; the idea is the same."],
 "Select each `month` and the number of `orders` placed in it, in month order.",
 "SELECT strftime('%Y-%m', order_date) AS month, COUNT(*) AS orders FROM orders GROUP BY month ORDER BY month;",
 [ROWS("Each month has the right number of orders, in order.")], ordered=True)
sa("a8", "CTEs: name a step",
 ["A **common table expression** names a query so the next one can use it like a table: `WITH totals AS (SELECT …) SELECT … FROM totals`.",
  "CTEs turn one giant query into readable steps. They're how analysts write SQL in real life."],
 "With a CTE `totals` holding each order's id and total, select the average order total as `avg_order`.",
 "WITH totals AS (SELECT oi.order_id, SUM(oi.qty * p.price) AS total FROM order_items oi JOIN products p ON p.id = oi.product_id GROUP BY oi.order_id) SELECT AVG(total) AS avg_order FROM totals;",
 [dict(src="WITH\\s+\\w+\\s+AS", msg="You used `WITH … AS`."), ROWS("The average order total is correct.")])
sa("a9", "Window functions: rank",
 ["A **window function** calculates across rows without folding them together. `RANK() OVER (ORDER BY total DESC)` numbers rows by total, while every row stays in the result.",
  "Compare with `GROUP BY`, which returns one row per group. Windows return one row per row, plus a value computed from its neighbours."],
 "Using a CTE of each customer's `name` and `total` spent, select `name`, `total` and `place` (their `RANK()` by total, biggest first), in place order.",
 "WITH spend AS (SELECT c.name, SUM(oi.qty * p.price) AS total FROM customers c JOIN orders o ON o.customer_id = c.id JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id GROUP BY c.id) SELECT name, total, RANK() OVER (ORDER BY total DESC) AS place FROM spend ORDER BY place;",
 [dict(src="OVER\\s*\\(", msg="You used a window function with `OVER`."), ROWS("Customers are ranked correctly.")], ordered=True)
sa("a10", "PARTITION BY: best in each group",
 ["`PARTITION BY` restarts the window for each group: `RANK() OVER (PARTITION BY category ORDER BY units DESC)` ranks products within their own category.",
  "Wrap it in a CTE and keep rank 1 to get the top item per group, a classic analytics question."],
 "For each category, select the `category`, product `name` and `units` (total quantity sold) of its best-selling product.",
 "WITH sold AS (SELECT p.category, p.name, SUM(oi.qty) AS units, RANK() OVER (PARTITION BY p.category ORDER BY SUM(oi.qty) DESC) AS r FROM order_items oi JOIN products p ON p.id = oi.product_id GROUP BY p.id) SELECT category, name, units FROM sold WHERE r = 1;",
 [dict(src="PARTITION\\s+BY", msg="You used `PARTITION BY`."), ROWS("You get the top product in each category.")],
 hint="Window functions can't go in `WHERE`, so rank inside a CTE and filter `WHERE r = 1` outside it.")
sa("a11", "Running totals",
 ["`SUM(x) OVER (ORDER BY month)` adds up every row so far: a running total. It's how dashboards draw cumulative revenue lines."],
 "With a CTE of monthly `revenue`, select `month`, `revenue` and `running` (the running total), in month order.",
 "WITH monthly AS (SELECT strftime('%Y-%m', o.order_date) AS month, SUM(oi.qty * p.price) AS revenue FROM orders o JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id GROUP BY month) SELECT month, revenue, SUM(revenue) OVER (ORDER BY month) AS running FROM monthly ORDER BY month;",
 [dict(src="SUM\\s*\\([^)]*\\)\\s*OVER", msg="You used `SUM(...) OVER`."), ROWS("The running total is correct for each month.")], ordered=True)
sa("a12", "LAG: compare with last month",
 ["`LAG(revenue) OVER (ORDER BY month)` returns the previous row's value (`NULL` for the first row). Subtract it to get month-over-month change.",
  "You can now join, group, label, chain steps with CTEs and use window functions. That's the toolkit of a data analyst."],
 "Using the same monthly CTE, select `month`, `revenue` and `change` (revenue minus the previous month's revenue), in month order.",
 "WITH monthly AS (SELECT strftime('%Y-%m', o.order_date) AS month, SUM(oi.qty * p.price) AS revenue FROM orders o JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id GROUP BY month) SELECT month, revenue, revenue - LAG(revenue) OVER (ORDER BY month) AS change FROM monthly ORDER BY month;",
 [dict(src="LAG\\s*\\(", msg="You used `LAG`."), ROWS("Each month's change is correct (the first month has none).")], ordered=True)
C.append(dict(id="sql-analytics", title="SQL Analytics", lang="sql", hue="#f97316", icon="chart", art="⨝", hours="2 h", seed=SHOP,
 schema="customers(id, name, city)\nproducts(id, name, category, price)\norders(id, customer_id, order_date)\norder_items(order_id, product_id, qty)",
 tagline="Joins, CTEs and window functions on a shop's data.",
 desc="The SQL that analysts and backend developers use every day. Join four tables, group and filter, label rows with CASE, then write CTEs and window functions for rankings, running totals and month-over-month change. Take SQL from Zero first.",
 project="a sales report for an online shop", steps=SA))

# =====================================================================================================  ALGORITHMS
AL = []
al = chain(AL)
al("g1", "Linear search",
 ["An **algorithm** is a precise recipe for solving a problem. The simplest search checks every item in turn until it finds the target.",
  "If the list has n items, the worst case checks all n. We say it takes **O(n)** time: double the list, double the work."],
 "Write `linear_search(items, target)` that returns the index of `target`, or `-1` if it isn't there. Print `linear_search([4, 8, 15, 16, 23, 42], 23)`.",
 'def linear_search(items, target):\n    for i, x in enumerate(items):\n        if x == target:\n            return i\n    return -1\n\n\nprint(linear_search([4, 8, 15, 16, 23, 42], 23))\n',
 [dict(py='linear_search([4, 8, 15, 16, 23, 42], 23) == 4 and linear_search([5, 1, 5], 5) == 0', msg="It returns the first index of the target."), dict(py='linear_search([1, 2], 9) == -1 and linear_search([], 1) == -1', msg="A missing target gives -1."),
  dict(outHas="4", msg="It prints 4.")])
al("g2", "Binary search",
 ["If the list is **sorted**, look at the middle item. If the target is bigger, it can only be in the right half; if smaller, the left half. Each step throws away half the list.",
  "1,000,000 items take at most 20 steps. That's **O(log n)**, and it's why sorted data is so valuable."],
 "Write `binary_search(items, target)` for a sorted list, returning the index or `-1`. Use `lo` and `hi` indexes and a `while lo <= hi` loop.",
 '\n\ndef binary_search(items, target):\n    lo, hi = 0, len(items) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if items[mid] == target:\n            return mid\n        if items[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1\n\n\nprint(binary_search([4, 8, 15, 16, 23, 42], 42))\n',
 [dict(py='all(binary_search(list(range(0, 200, 2)), x) == x // 2 for x in range(0, 200, 2))', msg="It finds every item in a sorted list."),
  dict(py='binary_search(list(range(0, 200, 2)), 7) == -1 and binary_search([], 3) == -1 and binary_search([1], 0) == -1', msg="It returns -1 for missing items, including an empty list."),
  dict(src="while", msg="It uses a loop, not `index()` or `in`.")],
 hint="`mid = (lo + hi) // 2`. Move `lo = mid + 1` or `hi = mid - 1` so the range always shrinks.")
al("g3", "Count the steps",
 ["Big-O is easier to believe when you measure it. Change each search to also count how many items it looks at.",
  "Return two values at once as a tuple: `return i, steps`."],
 "Write `count_linear(items, target)` and `count_binary(items, target)` that return how many comparisons each search makes. On `list(range(1000))` searching for `999`, print both counts.",
 '\n\ndef count_linear(items, target):\n    steps = 0\n    for x in items:\n        steps += 1\n        if x == target:\n            break\n    return steps\n\n\ndef count_binary(items, target):\n    lo, hi, steps = 0, len(items) - 1, 0\n    while lo <= hi:\n        steps += 1\n        mid = (lo + hi) // 2\n        if items[mid] == target:\n            break\n        if items[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return steps\n\n\nbig = list(range(1000))\nprint(count_linear(big, 999), count_binary(big, 999))\n',
 [dict(py='count_linear(list(range(1000)), 999) == 1000 and count_linear([7, 1], 7) == 1', msg="`count_linear` counts every item it looks at."),
  dict(py='1 <= count_binary(list(range(1000)), 999) <= 10 and count_binary(list(range(1000)), 499) == 1', msg="`count_binary` needs at most 10 steps for 1,000 items."),
  dict(outRe="1000 \\d+", msg="It prints both counts.")])
al("g4", "Recursion",
 ["A **recursive** function calls itself on a smaller version of the problem. It needs a **base case** that stops the calls, or it runs forever.",
  "`factorial(5) = 5 × factorial(4)`, down to `factorial(0) = 1`. Many algorithms (merge sort, tree searches) are naturally recursive."],
 "Write a recursive `factorial(n)` and a recursive `total(items)` that adds a list by returning `items[0] + total(items[1:])` (an empty list totals 0). Print `factorial(5)`.",
 '\n\ndef factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\n\n\ndef total(items):\n    if not items:\n        return 0\n    return items[0] + total(items[1:])\n\n\nprint(factorial(5))\n',
 [dict(py='factorial(0) == 1 and factorial(5) == 120 and factorial(10) == 3628800', msg="`factorial` is correct."), dict(py='total([]) == 0 and total([3, 4, 5]) == 12', msg="`total` adds a list."),
  dict(src="def total[\\s\\S]*total\\(", msg="`total` calls itself.")])
al("g5", "Selection sort",
 ["Sorting is the most studied problem in computing. **Selection sort**: find the smallest item, swap it to the front, repeat for the rest.",
  "Two nested loops over n items: **O(n²)**. Simple, but 1,000 items need about 500,000 comparisons."],
 "Write `selection_sort(items)` that returns a new sorted list (copy the input first with `items[:]`).",
 '\n\ndef selection_sort(items):\n    a = items[:]\n    for i in range(len(a)):\n        smallest = i\n        for j in range(i + 1, len(a)):\n            if a[j] < a[smallest]:\n                smallest = j\n        a[i], a[smallest] = a[smallest], a[i]\n    return a\n\n\nprint(selection_sort([5, 2, 9, 1, 5, 6]))\n',
 [dict(py='selection_sort([5, 2, 9, 1, 5, 6]) == [1, 2, 5, 5, 6, 9] and selection_sort([]) == []', msg="It sorts, including duplicates and empty lists."),
  dict(py='(lambda x: (selection_sort(x), x)[1] == [3, 1, 2])([3, 1, 2])', msg="It doesn't change the original list."), dict(py='"sorted(" not in _src and ".sort(" not in _src', msg="It doesn't use Python's built-in sorting.")])
al("g6", "Merging sorted lists",
 ["Two **sorted** lists can be merged in one pass: compare the fronts, take the smaller, repeat. When one list runs out, append the rest of the other.",
  "That's O(n), and it's the key move of merge sort, next."],
 "Write `merge(a, b)` that merges two sorted lists into one sorted list.",
 '\n\ndef merge(a, b):\n    out, i, j = [], 0, 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]:\n            out.append(a[i])\n            i += 1\n        else:\n            out.append(b[j])\n            j += 1\n    return out + a[i:] + b[j:]\n\n\nprint(merge([1, 4, 9], [2, 3, 10]))\n',
 [dict(py='merge([1, 4, 9], [2, 3, 10]) == [1, 2, 3, 4, 9, 10]', msg="It merges two sorted lists."), dict(py='merge([], [1, 2]) == [1, 2] and merge([5], []) == [5] and merge([1, 1], [1]) == [1, 1, 1]', msg="It handles empty lists and duplicates.")])
al("g7", "Merge sort",
 ["**Merge sort** splits the list in half, sorts each half (recursively), then merges them. A list of 0 or 1 items is already sorted: the base case.",
  "The list halves log n times and each level does O(n) merging, so it's **O(n log n)**. For 1,000 items that's about 10,000 steps instead of 500,000."],
 "Write `merge_sort(items)` using `merge`. Print `merge_sort([38, 27, 43, 3, 9, 82, 10])`.",
 '\n\ndef merge_sort(items):\n    if len(items) <= 1:\n        return items[:]\n    mid = len(items) // 2\n    return merge(merge_sort(items[:mid]), merge_sort(items[mid:]))\n\n\nprint(merge_sort([38, 27, 43, 3, 9, 82, 10]))\n',
 [dict(py='merge_sort([38, 27, 43, 3, 9, 82, 10]) == [3, 9, 10, 27, 38, 43, 82] and merge_sort([]) == [] and merge_sort([1]) == [1]', msg="It sorts correctly."),
  dict(py='(lambda r: merge_sort(r) == sorted(r))([(i * 7919) % 1009 for i in range(500)])', msg="It sorts 500 numbers correctly."), dict(src="def merge_sort[\\s\\S]*merge_sort\\(", msg="`merge_sort` is recursive.")])
al("g8", "Memoisation",
 ["The naive recursive Fibonacci, `fib(n) = fib(n-1) + fib(n-2)`, recomputes the same values again and again: `fib(40)` makes over 300 million calls.",
  "**Memoisation** stores each answer the first time, in a dictionary, and reuses it. Each `fib(k)` is computed once, so it's O(n). That's the core idea of dynamic programming."],
 "Write `fib(n, memo=None)` with `fib(0) = 0` and `fib(1) = 1` that caches results in a dict. Print `fib(80)`.",
 '\n\ndef fib(n, memo=None):\n    if memo is None:\n        memo = {}\n    if n < 2:\n        return n\n    if n not in memo:\n        memo[n] = fib(n - 1, memo) + fib(n - 2, memo)\n    return memo[n]\n\n\nprint(fib(80))\n',
 [dict(py='[fib(i) for i in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]', msg="The first ten values are right."), dict(py='fib(80) == 23416728348467685', msg="`fib(80)` is correct (and fast)."),
  dict(outHas="23416728348467685", msg="It prints fib(80).")],
 hint="Use `memo=None` and create the dict inside, so each top-level call starts fresh. A default of `{}` would be shared between calls.")
al("g9", "Breadth-first search",
 ["A maze is a **graph**: each open cell links to its neighbours. **Breadth-first search** explores in rings: everything 1 step away, then 2, and so on, using a queue.",
  "So the first time BFS reaches the exit, it got there in the fewest steps. `collections.deque` gives a fast queue with `popleft()`."],
 "Write `shortest_path(maze)` for a list of strings where `#` is a wall, `S` the start and `E` the exit. Return the fewest moves (up, down, left, right) from S to E, or `-1` if there's no way through.",
 '\n\nfrom collections import deque\n\n\ndef shortest_path(maze):\n    rows, cols = len(maze), len(maze[0])\n    start = next((r, c) for r in range(rows) for c in range(cols) if maze[r][c] == "S")\n    seen = {start}\n    queue = deque([(start, 0)])\n    while queue:\n        (r, c), dist = queue.popleft()\n        if maze[r][c] == "E":\n            return dist\n        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):\n            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != "#" and (nr, nc) not in seen:\n                seen.add((nr, nc))\n                queue.append(((nr, nc), dist + 1))\n    return -1\n\n\nmaze = [\n    "S.#.....",\n    ".##.###.",\n    "....#...",\n    "##.#..#E",\n]\nprint(shortest_path(maze))\n',
 [dict(py='shortest_path(["S.#.....", ".##.###.", "....#...", "##.#..#E"]) == 14', msg="It finds the 14-move path through the example maze."),
  dict(py='shortest_path(["SE"]) == 1 and shortest_path(["S#E"]) == -1', msg="It handles a neighbouring exit and a blocked one."), dict(py='shortest_path(["S..", "...", "..E"]) == 4', msg="It finds the shortest route in an open grid.")])
al("g10", "Race your algorithms",
 ["Time to see Big-O for real. `time.perf_counter()` reads a precise clock; the difference between two readings is how long the code between them took.",
  "You've written searching, sorting, recursion, memoisation and graph search: the foundations every harder algorithm builds on. The Problems section is the next stop."],
 "Make `data`, 2000 numbers in a scrambled order (for example `[(i * 7919) % 2003 for i in range(2000)]`). Time `selection_sort` and `merge_sort` on it, check both match `sorted(data)`, and print which was faster.",
 '\n\nimport time\n\ndata = [(i * 7919) % 2003 for i in range(2000)]\nstart = time.perf_counter()\nslow = selection_sort(data)\nslow_time = time.perf_counter() - start\nstart = time.perf_counter()\nfast = merge_sort(data)\nfast_time = time.perf_counter() - start\nassert slow == fast == sorted(data)\nwinner = "merge sort" if fast_time < slow_time else "selection sort"\nprint(f"selection sort: {slow_time:.3f}s, merge sort: {fast_time:.3f}s")\nprint(f"Faster: {winner}")\n',
 [dict(py='len(data) == 2000 and len(set(data)) > 1000', msg="`data` has 2000 scrambled numbers."), dict(py='slow == fast == sorted(data)', msg="Both sorts give the same, correct result."),
  dict(outHas="Faster: merge sort", msg="Merge sort wins.")])

C.append(dict(id="algorithms-py", title="Algorithms with Python", lang="python", hue="#e879f9", icon="flow", art="O(n)", hours="2.5 h",
 tagline="Searching, sorting, recursion and Big-O, by measuring them.",
 desc="Write the classic algorithms yourself and count their steps: linear and binary search, selection and merge sort, recursion, memoisation and breadth-first search through a maze. The bridge from writing code to solving Problems.",
 project="an algorithm toolkit and a sorting race", steps=AL))
