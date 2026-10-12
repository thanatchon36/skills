---
name: eval-harness
description: "Draft, not shipped: Build an LLM or RAG eval set before changing prompts or models."
metadata:
  internal: true
---

# eval-harness (in progress)

Not shipped in the plugin, and hidden from `npx skills` (`metadata.internal: true`). Feedback
welcome in issues.

**Purpose.** Before a prompt, model, or retrieval change, build a small labeled eval set from real traffic and a baseline score, so the change is judged by numbers rather than vibes.

**Trigger idea.** "switch to model X", "tweak the system prompt", or edits to prompt files when no eval set exists.

**Open questions before it can ship**

- Where the cases come from when there are no production logs yet.
- Which grader types to recommend by default (exact match, rubric, pairwise), and how to keep judge cost bounded.
- How to store the set so it's diffable (JSONL, with one case per line).
