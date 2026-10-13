---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
tags: [eval-harness, trigger, outcome]
---

We want to move our support bot (bot.py) to a cheaper model. How do we make sure the replies don't get worse? Set up whatever we need to check that, but don't call the API yet.
