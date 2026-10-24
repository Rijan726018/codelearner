"""Focused Bootcamp courses: each one goes deep on a single topic. Same format as tools/bootcamp_src.py.
Also assigns every course a track and a level, which the Bootcamp page groups by."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "projects_src"))
from bootcamp_src import C
from bootcamp_more import chain, T

# =====================================================================================================  ACCESSIBLE HTML
AX = []
def ax(id, title, body, task, solution, tests, **k):
    AX.append(dict(id=id, title=title, body=body, task=task, solution=solution, tests=tests, **k))
H0 = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Join the Reading Club</title>
</head>
<body>
  <h1>Join the Reading Club</h1>
  <p>One book a month, a friendly chat, no homework.</p>
</body>
</html>
"""
h1 = H0.replace("<html>", '<html lang="en">')
ax("ax1", "Say what language the page is in",
 ["Accessibility means everyone can use your page: people using screen readers, keyboards, magnifiers or voice control, and people on slow phones in bright sunshine. Most of it is just **correct HTML**.",
  "Start at the top. `<html lang=\"en\">` tells screen readers which language to pronounce, browsers which dictionary to spell-check with, and translators where to start."],
 "Add `lang=\"en\"` to the `<html>` element. Keep the `<title>`: it's the first thing a screen reader announces.",
 h1, [dict(sel="html", attr="lang", val="^[a-z]{2}", re=True, msg="`<html>` has a `lang` attribute."), dict(sel="title", nonempty=True, msg="The page has a `title`.")],
 starter=H0, hint="Change the opening tag to `<html lang=\"en\">`.")
LAND = """<body>
  <header>
    <p>Reading Club</p>
    <nav>
      <a href="#join">Join</a>
      <a href="#books">This year's books</a>
    </nav>
  </header>
  <main>
    <h1>Join the Reading Club</h1>
    <p>One book a month, a friendly chat, no homework.</p>
  </main>
  <footer>
    <p>Run by volunteers since 2019.</p>
  </footer>
</body>"""
h2 = h1.replace("""<body>
  <h1>Join the Reading Club</h1>
  <p>One book a month, a friendly chat, no homework.</p>
</body>""", LAND)
ax("ax2", "Landmarks",
 ["Screen-reader users jump around a page by **landmarks**: `<header>`, `<nav>`, `<main>` and `<footer>`. With them, \"skip to the main content\" is one keystroke; without them, it's listening to every link first.",
  "There should be exactly one `<main>`, holding the content that's unique to this page."],
 "Wrap the page in landmarks: a `<header>` containing a `<nav>` with two links, a `<main>` around the heading and paragraph, and a `<footer>`.",
 h2, [dict(sel="body > header nav a", count=2, msg="The `header` contains a `nav` with links."), dict(sel="main h1", msg="The `h1` is inside `main`."),
      dict(sel="body > footer", msg="There's a `footer`."), dict(sel="main ~ main", exists=False, msg="There's only one `main`.")],
 ref=("MDN: Landmark roles", "https://developer.mozilla.org/en-US/docs/Learn/Accessibility/WAI-ARIA_basics#signpostslandmarks"))
SKIP = h2.replace("<body>\n  <header>", '<body>\n  <a class="skip" href="#content">Skip to main content</a>\n  <header>').replace("  <main>", '  <main id="content">')
h3 = SKIP.replace("  <title>Join the Reading Club</title>\n", "  <title>Join the Reading Club</title>\n  <style>\n    .skip { position: absolute; left: -9999px; }\n    .skip:focus { left: 8px; top: 8px; background: white; padding: 8px; }\n  </style>\n")
ax("ax3", "A skip link",
 ["Keyboard users press Tab to move through links. Without help, they tab through the whole navigation on every page before reaching the content.",
  "A **skip link** is the first link on the page and points at `<main>`. It's hidden off-screen until it receives focus, then appears, so it helps keyboard users without cluttering the design."],
 "Make the first thing in `<body>` a link `<a class=\"skip\" href=\"#content\">Skip to main content</a>`, give `<main>` the `id=\"content\"`, and add CSS that moves `.skip` off-screen until `.skip:focus`.",
 h3, [dict(sel="body > a.skip:first-child", attr="href", val="#content", msg="The first element in `body` is the skip link to `#content`."), dict(sel="main#content", msg="`main` has `id=\"content\"`."),
      dict(src="\\.skip:focus", msg="There's a `.skip:focus` rule that shows it again.")])
HEADS = """  <main id="content">
    <h1>Join the Reading Club</h1>
    <p>One book a month, a friendly chat, no homework.</p>
    <h2>How it works</h2>
    <p>We meet on the first Tuesday of every month.</p>
    <h2 id="join">Sign up</h2>
  </main>"""
h4 = h3.replace("""  <main id="content">
    <h1>Join the Reading Club</h1>
    <p>One book a month, a friendly chat, no homework.</p>
  </main>""", HEADS)
ax("ax4", "Headings in order",
 ["Screen-reader users also navigate by **headings**, so headings are the page's table of contents. Use one `<h1>`, then `<h2>` for sections, `<h3>` inside those, and never skip a level just to get a smaller font: that's CSS's job."],
 "In `<main>`, after the paragraph, add an `<h2>How it works</h2>` with a paragraph under it, then an `<h2 id=\"join\">Sign up</h2>`.",
 h4, [dict(sel="main h2", count=2, msg="`main` has two `h2` sections."), dict(sel="h2#join", text="Sign up", msg="The second `h2` is `Sign up`, with `id=\"join\"`."),
      dict(sel="h1 ~ h1, h3, h4", exists=False, msg="There's one `h1` and no skipped levels.")])
IMGS = """    <h2>How it works</h2>
    <img src="https://picsum.photos/seed/club/480/240" alt="Six people laughing around a table covered in books and mugs">
    <p>We meet on the first Tuesday of every month.</p>"""
h5 = h4.replace("""    <h2>How it works</h2>
    <p>We meet on the first Tuesday of every month.</p>""", IMGS).replace("    <p>Reading Club</p>", '    <p><img src="https://picsum.photos/seed/logo/32" alt=""> Reading Club</p>')
ax("ax5", "Images: describe them, or hide them",
 ["Every `<img>` needs an `alt` attribute. If the picture carries meaning, describe what matters about it. If it's purely decorative (a logo next to the same words, a flourish), use an **empty** `alt=\"\"` so screen readers skip it.",
  "Leaving `alt` out entirely is the worst option: many screen readers then read the file name aloud."],
 "Add a photo under *How it works* with a descriptive `alt`, and a small logo image in the header's `<p>` with `alt=\"\"`, since the words next to it already say *Reading Club*.",
 h5, [dict(sel="img:not([alt])", exists=False, msg="Every image has an `alt` attribute."), dict(sel="main img", attr="alt", val="\\S+\\s+\\S+\\s+\\S+", re=True, msg="The photo has a description of a few words."),
      dict(sel="header img[alt='']", msg="The decorative logo has `alt=\"\"`.")],
 ref=("W3C: An alt decision tree", "https://www.w3.org/WAI/tutorials/images/decision-tree/"))
FORM = """    <h2 id="join">Sign up</h2>
    <form>
      <label for="name">Your name</label>
      <input id="name" name="name" autocomplete="name" required>
      <label for="email">Email</label>
      <input id="email" name="email" type="email" autocomplete="email" required>
      <button type="submit">Join the club</button>
    </form>"""
FORM6 = FORM.replace(' autocomplete="name" required', '').replace(' type="email" autocomplete="email" required', '')
h6 = h5.replace('    <h2 id="join">Sign up</h2>', FORM6)
h7 = h5.replace('    <h2 id="join">Sign up</h2>', FORM)
ax("ax6", "Every input has a label",
 ["A visible `<label>` connected to its input with `for` and `id` does three things: screen readers announce it, people with shaky hands can click the bigger label to focus the field, and everyone knows what to type.",
  "Placeholder text is not a label: it disappears as soon as you type."],
 "Under *Sign up*, add a `<form>` with a labelled name input (`#name`) and a labelled email input (`#email`), connected with `for` and `id`, and a submit button.",
 h6, [dict(sel="label[for='name'] ~ input#name", msg="`#name` has a `label` with `for=\"name\"`."), dict(sel="label[for='email'] ~ input#email", msg="`#email` has a `label` with `for=\"email\"`."),
      dict(sel="form button", msg="The form has a button.")], ref=("MDN: The label element", "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/label"))
ax("ax7", "Help people fill it in",
 ["The right `type` gives phone users the right keyboard (`type=\"email\"` shows `@`). `autocomplete` lets browsers fill in names and addresses, which matters a lot to people for whom typing is slow or painful. `required` lets the browser explain what's missing."],
 "Give the email input `type=\"email\"`, both inputs `required`, and `autocomplete` values `name` and `email`.",
 h7, [dict(sel="#email", attr="type", val="email", msg="`#email` has `type=\"email\"`."), dict(sel="#name[required][autocomplete='name']", msg="`#name` is required with `autocomplete=\"name\"`."),
      dict(sel="#email[required][autocomplete='email']", msg="`#email` is required with `autocomplete=\"email\"`.")])
HINT = """      <button type="submit">Join the club</button>"""
h8 = h7.replace(HINT, """      <label for="genre">Favourite kind of book</label>
      <input id="genre" name="genre" aria-describedby="genre-hint">
      <p id="genre-hint">Optional. It helps us pick next year's list.</p>
""" + HINT)
ax("ax8", "Connect hints to fields",
 ["Extra instructions under a field are invisible to screen-reader users unless you connect them. `aria-describedby=\"genre-hint\"` on the input makes the reader announce the hint's text right after the label.",
  "ARIA attributes add meaning that HTML alone can't express. The first rule of ARIA: if a plain HTML element does the job, use that instead."],
 "Add a third labelled input `#genre` and a hint paragraph `<p id=\"genre-hint\">` below it, and connect them with `aria-describedby`.",
 h8, [dict(sel="label[for='genre'] ~ input#genre", msg="`#genre` has a label."), dict(sel="#genre", attr="aria-describedby", val="genre-hint", msg="`#genre` points at the hint with `aria-describedby`."),
      dict(sel="p#genre-hint", nonempty=True, msg="The hint paragraph exists.")])
BTN = h8.replace('      <a href="#books">This year\'s books</a>', '      <a href="#books">This year\'s books</a>\n      <button type="button" id="menu" aria-expanded="false">Menu</button>')
h9 = BTN
ax("ax9", "Buttons are buttons",
 ["A `<div>` with a click handler looks like a button but isn't one: you can't Tab to it, Enter and Space don't press it, and screen readers don't announce it. A real `<button>` does all of that for free.",
  "`aria-expanded` tells screen readers whether a toggle (like a menu) is open or closed; your JavaScript would flip it when clicked."],
 "In the `<nav>`, add `<button type=\"button\" id=\"menu\" aria-expanded=\"false\">Menu</button>`. Don't use any clickable `<div>`s.",
 h9, [dict(sel="nav button#menu[type='button']", msg="The nav has a real `button#menu`."), dict(sel="#menu", attr="aria-expanded", val="false", msg="It has `aria-expanded=\"false\"`."),
      dict(sel="div[onclick], span[onclick]", exists=False, msg="There are no clickable `div`s or `span`s.")])
TABLE = """    <h2 id="books">This year's books</h2>
    <table>
      <caption>Books we're reading in 2026</caption>
      <thead>
        <tr><th scope="col">Month</th><th scope="col">Book</th></tr>
      </thead>
      <tbody>
        <tr><td>January</td><td>Kindred</td></tr>
        <tr><td>February</td><td>The Remains of the Day</td></tr>
      </tbody>
    </table>
  </main>"""
h10 = h9.replace("    </form>\n  </main>", "    </form>\n" + TABLE)
ax("ax10", "Tables with real headers",
 ["Screen readers read a table cell together with its column header (*Book: Kindred*), but only if the headers are real `<th>` elements. `scope=\"col\"` says which way a header points, and `<caption>` names the table.",
  "That's the core of accessible HTML: language, landmarks, a skip link, headings, alt text, labels, real buttons and real tables. Run any page through a checker like WAVE or axe to catch the rest."],
 "After the form, add `<h2 id=\"books\">` and a table with a `<caption>`, a header row of two `<th scope=\"col\">` cells (Month, Book) and at least two rows.",
 h10, [dict(sel="table caption", nonempty=True, msg="The table has a `caption`."), dict(sel="thead th[scope='col']", count=2, msg="There are two column headers with `scope=\"col\"`."),
       dict(sel="tbody tr", count=2, msg="There are at least two rows of books."), dict(sel="h2#books", msg="The section heading has `id=\"books\"`, so the nav link works.")],
 ref=("WAVE accessibility checker", "https://wave.webaim.org/"))
C.append(dict(id="a11y-html", title="Accessible HTML", lang="html", hue="#22d3ee", icon="eye", art="♿ <main>", hours="1.5 h",
 tagline="Pages everyone can use: landmarks, headings, alt text, labels and real buttons.",
 desc="Build a club sign-up page that works with screen readers, keyboards and phones. Language, landmarks, a skip link, heading order, alt text, labelled forms, hints, real buttons and data tables.",
 project="an accessible sign-up page", steps=AX))

# =====================================================================================================  PYTHON STRINGS
ST = []
st = chain(ST)
st("st1", "Strings are sequences",
 ["A string is a sequence of characters, numbered from **0**. `word[0]` is the first character, and negative numbers count from the end: `word[-1]` is the last.",
  "This course builds a small text toolkit: the kind of helpers every app needs for names, titles and emails."],
 "Set `word = \"Python\"`, then store its first character in `first` and its last in `last`, and print both.",
 'word = "Python"\nfirst = word[0]\nlast = word[-1]\nprint(first, last)\n',
 [dict(py='first == "P" and last == "n"', msg="`first` is P and `last` is n."), dict(src="\\[-1\\]", msg="You use a negative index for the last character."), dict(outHas="P n", msg="It prints `P n`.")])
st("st2", "Slicing",
 ["`s[start:stop]` takes characters from `start` up to (not including) `stop`. Leave one out to go from the beginning or to the end: `s[:4]` is the first four, `s[-7:]` the last seven.",
  "A third number is the step: `s[::-1]` walks backwards, which reverses the string."],
 "With `s = \"CodeLearner\"`, make `head` (the first 4 characters), `tail` (the last 7) and `backwards` (the whole string reversed).",
 '\ns = "CodeLearner"\nhead = s[:4]\ntail = s[-7:]\nbackwards = s[::-1]\nprint(head, tail, backwards)\n',
 [dict(py='head == "Code" and tail == "Learner"', msg="`head` is Code and `tail` is Learner."), dict(py='backwards == "renraeLedoC"', msg="`backwards` is the reversed string."), dict(src="::-1", msg="You reverse with a slice.")])
st("st3", "Cleaning up messy text",
 ["Text from forms is messy: extra spaces, random capitals. String methods return a **new** cleaned string (strings never change in place): `.strip()` trims spaces from both ends, `.lower()` and `.upper()` change case, `.title()` capitalises each word.",
  "Methods can be chained: `messy.strip().title()`."],
 "Given `messy = \"   ada LOVELACE  \"`, store a cleaned version `\"Ada Lovelace\"` in `clean` using `strip` and `title`.",
 '\nmessy = "   ada LOVELACE  "\nclean = messy.strip().title()\nprint(clean)\n',
 [dict(py='clean == "Ada Lovelace"', msg="`clean` is `Ada Lovelace`."), dict(py='messy == "   ada LOVELACE  "', msg="`messy` is unchanged: methods return new strings."), dict(src="\\.strip\\(\\)", msg="You use `strip()`.")])
st("st4", "Split and join",
 ["`text.split(\",\")` cuts a string into a list wherever the separator appears. `\" & \".join(items)` does the reverse: glues a list of strings together with a separator between each pair.",
  "They're the bridge between text and lists, which is how you process CSV lines, tags, file paths and sentences."],
 "Split `line = \"ada,grace,linus\"` into a list `names`, then make `joined = \"ada & grace & linus\"` with `join`.",
 '\nline = "ada,grace,linus"\nnames = line.split(",")\njoined = " & ".join(names)\nprint(joined)\n',
 [dict(py='names == ["ada", "grace", "linus"]', msg="`names` is the list of three names."), dict(py='joined == "ada & grace & linus"', msg="`joined` uses ` & ` between names."), dict(src="\\.join\\(", msg="You use `join`.")])
st("st5", "Search and replace",
 ["`\"code\" in sentence` asks *does it contain this?* `sentence.find(\"learn\")` returns the index where it first appears, or `-1`. `sentence.replace(old, new)` returns a copy with every `old` swapped for `new`."],
 "With `sentence = \"teh best way to learn code is to write teh code\"`, set `has_code` (is `code` in it?), `where` (index of `learn`) and `fixed` (every `teh` replaced by `the`).",
 '\nsentence = "teh best way to learn code is to write teh code"\nhas_code = "code" in sentence\nwhere = sentence.find("learn")\nfixed = sentence.replace("teh", "the")\nprint(fixed)\n',
 [dict(py="has_code is True and where == 16", msg="`has_code` is True and `where` is 16."), dict(py='fixed == "the best way to learn code is to write the code"', msg="`fixed` replaces every `teh`."), dict(py='sentence.find("python") == -1', msg="(`find` gives -1 for missing text.)")])
st("st6", "Formatting with f-strings",
 ["An f-string puts values straight into text: `f\"{qty} x {name}\"`. After a colon you can format: `{price:.2f}` shows two decimals, `{name:<10}` pads to 10 characters on the left, `{n:>5}` on the right.",
  "That's how receipts, tables and reports line up neatly."],
 "Write `receipt_line(name, qty, price)` returning `f\"{name:<10} x{qty:<3} ${qty * price:.2f}\"`, for example `Tea        x2   $7.00`. Print one line.",
 '\n\ndef receipt_line(name, qty, price):\n    return f"{name:<10} x{qty:<3} ${qty * price:.2f}"\n\n\nprint(receipt_line("Tea", 2, 3.5))\n',
 [dict(py='receipt_line("Tea", 2, 3.5) == "Tea        x2   $7.00"', msg="`receipt_line(\"Tea\", 2, 3.5)` lines up as `Tea        x2   $7.00`."), dict(py='receipt_line("Cake", 10, 1.25) == "Cake       x10  $12.50"', msg="It works for other values too.")],
 hint='`f"{name:<10} x{qty:<3} ${qty * price:.2f}"`')
st("st7", "Make a URL slug",
 ["A **slug** is the URL-friendly version of a title: `Hello, World! 2026` becomes `hello-world-2026`. Lowercase everything, keep letters and digits, and turn each run of anything else into a single `-`.",
  "`ch.isalnum()` is True for letters and digits. Building a list of pieces and joining at the end is faster and cleaner than adding to a string in a loop."],
 "Write `slugify(title)`: lowercase letters and digits stay, every run of other characters becomes one `-`, and there's no `-` at either end.",
 '\n\ndef slugify(title):\n    out = []\n    for ch in title.lower():\n        if ch.isalnum():\n            out.append(ch)\n        elif out and out[-1] != "-":\n            out.append("-")\n    return "".join(out).strip("-")\n\n\nprint(slugify("Hello, World! 2026"))\n',
 [dict(py='slugify("Hello, World! 2026") == "hello-world-2026"', msg="`Hello, World! 2026` becomes `hello-world-2026`."), dict(py='slugify("  --Python   & SQL--  ") == "python-sql"', msg="Runs of symbols collapse and the ends are trimmed."),
  dict(py='slugify("") == ""', msg="An empty title gives an empty slug.")])
st("st8", "Initials",
 ["Combine what you know: split a name into words, take the first character of each, uppercase it and add a dot. A generator expression inside `join` does it in one line."],
 "Write `initials(name)`: `\"ada lovelace\"` gives `\"A.L.\"`, and extra spaces don't matter.",
 '\n\ndef initials(name):\n    return "".join(part[0].upper() + "." for part in name.split())\n\n\nprint(initials("ada lovelace"))\n',
 [dict(py='initials("ada lovelace") == "A.L."', msg="`ada lovelace` gives `A.L.`"), dict(py='initials("  grace   brewster  hopper ") == "G.B.H."', msg="Extra spaces are ignored."), dict(py='initials("") == ""', msg="An empty name gives an empty string.")])
st("st9", "Mask an email address",
 ["Privacy screens often show `a**@example.com` instead of the full address. Split once at the `@` with `email.split(\"@\", 1)` (or `partition`), keep the first character, replace the rest of the name with `*`, and put it back together."],
 "Write `mask_email(email)`: keep the first character of the name, replace the rest of the name with `*`, keep the domain. `ada@example.com` → `a**@example.com`.",
 '\n\ndef mask_email(email):\n    name, domain = email.split("@", 1)\n    return name[0] + "*" * (len(name) - 1) + "@" + domain\n\n\nprint(mask_email("ada@example.com"))\n',
 [dict(py='mask_email("ada@example.com") == "a**@example.com"', msg="`ada@example.com` → `a**@example.com`."), dict(py='mask_email("x@y.org") == "x@y.org"', msg="A one-letter name stays as it is."),
  dict(py='mask_email("grace.hopper@navy.mil") == "g***********@navy.mil"', msg="Longer names get one `*` per hidden character.")])
st("st10", "Palindromes, ignoring punctuation",
 ["A palindrome reads the same backwards. To check a sentence like *A man, a plan, a canal: Panama*, first keep only the letters and digits, lowercased, then compare with its reverse.",
  "You now have a toolkit of string functions: slugs, initials, masking and cleaning. Strings are the most common data in real programs."],
 "Write `is_palindrome(text)` that ignores case, spaces and punctuation.",
 '\n\ndef is_palindrome(text):\n    letters = "".join(ch.lower() for ch in text if ch.isalnum())\n    return letters == letters[::-1]\n\n\nprint(is_palindrome("A man, a plan, a canal: Panama"))\n',
 [dict(py='is_palindrome("A man, a plan, a canal: Panama") and is_palindrome("Was it a car or a cat I saw?")', msg="Sentence palindromes are recognised."), dict(py='not is_palindrome("Python")', msg="Other text isn't."), dict(py='is_palindrome("")', msg="Empty text counts as a palindrome.")])
C.append(dict(id="py-strings", title="Python Strings & Text", lang="python", hue="#67e8f9", icon="pen", art='"abc"[::-1]', hours="1.5 h",
 tagline="Index, slice, clean, split, format and search text.",
 desc="Everything about Python strings, one idea per step: indexing and slicing, cleaning messy input, split and join, search and replace, f-string formatting, then a toolkit of slugs, initials, masked emails and palindromes.",
 project="a text-cleaning toolkit", steps=ST))

# =====================================================================================================  PYTHON FUNCTIONS
FN = []
fn = chain(FN)
fn("fn1", "Parameters and return values",
 ["A function takes inputs (**parameters**), does one job and hands back a result with `return`. Printing inside a function shows a value; returning it lets the rest of your program use it."],
 "Write `area(width, height)` that returns the area of a rectangle. Print `area(3, 4)`.",
 'def area(width, height):\n    return width * height\n\n\nprint(area(3, 4))\n',
 [dict(py="area(3, 4) == 12 and area(2.5, 2) == 5", msg="`area` returns width × height."), dict(src="return ", msg="It uses `return`."), dict(outHas="12", msg="It prints 12.")])
fn("fn2", "Default values",
 ["A parameter can have a **default**: `def greet(name, greeting=\"Hello\")`. Callers can leave it out, or pass their own.",
  "Defaults make functions easy to call in the common case and flexible in the rare one."],
 "Write `greet(name, greeting=\"Hello\")` returning `\"Hello, Ada!\"` style text.",
 '\n\ndef greet(name, greeting="Hello"):\n    return f"{greeting}, {name}!"\n\n\nprint(greet("Ada"))\nprint(greet("Grace", "Welcome back"))\n',
 [dict(py='greet("Ada") == "Hello, Ada!"', msg="The default greeting is Hello."), dict(py='greet("Grace", "Welcome back") == "Welcome back, Grace!"', msg="A custom greeting works.")])
fn("fn3", "Keyword arguments",
 ["You can pass arguments by name: `make_user(\"ada\", admin=True)`. Names make calls self-explanatory.",
  "A bare `*` in the parameter list makes everything after it **keyword-only**: `def make_user(name, *, admin=False)` refuses `make_user(\"ada\", True)`, where nobody could guess what `True` means."],
 "Write `make_user(name, *, admin=False, active=True)` returning a dict with those three keys.",
 '\n\ndef make_user(name, *, admin=False, active=True):\n    return {"name": name, "admin": admin, "active": active}\n\n\nprint(make_user("ada", admin=True))\n',
 [dict(py='make_user("ada") == {"name": "ada", "admin": False, "active": True}', msg="Defaults fill in admin and active."), dict(py='make_user("ada", active=False, admin=True)["admin"] is True', msg="Keyword arguments work in any order."),
  dict(py='_raises(lambda: make_user("ada", True), TypeError)', msg="Passing admin by position is refused.")])
fn("fn4", "Any number of arguments: *args",
 ["`def total(*nums)` collects every positional argument into a **tuple** called `nums`, so callers can pass none, one or twenty values: `total(1, 2, 3)`.",
  "The reverse works too: `total(*my_list)` spreads a list into separate arguments."],
 "Write `total(*nums)` returning the sum (0 for no arguments). Then call it with a list spread using `*`.",
 '\n\ndef total(*nums):\n    result = 0\n    for n in nums:\n        result += n\n    return result\n\n\nprices = [3, 4.5, 2]\nprint(total(*prices))\n',
 [dict(py="total() == 0 and total(5) == 5 and total(1, 2, 3) == 6", msg="`total` adds any number of arguments."), dict(src="total\\(\\*", msg="You call it with a spread list: `total(*...)`."), dict(outHas="9.5", msg="It prints 9.5.")])
fn("fn5", "Named extras: **kwargs",
 ["`**info` collects keyword arguments you didn't name in advance into a **dict**. It's how functions accept options they pass on elsewhere.",
  "`sorted(info.items())` gives the pairs in key order, so output is predictable."],
 "Write `describe(**info)` returning `\"a=1, b=2\"`: each `key=value`, sorted by key, joined with `, `. No arguments gives `\"\"`.",
 '\n\ndef describe(**info):\n    return ", ".join(f"{key}={value}" for key, value in sorted(info.items()))\n\n\nprint(describe(name="Ada", born=1815))\n',
 [dict(py='describe(b=2, a=1) == "a=1, b=2"', msg="Pairs are sorted by key."), dict(py='describe() == ""', msg="No arguments gives an empty string."), dict(outHas="born=1815, name=Ada", msg="It prints the sorted pairs.")])
fn("fn6", "Returning several values",
 ["`return low, high` returns a **tuple**, and the caller can unpack it straight away: `low, high = min_max(nums)`. It's cleaner than returning a list and remembering which index means what."],
 "Write `min_max(nums)` returning `(smallest, largest)`. Unpack the result into `low` and `high` for `[4, 1, 9, 7]`.",
 '\n\ndef min_max(nums):\n    return min(nums), max(nums)\n\n\nlow, high = min_max([4, 1, 9, 7])\nprint(low, high)\n',
 [dict(py="min_max([4, 1, 9, 7]) == (1, 9) and min_max([5]) == (5, 5)", msg="`min_max` returns a (min, max) tuple."), dict(py="low == 1 and high == 9", msg="You unpacked it into `low` and `high`.")])
fn("fn7", "Functions are values",
 ["In Python a function is a value like any other: store it in a variable, put it in a list, pass it to another function. `lambda x: x * 2` writes a tiny function inline.",
  "`sorted(words, key=len)` passes the function `len` to `sorted`, which calls it on each item to decide the order."],
 "Write `apply_twice(f, x)` returning `f(f(x))`. Then sort `words = [\"kiwi\", \"fig\", \"banana\"]` by length into `by_length` using `key=len`.",
 '\n\ndef apply_twice(f, x):\n    return f(f(x))\n\n\nprint(apply_twice(lambda n: n * 3, 2))\nwords = ["kiwi", "fig", "banana"]\nby_length = sorted(words, key=len)\nprint(by_length)\n',
 [dict(py="apply_twice(lambda n: n + 1, 5) == 7 and apply_twice(str.upper, 'hi') == 'HI'", msg="`apply_twice` calls the function twice."), dict(py='by_length == ["fig", "kiwi", "banana"]', msg="`by_length` is sorted by length."), dict(src="key=len", msg="You pass `key=len`.")])
fn("fn8", "Closures",
 ["A function defined inside another can use the outer function's variables, even after the outer one has returned. That's a **closure**: a function with memory.",
  "`nonlocal count` lets the inner function change the outer variable instead of creating a new local one."],
 "Write `make_counter()` that returns a function; each call of that function returns the next number, 1, 2, 3… Separate counters count separately.",
 '\n\ndef make_counter():\n    count = 0\n\n    def counter():\n        nonlocal count\n        count += 1\n        return count\n\n    return counter\n\n\nclicks = make_counter()\nclicks()\nprint(clicks())\n',
 [dict(py="(lambda c: (c(), c(), c()))(make_counter()) == (1, 2, 3)", msg="A counter returns 1, 2, 3…"), dict(py="(lambda a, b: (a(), a(), b()))(make_counter(), make_counter()) == (1, 2, 1)", msg="Two counters are independent."), dict(src="nonlocal", msg="You use `nonlocal`.")])
fn("fn9", "Decorators",
 ["A **decorator** takes a function and returns a new one that adds behaviour around it. `@shout` above a function definition is shorthand for `func = shout(func)`.",
  "`functools.wraps` copies the original's name and docstring onto the wrapper, so debugging still shows the right name. Web frameworks use decorators for routes, caching and logins."],
 "Write a decorator `shout` whose wrapper calls the function and returns the result in upper case. Use `functools.wraps`. Decorate `def hello(name): return f\"hello, {name}\"`.",
 '\n\nimport functools\n\n\ndef shout(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        return func(*args, **kwargs).upper()\n    return wrapper\n\n\n@shout\ndef hello(name):\n    return f"hello, {name}"\n\n\nprint(hello("ada"))\n',
 [dict(py='hello("ada") == "HELLO, ADA"', msg="`hello(\"ada\")` returns `HELLO, ADA`."), dict(py='hello.__name__ == "hello"', msg="`functools.wraps` keeps the name `hello`."), dict(py='shout(lambda: "x")() == "X"', msg="`shout` works on any function."), dict(src="@shout", msg="You use `@shout`.")])
fn("fn10", "The mutable default trap",
 ["Default values are created **once**, when the function is defined. So `def add_item(item, items=[])` shares one list between every call, and items pile up mysteriously.",
  "The fix is a pattern you'll see everywhere: default to `None`, then create a fresh list inside. You now know functions in depth: defaults, keyword-only arguments, `*args`, `**kwargs`, closures and decorators."],
 "Write `add_item(item, items=None)` that appends to `items` (or to a new list when none is given) and returns the list. Calls without a list must never share one.",
 '\n\ndef add_item(item, items=None):\n    if items is None:\n        items = []\n    items.append(item)\n    return items\n\n\nprint(add_item("a"), add_item("b"))\n',
 [dict(py='add_item("a") == ["a"] and add_item("b") == ["b"]', msg="Separate calls get separate lists."), dict(py='(lambda l: add_item("y", l) is l and l == ["x", "y"])(["x"])', msg="A given list is appended to and returned."), dict(src="items=None", msg="The default is `None`.")])
C.append(dict(id="py-functions", title="Python Functions in Depth", lang="python", hue="#38bdf8", icon="flow", art="def f(*a)", hours="1.5 h",
 tagline="Defaults, keyword-only arguments, *args, **kwargs, closures and decorators.",
 desc="Functions are the building block of every program. Go beyond the basics: default and keyword-only arguments, any number of arguments, returning tuples, functions as values, closures, decorators and the mutable-default trap.",
 project="a library of reusable helpers", steps=FN))

# =====================================================================================================  PYTHON ERRORS & TESTING
ER = []
er = chain(ER)
er("er1", "Catch an error",
 ["When something goes wrong, Python raises an **exception** and, unless you catch it, the program stops with a traceback. Read tracebacks from the bottom: the last line names the error and what happened.",
  "`try:` runs code that might fail; `except ZeroDivisionError:` runs only if that specific error happens. Catch the narrowest error you expect, never every error by accident."],
 "Write `safe_divide(a, b)` that returns `a / b`, or `None` when `b` is 0, using `try`/`except ZeroDivisionError`.",
 'def safe_divide(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return None\n\n\nprint(safe_divide(10, 4), safe_divide(1, 0))\n',
 [dict(py="safe_divide(10, 4) == 2.5 and safe_divide(1, 0) is None", msg="It divides, and returns None for 0."), dict(src="except ZeroDivisionError", msg="You catch `ZeroDivisionError` specifically.")])
er("er2", "Several kinds of failure",
 ["One `except` can name several errors in a tuple: `except (ValueError, TypeError):`. `int(\"abc\")` raises `ValueError`; `int(None)` raises `TypeError`."],
 "Write `to_int(value)` that returns `int(value)`, or `None` if it raises `ValueError` or `TypeError`.",
 '\n\ndef to_int(value):\n    try:\n        return int(value)\n    except (ValueError, TypeError):\n        return None\n\n\nprint(to_int("42"), to_int("abc"), to_int(None))\n',
 [dict(py='to_int("42") == 42 and to_int(" 7 ") == 7', msg="Valid numbers convert."), dict(py='to_int("abc") is None and to_int(None) is None and to_int("4.5") is None', msg="Bad values give None."), dict(src="except \\(ValueError, TypeError\\)", msg="You catch both in one `except`.")])
er("er3", "else and finally",
 ["`else:` runs only if the `try` block **didn't** raise. `finally:` runs no matter what, even after a `return`: it's where you close files and release resources.",
  "Keeping only the risky line inside `try` and the follow-up in `else` makes it obvious which line you expect to fail."],
 "Write `parse_all(items)` that returns a list of log strings: for each item, `\"ok N\"` (in `else`) or `\"bad X\"` (in `except ValueError`), and always `\"done X\"` (in `finally`).",
 '\n\ndef parse_all(items):\n    log = []\n    for item in items:\n        try:\n            n = int(item)\n        except ValueError:\n            log.append(f"bad {item}")\n        else:\n            log.append(f"ok {n}")\n        finally:\n            log.append(f"done {item}")\n    return log\n\n\nprint(parse_all(["1", "x"]))\n',
 [dict(py='parse_all(["1", "x"]) == ["ok 1", "done 1", "bad x", "done x"]', msg="The log shows else, except and finally in the right order."), dict(src="finally:", msg="You use `finally`."), dict(src="else:", msg="You use `else`.")])
er("er4", "Raise your own errors",
 ["Your functions should refuse impossible requests loudly: `raise ValueError(\"Insufficient funds\")`. A clear error at the point of the mistake beats a wrong answer that surfaces three files later.",
  "Check the inputs first (**guard clauses**), then do the work."],
 "Write `withdraw(balance, amount)` that returns the new balance. Raise `ValueError(\"Amount must be positive\")` for amounts of 0 or less, and `ValueError(\"Insufficient funds\")` if the amount is more than the balance.",
 '\n\ndef withdraw(balance, amount):\n    if amount <= 0:\n        raise ValueError("Amount must be positive")\n    if amount > balance:\n        raise ValueError("Insufficient funds")\n    return balance - amount\n\n\nprint(withdraw(100, 30))\n',
 [dict(py="withdraw(100, 30) == 70 and withdraw(5, 5) == 0", msg="Valid withdrawals return the new balance."), dict(py="_raises(lambda: withdraw(10, 50), ValueError) and _raises(lambda: withdraw(10, 0), ValueError)", msg="Bad amounts raise `ValueError`."),
  dict(src='raise ValueError\\("Insufficient funds"\\)', msg="The message says `Insufficient funds`.")])
er("er5", "Custom exceptions",
 ["Define your own exception by subclassing `Exception`: `class InsufficientFunds(Exception): pass`. Callers can then catch exactly your error, and its name explains the problem.",
  "Subclass an existing error (here `ValueError`) so code that already catches `ValueError` keeps working."],
 "Create `class InsufficientFunds(ValueError)` and make `withdraw` raise it (with the same message) instead of a plain `ValueError` when the balance is too low.",
 '',
 [dict(py="issubclass(InsufficientFunds, ValueError)", msg="`InsufficientFunds` is a `ValueError`."), dict(py="_raises(lambda: withdraw(10, 50), InsufficientFunds)", msg="Overdrawing raises `InsufficientFunds`."),
  dict(py="_raises(lambda: withdraw(10, -1), ValueError) and not _raises(lambda: withdraw(10, -1), InsufficientFunds)", msg="Negative amounts still raise a plain `ValueError`.")])
ER[-1]["solution"] = ER[-1]["solution"].replace('\n\ndef withdraw(balance, amount):', '\n\nclass InsufficientFunds(ValueError):\n    pass\n\n\ndef withdraw(balance, amount):').replace('        raise ValueError("Insufficient funds")', '        raise InsufficientFunds("Insufficient funds")')
er("er6", "assert: check your assumptions",
 ["`assert condition, \"message\"` raises `AssertionError` if the condition is false, and does nothing if it's true. It's the simplest test there is: write down what must be true.",
  "Tests are just code that calls your functions with known inputs and asserts the outputs."],
 "Below your functions, write three `assert` lines checking `withdraw(100, 30) == 70`, `to_int(\"7\") == 7` and `safe_divide(1, 0) is None`, then print `All good`.",
 '\nassert withdraw(100, 30) == 70, "withdraw should subtract"\nassert to_int("7") == 7, "to_int should parse digits"\nassert safe_divide(1, 0) is None, "dividing by zero gives None"\nprint("All good")\n',
 [dict(src="assert withdraw\\(", msg="You assert on `withdraw`."), dict(src="assert to_int\\(", msg="You assert on `to_int`."), dict(src="assert safe_divide\\(", msg="You assert on `safe_divide`."), dict(outHas="All good", msg="It prints `All good`.")])
er("er7", "Test functions",
 ["Real projects keep tests in functions named `test_…`, one behaviour each, so a failure tells you exactly what broke. Tools like **pytest** find and run them automatically.",
  "Test the edge cases, not just the happy path: zero, empty, the exact limit."],
 "Write three test functions, `test_withdraw_ok`, `test_withdraw_exact` (withdrawing the whole balance gives 0) and `test_to_int_bad` (`to_int(\"x\")` is None), each with an `assert`. Call all three.",
 '\n\ndef test_withdraw_ok():\n    assert withdraw(100, 30) == 70\n\n\ndef test_withdraw_exact():\n    assert withdraw(50, 50) == 0\n\n\ndef test_to_int_bad():\n    assert to_int("x") is None\n\n\ntest_withdraw_ok()\ntest_withdraw_exact()\ntest_to_int_bad()\n',
 [dict(py="all(callable(globals().get(n)) for n in ['test_withdraw_ok', 'test_withdraw_exact', 'test_to_int_bad'])", msg="The three test functions exist."), dict(py="test_withdraw_exact() is None and test_to_int_bad() is None", msg="They pass.")])
er("er8", "A tiny test runner",
 ["A test runner calls each test, catches `AssertionError` to count a failure instead of stopping, and reports a summary. That's most of what pytest does, minus the pretty colours.",
  "Functions are values, so a list of test functions is easy to loop over; `test.__name__` gives each one's name."],
 "Write `run_tests(tests)` that calls each test function, prints `PASS name` or `FAIL name`, and returns `(passed, failed)`. Run it on your three tests.",
 '\n\ndef run_tests(tests):\n    passed = failed = 0\n    for test in tests:\n        try:\n            test()\n        except AssertionError:\n            failed += 1\n            print(f"FAIL {test.__name__}")\n        else:\n            passed += 1\n            print(f"PASS {test.__name__}")\n    return passed, failed\n\n\nprint(run_tests([test_withdraw_ok, test_withdraw_exact, test_to_int_bad]))\n',
 [dict(py="run_tests([test_withdraw_ok, test_to_int_bad]) == (2, 0)", msg="Passing tests are counted."), dict(py="(lambda: run_tests([lambda: None, (lambda: (_ for _ in ()).throw(AssertionError()))]))() == (1, 1)", msg="A failing test is counted, not fatal."),
  dict(outHas="PASS test_withdraw_ok", msg="It prints `PASS test_withdraw_ok`.")])
er("er9", "Testing that errors happen",
 ["Good tests also check that bad input fails the right way. The pattern: call it inside `try`; if no error happens, the test fails; if the expected error happens, it passes. (pytest spells this `with pytest.raises(InsufficientFunds):`.)"],
 "Write `test_overdraw_raises()` that passes only if `withdraw(10, 50)` raises `InsufficientFunds`, and add it to your run.",
 '\n\ndef test_overdraw_raises():\n    try:\n        withdraw(10, 50)\n    except InsufficientFunds:\n        return\n    assert False, "expected InsufficientFunds"\n\n\nprint(run_tests([test_withdraw_ok, test_withdraw_exact, test_to_int_bad, test_overdraw_raises]))\n',
 [dict(py="test_overdraw_raises() is None", msg="The test passes against the real `withdraw`."), dict(outHas="PASS test_overdraw_raises", msg="The runner reports it as passing."),
  dict(src="except InsufficientFunds", msg="It expects `InsufficientFunds` specifically.")])
er("er10", "Test first",
 ["**Test-driven development**: write the tests first, watch them fail, then write just enough code to pass. It forces you to decide what *correct* means before you start.",
  "You now handle errors deliberately, raise your own, and prove your code works with tests. That's the habit that separates hobby code from professional code."],
 "These tests describe `grade(score)`: 90+ is `A`, 80+ `B`, 70+ `C`, below that `F`, and scores outside 0–100 raise `ValueError`. Write the tests `test_grades` and `test_grade_range`, then `grade`, and run all your tests.",
 '\n\ndef test_grades():\n    assert [grade(s) for s in (95, 90, 85, 70, 69, 0)] == ["A", "A", "B", "C", "F", "F"]\n\n\ndef test_grade_range():\n    for bad in (-1, 101):\n        try:\n            grade(bad)\n        except ValueError:\n            continue\n        assert False, f"{bad} should raise"\n\n\ndef grade(score):\n    if not 0 <= score <= 100:\n        raise ValueError("score must be 0-100")\n    if score >= 90:\n        return "A"\n    if score >= 80:\n        return "B"\n    if score >= 70:\n        return "C"\n    return "F"\n\n\nprint(run_tests([test_withdraw_ok, test_withdraw_exact, test_to_int_bad, test_overdraw_raises, test_grades, test_grade_range]))\n',
 [dict(py='[grade(s) for s in (100, 90, 89, 80, 79, 70, 69)] == ["A", "A", "B", "B", "C", "C", "F"]', msg="`grade` follows the boundaries exactly."), dict(py="_raises(lambda: grade(101), ValueError) and _raises(lambda: grade(-5), ValueError)", msg="Out-of-range scores raise."),
  dict(outHas="(6, 0)", msg="All six tests pass.")])
C.append(dict(id="py-testing", title="Python Errors & Testing", lang="python", hue="#f87171", icon="bug", art="assert ✓", hours="1.5 h",
 tagline="Catch, raise and design exceptions, then prove your code works with tests.",
 desc="Professional code fails loudly and is tested. Catch specific errors, use else and finally, raise your own and custom exceptions, then write asserts, test functions, a tiny test runner, tests for errors, and finish test-first.",
 project="a tested banking helper and test runner", steps=ER))

# =====================================================================================================  JAVASCRIPT ARRAYS
AR = []
ar = chain(AR)
MOVIES = '''const movies = [
  { title: "Arrival", year: 2016, rating: 7.9, minutes: 116, genres: ["Sci-Fi", "Drama"] },
  { title: "Spirited Away", year: 2001, rating: 8.6, minutes: 125, genres: ["Animation", "Fantasy"] },
  { title: "Parasite", year: 2019, rating: 8.5, minutes: 132, genres: ["Thriller", "Drama"] },
  { title: "Dune", year: 2021, rating: 8.0, minutes: 155, genres: ["Sci-Fi", "Adventure"] },
  { title: "Coco", year: 2017, rating: 8.4, minutes: 105, genres: ["Animation", "Family"] },
  { title: "Inception", year: 2010, rating: 8.8, minutes: 148, genres: ["Sci-Fi", "Thriller"] },
];
'''
ar("ar1", "Loop over an array",
 ["Arrays of objects are how most apps hold data: a list of movies, users or orders. `for (const movie of movies)` visits each item in order.",
  "This course is about the array methods that replace most loops. First, the loop itself."],
 "Below `movies`, use `for...of` to `console.log` each movie's title.",
 MOVIES + '\nfor (const movie of movies) {\n  console.log(movie.title);\n}\n',
 [dict(js='_out.trim().split("\\n").length === 6 && _out.startsWith("Arrival")', msg="All six titles are logged, starting with Arrival."), dict(src="for \\(const \\w+ of movies\\)", msg="You use `for...of`.")],
 example="for (const n of [1, 2, 3]) {\n  console.log(n * 2);\n}")
AR[0]["starter"] = MOVIES
ar("ar2", "map: transform every item",
 ["`array.map(fn)` calls `fn` on every item and returns a **new** array of the results, the same length as the original. `movies.map(m => m.title)` is every title."],
 "Make `titles`, an array of every title, with `map`.",
 '\nconst titles = movies.map(m => m.title);\nconsole.log(titles);\n',
 [dict(js='JSON.stringify(titles) === JSON.stringify(movies.map(m => m.title))', msg="`titles` holds every title in order."), dict(src="\\.map\\(", msg="You use `map`.")],
 ref=("MDN: Array.prototype.map", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map"))
ar("ar3", "filter: keep some",
 ["`array.filter(fn)` keeps only the items where `fn` returns true. The result can be shorter, and the original is untouched."],
 "Make `recent`: the movies released after 2015.",
 '\nconst recent = movies.filter(m => m.year > 2015);\nconsole.log(recent.length);\n',
 [dict(js='recent.length === 4 && recent.every(m => m.year > 2015)', msg="`recent` holds the 4 movies after 2015."), dict(js="movies.length === 6", msg="`movies` is unchanged."), dict(src="\\.filter\\(", msg="You use `filter`.")])
ar("ar4", "find and findIndex",
 ["`find(fn)` returns the **first** item that matches (or `undefined`); `findIndex(fn)` returns its position (or `-1`). They stop as soon as they find one."],
 "Set `dune` to the movie titled `Dune` with `find`, and `cocoAt` to the index of `Coco` with `findIndex`.",
 '\nconst dune = movies.find(m => m.title === "Dune");\nconst cocoAt = movies.findIndex(m => m.title === "Coco");\nconsole.log(dune.year, cocoAt);\n',
 [dict(js="dune === movies[3]", msg="`dune` is the Dune object itself."), dict(js="cocoAt === 4", msg="`cocoAt` is 4."), dict(js='movies.find(m => m.title === "Nope") === undefined', msg="(`find` gives `undefined` when nothing matches.)")])
ar("ar5", "some and every",
 ["`some(fn)` asks *does at least one match?*; `every(fn)` asks *do they all?* Both return true or false and stop early."],
 "Set `anyUnder8` (is any rating below 8?) and `allHaveGenres` (does every movie have at least one genre?).",
 '\nconst anyUnder8 = movies.some(m => m.rating < 8);\nconst allHaveGenres = movies.every(m => m.genres.length > 0);\nconsole.log(anyUnder8, allHaveGenres);\n',
 [dict(js="anyUnder8 === true && allHaveGenres === true", msg="Both are true."), dict(src="\\.some\\(", msg="You use `some`."), dict(src="\\.every\\(", msg="You use `every`.")])
ar("ar6", "reduce: combine into one value",
 ["`reduce((acc, item) => ..., start)` walks the array carrying an **accumulator**. Start at 0 and add each runtime to get a total; divide by the length for an average."],
 "Compute `totalMinutes` with `reduce`, then `averageRating` rounded to 2 decimals with `Number(x.toFixed(2))`.",
 '\nconst totalMinutes = movies.reduce((sum, m) => sum + m.minutes, 0);\nconst averageRating = Number((movies.reduce((sum, m) => sum + m.rating, 0) / movies.length).toFixed(2));\nconsole.log(totalMinutes, averageRating);\n',
 [dict(js="totalMinutes === 781", msg="`totalMinutes` is 781."), dict(js="averageRating === 8.37", msg="`averageRating` is 8.37."), dict(src="\\.reduce\\(", msg="You use `reduce`.")],
 ref=("MDN: Array.prototype.reduce", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce"))
ar("ar7", "sort, safely",
 ["`sort` changes the array **in place**, so copy it first with `[...movies]`. Give it a comparator: return a negative number to put `a` first, positive to put `b` first. `(a, b) => b.rating - a.rating` sorts by rating, highest first.",
  "Without a comparator, `sort` compares items as **strings**: `[10, 9, 1].sort()` gives `[1, 10, 9]`."],
 "Make `byRating`: a sorted copy, highest rating first. Leave `movies` in its original order.",
 '\nconst byRating = [...movies].sort((a, b) => b.rating - a.rating);\nconsole.log(byRating.map(m => m.title));\n',
 [dict(js='byRating.map(m => m.title).join() === "Inception,Spirited Away,Parasite,Coco,Dune,Arrival"', msg="`byRating` is highest first."), dict(js='movies[0].title === "Arrival"', msg="`movies` keeps its original order.")])
ar("ar8", "flatMap and Set: unique values",
 ["`flatMap` maps and then flattens one level: `movies.flatMap(m => m.genres)` is one long list of genres. A `Set` keeps only unique values, and `[...new Set(list)]` turns it back into an array."],
 "Make `genres`: every genre once, sorted alphabetically.",
 '\nconst genres = [...new Set(movies.flatMap(m => m.genres))].sort();\nconsole.log(genres);\n',
 [dict(js='genres.join() === "Adventure,Animation,Drama,Family,Fantasy,Sci-Fi,Thriller"', msg="`genres` lists each genre once, sorted."), dict(src="flatMap", msg="You use `flatMap`."), dict(src="new Set", msg="You use a `Set`.")])
ar("ar9", "Group and count",
 ["`reduce` can build an object as well as a number. Start with `{}` and, for each genre, add one to its count: `counts[g] = (counts[g] || 0) + 1`."],
 "Make `countByGenre`, an object from each genre to how many movies have it.",
 '\nconst countByGenre = movies.flatMap(m => m.genres).reduce((counts, g) => {\n  counts[g] = (counts[g] || 0) + 1;\n  return counts;\n}, {});\nconsole.log(countByGenre);\n',
 [dict(js='countByGenre["Sci-Fi"] === 3 && countByGenre.Drama === 2 && countByGenre.Family === 1', msg="Counts are right: Sci-Fi 3, Drama 2, Family 1."), dict(js="Object.keys(countByGenre).length === 7", msg="Every genre is counted.")])
ar("ar10", "Chain them",
 ["Each method returns a new array, so you can **chain** them into a pipeline that reads like a sentence: filter, then sort, then take the first few, then map to titles. `slice(0, 2)` takes the first two without changing the array.",
  "Most data processing in JavaScript, from React lists to API responses, is exactly this."],
 "Write `topByGenre(genre, n)` returning the titles of the `n` highest-rated movies in that genre. Log `topByGenre(\"Sci-Fi\", 2)`.",
 '\nfunction topByGenre(genre, n) {\n  return movies\n    .filter(m => m.genres.includes(genre))\n    .sort((a, b) => b.rating - a.rating)\n    .slice(0, n)\n    .map(m => m.title);\n}\nconsole.log(topByGenre("Sci-Fi", 2));\n',
 [dict(js='topByGenre("Sci-Fi", 2).join() === "Inception,Dune"', msg="The top 2 Sci-Fi movies are Inception and Dune."), dict(js='topByGenre("Animation", 5).join() === "Spirited Away,Coco"', msg="Asking for more than exist is fine."),
  dict(js='movies[0].title === "Arrival"', msg="`movies` is still unchanged (`filter` made a copy before `sort`).")])
C.append(dict(id="js-arrays", title="JavaScript Array Methods", lang="js", hue="#facc15", icon="layers", art=".map()", hours="1.5 h",
 tagline="map, filter, find, some, reduce, sort and chaining on real data.",
 desc="Replace most loops with array methods. Using a list of movies: map, filter, find and findIndex, some and every, reduce for totals and grouping, safe sorting, flatMap with Set, and chained pipelines.",
 project="a movie-data explorer", steps=AR))

# =====================================================================================================  ASYNC JAVASCRIPT (web)
from _lib import Page
P = Page("Async JavaScript")
AS = []
def asy(id, title, body, task, tests, **k):
    AS.append(dict(id=id, title=title, body=body, task=task, solution=P.render(), tests=tests, **k))
BLANK = P.render()
P.body = ['  <h1>Users</h1>', '  <button id="load">Load users</button>', '  <button id="fail">Try a broken request</button>', '  <p id="status">Nothing loaded yet.</p>', '  <ul id="users"></ul>']
P.css = ['    body { font-family: system-ui, sans-serif; padding: 24px; }', '    button { margin-right: 8px; }']
P.js = ['    console.log("A");', '    setTimeout(() => console.log("B"), 0);', '    console.log("C");']
asy("as1", "The event loop",
 ["JavaScript runs one thing at a time. Slow work (timers, network requests) doesn't block it: you hand over a function to run **later**, and the code carries on.",
  "`setTimeout(fn, 0)` doesn't run `fn` immediately. It queues it to run after the current code finishes, so `A`, then `C`, then `B` appear in the console."],
 "Build the page (an `h1`, buttons `#load` and `#fail`, `p#status`, an empty `ul#users`). In a `<script>`, log `A`, schedule `B` with `setTimeout(..., 0)`, then log `C`.",
 [T("_logs()==='A\\nC\\nB'", "The console shows A, C, B."), T("!!$('#load') && !!$('#fail') && !!$('#status') && !!$('ul#users')", "The page has the buttons, status and list.")],
 starter=BLANK, ref=("MDN: The event loop", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop"))
P.js = ['    function delay(ms) {', '      return new Promise(resolve => setTimeout(resolve, ms));', '    }']
asy("as2", "Promises",
 ["A **Promise** is a value that isn't ready yet: it will either **resolve** with a result or **reject** with an error. `new Promise(resolve => ...)` creates one; you call `resolve` when the work is done.",
  "`delay(ms)` returns a promise that resolves after `ms` milliseconds: the simplest useful promise."],
 "Replace the script with `delay(ms)`, a function returning `new Promise(resolve => setTimeout(resolve, ms))`.",
 [T("delay(10) instanceof Promise", "`delay` returns a Promise."), T("window.__t >= 90", "`delay(100)` really waits about 100 ms.", do="const t0 = performance.now(); await delay(100); window.__t = performance.now() - t0;")],
 ref=("MDN: Using promises", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises"))
P.js += ['', '    delay(50).then(() => "ready").then(word => console.log(word));']
asy("as3", "then chains",
 ["`promise.then(fn)` runs `fn` with the result once the promise resolves, and returns a **new** promise for whatever `fn` returns. So you can chain steps: `delay(50).then(() => \"ready\").then(console.log)`."],
 "After 50 ms, produce the string `ready` in one `then` and log it in a second `then`.",
 [T("_logs().trim()==='ready'", "`ready` is logged after the delay.", wait=200), dict(src="\\.then\\([\\s\\S]*\\.then\\(", msg="You chain two `then` calls.")])
P.js = ['    const USERS = [{ name: "Ada" }, { name: "Grace" }, { name: "Linus" }];', '',
  '    // A pretend server: /users answers after 200 ms; anything else fails.', '    function fakeFetch(url) {', '      return new Promise((resolve, reject) => {',
  '        setTimeout(() => {', '          if (url === "/users") resolve({ ok: true, json: async () => USERS });', '          else reject(new Error("Network error"));', '        }, 200);', '      });', '    }', '',
  '    async function loadUsers(url = "/users") {', '      const response = await fakeFetch(url);', '      return await response.json();', '    }']
asy("as4", "async and await",
 ["`async function` lets you write promise code that reads top to bottom. Inside it, `await promise` pauses **that function** (not the page) until the promise settles, then gives you the result.",
  "Real `fetch` works the same way: `const res = await fetch(url); const data = await res.json();`. Here a `fakeFetch` stands in for a server, so the course works offline."],
 "Replace the script with the `USERS` data, the `fakeFetch` function shown in the solution, and `async function loadUsers(url = \"/users\")` that awaits `fakeFetch(url)` and then `response.json()`.",
 [T("window.__u.length===3 && window.__u[0].name==='Ada'", "`loadUsers()` resolves to the three users.", do="window.__u = await loadUsers();"), dict(src="async function loadUsers", msg="`loadUsers` is an `async` function."), dict(src="await ", msg="You use `await`.")],
 hint="Copy `fakeFetch` exactly; your part is `loadUsers`: `const response = await fakeFetch(url); return await response.json();`")
P.js += ['', '    const statusEl = document.querySelector("#status");', '    const list = document.querySelector("#users");', '',
  '    async function show(url) {', '      statusEl.textContent = "Loading…";', '      list.innerHTML = "";', '      const users = await loadUsers(url);', '      for (const user of users) {',
  '        const li = document.createElement("li");', '        li.textContent = user.name;', '        list.append(li);', '      }', '      statusEl.textContent = `${users.length} users`;', '    }', '',
  '    document.querySelector("#load").addEventListener("click", () => show("/users"));']
asy("as5", "Show a loading state",
 ["While data is on its way, tell people: set the status to `Loading…` **before** awaiting, then replace it with the result. Without it, the page looks frozen.",
  "`show` is `async`, and a click handler can call it without waiting: the browser keeps responding while it runs."],
 "Write `async function show(url)`: set `#status` to `Loading…`, clear the list, await `loadUsers(url)`, add an `li` per user, then set the status to `3 users`. The `#load` button calls `show(\"/users\")`.",
 [T("_text('#status')==='Loading…'", "Clicking shows `Loading…` straight away.", do="_click('#load');"),
  T("$$('#users li').length===3 && _text('#status')==='3 users'", "Then it lists the users and says `3 users`.", do="_click('#load');", wait=500)])
P.sub_js('''      const users = await loadUsers(url);
      for (const user of users) {
        const li = document.createElement("li");
        li.textContent = user.name;
        list.append(li);
      }
      statusEl.textContent = `${users.length} users`;''', '''      try {
        const users = await loadUsers(url);
        for (const user of users) {
          const li = document.createElement("li");
          li.textContent = user.name;
          list.append(li);
        }
        statusEl.textContent = `${users.length} users`;
      } catch (error) {
        statusEl.textContent = "Couldn't load users. Try again.";
        console.error(error.message);
      }''')
P.js += ['    document.querySelector("#fail").addEventListener("click", () => show("/broken"));']
asy("as6", "Handle failures",
 ["Networks fail. When an awaited promise rejects, `await` **throws** the error, so a normal `try`/`catch` handles it, exactly like synchronous code.",
  "Always leave the page in a sensible state: replace `Loading…` with a message that says what happened and what to do."],
 "Wrap the loading in `try`/`catch`. On failure, set the status to `Couldn't load users. Try again.` and log the error's message with `console.error`. The `#fail` button calls `show(\"/broken\")`.",
 [T("_text('#status')===\"Couldn't load users. Try again.\" && $$('#users li').length===0", "A failed request shows a helpful message.", do="_click('#fail');", wait=500),
  T("_logs().includes('Network error')", "The error message is logged.", do="_click('#fail');", wait=500), T("$$('#users li').length===3", "Successful loads still work.", do="_click('#load');", wait=500)])
P.sub_js('          if (url === "/users") resolve({ ok: true, json: async () => USERS });', '          if (url === "/users") resolve({ ok: true, json: async () => USERS });\n          else if (url === "/posts") resolve({ ok: true, json: async () => [{ title: "Hello" }, { title: "Async is fun" }] });')
P.js += ['', '    async function loadEverything() {', '      const [users, posts] = await Promise.all([loadUsers("/users"), loadUsers("/posts")]);', '      return { users, posts };', '    }']
asy("as7", "Run requests in parallel",
 ["Two `await`s in a row run one after the other: 200 ms + 200 ms. If the requests don't depend on each other, start both and wait for both with `Promise.all([a, b])`: about 200 ms in total.",
  "`Promise.all` resolves to an array of results in the same order, ready to destructure. If any one rejects, the whole thing rejects."],
 "Make `fakeFetch` also answer `/posts` with two posts. Write `async function loadEverything()` that loads `/users` and `/posts` in parallel with `Promise.all` and returns `{ users, posts }`.",
 [T("window.__r.users.length===3 && window.__r.posts.length===2", "It returns users and posts.", do="window.__r = await loadEverything();"),
  T("window.__ms < 350", "Both load in parallel (well under 400 ms).", do="const t0 = performance.now(); await loadEverything(); window.__ms = performance.now() - t0;"), dict(src="Promise\\.all\\(", msg="You use `Promise.all`.")])
P.js += ['', '    function withTimeout(promise, ms) {', '      const timeout = new Promise((_, reject) => setTimeout(() => reject(new Error("Timed out")), ms));', '      return Promise.race([promise, timeout]);', '    }']
asy("as8", "Give up after a timeout",
 ["`Promise.race([a, b])` settles as soon as the **first** one does. Race a request against a timer that rejects, and you get a timeout: crucial on slow mobile networks.",
  "You now know the whole async toolkit: the event loop, promises, then, async/await, loading states, try/catch, Promise.all and Promise.race."],
 "Write `withTimeout(promise, ms)` that rejects with `Error(\"Timed out\")` if `promise` hasn't settled within `ms`, using `Promise.race`.",
 [T("window.__v.length===3", "A fast enough request still resolves.", do="window.__v = await withTimeout(loadUsers(), 1000);"),
  T("window.__e==='Timed out'", "A slow one rejects with `Timed out`.", do="try { await withTimeout(loadUsers(), 50); window.__e = 'no error'; } catch (e) { window.__e = e.message; }"), dict(src="Promise\\.race\\(", msg="You use `Promise.race`.")])
C.append(dict(id="js-async", title="Async JavaScript", lang="web", hue="#a78bfa", icon="clock", art="await", hours="1.5 h",
 tagline="The event loop, promises, async/await, errors and parallel requests.",
 desc="How JavaScript waits without freezing. The event loop, making and chaining promises, async/await, loading states, handling failed requests, Promise.all for parallel work and Promise.race for timeouts, all against a pretend server.",
 project="a page that loads data like a real app", steps=AS))

# =====================================================================================================  REGULAR EXPRESSIONS (JS)
RX = []
rx = chain(RX)
rx("rx1", "Does it match?",
 ["A **regular expression** is a pattern for text. In JavaScript you write it between slashes, `/\\d/`, and `pattern.test(text)` answers *is it in there?*",
  "`\\d` means any digit, `\\w` any letter, digit or underscore, `\\s` any whitespace. This course builds a set of validators and extractors, the everyday uses of regex."],
 "Write `hasDigit(text)` that returns true if the text contains a digit, using `/\\d/.test`.",
 'function hasDigit(text) {\n  return /\\d/.test(text);\n}\nconsole.log(hasDigit("room 101"), hasDigit("lobby"));\n',
 [dict(js='hasDigit("room 101") && hasDigit("7") && !hasDigit("lobby") && !hasDigit("")', msg="It's true only when there's a digit."), dict(src="\\.test\\(", msg="You use `.test`.")],
 ref=("MDN: Regular expressions", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions"))
rx("rx2", "Anchors and counts",
 ["`^` means *start of the text* and `$` *end of the text*, so `/^\\d{5}$/` matches exactly five digits and nothing else. `{5}` repeats the previous piece exactly 5 times; `{2,4}` means 2 to 4; `+` one or more; `*` zero or more; `?` optional.",
  "Without anchors, `/\\d{5}/` would happily match the middle of `abc123456`."],
 "Write `isZip(text)`: exactly five digits. Then `isPhone(text)`: three digits, a dash, four digits (`555-0199`).",
 '\nfunction isZip(text) {\n  return /^\\d{5}$/.test(text);\n}\nfunction isPhone(text) {\n  return /^\\d{3}-\\d{4}$/.test(text);\n}\n',
 [dict(js='isZip("90210") && !isZip("9021") && !isZip("902100") && !isZip("ab210")', msg="`isZip` accepts exactly five digits."), dict(js='isPhone("555-0199") && !isPhone("5550199") && !isPhone("x555-0199")', msg="`isPhone` needs 3 digits, a dash and 4 digits.")])
rx("rx3", "Choices and flags",
 ["`|` means *or*: `/^(red|green|blue)$/` matches one of three words; the parentheses group the choices so the anchors apply to all of them. A flag after the closing slash changes how matching works: `i` ignores case."],
 "Write `isPrimary(text)`: true for `red`, `green` or `blue` in any capitalisation, and nothing else.",
 '\nfunction isPrimary(text) {\n  return /^(red|green|blue)$/i.test(text);\n}\n',
 [dict(js='isPrimary("red") && isPrimary("BLUE") && isPrimary("Green")', msg="Any capitalisation works."), dict(js='!isPrimary("reddish") && !isPrimary("purple") && !isPrimary("")', msg="Other text doesn't match."), dict(src="/i", msg="You use the `i` flag.")])
rx("rx4", "Find every match",
 ["`text.match(/\\d+/g)` returns an array of **every** match thanks to the `g` (global) flag, or `null` when there are none. `|| []` turns that `null` into an empty array so the caller can always loop."],
 "Write `numbersIn(text)` returning every run of digits as numbers: `\"a1b22c333\"` gives `[1, 22, 333]`.",
 '\nfunction numbersIn(text) {\n  return (text.match(/\\d+/g) || []).map(Number);\n}\nconsole.log(numbersIn("a1b22c333"));\n',
 [dict(js='JSON.stringify(numbersIn("a1b22c333")) === "[1,22,333]"', msg="`a1b22c333` gives `[1, 22, 333]`."), dict(js='JSON.stringify(numbersIn("none here")) === "[]"', msg="No digits gives `[]`."), dict(src="/g", msg="You use the `g` flag.")])
rx("rx5", "Capture groups",
 ["Parentheses also **capture** what they matched. `\"2026-10-24\".match(/^(\\d{4})-(\\d{2})-(\\d{2})$/)` returns an array whose items 1, 2 and 3 are the year, month and day.",
  "Destructuring skips the whole match: `const [, year, month, day] = match;`"],
 "Write `parseDate(text)` returning `{ year, month, day }` as numbers for `YYYY-MM-DD` text, or `null` if it doesn't match.",
 '\nfunction parseDate(text) {\n  const match = text.match(/^(\\d{4})-(\\d{2})-(\\d{2})$/);\n  if (!match) return null;\n  const [, year, month, day] = match;\n  return { year: Number(year), month: Number(month), day: Number(day) };\n}\n',
 [dict(js='JSON.stringify(parseDate("2026-10-24")) === JSON.stringify({ year: 2026, month: 10, day: 24 })', msg="`2026-10-24` parses into numbers."), dict(js='parseDate("24/10/2026") === null && parseDate("2026-1-24") === null', msg="Other formats give `null`.")])
rx("rx6", "Named groups",
 ["`(?<hour>\\d{2})` names a group, and `match.groups.hour` reads it. Names make long patterns readable, and you don't have to count parentheses."],
 "Write `parseTime(text)` for `HH:MM` that returns `{ hour, minute }` as numbers using named groups, or `null`.",
 '\nfunction parseTime(text) {\n  const match = text.match(/^(?<hour>\\d{2}):(?<minute>\\d{2})$/);\n  if (!match) return null;\n  return { hour: Number(match.groups.hour), minute: Number(match.groups.minute) };\n}\n',
 [dict(js='JSON.stringify(parseTime("14:05")) === JSON.stringify({ hour: 14, minute: 5 })', msg="`14:05` parses."), dict(js='parseTime("2pm") === null', msg="Other text gives `null`."), dict(src="\\(\\?<\\w+>", msg="You use named groups.")])
rx("rx7", "Replace with groups",
 ["In `replace`, `$1`, `$2` and so on insert what each group captured, so you can rearrange text: `\"Lovelace, Ada\".replace(/^(\\w+), (\\w+)$/, \"$2 $1\")` gives `Ada Lovelace`."],
 "Write `flipName(text)` that turns `Last, First` into `First Last`, and leaves other text unchanged.",
 '\nfunction flipName(text) {\n  return text.replace(/^(\\w+), (\\w+)$/, "$2 $1");\n}\n',
 [dict(js='flipName("Lovelace, Ada") === "Ada Lovelace" && flipName("Hopper, Grace") === "Grace Hopper"', msg="`Last, First` becomes `First Last`."), dict(js='flipName("Ada Lovelace") === "Ada Lovelace"', msg="Text without a comma is unchanged."), dict(src="\\$2 \\$1", msg="You use `$2 $1`.")])
rx("rx8", "Replace with a function",
 ["`replace` can take a function instead of a string: it's called for each match with the match and its groups, and returns the replacement. Perfect for case changes, like `snake_case` to `camelCase`."],
 "Write `camelCase(text)`: `user_first_name` becomes `userFirstName`. Use `/_(\\w)/g` and a function that upper-cases the captured letter.",
 '\nfunction camelCase(text) {\n  return text.replace(/_(\\w)/g, (match, letter) => letter.toUpperCase());\n}\n',
 [dict(js='camelCase("user_first_name") === "userFirstName" && camelCase("id") === "id"', msg="`user_first_name` becomes `userFirstName`."), dict(js='camelCase("a_b_c") === "aBC"', msg="Every underscore is handled (the `g` flag).")])
rx("rx9", "A sensible email check",
 ["Real email addresses are wildly varied, so don't try to match the full standard. A practical check: no spaces, one `@`, something before it, and a dot in the domain followed by at least two characters: `/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/`.",
  "`[^\\s@]` is a **negated character class**: any character except whitespace or `@`. The final word on whether an address works is sending it a message."],
 "Write `looksLikeEmail(text)` with that pattern.",
 '\nfunction looksLikeEmail(text) {\n  return /^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/.test(text);\n}\n',
 [dict(js='looksLikeEmail("ada@example.com") && looksLikeEmail("first.last+tag@mail.co.uk")', msg="Normal addresses pass."), dict(js='!looksLikeEmail("ada@") && !looksLikeEmail("ada example.com") && !looksLikeEmail("a@b.c") && !looksLikeEmail("a@@b.com")', msg="Broken ones fail.")])
rx("rx10", "Split on a pattern",
 ["`split` accepts a regex too: `text.split(/[^A-Za-z']+/)` cuts at every run of non-letters, handling commas, double spaces and punctuation in one go. Filter out the empty strings at the ends.",
  "You can now validate, extract, rearrange and split text with regular expressions, a tool you'll use in every language and editor."],
 "Write `wordsIn(text)` returning the words (letters and apostrophes) in order: `\"Hello,  world! It's 2026.\"` gives `[\"Hello\", \"world\", \"It's\"]`.",
 '\nfunction wordsIn(text) {\n  return text.split(/[^A-Za-z\']+/).filter(Boolean);\n}\nconsole.log(wordsIn("Hello,  world! It\'s 2026."));\n',
 [dict(js='JSON.stringify(wordsIn("Hello,  world! It\'s 2026.")) === JSON.stringify(["Hello", "world", "It\'s"])', msg="Words come out cleanly."), dict(js='JSON.stringify(wordsIn("...")) === "[]"', msg="No words gives `[]`.")])
C.append(dict(id="js-regex", title="Regular Expressions", lang="js", hue="#fb7185", icon="target", art="/\\d+/g", hours="1.5 h",
 tagline="Validate, extract, rearrange and split text with patterns.",
 desc="Regular expressions from zero: digits and character classes, anchors and counts, alternatives and flags, global matches, capture and named groups, replacing with groups and functions, a practical email check and splitting on patterns.",
 project="a toolkit of validators and text extractors", steps=RX))

# =====================================================================================================  SQL DATA MODELING
DM = []
AUTH = """CREATE TABLE authors (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  country TEXT
);
INSERT INTO authors (name, country) VALUES
  ('Octavia E. Butler', 'USA'),
  ('Kazuo Ishiguro', 'UK'),
  ('Ursula K. Le Guin', 'USA');
"""
def dmstep(id, title, body, task, schema, query, tests, ordered=False, **k):
    DM.append(dict(id=id, title=title, body=body, task=task, solution=schema + "\n" + query + "\n", ref=schema + "\n" + query + "\n", tests=tests, ordered=ordered, **k))
S1 = AUTH
dmstep("dm1", "Primary keys and NOT NULL",
 ["**Data modeling** is deciding what tables exist, what each column may hold, and how tables connect. Good constraints make bad data impossible instead of merely unlikely.",
  "`id INTEGER PRIMARY KEY` gives every row a unique id that SQLite fills in for you. `NOT NULL` makes a column required; `UNIQUE` refuses duplicates. This course models a small bookshop."],
 "Create `authors` with `id INTEGER PRIMARY KEY`, `name TEXT NOT NULL UNIQUE` and `country TEXT`. Insert Octavia E. Butler (USA), Kazuo Ishiguro (UK) and Ursula K. Le Guin (USA) without giving ids, then select all authors.",
 S1, "SELECT * FROM authors;", [dict(src="NOT NULL UNIQUE", msg="`name` is `NOT NULL UNIQUE`."), dict(rows=True, ordered=True, msg="Three authors, with ids 1 to 3 filled in automatically.")], starter="-- A bookshop database\n")
BOOKS = """
CREATE TABLE books (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  author_id INTEGER NOT NULL REFERENCES authors(id),
  price REAL NOT NULL CHECK (price >= 0),
  status TEXT NOT NULL DEFAULT 'in stock'
);
INSERT INTO books (title, author_id, price) VALUES
  ('Kindred', 1, 12.5),
  ('Parable of the Sower', 1, 11.0),
  ('Never Let Me Go', 2, 10.0),
  ('The Dispossessed', 3, 13.0);
INSERT INTO books (title, author_id, price, status) VALUES ('Klara and the Sun', 2, 15.0, 'pre-order');
"""
S2 = S1 + BOOKS
dmstep("dm2", "Foreign keys, CHECK and DEFAULT",
 ["A **foreign key** says a column must hold the id of a row in another table: `author_id INTEGER NOT NULL REFERENCES authors(id)`. That's a **one-to-many** relationship: one author, many books.",
  "`CHECK (price >= 0)` rejects impossible values. `DEFAULT 'in stock'` fills a column you leave out of an `INSERT`."],
 "Create `books` (`id`, `title` required, `author_id` referencing `authors`, `price` required and never negative, `status` defaulting to `'in stock'`). Insert the four books from the hint without a status, plus *Klara and the Sun* (author 2, 15.0) with status `'pre-order'`. Select every book's `title` and `status`.",
 S2, "SELECT title, status FROM books;", [dict(src="REFERENCES authors", msg="`author_id` references `authors`."), dict(src="CHECK \\(price >= 0\\)", msg="`price` has a `CHECK`."), dict(src="DEFAULT 'in stock'", msg="`status` has a default."),
  dict(rows=True, ordered=True, msg="Four books are `in stock` by default and one is a pre-order.")],
 hint="Books (title, author_id, price): Kindred 1 12.5, Parable of the Sower 1 11.0, Never Let Me Go 2 10.0, The Dispossessed 3 13.0.")
S3 = "PRAGMA foreign_keys = ON;\n" + S2
dmstep("dm3", "Make SQLite enforce foreign keys",
 ["For historical reasons SQLite only *enforces* foreign keys when you switch it on for the connection: `PRAGMA foreign_keys = ON;`. Other databases always enforce them. With it on, a book pointing at author 99 is refused.",
  "Put it first, before creating and filling tables."],
 "Add `PRAGMA foreign_keys = ON;` as the very first line, and finish with `PRAGMA foreign_keys;` to confirm it reports 1.",
 S3, "PRAGMA foreign_keys;", [dict(src="^PRAGMA foreign_keys = ON;", msg="The first line switches foreign keys on."), dict(rows=True, msg="`PRAGMA foreign_keys` reports 1.")])
dmstep("dm4", "One-to-many: count, including zero",
 ["To count each author's books, including authors with none, start from `authors` and `LEFT JOIN` books. `COUNT(books.id)` counts only matched rows, so an author with no books gets 0."],
 "Add an author `Ted Chiang` (USA) with no books. List every author's `name` and number of `books`, most first, then by name.",
 S3 + "INSERT INTO authors (name, country) VALUES ('Ted Chiang', 'USA');\n",
 "SELECT authors.name, COUNT(books.id) AS books\nFROM authors\nLEFT JOIN books ON books.author_id = authors.id\nGROUP BY authors.id\nORDER BY books DESC, authors.name;",
 [dict(src="LEFT JOIN", msg="You use `LEFT JOIN`."), dict(rows=True, ordered=True, msg="Every author appears, Ted Chiang with 0.")], ordered=True)
S5 = S3 + "INSERT INTO authors (name, country) VALUES ('Ted Chiang', 'USA');\n" + """
CREATE TABLE tags (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);
CREATE TABLE book_tags (
  book_id INTEGER NOT NULL REFERENCES books(id),
  tag_id INTEGER NOT NULL REFERENCES tags(id),
  PRIMARY KEY (book_id, tag_id)
);
INSERT INTO tags (name) VALUES ('classic'), ('dystopia'), ('award-winner');
INSERT INTO book_tags VALUES (1, 1), (2, 2), (3, 2), (3, 3), (4, 1), (4, 3);
"""
dmstep("dm5", "Many-to-many with a join table",
 ["A book can have many tags and a tag many books. That's **many-to-many**, and it needs a third table, `book_tags`, holding pairs of ids. Its primary key is the *pair*, `PRIMARY KEY (book_id, tag_id)`, so the same tag can't be added to a book twice."],
 "Create `tags` (`id`, unique `name`) and `book_tags` (`book_id`, `tag_id`, both foreign keys, with a composite primary key). Insert the tags `classic`, `dystopia`, `award-winner` and the pairs (1,1), (2,2), (3,2), (3,3), (4,1), (4,3). Select the titles of books tagged `award-winner`, by title.",
 S5, "SELECT books.title\nFROM books\nJOIN book_tags ON book_tags.book_id = books.id\nJOIN tags ON tags.id = book_tags.tag_id\nWHERE tags.name = 'award-winner'\nORDER BY books.title;",
 [dict(src="PRIMARY KEY \\(book_id, tag_id\\)", msg="`book_tags` has a composite primary key."), dict(rows=True, ordered=True, msg="Never Let Me Go and The Dispossessed.")], ordered=True)
S6 = S5 + "INSERT OR IGNORE INTO authors (name, country) VALUES ('Kazuo Ishiguro', 'Japan');\n"
dmstep("dm6", "When a constraint says no",
 ["Inserting a second *Kazuo Ishiguro* breaks the `UNIQUE` rule, and the whole script stops with an error. `INSERT OR IGNORE` skips rows that would break a uniqueness rule instead, which is handy when importing data that may repeat.",
  "Use it on purpose, not to hide mistakes: the constraint is there to protect you."],
 "Try to add Kazuo Ishiguro again (country `'Japan'`) with `INSERT OR IGNORE`, then count the authors as `authors`.",
 S6, "SELECT COUNT(*) AS authors FROM authors;", [dict(src="INSERT OR IGNORE", msg="You use `INSERT OR IGNORE`."), dict(rows=True, msg="There are still 4 authors.")])
S7 = S6 + """
CREATE TABLE stock (
  book_id INTEGER PRIMARY KEY REFERENCES books(id),
  copies INTEGER NOT NULL CHECK (copies >= 0)
);
INSERT INTO stock VALUES (1, 3), (2, 1);
INSERT INTO stock (book_id, copies) VALUES (1, 2), (3, 4)
  ON CONFLICT (book_id) DO UPDATE SET copies = copies + excluded.copies;
"""
dmstep("dm7", "Upsert: insert or update",
 ["A delivery arrives: some books are new to the stock table, others need their count increased. **Upsert** does both in one statement: `INSERT ... ON CONFLICT (book_id) DO UPDATE SET copies = copies + excluded.copies`.",
  "`excluded` refers to the row you tried to insert, so `excluded.copies` is the delivery's count."],
 "Create `stock` (`book_id` as primary key and foreign key, `copies` never negative) with rows (1, 3) and (2, 1). Then upsert a delivery of (1, 2) and (3, 4) that adds to existing counts. Select `book_id` and `copies` by `book_id`.",
 S7, "SELECT book_id, copies FROM stock ORDER BY book_id;", [dict(src="ON CONFLICT \\(book_id\\) DO UPDATE", msg="You use `ON CONFLICT ... DO UPDATE`."), dict(src="excluded\\.copies", msg="You add `excluded.copies`."),
  dict(rows=True, ordered=True, msg="Book 1 has 5 copies, book 2 has 1, book 3 has 4.")], ordered=True)
S8 = S7 + """
BEGIN;
UPDATE stock SET copies = copies - 1 WHERE book_id = 2;
UPDATE books SET status = 'sold out' WHERE id = 2;
COMMIT;
BEGIN;
UPDATE stock SET copies = 0;
ROLLBACK;
"""
dmstep("dm8", "Transactions",
 ["Selling the last copy of a book means two changes: lower the stock **and** mark the book sold out. If the second fails, the first must be undone. A **transaction** makes several statements all-or-nothing: `BEGIN;` … `COMMIT;` keeps them, `ROLLBACK;` throws them away.",
  "Banks, shops and booking systems depend on this."],
 "In one transaction, sell book 2 (copies minus 1 and status `'sold out'`) and commit. Then start another transaction that sets every book's copies to 0, and roll it back. Select `title`, `status` and `copies` for every book in `stock`, by book id.",
 S8, "SELECT books.title, books.status, stock.copies\nFROM stock\nJOIN books ON books.id = stock.book_id\nORDER BY books.id;",
 [dict(src="BEGIN;[\\s\\S]*COMMIT;", msg="You commit a transaction."), dict(src="ROLLBACK;", msg="You roll one back."), dict(rows=True, ordered=True, msg="Book 2 is sold out with 0 copies, and the rolled-back change left the others alone.")], ordered=True)
S9 = S8 + "\nCREATE INDEX idx_books_author ON books (author_id);\n"
dmstep("dm9", "Indexes",
 ["An **index** is like a book's index: a sorted lookup that lets the database find rows without reading the whole table. Index the columns you filter and join on, such as foreign keys.",
  "Primary keys are indexed automatically. Indexes speed up reads and slightly slow down writes, so add them where queries need them."],
 "Create an index `idx_books_author` on `books (author_id)`. Confirm it exists: select `name` from `sqlite_master` where `type = 'index'` and the name starts with `idx_`.",
 S9, "SELECT name FROM sqlite_master WHERE type = 'index' AND name LIKE 'idx_%';", [dict(src="CREATE INDEX idx_books_author ON books ?\\(author_id\\)", msg="You index `books(author_id)`."), dict(rows=True, msg="The index is listed.")])
S10 = S9 + """
CREATE VIEW catalogue AS
SELECT books.title, authors.name AS author, books.price, COALESCE(stock.copies, 0) AS copies
FROM books
JOIN authors ON authors.id = books.author_id
LEFT JOIN stock ON stock.book_id = books.id;
"""
dmstep("dm10", "A view for the shop front",
 ["The shop's website shouldn't need to know about four tables. A **view** packages a query under a name: `CREATE VIEW catalogue AS SELECT ...`. `COALESCE(stock.copies, 0)` shows 0 for books with no stock row.",
  "You've modelled a real database: keys, constraints, one-to-many and many-to-many relationships, upserts, transactions, indexes and views."],
 "Create a view `catalogue` with each book's `title`, `author` name, `price` and `copies` (0 when there's no stock row). Select from it the books with at least 1 copy, cheapest first.",
 S10, "SELECT title, author, price, copies FROM catalogue WHERE copies >= 1 ORDER BY price;",
 [dict(src="CREATE VIEW catalogue", msg="You create the `catalogue` view."), dict(src="COALESCE\\(", msg="You use `COALESCE` for missing stock."), dict(rows=True, ordered=True, msg="Never Let Me Go and Kindred are in stock, cheapest first.")], ordered=True)
C.append(dict(id="sql-modeling", title="SQL Data Modeling", lang="sql", hue="#4ade80", icon="db", art="PK ⟷ FK", hours="1.5 h", seed="",
 schema="You create every table yourself in this course.",
 tagline="Keys, constraints, relationships, upserts, transactions, indexes and views.",
 desc="Design a bookshop database the way professionals do: primary and foreign keys, NOT NULL, UNIQUE, CHECK and DEFAULT, one-to-many and many-to-many relationships, conflict handling, upserts, transactions, indexes and views.",
 project="a bookshop database", steps=DM))

# =====================================================================================================  TRACKS AND LEVELS
TRACK = {"web-page": ("web", "Beginner"), "css-layout": ("web", "Beginner"), "a11y-html": ("web", "Intermediate"), "js-dom": ("web", "Intermediate"), "js-async": ("javascript", "Intermediate"),
         "python-zero": ("python", "Beginner"), "py-strings": ("python", "Beginner"), "py-functions": ("python", "Intermediate"), "python-oop": ("python", "Intermediate"), "py-testing": ("python", "Intermediate"),
         "js-zero": ("javascript", "Beginner"), "js-arrays": ("javascript", "Beginner"), "js-regex": ("javascript", "Intermediate"),
         "sql-zero": ("data", "Beginner"), "sql-analytics": ("data", "Intermediate"), "sql-modeling": ("data", "Intermediate"),
         "algorithms-py": ("cs", "Intermediate")}
TRACKS = [
  {"id": "web", "name": "Web foundations", "icon": "globe", "blurb": "HTML, CSS and the DOM: build pages that look good and work for everyone."},
  {"id": "python", "name": "Python", "icon": "code", "blurb": "The friendliest first language, from your first print to tested, well-structured code."},
  {"id": "javascript", "name": "JavaScript", "icon": "braces", "blurb": "The language of the web: data, patterns, text and asynchronous code."},
  {"id": "data", "name": "Data & SQL", "icon": "db", "blurb": "Ask questions of data, then design databases that keep it correct."},
  {"id": "cs", "name": "Computer science", "icon": "flow", "blurb": "The algorithms behind everything, measured and built by hand."}]
order = {t["id"]: i for i, t in enumerate(TRACKS)}
lvl = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
for c in C:
    c["track"], c["level"] = TRACK[c["id"]]
C.sort(key=lambda c: (order[c["track"]], lvl[c["level"]], list(TRACK).index(c["id"])))
