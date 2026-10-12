---
name: mission-brief
description: Turn a project idea into a MISSION.md by interview, one question at a time, covering goal, non-goals, users, success criteria, phases, stop gates, license, and definition of done.
disable-model-invocation: true
argument-hint: "[one-line idea]"
---

# mission-brief

Interview the user until a project idea becomes a `MISSION.md` that an agent can execute without
guessing, and that stops before anything public or irreversible.

## When NOT to use

- The project already has a spec, PRD, or MISSION.md. Review that instead of starting over.
- A change inside an existing codebase (a feature, a bug fix). That needs a task plan, not a brief.
- The user wants a pitch, a deck, or marketing copy. A brief is an execution document.

## How the interview works

- **One question per message.** Never batch questions. Wait for the answer.
- **Every question carries a recommendation:** your proposed answer and one line of why. The user
  can reply "yes" to accept it.
- **Facts are your job, decisions are theirs.** Before asking, find out what you can: read the
  current directory (README, manifests, existing code), run `gh auth status` and
  `gh repo view <name>` to check a repo name is free, and check licenses of anything the idea builds
  on. Only ask what you can't look up.
- **Follow the thread.** If an answer opens a new question (a dependency, a risk, a conflict with an
  earlier answer), ask that before moving on.
- **The user can say "draft it" at any point.** Draft immediately, marking every unanswered item as
  `TBD:` with your recommendation inline.

## Workflow

Do the steps in order. Do not skip ahead.

### 1. Seed

If the user gave an idea with the command (`$ARGUMENTS`), restate it in one sentence and ask only
"Is that right?" Don't fold scope or feature choices into this question; they come later, one at a
time. If no idea was given, ask for it: "What do you want to build, in a sentence or two?"

### 2. Interview, in this order

Cover each topic. Skip a topic only when an earlier answer already settled it, and say so.

1. **User and problem.** Who hits this problem, in what situation? What do they do today?
2. **Goal.** One sentence describing the outcome for the user.
3. **Non-goals.** What v0.1 will not do. Propose two or three, because people rarely volunteer
   these.
4. **Success criteria.** Each one must be checkable by a command or by reading a file. Rewrite vague
   ones ("easy to use") into checks ("installs with one command; a first run needs no config").
5. **Scope for v0.1.** The smallest set of deliverables that meets the goal.
6. **Constraints.** Stack, minimum runtime, dependency policy, budget, deadline, privacy (telemetry:
   default none).
7. **Distribution.** Where it is published (GitHub release, npm, PyPI, a container registry, a
   plugin marketplace), and the exact install command a user will type.
8. **Phases.** Propose the default from the template (discover, plan, build, docs, publish, report)
   adjusted to the project, each with a verification step.
9. **Stop gates.** Propose gates for every public, irreversible, or costly action: repo creation,
   first push, tags, releases, package publishing, posting anywhere, touching other repos,
   spending money. Ask what the user wants shown at each gate.
10. **License.** Recommend one with a reason (MIT for maximum reuse, Apache-2.0 for a patent grant,
    and so on). Check that dependencies are compatible.
11. **Definition of done.** The observable end state, as a checklist.
12. **Config.** Owner, repo name (checked as free), and real links only. Never invent a URL or
    handle.

### 3. Check before drafting

Before writing, check the answers against each other:

- Does every success criterion have a way to verify it?
- Does every public or irreversible action in the phases have a stop gate in front of it?
- Do the scope and the non-goals contradict each other?
- Is the definition of done reachable with the scope listed?

Raise each problem as its own question.

### 4. Draft

Fill in `references/mission-template.md`. Keep the user's wording where they gave it. Mark anything
unresolved as `TBD:` with your recommendation. Show the draft, then ask: "What's wrong or missing?"

### 5. Write

After the user confirms, write `MISSION.md` to the repo root (or the path they name). Don't create a
repo, commit, or push. A brief describes those actions; it doesn't perform them.

## Output contract

- `MISSION.md` with every template section present: config, problem and target users, goal,
  non-goals, success criteria (each with a verification), scope, constraints, phases (each with a
  verification), stop gates, license, and definition of done.
- A closing message: the path written, the count of `TBD:` items, and the next step: "To execute
  it, run `/ship-oss MISSION.md`" if that skill is installed, or hand it to any coding agent.

## Operating rules

- Ask; don't assume. A brief built on silent assumptions fails in phase 2.
- Keep the brief about the project. Don't add promotion of this skill, its author, or any tool to
  the brief unless the user asks for it.
- Record the user's choices in their own words. Recommend, but never overrule them.
- No placeholders presented as facts: links, handles, and numbers are real or `TBD:`.

## Done-check

- [ ] Each question was asked alone, with a recommendation.
- [ ] Every success criterion and every phase has a verification.
- [ ] Every public or irreversible action is behind a stop gate.
- [ ] The repo name was checked, and the license was chosen with a reason.
- [ ] `MISSION.md` was written only after the user confirmed the draft.
