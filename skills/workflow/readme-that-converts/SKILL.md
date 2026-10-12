---
name: readme-that-converts
description: Write, rewrite, or review a project's top-level README.md so a stranger understands the problem from the first sentence, can copy-paste a working install from the first screen, and sees real output from a real run, followed by why it exists, limitations, and roadmap. Use when creating or rewriting a README, when the user asks to "improve / review / fix the README", "make the README clearer", or "get the repo ready for people to try", when preparing an open-source repo for release, or on "/readme-that-converts". Not for CONTRIBUTING.md, changelogs, API reference docs, docstrings, or internal design docs.
---

# readme-that-converts

Make a README that turns a visitor into a user. The visitor should know in one sentence whether
this solves their problem, and be running it from the first screen.

## When NOT to use

- Other docs: `CONTRIBUTING.md`, `CHANGELOG.md`, API reference, docstrings, ADRs, internal design
  docs.
- A README for a private or internal repo where "a stranger" isn't the reader. The structure still
  helps, but skip the trust rules about positioning.
- Translating an existing README. Translate it faithfully instead of restructuring it.

## Workflow

Do the steps in order. Do not skip ahead.

### 1. Collect facts, not adjectives

Read the code, the manifest (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`), the
`LICENSE`, the CI config, and any existing README. Write down:

- What problem does it solve, and for whom? Use the user's words if they gave any.
- How is it installed today? Is it actually published (npm, PyPI, a release, a marketplace), or only
  runnable from a clone?
- What is the shortest command that produces useful output?
- What does it not do? Look for TODOs, unsupported inputs, and platform checks.
- The license, from the `LICENSE` file, not from memory.

If a fact is missing (no license file, the package isn't published), don't invent it. Note it as a
gap for step 5.

### 2. Gate: run it

Run the install (or the from-clone path) and the shortest useful command on an example input in the
repo. If there is no example input, create a small one under `examples/` and say so. Capture the
real output.

If you can't run it (missing credentials, hardware, a paid service), don't fabricate output. Write
the section with a `TODO: paste real output from <command>` and tell the user. Every install command
in the README must have been run here, or be marked "(untested)".

### 3. Write, in this order

Follow `references/structure.md` for what each section must contain:

1. **First sentence**: the reader's problem, concretely, and what this does about it.
2. **Install and first run**: one copy-paste block on the first screen, with prerequisites.
3. **Example**: the real command and real output from step 2, reproducible from the repo.
4. **Why**: what people do today and where that falls short. Two or three short paragraphs.
5. **Usage**: tasks, options, and real `--help` output for CLIs.
6. **Limitations**: what it doesn't do, and known wrong results.
7. **Roadmap**: a few concrete items (optional for small projects).
8. **Contributing and license**.

When rewriting, keep every true, useful fact from the old README (options, caveats, credits). Move
it; don't drop it.

### 4. Lint

```sh
python3 "${CLAUDE_SKILL_DIR}/scripts/readme_lint.py" README.md
```

(Outside Claude Code: `scripts/readme_lint.py` next to this file.) It checks the first-sentence
length, a code block and install command on the first screen, the limitations and license sections,
hype words, badge count, and broken relative links. Fix every FAIL, or say why one doesn't apply.

### 5. Report

Use the output contract.

## Review mode

When the user asks for a review rather than a rewrite: do steps 1 and 4, then return findings
ranked by how many visitors each one loses (first-screen problems first). Each finding gets the
line, what's wrong, and the concrete replacement text. Don't rewrite the file unless asked.

## Output contract

For a write or rewrite: the file itself, then a short report:

```text
README: <written | rewritten> (<N> lines)
Ran: <commands actually executed, and the result of each>
Untested: <commands in the README that were not run, or "none">
Gaps for you: <missing license, unpublished package, TODO output, ...>
Lint: <all pass | FAILs left, with reasons>
```

For a review: a ranked list of `README.md:<line>`, the problem, and the suggested text, then the
lint output.

## Operating rules

- No hype words, no marketing superlatives, no claims without evidence ("fast" needs a number).
- No badges except real checks (CI, version, license), and four at most.
- Never add promotional lines, "made with" credits, or links to unrelated projects, including this
  skill or its author. The README is the user's.
- Keep commands copy-pasteable: no prompts (`$`) inside code blocks meant for copying, and no
  unexplained placeholders.
- Match the project's existing language and spelling. Don't translate unless asked.

## Done-check

- [ ] The first sentence names the problem a reader has, not the project's adjectives.
- [ ] An install command and first run are on the first screen, and each was run or is marked
      "(untested)".
- [ ] The example output came from a real run in this session, or is an explicit TODO.
- [ ] A limitations section exists and is specific.
- [ ] The lint passes, or every remaining FAIL is explained.
