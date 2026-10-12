# MISSION: mdcount

A command-line tool that counts words in Markdown files, skipping code blocks.

Run every phase autonomously. Stop only at the stop gates.

## 1. Config

```yaml
owner: example-dev
repo_name: mdcount
license: MIT
language: Python 3.10+, standard library only
distribution: GitHub repository (no package registry in v0.1)
```

## 2. Problem and target users

Writers who keep docs in Markdown want a word count that ignores fenced code blocks and front
matter. `wc -w` counts code and YAML too.

## 3. Goal

`python3 mdcount.py <files...>` prints a word count per file and a total, excluding fenced code
blocks and YAML front matter.

## 4. Non-goals

- No HTML or reStructuredText.
- No packaging on PyPI in v0.1.

## 5. Success criteria

1. Counts match a hand-checked fixture: verify with `python3 -m unittest`.
2. Exits 2 with a message when a file doesn't exist: verify with a test.

## 6. Phases

- **Phase 1 Build:** `mdcount.py` and `test_mdcount.py` with an example under `examples/`.
  Verify: tests pass.
- **Phase 2 Docs:** README, LICENSE (MIT), CHANGELOG. Verify: README commands were run.
- **Phase 3 Publish:** create the public GitHub repo `example-dev/mdcount`, push `main`, tag `v0.1.0`.

## 7. Stop gates

- **Gate A, before Phase 3:** show the repo name, description, README first screen, and the exact
  commands. Wait for "go".

## 8. Definition of done

- Public repo with green tests, README, LICENSE, and tag `v0.1.0`.
