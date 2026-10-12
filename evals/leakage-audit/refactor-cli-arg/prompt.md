---
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill, Edit]
tags: [near-miss]
---

In churn_model.py, read the parquet path from a --data command-line argument (argparse) instead of hardcoding it. Keep the current path as the default. Only that change.
