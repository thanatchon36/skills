NOT READY: the README's first screen has no real example (it starts at line 64), and this draft describes the 7 skills of v0.1.0, not the 8 in v0.2.0 (eval-harness is missing). Fix both before posting.

# LinkedIn

Coding agents are good at writing code. They are much worse at the other half of shipping an
open-source project.

They skip verification, put invented output in READMEs, and make things public before anyone has
reviewed them. TBD: your own example, if you have a true one. I wrote seven agent skills for that
half, packaged as a Claude Code plugin.

The main flow has three steps. /mission-brief interviews you and writes a one-page brief with
checkable success criteria. /ship-oss executes the brief phase by phase, and it stops for an
explicit "go" before anything becomes public. /launch-kit drafts announcement posts and never
posts them.

There are also three standalone skills: a README writer and reviewer, a runtime-version drift
checker, and a data-leakage audit for pandas, scikit-learn, and PySpark code.

TBD: rewrite in your own words. One lesson: the useful part of a skill is often what it refuses to do. Each one says when not
to use it, and the evals check that too. Every skill has prompts that must not trigger it.

It's MIT-licensed and tested with Claude Code. Other agents can install it through npx skills, but
I haven't tested those yet.

https://github.com/thanatchon36/skills

Reports of a skill firing at the wrong time are the most useful feedback I can get.
