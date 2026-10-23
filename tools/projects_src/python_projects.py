from _lib import *

GUESSES = [str(i) for i in range(1, 101)]

# =============================================================================================== NUMBER GUESSING GAME
S = []
v1 = 'import random\n\nsecret = random.randint(1, 100)\nprint("I\'m thinking of a number between 1 and 100.")\n'
S.append(step("ng1", "Pick a secret number",
  ["Python comes with a library of ready-made tools. `import random` loads the module for random numbers, and `random.randint(1, 100)` returns a whole number from 1 to 100, **including** both ends.",
   "Store it in a variable so the rest of the program can compare guesses against it."],
  "Import `random`, store a random number from 1 to 100 in `secret`, and print `I'm thinking of a number between 1 and 100.`",
  v1, [dict(src="import random", msg="You import `random`."), dict(py="isinstance(secret, int) and 1 <= secret <= 100", msg="`secret` is a whole number from 1 to 100."),
       dict(outHas="between 1 and 100", msg="The program announces the range.")],
  starter="# Number guessing game\n", core="s1m5", ref=("Python docs: random.randint", "https://docs.python.org/3/library/random.html#random.randint")))
v2 = v1.replace('\nsecret =', '\n\ndef check_guess(secret, guess):\n    if guess < secret:\n        return "Too low"\n    if guess > secret:\n        return "Too high"\n    return "Correct"\n\n\nsecret =')
S.append(step("ng2", "Judge a guess",
  ["Put the rule of the game in a **function**: given the secret and a guess, return `\"Too low\"`, `\"Too high\"` or `\"Correct\"`. A function with no printing and no input is easy to test and reuse.",
   "Each `return` ends the function immediately, so you don't need `elif` after a branch that returns."],
  "Write `check_guess(secret, guess)` returning `\"Too low\"`, `\"Too high\"` or `\"Correct\"`.",
  v2, [dict(py='check_guess(50, 10) == "Too low"', msg="`check_guess(50, 10)` is `Too low`."), dict(py='check_guess(50, 90) == "Too high"', msg="`check_guess(50, 90)` is `Too high`."),
       dict(py='check_guess(50, 50) == "Correct"', msg="`check_guess(50, 50)` is `Correct`."), dict(py='check_guess(1, 2) == "Too high" and check_guess(2, 1) == "Too low"', msg="Neighbouring numbers work too.")], core="s1m3"))
v3 = v2 + '\nattempts = 0\nwhile True:\n    guess = int(input("Your guess: "))\n    attempts += 1\n    result = check_guess(secret, guess)\n    print(result)\n    if result == "Correct":\n        break\nprint(f"You got it in {attempts} attempts.")\n'
S.append(step("ng3", "Keep guessing until it's right",
  ["`input(\"Your guess: \")` waits for the player to type a line and returns it as a **string**. `int(...)` turns it into a number you can compare.",
   "`while True:` repeats forever; `break` jumps out once the guess is correct. Count the attempts as you go.",
   "In this editor, `input()` reads from the **Input** box above the editor: one line per call. The checks fill it in for you."],
  "Write a `while True` loop that reads a guess with `input`, converts it with `int`, counts `attempts`, prints the result of `check_guess`, and stops when it's correct. Afterwards print `You got it in N attempts.`",
  v3, [dict(outHas="You got it in", msg="The game ends with `You got it in N attempts.`"), dict(py="attempts == secret", msg="`attempts` counts every guess (the checks guess 1, 2, 3 and so on)."),
       dict(src="while ", msg="You use a `while` loop.")], stdin=GUESSES, core="s1m2"))
v4 = v3.replace('    guess = int(input("Your guess: "))\n', '    text = input("Your guess: ")\n    try:\n        guess = int(text)\n    except ValueError:\n        print("Please enter a whole number.")\n        continue\n')
S.append(step("ng4", "Survive bad input",
  ["Type `abc` and `int(\"abc\")` crashes the program with a `ValueError`. Real programs expect bad input and recover.",
   "`try:` runs code that might fail; `except ValueError:` runs only if that error happens. `continue` skips straight to the next loop round without counting the attempt."],
  "Wrap the conversion in `try`/`except ValueError`. On bad input print `Please enter a whole number.` and `continue` without counting an attempt.",
  v4, [dict(outHas="Please enter a whole number.", msg="Bad input prints `Please enter a whole number.`"), dict(py="attempts == secret", msg="Bad input isn't counted as an attempt."),
       dict(src="except ValueError", msg="You catch `ValueError` specifically.")], stdin=["abc", "", "4.5"] + GUESSES, core="s1m5",
  ref=("Python tutorial: Handling exceptions", "https://docs.python.org/3/tutorial/errors.html#handling-exceptions")))
v5 = ('import random\n\n\ndef check_guess(secret, guess):\n    if guess < secret:\n        return "Too low"\n    if guess > secret:\n        return "Too high"\n    return "Correct"\n\n\n'
      'def play_round(secret):\n    print("I\'m thinking of a number between 1 and 100.")\n    attempts = 0\n    while True:\n        text = input("Your guess: ")\n        try:\n            guess = int(text)\n        except ValueError:\n            print("Please enter a whole number.")\n            continue\n'
      '        attempts += 1\n        result = check_guess(secret, guess)\n        print(result)\n        if result == "Correct":\n            return attempts\n\n\n'
      'secret = random.randint(1, 100)\nattempts = play_round(secret)\nprint(f"You got it in {attempts} attempts.")\n')
S.append(step("ng5", "Refactor into a function",
  ["The game loop is getting long. Move it into `play_round(secret)`, which plays one round and **returns** the number of attempts. Returning from inside the loop ends both the loop and the function.",
   "This is **refactoring**: same behaviour, better structure. It sets up the next steps, where you'll call `play_round` more than once."],
  "Move the round (announcement, loop, attempt counting) into `play_round(secret)` that returns `attempts`. The main code picks the secret, calls it and prints the result.",
  v5, [dict(py="callable(play_round)", msg="There's a `play_round` function."), dict(py="attempts == secret", msg="It returns the number of attempts."),
       dict(outHas="You got it in", msg="The game still finishes with the attempts message.")], stdin=GUESSES, core="s1m3"))
v6 = v5.replace('\n\nsecret = random.randint(1, 100)', '\n\ndef rating(attempts):\n    if attempts <= 5:\n        return "Amazing"\n    if attempts <= 10:\n        return "Good"\n    return "Keep practising"\n\n\nsecret = random.randint(1, 100)').replace('print(f"You got it in {attempts} attempts.")', 'print(f"You got it in {attempts} attempts. {rating(attempts)}")')
S.append(step("ng6", "Rate the player",
  ["Add some personality: `rating(attempts)` turns a number into a verdict. A good guesser needs at most 7 tries for 1–100, because halving the range each time (**binary search**) gets there in ⌈log₂ 100⌉ = 7 guesses."],
  "Write `rating(attempts)`: `\"Amazing\"` for 5 or fewer, `\"Good\"` for 10 or fewer, otherwise `\"Keep practising\"`. Add the rating to the final message.",
  v6, [dict(py='rating(1) == "Amazing" and rating(5) == "Amazing"', msg="5 or fewer is Amazing."), dict(py='rating(6) == "Good" and rating(10) == "Good"', msg="6 to 10 is Good."),
       dict(py='rating(11) == "Keep practising"', msg="More than 10 is Keep practising."), dict(py="rating(secret) in _out", msg="The final message includes the rating.")], stdin=GUESSES, core="s2m3"))
v7 = v6.replace('secret = random.randint(1, 100)\nattempts = play_round(secret)\nprint(f"You got it in {attempts} attempts. {rating(attempts)}")\n',
  'best = None\nwhile True:\n    secret = random.randint(1, 100)\n    attempts = play_round(secret)\n    print(f"You got it in {attempts} attempts. {rating(attempts)}")\n    if best is None or attempts < best:\n        best = attempts\n        print("New best score.")\n    again = input("Play again? (y/n) ")\n    if again.strip().lower() != "y":\n        break\nprint(f"Best score: {best} attempts. Thanks for playing.")\n')
S.append(step("ng7", "Play again and keep a best score",
  ["Wrap the round in an outer loop that asks `Play again? (y/n)`. Track the best (lowest) score across rounds.",
   "`best = None` means *no score yet*; `if best is None or attempts < best` handles the first round and every later one. `.strip().lower()` accepts `Y`, ` y ` and `y` alike."],
  "Loop rounds until the player answers anything other than `y`. Keep `best` (fewest attempts so far), print `New best score.` when it improves, and finish with `Best score: N attempts. Thanks for playing.`",
  v7, [dict(outHas="Play again?", msg="The game asks `Play again? (y/n)`."), dict(py="best == attempts == secret", msg="`best` holds the best score."),
       dict(outHas="Best score:", msg="It finishes with the best score.")], stdin=GUESSES + ["n"]))
project(id="guessing-game", title="Number Guessing Game", lang="python", level="Beginner", hours="1 h", hue="#38d3f0", icon="target", art="? 42 ?",
  tagline="Your first complete Python game: random numbers, loops, input and a best score.",
  desc=["The perfect first Python project. You'll go from one line to a polished little game, meeting variables, functions, `while` loops, user input, error handling and refactoring along the way.",
        "Every concept arrives exactly when the game needs it, so it sticks."],
  final="A command-line game that picks a secret number, tells you whether each guess is too high or too low, survives typos, rates your skill and keeps your best score across rounds.",
  skills=["modules (random)", "functions", "while loops", "input()", "try/except", "refactoring", "binary search intuition"],
  prereq="the first half of **Python from Zero** (print, variables, if).", core=["s1m2", "s1m3", "s1m5"],
  stretch=["Add difficulty levels (1–10, 1–100, 1–1000) with a guess limit.", "Make the computer guess *your* number using binary search.", "Save the best score to a file with `open()`."],
  demo_pre="import random\nrandom.seed(7)\n", demo_stdin=["50", "hello", "25", "37", "43", "40", "42", "n"],
  milestones=[milestone("The rules", "A secret number and a function that judges guesses.", S[0:2]),
              milestone("The game loop", "Read guesses until the player wins, without crashing on typos.", S[2:4]),
              milestone("A proper game", "Clean functions, a rating and replays with a best score.", S[4:7])])

# =============================================================================================== TEXT ADVENTURE
S = []
ROOMS = '''rooms = {
    "hall": {"description": "A dusty entrance hall.", "exits": {"north": "library", "east": "kitchen"}, "item": None},
    "library": {"description": "Shelves of old books. A cold draught comes from the east.", "exits": {"south": "hall", "east": "vault"}, "item": "lamp"},
    "kitchen": {"description": "A cold kitchen. Something glints in the sink.", "exits": {"west": "hall"}, "item": "key"},
    "vault": {"description": "A heavy iron vault.", "exits": {"west": "library"}, "item": None},
}
'''
C = Code("# The Vault: a text adventure\n\n" + ROOMS)
S.append(step("ta1", "A world made of dictionaries",
  ["A text adventure is a map of rooms. Each room has a description, exits (direction → room name) and maybe an item. Nested **dictionaries** model that perfectly: `rooms[\"hall\"][\"exits\"][\"north\"]` is `\"library\"`.",
   "`None` means *nothing here*. It's Python's way of saying a value is deliberately empty."],
  "Create the `rooms` dictionary with these four rooms exactly: **hall** (exits north → library, east → kitchen), **library** (south → hall, east → vault, item `lamp`), **kitchen** (west → hall, item `key`) and **vault** (west → library). Every room has `description`, `exits` and `item` keys.",
  C.text, [dict(py='set(rooms) == {"hall", "library", "kitchen", "vault"}', msg="The four rooms exist."),
           dict(py='all(set(r) >= {"description", "exits", "item"} for r in rooms.values())', msg="Each room has `description`, `exits` and `item`."),
           dict(py='rooms["hall"]["exits"] == {"north": "library", "east": "kitchen"} and rooms["library"]["exits"] == {"south": "hall", "east": "vault"}', msg="The hall and library exits are right."),
           dict(py='rooms["kitchen"]["item"] == "key" and rooms["library"]["item"] == "lamp" and rooms["hall"]["item"] is None', msg="The key is in the kitchen and the lamp in the library."),
           dict(py='all(dest in rooms for r in rooms.values() for dest in r["exits"].values())', msg="Every exit leads to a room that exists.")],
  starter="# The Vault: a text adventure\n\n", core="s1m4"))
C.add('''

def describe(name):
    room = rooms[name]
    text = f"{room['description']} Exits: {', '.join(sorted(room['exits']))}."
    if room["item"]:
        text += f" You see a {room['item']}."
    return text
''')
S.append(step("ta2", "Describe a room",
  ["`describe(name)` builds the text the player reads. Sorting the exit names (`sorted(...)`) makes the output predictable, and `', '.join(...)` puts commas between them.",
   "Inside an f-string that uses double quotes, use single quotes for dictionary keys: `f\"{room['description']}\"`."],
  "Write `describe(name)` returning the description, then ` Exits: ` and the sorted exit names joined by commas, ending with a full stop. If the room has an item, add ` You see a <item>.`",
  C.text, [dict(py='describe("hall") == "A dusty entrance hall. Exits: east, north."', msg="`describe(\"hall\")` is exactly `A dusty entrance hall. Exits: east, north.`"),
           dict(py='describe("kitchen").endswith("Exits: west. You see a key.")', msg="Rooms with an item mention it."),
           dict(py='describe("library").startswith("Shelves of old books.")', msg="Each room starts with its own description.")], core="s1m3"))
C.add('''

def move(current, direction):
    exits = rooms[current]["exits"]
    if direction not in exits:
        print("You can't go that way.")
        return current
    return exits[direction]
''')
S.append(step("ta3", "Move between rooms",
  ["Moving is a dictionary lookup: if the direction is one of the current room's exits, return where it leads. If not, tell the player and stay put by returning the current room.",
   "`in` checks whether a key exists: `\"north\" in exits`."],
  "Write `move(current, direction)` that returns the new room's name, or prints `You can't go that way.` and returns `current` when there's no such exit.",
  C.text, [dict(py='move("hall", "north") == "library"', msg="Going north from the hall reaches the library."), dict(py='move("library", "south") == "hall"', msg="Going south from the library reaches the hall."),
           dict(py='move("hall", "west") == "hall" and move("kitchen", "north") == "kitchen"', msg="A missing exit keeps you where you are.")]))
C.add('''

inventory = []


def take(name):
    room = rooms[name]
    if room["item"] is None:
        return "There is nothing here."
    item = room["item"]
    inventory.append(item)
    room["item"] = None
    return f"You take the {item}."
''')
S.append(step("ta4", "Pick things up",
  ["The player's bag is a list, `inventory`. Taking an item moves it out of the room (set the room's item to `None`) and into the list.",
   "Lists and dictionaries are **mutable**: changing `rooms[name][\"item\"]` inside the function changes the one shared world, not a copy."],
  "Create an empty `inventory` list. Write `take(name)`: if the room has no item return `There is nothing here.`; otherwise add the item to `inventory`, remove it from the room and return `You take the <item>.`",
  C.text, [dict(py='take("kitchen") == "You take the key." and "key" in inventory and rooms["kitchen"]["item"] is None', msg="Taking the key moves it into the inventory."),
           dict(py='take("hall") == "There is nothing here."', msg="Empty rooms have nothing to take."),
           dict(py='take("kitchen") == "There is nothing here."', msg="An item can only be taken once.")], core="s1m4"))
C.sub('''    if direction not in exits:
        print("You can't go that way.")
        return current
    return exits[direction]''', '''    if direction not in exits:
        print("You can't go that way.")
        return current
    destination = exits[direction]
    if destination == "vault" and "key" not in inventory:
        print("The vault is locked. You need a key.")
        return current
    return destination''')
C.sub('''

def move(current, direction):''', '''

inventory = []


def move(current, direction):''')
C.sub('''

inventory = []


def take(name):''', '''

def take(name):''')
S.append(step("ta5", "A locked door",
  ["Puzzles make it a game. The vault only opens if the key is in your inventory. That's one extra condition inside `move`.",
   "Because `move` now reads `inventory`, define `inventory` *before* `move` in the file. Python looks up names when the function runs, but defining things before their first use keeps code easy to follow."],
  "Make `move` refuse to enter the vault without the key: print `The vault is locked. You need a key.` and stay put. Move `inventory = []` above `move`.",
  C.text, [dict(py='move("library", "east") == "library"', msg="Without the key you can't enter the vault."),
           dict(src="The vault is locked", msg="The player is told the vault is locked."),
           dict(py='(take("kitchen"), move("library", "east"))[1] == "vault"', msg="With the key, the vault opens.")]))
C.add('''

def handle(command, current):
    words = command.split()
    if not words:
        return current
    verb = words[0]
    if verb == "go" and len(words) > 1:
        new = move(current, words[1])
        if new != current:
            print(describe(new))
        return new
    if verb == "take":
        print(take(current))
    elif verb == "look":
        print(describe(current))
    elif verb == "inventory":
        print("You carry: " + (", ".join(inventory) if inventory else "nothing"))
    else:
        print("I don't understand that.")
    return current
''')
S.append(step("ta6", "Understand commands",
  ["Players type commands like `go north` or `take`. `command.split()` breaks text into words: `[\"go\", \"north\"]`. The first word (the **verb**) decides what happens.",
   "`handle` always returns the room the player ends up in, so the game loop can just write `current = handle(command, current)`."],
  "Write `handle(command, current)` supporting `go <direction>` (print the new room's description when you move), `take`, `look`, `inventory` (`You carry: ...` or `nothing`), and `I don't understand that.` for anything else. Return the current room.",
  C.text, [dict(py='handle("go north", "hall") == "library"', msg="`go north` from the hall returns `library`."), dict(py='handle("dance", "hall") == "hall"', msg="Unknown commands leave you in place."),
           dict(py='handle("take", "kitchen") == "kitchen" and "key" in inventory', msg="`take` picks up the room's item."), dict(py='handle("", "hall") == "hall"', msg="An empty command does nothing.")]))
C.add('''

current = "hall"
print(describe(current))
while True:
    command = input("> ").strip().lower()
    if command == "quit":
        print("Bye.")
        break
    current = handle(command, current)
    if current == "vault":
        print("The vault swings open. Gold everywhere. You win.")
        break
''')
S.append(step("ta7", "The game loop",
  ["Tie it together: start in the hall, then loop: read a command, handle it, and check for the win. `quit` ends the game early.",
   "Normalising input with `.strip().lower()` means `GO North ` works the same as `go north`."],
  "Start at `hall`, print its description, then loop reading commands with `input(\"> \")` until `quit` (print `Bye.`) or until the player reaches the vault (print a message ending in `You win.`).",
  C.text, [dict(outHas="You win.", msg="Reaching the vault wins the game."), dict(py='current == "vault"', msg="The game ends in the vault."),
           dict(outHas="The vault is locked", msg="Trying the vault before finding the key is refused.")],
  stdin=["go north", "go east", "go south", "GO East ", "take", "inventory", "go west", "go north", "go east"]))
project(id="text-adventure", title="Text Adventure: The Vault", lang="python", level="Beginner", hours="1.5 h", hue="#a3e635", icon="compass", art="> go north",
  tagline="Explore rooms, find the key, open the vault. Built entirely from dictionaries and functions.",
  desc=["Classic text adventures like Zork were built from exactly what you'll use here: a map stored as data, small functions that change it, and a loop that reads commands.",
        "It's the most fun way to get comfortable with nested dictionaries, lists and parsing text."],
  final="A playable adventure with four rooms, an item to find, a locked vault and a command parser that understands `go`, `take`, `look`, `inventory` and `quit`.",
  skills=["nested dictionaries", "lists", "functions", "string parsing", "game loops", "mutable state"],
  prereq="**Python from Zero**, or the Number Guessing Game.", core=["s1m4", "s1m3"],
  stretch=["Add more rooms and a second puzzle (the lamp could reveal a hidden exit).", "Load the world from a JSON file.", "Add a `drop` command and a score.", "Save and load the game."],
  demo_stdin=["look", "go north", "go east", "go south", "go east", "take", "go west", "go north", "go east"],
  milestones=[milestone("The world", "Rooms as data, described in words.", S[0:2]), milestone("Moving and items", "Walk around, pick things up, meet a locked door.", S[2:5]),
              milestone("The game", "Understand commands and run the game loop.", S[5:7])])

# =============================================================================================== PASSWORD TOOLKIT
S = []
C = Code('# Password toolkit\n\n\ndef check_length(password):\n    return len(password) >= 8\n')
S.append(step("pw1", "The length rule",
  ["Length is the single biggest factor in password strength: every extra character multiplies the guesses an attacker needs.",
   "A function that answers a yes/no question returns a **boolean**. `len(password) >= 8` already *is* `True` or `False`, so return it directly instead of writing an `if`."],
  "Write `check_length(password)` that returns `True` when the password has at least 8 characters.",
  C.text, [dict(py='check_length("abcdefgh") is True', msg="8 characters passes."), dict(py='check_length("abcdefg") is False', msg="7 characters fails."), dict(py='check_length("") is False', msg="An empty password fails.")],
  starter="# Password toolkit\n", core="s1m3"))
C.add('''

def strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(not c.isalnum() for c in password):
        score += 1
    return score
''')
S.append(step("pw2", "A strength score",
  ["Score a password out of 6: one point each for 8+ characters, 12+ characters, a lowercase letter, an uppercase letter, a digit and a symbol.",
   "`any(c.isupper() for c in password)` asks *is there at least one uppercase character?* String methods like `isupper`, `isdigit` and `isalnum` (letter or digit) do the per-character test."],
  "Write `strength(password)` returning the score from 0 to 6 using those six rules. A symbol is any character that isn't a letter or digit.",
  C.text, [dict(py='strength("abc") == 1', msg="`abc` scores 1 (lowercase only)."), dict(py='strength("Password1!") == 5', msg="`Password1!` scores 5."),
           dict(py='strength("Tr0ub4dor&3xyz") == 6', msg="`Tr0ub4dor&3xyz` scores the full 6."), dict(py='strength("") == 0', msg="An empty password scores 0.")],
  ref=("Python docs: built-in any()", "https://docs.python.org/3/library/functions.html#any")))
C.add('''

def label(score):
    if score <= 2:
        return "Weak"
    if score <= 4:
        return "Medium"
    return "Strong"
''')
S.append(step("pw3", "Weak, medium or strong",
  ["Numbers are for programs; words are for people. Map the score to a label: 0–2 is `Weak`, 3–4 is `Medium`, 5–6 is `Strong`."],
  "Write `label(score)` returning `\"Weak\"`, `\"Medium\"` or `\"Strong\"`.",
  C.text, [dict(py='[label(s) for s in range(7)] == ["Weak", "Weak", "Weak", "Medium", "Medium", "Strong", "Strong"]', msg="Scores 0–6 map to the right labels."),
           dict(py='label(strength("Password1!")) == "Strong"', msg="`Password1!` is labelled Strong.")]))
C.add('''

def feedback(password):
    tips = []
    if len(password) < 8:
        tips.append("Use at least 8 characters.")
    if len(password) < 12:
        tips.append("Use 12 or more characters for a strong password.")
    if not any(c.islower() for c in password):
        tips.append("Add a lowercase letter.")
    if not any(c.isupper() for c in password):
        tips.append("Add an uppercase letter.")
    if not any(c.isdigit() for c in password):
        tips.append("Add a number.")
    if all(c.isalnum() for c in password):
        tips.append("Add a symbol such as ! or #.")
    return tips
''')
S.append(step("pw4", "Helpful feedback",
  ["A score alone doesn't help anyone fix their password. Return a **list** of tips, one per rule that isn't met, so the caller can show them however it likes.",
   "Note `all(c.isalnum() for c in password)`: *every character is a letter or digit* means there's no symbol."],
  "Write `feedback(password)` returning a list of tips, in this order and wording, for each failed rule: `Use at least 8 characters.`, `Use 12 or more characters for a strong password.`, `Add a lowercase letter.`, `Add an uppercase letter.`, `Add a number.`, `Add a symbol such as ! or #.`",
  C.text, [dict(py='feedback("Password1!") == ["Use 12 or more characters for a strong password."]', msg="`Password1!` only needs more length."),
           dict(py='len(feedback("")) == 6 and feedback("")[0] == "Use at least 8 characters."', msg="An empty password gets all six tips."),
           dict(py='feedback("Tr0ub4dor&3xyz") == []', msg="A perfect password gets no tips.")]))
C.sub('''def strength(password):
    score = 0''', '''COMMON = {"password", "123456", "123456789", "qwerty", "password1", "111111", "letmein", "iloveyou", "admin", "welcome"}


def strength(password):
    if password.lower() in COMMON:
        return 0
    score = 0''')
S.append(step("pw5", "Reject common passwords",
  ["`Password1` ticks several boxes, but it's one of the first guesses any attacker tries. Real checkers compare against lists of leaked passwords.",
   "A **set** is the right container: `x in my_set` is instant even for millions of entries, while searching a list checks every item."],
  "Create a set `COMMON` of common passwords (include at least `password`, `password1`, `123456`, `qwerty`). Make `strength` return 0 for any password whose lowercase form is in it.",
  C.text, [dict(py='isinstance(COMMON, set) and {"password", "password1", "123456", "qwerty"} <= COMMON', msg="`COMMON` is a set containing the common passwords."),
           dict(py='strength("Password1") == 0 and strength("QWERTY") == 0', msg="Common passwords score 0, whatever their case."),
           dict(py='strength("Password1!") == 5', msg="Other passwords are scored as before.")], core="s2m2"))
C.text = C.text.replace('# Password toolkit\n', '# Password toolkit\nimport secrets\nimport string\n', 1)
C.add('''

def generate(length=16):
    pools = [string.ascii_lowercase, string.ascii_uppercase, string.digits, "!@#$%^&*-_=+?"]
    chars = [secrets.choice(pool) for pool in pools]
    everything = "".join(pools)
    chars += [secrets.choice(everything) for _ in range(length - len(pools))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)
''')
S.append(step("pw6", "Generate strong passwords",
  ["For anything security-related use the `secrets` module, not `random`: `random` is predictable by design, `secrets` is built for this.",
   "To guarantee every character class appears, pick one character from each pool first, fill the rest from all pools, then shuffle so the guaranteed ones aren't always at the start. `length=16` is a **default argument**."],
  "Import `secrets` and `string`. Write `generate(length=16)` returning a random password of that length that always contains a lowercase letter, an uppercase letter, a digit and a symbol.",
  C.text, [dict(py="len(generate()) == 16 and len(generate(24)) == 24", msg="The length is 16 by default and adjustable."),
           dict(py="all(strength(generate()) == 6 for _ in range(20))", msg="Generated passwords always score 6."),
           dict(py="len({generate() for _ in range(10)}) == 10", msg="Every password is different."), dict(src="import secrets", msg="You use the `secrets` module.")],
  ref=("Python docs: secrets", "https://docs.python.org/3/library/secrets.html")))
C.add('''

def report(passwords):
    for password in passwords:
        score = strength(password)
        print(f"{password:<24} {score}/6  {label(score)}")
        for tip in feedback(password):
            print(f"    - {tip}")


report(["hello", "Password1", "Password1!", "correct-Horse-7-battery"])
print("Suggested:", generate())
''')
S.append(step("pw7", "A strength report",
  ["Finish with a tool people can run: check a list of passwords and print a neat report. `f\"{password:<24}\"` pads text to 24 characters, which lines the columns up.",
   "Reusing your own functions (`strength`, `label`, `feedback`, `generate`) is the payoff for building small pieces first."],
  "Write `report(passwords)` printing, for each password, the password padded to 24 characters, `score/6` and the label, followed by each tip on its own indented line. Call it on a few passwords and print a suggested password.",
  C.text, [dict(outRe="hello\\s+1/6\\s+Weak", msg="`hello` is reported as `1/6  Weak`."), dict(outRe="Password1\\s+0/6\\s+Weak", msg="`Password1` is caught as common."),
           dict(outHas="- Add a number.", msg="Tips are listed under each password."), dict(outHas="Suggested:", msg="A generated password is suggested.")]))
project(id="password-toolkit", title="Password Toolkit", lang="python", level="Beginner", hours="1 h", hue="#fbbf24", icon="key", art="******",
  tagline="Score passwords, explain how to fix them, block common ones and generate strong replacements.",
  desc=["You'll build the kind of password checker you see on sign-up forms, plus a generator, and learn why some approaches are secure and others aren't.",
        "It's a compact tour of strings, booleans, `any`/`all`, sets and the standard library, with a real security lesson attached."],
  final="A toolkit that scores any password out of 6, labels it, lists exactly what to improve, rejects leaked favourites and generates strong passwords with the `secrets` module.",
  skills=["string methods", "booleans", "any() and all()", "lists", "sets", "secrets module", "f-string formatting"],
  prereq="**Python from Zero**.", core=["s1m3", "s2m2", "s7m4"],
  stretch=["Estimate crack time from the size of the character pool and the length.", "Load the common-password list from a file (millions of entries).", "Generate memorable passphrases from a word list."],
  demo_stdin=[],
  milestones=[milestone("Scoring", "Rules, a 0–6 score and a label.", S[0:3]), milestone("Helping people", "Explain what to fix and block common passwords.", S[3:5]),
              milestone("Generating and reporting", "Secure generation and a printed report.", S[5:7])])

# =============================================================================================== BANK ACCOUNT SYSTEM
S = []
C = Code('''# Bank account system


class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
''')
S.append(step("bk1", "Your first class",
  ["A **class** is a blueprint for objects that bundle data with behaviour. `Account(\"Ada\")` creates one account object; each has its own `owner` and `balance`.",
   "`__init__` runs when an object is created. `self` is the object being built, so `self.balance = balance` stores the value *on that object*."],
  "Define a class `Account` whose `__init__(self, owner, balance=0)` stores `owner` and `balance` on the object.",
  C.text, [dict(py='Account("Ada").owner == "Ada" and Account("Ada").balance == 0', msg="A new account stores its owner and starts at 0."),
           dict(py='Account("Bo", 50).balance == 50', msg="A starting balance can be given."),
           dict(py='(lambda a, b: (setattr(a, "balance", 99), b.balance)[1])(Account("A"), Account("B")) == 0', msg="Each account has its own balance.")],
  starter="# Bank account system\n", core="s1m6", ref=("Python tutorial: Classes", "https://docs.python.org/3/tutorial/classes.html")))
C.add('''
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive.")
        self.balance += amount
        return self.balance
''')
S.append(step("bk2", "Deposits that can't be faked",
  ["A **method** is a function that belongs to a class; it always receives `self` first. `account.deposit(50)` changes that account's balance.",
   "Protect the rules: a deposit of 0 or less is a bug, so `raise ValueError(...)` stops it loudly instead of silently corrupting the balance."],
  "Add `deposit(self, amount)` that raises `ValueError` for amounts of 0 or less, otherwise adds to the balance and returns the new balance.",
  C.text, [dict(py='(lambda a: (a.deposit(50), a.deposit(25))[1])(Account("Ada")) == 75', msg="Deposits add up and return the new balance."),
           dict(py='_raises(lambda: Account("Ada").deposit(0), ValueError) and _raises(lambda: Account("Ada").deposit(-5), ValueError)', msg="Zero or negative deposits raise `ValueError`.")]))
C.text = C.text.replace('# Bank account system\n', '# Bank account system\n\n\nclass InsufficientFunds(Exception):\n    pass\n', 1)
C.add('''
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive.")
        if amount > self.balance:
            raise InsufficientFunds(f"{self.owner} has only {self.balance:.2f}.")
        self.balance -= amount
        return self.balance
''')
S.append(step("bk3", "Withdrawals and your own exception",
  ["Withdrawing more than the balance isn't a typo, it's a business rule. Give it its own exception type so callers can handle it specifically: `class InsufficientFunds(Exception): pass`.",
   "Custom exceptions make errors self-describing: `except InsufficientFunds:` reads like the business rule it enforces."],
  "Define `InsufficientFunds` (a subclass of `Exception`). Add `withdraw(self, amount)`: `ValueError` for 0 or less, `InsufficientFunds` if it exceeds the balance, otherwise subtract and return the new balance.",
  C.text, [dict(py='Account("Ada", 100).withdraw(30) == 70', msg="Withdrawing reduces the balance."),
           dict(py='_raises(lambda: Account("Ada", 10).withdraw(11), InsufficientFunds)', msg="Overdrawing raises `InsufficientFunds`."),
           dict(py='(lambda a: (_raises(lambda: a.withdraw(20), InsufficientFunds), a.balance)[1])(Account("Ada", 10)) == 10', msg="A refused withdrawal leaves the balance unchanged."),
           dict(py='issubclass(InsufficientFunds, Exception) and _raises(lambda: Account("A", 5).withdraw(0), ValueError)', msg="Zero withdrawals raise `ValueError`.")], core="s1m5"))
C.sub('''        self.balance = balance
''', '''        self.balance = balance
        self.history = []
''')
C.sub('''        self.balance += amount
        return self.balance''', '''        self.balance += amount
        self.history.append(("deposit", amount))
        return self.balance''')
C.sub('''        self.balance -= amount
        return self.balance''', '''        self.balance -= amount
        self.history.append(("withdraw", amount))
        return self.balance''')
C.add('''
    def __str__(self):
        return f"Account({self.owner}, balance={self.balance:.2f})"
''')
S.append(step("bk4", "History and a readable account",
  ["Banks never just change a number; they keep a record. Append a tuple like `(\"deposit\", 50)` to `self.history` on every successful transaction.",
   "`__str__` is a **special method**: it decides what `print(account)` shows. Format money with two decimals: `{self.balance:.2f}`."],
  "Give each account a `history` list and record `(\"deposit\", amount)` / `(\"withdraw\", amount)` after each successful transaction. Add `__str__` returning `Account(<owner>, balance=<balance with 2 decimals>)`.",
  C.text, [dict(py='(lambda a: (a.deposit(50), a.withdraw(20), a.history)[2])(Account("Ada")) == [("deposit", 50), ("withdraw", 20)]', msg="Transactions are recorded in order."),
           dict(py='(lambda a: (_raises(lambda: a.withdraw(5), InsufficientFunds), a.history)[1])(Account("Ada")) == []', msg="Refused transactions aren't recorded."),
           dict(py='str(Account("Ada", 12.5)) == "Account(Ada, balance=12.50)"', msg="`str(account)` shows `Account(Ada, balance=12.50)`.")]))
C.add('''

class SavingsAccount(Account):
    def __init__(self, owner, balance=0, rate=0.02):
        super().__init__(owner, balance)
        self.rate = rate

    def add_interest(self):
        interest = round(self.balance * self.rate, 2)
        if interest > 0:
            self.deposit(interest)
        return interest
''')
S.append(step("bk5", "Inheritance: a savings account",
  ["A savings account *is an* account with one extra feature. **Inheritance** says that in code: `class SavingsAccount(Account):` gets every method of `Account` for free.",
   "`super().__init__(owner, balance)` runs the parent's setup, then you add what's new (`self.rate`). Reusing `self.deposit` for interest keeps the history correct automatically."],
  "Create `SavingsAccount(Account)` with an extra `rate` (default `0.02`) and `add_interest()`, which deposits `balance * rate` rounded to 2 decimals (only if it's above 0) and returns it.",
  C.text, [dict(py='(lambda s: (s.add_interest(), s.balance)[1])(SavingsAccount("Ada", 1000)) == 1020', msg="2% interest on 1000 adds 20."),
           dict(py='SavingsAccount("Ada", 100, rate=0.05).add_interest() == 5', msg="The rate can be changed."),
           dict(py='isinstance(SavingsAccount("Ada"), Account) and SavingsAccount("Ada", 50).withdraw(10) == 40', msg="Savings accounts are accounts: withdraw still works."),
           dict(py='SavingsAccount("Ada").add_interest() == 0', msg="No interest on an empty account (and no error).")], core="s1m6"))
C.add('''

class Bank:
    def __init__(self):
        self.accounts = {}

    def open(self, owner, kind="checking"):
        if owner in self.accounts:
            raise ValueError(f"{owner} already has an account.")
        account = SavingsAccount(owner) if kind == "savings" else Account(owner)
        self.accounts[owner] = account
        return account

    def transfer(self, source, target, amount):
        sender = self.accounts[source]
        receiver = self.accounts[target]
        sender.withdraw(amount)
        receiver.deposit(amount)

    def total(self):
        return sum(account.balance for account in self.accounts.values())
''')
S.append(step("bk6", "A bank that holds accounts",
  ["Objects can contain other objects. A `Bank` keeps a dictionary from owner name to account, and offers operations that span accounts.",
   "Order matters in `transfer`: withdraw first. If that raises `InsufficientFunds`, the deposit never happens, so money can't be created out of nothing."],
  "Write `Bank` with `open(owner, kind=\"checking\")` (a `SavingsAccount` for `\"savings\"`, `ValueError` for duplicates), `transfer(source, target, amount)` and `total()` (sum of all balances).",
  C.text, [dict(py='(lambda b: (b.open("Ada").deposit(100), b.open("Bo"), b.transfer("Ada", "Bo", 40), (b.accounts["Ada"].balance, b.accounts["Bo"].balance))[3])(Bank()) == (60, 40)', msg="Transfers move money between accounts."),
           dict(py='(lambda b: (b.open("Ada").deposit(10), b.open("Bo"), _raises(lambda: b.transfer("Ada", "Bo", 50), InsufficientFunds), b.total())[3])(Bank()) == 10', msg="A failed transfer changes nothing."),
           dict(py='isinstance(Bank().open("Cy", "savings"), SavingsAccount)', msg="`open(..., \"savings\")` creates a savings account."),
           dict(py='(lambda b: (b.open("Ada"), _raises(lambda: b.open("Ada"), ValueError))[1])(Bank())', msg="Opening a second account for the same person raises `ValueError`.")]))
C.sub('''    def __str__(self):''', '''    def statement(self):
        lines = [f"Statement for {self.owner}"]
        for kind, amount in self.history:
            sign = "+" if kind == "deposit" else "-"
            lines.append(f"  {kind:<10}{sign}{amount:>9.2f}")
        lines.append(f"  {'balance':<10}{self.balance:>10.2f}")
        return "\\n".join(lines)

    def __str__(self):''')
C.add('''

bank = Bank()
bank.open("Ada").deposit(250)
bank.open("Grace", "savings").deposit(1000)
bank.transfer("Ada", "Grace", 75.5)
bank.accounts["Grace"].add_interest()
for account in bank.accounts.values():
    print(account)
print(bank.accounts["Grace"].statement())
print(f"Total held: {bank.total():.2f}")
''')
S.append(step("bk7", "Statements and a demo run",
  ["Finish with output a customer would recognise. Format numbers in columns: `{amount:>9.2f}` right-aligns to 9 characters with 2 decimals.",
   "Then write a short script at the bottom that uses everything: open accounts, deposit, transfer, add interest and print."],
  "Add `statement()` to `Account`, returning `Statement for <owner>`, one line per transaction (`kind`, then `+` or `-` and the amount), and a final balance line. Then open two accounts, move some money, add interest and print the accounts, a statement and the bank's total.",
  C.text, [dict(py='"Statement for Ada" in Account("Ada").statement()', msg="Statements start with `Statement for <owner>`."),
           dict(py='(lambda a: (a.deposit(10), a.withdraw(4), a.statement().splitlines())[2])(Account("Ada"))[1:3] == ["  deposit   +    10.00", "  withdraw  -     4.00"]', msg="Each transaction is one aligned line with a sign."),
           dict(outHas="Total held:", msg="The demo prints the bank's total."), dict(outHas="Account(Ada, balance=174.50)", msg="The demo prints each account.")]))
project(id="bank-system", title="Bank Account System", lang="python", level="Intermediate", hours="2 h", hue="#34d399", icon="building", art="$ 1,020.00",
  tagline="Object-oriented Python done properly: classes, rules, custom exceptions and inheritance.",
  desc=["Banking is the classic way to learn object-oriented programming because the rules are clear and mistakes are obvious: money must never appear or vanish.",
        "You'll build accounts that protect their own rules, a savings account that inherits from them, and a bank that coordinates transfers safely."],
  final="A small banking library with accounts, deposits, withdrawals, transaction history, savings interest, safe transfers between accounts and printed statements.",
  skills=["classes and objects", "methods", "raising exceptions", "custom exceptions", "special methods (__str__)", "inheritance and super()", "composition"],
  prereq="**Python from Zero** and comfort writing functions.", core=["s1m6", "s1m5", "s5m1"],
  stretch=["Store money as integer cents (or `Decimal`) to avoid floating-point errors.", "Add a monthly fee to checking accounts.", "Persist the bank to a JSON file.", "Write pytest tests for every rule."],
  demo_stdin=[],
  milestones=[milestone("An account", "A class with data and a protected deposit.", S[0:2]), milestone("Rules and records", "Withdrawals, custom errors and a history.", S[2:4]),
              milestone("A bank", "Inheritance, transfers and statements.", S[4:7])])

# =============================================================================================== TIC-TAC-TOE AI
S = []
C = Code('''# Tic-tac-toe with an unbeatable AI


def show(board):
    rows = [" | ".join(board[i:i + 3]) for i in (0, 3, 6)]
    return "\\n---------\\n".join(rows)
''')
S.append(step("tt1", "Draw the board",
  ["Represent the board as a list of 9 strings, indexes 0 to 8 reading left to right, top to bottom. Each square is `\"X\"`, `\"O\"` or `\" \"` (empty).",
   "Slicing `board[i:i + 3]` gives one row; `\" | \".join(row)` draws it. Building a string (instead of printing inside the function) makes it testable."],
  "Write `show(board)` returning the three rows joined by `\\n---------\\n`, with squares in a row separated by ` | `.",
  C.text, [dict(py='show(list("XOXOXOXOX")).splitlines() == ["X | O | X", "---------", "O | X | O", "---------", "X | O | X"]', msg="A full board is drawn as three rows with separators."),
           dict(py='show([" "] * 9).count("|") == 6', msg="An empty board still shows its grid.")],
  starter="# Tic-tac-toe with an unbeatable AI\n", core="s1m4"))
C.add('''

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def winner(board):
    for a, b, c in LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None
''')
S.append(step("tt2", "Who won?",
  ["There are only 8 winning lines: 3 rows, 3 columns, 2 diagonals. List them as tuples of indexes and check each one.",
   "Python allows chained comparisons: `board[a] == board[b] == board[c]` means both equalities hold. Remember to ignore three *empty* squares in a row."],
  "Define `LINES` (the 8 winning index triples) and `winner(board)` returning `\"X\"`, `\"O\"` or `None`.",
  C.text, [dict(py='winner(list("XXX      ")) == "X" and winner(list("O  O  O  ")) == "O"', msg="Rows and columns count."), dict(py='winner(list("X   X   X")) == "X" and winner(list("  O O O  ")) == "O"', msg="Both diagonals count."),
           dict(py='winner([" "] * 9) is None and winner(list("XOXXOOOXX")) is None', msg="Empty and drawn boards have no winner.")]))
C.add('''

def available(board):
    return [i for i, square in enumerate(board) if square == " "]


def game_over(board):
    return winner(board) is not None or not available(board)
''')
S.append(step("tt3", "Free squares and game over",
  ["`enumerate(board)` gives index and value together, perfect for a **list comprehension** that collects the empty indexes.",
   "The game is over when someone has won or there's nowhere left to play. An empty list is falsy, so `not available(board)` means *board full*."],
  "Write `available(board)` (the indexes of empty squares) and `game_over(board)`.",
  C.text, [dict(py='available(list("X O  X   ")) == [1, 3, 4, 6, 7, 8]', msg="`available` lists empty squares in order."), dict(py='game_over(list("XXX      ")) and game_over(list("XOXXOOOXX"))', msg="A win or a full board ends the game."),
           dict(py='not game_over([" "] * 9)', msg="An empty board isn't over.")], core="s1m4"))
C.add('''

def minimax(board, player):
    win = winner(board)
    if win == "X":
        return 1
    if win == "O":
        return -1
    if not available(board):
        return 0
    scores = []
    for i in available(board):
        board[i] = player
        scores.append(minimax(board, "O" if player == "X" else "X"))
        board[i] = " "
    return max(scores) if player == "X" else min(scores)
''')
S.append(step("tt4", "Minimax: looking ahead",
  ["How does a computer play perfectly? It imagines **every** possible future. **Minimax** scores a finished game +1 if X won, −1 if O won and 0 for a draw. X picks the move with the highest score, O the lowest, assuming both play perfectly.",
   "It's **recursion**: to score a position, try each move, score the resulting position with `minimax` itself, then undo the move. Base cases are finished games."],
  "Write `minimax(board, player)` returning +1, −1 or 0: the result with perfect play from here, where `player` moves next. Try each free square, recurse with the other player, undo the move, and return the max (X) or min (O).",
  C.text, [dict(py='minimax(list("XX OO    "), "X") == 1', msg="X to move with two in a row: X wins (+1)."), dict(py='minimax(list("XX OO    "), "O") == -1', msg="O to move there: O wins first (−1)."),
           dict(py='minimax(list("XOXXOOOX "), "X") == 0', msg="A position that can only end in a draw scores 0."),
           dict(py='minimax(list("X   O    "), "X") == 0', msg="An even early position is a draw with perfect play.")], core="s2m6",
  ref=("Wikipedia: Minimax", "https://en.wikipedia.org/wiki/Minimax")))
C.add('''

def best_move(board, player):
    best_score = None
    best = None
    for i in available(board):
        board[i] = player
        score = minimax(board, "O" if player == "X" else "X")
        board[i] = " "
        better = best_score is None or (score > best_score if player == "X" else score < best_score)
        if better:
            best_score, best = score, i
    return best
''')
S.append(step("tt5", "Choose the best move",
  ["Minimax scores positions; now use it to **choose**. For each free square, place the piece, score the result with the opponent to move, and keep the best: highest for X, lowest for O.",
   "Ties go to the first square found, which makes the AI deterministic and easy to test."],
  "Write `best_move(board, player)` returning the index of the best square for `player`.",
  C.text, [dict(py='best_move(list("XX OO    "), "X") == 2', msg="X takes the winning square."), dict(py='best_move(list("XO XO    "), "X") == 6', msg="X completes its column."),
           dict(py='best_move(list("XX  O    "), "O") == 2', msg="O blocks X's two in a row."), dict(py='best_move(list("X O X    "), "O") == 8 and best_move(list("X  XOO X "), "O") == 6', msg="O blocks diagonal and column threats.")]))
C.add('''

def play(human_moves):
    board = [" "] * 9
    moves = iter(human_moves)
    turn = "X"
    while not game_over(board):
        if turn == "X":
            move = next((m for m in moves if board[m] == " "), None)
            if move is None:
                move = available(board)[0]
        else:
            move = best_move(board, "O")
        board[move] = turn
        turn = "O" if turn == "X" else "X"
    return winner(board) or "Draw"
''')
S.append(step("tt6", "Prove it can't lose",
  ["Before playing against a person, test the AI against scripted opponents. `play(human_moves)` plays X from a list of preferred squares (skipping taken ones) against the AI as O.",
   "`next((m for m in moves if ...), None)` pulls the next usable move from an iterator, or `None` when the list runs out."],
  "Write `play(human_moves)` that runs a full game (X from the list, falling back to the first free square; O from `best_move`) and returns `\"X\"`, `\"O\"` or `\"Draw\"`.",
  C.text, [dict(py='all(play(seq) != "X" for seq in [[0, 1, 2, 3, 4, 5, 6, 7, 8], [4, 0, 8, 2, 6], [0, 8, 2, 6, 4], [1, 3, 5, 7, 0], [8, 7, 6, 5, 4, 3]])', msg="X never wins against the AI."),
           dict(py='play([0, 1, 3]) == "O"', msg="A careless X loses."), dict(py='play([4, 0, 8, 2, 6, 1, 7, 3, 5]) in ("O", "Draw")', msg="Games always finish with a result.")]))
C.add('''

def ask_move(board):
    while True:
        text = input("Your move (1-9): ").strip()
        if text.isdigit() and 1 <= int(text) <= 9 and board[int(text) - 1] == " ":
            return int(text) - 1
        print("Pick a free square from 1 to 9.")


board = [" "] * 9
print("You are X. Squares are numbered 1-9, left to right, top to bottom.")
while not game_over(board):
    board[ask_move(board)] = "X"
    if not game_over(board):
        board[best_move(board, "O")] = "O"
    print(show(board))
    print()
result = winner(board)
print("It's a draw." if result is None else f"{result} wins.")
''')
S.append(step("tt7", "Play against it",
  ["Finally, a human player. People count squares from 1, so convert with `- 1`, and keep asking until the input is a free square from 1 to 9.",
   "Notice how little new code this needs: `show`, `game_over`, `best_move` and `winner` do all the work."],
  "Write `ask_move(board)` that keeps asking with `input` until it gets a free square from 1 to 9 (returning a 0-based index). Then run the game: you as X, the AI as O, printing the board after each round and the result at the end.",
  C.text, [dict(outHas="Pick a free square", msg="Invalid moves are refused."), dict(py='"X wins" not in _out and ("O wins" in _out or "draw" in _out)', msg="The game finishes and the AI doesn't lose."),
           dict(py="game_over(board)", msg="The game runs until it's over.")],
  stdin=["0", "5", "abc", "5", "1", "3", "7", "8", "9", "2", "4", "6"]))
project(id="tic-tac-toe-ai", title="Tic-Tac-Toe with an Unbeatable AI", lang="python", level="Advanced", hours="2 h", hue="#8b7dff", icon="grid", art="X O X",
  tagline="Write the minimax algorithm and build an opponent that never loses.",
  desc=["The game is simple; the AI is the lesson. You'll implement **minimax**, the recursive search behind classic game-playing programs, and watch it play perfectly.",
        "Along the way: board representation, list comprehensions, recursion with backtracking, and testing an algorithm against scripted opponents before a human ever touches it."],
  final="A playable tic-tac-toe game in the terminal against an AI that searches every possible future and never loses.",
  skills=["lists as boards", "list comprehensions", "recursion", "backtracking", "minimax", "testing algorithms", "input validation"],
  prereq="comfort with Python functions and lists. The **Recursion** lessons in Stage 1 help a lot.", core=["s1m6", "s2m6"],
  stretch=["Add alpha-beta pruning and count how many positions it skips.", "Let the AI play X or O, and the human choose.", "Generalise to 4×4 boards (and see why you need pruning or a depth limit).", "Cache scores of positions you've already seen (memoisation)."],
  demo_stdin=["5", "9", "3", "2", "4", "6", "1", "7", "8"],
  milestones=[milestone("The board", "Draw it, detect wins and know when it's over.", S[0:3]), milestone("The AI", "Minimax and choosing the best move.", S[3:5]),
              milestone("The game", "Prove the AI can't lose, then play it.", S[5:7])])
