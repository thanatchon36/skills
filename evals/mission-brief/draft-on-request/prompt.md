---
max_turns: 20
timeout_seconds: 400
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write]
tags: [mission-brief, trigger, outcome]
---

/thanatchon-skills:mission-brief mdlinks: a CLI that finds broken links in a repo's Markdown files

I already know the answers, so draft it now and write MISSION.md directly, no need to confirm the draft with me. Users: maintainers of docs-heavy repos who find broken links only after readers report them. Goal: one command that lists every broken relative link and anchor with file:line. Not doing external URL checks in v0.1. Success: finds all broken links in a fixture repo and exits non-zero; runs in under 2 seconds on 1,000 files. Node 22+, zero runtime dependencies, published to npm as mdlinks. MIT license. Owner: example-dev, repo mdlinks. Stop before creating the repo, any push, tag, or npm publish.
