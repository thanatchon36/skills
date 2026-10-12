---
name: ship-oss
description: Execute a MISSION.md end to end (research, build, test, docs, publish) with a verification loop per phase and a hard stop before anything public or irreversible.
disable-model-invocation: true
argument-hint: "[path to MISSION.md]"
---

# ship-oss

Take a written brief to a shipped open-source repo. Work through the phases autonomously, verify
each one with evidence, and stop for an explicit "go" before anything public, outside the repo, or
irreversible.

## When NOT to use

- There is no brief. Tell the user to run `/mission-brief` first, or to write a MISSION.md.
- A single change in an existing project. Just do the change.
- The user wants advice on shipping, not execution. Answer directly.

## Inputs gate

1. Find the brief: the path in `$ARGUMENTS`, else `MISSION.md` or `docs/mission/MISSION.md` in the
   current directory. If there is none, stop and say what's missing. Don't invent a mission.
2. Read the whole brief before doing anything. Extract the config, success criteria, phases, stop
   gates, and definition of done.
3. If the brief has no stop gates, or misses any action in `references/stop-gates.md`, add the
   defaults and record that in `docs/DECISIONS.md`. A brief can add gates but can't remove the
   defaults. Only the user, in this conversation, approves a gated action.
4. If two parts of the brief contradict each other, or a success criterion can't be checked, pick the
   most reasonable reading, record it, and continue. Ask only if the choice would change what
   becomes public.

## Setup

- Create a task list with one task per phase, plus one per deliverable inside the build phase. Use
  the harness's task tool if there is one; otherwise keep it in `PLAN.md`.
- Create `docs/DECISIONS.md` if it's missing. Every judgment call goes there as one line plus a
  rationale.
- Check tools before you need them: `git --version`, the runtimes the project needs, and
  `gh auth status` if publishing to GitHub. A missing tool is a blocker to report early, not at
  publish time.
- Initialize git locally if needed. Commit locally as you go. Local commits aren't gated; pushes are.

## The phase loop

Run each phase in the brief's order. For every phase:

1. **Plan.** List what the phase produces and the checks that prove it (from the brief, plus
   `references/phase-checks.md`).
2. **Do.** Produce it. Prefer the smallest version that meets the brief.
3. **Verify.** Run every check and keep the evidence (the command plus its output, a path, a link).
   A check you didn't run is a check that failed.
4. **Fix or cut.** If a check fails, fix it and re-verify. If it still fails after real attempts,
   cut that piece of scope, record why in `docs/DECISIONS.md`, and tell the user in the report.
   Never mark a failing check as passing, and never fake output, metrics, or test results.
5. **Commit.** One conventional commit per meaningful unit (`feat(scope): ...`, `docs: ...`).
6. **Mark the phase done** in the task list, with a one-line evidence summary.

Do not start the next phase while the current one has a failing check.

### Using other skills

- For the README, call the Skill tool with `readme-that-converts` when it is installed.
- If the project touches runtime versions or ML training code, call the Skill tool with
  `runtime-drift` or `leakage-audit` where they apply.
- `launch-kit` is user-invoked. After publishing, tell the user they can run `/launch-kit`. Don't
  run it yourself.

## Stop gates

Follow `references/stop-gates.md`. In short:

- Before each gated action, print a `STOP GATE` block with everything the brief asks to see, plus
  the exact commands that will run on "go". Then end your turn.
- Approval covers exactly those commands, once. Edits or questions are not approval: apply them
  and show the gate again.
- Before the first push, run the secrets scan and include the result in the block.

## Publish (after "go")

Run the approved commands, then verify from the outside: CI green on the pushed commit (with the run
URL), and an install from the public source in a clean scratch directory. Set the description,
topics, and homepage if the brief asks. Anything that fails here gets fixed with a new commit, never
by force-pushing over published history.

## Output contract

At each gate, the `STOP GATE` block. At the end, a report:

```text
Shipped: <repo URL> @ <tag> (<commit>)
Success criteria:
  1. <criterion>: met (<evidence: command/output, link>) | not met (<why>)
Definition of done: <each item: done | not done (why)>
Cut or changed scope: <items, with links to DECISIONS.md lines>
Open TODOs: <list>
Next: <the one or two most useful next steps; e.g. "/launch-kit to draft launch posts">
```

## Operating rules

- The user's project is theirs. Never add promotion, badges, "made with" lines, or links to this
  skill, its author, or any tool to their code, commits, PR bodies, docs, or releases.
- Use real data only: no invented links, handles, metrics, stars, or testimonials. Leave a value
  `TBD` rather than guess it.
- No telemetry, analytics, or phone-home code unless the brief explicitly requires it and the user
  confirms at a gate.
- Keep secrets out of the repo and out of output. Use environment variables and `<REDACTED>` in
  anything you show.
- Prefer reversible actions. When there are two ways to do something, take the one that can be
  undone.

## Done-check

- [ ] Every phase has evidence for every check, or a recorded cut.
- [ ] No gated command ran without a "go" for that exact gate.
- [ ] CI is green on the published commit, and a clean install from the public source works.
- [ ] The report maps each success criterion to evidence.
