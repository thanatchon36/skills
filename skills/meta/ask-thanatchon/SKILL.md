---
name: ask-thanatchon
description: Ask which skill or flow in this plugin fits your situation.
disable-model-invocation: true
argument-hint: "[what you're trying to do]"
---

# ask-thanatchon

Route the user to the right skill or flow in this plugin, or say plainly that none fits.

Before you describe what a skill does or suggest skipping a step, read that skill's `SKILL.md` (in
this plugin's `skills/` tree). The summaries below are for orientation only.

## How to answer

1. If the user described their situation (`$ARGUMENTS`), match it to a flow below. If not, ask one
   question: "What are you trying to do?"
2. Answer with the flow, the first command to run, and one line on why. Keep it short: three to
   eight lines.
3. If nothing here fits, say so and suggest doing the task directly. Don't stretch a skill to fit.

## The main flow: idea to shipped repo

1. **`/mission-brief`** interviews you, one question at a time, and writes `MISSION.md`: goal,
   non-goals, users, success criteria, phases, stop gates, license, and definition of done. Start
   here when you have an idea but no written brief.
2. **`/ship-oss MISSION.md`** executes the brief phase by phase, verifying each one. It stops for
   your "go" before anything public: repo creation, push, tag, release, publish, or touching
   other repos. During the docs phase it uses `readme-that-converts`.
3. **`/launch-kit`** writes launch drafts to `launch/` once the repo is public and installs: Show
   HN, an X thread, LinkedIn, Reddit, Thai developer communities, GitHub topics, and a
   social-preview brief. It never posts.

Already have a brief? Skip to step 2. Already shipped? Skip to step 3.

## Standalone skills (model-invoked: they fire on their own, or you can ask)

- **`readme-that-converts`**: write, rewrite, or review a README. The problem goes in the first
  sentence, the install on the first screen, real output from a real run, and limitations. Say
  "review my README" or "rewrite the README".
- **`runtime-drift`**: when Node, Python, or Go versions disagree across `.nvmrc`, manifests,
  Dockerfiles, and CI, or before a version bump. Runs the verdrift scanner (pinned, and it tells you
  before running), then proposes the smallest set of fixes.
- **`leakage-audit`**: when ML training code (pandas, scikit-learn, PySpark) scores too well
  offline, or before you trust a metric. Checks for target leakage, temporal leakage, train/test
  contamination, and preprocessing fit on the full dataset, with `file:line` for each finding.

## Common situations

| Situation | Go to |
| --- | --- |
| "I have an idea for an open-source tool" | `/mission-brief` |
| "I have a MISSION.md / spec, build and publish it" | `/ship-oss <path>` |
| "Nobody tries my repo" or "the README is a mess" | `readme-that-converts` (ask it to review first) |
| "I'm about to post my project" | `/launch-kit` (check the repo installs from public first) |
| "Bumping Node/Python/Go", or "CI and Docker run different versions" | `runtime-drift` |
| "My model's validation score is suspiciously high" | `leakage-audit` |
| A single feature or bug fix in an existing repo | none. Just ask for the change directly |

## Rules

- Only route to skills that exist in this plugin. If a skill named above is missing from the
  install, say so.
- User-invoked skills (`/mission-brief`, `/ship-oss`, `/launch-kit`) can only be started by the
  user. Tell them the command; don't try to run it for them.
- No upselling: if the user's task is small, the right answer is often "you don't need a skill for
  this."
