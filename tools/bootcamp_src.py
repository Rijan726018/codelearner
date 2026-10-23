"""Source for data/bootcamp.json (run tools/build_bootcamp.py).
Each step's starter code is the previous step's solution unless a step sets `starter`.
Check types: out / outHas / outRe (stdout), src (regex on the code), py / js (expression after the code runs, with _out and _src),
html: sel + exists/nonempty/text/attr(+val,re)/style(+val,re)/count, sql: rows(+ordered)/cols/count computed from `ref`."""

C = []

# =====================================================================================================  HTML & CSS
C.append(dict(id="web-page", title="Build Your First Web Page", lang="html", hue="#ff5c93", icon="globe", art="</>", hours="2 h",
 tagline="HTML structure and CSS style, with a live preview.",
 desc="Every website is HTML (the content and structure) dressed up with CSS (the style). Write both, watch your page appear as you type, and finish with a styled profile page.",
 project="your own profile page", steps=[
 dict(id="w1", title="Your first HTML element",
  body=["HTML describes the content of a page using **elements**. Most elements have an opening tag like `<h1>`, some content, and a closing tag with a slash like `</h1>`.","`<h1>` is the biggest heading on a page. Browsers show it large and bold. The preview on the right updates as you type."],
  example="<h1>Welcome to my site</h1>",
  task="Below the comment, add an `<h1>` element containing your name, for example `<h1>Hi, I'm Ada</h1>`.",
  starter="<!-- Write your code below this line -->\n",
  solution="<!-- Write your code below this line -->\n<h1>Hi, I'm Ada</h1>\n",
  tests=[dict(sel="h1", msg="Your page has an `h1` element."), dict(sel="h1", nonempty=True, msg="Your `h1` has some text inside it.")],
  hint="Type the opening tag `<h1>`, then your text, then the closing tag `</h1>`."),
 dict(id="w2", title="Paragraphs",
  body=["The `<p>` element holds a paragraph of text. Browsers add a little space above and below each paragraph automatically.","Elements are written in the order they appear on the page, top to bottom."],
  task="Under your heading, add a `<p>` element with one sentence about yourself.",
  solution="<!-- Write your code below this line -->\n<h1>Hi, I'm Ada</h1>\n<p>I'm learning to code so I can build my own apps.</p>\n",
  tests=[dict(sel="p", msg="Your page has a `p` element."), dict(sel="p", nonempty=True, msg="Your paragraph has text."), dict(sel="h1", msg="Your `h1` is still there.")],
  hint="`<p>Your sentence here.</p>`"),
 dict(id="w3", title="Sub-headings",
  body=["Headings go from `<h1>` (most important) down to `<h6>`. Use one `<h1>` per page, then `<h2>` for sections, `<h3>` for sub-sections, and so on.","Search engines and screen readers use headings to understand how your page is organised, so pick them by meaning, not by size."],
  task="Add an `<h2>` with the text `About me`, then a new paragraph under it.",
  solution="<!-- Write your code below this line -->\n<h1>Hi, I'm Ada</h1>\n<p>I'm learning to code so I can build my own apps.</p>\n<h2>About me</h2>\n<p>I live in London and I love puzzles, music and long walks.</p>\n",
  tests=[dict(sel="h2", text="About me", msg="There's an `h2` with the text About me."), dict(sel="p", count=2, msg="Your page has at least two paragraphs.")]),
 dict(id="w4", title="Emphasis: strong and em",
  body=["Inside text you can mark words as important with `<strong>` (shown in bold) or emphasised with `<em>` (shown in italics).","These are **inline** elements: they sit inside a line of text instead of starting a new block."],
  example="<p>I <strong>really</strong> like <em>tea</em>.</p>",
  task="In one of your paragraphs, wrap a word in `<strong>` and another word in `<em>`.",
  solution="<!-- Write your code below this line -->\n<h1>Hi, I'm Ada</h1>\n<p>I'm learning to code so I can build my <strong>own</strong> apps.</p>\n<h2>About me</h2>\n<p>I live in London and I love <em>puzzles</em>, music and long walks.</p>\n",
  tests=[dict(sel="p strong", msg="A paragraph contains a `strong` element."), dict(sel="p em", msg="A paragraph contains an `em` element.")]),
 dict(id="w5", title="Lists",
  body=["An unordered (bulleted) list is a `<ul>` element containing one `<li>` (list item) per bullet. Use `<ol>` instead for a numbered list.","Elements inside other elements are called **children**. Indenting children makes your HTML much easier to read."],
  example="<ul>\n  <li>Python</li>\n  <li>HTML</li>\n</ul>",
  task="Add an `<h2>` that says `My skills`, followed by a `<ul>` with at least three `<li>` items.",
  solution="<!-- Write your code below this line -->\n<h1>Hi, I'm Ada</h1>\n<p>I'm learning to code so I can build my <strong>own</strong> apps.</p>\n<h2>About me</h2>\n<p>I live in London and I love <em>puzzles</em>, music and long walks.</p>\n<h2>My skills</h2>\n<ul>\n  <li>HTML</li>\n  <li>CSS</li>\n  <li>Problem solving</li>\n</ul>\n",
  tests=[dict(sel="h2", count=2, msg="You have two `h2` headings."), dict(sel="ul", msg="Your page has a `ul` list."), dict(sel="ul li", count=3, msg="The list has at least three `li` items.")]),
 dict(id="w6", title="Links",
  body=["The anchor element `<a>` makes a link. Its `href` **attribute** says where the link goes. Attributes live inside the opening tag: `name=\"value\"`.","The text between `<a>` and `</a>` is what people click."],
  example='<a href="https://developer.mozilla.org">MDN Web Docs</a>',
  task="Add a paragraph containing a link to a website you like. The `href` must start with `https://`.",
  solution="<!-- Write your code below this line -->\n<h1>Hi, I'm Ada</h1>\n<p>I'm learning to code so I can build my <strong>own</strong> apps.</p>\n<h2>About me</h2>\n<p>I live in London and I love <em>puzzles</em>, music and long walks.</p>\n<h2>My skills</h2>\n<ul>\n  <li>HTML</li>\n  <li>CSS</li>\n  <li>Problem solving</li>\n</ul>\n<p>My favourite site: <a href=\"https://developer.mozilla.org\">MDN Web Docs</a></p>\n",
  tests=[dict(sel="a", msg="Your page has an `a` element."), dict(sel="a", attr="href", val="^https://", re=True, msg="The link's `href` starts with `https://`."), dict(sel="a", nonempty=True, msg="The link has clickable text.")]),
 dict(id="w7", title="Images and alt text",
  body=["`<img>` shows an image. It has no closing tag. `src` is the image's address and `alt` describes it for people using screen readers, and for everyone when the image fails to load.","Good alt text says what matters about the picture in a few words. It's not optional: it's how a large part of the web's audience experiences images."],
  example='<img src="https://picsum.photos/200" alt="A random landscape photo">',
  task="Add an `<img>` with a `src` and a meaningful `alt` description. Any image address works; if it can't load, the alt text shows instead.",
  solution="<!-- Write your code below this line -->\n<h1>Hi, I'm Ada</h1>\n<img src=\"https://picsum.photos/160\" alt=\"A photo that represents me\">\n<p>I'm learning to code so I can build my <strong>own</strong> apps.</p>\n<h2>About me</h2>\n<p>I live in London and I love <em>puzzles</em>, music and long walks.</p>\n<h2>My skills</h2>\n<ul>\n  <li>HTML</li>\n  <li>CSS</li>\n  <li>Problem solving</li>\n</ul>\n<p>My favourite site: <a href=\"https://developer.mozilla.org\">MDN Web Docs</a></p>\n",
  tests=[dict(sel="img", msg="Your page has an `img` element."), dict(sel="img", attr="src", val=".+", re=True, msg="The image has a `src`."), dict(sel="img", attr="alt", val="\\S{2,}", re=True, msg="The image has a meaningful `alt` description.")]),
 dict(id="w8", title="Group content with main",
  body=["Semantic elements describe *what* a region is. `<main>` wraps the main content of a page; `<header>`, `<nav>`, `<section>` and `<footer>` mark other regions.","They don't change how things look, but they help screen readers, search engines and other developers."],
  task="Wrap everything below the comment (heading, image, paragraphs, list and link) in a single `<main>` element.",
  solution="<!-- Write your code below this line -->\n<main>\n  <h1>Hi, I'm Ada</h1>\n  <img src=\"https://picsum.photos/160\" alt=\"A photo that represents me\">\n  <p>I'm learning to code so I can build my <strong>own</strong> apps.</p>\n  <h2>About me</h2>\n  <p>I live in London and I love <em>puzzles</em>, music and long walks.</p>\n  <h2>My skills</h2>\n  <ul>\n    <li>HTML</li>\n    <li>CSS</li>\n    <li>Problem solving</li>\n  </ul>\n  <p>My favourite site: <a href=\"https://developer.mozilla.org\">MDN Web Docs</a></p>\n</main>\n",
  tests=[dict(sel="main", msg="Your page has a `main` element."), dict(sel="main h1", msg="The `h1` is inside `main`."), dict(sel="main ul", msg="The list is inside `main`."), dict(sel="main a", msg="The link is inside `main`.")]),
 dict(id="w9", title="A complete HTML document",
  body=["Real pages have a skeleton: `<!DOCTYPE html>` on the first line, then `<html>` containing a `<head>` (information about the page) and a `<body>` (what you see).","The `<title>` in the head is the text shown on the browser tab and in search results."],
  example="<!DOCTYPE html>\n<html>\n<head>\n  <title>My Profile</title>\n</head>\n<body>\n  ...your content...\n</body>\n</html>",
  task="Turn your code into a full document: add `<!DOCTYPE html>`, `<html>`, a `<head>` with a `<title>`, and put your `<main>` inside `<body>`. You can delete the comment.",
  solution="<!DOCTYPE html>\n<html>\n<head>\n  <title>Ada's Profile</title>\n</head>\n<body>\n  <main>\n    <h1>Hi, I'm Ada</h1>\n    <img src=\"https://picsum.photos/160\" alt=\"A photo that represents me\">\n    <p>I'm learning to code so I can build my <strong>own</strong> apps.</p>\n    <h2>About me</h2>\n    <p>I live in London and I love <em>puzzles</em>, music and long walks.</p>\n    <h2>My skills</h2>\n    <ul>\n      <li>HTML</li>\n      <li>CSS</li>\n      <li>Problem solving</li>\n    </ul>\n    <p>My favourite site: <a href=\"https://developer.mozilla.org\">MDN Web Docs</a></p>\n  </main>\n</body>\n</html>\n",
  tests=[dict(src="<!DOCTYPE html>", msg="The first line is `<!DOCTYPE html>`."), dict(src="<html[\\s>][\\s\\S]*</html>", msg="Everything is inside `<html>` … `</html>`."), dict(sel="head title", nonempty=True, msg="The `head` has a `title` with text."), dict(src="<body[\\s>][\\s\\S]*<main", msg="`main` is inside `<body>`.")]),
 dict(id="w10", title="Your first CSS rule",
  body=["CSS styles HTML. A **rule** has a selector (which elements), then properties in braces: `h1 { color: tomato; }`.","For now, put CSS inside a `<style>` element in the `<head>`. Colours can be names (`tomato`), hex codes (`#5b45f0`) or `rgb(91, 69, 240)`."],
  example="<style>\n  h1 { color: #5b45f0; }\n</style>",
  task="Add a `<style>` element inside `<head>` and give your `h1` a colour other than black.",
  solution="<!DOCTYPE html>\n<html>\n<head>\n  <title>Ada's Profile</title>\n  <style>\n    h1 { color: #5b45f0; }\n  </style>\n</head>\n<body>\n  <main>\n    <h1>Hi, I'm Ada</h1>\n    <img src=\"https://picsum.photos/160\" alt=\"A photo that represents me\">\n    <p>I'm learning to code so I can build my <strong>own</strong> apps.</p>\n    <h2>About me</h2>\n    <p>I live in London and I love <em>puzzles</em>, music and long walks.</p>\n    <h2>My skills</h2>\n    <ul>\n      <li>HTML</li>\n      <li>CSS</li>\n      <li>Problem solving</li>\n    </ul>\n    <p>My favourite site: <a href=\"https://developer.mozilla.org\">MDN Web Docs</a></p>\n  </main>\n</body>\n</html>\n",
  tests=[dict(sel="head style", msg="There's a `style` element in the `head`."), dict(sel="h1", style="color", val="^(?!rgb\\(0, 0, 0\\)$)", re=True, msg="Your `h1` is not black.")]),
 dict(id="w11", title="Fonts and backgrounds",
  body=["Styles on `body` apply to the whole page, because most text properties are **inherited** by the elements inside.","`font-family` picks a typeface; always end with a generic fallback like `sans-serif`. `background-color` fills the page."],
  example="body {\n  font-family: Arial, sans-serif;\n  background-color: #f4f1ff;\n}",
  task="Add a `body` rule that sets `font-family` to a list ending in `sans-serif` and gives the page a `background-color`.",
  solution="<!DOCTYPE html>\n<html>\n<head>\n  <title>Ada's Profile</title>\n  <style>\n    body {\n      font-family: Arial, sans-serif;\n      background-color: #f4f1ff;\n    }\n    h1 { color: #5b45f0; }\n  </style>\n</head>\n<body>\n  <main>\n    <h1>Hi, I'm Ada</h1>\n    <img src=\"https://picsum.photos/160\" alt=\"A photo that represents me\">\n    <p>I'm learning to code so I can build my <strong>own</strong> apps.</p>\n    <h2>About me</h2>\n    <p>I live in London and I love <em>puzzles</em>, music and long walks.</p>\n    <h2>My skills</h2>\n    <ul>\n      <li>HTML</li>\n      <li>CSS</li>\n      <li>Problem solving</li>\n    </ul>\n    <p>My favourite site: <a href=\"https://developer.mozilla.org\">MDN Web Docs</a></p>\n  </main>\n</body>\n</html>\n",
  tests=[dict(sel="body", style="font-family", val="sans-serif", re=True, msg="The body's font list includes `sans-serif`."), dict(sel="body", style="background-color", val="^(?!rgba\\(0, 0, 0, 0\\)$)", re=True, msg="The body has a background colour.")]),
 dict(id="w12", title="Classes and the box model",
  body=["A **class** lets you style chosen elements: add `class=\"card\"` in the HTML and target it in CSS with a dot, `.card { … }`.","Every element is a box: content, then **padding** (space inside the border), then the border, then **margin** (space outside). `border-radius` rounds the corners."],
  example=".card {\n  background-color: white;\n  padding: 24px;\n  border-radius: 16px;\n}",
  task="Give your `<main>` the class `card`, then write a `.card` rule with a `background-color`, some `padding` and a `border-radius`.",
  solution="<!DOCTYPE html>\n<html>\n<head>\n  <title>Ada's Profile</title>\n  <style>\n    body {\n      font-family: Arial, sans-serif;\n      background-color: #f4f1ff;\n    }\n    h1 { color: #5b45f0; }\n    .card {\n      background-color: white;\n      padding: 24px;\n      border-radius: 16px;\n    }\n  </style>\n</head>\n<body>\n  <main class=\"card\">\n    <h1>Hi, I'm Ada</h1>\n    <img src=\"https://picsum.photos/160\" alt=\"A photo that represents me\">\n    <p>I'm learning to code so I can build my <strong>own</strong> apps.</p>\n    <h2>About me</h2>\n    <p>I live in London and I love <em>puzzles</em>, music and long walks.</p>\n    <h2>My skills</h2>\n    <ul>\n      <li>HTML</li>\n      <li>CSS</li>\n      <li>Problem solving</li>\n    </ul>\n    <p>My favourite site: <a href=\"https://developer.mozilla.org\">MDN Web Docs</a></p>\n  </main>\n</body>\n</html>\n",
  tests=[dict(sel="main.card", msg="`main` has the class `card`."), dict(sel=".card", style="padding-top", val="^(?!0px$)", re=True, msg="`.card` has padding."), dict(sel=".card", style="border-top-left-radius", val="^(?!0px$)", re=True, msg="`.card` has rounded corners."), dict(sel=".card", style="background-color", val="^(?!rgba\\(0, 0, 0, 0\\)$)", re=True, msg="`.card` has a background colour.")]),
 dict(id="w13", title="Centre the card",
  body=["`max-width` stops a box from getting too wide on big screens, which keeps lines of text comfortable to read.","Setting the left and right margins to `auto` splits the leftover space equally, which centres a block horizontally: `margin: 0 auto;` (0 top and bottom, auto left and right)."],
  task="In `.card`, set a `max-width` (for example `600px`) and centre it with `margin: 0 auto;`.",
  solution="<!DOCTYPE html>\n<html>\n<head>\n  <title>Ada's Profile</title>\n  <style>\n    body {\n      font-family: Arial, sans-serif;\n      background-color: #f4f1ff;\n    }\n    h1 { color: #5b45f0; }\n    .card {\n      background-color: white;\n      padding: 24px;\n      border-radius: 16px;\n      max-width: 600px;\n      margin: 0 auto;\n    }\n  </style>\n</head>\n<body>\n  <main class=\"card\">\n    <h1>Hi, I'm Ada</h1>\n    <img src=\"https://picsum.photos/160\" alt=\"A photo that represents me\">\n    <p>I'm learning to code so I can build my <strong>own</strong> apps.</p>\n    <h2>About me</h2>\n    <p>I live in London and I love <em>puzzles</em>, music and long walks.</p>\n    <h2>My skills</h2>\n    <ul>\n      <li>HTML</li>\n      <li>CSS</li>\n      <li>Problem solving</li>\n    </ul>\n    <p>My favourite site: <a href=\"https://developer.mozilla.org\">MDN Web Docs</a></p>\n  </main>\n</body>\n</html>\n",
  tests=[dict(sel=".card", style="max-width", val="^(?!none$)", re=True, msg="`.card` has a `max-width`."), dict(src="margin\\s*:\\s*0(px)?\\s+auto|margin-left\\s*:\\s*auto", msg="`.card` uses `margin: 0 auto` to centre itself.")]),
 dict(id="w14", title="Style links and hover",
  body=["A **pseudo-class** styles an element in a particular state. `a:hover` applies while the mouse is over a link.","Hover effects tell people something is clickable. Keep the change visible but not jarring."],
  example="a { color: #0891b2; }\na:hover { color: #e11d74; }",
  task="Add an `a` rule that sets a link colour, and an `a:hover` rule that changes something when the link is hovered.",
  solution="<!DOCTYPE html>\n<html>\n<head>\n  <title>Ada's Profile</title>\n  <style>\n    body {\n      font-family: Arial, sans-serif;\n      background-color: #f4f1ff;\n    }\n    h1 { color: #5b45f0; }\n    .card {\n      background-color: white;\n      padding: 24px;\n      border-radius: 16px;\n      max-width: 600px;\n      margin: 0 auto;\n    }\n    a { color: #0891b2; }\n    a:hover { color: #e11d74; }\n  </style>\n</head>\n<body>\n  <main class=\"card\">\n    <h1>Hi, I'm Ada</h1>\n    <img src=\"https://picsum.photos/160\" alt=\"A photo that represents me\">\n    <p>I'm learning to code so I can build my <strong>own</strong> apps.</p>\n    <h2>About me</h2>\n    <p>I live in London and I love <em>puzzles</em>, music and long walks.</p>\n    <h2>My skills</h2>\n    <ul>\n      <li>HTML</li>\n      <li>CSS</li>\n      <li>Problem solving</li>\n    </ul>\n    <p>My favourite site: <a href=\"https://developer.mozilla.org\">MDN Web Docs</a></p>\n  </main>\n</body>\n</html>\n",
  tests=[dict(src="(^|[\\s}])a\\s*\\{[^}]*color", msg="There's an `a` rule that sets `color`."), dict(src="a:hover\\s*\\{", msg="There's an `a:hover` rule.")]),
 dict(id="w15", title="Flexbox: skills in a row",
  body=["`display: flex` lays out an element's children in a row. `gap` adds space between them.","`list-style: none` removes bullets, and `padding: 0` removes the list's default indent. A little padding and a background on each `li` turns them into tags."],
  example="ul {\n  display: flex;\n  gap: 8px;\n  list-style: none;\n  padding: 0;\n}",
  task="Make the skills list a flex row: give `ul` `display: flex`, a `gap`, and `list-style: none`. Style `li` with a `background-color` and some `padding` so each skill looks like a tag.",
  solution="<!DOCTYPE html>\n<html>\n<head>\n  <title>Ada's Profile</title>\n  <style>\n    body {\n      font-family: Arial, sans-serif;\n      background-color: #f4f1ff;\n    }\n    h1 { color: #5b45f0; }\n    .card {\n      background-color: white;\n      padding: 24px;\n      border-radius: 16px;\n      max-width: 600px;\n      margin: 0 auto;\n    }\n    a { color: #0891b2; }\n    a:hover { color: #e11d74; }\n    ul {\n      display: flex;\n      gap: 8px;\n      list-style: none;\n      padding: 0;\n    }\n    li {\n      background-color: #ebe8ff;\n      padding: 6px 12px;\n      border-radius: 99px;\n    }\n  </style>\n</head>\n<body>\n  <main class=\"card\">\n    <h1>Hi, I'm Ada</h1>\n    <img src=\"https://picsum.photos/160\" alt=\"A photo that represents me\">\n    <p>I'm learning to code so I can build my <strong>own</strong> apps.</p>\n    <h2>About me</h2>\n    <p>I live in London and I love <em>puzzles</em>, music and long walks.</p>\n    <h2>My skills</h2>\n    <ul>\n      <li>HTML</li>\n      <li>CSS</li>\n      <li>Problem solving</li>\n    </ul>\n    <p>My favourite site: <a href=\"https://developer.mozilla.org\">MDN Web Docs</a></p>\n  </main>\n</body>\n</html>\n",
  tests=[dict(sel="ul", style="display", val="flex", msg="`ul` uses `display: flex`."), dict(sel="ul", style="list-style-type", val="none", msg="The bullets are gone (`list-style: none`)."), dict(sel="li", style="background-color", val="^(?!rgba\\(0, 0, 0, 0\\)$)", re=True, msg="Each `li` has a background colour."), dict(sel="li", style="padding-left", val="^(?!0px$)", re=True, msg="Each `li` has padding.")]),
 dict(id="w16", title="Add a footer and ship it",
  body=["A `<footer>` closes a page: credits, contact links, copyright. Put it inside `body`, after `main`.","You've built a real web page. To put it online for free, look up GitHub Pages or Netlify Drop: both host a single HTML file in a couple of minutes."],
  task="After `</main>`, add a `<footer>` with a short line of text, for example `Built by Ada with HTML and CSS`.",
  solution="<!DOCTYPE html>\n<html>\n<head>\n  <title>Ada's Profile</title>\n  <style>\n    body {\n      font-family: Arial, sans-serif;\n      background-color: #f4f1ff;\n    }\n    h1 { color: #5b45f0; }\n    .card {\n      background-color: white;\n      padding: 24px;\n      border-radius: 16px;\n      max-width: 600px;\n      margin: 0 auto;\n    }\n    a { color: #0891b2; }\n    a:hover { color: #e11d74; }\n    ul {\n      display: flex;\n      gap: 8px;\n      list-style: none;\n      padding: 0;\n    }\n    li {\n      background-color: #ebe8ff;\n      padding: 6px 12px;\n      border-radius: 99px;\n    }\n  </style>\n</head>\n<body>\n  <main class=\"card\">\n    <h1>Hi, I'm Ada</h1>\n    <img src=\"https://picsum.photos/160\" alt=\"A photo that represents me\">\n    <p>I'm learning to code so I can build my <strong>own</strong> apps.</p>\n    <h2>About me</h2>\n    <p>I live in London and I love <em>puzzles</em>, music and long walks.</p>\n    <h2>My skills</h2>\n    <ul>\n      <li>HTML</li>\n      <li>CSS</li>\n      <li>Problem solving</li>\n    </ul>\n    <p>My favourite site: <a href=\"https://developer.mozilla.org\">MDN Web Docs</a></p>\n  </main>\n  <footer>Built by Ada with HTML and CSS</footer>\n</body>\n</html>\n",
  tests=[dict(sel="footer", msg="Your page has a `footer`."), dict(sel="footer", nonempty=True, msg="The footer has text."), dict(sel="main + footer", msg="The footer comes right after `main`.")]),
]))

# =====================================================================================================  PYTHON
PY = []
def py(id, title, body, task, add_code, tests, hint=None, example=None):
    prev = PY[-1]["solution"] if PY else ""
    PY.append(dict(id=id, title=title, body=body, task=task, solution=prev + add_code, tests=tests, **({"hint":hint} if hint else {}), **({"example":example} if example else {})))

py("p1","Hello, world!",
 ["A program is a list of instructions the computer runs from top to bottom. In Python, `print()` shows something on the screen.","Text in code is called a **string** and goes inside quotes. Press **Check your code** (or Ctrl/⌘ + Enter) to run your program and see the output."],
 "Write a line that prints exactly `Hello, world!`",
 'print("Hello, world!")\n',
 [dict(out="Hello, world!", msg="The output is exactly `Hello, world!`")],
 hint='`print("Hello, world!")` — mind the capital H, the comma and the exclamation mark.')
py("p2","Several lines",
 ["Each `print()` call prints one line. Python runs them in order.","A line starting with `#` is a **comment**. Python ignores it; it's a note for humans."],
 "Below your first line, add two more `print()` calls: one with your name and one with why you're learning to code.",
 '# About me\nprint("My name is Ada")\nprint("I want to build my own apps")\n',
 [dict(outRe="Hello, world!\\n.+\\n.+", msg="Your program prints at least three lines."), dict(src="#", msg="Your code has a comment.")],
 example='print("first line")\nprint("second line")')
py("p3","Python is a calculator",
 ["Python does maths with `+`, `-`, `*` (multiply) and `/` (divide). Numbers don't need quotes.","`print(2 + 3)` prints `5`, but `print(\"2 + 3\")` prints the text `2 + 3`. Quotes make all the difference."],
 "Print how many hours there are in a year: `365 * 24`.",
 'print(365 * 24)\n',
 [dict(outHas="8760", msg="The output includes 8760.")])
py("p4","Variables",
 ["A **variable** is a name for a value: `student = \"Ada\"`. The `=` means *store this value under this name*, not *is equal to*.","After that, use the name anywhere you'd use the value: `print(student)`."],
 "Create a variable `student` holding the string `\"Ada\"` and print it.",
 '\nstudent = "Ada"\nprint(student)\n',
 [dict(py='student == "Ada"', msg="`student` holds the text `Ada`."), dict(py='"Ada" in _out', msg="Your program prints the student's name.")])
py("p5","Numbers in variables",
 ["Variables can hold numbers too. Integers like `88` are written without quotes.","You can combine variables in expressions: `total = a + b + c` adds them and stores the result."],
 "Create `score1 = 88`, `score2 = 92` and `score3 = 79`. Store their sum in `total` and print it.",
 'score1 = 88\nscore2 = 92\nscore3 = 79\ntotal = score1 + score2 + score3\nprint(total)\n',
 [dict(py="score1 == 88 and score2 == 92 and score3 == 79", msg="The three scores are 88, 92 and 79."), dict(py="total == 259", msg="`total` is 259."), dict(outHas="259", msg="The total is printed.")])
py("p6","Division and rounding",
 ["`/` always gives a decimal number (a **float**): `7 / 2` is `3.5`.","`round(x, 1)` rounds to one decimal place: `round(86.333, 1)` is `86.3`."],
 "Compute `average = total / 3`, then print it rounded to one decimal place.",
 'average = total / 3\nprint(round(average, 1))\n',
 [dict(py="abs(average - 259 / 3) < 1e-9", msg="`average` is `total / 3`."), dict(outHas="86.3", msg="The rounded average 86.3 is printed.")])
py("p7","f-strings",
 ["An **f-string** puts values inside text. Write `f` before the quotes and put expressions in braces: `f\"{student} scored {total}\"`.","It's the cleanest way to build messages from variables."],
 "Print a sentence in exactly this shape, using an f-string: `Ada averaged 86.3`",
 'print(f"{student} averaged {round(average, 1)}")\n',
 [dict(src='f"|f\'', msg="You used an f-string."), dict(py='"Ada averaged 86.3" in _out', msg="The output contains `Ada averaged 86.3`.")],
 example='name = "Grace"\nage = 85\nprint(f"{name} is {age} years old")')
py("p8","Decisions with if / elif / else",
 ["`if` runs a block only when a condition is true. Indent the block with 4 spaces; the indentation is how Python knows what's inside.","`elif` (else if) checks the next condition only when the previous ones were false; `else` catches everything left."],
 "Set `grade` to `\"A\"` if `average >= 90`, `\"B\"` if `>= 80`, `\"C\"` if `>= 70`, otherwise `\"F\"`. Then print `grade`.",
 'if average >= 90:\n    grade = "A"\nelif average >= 80:\n    grade = "B"\nelif average >= 70:\n    grade = "C"\nelse:\n    grade = "F"\nprint(grade)\n',
 [dict(src="elif", msg="You used `elif`."), dict(py='grade == "B"', msg="With an average of 86.3, `grade` is `B`.")],
 example='temperature = 30\nif temperature > 25:\n    print("Hot")\nelse:\n    print("Not hot")')
py("p9","True or False",
 ["A comparison like `average >= 60` produces a **boolean**: `True` or `False`.","Comparisons: `==` equal, `!=` not equal, `<`, `>`, `<=`, `>=`. Note the double `==` for comparing; single `=` stores."],
 "Create `passed` holding the result of `average >= 60`, and print it.",
 'passed = average >= 60\nprint(passed)\n',
 [dict(py="passed is True", msg="`passed` is `True`."), dict(py='"True" in _out', msg="`True` is printed.")])
py("p10","Lists",
 ["A **list** holds many values in order: `scores = [88, 92, 79]`.","Positions (indexes) start at 0: `scores[0]` is the first item. `len(scores)` is how many items there are."],
 "Create `scores = [88, 92, 79]`, then print the first score and the length of the list.",
 'scores = [88, 92, 79]\nprint(scores[0])\nprint(len(scores))\n',
 [dict(py="scores == [88, 92, 79]", msg="`scores` is `[88, 92, 79]`."), dict(src="scores\\[0\\]", msg="You printed `scores[0]`."), dict(src="len\\(scores\\)", msg="You printed `len(scores)`.")])
py("p11","Loops: for",
 ["A `for` loop runs its block once for each item: `for s in scores:` gives `s` each value in turn.","Loops are how one short program can process a million items."],
 "Write a `for` loop over `scores` that prints each score.",
 'for s in scores:\n    print(s)\n',
 [dict(src="for\\s+\\w+\\s+in\\s+scores\\s*:", msg="There's a `for … in scores:` loop."), dict(py='_out.count("88") >= 2 and "92" in _out and "79" in _out', msg="Each score is printed.")],
 example='for fruit in ["apple", "pear"]:\n    print(fruit)')
py("p12","Add up with a loop",
 ["The **accumulator** pattern: start a variable at 0, then add each item to it inside a loop. `x += 5` is short for `x = x + 5`.","You'll use this pattern for sums, counts, maximums and more, in every language."],
 "Recompute `total` with a loop: set `total = 0`, add each score with `+=`, then print `total`.",
 'total = 0\nfor s in scores:\n    total += s\nprint(total)\n',
 [dict(src="\\+=", msg="You used `+=` inside a loop."), dict(py="total == 259", msg="`total` is 259 again.")])
py("p13","Functions",
 ["A **function** packages code under a name so you can reuse it. `def` defines it; parameters go in parentheses; `return` sends a result back.","Calling `average_of([1, 2, 3])` runs the body with `nums` set to that list."],
 "Define `average_of(nums)` that returns the average of a list of numbers. (`sum(nums)` and `len(nums)` will help.)",
 '\ndef average_of(nums):\n    return sum(nums) / len(nums)\n',
 [dict(py="abs(average_of([1, 2, 3]) - 2) < 1e-9", msg="`average_of([1, 2, 3])` returns 2."), dict(py="average_of([10]) == 10", msg="`average_of([10])` returns 10."), dict(py="abs(average_of([88, 92, 79]) - 259 / 3) < 1e-9", msg="It works on `scores` too.")],
 example='def greet(name):\n    return f"Hello, {name}!"\n\nprint(greet("Ada"))')
py("p14","A grading function",
 ["Functions can contain `if` statements. A `return` immediately ends the function, so the first matching branch wins.","Small functions with one job are easy to test, and you'll test them all the time."],
 "Define `letter_grade(avg)` that returns `\"A\"`, `\"B\"`, `\"C\"` or `\"F\"` using the same thresholds as before.",
 '\ndef letter_grade(avg):\n    if avg >= 90:\n        return "A"\n    if avg >= 80:\n        return "B"\n    if avg >= 70:\n        return "C"\n    return "F"\n',
 [dict(py='letter_grade(95) == "A"', msg="`letter_grade(95)` is A."), dict(py='letter_grade(85) == "B"', msg="`letter_grade(85)` is B."), dict(py='letter_grade(72) == "C"', msg="`letter_grade(72)` is C."), dict(py='letter_grade(50) == "F"', msg="`letter_grade(50)` is F."), dict(py='letter_grade(90) == "A" and letter_grade(80) == "B"', msg="Boundaries work: 90 is A and 80 is B.")])
py("p15","Dictionaries",
 ["A **dictionary** maps keys to values: `ages = {\"Ada\": 36, \"Alan\": 41}`. Look up with `ages[\"Ada\"]`.","Values can be anything, even lists."],
 'Create `students` mapping `"Ada"` to `[88, 92, 79]`, `"Linus"` to `[70, 65, 81]` and `"Grace"` to `[95, 98, 91]`.',
 '\nstudents = {\n    "Ada": [88, 92, 79],\n    "Linus": [70, 65, 81],\n    "Grace": [95, 98, 91],\n}\n',
 [dict(py='students["Ada"] == [88, 92, 79]', msg="Ada's scores are right."), dict(py='students["Linus"] == [70, 65, 81]', msg="Linus's scores are right."), dict(py='students["Grace"] == [95, 98, 91]', msg="Grace's scores are right."), dict(py="len(students) == 3", msg="There are exactly three students.")])
py("p16","Loop over a dictionary",
 ["`for name, marks in students.items():` gives you each key and value together.","Now combine everything: functions inside a loop, inside an f-string."],
 "Loop over `students` and print one line per student in the form `Ada: B`, using your two functions.",
 '\nfor name, marks in students.items():\n    print(f"{name}: {letter_grade(average_of(marks))}")\n',
 [dict(src="\\.items\\(\\)", msg="You looped with `.items()`."), dict(py='"Ada: B" in _out', msg="`Ada: B` is printed."), dict(py='"Linus: C" in _out', msg="`Linus: C` is printed."), dict(py='"Grace: A" in _out', msg="`Grace: A` is printed.")])
py("p17","Find the top student",
 ["To find the best item, keep a **best so far** and replace it whenever you see something better.","Start `best_avg` at `-1` so the first student always beats it."],
 "Find the student with the highest average. Store their name in `best` and print it.",
 '\nbest = None\nbest_avg = -1\nfor name, marks in students.items():\n    avg = average_of(marks)\n    if avg > best_avg:\n        best, best_avg = name, avg\nprint(f"Top student: {best}")\n',
 [dict(py='best == "Grace"', msg="`best` is Grace."), dict(py='"Grace" in _out.splitlines()[-1]', msg="The last line printed mentions Grace.")])
py("p18","Class average: your program is complete",
 ["Lists can be combined with `+`, and `sum()` works on any list of numbers.","You just wrote a real program: variables, decisions, loops, functions and data structures. That's the core of every language."],
 "Compute `class_average`: the average of **all nine** scores from every student. Print it rounded to 2 decimals.",
 '\nall_scores = []\nfor marks in students.values():\n    all_scores += marks\nclass_average = average_of(all_scores)\nprint(f"Class average: {round(class_average, 2)}")\n',
 [dict(py="abs(class_average - 759 / 9) < 1e-9", msg="`class_average` is the average of all nine scores."), dict(py='"84.33" in _out', msg="It prints 84.33.")],
 hint="Collect every score into one list first, then reuse `average_of`.")
C.append(dict(id="python-zero", title="Python from Zero", lang="python", hue="#38d3f0", icon="code", art="py>", hours="3 h",
 tagline="Your first programming language, one idea at a time.",
 desc="The friendliest place to start. Print, store values, make decisions, repeat with loops and write functions, all while building a small grade-report program.",
 project="a student grade-report program", steps=PY))

# =====================================================================================================  JAVASCRIPT
JS = []
def js(id, title, body, task, add_code, tests, hint=None, example=None):
    prev = JS[-1]["solution"] if JS else ""
    JS.append(dict(id=id, title=title, body=body, task=task, solution=prev + add_code, tests=tests, **({"hint":hint} if hint else {}), **({"example":example} if example else {})))
js("j1","Hello, JavaScript",
 ["JavaScript is the language of the web: every browser runs it. `console.log()` prints a value to the console (the output panel).","Statements usually end with a semicolon `;`."],
 "Print exactly `Hello, JavaScript!`",
 'console.log("Hello, JavaScript!");\n',
 [dict(out="Hello, JavaScript!", msg="The output is exactly `Hello, JavaScript!`")])
js("j2","const and let",
 ["`const` creates a variable that can't be reassigned. `let` creates one that can.","Default to `const`; use `let` only when the value must change."],
 'Create `const shop = "Code Café";` and `let items = 0;` then print `shop`.',
 'const shop = "Code Café";\nlet items = 0;\nconsole.log(shop);\n',
 [dict(js='shop === "Code Café"', msg="`shop` is `Code Café`."), dict(js="items === 0", msg="`items` starts at 0."), dict(src="const\\s+shop", msg="`shop` is declared with `const`."), dict(src="let\\s+items", msg="`items` is declared with `let`.")])
js("j3","Numbers and maths",
 ["JavaScript has one number type for integers and decimals. Use `+ - * /` and `%` (remainder).","Decimals can surprise you: `0.1 + 0.2` is `0.30000000000000004`, because computers store numbers in binary. That's why shops often count in cents."],
 "Create `const price = 4.5;` and `const qty = 3;` then print `price * qty`.",
 'const price = 4.5;\nconst qty = 3;\nconsole.log(price * qty);\n',
 [dict(js="price === 4.5 && qty === 3", msg="`price` is 4.5 and `qty` is 3."), dict(js='_out.includes("13.5")', msg="13.5 is printed.")])
js("j4","Template literals",
 ["Backtick strings can embed values: `` `Total: ${price * qty}` ``. Anything inside `${ }` is evaluated.","They can also span several lines, which is handy for building text."],
 "Print exactly `3 coffees cost $13.5` using a template literal with `qty` and `price * qty`.",
 'console.log(`${qty} coffees cost $${price * qty}`);\n',
 [dict(src="`", msg="You used a template literal (backticks)."), dict(js='_out.includes("3 coffees cost $13.5")', msg="The output includes `3 coffees cost $13.5`.")])
js("j5","if / else",
 ["`if (condition) { … } else { … }` chooses a branch. Comparisons: `===` (equal), `!==`, `<`, `>`, `<=`, `>=`.","Always use `===` rather than `==`: the double version converts types in surprising ways (`0 == \"\"` is true!)."],
 "Create `const total = price * qty;` and `let shipping;`. If `total >= 20`, set `shipping` to 0, otherwise 5. Print `shipping`.",
 'const total = price * qty;\nlet shipping;\nif (total >= 20) {\n  shipping = 0;\n} else {\n  shipping = 5;\n}\nconsole.log(shipping);\n',
 [dict(src="if\\s*\\(", msg="You used an `if` statement."), dict(js="shipping === 5", msg="With a total of 13.5, `shipping` is 5.")])
js("j6","The ternary operator",
 ["`condition ? a : b` is a compact if/else that produces a value.","Great for simple choices; use a full `if` when either branch gets long."],
 'Create `const freeShipping = total >= 20 ? "yes" : "no";` and print it.',
 'const freeShipping = total >= 20 ? "yes" : "no";\nconsole.log(freeShipping);\n',
 [dict(src="\\?[^:]+:", msg="You used `? :`."), dict(js='freeShipping === "no"', msg="`freeShipping` is `no`.")])
js("j7","Arrays",
 ["An **array** is an ordered list: `const cart = [4.5, 3.25, 6];`. Indexes start at 0.","`cart.length` is the number of items, and `cart.push(x)` adds one to the end."],
 "Create `const cart = [4.5, 3.25, 6];` and print its length.",
 'const cart = [4.5, 3.25, 6];\nconsole.log(cart.length);\n',
 [dict(js="JSON.stringify(cart) === '[4.5,3.25,6]'", msg="`cart` is `[4.5, 3.25, 6]`."), dict(src="cart\\.length", msg="You printed `cart.length`.")])
js("j8","Loops: for...of",
 ["`for (const item of cart) { … }` runs once per item.","Combine it with an accumulator to total things up."],
 "Create `let sum = 0;` and use a `for...of` loop to add every price in `cart` to `sum`. Print `sum`.",
 'let sum = 0;\nfor (const p of cart) {\n  sum += p;\n}\nconsole.log(sum);\n',
 [dict(src="for\\s*\\(\\s*(const|let)\\s+\\w+\\s+of\\s+cart", msg="You used `for (… of cart)`."), dict(js="sum === 13.75", msg="`sum` is 13.75.")])
js("j9","Functions",
 ["`function addTax(amount) { return amount * 1.1; }` defines a reusable function. `return` gives back the result.","Calling `addTax(10)` returns `11.000000000000002`. Floating point again, which is why money code rounds."],
 "Define `function addTax(amount)` that returns the amount plus 10% tax.",
 '\nfunction addTax(amount) {\n  return amount * 1.1;\n}\n',
 [dict(js="typeof addTax === 'function'", msg="`addTax` is a function."), dict(js="Math.abs(addTax(10) - 11) < 1e-9", msg="`addTax(10)` returns 11."), dict(js="Math.abs(addTax(0)) < 1e-9", msg="`addTax(0)` returns 0.")])
js("j10","Arrow functions",
 ["Arrow functions are a shorter syntax: `const double = n => n * 2;`. With two parameters, use parentheses: `(a, b) => a + b`.","You'll see them everywhere in modern JavaScript, especially with array methods."],
 "Create `const discount = (amount, pct) => …` that returns the amount reduced by `pct` percent.",
 'const discount = (amount, pct) => amount * (1 - pct / 100);\n',
 [dict(src="=>", msg="You used an arrow function."), dict(js="discount(100, 20) === 80", msg="`discount(100, 20)` is 80."), dict(js="discount(50, 0) === 50", msg="`discount(50, 0)` is 50.")])
js("j11","Objects",
 ["An **object** groups related values under named keys: `{ name: \"Latte\", price: 4.5 }`.","Read a value with a dot: `item.name`."],
 'Create `const item = { name: "Latte", price: 4.5, qty: 2 };` and print `item.name`.',
 'const item = { name: "Latte", price: 4.5, qty: 2 };\nconsole.log(item.name);\n',
 [dict(js='item.name === "Latte" && item.price === 4.5 && item.qty === 2', msg="`item` has the right name, price and qty."), dict(js='_out.includes("Latte")', msg="`Latte` is printed.")])
js("j12","An array of objects",
 ["Real data is usually a list of objects, one per thing: users, products, orders.","This shape is exactly what JSON from a web API looks like."],
 'Create `order`: an array of three objects: Latte (4.5, qty 2), Bagel (3.25, qty 1) and Juice (6, qty 1), each with `name`, `price` and `qty`.',
 'const order = [\n  { name: "Latte", price: 4.5, qty: 2 },\n  { name: "Bagel", price: 3.25, qty: 1 },\n  { name: "Juice", price: 6, qty: 1 },\n];\n',
 [dict(js="Array.isArray(order) && order.length === 3", msg="`order` has three items."), dict(js='order[0].name === "Latte" && order[0].qty === 2', msg="The first item is two Lattes."), dict(js='order[1].price === 3.25 && order[2].price === 6', msg="Bagel costs 3.25 and Juice costs 6.")])
js("j13","map: transform every item",
 ["`array.map(fn)` returns a **new** array with `fn` applied to each item. The original is unchanged.","`order.map(i => i.name)` gives `[\"Latte\", \"Bagel\", \"Juice\"]`."],
 "Create `lineTotals` with `map`: each item's `price * qty`.",
 'const lineTotals = order.map(i => i.price * i.qty);\n',
 [dict(src="\\.map\\(", msg="You used `.map`."), dict(js="JSON.stringify(lineTotals) === '[9,3.25,6]'", msg="`lineTotals` is `[9, 3.25, 6]`.")])
js("j14","filter: keep some items",
 ["`array.filter(fn)` keeps the items for which `fn` returns true.","Chaining `filter` then `map` reads like a sentence: keep these, then transform them."],
 "Create `pricey`: the items in `order` whose `price` is more than 4.",
 'const pricey = order.filter(i => i.price > 4);\n',
 [dict(src="\\.filter\\(", msg="You used `.filter`."), dict(js='pricey.length === 2 && pricey.every(i => i.price > 4)', msg="`pricey` holds the two items over 4.")])
js("j15","reduce: combine into one value",
 ["`array.reduce((acc, item) => …, start)` walks the array carrying an accumulator. It's the functional version of the loop-and-add pattern.","Always pass the starting value (here `0`); it avoids a crash on empty arrays."],
 "Create `orderTotal` using `reduce`: the sum of `price * qty` over the whole order.",
 'const orderTotal = order.reduce((s, i) => s + i.price * i.qty, 0);\nconsole.log(orderTotal);\n',
 [dict(src="\\.reduce\\(", msg="You used `.reduce`."), dict(js="orderTotal === 18.25", msg="`orderTotal` is 18.25.")])
js("j16","Print a receipt",
 ["Put it all together: a function that takes data and returns a formatted string.","`array.join(\"\\n\")` glues strings together with newlines between them."],
 "Write `function receipt(order)` that returns one line per item like `Latte x2 = 9`, then a final line `Total: 18.25`. Print `receipt(order)`.",
 '\nfunction receipt(order) {\n  const lines = order.map(i => `${i.name} x${i.qty} = ${i.price * i.qty}`);\n  const total = order.reduce((s, i) => s + i.price * i.qty, 0);\n  lines.push(`Total: ${total}`);\n  return lines.join("\\n");\n}\nconsole.log(receipt(order));\n',
 [dict(js="typeof receipt === 'function'", msg="`receipt` is a function."), dict(js='receipt(order).includes("Latte x2 = 9")', msg="The receipt has the line `Latte x2 = 9`."), dict(js='receipt(order).includes("Total: 18.25")', msg="The receipt ends with `Total: 18.25`."), dict(js='receipt([{name:"Tea",price:2,qty:3}]).includes("Total: 6")', msg="It works for any order, not just this one.")])
C.append(dict(id="js-zero", title="JavaScript from Zero", lang="js", hue="#fbbf24", icon="braces", art="{js}", hours="3 h",
 tagline="The language every browser speaks.",
 desc="Variables, decisions, arrays, functions and objects, then the modern trio of map, filter and reduce, by building a café order calculator that prints a receipt.",
 project="a café order calculator with receipts", steps=JS))

# =====================================================================================================  SQL
SEED = """CREATE TABLE directors (id INTEGER PRIMARY KEY, name TEXT, country TEXT);
INSERT INTO directors VALUES (1,'Christopher Nolan','UK'),(2,'Greta Gerwig','USA'),(3,'Bong Joon-ho','South Korea'),(4,'Hayao Miyazaki','Japan'),(5,'Denis Villeneuve','Canada');
CREATE TABLE movies (id INTEGER PRIMARY KEY, title TEXT, year INTEGER, genre TEXT, score REAL, director_id INTEGER REFERENCES directors(id));
INSERT INTO movies VALUES (1,'Inception',2010,'Sci-Fi',8.8,1),(2,'Interstellar',2014,'Sci-Fi',8.7,1),(3,'The Dark Knight',2008,'Action',9.0,1),(4,'Oppenheimer',2023,'Drama',8.4,1),(5,'Lady Bird',2017,'Drama',7.4,2),(6,'Little Women',2019,'Drama',7.8,2),(7,'Barbie',2023,'Comedy',6.9,2),(8,'Parasite',2019,'Thriller',8.5,3),(9,'Snowpiercer',2013,'Sci-Fi',7.1,3),(10,'Spirited Away',2001,'Animation',8.6,4),(11,'Princess Mononoke',1997,'Animation',8.3,4),(12,'Arrival',2016,'Sci-Fi',7.9,5),(13,'Dune',2021,'Sci-Fi',8.0,5);
"""
SQ = []
def sq(id, title, body, task, ref, tests, hint=None, example=None, ordered=False):
    SQ.append(dict(id=id, title=title, body=body, task=task, solution=ref, ref=ref, ordered=ordered, starter="-- Write your query below\n", tests=tests, **({"hint":hint} if hint else {}), **({"example":example} if example else {})))
sq("q1","SELECT everything",
 ["A database stores data in **tables**: rows (records) and columns (fields). SQL is the language for asking questions of it.","`SELECT * FROM movies;` returns every column (`*`) of every row in the `movies` table."],
 "Select every column from the `movies` table.", "SELECT * FROM movies;",
 [dict(rows=True, msg="Your query returns all 13 movies with every column.")])
sq("q2","Choose columns",
 ["List the columns you want, separated by commas, instead of `*`. Asking only for what you need is faster and clearer.","Column names come back in the order you list them."],
 "Select just the `title` and `year` of every movie.", "SELECT title, year FROM movies;",
 [dict(cols=["title","year"], msg="The result has exactly the columns `title` and `year`."), dict(rows=True, msg="Every movie is included.")])
sq("q3","Filter with WHERE",
 ["`WHERE` keeps only rows that match a condition: `WHERE year > 2015`.","Text values go in single quotes: `WHERE genre = 'Drama'`."],
 "Select the `title` of every movie released **after 2015**.", "SELECT title FROM movies WHERE year > 2015;",
 [dict(src="WHERE", msg="You used `WHERE`."), dict(rows=True, msg="You get exactly the movies after 2015.")])
sq("q4","AND and OR",
 ["Combine conditions with `AND` (both must be true) and `OR` (either).","Use parentheses when you mix them, so the meaning is unambiguous."],
 "Select the `title` and `score` of **Sci-Fi** movies with a score of **at least 8.0**.", "SELECT title, score FROM movies WHERE genre = 'Sci-Fi' AND score >= 8.0;",
 [dict(src="AND", msg="You combined conditions with `AND`."), dict(rows=True, msg="You get exactly the Sci-Fi movies scoring 8.0 or more.")])
sq("q5","Sort with ORDER BY",
 ["`ORDER BY score DESC` sorts from highest to lowest; `ASC` (the default) sorts lowest first.","Without ORDER BY, a database may return rows in any order. Never rely on it."],
 "Select `title` and `score` for all movies, highest score first.", "SELECT title, score FROM movies ORDER BY score DESC;",
 [dict(src="ORDER\\s+BY", msg="You used `ORDER BY`."), dict(rows=True, ordered=True, msg="All movies appear, sorted by score from high to low.")], ordered=True)
sq("q6","Top N with LIMIT",
 ["`LIMIT 3` keeps only the first three rows of the result.","Combined with ORDER BY, it answers every 'top N' question."],
 "Select the `title` of the **3 highest-scoring** movies.", "SELECT title FROM movies ORDER BY score DESC LIMIT 3;",
 [dict(src="LIMIT", msg="You used `LIMIT`."), dict(rows=True, ordered=True, msg="You get the top three titles, best first.")], ordered=True)
sq("q7","Count rows",
 ["**Aggregate functions** summarise many rows into one: `COUNT(*)`, `SUM(col)`, `AVG(col)`, `MIN(col)`, `MAX(col)`.","`SELECT COUNT(*) FROM movies WHERE …` counts matching rows."],
 "Count how many movies are in the **Drama** genre.", "SELECT COUNT(*) FROM movies WHERE genre = 'Drama';",
 [dict(src="COUNT\\s*\\(", msg="You used `COUNT`."), dict(rows=True, msg="The count is correct.")])
sq("q8","Group with GROUP BY",
 ["`GROUP BY genre` splits rows into one group per genre; aggregates then run once per group.","Every selected column must either be in the GROUP BY or inside an aggregate."],
 "For each `genre`, show the genre and how many movies it has.", "SELECT genre, COUNT(*) FROM movies GROUP BY genre;",
 [dict(src="GROUP\\s+BY", msg="You used `GROUP BY`."), dict(rows=True, msg="One row per genre with the right counts.")])
sq("q9","Averages and aliases",
 ["`AVG(score)` averages a column. `ROUND(x, 2)` rounds to two decimals.","`AS` gives a result column a readable name: `ROUND(AVG(score), 2) AS avg_score`."],
 "For each `genre`, show the genre and its average score rounded to 2 decimals, named `avg_score`.", "SELECT genre, ROUND(AVG(score), 2) AS avg_score FROM movies GROUP BY genre;",
 [dict(cols=["genre","avg_score"], msg="The columns are `genre` and `avg_score`."), dict(rows=True, msg="Each genre's rounded average is correct.")])
sq("q10","Filter groups with HAVING",
 ["`WHERE` filters rows **before** grouping; `HAVING` filters groups **after** aggregating.","So 'genres with more than 2 movies' needs `HAVING COUNT(*) > 2`."],
 "Show each `genre` that has **more than 2** movies, with its count.", "SELECT genre, COUNT(*) FROM movies GROUP BY genre HAVING COUNT(*) > 2;",
 [dict(src="HAVING", msg="You used `HAVING`."), dict(rows=True, msg="Only genres with more than two movies appear.")])
sq("q11","JOIN two tables",
 ["Movies store a `director_id`, not the director's name. That avoids repeating data. A **JOIN** puts it back together.","`FROM movies JOIN directors ON movies.director_id = directors.id` pairs each movie with its director's row."],
 "Show each movie's `title` with its director's `name`.", "SELECT movies.title, directors.name FROM movies JOIN directors ON movies.director_id = directors.id;",
 [dict(src="JOIN", msg="You used `JOIN`."), dict(rows=True, msg="Every movie appears with its director's name.")],
 example="SELECT a.col, b.col\nFROM a\nJOIN b ON a.b_id = b.id;")
sq("q12","JOIN + GROUP BY",
 ["Joins and aggregates combine naturally: join first, then group by a column from either table.","This is the heart of analytics queries."],
 "Show each director's `name` and the number of movies they directed.", "SELECT directors.name, COUNT(*) FROM movies JOIN directors ON movies.director_id = directors.id GROUP BY directors.name;",
 [dict(src="JOIN", msg="You used `JOIN`."), dict(src="GROUP\\s+BY", msg="You used `GROUP BY`."), dict(rows=True, msg="Each director appears with the right count.")])
sq("q13","INSERT a row",
 ["`INSERT INTO movies (title, year, genre, score, director_id) VALUES (...)` adds a row. The `id` fills itself in.","Each run starts from a fresh copy of the database, so experiment freely."],
 "Insert Christopher Nolan's **Tenet** (2020, genre `Action`, score 7.3, `director_id` 1). Then run `SELECT COUNT(*) FROM movies;` to prove there are now 14.", "INSERT INTO movies (title, year, genre, score, director_id) VALUES ('Tenet', 2020, 'Action', 7.3, 1);\nSELECT COUNT(*) FROM movies;",
 [dict(src="INSERT\\s+INTO", msg="You used `INSERT INTO`."), dict(rows=True, msg="The final count is 14.")],
 hint="Two statements, each ending in a semicolon: the INSERT, then the SELECT.")
sq("q14","UPDATE carefully",
 ["`UPDATE movies SET score = 9.1 WHERE title = 'Arrival';` changes matching rows.","**Always** write the WHERE first. An UPDATE without WHERE changes every row in the table."],
 "Set Arrival's score to `8.2`, then select the `title` and `score` of Arrival to confirm.", "UPDATE movies SET score = 8.2 WHERE title = 'Arrival';\nSELECT title, score FROM movies WHERE title = 'Arrival';",
 [dict(src="UPDATE", msg="You used `UPDATE`."), dict(src="UPDATE[\\s\\S]*WHERE", msg="Your UPDATE has a `WHERE`."), dict(rows=True, msg="Arrival now scores 8.2.")])
sq("q15","Subqueries",
 ["A query can contain another query in parentheses. `(SELECT AVG(score) FROM movies)` evaluates to a single number you can compare against.","Subqueries let you answer two-step questions in one statement."],
 "Select the `title` of every movie that scores **above the average** score of all movies.", "SELECT title FROM movies WHERE score > (SELECT AVG(score) FROM movies);",
 [dict(src="\\(\\s*SELECT", msg="You used a subquery."), dict(rows=True, msg="You get exactly the above-average movies.")])
C.append(dict(id="sql-zero", title="SQL from Zero", lang="sql", hue="#a3e635", icon="db", art="SQL", hours="2 h", seed=SEED,
 schema="movies(id, title, year, genre, score, director_id)\ndirectors(id, name, country)",
 tagline="Ask questions of data. Every app has a database.",
 desc="Query a real SQLite database of films and directors: filter, sort, count, group, join tables and change data safely. The most useful skill in tech that isn't a programming language.",
 project="a film-database analysis", steps=SQ))

# =====================================================================================================  CSS LAYOUT
LAYOUT_HTML = """<!DOCTYPE html>
<html>
<head>
  <title>Layout Lab</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; background: #f6f7fb; color: #0e1330; }
    header { background: #0e1330; color: white; padding: 16px 24px; }
    section { padding: 24px; }
    .card { background: white; border-radius: 14px; padding: 20px; box-shadow: 0 4px 14px rgba(0,0,0,.08); }
    .gallery div { background: #ebe8ff; border-radius: 10px; padding: 30px; text-align: center; font-weight: bold; }
    /* Write your CSS below this line */

  </style>
</head>
<body>
  <header><h1>Layout Lab</h1></header>
  <section>
    <h2>Plans</h2>
    <div class="cards">
      <div class="card"><h3>Starter</h3><p>For learning the basics.</p></div>
      <div class="card"><h3>Builder</h3><p>For your first projects.</p></div>
      <div class="card"><h3>Pro</h3><p>For shipping real products.</p></div>
    </div>
  </section>
  <section>
    <h2>Gallery</h2>
    <div class="gallery">
      <div class="wide">1</div><div>2</div><div>3</div><div>4</div><div>5</div><div>6</div>
    </div>
  </section>
</body>
</html>
"""
LY = []
def ly(id, title, body, task, css, tests, hint=None, example=None, html_change=None):
    prev = LY[-1]["solution"] if LY else LAYOUT_HTML
    sol = prev.replace("\n  </style>", css + "\n  </style>", 1) if css else prev
    if html_change: sol = sol.replace(*html_change)
    LY.append(dict(id=id, title=title, body=body, task=task, solution=sol, tests=tests, **({"starter": LAYOUT_HTML} if not LY else {}), **({"hint":hint} if hint else {}), **({"example":example} if example else {})))
ly("l1","Flexbox: a row of cards",
 ["Flexbox arranges a container's direct children along a line. Turn it on with `display: flex` on the **container**, not the children.","The three plan cards are inside `.cards`. Right now they stack vertically, because `div`s are blocks."],
 "Below the comment in the `<style>`, make `.cards` a flex container.",
 "\n    .cards {\n      display: flex;", [dict(sel=".cards", style="display", val="flex", msg="`.cards` has `display: flex`.")],
 hint="`.cards { display: flex; }` — the closing brace comes in the next steps; for now you can close it yourself.")
LY[-1]["solution"] = LY[-1]["solution"].replace("display: flex;\n  </style>", "display: flex;\n    }\n  </style>")
def ly_into_cards(id, title, body, task, decl, tests, **k):
    prev = LY[-1]["solution"]
    i = prev.index(".cards {"); j = prev.index("\n    }", i)
    sol = prev[:j] + "\n" + decl + prev[j:]
    LY.append(dict(id=id, title=title, body=body, task=task, solution=sol, tests=tests, **k))
ly_into_cards("l2","Gap between items",
 ["`gap` puts space between flex items without adding it to the outside edges, so no more fiddling with margins.","It works in Grid too."],
 "Give `.cards` a `gap` (for example `16px`).", "      gap: 16px;",
 [dict(sel=".cards", style="column-gap", val="^(?!normal$|0px$)", re=True, msg="`.cards` has a `gap`.")])
ly_into_cards("l3","Grow to fill",
 ["Flex items can share leftover space. `flex: 1` on each item means *grow equally*.","Put this on the **children** (`.cards .card`), not the container."],
 "Make every card inside `.cards` grow equally to fill the row (`flex: 1`), and make the row wrap on small screens with `flex-wrap: wrap` on `.cards`.", "      flex-wrap: wrap;",
 [dict(sel=".cards", style="flex-wrap", val="wrap", msg="`.cards` wraps (`flex-wrap: wrap`)."), dict(sel=".cards .card", style="flex-grow", val="1", msg="Each card grows (`flex: 1`).")])
LY[-1]["solution"] = LY[-1]["solution"].replace("\n  </style>", "\n    .cards .card {\n      flex: 1;\n      min-width: 180px;\n    }\n  </style>", 1)
ly("l4","Grid: three columns",
 ["CSS Grid lays out items in rows **and** columns. `grid-template-columns: repeat(3, 1fr)` makes three equal columns; `fr` means a fraction of the free space.","Use Flexbox for one-dimensional rows, Grid for two-dimensional layouts."],
 "Make `.gallery` a grid with three equal columns.",
 "\n    .gallery {\n      display: grid;\n      grid-template-columns: repeat(3, 1fr);\n    }",
 [dict(sel=".gallery", style="display", val="grid", msg="`.gallery` has `display: grid`."), dict(sel=".gallery", style="grid-template-columns", val="^\\S+ \\S+ \\S+$", re=True, msg="The grid has three columns.")])
def ly_into_gallery(id, title, body, task, decl, tests, **k):
    prev = LY[-1]["solution"]
    sol = prev.replace("grid-template-columns: repeat(3, 1fr);\n    }", "grid-template-columns: repeat(3, 1fr);\n" + decl + "\n    }", 1)
    LY.append(dict(id=id, title=title, body=body, task=task, solution=sol, tests=tests, **k))
ly_into_gallery("l5","Grid gaps",
 ["`gap` works the same way in Grid: space between rows and columns.","You can set them separately with `row-gap` and `column-gap`."],
 "Add a `gap` to `.gallery`.", "      gap: 12px;",
 [dict(sel=".gallery", style="row-gap", val="^(?!normal$|0px$)", re=True, msg="`.gallery` has a `gap`.")])
ly("l6","Span two columns",
 ["Items can span several tracks: `grid-column: span 2` makes an item two columns wide.","The tile with class `wide` is a good candidate for a featured image."],
 "Make `.gallery .wide` span two columns.",
 "\n    .gallery .wide {\n      grid-column: span 2;\n    }",
 [dict(sel=".gallery .wide", style="grid-column-start", val="span 2", msg="`.wide` spans two columns.")])
ly("l7","Responsive with a media query",
 ["A **media query** applies CSS only when a condition holds, usually the screen width: `@media (max-width: 600px) { … }`.","Design for small screens first, then add columns as space allows, and test by resizing your browser."],
 "Add a media query that, below 600px wide, switches `.gallery` to a single column (`grid-template-columns: 1fr`).",
 "\n    @media (max-width: 600px) {\n      .gallery { grid-template-columns: 1fr; }\n    }",
 [dict(src="@media\\s*\\(\\s*max-width\\s*:\\s*\\d+px\\s*\\)", msg="There's a `@media (max-width: …)` query."), dict(src="@media[^{]*\\{[^}]*\\.gallery\\s*\\{[^}]*grid-template-columns\\s*:\\s*1fr", msg="Inside it, `.gallery` becomes one column.")])
ly("l8","Sticky header",
 ["`position: sticky; top: 0;` keeps an element pinned to the top once you scroll past it, while it still takes up its normal space.","Give it a `z-index` so content scrolls underneath rather than over it."],
 "Make the `header` sticky at the top.",
 "\n    header {\n      position: sticky;\n      top: 0;\n      z-index: 10;\n    }",
 [dict(sel="header", style="position", val="sticky", msg="`header` has `position: sticky`."), dict(sel="header", style="top", val="0px", msg="It sticks at `top: 0`.")])
ly("l9","CSS custom properties",
 ["Custom properties (CSS variables) store values for reuse: define `--brand: #5b45f0;` in `:root`, use it with `var(--brand)`.","Change one line and your whole colour scheme follows. Design systems are built on them."],
 "Define `--brand` in `:root` and use `var(--brand)` as the `header`'s background colour.",
 "\n    :root { --brand: #5b45f0; }\n    header { background: var(--brand); }",
 [dict(src="--brand\\s*:", msg="`--brand` is defined."), dict(src="var\\(\\s*--brand\\s*\\)", msg="`var(--brand)` is used."), dict(sel="header", style="background-color", val="^(?!rgb\\(14, 19, 48\\)$)", re=True, msg="The header's background changed.")])
ly("l10","Hover transitions",
 ["`transition: transform 0.2s;` animates changes to `transform` instead of jumping.","Pair it with a `:hover` rule. A small lift (`translateY(-4px)`) is a classic card effect."],
 "Give `.card` a `transition` on `transform`, and make `.card:hover` move up with `transform: translateY(-4px)`.",
 "\n    .card { transition: transform 0.2s; }\n    .card:hover { transform: translateY(-4px); }",
 [dict(sel=".card", style="transition-property", val="transform|all", re=True, msg="`.card` transitions `transform`."), dict(src="\\.card:hover\\s*\\{[^}]*transform", msg="`.card:hover` sets a `transform`.")])
C.append(dict(id="css-layout", title="CSS Layout Lab", lang="html", hue="#8b7dff", icon="grid", art="⊞", hours="1.5 h",
 tagline="Flexbox, Grid and responsive design.",
 desc="Take a plain page and give it a modern layout: flex rows, grid galleries, spanning tiles, media queries, a sticky header, CSS variables and smooth hover effects.",
 project="a responsive landing page", steps=LY))
