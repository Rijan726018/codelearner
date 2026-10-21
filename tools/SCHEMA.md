# Stage content schema — The 10,000-Hour Map v2

Write ONE file per stage: `data/<stageId>.json` (e.g. `data/s1.json`). It must be valid JSON (no comments, no trailing commas). Use double-quoted strings; escape newlines in code as `\n`.

## Teaching principles you must follow (learning-science based)
- Each lesson = one daily session of 60–90 min. Small, concrete, one objective.
- **Worked example first, then practice** (worked-example effect for novices). Later stages fade the worked example toward problem-first.
- **Retrieval practice**: every lesson ends with 3–4 questions the learner must answer from memory.
- **Levelled questions**: level 1 = Recall (facts, definitions), level 2 = Apply (use it on a new case, predict output), level 3 = Analyze (debug, compare trade-offs, design). Every lesson has at least one L1, one L2 and one L3.
- **Interleaving**: module exams mix topics from all lessons in the module; include at least one question that connects to an EARLIER module.
- **Generation**: the `tryit` task asks the learner to produce something (code, a diagram, an explanation), not just read.
- **Concrete over abstract**: real code, real numbers, real tools. No lorem ipsum, no filler, no motivational fluff.
- Questions must be unambiguous and have exactly one correct answer. `explain` says WHY, including why the tempting wrong answer is wrong.
- Accuracy matters more than volume. If a `predict` output or a `trace` is not 100% certain, use an mcq instead.

## Top-level shape
```json
{
  "id": "s1",
  "modules": [ Module, ... ]
}
```

## Module
```json
{
  "id": "s1m1",
  "title": "Talking to the computer",
  "summary": "One sentence on what this module gives you.",
  "lessons": [ Lesson, ... ],          // 4–6 lessons
  "project": {
    "title": "Tip calculator CLI",
    "brief": "2–3 sentences: what to build and why it uses this module's skills.",
    "milestones": ["Step 1 ...", "Step 2 ...", "Step 3 ...", "Step 4 ..."],   // 4–6 concrete, checkable steps
    "stretch": "One harder extension."
  },
  "exam": [ Question, ... ]           // 6–8 questions, mostly level 2–3, interleaved across the module's lessons
}
```

## Lesson
```json
{
  "id": "s1m1l1",                     // <moduleId>l<n>
  "title": "Your first program",
  "minutes": 60,
  "objective": "By the end you can ... (one sentence, observable)",
  "concept": ["paragraph 1", "paragraph 2", "paragraph 3"],   // 2–4 short paragraphs, 60–120 words each. Inline `code` with backticks and **bold** allowed. Nothing else.
  "visual": Visual,                   // optional but strongly encouraged; include in at least 2/3 of lessons
  "example": { "lang": "python", "code": "print('hi')", "explain": "1–3 sentences walking through it." },   // optional for non-code lessons
  "tryit": "A specific task the learner does in their editor or on paper, 2–4 sentences.",
  "questions": [ Question, ... ],     // 3–4
  "resource": { "title": "CS50x Week 6", "url": "https://cs50.harvard.edu/x/weeks/6/" }   // one real, stable, free URL you are confident exists
}
```

## Visual (pick ONE type per lesson)
- `{"type":"steps","title":"...","steps":[{"label":"Source code","detail":"what you write"}, ...]}` — 3–6 boxes rendered as a left-to-right flow with arrows. For pipelines, processes, request lifecycles.
- `{"type":"compare","title":"...","left":{"title":"list","points":["..",".."]},"right":{"title":"tuple","points":["..",".."]}}` — side-by-side contrast.
- `{"type":"table","title":"...","headers":["Op","Cost"],"rows":[["lookup","O(1)"],...]}` — up to 6 rows.
- `{"type":"trace","title":"...","code":"x = 2\ny = x * 3\nprint(y)","steps":[{"line":1,"vars":{"x":"2"},"out":""},{"line":2,"vars":{"x":"2","y":"6"},"out":""},{"line":3,"vars":{"x":"2","y":"6"},"out":"6"}]}` — an interactive step-through debugger. `line` is 1-based. `vars` is the full variable state AFTER that line runs (strings). `out` is cumulative stdout so far. Max 12 steps. Only use when you can trace it with certainty.
- `{"type":"boxes","title":"...","items":[{"label":"Stack","detail":"..."},{"label":"Heap","detail":"..."}]}` — labelled regions (memory layouts, layers, architecture).

## Question (types)
All have `"id"` (`<lessonId>q<n>` or `<moduleId>e<n>` for exam), `"level"` (1|2|3), `"type"`, `"prompt"`, `"explain"`. Optional `"code"` (shown in a code block above the options).
- mcq: `{"type":"mcq","options":["a","b","c","d"],"answer":2}` — `answer` is the 0-based index. 3–4 options, plausible distractors.
- predict: `{"type":"predict","code":"print(3 // 2)","answer":"1","accept":[]}` — learner types the exact output; compared after trimming whitespace. `accept` lists other exact strings to accept. Keep outputs short (one line ideally).
- parsons: `{"type":"parsons","prompt":"Arrange the lines to ...","lines":["def f(n):","    if n == 0:","        return 1","    return n * f(n - 1)"]}` — `lines` in the CORRECT order, with indentation included; the app shuffles them. 3–7 lines. The correct order must be unique.

## Ids
Stage `sN`, modules `sNmK`, lessons `sNmKlJ`, questions `sNmKlJqI`, exam questions `sNmKeI`. All ids unique.
