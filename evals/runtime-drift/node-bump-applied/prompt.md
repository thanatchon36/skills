---
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash, Edit, Write]
tags: [runtime-drift, trigger, outcome]
---

We're dropping Node 20 and moving this repo to Node 22. Update every file that needs it so local, Docker and CI all agree on 22, then confirm nothing is left over for Node.
