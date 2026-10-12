---
max_turns: 25
timeout_seconds: 400
allowed_tools: [Read, Glob, Grep, Skill, Bash]
tags: [runtime-drift, trigger, outcome]
---

The api service's Docker image runs Python 3.10 but I think pyproject says 3.11+. Which other places in this repo declare a Python version, and do they agree? Report only, no edits.
