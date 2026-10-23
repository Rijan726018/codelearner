import random
from _lib import *

LETTERS = list("etaoinsrhldcumfpgwybvkxjqz")

# =============================================================================================== HANGMAN (Python)
S = []
HEAD = 'import random\n\nWORDS = ["python", "variable", "function", "keyboard", "browser", "library", "compiler", "network"]\n'
F_MASK = 'def masked(word, guessed):\n    return " ".join(c if c in guessed else "_" for c in word)\n'
F_SOLVED = 'def is_solved(word, guessed):\n    return all(c in guessed for c in word)\n'
def hprog(funcs, main):
    return HEAD + "".join("\n\n" + f for f in funcs) + "\n\n" + main

INTRO = 'secret = random.choice(WORDS)\nprint(f"Guess the word: {len(secret)} letters.")\n'
hv1 = hprog([], INTRO)
S.append(step("hm1", "Pick a secret word",
  ["Hangman needs a word the player can't see. Keep the possible words in a **list**, and let `random.choice(WORDS)` pick one at random.",
   "Constants that never change, like the word list, are written in `UPPER_CASE` by convention, so readers know not to modify them."],
  "Import `random`, make a list `WORDS` with at least five words, choose one into `secret`, and print `Guess the word: N letters.`",
  hv1, [dict(src="random\\.choice", msg="You use `random.choice`."), dict(py="len(WORDS) >= 5 and secret in WORDS", msg="`secret` is one of at least five `WORDS`."),
        dict(outRe="Guess the word: \\d+ letters\\.", msg="It prints how many letters the word has.")],
  starter="# Hangman\n", core="s1m4", ref=("Python docs: random.choice", "https://docs.python.org/3/library/random.html#random.choice")))
hv2 = hprog([F_MASK], INTRO + 'print(masked(secret, set()))\n')
S.append(step("hm2", "Show the hidden word",
  ["The player sees blanks for letters they haven't found: `p _ _ _ o _`. Build that with a **generator expression** inside `join`: for each character, show it if it's been guessed, otherwise `_`.",
   "Use a **set** for the guessed letters: checking `c in guessed` is instant, and a letter can't be in it twice."],
  "Write `masked(word, guessed)` that returns the word with unguessed letters as `_`, separated by spaces. Print the masked secret with an empty set.",
  hv2, [dict(py='masked("python", {"p", "o"}) == "p _ _ _ o _"', msg='`masked("python", {"p", "o"})` is `p _ _ _ o _`.'),
        dict(py='masked("aa", set()) == "_ _" and masked("ab", {"a", "b"}) == "a b"', msg="All hidden and all found both work."), dict(outRe="^_( _)+$", msg="It prints the hidden word as blanks.")],
  example='" ".join(["a", "b", "c"])   # "a b c"', core="s1m4"))
hv3 = hprog([F_MASK, F_SOLVED], INTRO + 'print(masked(secret, set()))\n')
S.append(step("hm3", "Has the player won?",
  ["The word is solved when **every** letter is in the guessed set. `all(...)` returns `True` only if every item is true, and stops at the first false one."],
  "Write `is_solved(word, guessed)` using `all`.",
  hv3, [dict(py='is_solved("abba", {"a", "b"}) and not is_solved("abc", {"a", "b"})', msg="It's true only when every letter is guessed."),
        dict(py='is_solved("hi", {"h", "i", "z"})', msg="Extra wrong letters don't matter."), dict(src="all\\(", msg="You use `all`.")], core="s1m3"))
LOOP = ('secret = random.choice(WORDS)\nprint(f"Guess the word: {len(secret)} letters.")\nguessed = set()\nlives = 6\nprint(masked(secret, guessed))\n'
        'while lives > 0 and not is_solved(secret, guessed):\n    letter = input("Letter: ").strip().lower()\n    guessed.add(letter)\n'
        '    if letter not in secret:\n        lives -= 1\n        print(f"No {letter}. Lives left: {lives}")\n    print(masked(secret, guessed))\n'
        'if is_solved(secret, guessed):\n    print(f"You won. The word was {secret}.")\nelse:\n    print(f"Out of lives. The word was {secret}.")\n')
hv4 = hprog([F_MASK, F_SOLVED], LOOP)
WRONG = "lives == 6 - len([c for c in guessed if c not in secret])"
S.append(step("hm4", "The game loop",
  ["The game repeats while the player still has lives **and** hasn't solved the word. Each round: read a letter, add it to `guessed`, take a life if it's not in the word, and show the word again.",
   "After the loop, check *why* it ended to print the right message.",
   "The checks type letters into the **Input** box for you: one per line, in the order e, t, a, o, i, n…"],
  "Start with `guessed = set()` and `lives = 6`. Loop while lives remain and the word isn't solved, reading a letter with `input`. Wrong letters cost a life. End with `You won. The word was X.` or `Out of lives. The word was X.`",
  hv4, [dict(outHas="The word was", msg="The game ends with a message naming the word."), dict(py=WRONG, msg="Each wrong letter costs exactly one life."),
        dict(py="is_solved(secret, guessed) or lives == 0", msg="The loop stops when the word is solved or lives run out."), dict(src="while ", msg="You use a `while` loop.")],
  stdin=LETTERS, core="s1m2"))
LOOP5 = LOOP.replace('    guessed.add(letter)\n', '    if len(letter) != 1 or not letter.isalpha():\n        print("Type one letter.")\n        continue\n    if letter in guessed:\n        print("You already tried that.")\n        continue\n    guessed.add(letter)\n')
hv5 = hprog([F_MASK, F_SOLVED], LOOP5)
S.append(step("hm5", "Be kind to typos",
  ["Right now `ab`, `7` or an empty line counts as a guess, and guessing `e` twice costs two lives. A good game checks input first.",
   "`str.isalpha()` is `True` only for letters. `continue` skips the rest of this round and asks again, without touching `lives`."],
  "Before adding a guess, reject anything that isn't exactly one letter (print `Type one letter.`) and letters already tried (print `You already tried that.`). Neither costs a life.",
  hv5, [dict(outHas="Type one letter.", msg="`ab` and `1` print `Type one letter.`"), dict(outHas="You already tried that.", msg="A repeated letter prints `You already tried that.`"),
        dict(py=WRONG + ' and "ab" not in guessed and "1" not in guessed', msg="Rejected input never costs a life or enters `guessed`.")],
  stdin=["ab", "1", "", "e", "e"] + LETTERS, ref=("Python docs: str.isalpha", "https://docs.python.org/3/library/stdtypes.html#str.isalpha")))
LOOP6 = (LOOP5.replace('guessed = set()\nlives = 6\n', 'guessed = set()\nwrong = []\nlives = 6\n')
         .replace('        lives -= 1\n        print(f"No {letter}. Lives left: {lives}")\n    print(masked(secret, guessed))\n',
                  '        lives -= 1\n        wrong.append(letter)\n        print(f"No {letter}.")\n    print(masked(secret, guessed))\n    print(f"Lives: {lives}   Wrong: {\' \'.join(wrong)}")\n'))
hv6 = hprog([F_MASK, F_SOLVED], LOOP6)
S.append(step("hm6", "Show what went wrong",
  ["Players want to see the letters they've already missed. Keep them in a **list** called `wrong`, in the order they were guessed, and print a status line after every guess.",
   "`' '.join(wrong)` turns `['z', 'q']` into `z q`. An empty list joins to an empty string."],
  "Add `wrong = []`. Append each wrong letter to it, and after every guess print `Lives: N   Wrong: x y z` (three spaces before Wrong).",
  hv6, [dict(py="set(wrong) == {c for c in guessed if c not in secret} and lives == 6 - len(wrong)", msg="`wrong` holds exactly the wrong letters."),
        dict(outRe="Lives: \\d   Wrong: ", msg="A status line shows lives and wrong letters."), dict(py="len(wrong) == len(set(wrong))", msg="No wrong letter is listed twice.")],
  stdin=LETTERS))
PLAY = ('def play(secret):\n    guessed = set()\n    wrong = []\n    lives = 6\n    print(f"Guess the word: {len(secret)} letters.")\n    print(masked(secret, guessed))\n'
        '    while lives > 0 and not is_solved(secret, guessed):\n        letter = input("Letter: ").strip().lower()\n'
        '        if len(letter) != 1 or not letter.isalpha():\n            print("Type one letter.")\n            continue\n'
        '        if letter in guessed:\n            print("You already tried that.")\n            continue\n        guessed.add(letter)\n'
        '        if letter not in secret:\n            lives -= 1\n            wrong.append(letter)\n            print(f"No {letter}.")\n'
        '        print(masked(secret, guessed))\n        print(f"Lives: {lives}   Wrong: {\' \'.join(wrong)}")\n'
        '    if is_solved(secret, guessed):\n        print(f"You won. The word was {secret}.")\n        return True\n'
        '    print(f"Out of lives. The word was {secret}.")\n    return False\n')
MAIN7 = ('wins = 0\nrounds = 0\nwhile True:\n    rounds += 1\n    if play(random.choice(WORDS)):\n        wins += 1\n    print(f"Wins: {wins} of {rounds}")\n'
         '    again = input("Play again? (y/n) ")\n    if again.strip().lower() != "y":\n        break\nprint("Thanks for playing.")\n')
hv7 = hprog([F_MASK, F_SOLVED, PLAY], MAIN7)
S.append(step("hm7", "Rounds and a score",
  ["Move one round into `play(secret)`, which **returns** `True` for a win and `False` for a loss. Then the main loop can play as many rounds as the player wants and keep score.",
   "Returning a result instead of printing it is what makes a function reusable: the caller decides what to do with it."],
  "Write `play(secret)` that runs one round and returns whether the player won. Loop rounds, counting `wins` and `rounds`, print `Wins: W of R` after each, and ask `Play again? (y/n)`. Finish with `Thanks for playing.`",
  hv7, [dict(py="callable(play) and rounds >= 1 and 0 <= wins <= rounds", msg="`play` exists and `wins`/`rounds` are counted."), dict(outRe="Wins: \\d+ of \\d+", msg="It prints the score after each round."),
        dict(outHas="Thanks for playing.", msg="It says goodbye at the end."), dict(src="return True", msg="`play` returns `True` for a win.")],
  stdin=LETTERS + ["n"], core="s1m3"))

def hangman_demo(seed):
    """A sample run by a player who knows the word: a typo, a repeat and one miss, then the right letters."""
    word = random.Random(seed).choice(["python", "variable", "function", "keyboard", "browser", "library", "compiler", "network"])
    feed = ["e", "ab", "e", "z"] if "e" in word else ["a", "ab", "a", "z"]
    for c in word:
        if c not in feed:
            feed.append(c)
    return feed + ["n"]
project(id="hangman", title="Hangman", lang="python", level="Beginner", hours="1 h", hue="#f472b6", icon="key", art="p _ t h _ n",
  tagline="The classic word game: lists, sets, loops and input handling that survives any typo.",
  desc=["Hangman is small enough to finish in an hour and rich enough to teach the core of Python: picking from a list, sets for fast lookups, `while` loops with two conditions, and validating what people type.",
        "You'll finish by refactoring the game into a function that returns a result, which is how real programs are built."],
  final="A replayable command-line Hangman with a hidden word, six lives, a list of wrong guesses, typo-proof input and a running score.",
  skills=["lists", "sets", "random.choice", "generator expressions", "all()", "while loops", "input validation", "functions that return results"],
  prereq="the first half of **Python from Zero**.", core=["s1m2", "s1m3", "s1m4"],
  stretch=["Draw the gallows in ASCII art, one piece per lost life.", "Pick words by difficulty (length) chosen at the start.", "Load words from a text file with `open()`.", "Give a hint (reveal one letter) at the cost of a life."],
  demo_pre="import random\nrandom.seed(4)\n", demo_stdin=hangman_demo(4),
  milestones=[milestone("The word", "A secret word, shown as blanks.", S[0:3]), milestone("The game", "Guess letters until you win or run out of lives.", S[3:6]),
              milestone("Replay", "A function per round, and a score.", S[6:7])])

# =============================================================================================== TEXT ANALYZER (Python)
S = []
TEXT_HEAD = '''import string

TEXT = """Coding is a craft. You learn it by writing code, reading code and fixing code.
The best way to learn is to build small things, then bigger things.
Every bug you fix teaches you something. Every project you finish makes the next one easier.
So write a little code every day, and be patient with yourself."""
'''
F_WORDS = 'def words(text):\n    result = []\n    for raw in text.split():\n        word = raw.strip(string.punctuation).lower()\n        if word:\n            result.append(word)\n    return result\n'
F_FREQ = 'def frequencies(text):\n    counts = {}\n    for word in words(text):\n        counts[word] = counts.get(word, 0) + 1\n    return counts\n'
F_TOP = 'def top_words(text, n):\n    counts = frequencies(text)\n    ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))\n    return ranked[:n]\n'
F_TOP2 = 'def top_words(text, n, skip=()):\n    counts = {w: c for w, c in frequencies(text).items() if w not in skip}\n    ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))\n    return ranked[:n]\n'
STOP = 'STOP = {"a", "an", "and", "the", "is", "it", "to", "of", "in", "by", "be", "so", "then", "with", "you", "your", "yourself"}\n'
F_SENT = 'def sentence_count(text):\n    pieces = re.split(r"[.!?]+", text)\n    return len([p for p in pieces if p.strip()])\n'
F_READ = 'def reading_minutes(text, wpm=200):\n    return max(1, math.ceil(len(words(text)) / wpm))\n'
F_BAR = 'def bar_chart(pairs):\n    width = max(len(word) for word, count in pairs)\n    lines = [f"{word.ljust(width)} {\'#\' * count} {count}" for word, count in pairs]\n    return "\\n".join(lines)\n'
F_REPORT = ('def report(text):\n    lines = [\n        f"Words: {len(words(text))}",\n        f"Different words: {len(frequencies(text))}",\n        f"Sentences: {sentence_count(text)}",\n'
            '        f"Reading time: {reading_minutes(text)} min",\n        "Top words:",\n        bar_chart(top_words(text, 5, skip=STOP)),\n    ]\n    return "\\n".join(lines)\n')
def tprog(funcs, main, head=TEXT_HEAD):
    return head + "".join("\n\n" + f for f in funcs) + "\n\n" + main
S.append(step("wf1", "Split text into words",
  ["Text analysis starts by turning a string into a list of **words**. `text.split()` splits on any whitespace, but leaves punctuation attached: `\"code,\"` is not the same as `\"code\"`.",
   "`word.strip(string.punctuation)` removes punctuation from both ends, and `.lower()` makes `Every` and `every` the same word. Skip anything that becomes empty."],
  "Below `TEXT`, write `words(text)` that returns the lowercase words without surrounding punctuation. Print how many words `TEXT` has.",
  tprog([F_WORDS], 'print(len(words(TEXT)), "words")\n'),
  [dict(py='words("Hello, world! Hello.") == ["hello", "world", "hello"]', msg="Punctuation is stripped and words are lowercase."), dict(py='words("  --  ") == []', msg="Punctuation-only pieces are skipped."),
   dict(py='words("Don\'t stop") == ["don\'t", "stop"]', msg="Apostrophes inside words are kept."), dict(outHas="56 words", msg="It prints `56 words`.")],
  starter=TEXT_HEAD, core="s1m4", ref=("Python docs: str.strip", "https://docs.python.org/3/library/stdtypes.html#str.strip")))
S.append(step("wf2", "Count every word",
  ["A **dictionary** from word to count is the classic way to count things: look the word up with `counts.get(word, 0)` (0 if it's new) and add one.",
   "The number of keys is the number of *different* words."],
  "Write `frequencies(text)` returning a dict of word counts. Print how many different words `TEXT` has.",
  tprog([F_WORDS, F_FREQ], 'print(len(words(TEXT)), "words")\nprint(len(frequencies(TEXT)), "different words")\n'),
  [dict(py='frequencies("a b a") == {"a": 2, "b": 1}', msg='`frequencies("a b a")` is `{"a": 2, "b": 1}`.'), dict(py='frequencies("") == {}', msg="Empty text gives an empty dict."),
   dict(py='frequencies(TEXT)["code"] == 4', msg="`code` appears 4 times in `TEXT`."), dict(outHas="different words", msg="It prints the number of different words.")], core="s2m2"))
S.append(step("wf3", "The most common words",
  ["`counts.items()` gives `(word, count)` pairs. Sort them with a **key function**: `lambda pair: (-pair[1], pair[0])` sorts by count, biggest first (the minus sign), and alphabetically when counts tie.",
   "Slicing `ranked[:n]` keeps the first n."],
  "Write `top_words(text, n)` returning the n most common `(word, count)` pairs, ties broken alphabetically. Print the top 5 for `TEXT`.",
  tprog([F_WORDS, F_FREQ, F_TOP], 'print(len(words(TEXT)), "words")\nprint(len(frequencies(TEXT)), "different words")\nprint(top_words(TEXT, 5))\n'),
  [dict(py='top_words("b a b c a b", 2) == [("b", 3), ("a", 2)]', msg="The most frequent come first."), dict(py='top_words("z y x", 2) == [("x", 1), ("y", 1)]', msg="Ties are alphabetical."),
   dict(py='top_words(TEXT, 1) == [("code", 4)]', msg="The top word in `TEXT` is `code`.")], core="s2m3"))
S.append(step("wf4", "Ignore the boring words",
  ["The most common English words (*the*, *and*, *to*) tell you nothing about a text. Analysts drop these **stop words**. A set makes `w not in skip` instant.",
   "A **default argument**, `skip=()`, keeps old calls like `top_words(text, 5)` working unchanged."],
  "Add a `STOP` set of common words. Give `top_words` a third parameter `skip=()` and leave out those words. Print the top 5 non-stop words.",
  tprog([F_WORDS, F_FREQ, F_TOP2], 'print(len(words(TEXT)), "words")\nprint(len(frequencies(TEXT)), "different words")\nprint(top_words(TEXT, 5, skip=STOP))\n', head=TEXT_HEAD + "\n" + STOP),
  [dict(py='top_words("the cat the hat cat", 1, skip={"the"}) == [("cat", 2)]', msg="Skipped words are left out."), dict(py='top_words("b a b", 1) == [("b", 2)]', msg="Without `skip` it works as before."),
   dict(py='isinstance(STOP, set) and "the" in STOP and all(w not in STOP for w, c in top_words(TEXT, 5, skip=STOP))', msg="`STOP` is a set and none of its words reach the top 5.")]))
HEAD5 = TEXT_HEAD.replace("import string\n", "import math\nimport re\nimport string\n") + "\n" + STOP
S.append(step("wf5", "Sentences and reading time",
  ["`re.split(r\"[.!?]+\", text)` splits wherever one or more of `.`, `!` or `?` appear: a tiny **regular expression**. Count the pieces that aren't blank.",
   "Reading speed is about 200 words a minute. `math.ceil` rounds up, so 201 words is 2 minutes, and `max(1, ...)` makes sure even a short note says 1 minute."],
  "Import `math` and `re`. Write `sentence_count(text)` and `reading_minutes(text, wpm=200)`. Print both for `TEXT`.",
  tprog([F_WORDS, F_FREQ, F_TOP2, F_SENT, F_READ], 'print(len(words(TEXT)), "words")\nprint(sentence_count(TEXT), "sentences")\nprint(reading_minutes(TEXT), "min read")\n', head=HEAD5),
  [dict(py='sentence_count("Hi. How are you? Fine!") == 3 and sentence_count("Wait... what") == 2', msg="Sentences are counted, and `...` ends only one."),
   dict(py='reading_minutes("word " * 450) == 3 and reading_minutes("hi") == 1', msg="Reading time rounds up, with a minimum of 1."), dict(py="sentence_count(TEXT) == 6", msg="`TEXT` has 6 sentences.")],
  ref=("Python docs: re.split", "https://docs.python.org/3/library/re.html#re.split")))
S.append(step("wf6", "A bar chart in text",
  ["Charts don't need graphics: `'#' * 4` is `####`. Pad each word to the same width with `word.ljust(width)` so the bars line up.",
   "Build a list of lines, then `\"\\n\".join(lines)` makes one string, which is easier to test than printing line by line."],
  "Write `bar_chart(pairs)` that turns `(word, count)` pairs into lines like `code ### 3`, words padded to the longest. Print the chart of the top 5 non-stop words.",
  tprog([F_WORDS, F_FREQ, F_TOP2, F_SENT, F_READ, F_BAR], 'print(bar_chart(top_words(TEXT, 5, skip=STOP)))\n', head=HEAD5),
  [dict(py='bar_chart([("code", 3), ("a", 1)]) == "code ### 3\\na    # 1"', msg="Bars line up and show the count."), dict(py='bar_chart([("hi", 2)]) == "hi ## 2"', msg="A single bar works."),
   dict(outHas="code   #### 4\nevery  ### 3", msg="The chart for `TEXT` starts with `code` and `every`, bars aligned.")]))
S.append(step("wf7", "The full report",
  ["Combine everything into `report(text)`, which returns the whole analysis as one string. Because every piece is a small function, the report is just a list of lines.",
   "Try pasting your own writing into `TEXT`."],
  "Write `report(text)` returning lines for words, different words, sentences, reading time, `Top words:` and the bar chart. Print `report(TEXT)`.",
  tprog([F_WORDS, F_FREQ, F_TOP2, F_SENT, F_READ, F_BAR, F_REPORT], 'print(report(TEXT))\n', head=HEAD5),
  [dict(py='report(TEXT).splitlines()[:5] == ["Words: 56", "Different words: 41", "Sentences: 6", "Reading time: 1 min", "Top words:"]', msg="The report starts with the five summary lines."),
   dict(py='report("Hi there. Bye.").startswith("Words: 3\\nDifferent words: 3\\nSentences: 2")', msg="It works on any text."), dict(outHas="Top words:\ncode   #### 4", msg="It prints the report with the chart.")]))
project(id="text-analyzer", title="Text Analyzer", lang="python", level="Beginner", hours="1 h", hue="#60a5fa", icon="book", art="### 4",
  tagline="Count words, find the most common ones, estimate reading time and draw a chart in text.",
  desc=["Word counters, search engines and spam filters all start the same way: split text into words and count them. You'll build a small analyzer that does exactly that.",
        "It's the best practice there is for strings, dictionaries, sorting with keys and breaking a problem into small functions."],
  final="A `report(text)` function that prints word and sentence counts, reading time and a bar chart of the top words, ignoring stop words.",
  skills=["string methods", "dictionaries for counting", "sorting with key functions", "sets", "default arguments", "regular expressions", "string formatting"],
  prereq="**Python from Zero**.", core=["s1m4", "s2m2", "s2m3"],
  stretch=["Read the text from a file with `open()`.", "Find the longest word and the average word length.", "Compare two texts: which words appear in one but not the other? (Hint: set difference.)", "Use `collections.Counter` and compare it with your version."],
  demo_stdin=[],
  milestones=[milestone("Words", "Split text into clean words and count them.", S[0:2]), milestone("Insight", "The most common words, minus the boring ones.", S[2:4]),
              milestone("The report", "Sentences, reading time, a chart and the full report.", S[4:7])])

# =============================================================================================== MAZE SOLVER (Python)
S = []
MAZE_HEAD = '''MAZE = [
    "###########",
    "#S....#...#",
    "#.###.#.#.#",
    "#.#...#.#.#",
    "#.#.###.#.#",
    "#.......#E#",
    "###########",
]
'''
F_FIND = 'def find(grid, target):\n    for r, row in enumerate(grid):\n        c = row.find(target)\n        if c != -1:\n            return (r, c)\n    return None\n'
F_NEIGH = ('def neighbours(grid, cell):\n    r, c = cell\n    result = []\n    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):\n        nr, nc = r + dr, c + dc\n'
           '        if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] != "#":\n            result.append((nr, nc))\n    return result\n')
F_DIST = ('def shortest_distance(grid, start, end):\n    queue = deque([(start, 0)])\n    seen = {start}\n    while queue:\n        cell, dist = queue.popleft()\n        if cell == end:\n            return dist\n'
          '        for nb in neighbours(grid, cell):\n            if nb not in seen:\n                seen.add(nb)\n                queue.append((nb, dist + 1))\n    return -1\n')
F_PATH = ('def shortest_path(grid, start, end):\n    queue = deque([start])\n    came_from = {start: None}\n    while queue:\n        cell = queue.popleft()\n        if cell == end:\n            break\n'
          '        for nb in neighbours(grid, cell):\n            if nb not in came_from:\n                came_from[nb] = cell\n                queue.append(nb)\n    if end not in came_from:\n        return []\n'
          '    path = []\n    cell = end\n    while cell is not None:\n        path.append(cell)\n        cell = came_from[cell]\n    path.reverse()\n    return path\n')
F_DRAW = ('def draw(grid, path):\n    rows = [list(row) for row in grid]\n    for r, c in path:\n        if rows[r][c] == ".":\n            rows[r][c] = "o"\n    return "\\n".join("".join(row) for row in rows)\n')
F_DFS = ('def dfs_path(grid, start, end):\n    stack = [start]\n    came_from = {start: None}\n    while stack:\n        cell = stack.pop()\n        if cell == end:\n            break\n'
         '        for nb in neighbours(grid, cell):\n            if nb not in came_from:\n                came_from[nb] = cell\n                stack.append(nb)\n    if end not in came_from:\n        return []\n'
         '    path = []\n    cell = end\n    while cell is not None:\n        path.append(cell)\n        cell = came_from[cell]\n    return path[::-1]\n')
F_SOLVE = ('def solve(grid):\n    start, end = find(grid, "S"), find(grid, "E")\n    path = shortest_path(grid, start, end)\n    if not path:\n        print("No way out.")\n        return None\n'
           '    print(draw(grid, path))\n    print(f"Shortest path: {len(path) - 1} steps")\n    return len(path) - 1\n')
def mprog(funcs, main, imports=""):
    return imports + MAZE_HEAD + "".join("\n\n" + f for f in funcs) + "\n\n" + main
IMP = "from collections import deque\n\n"
VALID = "lambda p: all(abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1 and MAZE[b[0]][b[1]] != '#' for a, b in zip(p, p[1:]))"
S.append(step("mz1", "The maze as data",
  ["A grid is a **list of strings**: `MAZE[row][col]` is one character. `#` is a wall, `.` is open floor, `S` is the start and `E` the exit.",
   "Positions are `(row, col)` **tuples**. `str.find(ch)` returns the column of a character in a row, or `-1` if it isn't there."],
  "Below `MAZE`, write `find(grid, target)` that returns the `(row, col)` of the first `target` character, or `None`. Print where `S` and `E` are.",
  mprog([F_FIND], 'print("Start:", find(MAZE, "S"))\nprint("Exit:", find(MAZE, "E"))\n'),
  [dict(py='find(MAZE, "S") == (1, 1) and find(MAZE, "E") == (5, 9)', msg="`S` is at (1, 1) and `E` at (5, 9)."), dict(py='find(["..", ".X"], "X") == (1, 1) and find(["ab"], "z") is None', msg="It works on any grid and returns `None` when missing."),
   dict(outHas="Start: (1, 1)", msg="It prints the start.")],
  starter=MAZE_HEAD, core="s2m5"))
S.append(step("mz2", "Where can I step?",
  ["From any cell you can move up, down, left or right. A move is allowed if it stays inside the grid and isn't a wall.",
   "Listing the four directions as `(dr, dc)` pairs, `((-1, 0), (1, 0), (0, -1), (0, 1))`, avoids four near-identical `if` blocks."],
  "Write `neighbours(grid, cell)` returning the open cells next to `cell`, in the order up, down, left, right.",
  mprog([F_FIND, F_NEIGH], 'print("Start:", find(MAZE, "S"))\nprint("Exit:", find(MAZE, "E"))\nprint(neighbours(MAZE, find(MAZE, "S")))\n'),
  [dict(py='neighbours(MAZE, (1, 1)) == [(2, 1), (1, 2)]', msg="From the start you can go down or right."), dict(py='neighbours(MAZE, (3, 4)) == [(3, 3), (3, 5)]', msg="Walls above and below are excluded."),
   dict(py='neighbours(["..", ".."], (0, 0)) == [(1, 0), (0, 1)]', msg="Cells outside the grid are excluded.")], core="s2m5"))
S.append(step("mz3", "Breadth-first search",
  ["**BFS** explores the maze in rings: every cell 1 step away, then 2, then 3. A **queue** (first in, first out) keeps that order; `collections.deque` gives a fast `popleft()`.",
   "Because cells are reached in order of distance, the first time BFS reaches the exit is guaranteed to be the shortest way there. A `seen` set stops it going in circles."],
  "Import `deque`. Write `shortest_distance(grid, start, end)` that returns the fewest steps from start to end, or `-1` if there's no way.",
  mprog([F_FIND, F_NEIGH, F_DIST], 'start, end = find(MAZE, "S"), find(MAZE, "E")\nprint("Shortest distance:", shortest_distance(MAZE, start, end))\n', IMP),
  [dict(py='shortest_distance(MAZE, (1, 1), (5, 9)) == 20', msg="The exit is 20 steps from the start."), dict(py='shortest_distance(["S#E"], (0, 0), (0, 2)) == -1', msg="A blocked exit gives -1."),
   dict(py='shortest_distance(["S.E"], (0, 0), (0, 0)) == 0', msg="Start equal to end is 0 steps."), dict(src="deque", msg="You use a `deque` as the queue.")],
  ref=("Python docs: collections.deque", "https://docs.python.org/3/library/collections.html#collections.deque"), core="s2m5"))
S.append(step("mz4", "Remember the way back",
  ["A distance is nice, but you want the route. Store, for each cell, the cell you came from: `came_from[next] = cell`. It doubles as the `seen` set.",
   "When you reach the exit, follow `came_from` backwards to the start, then reverse the list."],
  "Write `shortest_path(grid, start, end)` returning the list of cells from start to end (both included), or `[]` if there's no way. Print its length minus one.",
  mprog([F_FIND, F_NEIGH, F_DIST, F_PATH], 'start, end = find(MAZE, "S"), find(MAZE, "E")\npath = shortest_path(MAZE, start, end)\nprint("Steps:", len(path) - 1)\n', IMP),
  [dict(py='(lambda p: p[0] == (1, 1) and p[-1] == (5, 9) and len(p) == 21)(shortest_path(MAZE, (1, 1), (5, 9)))', msg="The path runs from S to E in 20 steps."),
   dict(py=f"({VALID})(shortest_path(MAZE, (1, 1), (5, 9)))", msg="Every step moves to a neighbouring open cell."), dict(py='shortest_path(["S#E"], (0, 0), (0, 2)) == []', msg="No route gives `[]`.")]))
S.append(step("mz5", "Draw the route",
  ["Strings can't be changed in place, so turn each row into a list of characters, mark the route with `o`, and join everything back together.",
   "Leave `S` and `E` as they are, so the start and exit stay visible."],
  "Write `draw(grid, path)` that returns the maze as one string with path cells (but not `S` or `E`) shown as `o`. Print the drawing.",
  mprog([F_FIND, F_NEIGH, F_DIST, F_PATH, F_DRAW], 'start, end = find(MAZE, "S"), find(MAZE, "E")\npath = shortest_path(MAZE, start, end)\nprint(draw(MAZE, path))\n', IMP),
  [dict(py='draw(["S.E"], [(0, 0), (0, 1), (0, 2)]) == "SoE"', msg='`draw(["S.E"], ...)` is `SoE`.'), dict(py='draw(["S.", ".E"], []) == "S.\\n.E"', msg="Rows are joined with newlines."),
   dict(py='draw(MAZE, shortest_path(MAZE, (1, 1), (5, 9))).count("o") == 19', msg="The drawn route has 19 `o` cells between S and E."), dict(outHas="#o###.#o#o#", msg="It prints the drawing.")]))
S.append(step("mz6", "Depth-first search, for comparison",
  ["Swap the queue for a **stack** (`list.append` and `list.pop`) and you get **DFS**: it dives down one corridor as far as it can before backtracking.",
   "DFS still finds *a* way out, but not necessarily the shortest. Comparing the two is the best way to see why BFS is the right tool for shortest paths."],
  "Write `dfs_path(grid, start, end)` like `shortest_path` but with a stack. Print both path lengths.",
  mprog([F_FIND, F_NEIGH, F_DIST, F_PATH, F_DRAW, F_DFS], 'start, end = find(MAZE, "S"), find(MAZE, "E")\nprint("BFS:", len(shortest_path(MAZE, start, end)) - 1, "steps")\nprint("DFS:", len(dfs_path(MAZE, start, end)) - 1, "steps")\n', IMP),
  [dict(py=f'(lambda p: p[0] == (1, 1) and p[-1] == (5, 9) and ({VALID})(p))(dfs_path(MAZE, (1, 1), (5, 9)))', msg="DFS finds a valid route from S to E."),
   dict(py='len(dfs_path(MAZE, (1, 1), (5, 9))) >= len(shortest_path(MAZE, (1, 1), (5, 9)))', msg="It's never shorter than the BFS route."), dict(py='dfs_path(["S#E"], (0, 0), (0, 2)) == []', msg="No route gives `[]`."),
   dict(outHas="BFS: 20 steps", msg="It prints both lengths.")]))
BLOCKED = 'BLOCKED = [\n    "#####",\n    "#S#E#",\n    "#####",\n]\n'
S.append(step("mz7", "Solve any maze",
  ["Wrap it all in `solve(grid)`: find S and E, search, and either draw the route or say there's no way out. Return the number of steps (or `None`), so other code can use the answer.",
   "Try drawing your own maze in `MAZE`: as long as it has one `S` and one `E`, your solver handles it."],
  "Write `solve(grid)` that prints the drawing and `Shortest path: N steps` and returns N, or prints `No way out.` and returns `None`. Solve `MAZE` and a `BLOCKED` maze.",
  mprog([F_FIND, F_NEIGH, F_DIST, F_PATH, F_DRAW, F_DFS, F_SOLVE], BLOCKED + '\nsolve(MAZE)\nsolve(BLOCKED)\n', IMP),
  [dict(py='solve(["S.E"]) == 2 and solve(["S#E"]) is None', msg="`solve` returns the step count, or `None` with no way out."), dict(outHas="Shortest path: 20 steps", msg="It solves `MAZE` in 20 steps."),
   dict(outHas="No way out.", msg="It reports the blocked maze.")]))
project(id="maze-solver", title="Maze Solver", lang="python", level="Advanced", hours="1.5 h", hue="#8b7dff", icon="route", art="S o o E",
  tagline="Find the shortest way out of any maze with breadth-first search, and draw the route.",
  desc=["Sat-navs, game characters and network routers all solve the same problem: the shortest route through a graph. You'll build that from scratch on a grid maze.",
        "You'll implement breadth-first search, reconstruct the path, draw it, and compare it against depth-first search to see why the choice of algorithm matters."],
  final="A solver that takes any text maze, finds the shortest route with BFS, draws it, and reports when there's no way out.",
  skills=["grids as lists of strings", "tuples", "queues (deque)", "breadth-first search", "path reconstruction", "depth-first search", "graph thinking"],
  prereq="**Algorithms with Python** (or comfort with lists, dicts and loops).", core=["s2m5", "s2m1"],
  stretch=["Allow diagonal moves.", "Add weighted cells (mud costs 3) and switch to Dijkstra's algorithm with `heapq`.", "Generate random mazes with a randomised DFS.", "Count how many cells each algorithm visits."],
  demo_stdin=[],
  milestones=[milestone("The grid", "Mazes as data, and the moves from each cell.", S[0:2]), milestone("Searching", "BFS for distance and the route itself.", S[2:4]),
              milestone("Results", "Draw it, compare with DFS, solve any maze.", S[4:7])])

# =============================================================================================== SHOPPING CART (JavaScript)
S = []
C = Code('''// Shopping cart logic. Prices are whole cents, so the maths stays exact.

const PRODUCTS = {
  tee: { name: "T-shirt", price: 1800 },
  mug: { name: "Mug", price: 950 },
  cap: { name: "Cap", price: 1450 },
  socks: { name: "Socks", price: 600 },
};

function formatPrice(cents) {
  return "$" + (cents / 100).toFixed(2);
}
''')
S.append(step("sc1", "Products and prices in cents",
  ["Money and floating point don't mix: `0.1 + 0.2` is `0.30000000000000004`. Shops store prices as whole **cents** and only convert to dollars for display.",
   "An object keyed by product id is a quick lookup table: `PRODUCTS.mug.price` is `950`."],
  "Create `PRODUCTS` with tee (T-shirt, 1800), mug (Mug, 950), cap (Cap, 1450) and socks (Socks, 600). Write `formatPrice(cents)` returning a string like `$18.00`.",
  C.text, [dict(js='PRODUCTS.mug.price === 950 && PRODUCTS.tee.name === "T-shirt" && Object.keys(PRODUCTS).length === 4', msg="`PRODUCTS` has the four products, priced in cents."),
           dict(js='formatPrice(1800) === "$18.00" && formatPrice(5) === "$0.05" && formatPrice(0) === "$0.00"', msg="`formatPrice` shows dollars with two decimals.")],
  starter="// Shopping cart logic\n", core="s1m4", ref=("MDN: Number.prototype.toFixed", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed")))
C.add('''
function addToCart(cart, id, qty = 1) {
  if (!PRODUCTS[id]) throw new Error(`Unknown product: ${id}`);
  if (cart.some(line => line.id === id)) {
    return cart.map(line => (line.id === id ? { ...line, qty: line.qty + qty } : line));
  }
  return [...cart, { id, qty }];
}
''')
SAME = "(a, b) => JSON.stringify(a) === JSON.stringify(b)"
S.append(step("sc2", "Add to cart, without mutating",
  ["A cart is an array of lines like `{ id: \"mug\", qty: 2 }`. Instead of changing it, return a **new** array: `[...cart, line]` copies and appends, and `map` with `{ ...line, qty }` copies one line with a new quantity.",
   "Never changing data in place (**immutability**) is how React and Redux work, and it makes bugs much easier to find. Throwing an `Error` for an unknown id catches typos early."],
  "Write `addToCart(cart, id, qty = 1)` that returns a new cart: add a line, or increase the quantity if the product is already there. Throw an `Error` for unknown products.",
  C.text, [dict(js=f'({SAME})(addToCart([], "mug"), [{{ id: "mug", qty: 1 }}])', msg='`addToCart([], "mug")` gives one line with qty 1.'),
           dict(js=f'({SAME})(addToCart(addToCart([], "mug"), "mug", 2), [{{ id: "mug", qty: 3 }}])', msg="Adding the same product again increases its quantity."),
           dict(js='(() => { const c = [{ id: "cap", qty: 1 }]; addToCart(c, "cap"); addToCart(c, "tee"); return c.length === 1 && c[0].qty === 1; })()', msg="The original cart is never changed."),
           dict(js='(() => { try { addToCart([], "boat"); return false; } catch (e) { return e instanceof Error; } })()', msg="An unknown product throws an `Error`.")],
  ref=("MDN: Spread syntax", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax")))
C.add('''
function setQty(cart, id, qty) {
  if (qty <= 0) return cart.filter(line => line.id !== id);
  return cart.map(line => (line.id === id ? { ...line, qty } : line));
}

function removeFromCart(cart, id) {
  return setQty(cart, id, 0);
}
''')
S.append(step("sc3", "Change and remove",
  ["`filter` keeps the lines that pass a test, so removing a product is `cart.filter(line => line.id !== id)`.",
   "Setting a quantity of 0 or less should remove the line, which means `removeFromCart` can simply call `setQty(cart, id, 0)`: one rule, one place."],
  "Write `setQty(cart, id, qty)` (0 or less removes the line) and `removeFromCart(cart, id)`. Both return new carts.",
  C.text, [dict(js=f'({SAME})(setQty([{{ id: "mug", qty: 1 }}], "mug", 4), [{{ id: "mug", qty: 4 }}])', msg="`setQty` changes a quantity."),
           dict(js=f'({SAME})(setQty([{{ id: "mug", qty: 1 }}, {{ id: "cap", qty: 2 }}], "mug", 0), [{{ id: "cap", qty: 2 }}])', msg="A quantity of 0 removes the line."),
           dict(js=f'({SAME})(removeFromCart([{{ id: "tee", qty: 1 }}, {{ id: "cap", qty: 1 }}], "tee"), [{{ id: "cap", qty: 1 }}])', msg="`removeFromCart` removes a product."),
           dict(js='(() => { const c = [{ id: "mug", qty: 1 }]; setQty(c, "mug", 9); removeFromCart(c, "mug"); return c[0].qty === 1; })()', msg="The original cart is unchanged.")]))
C.add('''
function lineTotal(line) {
  return PRODUCTS[line.id].price * line.qty;
}

function subtotal(cart) {
  return cart.reduce((sum, line) => sum + lineTotal(line), 0);
}
''')
S.append(step("sc4", "Add it all up",
  ["`reduce` walks an array carrying a running value: start at `0` and add each line's total. It's the standard way to sum a list in JavaScript.",
   "Keep `lineTotal(line)` separate: the receipt will need it too."],
  "Write `lineTotal(line)` (price × quantity) and `subtotal(cart)` using `reduce`.",
  C.text, [dict(js='lineTotal({ id: "mug", qty: 3 }) === 2850', msg="`lineTotal` multiplies price by quantity."), dict(js='subtotal([{ id: "tee", qty: 2 }, { id: "socks", qty: 1 }]) === 4200', msg="`subtotal` adds every line."),
           dict(js="subtotal([]) === 0", msg="An empty cart's subtotal is 0."), dict(src="\\.reduce\\(", msg="You use `reduce`.")],
  ref=("MDN: Array.prototype.reduce", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce")))
C.add('''
function discount(amount, code) {
  if (!code) return 0;
  if (code === "SAVE10") return Math.round(amount * 0.1);
  if (code === "FIVEOFF") return Math.min(500, amount);
  throw new Error(`Unknown code: ${code}`);
}
''')
S.append(step("sc5", "Discount codes",
  ["Codes are business rules, so keep them in one function. `SAVE10` takes 10% off (rounded to a whole cent with `Math.round`); `FIVEOFF` takes $5 off, but never more than the order itself, which is what `Math.min` guarantees.",
   "No code means no discount. A code you don't recognise is an error the page should show, not silently ignore."],
  "Write `discount(amount, code)` returning the discount in cents: 0 with no code, 10% for `SAVE10`, up to 500 for `FIVEOFF`, and throw for anything else.",
  C.text, [dict(js='discount(4200, "SAVE10") === 420 && discount(1005, "SAVE10") === 101', msg="`SAVE10` is 10%, rounded."), dict(js='discount(4200, "FIVEOFF") === 500 && discount(300, "FIVEOFF") === 300', msg="`FIVEOFF` is $5, but never more than the amount."),
           dict(js='discount(4200) === 0 && discount(4200, "") === 0', msg="No code, no discount."), dict(js='(() => { try { discount(100, "FREE"); return false; } catch (e) { return true; } })()', msg="Unknown codes throw.")]))
C.add('''
const TAX_RATE = 0.08;

function totals(cart, code) {
  const sub = subtotal(cart);
  const off = discount(sub, code);
  const tax = Math.round((sub - off) * TAX_RATE);
  return { subtotal: sub, discount: off, tax, total: sub - off + tax };
}
''')
S.append(step("sc6", "Tax and the final total",
  ["Order matters: the discount comes off first, then tax is charged on what's left. Round the tax to a whole cent.",
   "Returning an object, `{ subtotal, discount, tax, total }`, gives the caller every number at once, ready for a receipt or a checkout page."],
  "Add `TAX_RATE = 0.08` and write `totals(cart, code)` returning `{ subtotal, discount, tax, total }` in cents.",
  C.text, [dict(js=f'({SAME})(totals([{{ id: "tee", qty: 2 }}, {{ id: "socks", qty: 1 }}], "SAVE10"), {{ subtotal: 4200, discount: 420, tax: 302, total: 4082 }})', msg="2 T-shirts and socks with SAVE10 total $40.82."),
           dict(js=f'({SAME})(totals([{{ id: "mug", qty: 1 }}]), {{ subtotal: 950, discount: 0, tax: 76, total: 1026 }})', msg="Without a code there's no discount."),
           dict(js='totals([], "FIVEOFF").total === 0', msg="An empty cart totals 0, even with a code.")]))
C.add('''
function receipt(cart, code) {
  const t = totals(cart, code);
  const lines = cart.map(line => `${line.qty} x ${PRODUCTS[line.id].name}: ${formatPrice(lineTotal(line))}`);
  lines.push(`Subtotal: ${formatPrice(t.subtotal)}`);
  if (t.discount > 0) lines.push(`Discount (${code}): -${formatPrice(t.discount)}`);
  lines.push(`Tax: ${formatPrice(t.tax)}`);
  lines.push(`Total: ${formatPrice(t.total)}`);
  return lines.join("\\n");
}

let cart = [];
cart = addToCart(cart, "tee", 2);
cart = addToCart(cart, "socks");
cart = addToCart(cart, "mug");
cart = removeFromCart(cart, "mug");
console.log(receipt(cart, "SAVE10"));
''')
S.append(step("sc7", "Print the receipt",
  ["The receipt is presentation, so it's the only place that formats money. Everything else stays in cents.",
   "Finish by using your functions the way a store would: build a cart step by step, then print it."],
  "Write `receipt(cart, code)` with a line per product (`2 x T-shirt: $36.00`), then Subtotal, Discount (only if there is one), Tax and Total. Build a cart and `console.log` its receipt with `SAVE10`.",
  C.text, [dict(js='receipt([{ id: "tee", qty: 2 }, { id: "socks", qty: 1 }], "SAVE10") === "2 x T-shirt: $36.00\\n1 x Socks: $6.00\\nSubtotal: $42.00\\nDiscount (SAVE10): -$4.20\\nTax: $3.02\\nTotal: $40.82"', msg="The receipt lists lines, subtotal, discount, tax and total."),
           dict(js='!receipt([{ id: "mug", qty: 1 }]).includes("Discount")', msg="There's no discount line without a code."), dict(js='_out.includes("Total: $")', msg="Your program prints a receipt.")]))
project(id="shopping-cart", title="Shopping Cart Logic", lang="js", level="Beginner", hours="1 h", hue="#fb923c", icon="bars", art="$40.82",
  tagline="The engine behind every online shop: carts, quantities, discount codes, tax and receipts.",
  desc=["Every online shop runs the same logic underneath the pretty pages. You'll write it as small, testable functions: no HTML, just the rules.",
        "You'll learn why money is stored in cents, how to update data without mutating it, and how to use `map`, `filter` and `reduce` for real work."],
  final="A cart module with add, change and remove, subtotals, discount codes, tax and a formatted receipt, all exact to the cent and never mutating data.",
  skills=["objects as lookup tables", "immutability", "spread syntax", "map / filter / reduce", "throwing errors", "money in cents", "template literals"],
  prereq="**JavaScript from Zero**.", core=["s1m4", "s4m5"],
  stretch=["Add a `BUNDLE` code: buy 2 T-shirts, get socks free.", "Support stock levels and refuse to add more than is available.", "Wire it to a web page with buttons and a live total.", "Write tests for every function with `console.assert`."],
  milestones=[milestone("The cart", "Prices in cents and a cart you never mutate.", S[0:3]), milestone("Money", "Subtotals, discounts and tax.", S[3:6]), milestone("Checkout", "A formatted receipt.", S[6:7])])

# =============================================================================================== MUSIC STREAMING ANALYTICS (SQL)
S = []
CAT = '''-- Music streaming analytics

CREATE TABLE artists (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);
INSERT INTO artists VALUES
  (1, 'Nova Lane'), (2, 'Static Bloom'), (3, 'Juniper Row'), (4, 'Kilo Echo');

CREATE TABLE tracks (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  artist_id INTEGER NOT NULL REFERENCES artists(id),
  seconds INTEGER NOT NULL
);
INSERT INTO tracks VALUES
  (1, 'Night Drive', 1, 212), (2, 'Glass Hearts', 1, 185),
  (3, 'Paper Moons', 2, 240), (4, 'Low Tide', 2, 198),
  (5, 'Wildflower', 3, 205), (6, 'Copper Sky', 3, 231),
  (7, 'Signal', 4, 176), (8, 'Afterglow', 4, 264);
'''
PLAYS = '''
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  country TEXT NOT NULL
);
INSERT INTO users VALUES
  (1, 'ana', 'PT'), (2, 'ben', 'UK'), (3, 'chi', 'NG'), (4, 'dev', 'IN'), (5, 'eli', 'UK');

CREATE TABLE plays (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  track_id INTEGER NOT NULL REFERENCES tracks(id),
  played_at TEXT NOT NULL
);
INSERT INTO plays VALUES
  (1, 1, 1, '2026-10-01 08:10'), (2, 1, 3, '2026-10-01 08:14'), (3, 2, 1, '2026-10-01 09:00'),
  (4, 3, 5, '2026-10-01 12:30'), (5, 2, 7, '2026-10-01 18:45'), (6, 1, 1, '2026-10-02 07:55'),
  (7, 3, 6, '2026-10-02 10:05'), (8, 4, 1, '2026-10-02 11:20'), (9, 4, 3, '2026-10-02 11:25'),
  (10, 2, 8, '2026-10-02 19:00'), (11, 3, 5, '2026-10-02 21:40'), (12, 5, 3, '2026-10-03 06:30'),
  (13, 5, 1, '2026-10-03 06:35'), (14, 1, 2, '2026-10-03 08:00'), (15, 4, 5, '2026-10-03 13:10'),
  (16, 2, 1, '2026-10-03 17:00'), (17, 3, 3, '2026-10-03 20:15'), (18, 4, 4, '2026-10-03 22:05'),
  (19, 5, 8, '2026-10-03 23:30');
'''
ALL = CAT + PLAYS
S.append(step("mu1", "Artists and tracks",
  ["A streaming service's catalogue is two tables: **artists**, and **tracks** that point at their artist with a foreign key. A track's length is stored in whole seconds.",
   "Several rows can go in one `INSERT` by separating them with commas."],
  "Create `artists` (id, name) and `tracks` (id, title, artist_id → artists, seconds) and insert the data from the hint. End with a query listing each track's `title` and its artist's `name`, ordered by track id.",
  CAT + "\nSELECT tracks.title, artists.name\nFROM tracks\nJOIN artists ON artists.id = tracks.artist_id\nORDER BY tracks.id;\n",
  [dict(src="REFERENCES artists", msg="`tracks.artist_id` references `artists`."), dict(rows=True, ordered=True, msg="All 8 tracks are listed with their artist.")],
  hint="Artists: 1 Nova Lane, 2 Static Bloom, 3 Juniper Row, 4 Kilo Echo. Tracks (id, title, artist, seconds): 1 Night Drive 1 212, 2 Glass Hearts 1 185, 3 Paper Moons 2 240, 4 Low Tide 2 198, 5 Wildflower 3 205, 6 Copper Sky 3 231, 7 Signal 4 176, 8 Afterglow 4 264.",
  starter="-- Music streaming analytics\n", core="s4m4"))
S.append(step("mu2", "Users and plays",
  ["Every time someone presses play, the service records an **event**: who, what and when. Event tables grow fastest and answer the most questions.",
   "Timestamps are stored as `'YYYY-MM-DD HH:MM'` text, which SQLite's date functions understand and which sorts correctly."],
  "Add `users` (id, name, country) and `plays` (id, user_id, track_id, played_at) with the data from the hint (the full insert is long, so copy it from the solution if you get stuck). End with `SELECT COUNT(*) AS plays FROM plays;`",
  ALL + "\nSELECT COUNT(*) AS plays FROM plays;\n",
  [dict(src="REFERENCES users", msg="`plays.user_id` references `users`."), dict(src="REFERENCES tracks", msg="`plays.track_id` references `tracks`."), dict(rows=True, msg="There are 19 plays.")],
  hint="Users: 1 ana PT, 2 ben UK, 3 chi NG, 4 dev IN, 5 eli UK. Plays are (id, user_id, track_id, played_at); there are 19 of them across 2026-10-01 to 2026-10-03."))
S.append(step("mu3", "The chart: top tracks",
  ["Join plays to tracks and artists, group by track and count. `ORDER BY plays DESC LIMIT 3` is the top 3: that's how every chart is made."],
  "List the top 3 tracks: `title`, artist `name` as `artist` and the number of `plays`, most played first.",
  ALL + "\nSELECT tracks.title, artists.name AS artist, COUNT(*) AS plays\nFROM plays\nJOIN tracks ON tracks.id = plays.track_id\nJOIN artists ON artists.id = tracks.artist_id\nGROUP BY tracks.id\nORDER BY plays DESC\nLIMIT 3;\n",
  [dict(src="LIMIT 3", msg="You keep the top 3 with `LIMIT`."), dict(rows=True, ordered=True, msg="Night Drive (6), Paper Moons (4), Wildflower (3).")], core="s4m4"))
S.append(step("mu4", "Minutes listened",
  ["`SUM(tracks.seconds)` adds up listening time. Divide by `60.0`, not `60`: dividing two integers in SQL throws the fraction away. `ROUND(x, 1)` keeps one decimal."],
  "For each user, show `name` and total `minutes` listened (one decimal), most first, then by name.",
  ALL + "\nSELECT users.name, ROUND(SUM(tracks.seconds) / 60.0, 1) AS minutes\nFROM plays\nJOIN users ON users.id = plays.user_id\nJOIN tracks ON tracks.id = plays.track_id\nGROUP BY users.id\nORDER BY minutes DESC, users.name;\n",
  [dict(src="60\\.0", msg="You divide by `60.0`."), dict(rows=True, ordered=True, msg="Every user's minutes are right, in order.")]))
S.append(step("mu5", "Daily activity",
  ["`date(played_at)` keeps just the day. `COUNT(DISTINCT user_id)` counts each listener once, however many songs they played: that's **daily active users**, the number every app watches."],
  "For each `day`, show the number of `plays` and of distinct `listeners`, in date order.",
  ALL + "\nSELECT date(played_at) AS day, COUNT(*) AS plays, COUNT(DISTINCT user_id) AS listeners\nFROM plays\nGROUP BY day\nORDER BY day;\n",
  [dict(src="DISTINCT", msg="You use `COUNT(DISTINCT ...)`."), dict(rows=True, ordered=True, msg="Each day's plays and listeners are right.")]))
S.append(step("mu6", "Each artist's biggest hit",
  ["A **window function** ranks rows without collapsing them. `RANK() OVER (PARTITION BY artist ORDER BY plays DESC)` restarts the ranking for each artist.",
   "Window functions can't go in `WHERE`, so compute the rank in a **CTE** (`WITH ranked AS (...)`) and filter outside it."],
  "For each artist, show `artist`, its most played track as `title` and its `plays`, ordered by artist name.",
  ALL + "\nWITH ranked AS (\n  SELECT artists.name AS artist, tracks.title, COUNT(plays.id) AS plays,\n         RANK() OVER (PARTITION BY artists.id ORDER BY COUNT(plays.id) DESC) AS r\n  FROM tracks\n  JOIN artists ON artists.id = tracks.artist_id\n  LEFT JOIN plays ON plays.track_id = tracks.id\n  GROUP BY tracks.id\n)\nSELECT artist, title, plays FROM ranked WHERE r = 1 ORDER BY artist;\n",
  [dict(src="PARTITION BY", msg="You rank within each artist using `PARTITION BY`."), dict(rows=True, ordered=True, msg="One top track per artist.")], core="s6m2"))
S.append(step("mu7", "Plays by country, as a share",
  ["`SUM(COUNT(*)) OVER ()` is the grand total across all groups, computed alongside each group. Divide by it (times `100.0`) to get each country's percentage in the same query."],
  "Show each `country`, its `plays` and its share `pct` of all plays (one decimal), most plays first, then by country.",
  ALL + "\nSELECT users.country, COUNT(*) AS plays,\n       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct\nFROM plays\nJOIN users ON users.id = plays.user_id\nGROUP BY users.country\nORDER BY plays DESC, users.country;\n",
  [dict(src="OVER\\s*\\(\\s*\\)", msg="You use a window over all rows: `OVER ()`."), dict(rows=True, ordered=True, msg="Each country's plays and share are right.")]))
S.append(step("mu8", "New listeners per day",
  ["Growth teams ask: how many people listened for the first time each day? Find each user's first day with `MIN(date(played_at))` in a CTE, then count users per first day.",
   "That's a **cohort** query, the start of every retention report."],
  "Show each `day` and how many users had their first play that day as `new_listeners`, in date order.",
  ALL + "\nWITH first_play AS (\n  SELECT user_id, MIN(date(played_at)) AS day\n  FROM plays\n  GROUP BY user_id\n)\nSELECT day, COUNT(*) AS new_listeners\nFROM first_play\nGROUP BY day\nORDER BY day;\n",
  [dict(src="MIN\\(", msg="You find each user's first play with `MIN`."), dict(rows=True, ordered=True, msg="3 new listeners on the 1st, then 1 on each following day.")]))
project(id="music-analytics", title="Music Streaming Analytics", lang="sql", level="Advanced", hours="1.5 h", hue="#e879f9", icon="chart", art="▶ 19 plays",
  tagline="Model a streaming service and answer the questions its data team asks every morning.",
  desc=["Streaming services live on their play data. You'll design the tables, load a few days of listening, and write the queries behind charts, dashboards and growth reports.",
        "It's a tour of analytics SQL: joins across four tables, grouping, distinct counts, date functions, CTEs and window functions."],
  final="A four-table music database with queries for the top chart, minutes listened, daily active users, each artist's biggest hit, plays by country and new listeners per day.",
  skills=["schema design", "event tables", "multi-table JOINs", "COUNT(DISTINCT)", "date functions", "CTEs", "window functions (RANK, SUM OVER)", "cohort queries"],
  prereq="the **SQL Analytics** bootcamp course, or the **Library Database** project.", core=["s4m4", "s6m2"],
  stretch=["Find users who played the same track twice.", "Compute each user's favourite artist.", "Rank days by plays with `DENSE_RANK`.", "Add a `skipped` column and find the most-skipped track."],
  milestones=[milestone("The data model", "Catalogue, users and play events.", S[0:2]), milestone("Everyday questions", "Charts, listening time and daily activity.", S[2:5]),
              milestone("Analyst level", "Window functions and cohorts.", S[5:8])])
