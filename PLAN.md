# PLAN: thanatchon-skills v0.1

Brief: [`docs/mission/MISSION.md`](docs/mission/MISSION.md). Research:
[`docs/research/`](docs/research/). Choices and their reasons: [`docs/DECISIONS.md`](docs/DECISIONS.md).

## Tagline

> Agent skills that take an open-source project from a one-page MISSION.md to a shipped public repo.

The same line is used as the GitHub description, the `plugin.json` description, and the README's
first line.

## Lineup (7 shipped)

| Skill | Bucket | Invocation | Description (as shipped in frontmatter) |
| --- | --- | --- | --- |
| `mission-brief` | workflow | user | Turn a project idea into a MISSION.md by interview, one question at a time: goal, non-goals, users, success criteria, phases, stop gates, license, definition of done. |
| `ship-oss` | workflow | user | Execute a MISSION.md end to end (research, build, test, docs, publish) with a verification loop per phase and a hard stop before anything public or irreversible. |
| `readme-that-converts` | workflow | model | Write, rewrite, or review a project README so a stranger gets the problem from the first sentence and a working install on the first screen. Triggers on README work, not other docs. |
| `launch-kit` | workflow | user | Draft launch posts for a repo (Show HN, X thread, LinkedIn, Reddit, Thai developer communities) plus GitHub topics and a social-preview brief, written to `launch/`. Never posts anything. |
| `runtime-drift` | engineering | model | Find and fix Node, Python, or Go versions that disagree across version files, manifests, Dockerfiles, and CI, using verdrift as a deterministic scanner. Triggers on runtime version work, not library upgrades. |
| `leakage-audit` | data-ml | model | Audit pandas, PySpark, or scikit-learn training code for target leakage, temporal leakage, train/test contamination, and preprocessing fit on the full dataset, citing `file:line` per finding. |
| `ask-thanatchon` | meta | user | Ask which skill or flow in this plugin fits your situation. |

Model-invoked descriptions carry explicit trigger phrases and "not for" exclusions in the
frontmatter itself. The table shows the summaries.

### In progress (not shipped; `metadata.internal: true`)

`eval-harness`, `rag-triage`, `backtest-honesty`, `model-card`. Each is a stub with its purpose,
trigger idea, and an open-questions list. None appears in `plugin.json` or the README skill list.

### Flows (what `ask-thanatchon` routes)

1. **Idea to shipped repo:** `/mission-brief`, then `/ship-oss`. `readme-that-converts` fires inside
   the docs phase, and `/launch-kit` comes after publish.
2. **Existing repo, better README:** `readme-that-converts` (model-invoked, or ask for it).
3. **Version bump or CI/Docker drift:** `runtime-drift`.
4. **ML pipeline review:** `leakage-audit`.

## Quality bar per skill

1. `claude plugin validate . --strict` passes.
2. `evals/<skill>/`: at least 3 should-trigger and 3 near-miss cases, plus outcome graders where the
   outcome can be checked deterministically.
3. Local marketplace install in a scratch dir shows exactly the 7 skills under `thanatchon-skills:`.
4. `runtime-drift` on verdrift `examples/drifted` reports the same 4 problems.
5. `leakage-audit` finds every planted leak in `fixtures/leakage/leaky/` and nothing in
   `fixtures/leakage/clean/`.
6. Every README install command was run, or is labeled untested.
7. CI: validate, frontmatter lint, markdown link check.

## README outline

1. Tagline (first line), then a one-line flagship callout to verdrift.
2. Install (first screen): Claude Code two-liner, `npx skills`, a "pick one" note.
3. The problem: agents can write code, but shipping an open-source repo is a sequence of judgment
   calls (scope, README, licensing, release, launch) where they skip steps and publish too early.
4. What's inside: failure mode, then fix, then skill (grouped as user-invoked and model-invoked).
5. Example: a real `runtime-drift` run on verdrift's fixture (real output).
6. Built with these skills: verdrift (commits, CI, release) and this repo (its own MISSION.md).
7. How to know it's working.
8. Limitations, then roadmap (the in-progress skills).
9. More from me, then license.

## Build order

`runtime-drift` and `leakage-audit` first (deterministic outcomes, easiest to verify), then
`readme-that-converts`, `mission-brief`, `ship-oss`, `launch-kit`, and `ask-thanatchon` last (it maps
the others).
