"""Helpers for Build & Learn projects.

A project is a list of milestones, each a list of steps. Every step's solution is the whole program at that point;
its starter is the previous step's solution (or the project's `start`). Check types match the bootcamp's (see
tools/bootcamp_src.py), plus `web` checks: {"js": expression, "do": statements run first, "storage": {...}}.
In web checks the page is fresh for every check and these helpers exist: $ $$ _click _type _press _submit _text
_wait _logs _visible."""

PROJECTS = []
TRACKS = []

def project(**k):
    PROJECTS.append(k)
    return k

def step(id, title, body, task, solution, tests, **extra):
    return dict(id=id, title=title, body=body, task=task, solution=solution, tests=tests, **extra)

def milestone(title, goal, steps):
    return dict(title=title, goal=goal, steps=steps)


class Page:
    """Builds a single-file web app from three sections, so each step can change one of them."""
    def __init__(self, title):
        self.title, self.css, self.body, self.js = title, [], [], []

    def render(self):
        css = "\n".join(self.css)
        body = "\n".join(self.body)
        js = "\n".join(self.js)
        out = f"<!DOCTYPE html>\n<html>\n<head>\n  <meta charset=\"utf-8\">\n  <title>{self.title}</title>\n  <style>\n{css}\n  </style>\n</head>\n<body>\n{body}\n"
        if js.strip():
            out += f"  <script>\n{js}\n  </script>\n"
        return out + "</body>\n</html>\n"

    @staticmethod
    def _sub(parts, old, new):
        text = "\n".join(parts)
        assert text.count(old) == 1, f"expected exactly one occurrence of {old!r}"
        return text.replace(old, new).split("\n")

    def sub_css(self, old, new): self.css = self._sub(self.css, old, new)
    def sub_body(self, old, new): self.body = self._sub(self.body, old, new)
    def sub_js(self, old, new): self.js = self._sub(self.js, old, new)


class Code:
    """Accumulates a Python / JavaScript / SQL program across steps."""
    def __init__(self, text=""):
        self.text = text

    def add(self, more):
        self.text += more
        return self.text

    def sub(self, old, new):
        assert self.text.count(old) == 1, f"expected exactly one occurrence of {old!r}"
        self.text = self.text.replace(old, new)
        return self.text
