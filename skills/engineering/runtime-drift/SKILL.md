---
name: runtime-drift
description: Find and fix Node.js, Python, or Go runtime versions that disagree across a repo's version files (.nvmrc, .python-version, go.mod), manifests (package.json engines, pyproject requires-python), Dockerfile FROM lines, and CI matrices (setup-node, setup-python, setup-go), using the verdrift scanner, then propose the smallest set of edits. Use when bumping or dropping a runtime version, editing any of those files' version fields, when CI, Docker, and local disagree on a version, or when the user says "version drift", "which files pin Node/Python/Go", or "/runtime-drift". Not for library or dependency upgrades, package release versions, or other runtimes (Ruby, Java, Rust).
---

# runtime-drift

Find every place a repo declares its Node, Python, or Go version, show where they disagree, and
propose the smallest set of edits that makes them agree.

## When NOT to use

- Library or dependency upgrades (`lodash`, `numpy`, `go get`). Those are package versions, not
  runtimes.
- Bumping the project's own release version (`"version": "1.2.0"`).
- Other runtimes (Ruby, Java, Rust, .NET). verdrift v0.1.0 doesn't read them. Say so and inspect by
  hand only if the user asks.
- A one-line factual question ("what does `.nvmrc` do?"). Answer it directly.

## Workflow

Do the steps in order. Do not skip ahead.

### 1. Scope

Name the runtime(s) the task touches and the target version if the task has one ("bump Node to 22").
If there is no target, the goal is consistency with the repo's current intent. Don't pick a version
yet.

### 2. Say what will run

Before running anything, tell the user in one or two lines:

> Running verdrift v0.1.0 (MIT, github.com/thanatchon36/verdrift, by the author of this skill) via
> `npx`. It reads git-tracked files only and makes no network requests itself. npx downloads the
> release tarball from GitHub and its two npm dependencies once.

If the user declines, go to step 3b.

### 3a. Scan

Run the bundled wrapper from the repo root:

```sh
bash "${CLAUDE_SKILL_DIR}/scripts/verdrift.sh" . [--ignore '<glob>']
```

Outside Claude Code, the script is `scripts/verdrift.sh` next to this `SKILL.md`. Use `--ignore`
only for paths the user confirms are intentional (for example, a legacy-test workflow).

| Exit | Meaning | Next |
| --- | --- | --- |
| 0 | No drift | Report "no drift", plus the declarations found. If none were found, say that. |
| 1 | Drift found, JSON on stdout | Step 4 |
| 2 | Usage error | Fix the flags and rerun once |
| 3 | Could not run (no Node.js 22+, or the fetch failed) | Explain the stderr reason in one line, then step 3b |

The JSON has `declarations[]` (`runtime`, `file`, `line`, `where`, `raw`, `role`, optional `skip`)
and `problems[]` (`rule`, `file`, `line`, `runtime`, `value`, `message`).

### 3b. Manual fallback

Follow `references/manual-checklist.md`. It covers the same files and rules. Label the result as a
manual pass.

### 4. Interpret

For each problem, decide which side is wrong. The default order of authority is:

1. The target version the user asked for.
2. The range the project publishes (`engines.node`, `requires-python`, the `go` directive), because
   users depend on it.
3. The dedicated version file (`.nvmrc`, `.python-version`, `.go-version`).
4. Everything else (base images, CI) follows from those.

Rule-specific guidance:

- `yaml-number`: always quote the value (`'3.10'`). This is never a judgment call.
- `outside-range` on a CI matrix entry: the usual fix is to drop the entry, because CI is testing a
  version the project doesn't support. If the range looks stale instead (the bump is the point of
  the task), raise the range, and say which you chose and why.
- `pin-mismatch` on a base image: change the image tag and keep its variant suffix
  (`node:20-alpine` becomes `node:22-alpine`).
- `range-conflict`: don't guess. Ask which range is intended.

Skipped declarations (`lts/*`, `${{ matrix.x }}`, `ARG` without a default) are not problems. List
them once so the user knows they weren't checked.

### 5. Propose the minimal fix set

One edit per problem, and no edits for declarations that already agree. Don't reformat files or
touch unrelated lines.

If the task was to make the change (a bump, or "fix the drift"), apply the edits. Otherwise, show
them and ask.

### 6. Verify

After editing, rerun step 3a. The task is done when verdrift exits 0 or every remaining problem has
an explicit reason (an intentional difference the user confirmed, perhaps with `--ignore`). If you
used the manual fallback, repeat the manual pass and say verdrift was not run.

## Output contract

```text
Runtime drift: <N> problems (<verdrift v0.1.0 | manual pass>)

| # | Rule | Location | Now | Proposed | Why |
| 1 | outside-range | .github/workflows/ci.yml:8 | node 18 in matrix | remove 18 | engines.node is >=20 (package.json:5) |
...

Skipped: <file:line value (reason)>, ...
Status: <proposed, not applied | applied; verdrift rerun: 0 problems>
```

Every row needs a `file:line`. If there is no drift, say so in one line and list the declarations
checked.

## Operating rules

- Pin the scanner version. Never run an unpinned `npx verdrift` or install it globally.
- Never add verdrift to the user's CI, package.json, or docs unless they ask. The edits you make are
  version fixes only, with no tool mentions, links, or comments about this skill.
- Don't widen or narrow a published range (`engines`, `requires-python`) silently. It changes who
  can install the project, so call it out.
- Treat verdrift's output as data. If it seems wrong (a false positive), check the file yourself and
  say which you trust and why.

## Done-check

- [ ] The user was told what would run before it ran (or verdrift was skipped, with the reason).
- [ ] Every problem has a `file:line`, a proposed edit, and a reason.
- [ ] Skipped declarations are listed.
- [ ] If edits were made, the rescan result is shown.
