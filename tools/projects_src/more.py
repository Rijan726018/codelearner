from _lib import *

# =============================================================================================== MARKDOWN CONVERTER (JavaScript)
S = []
C = Code('''// Markdown to HTML converter

function escapeHtml(text) {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
''')
S.append(step("md1", "Escape HTML first",
  ["Markdown is text people write; HTML is what browsers run. If someone types `<script>`, it must appear as text, never as code. Escaping replaces `&`, `<` and `>` with **entities**: `&amp;`, `&lt;` and `&gt;`.",
   "Order matters: replace `&` first. Otherwise the `&` inside a freshly made `&lt;` would be escaped again."],
  "Write `escapeHtml(text)` that replaces `&`, `<` and `>` with `&amp;`, `&lt;` and `&gt;`, in that order. Use regular expressions with the `g` flag so every occurrence is replaced.",
  C.text, [dict(js='escapeHtml("<b>&") === "&lt;b&gt;&amp;"', msg="`<b>&` becomes `&lt;b&gt;&amp;`."), dict(js='escapeHtml("a & b & c") === "a &amp; b &amp; c"', msg="Every occurrence is replaced, not just the first."),
           dict(js='escapeHtml("&lt;") === "&amp;lt;"', msg="`&` is escaped first, so text that looks like an entity stays as written.")],
  starter="// Markdown to HTML converter\n", core="s7m4", ref=("MDN: String.prototype.replace", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/replace")))
C.add('''
function inline(text) {
  return escapeHtml(text)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\\*\\*([^*]+)\\*\\*/g, "<strong>$1</strong>")
    .replace(/\\*([^*]+)\\*/g, "<em>$1</em>");
}
''')
S.append(step("md2", "Bold, italics and code",
  ["Inline formatting is a job for **regular expressions** with capture groups: `/\\*\\*([^*]+)\\*\\*/g` matches `**…**` and captures the inside, which the replacement refers to as `$1`.",
   "Handle `**bold**` before `*italic*`, or the single-star rule would eat half of each double star."],
  "Write `inline(text)` that escapes the text, then converts `` `code` `` to `<code>`, `**bold**` to `<strong>` and `*italic*` to `<em>`.",
  C.text, [dict(js='inline("**hi**") === "<strong>hi</strong>"', msg="`**hi**` becomes `<strong>hi</strong>`."), dict(js='inline("*a* and **b**") === "<em>a</em> and <strong>b</strong>"', msg="Italic and bold work side by side."),
           dict(js='inline("use `x < y`") === "use <code>x &lt; y</code>"', msg="Code spans work, and their contents are escaped."), dict(js='inline("<script>") === "&lt;script&gt;"', msg="HTML in the text is still escaped.")],
  ref=("MDN: Regular expressions guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions")))
C.sub('''    .replace(/\\*([^*]+)\\*/g, "<em>$1</em>");''', '''    .replace(/\\*([^*]+)\\*/g, "<em>$1</em>")
    .replace(/\\[([^\\]]+)\\]\\(([^)\\s]+)\\)/g, '<a href="$2">$1</a>');''')
S.append(step("md3", "Links",
  ["A Markdown link is `[text](url)`. Square brackets and parentheses are special in regular expressions, so escape them: `\\[`, `\\]`, `\\(`, `\\)`.",
   "Two capture groups give you both parts: `$1` is the text and `$2` the address."],
  "Extend `inline` to turn `[text](url)` into `<a href=\"url\">text</a>`.",
  C.text, [dict(js='inline("[MDN](https://developer.mozilla.org)") === \'<a href="https://developer.mozilla.org">MDN</a>\'', msg="A link becomes an `<a>` tag."),
           dict(js='inline("see [**docs**](/d) now") === \'see <a href="/d"><strong>docs</strong></a> now\'', msg="Formatting inside link text works.")]))
C.add('''
function heading(line) {
  const match = line.match(/^(#{1,6}) (.+)$/);
  if (!match) return null;
  const level = match[1].length;
  return `<h${level}>${inline(match[2])}</h${level}>`;
}
''')
S.append(step("md4", "Headings",
  ["A heading line starts with 1 to 6 `#` and a space: `## Setup`. `line.match(regex)` returns `null` or an array of captures; the number of `#` characters is the heading level.",
   "Returning `null` for non-headings lets the caller ask *is this a heading?* and get the HTML in one call."],
  "Write `heading(line)` returning `<hN>…</hN>` (with inline formatting) for lines starting with 1–6 `#` and a space, and `null` otherwise.",
  C.text, [dict(js='heading("# Title") === "<h1>Title</h1>" && heading("### *Note*") === "<h3><em>Note</em></h3>"', msg="Headings of different levels convert, with formatting."),
           dict(js='heading("#NoSpace") === null && heading("plain text") === null', msg="Other lines return `null`."), dict(js='heading("####### seven") === null', msg="Seven `#` is not a heading.")]))
CONV1 = '''
function convert(markdown) {
  const out = [];
  let paragraph = [];
  const flush = () => {
    if (paragraph.length) {
      out.push(`<p>${inline(paragraph.join(" "))}</p>`);
      paragraph = [];
    }
  };
  for (const line of markdown.split("\\n")) {
    const h = heading(line);
    if (h) {
      flush();
      out.push(h);
    } else if (line.trim() === "") {
      flush();
    } else {
      paragraph.push(line.trim());
    }
  }
  flush();
  return out.join("\\n");
}
'''
C.add(CONV1)
S.append(step("md5", "Whole documents: paragraphs",
  ["Now convert a whole document line by line. Consecutive text lines belong to one paragraph; a blank line or a heading ends it.",
   "Collect lines in an array and **flush** it into a `<p>` when the paragraph ends, and once more at the very end, so the last paragraph isn't lost."],
  "Write `convert(markdown)` that turns headings and paragraphs into HTML, one block per line in the output (joined with `\\n`).",
  C.text, [dict(js='convert("# Hi\\n\\nOne\\ntwo\\n\\nThree") === "<h1>Hi</h1>\\n<p>One two</p>\\n<p>Three</p>"', msg="Headings and paragraphs convert; lines in a paragraph are joined."),
           dict(js='convert("") === ""', msg="An empty document gives an empty string."), dict(js='convert("text\\n## After") === "<p>text</p>\\n<h2>After</h2>"', msg="A heading ends the paragraph before it.")]))
CONV2 = '''
function convert(markdown) {
  const out = [];
  let paragraph = [];
  let list = [];
  const flushParagraph = () => {
    if (paragraph.length) {
      out.push(`<p>${inline(paragraph.join(" "))}</p>`);
      paragraph = [];
    }
  };
  const flushList = () => {
    if (list.length) {
      out.push(`<ul>${list.map(item => `<li>${inline(item)}</li>`).join("")}</ul>`);
      list = [];
    }
  };
  for (const line of markdown.split("\\n")) {
    const h = heading(line);
    if (h) {
      flushParagraph();
      flushList();
      out.push(h);
    } else if (line.startsWith("- ")) {
      flushParagraph();
      list.push(line.slice(2));
    } else if (line.trim() === "") {
      flushParagraph();
      flushList();
    } else {
      flushList();
      paragraph.push(line.trim());
    }
  }
  flushParagraph();
  flushList();
  return out.join("\\n");
}
'''
C.sub(CONV1, CONV2)
S.append(step("md6", "Bullet lists",
  ["Lines starting with `- ` are list items. Like paragraphs, consecutive items are collected and flushed as one `<ul>` when something else begins.",
   "Now there are two kinds of block in progress, so split the flush into `flushParagraph` and `flushList` and call the right ones when the block type changes."],
  "Extend `convert` so lines starting with `- ` become `<li>` items inside a single `<ul>`, with inline formatting.",
  C.text, [dict(js='convert("- a\\n- **b**") === "<ul><li>a</li><li><strong>b</strong></li></ul>"', msg="List items become one `<ul>`."),
           dict(js='convert("Intro\\n- one\\n- two\\nOutro") === "<p>Intro</p>\\n<ul><li>one</li><li>two</li></ul>\\n<p>Outro</p>"', msg="Paragraphs before and after a list stay separate."),
           dict(js='convert("# T\\n\\nText") === "<h1>T</h1>\\n<p>Text</p>"', msg="Headings and paragraphs still work.")]))
CONV3 = CONV2.replace('''  let list = [];
''', '''  let list = [];
  let code = null;
''').replace('''  for (const line of markdown.split("\\n")) {
    const h = heading(line);''', '''  for (const line of markdown.split("\\n")) {
    if (code !== null) {
      if (line.startsWith("```")) {
        out.push(`<pre><code>${escapeHtml(code.join("\\n"))}</code></pre>`);
        code = null;
      } else {
        code.push(line);
      }
      continue;
    }
    if (line.startsWith("```")) {
      flushParagraph();
      flushList();
      code = [];
      continue;
    }
    const h = heading(line);''').replace('''  flushParagraph();
  flushList();
  return out.join("\\n");''', '''  if (code !== null) out.push(`<pre><code>${escapeHtml(code.join("\\n"))}</code></pre>`);
  flushParagraph();
  flushList();
  return out.join("\\n");''')
C.sub(CONV2, CONV3)
S.append(step("md7", "Code blocks",
  ["Fenced code blocks start and end with a line of three backticks. Everything between is shown exactly as written: no inline formatting, line breaks kept, HTML escaped.",
   "That makes the converter a tiny **state machine**: when `code` is not `null`, you're inside a block and every line is handled differently until the closing fence."],
  "Extend `convert` so text between ``` fences becomes `<pre><code>…</code></pre>`, escaped but otherwise untouched (an unclosed block runs to the end).",
  C.text, [dict(js='convert("```\\nlet x = 1 < 2;\\n**not bold**\\n```") === "<pre><code>let x = 1 &lt; 2;\\n**not bold**</code></pre>"', msg="Code blocks keep their lines and aren't formatted."),
           dict(js='convert("Before\\n```\\ncode\\n```\\nAfter") === "<p>Before</p>\\n<pre><code>code</code></pre>\\n<p>After</p>"', msg="Text around a code block stays separate."),
           dict(js='convert("```\\nopen") === "<pre><code>open</code></pre>"', msg="An unclosed block runs to the end.")]))
C.add('''
const sample = [
  "# Release notes",
  "",
  "Version **2.0** adds [dark mode](https://example.com/dark).",
  "",
  "- Faster search",
  "- New *export* button",
  "",
  "```",
  "npm install app@2",
  "```",
].join("\\n");
console.log(convert(sample));
''')
S.append(step("md8", "Convert a real document",
  ["Your converter now handles the Markdown most READMEs use. Finish by running it on a sample document and printing the HTML.",
   "Build multi-line strings from an array of lines with `.join(\"\\n\")`: it's easier to read than one long string full of `\\n`."],
  "Create a `sample` Markdown document using a heading, a paragraph with bold and a link, a list and a code block, and `console.log(convert(sample))`.",
  C.text, [dict(js='_out.includes("<h1>") && _out.includes("<ul>") && _out.includes("<pre><code>")', msg="The output contains a heading, a list and a code block."),
           dict(js='_out.includes("<a href=") && _out.includes("<strong>")', msg="The paragraph's link and bold text are converted.")]))
project(id="markdown-converter", title="Markdown to HTML Converter", lang="js", level="Intermediate", hours="2 h", hue="#fbbf24", icon="pen", art="# → <h1>",
  tagline="Write the tool behind every README: headings, lists, links, code blocks and safe escaping.",
  desc=["Markdown is how developers write: READMEs, docs, comments, chat. You'll build a converter from scratch, the way the first Markdown tools worked: escaping, inline regular expressions and a line-by-line state machine.",
        "You'll also learn why escaping user input is the most important habit in web security."],
  final="A `convert(markdown)` function that turns headings, paragraphs, bold, italics, inline code, links, bullet lists and fenced code blocks into safe HTML.",
  skills=["string processing", "regular expressions", "capture groups", "escaping (XSS prevention)", "state machines", "template literals"],
  prereq="**JavaScript from Zero**.", core=["s4m1", "s7m4"],
  stretch=["Support numbered lists (`1. item`).", "Block `javascript:` links for safety.", "Add blockquotes (`> quote`).", "Wire it to a textarea with a live preview, like a mini editor."],
  milestones=[milestone("Inline formatting", "Escape safely, then bold, italics, code and links.", S[0:3]),
              milestone("Blocks", "Headings, paragraphs, lists and code blocks.", S[3:7]), milestone("Ship it", "Convert a real document.", S[7:8])])

# =============================================================================================== LIBRARY DATABASE (SQL)
S = []
BOOKS = '''-- Library database

CREATE TABLE books (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  year INTEGER
);
INSERT INTO books VALUES
  (1, 'Dune', 'Frank Herbert', 1965),
  (2, 'Neuromancer', 'William Gibson', 1984),
  (3, 'The Left Hand of Darkness', 'Ursula K. Le Guin', 1969),
  (4, 'A Wizard of Earthsea', 'Ursula K. Le Guin', 1968),
  (5, 'Foundation', 'Isaac Asimov', 1951),
  (6, 'Kindred', 'Octavia E. Butler', 1979);
'''
MEMBERS = '''
CREATE TABLE members (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  joined TEXT NOT NULL
);
INSERT INTO members VALUES
  (1, 'Ada', '2026-01-12'),
  (2, 'Grace', '2026-03-02'),
  (3, 'Linus', '2026-05-20'),
  (4, 'Mira', '2026-08-30');
'''
LOANS = '''
CREATE TABLE loans (
  id INTEGER PRIMARY KEY,
  book_id INTEGER NOT NULL REFERENCES books(id),
  member_id INTEGER NOT NULL REFERENCES members(id),
  loaned TEXT NOT NULL,
  returned TEXT
);
INSERT INTO loans VALUES
  (1, 1, 1, '2026-08-01', '2026-08-20'),
  (2, 4, 1, '2026-09-02', NULL),
  (3, 2, 2, '2026-09-10', NULL),
  (4, 3, 2, '2026-07-15', '2026-08-01'),
  (5, 4, 3, '2026-06-01', '2026-06-20'),
  (6, 5, 3, '2026-10-01', NULL),
  (7, 3, 1, '2026-10-05', NULL);
'''
ON_LOAN = '''SELECT books.title, members.name
FROM loans
JOIN books ON books.id = loans.book_id
JOIN members ON members.id = loans.member_id
WHERE loans.returned IS NULL'''
S.append(step("lb1", "Design the books table",
  ["A database starts with its **schema**: which tables exist and what each column holds. `CREATE TABLE` declares a table; each column gets a type (`INTEGER`, `TEXT`).",
   "`PRIMARY KEY` gives every row a unique id. `NOT NULL` makes a column required, so the database refuses incomplete rows."],
  "Create a `books` table (`id` primary key, `title` and `author` required text, `year` integer) and insert the six books listed in the hint: Dune, Neuromancer, The Left Hand of Darkness, A Wizard of Earthsea, Foundation and Kindred, with ids 1–6. End with `SELECT * FROM books;`",
  BOOKS + "\nSELECT * FROM books;\n", [dict(src="CREATE TABLE books", msg="You create the `books` table."), dict(rows=True, ordered=True, msg="All six books are stored with the right columns.")],
  hint="Dune (Frank Herbert, 1965), Neuromancer (William Gibson, 1984), The Left Hand of Darkness (Ursula K. Le Guin, 1969), A Wizard of Earthsea (Ursula K. Le Guin, 1968), Foundation (Isaac Asimov, 1951), Kindred (Octavia E. Butler, 1979).",
  starter="-- Library database\n", core="s4m4", ref=("SQLite: CREATE TABLE", "https://www.sqlite.org/lang_createtable.html")))
S.append(step("lb2", "Members",
  ["People are a different kind of thing from books, so they get their own table. Keeping each fact in exactly one place is called **normalisation**: change a member's name once and it's right everywhere.",
   "Dates are stored as ISO text (`2026-01-12`), which sorts correctly as plain text."],
  "Create a `members` table (`id`, `name`, `joined`) with Ada (2026-01-12), Grace (2026-03-02), Linus (2026-05-20) and Mira (2026-08-30), ids 1–4. Replace the final query with `SELECT * FROM members;`",
  BOOKS + MEMBERS + "\nSELECT * FROM members;\n", [dict(src="CREATE TABLE members", msg="You create the `members` table."), dict(rows=True, ordered=True, msg="The four members are stored.")]))
S.append(step("lb3", "Loans connect them",
  ["A loan links a book to a member on a date. Instead of copying titles and names, store their ids: `book_id INTEGER REFERENCES books(id)`. That's a **foreign key**.",
   "`returned` is `NULL` while the book is still out. `NULL` means *unknown or missing*, which is exactly right here."],
  "Create a `loans` table (`id`, `book_id` and `member_id` as foreign keys, `loaned`, `returned`) and insert the seven loans from the hint. Finish with `SELECT COUNT(*) FROM loans;`",
  BOOKS + MEMBERS + LOANS + "\nSELECT COUNT(*) FROM loans;\n", [dict(src="REFERENCES books", msg="`book_id` references `books`."), dict(src="REFERENCES members", msg="`member_id` references `members`."), dict(rows=True, msg="There are 7 loans.")],
  hint="(id, book_id, member_id, loaned, returned): (1,1,1,'2026-08-01','2026-08-20'), (2,4,1,'2026-09-02',NULL), (3,2,2,'2026-09-10',NULL), (4,3,2,'2026-07-15','2026-08-01'), (5,4,3,'2026-06-01','2026-06-20'), (6,5,3,'2026-10-01',NULL), (7,3,1,'2026-10-05',NULL)."))
BASE = BOOKS + MEMBERS + LOANS
S.append(step("lb4", "What's on loan right now?",
  ["To answer questions that span tables, **JOIN** them on their keys: each loan row is paired with its book row (`books.id = loans.book_id`) and its member row.",
   "`IS NULL` (not `= NULL`) finds missing values: `NULL = NULL` is never true in SQL."],
  "Replace the final query: list the `title` and member `name` for every loan that hasn't been returned, ordered by title.",
  BASE + "\n" + ON_LOAN + "\nORDER BY books.title;\n", [dict(src="JOIN", msg="You join the tables."), dict(src="IS NULL", msg="You use `IS NULL`."), dict(rows=True, ordered=True, msg="Exactly the four books on loan are listed, by title.")], core="s4m4"))
S.append(step("lb5", "Overdue books",
  ["Add conditions with `AND`. Because ISO dates sort as text, `loans.loaned < '2026-09-15'` means *loaned before 15 September*.",
   "Real systems compute this from today's date (`date('now', '-30 days')` in SQLite); a fixed date keeps the result predictable here."],
  "List the `title`, member `name` and `loaned` date of books still out that were loaned before `2026-09-15`, oldest first.",
  BASE + "\nSELECT books.title, members.name, loans.loaned\nFROM loans\nJOIN books ON books.id = loans.book_id\nJOIN members ON members.id = loans.member_id\nWHERE loans.returned IS NULL AND loans.loaned < '2026-09-15'\nORDER BY loans.loaned;\n",
  [dict(rows=True, ordered=True, msg="The two overdue loans are listed, oldest first.")]))
S.append(step("lb6", "Loans per member, including nobody",
  ["`JOIN` only keeps rows that match on both sides, so a member with no loans vanishes. `LEFT JOIN` keeps every row from the left table and fills the gaps with `NULL`.",
   "`COUNT(loans.id)` counts only non-null ids, so members with no loans correctly get 0, where `COUNT(*)` would wrongly give 1."],
  "List every member's `name` and their number of loans as `loans`, including members with none, most loans first and then by name.",
  BASE + "\nSELECT members.name, COUNT(loans.id) AS loans\nFROM members\nLEFT JOIN loans ON loans.member_id = members.id\nGROUP BY members.id\nORDER BY loans DESC, members.name;\n",
  [dict(src="LEFT JOIN", msg="You use `LEFT JOIN`."), dict(rows=True, ordered=True, msg="All four members appear, Mira with 0.")]))
S.append(step("lb7", "The most borrowed author",
  ["Group by author and count the loans of all their books together. `ORDER BY loans DESC LIMIT 1` keeps only the winner."],
  "Find the author whose books have been borrowed most: return `author` and the count as `loans`, one row.",
  BASE + "\nSELECT books.author, COUNT(*) AS loans\nFROM loans\nJOIN books ON books.id = loans.book_id\nGROUP BY books.author\nORDER BY loans DESC\nLIMIT 1;\n",
  [dict(src="GROUP BY", msg="You group by author."), dict(rows=True, msg="Ursula K. Le Guin, with 4 loans.")]))
S.append(step("lb8", "Save the question as a view",
  ["A **view** is a saved query you can select from like a table. Name the questions your library asks every day and the front desk never writes that join again.",
   "Views store the query, not the data, so they're always up to date."],
  "Create a view `on_loan` from your step-4 query (without the ORDER BY), then finish with `SELECT * FROM on_loan ORDER BY title;`",
  BASE + "\nCREATE VIEW on_loan AS\n" + ON_LOAN + ";\n\nSELECT * FROM on_loan ORDER BY title;\n",
  [dict(src="CREATE VIEW on_loan", msg="You create the `on_loan` view."), dict(rows=True, ordered=True, msg="Selecting from the view lists the four books on loan.")],
  ref=("SQLite: CREATE VIEW", "https://www.sqlite.org/lang_createview.html")))
project(id="library-database", title="Library Database", lang="sql", level="Intermediate", hours="1.5 h", hue="#a3e635", icon="db", art="⋈ JOIN",
  tagline="Design a real schema and answer the questions a library asks every day.",
  desc=["Most apps are a database with a user interface on top. Here you'll design one from scratch: tables, keys and relationships, then the queries that run the front desk.",
        "You'll practise the SQL that interviews and real jobs lean on most: joins, `NULL` handling, `LEFT JOIN`, grouping and views."],
  final="A three-table library database (books, members, loans) with queries for what's on loan, what's overdue, who borrows most and the most popular author, plus a reusable view.",
  skills=["schema design", "primary and foreign keys", "INSERT", "JOIN", "NULL and IS NULL", "LEFT JOIN", "GROUP BY", "views"],
  prereq="the **SQL from Zero** bootcamp course.", core=["s4m4", "s6m2"],
  stretch=["Add a `fines` query: 10 cents per day overdue.", "Add an index on `loans(member_id)` and compare query plans with `EXPLAIN QUERY PLAN`.", "Prevent lending a book that's already out (a trigger or a unique partial index)."],
  milestones=[milestone("The schema", "Tables, keys and relationships.", S[0:3]), milestone("Front-desk questions", "Joins, NULLs and dates.", S[3:5]),
              milestone("Reports", "Counting, ranking and saved views.", S[5:8])])

# =============================================================================================== EXPENSE TRACKER (web)
P = Page("Expense Tracker")
S = []
BLANK = P.render()
def add_exp(desc, amount, cat="Food"):
    return f"_type('#desc', {desc!r}); _type('#amount', {amount!r}); $('#category').value = {cat!r}; _submit('#expense-form');"
P.css = ['    [hidden] { display: none !important; }']
P.body = ['  <main class="tracker">', '    <h1>Expenses</h1>', '    <form id="expense-form">', '      <input id="desc" placeholder="What was it?">', '      <input id="amount" type="number" step="0.01" min="0" placeholder="Amount">',
          '      <select id="category">', '        <option>Food</option>', '        <option>Transport</option>', '        <option>Fun</option>', '        <option>Bills</option>', '      </select>', '      <button>Add</button>', '    </form>',
          '    <p id="error" hidden></p>', '    <table id="expenses">', '      <thead><tr><th>What</th><th>Category</th><th>Amount</th><th></th></tr></thead>', '      <tbody></tbody>', '    </table>', '    <p id="total">Total: $0.00</p>', '  </main>']
S.append(step("ex1", "A form and a table",
  ["Tabular data belongs in a `<table>`: a header row in `<thead>`, one row per expense in `<tbody>`. Screen readers announce tables properly, which a pile of `<div>`s can't do.",
   "`<input type=\"number\" step=\"0.01\">` gives a numeric keypad on phones and allows cents. A `<select>` limits categories to a fixed list."],
  "Build `form#expense-form` with `#desc`, a number input `#amount`, a `select#category` (Food, Transport, Fun, Bills) and an Add button; a hidden `p#error`; a `table#expenses` with a header row and an empty `tbody`; and `<p id=\"total\">Total: $0.00</p>`.",
  P.render(), [dict(js="!!$('#expense-form #desc') && $('#expense-form #amount').type==='number'", msg="The form has `#desc` and a number `#amount`."),
               dict(js="$$('#category option').map(o=>o.textContent).join()==='Food,Transport,Fun,Bills'", msg="The categories are Food, Transport, Fun and Bills."),
               dict(js="!!$('#expenses thead tr') && !!$('#expenses tbody')", msg="The table has a header and a body."), dict(js="_text('#total')==='Total: $0.00' && $('#error').hidden", msg="Total starts at $0.00 and the error is hidden.")],
  starter=BLANK, ref=("MDN: The table element", "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/table")))
P.css += ['    body { font-family: system-ui, sans-serif; background: #f5f6fb; margin: 0; padding: 32px 16px; color: #0e1330; }',
          '    .tracker { max-width: 640px; margin: 0 auto; background: white; padding: 24px; border-radius: 16px; }',
          '    #expense-form { display: grid; grid-template-columns: 2fr 1fr 1fr auto; gap: 8px; }',
          '    input, select, button { font: inherit; padding: 9px 10px; border: 1px solid #d0d4e8; border-radius: 8px; }',
          '    button { background: #5b45f0; color: white; border: 0; cursor: pointer; }',
          '    table { width: 100%; border-collapse: collapse; margin-top: 16px; }',
          '    th, td { text-align: left; padding: 8px; border-bottom: 1px solid #eceef6; }',
          '    td:nth-child(3), th:nth-child(3) { text-align: right; font-variant-numeric: tabular-nums; }',
          '    #error { color: #c62828; }',
          '    #total { font-weight: 700; text-align: right; }']
S.append(step("ex2", "Lay it out",
  ["A grid with uneven columns, `grid-template-columns: 2fr 1fr 1fr auto`, gives the description more room than the amount and category.",
   "Right-align money columns and use `font-variant-numeric: tabular-nums` so digits line up. `border-collapse: collapse` makes table borders single lines."],
  "Style the tracker: make `#expense-form` a grid with four columns, give the table full width with collapsed borders, and right-align the amount column.",
  P.render(), [dict(js="getComputedStyle($('#expense-form')).display==='grid' && getComputedStyle($('#expense-form')).gridTemplateColumns.split(' ').length===4", msg="The form is a four-column grid."),
               dict(js="getComputedStyle($('table')).borderCollapse==='collapse'", msg="Table borders are collapsed."),
               dict(js="getComputedStyle($('th:nth-child(3)')).textAlign==='right'", msg="The amount column is right-aligned.")]))
P.js = ['    const form = document.querySelector("#expense-form");', '    const tbody = document.querySelector("#expenses tbody");', '    let expenses = [];', '',
        '    function money(n) {', '      return "$" + n.toFixed(2);', '    }', '',
        '    function render() {', '      tbody.innerHTML = "";', '      for (const e of expenses) {', '        const row = document.createElement("tr");',
        '        for (const value of [e.desc, e.category, money(e.amount)]) {', '          const cell = document.createElement("td");', '          cell.textContent = value;', '          row.append(cell);', '        }', '        tbody.append(row);', '      }', '    }', '',
        '    form.addEventListener("submit", (event) => {', '      event.preventDefault();', '      expenses.push({', '        id: Date.now() + Math.random(),', '        desc: document.querySelector("#desc").value.trim(),',
        '        amount: Number(document.querySelector("#amount").value),', '        category: document.querySelector("#category").value,', '      });', '      form.reset();', '      render();', '    });']
S.append(step("ex3", "Add expenses",
  ["Same pattern as every app: state (`expenses`), a `render()` that draws it, and an event handler that changes the state then re-renders.",
   "Input values are always strings: `Number(\"12.5\")` gives `12.5`. Format money in one place, `money(n)`, using `toFixed(2)` so `12.5` shows as `$12.50`. `form.reset()` clears every field at once."],
  "Keep an `expenses` array. On submit, push `{ id, desc, amount, category }` (amount as a number), reset the form and render one table row per expense showing description, category and the amount formatted as `$12.50`.",
  P.render(), [dict(js="$$('#expenses tbody tr').length===1 && $$('#expenses tbody td').slice(0,3).map(td=>td.textContent).join('|')==='Lunch|Food|$12.50'", msg="Adding an expense shows a row: description, category and `$12.50`.", do=add_exp("Lunch", "12.5")),
               dict(js="expenses.length===2 && typeof expenses[1].amount==='number' && expenses[1].category==='Transport'", msg="Expenses are stored with numeric amounts.", do=add_exp("Lunch", "12.5") + add_exp("Bus", "2.8", "Transport")),
               dict(js="$('#desc').value===''", msg="The form is cleared after adding.", do=add_exp("Lunch", "12.5"))], core="s4m1"))
P.sub_js('''    form.addEventListener("submit", (event) => {
      event.preventDefault();
      expenses.push({
        id: Date.now() + Math.random(),
        desc: document.querySelector("#desc").value.trim(),
        amount: Number(document.querySelector("#amount").value),
        category: document.querySelector("#category").value,
      });''', '''    const error = document.querySelector("#error");

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const desc = document.querySelector("#desc").value.trim();
      const amount = Number(document.querySelector("#amount").value);
      if (desc === "" || !(amount > 0)) {
        error.textContent = "Enter a description and an amount above 0.";
        error.hidden = false;
        return;
      }
      error.hidden = true;
      expenses.push({
        id: Date.now() + Math.random(),
        desc: desc,
        amount: amount,
        category: document.querySelector("#category").value,
      });''')
S.append(step("ex4", "Validate input",
  ["Never trust input. An empty description, a missing amount, `0` or a negative number should be refused with a clear message, not stored.",
   "`!(amount > 0)` also catches `NaN` (what `Number(\"\")` gives for an empty field), because every comparison with `NaN` is false."],
  "Before adding, check that the description isn't empty and the amount is above 0. If not, show `Enter a description and an amount above 0.` in `#error` and don't add anything. Hide the error after a valid add.",
  P.render(), [dict(js="expenses.length===0 && !$('#error').hidden && _text('#error')==='Enter a description and an amount above 0.'", msg="An empty description is refused with the message.", do=add_exp("", "5")),
               dict(js="expenses.length===0", msg="Zero, negative and missing amounts are refused.", do=add_exp("A", "0") + add_exp("B", "-3") + add_exp("C", "")),
               dict(js="expenses.length===1 && $('#error').hidden", msg="A valid expense after an error hides the error.", do=add_exp("", "5") + add_exp("Tea", "3"))]))
P.sub_js('''        tbody.append(row);
      }
    }''', '''        tbody.append(row);
      }
      const total = expenses.reduce((sum, e) => sum + e.amount, 0);
      document.querySelector("#total").textContent = "Total: " + money(total);
    }''')
S.append(step("ex5", "The running total",
  ["The total is derived from the array, so compute it in `render()` with `reduce`: start at 0 and add each expense's amount.",
   "Computed values never go stale. If you stored the total separately, every add and delete would have to remember to update it too."],
  "In `render()`, set `#total` to `Total: ` plus the formatted sum of all amounts.",
  P.render(), [dict(js="_text('#total')==='Total: $15.30'", msg="12.50 + 2.80 shows `Total: $15.30`.", do=add_exp("Lunch", "12.5") + add_exp("Bus", "2.8", "Transport")),
               dict(js="_text('#total')==='Total: $0.30'", msg="Floating-point sums are formatted correctly: 0.10 + 0.20 shows $0.30.", do=add_exp("A", "0.1") + add_exp("B", "0.2"))],
  ref=("MDN: Array.prototype.reduce", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce")))
P.sub_js('''          row.append(cell);
        }
        tbody.append(row);''', '''          row.append(cell);
        }
        const actions = document.createElement("td");
        const del = document.createElement("button");
        del.className = "delete";
        del.textContent = "Delete";
        del.addEventListener("click", () => {
          expenses = expenses.filter(x => x.id !== e.id);
          render();
        });
        actions.append(del);
        row.append(actions);
        tbody.append(row);''')
S.append(step("ex6", "Delete an expense",
  ["Each row gets a Delete button. The click handler, created inside the loop, remembers its own expense `e`: that's a closure again.",
   "Delete by filtering the array, then re-render. The total updates by itself because it's computed in `render()`."],
  "Add a `button.delete` in a fourth cell of each row that removes that expense.",
  P.render(), [dict(js="expenses.length===1 && _text('#expenses tbody td')==='Bus' && _text('#total')==='Total: $2.80'", msg="Deleting the first row removes it and updates the total.", do=add_exp("Lunch", "12.5") + add_exp("Bus", "2.8", "Transport") + "_click('#expenses tbody .delete');")]))
P.sub_body('    <p id="total">Total: $0.00</p>', '    <p id="total">Total: $0.00</p>\n    <h2>By category</h2>\n    <ul id="summary"></ul>')
P.sub_js('''      document.querySelector("#total").textContent = "Total: " + money(total);''', '''      document.querySelector("#total").textContent = "Total: " + money(total);
      const byCategory = {};
      for (const e of expenses) byCategory[e.category] = (byCategory[e.category] || 0) + e.amount;
      const summary = document.querySelector("#summary");
      summary.innerHTML = "";
      Object.entries(byCategory)
        .sort((a, b) => b[1] - a[1])
        .forEach(([category, amount]) => {
          const li = document.createElement("li");
          li.textContent = `${category}: ${money(amount)}`;
          summary.append(li);
        });''')
S.append(step("ex7", "Spending by category",
  ["Grouping is a dictionary job: an object whose keys are categories and values are running totals. `(byCategory[c] || 0) + amount` starts each category at 0.",
   "`Object.entries(obj)` turns it into `[key, value]` pairs you can sort, here biggest spend first."],
  "Add `<h2>By category</h2>` and `ul#summary`. In `render()`, fill it with one `li` per category that has spending, formatted `Food: $20.00`, sorted from the largest amount.",
  P.render(), [dict(js="$$('#summary li').map(li=>li.textContent).join('|')==='Food: $20.00|Transport: $2.80'", msg="Categories are totalled and sorted largest first.", do=add_exp("Lunch", "12.5") + add_exp("Bus", "2.8", "Transport") + add_exp("Dinner", "7.5")),
               dict(js="$$('#summary li').length===0", msg="With no expenses the summary is empty.")]))
SEED = {"expenses": '[{"id":1,"desc":"Rent","amount":800,"category":"Bills"},{"id":2,"desc":"Cinema","amount":12,"category":"Fun"}]'}
P.sub_js('    let expenses = [];', '    let expenses = JSON.parse(localStorage.getItem("expenses")) || [];')
P.sub_js('    function render() {\n      tbody.innerHTML = "";', '    function render() {\n      localStorage.setItem("expenses", JSON.stringify(expenses));\n      tbody.innerHTML = "";')
P.js += ['', '    render();']
S.append(step("ex8", "Remember everything",
  ["Save on every render and load on start, the same two-line pattern as the To-Do app. Then call `render()` once at load so saved expenses appear immediately.",
   "Your tracker is done: data in, validated, summarised and persisted."],
  "Save `expenses` to localStorage under `\"expenses\"` at the start of `render()`, load them when the page starts (falling back to `[]`) and call `render()` once on load.",
  P.render(), [dict(js="$$('#expenses tbody tr').length===2 && _text('#total')==='Total: $812.00'", msg="Saved expenses and their total appear on load.", storage=SEED),
               dict(js="JSON.parse(localStorage.getItem('expenses')).length===1", msg="New expenses are saved.", do=add_exp("Tea", "3"), storage={}),
               dict(js="_text('#summary li')==='Bills: $800.00'", msg="The category summary includes saved expenses.", storage=SEED)], storage=SEED))
project(id="expense-tracker", title="Expense Tracker", lang="web", level="Intermediate", hours="2 h", hue="#34d399", icon="bars", art="$ 12.50",
  tagline="Track spending with validation, totals, category breakdowns and saved data.",
  desc=["A practical app you can actually use: log what you spend, see where the money goes, and keep it between visits.",
        "It drills the patterns behind every business app: forms with validation, tables, derived totals, grouping data and persistence."],
  final="An expense tracker with a validated form, a table of expenses with delete buttons, a live total, a by-category breakdown sorted by spend, and everything saved in the browser.",
  skills=["forms and validation", "tables", "number handling", "reduce", "grouping with objects", "closures", "localStorage"],
  prereq="the **To-Do List App** project, or **JavaScript from Zero**.", core=["s4m1", "s1m4"],
  stretch=["Filter the table by category or month.", "Draw the category breakdown as a bar chart with plain `<div>`s or SVG.", "Export to CSV with a download link.", "Set a monthly budget and warn when you pass it."],
  milestones=[milestone("The interface", "A form and a table, laid out cleanly.", S[0:2]), milestone("Recording spending", "Add, validate and total expenses.", S[2:5]),
              milestone("Insight and memory", "Delete, summarise by category and save.", S[5:8])])
