# In progress

Drafts. They are not listed in `.claude-plugin/plugin.json`, so the plugin doesn't ship them, and
each has `metadata.internal: true`, so `npx skills` hides them unless `INSTALL_INTERNAL_SKILLS=1` is
set. They may change or disappear.

- [eval-harness](./eval-harness/SKILL.md): build an LLM or RAG eval set before changing prompts or models.
- [rag-triage](./rag-triage/SKILL.md): classify RAG failures as retrieval, ranking, or generation.
- [backtest-honesty](./backtest-honesty/SKILL.md): look-ahead bias, survivorship, costs and slippage.
- [model-card](./model-card/SKILL.md): a model card from what the training repo actually shows.
