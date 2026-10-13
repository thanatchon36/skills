---
max_turns: 15
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
tags: [eval-harness, trigger]
---

We're changing the chunk size in our RAG pipeline from 512 to 1024 tokens. Before I merge it, how should I test that it isn't worse?
