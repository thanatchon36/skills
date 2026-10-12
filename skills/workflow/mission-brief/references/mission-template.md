# MISSION: <project name>

<One sentence: what this project is and who it is for.>

Run every phase autonomously. Stop only at the stop gates. When something is ambiguous, choose the
most reasonable option, record it in `docs/DECISIONS.md` with one line of rationale, and keep going.

## 1. Config

```yaml
owner: <github user or org>
repo_name: <name>
license: <SPDX id>
language: <primary language and minimum version>
distribution: <npm | PyPI | GitHub release | container | plugin marketplace | none>
links: {}          # only real links; never invent one
```

## 2. Problem and target users

- **Who:** <the specific person, in the situation where they hit the problem>
- **Problem:** <what goes wrong today, with a concrete example: a file, an error, a command>
- **Today's workaround:** <what they do instead, and why it falls short>

## 3. Goal

<One sentence describing the outcome for the user, not the implementation.>

## 4. Non-goals

- <Things this project will not do in v0.1, each with one line of why>

## 5. Success criteria

Each one must be checkable by running something or reading something.

1. <criterion>: verify with `<command or check>`
2. ...

## 6. Scope for v0.1

| Deliverable | Notes |
| --- | --- |
| <feature, command, file> | <constraint or acceptance detail> |

Out of scope until later: <list>

## 7. Constraints

- Stack and runtime: <...>
- Dependencies policy: <e.g. standard library only, or a pinned allowlist>
- Budget and time: <...>
- Data, privacy, and security: <no telemetry, no secrets in the repo, ...>

## 8. Phases

Each phase ends with a verification step that must pass before the next phase starts.

- **Phase 0 Discover:** <research to do, prior art to read>. Output: <file>. Verify: <check>.
- **Phase 1 Plan:** `PLAN.md` with <contents>. Verify: <check>.
- **Phase 2 Build:** <thin end-to-end slice first, then ...>. Verify: <tests, a real run>.
- **Phase 3 Docs:** README, CHANGELOG, CONTRIBUTING, LICENSE. Verify: every README command was run.
- **Phase 4 Publish:** <repo, release, package>. Verify: install from the public source in a clean
  directory.
- **Phase 5 Report:** what shipped, links, open TODOs.

## 9. Stop gates

Stop and wait for an explicit "go" before each of these. At each gate, show the listed items.

- **Gate A, before anything public** (repo creation, first push, tag, release, package publish):
  show <name, description, README first screen, version, what will be published>.
- **Gate B, before touching anything outside this repo:** show <the exact diff or command>.
- <Gate C, before anything that costs money or can't be undone: ...>

## 10. Definition of done

- <the observable end state, e.g. "installs with one command from the public source">
- <CI green on main>
- <README first screen shows the problem, the install, and a real example>
- <everything in the success criteria verified, with the evidence linked in the report>
