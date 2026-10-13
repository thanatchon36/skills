NOT READY: no v0.1.0 release yet, and the README's first screen has no real example (it starts at line 64). Post after both are fixed.

# Show HN

**Title** (73 chars):

Show HN: Agent skills that ship an open-source repo from a one-page brief

**URL:** https://github.com/thanatchon36/skills

**First comment (from the author):**

I'm the author. These are seven agent skills, packaged as a Claude Code plugin and installable
into other agents with `npx skills`. They cover the part of an open-source project that comes after
the code: deciding what "done" means, writing a README a stranger can act on, cutting a release,
and drafting the announcement.

Agents tend to skip that part: they invent output for READMEs, skip verification, and make
things public before anyone has looked. TBD: one sentence of your own experience, if you have one
that's true. The three
user-invoked skills form a flow. /mission-brief interviews you one question at a time and writes a
MISSION.md. /ship-oss executes it phase by phase and stops for an explicit "go" before creating a
repo, pushing, tagging, or releasing. /launch-kit drafts posts like this one and never posts them.

Three skills work on their own. runtime-drift runs verdrift (another project of mine, pinned to
v0.1.0, and it says so before running) to find disagreeing Node, Python, and Go versions.
leakage-audit checks pandas, scikit-learn, and PySpark code for data leakage, with file:line for
each finding. readme-that-converts writes or reviews READMEs and ships a lint script.

Each skill has at least 3 prompts that should trigger it and 3 that must not, run with
`claude plugin eval`. Where the outcome is checkable, the graders check it. For example,
leakage-audit must find all 8 leaks planted in a fixture and report 0 on the fixed twin. Results,
including the runs that didn't complete, are in docs/evals.md.

Limits: it has only been tested with Claude Code, runtime-drift needs Node 22 and network access,
and leakage-audit reads code statically, so it can't see leaks in upstream SQL.

I'd most like to hear about prompts where a skill fired when it shouldn't have, or didn't fire
when it should have.
