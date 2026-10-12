#!/usr/bin/env python3
"""Mechanical checks for a project README. Standard library only.

Usage: python3 readme_lint.py [README.md]

Prints one line per check, PASS or FAIL, with the line number when it helps, then exits 1 if any
check failed. Content judgment (is the first sentence the problem? is the example real?) is not
something a script can decide; this only catches the mechanical misses.
"""

import os
import re
import sys

FIRST_SCREEN = 40  # lines; roughly one screen on GitHub at a normal window size
HYPE = re.compile(
    r"\b(blazing(ly)?|revolutioni[sz]\w*|seamless(ly)?|next[- ]generation|cutting[- ]edge|"
    r"state[- ]of[- ]the[- ]art|unparalleled|game[- ]chang\w*|effortless(ly)?|supercharge\w*|"
    r"world[- ]class|best[- ]in[- ]class|10x)\b",
    re.I,
)
INSTALL = re.compile(
    r"\b(npx|npm (i|install)|pnpm (add|dlx)|yarn (add|dlx)|pip install|pipx install|uv (tool|pip|add)|"
    r"brew install|go install|cargo install|gem install|docker run|git clone|curl|/plugin)\b"
)
SECTIONS = {
    "limitations": re.compile(r"^#{2,3}\s.*(limitation|caveat|known issues|not (yet )?supported)", re.I),
    "license": re.compile(r"^#{2,3}\s.*licen[cs]e", re.I),
}


def main(argv):
    path = argv[0] if argv else "README.md"
    if not os.path.exists(path):
        print(f"FAIL  {path} not found")
        return 1
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()
    base = os.path.dirname(os.path.abspath(path))
    results = []

    prose = [
        (i, l) for i, l in enumerate(lines, 1)
        if l.strip() and not l.lstrip().startswith(("#", "[!", "![", "<", "|", "```", ">")) and "shields.io" not in l
    ]
    if prose:
        i, first = prose[0]
        words = len(first.split())
        results.append((words <= 45, f"first sentence at line {i} is {words} words (keep the problem statement under ~45)"))
    else:
        results.append((False, "no prose paragraph found"))

    fence = next((i for i, l in enumerate(lines, 1) if l.lstrip().startswith("```")), None)
    results.append((fence is not None and fence <= FIRST_SCREEN,
                    f"first code block at line {fence} (want <= {FIRST_SCREEN}, on the first screen)"))

    in_fence, install_at = False, None
    for i, l in enumerate(lines[:FIRST_SCREEN], 1):
        if l.lstrip().startswith("```"):
            in_fence = not in_fence
        elif in_fence and INSTALL.search(l):
            install_at = i
            break
    results.append((install_at is not None,
                    f"install command on the first screen: {'line ' + str(install_at) if install_at else 'none in a code block within ' + str(FIRST_SCREEN) + ' lines'}"))

    for name, rx in SECTIONS.items():
        hit = next((i for i, l in enumerate(lines, 1) if rx.search(l)), None)
        results.append((hit is not None, f"'{name}' section {'at line ' + str(hit) if hit else 'missing'}"))

    hype = [(i, m.group(0)) for i, l in enumerate(lines, 1) for m in HYPE.finditer(l)]
    results.append((not hype, "hype words: " + (", ".join(f"{w!r} (line {i})" for i, w in hype) or "none")))

    badges = sum(l.count("shields.io") + l.count("badge.svg") for l in lines[:10])
    results.append((badges <= 4, f"{badges} badges in the first 10 lines (keep it to 4 or fewer)"))

    broken = []
    for i, l in enumerate(lines, 1):
        for target in re.findall(r"\]\(([^)\s#]+)(?:#[^)]*)?\)", l):
            if re.match(r"^[a-z]+:", target):
                continue
            if not os.path.exists(os.path.join(base, target)):
                broken.append(f"{target} (line {i})")
    results.append((not broken, "relative links: " + (", ".join(broken) + " not found" if broken else "all resolve")))

    empty = [i for i, l in enumerate(lines, 1) if re.search(r"\]\(\s*\)", l)]
    results.append((not empty, "empty link targets: " + (", ".join(f"line {i}" for i in empty) or "none")))

    for ok, msg in results:
        print(("PASS  " if ok else "FAIL  ") + msg)
    return 0 if all(ok for ok, _ in results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
