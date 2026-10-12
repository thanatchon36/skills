---
name: model-card
description: "Draft, not shipped: Write a model card from a training repo."
metadata:
  internal: true
---

# model-card (in progress)

Not shipped in the plugin, and hidden from `npx skills` (`metadata.internal: true`). Feedback
welcome in issues.

**Purpose.** Write a model card (intended use, data, metrics with their split, limitations, ethical considerations) from what the training code and eval outputs actually show, and mark unknowns.

**Trigger idea.** "write a model card", or preparing a model for release or internal review.

**Open questions before it can ship**

- Which template to align with (Mitchell et al. 2019, or Hugging Face's).
- How to source metrics: only from files in the repo, never from memory.
- How to tie it into AI governance checklists without bloating it.
