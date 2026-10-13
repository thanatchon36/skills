---
max_turns: 20
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Bash]
tags: [eval-harness, trigger, outcome]
---

We rewrote the system prompt for our support bot and ran our 30-case eval set on the old and the new prompt. The results are in results/. Is the new prompt better? Should we ship it?
