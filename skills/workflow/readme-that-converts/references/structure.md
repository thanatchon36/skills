# README structure, section by section

The order is fixed because readers drop off in this order: most decide from the first screen, and
fewer read to the end. Each section says what it must contain, and the common miss.

## 1. First sentence: the problem, concretely

What it must contain: the situation the reader is in, in their words, plus what the project does
about it. Name real files, commands, or errors where possible.

- Weak: "csvdiff is a powerful tool for data comparison."
- Strong: "You exported the same table twice and need to know which rows changed. csvdiff compares
  two CSV files by a key column and prints added, removed, and changed rows."

The common miss: starting with the project's history, philosophy, or a list of adjectives.

## 2. Install and first run (on the first screen)

What it must contain: one copy-paste block that a stranger can run as is, the prerequisites it needs
(runtime version, OS), and the shortest command that produces output.

- Show the install the project actually supports (`pipx install`, `npx`, `brew`, a plugin
  marketplace). If there are several, lead with one and put the rest in a short list.
- Every command must have been run on the current version. If one wasn't, write "(untested)" next
  to it rather than leaving it out silently.
- No placeholders the reader has to guess (`<your-thing>`) unless they're explained right there.

The common miss: install hidden below a features list, or a "Getting started" link to a docs site.

## 3. A real example

What it must contain: a command, and the output it really printed, copied from a real run. Use a
small example input in the repo, so readers can reproduce it, and say how.

The common miss: hand-written "example output" that the tool never produced, or output from an old
version. If you can't run the tool, say so and leave a TODO rather than inventing output.

## 4. Why it exists

What it must contain: the gap the project fills. What people do today (a one-off script, a manual
check, a heavier tool), and why that falls short. Two or three short paragraphs at most.

The common miss: a comparison table that only ticks your own column, or attacks on alternatives.
Be fair, and say when another tool is the better choice.

## 5. Usage and reference

What it must contain: the options and the common tasks, written as tasks ("Use in CI", "Ignore a
file"). For CLIs, paste the real `--help` output. Long reference material goes in `docs/`, linked
from here.

## 6. Limitations

What it must contain: what it doesn't do, known wrong results, platform gaps, and scale limits.
This section builds more trust than any feature list. Readers who hit a limit you documented don't
file angry issues.

## 7. Roadmap

What it must contain: a few concrete next items, without dates you can't keep. Optional for small
projects.

## 8. Contributing and license

Contributing: the most useful kind of contribution (often "a bug report with a minimal
reproduction"), and a link to `CONTRIBUTING.md` if there is one. License: the SPDX name, linked to
the `LICENSE` file, and the file must exist.

## Things that cost trust

- Badges for things that aren't checks (stars, "made with love"), or more than about four.
- Hype words: "blazing", "seamless", "revolutionary", "next-generation", "state-of-the-art".
  `scripts/readme_lint.py` flags the common ones.
- Claims without evidence: "fast" with no number, "production-ready" with no users or tests.
- Stale output, dead links, and install commands for a package that was never published.
- Promotional lines unrelated to the project (other products, "built with X" credits) above the
  install. One honest line about a related project of yours is fine, kept short and labeled.

## A reference example

[verdrift's README at v0.1.0](https://github.com/thanatchon36/verdrift/blob/v0.1.0/README.md) (by the
author of this skill) follows this order. It has a one-sentence problem with real file names, a
one-line install, a reproducible example with real output, why, limitations, and roadmap. Use it as
a shape, not as text to copy.
