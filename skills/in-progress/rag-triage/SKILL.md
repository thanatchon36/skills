---
name: rag-triage
description: "Draft, not shipped: Classify RAG failures as retrieval, ranking, or generation."
metadata:
  internal: true
---

# rag-triage (in progress)

Not shipped in the plugin, and hidden from `npx skills` (`metadata.internal: true`). Feedback
welcome in issues.

**Purpose.** Given failing RAG answers, decide for each one whether the right chunk was never retrieved, was retrieved but ranked out of context, or was in context and the model ignored or misread it. Then point to the fix for that layer.

**Trigger idea.** "the chatbot answers wrong", "RAG is hallucinating", or a list of bad answers with their retrieved chunks.

**Open questions before it can ship**

- What minimum logging is needed (query, top-k ids, scores, final context).
- How to triage without gold chunk labels.
- A deterministic script for recall@k when labels exist.
