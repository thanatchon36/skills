---
name: backtest-honesty
description: "Draft, not shipped: Audit trading backtests for look-ahead bias, survivorship, and missing costs."
metadata:
  internal: true
---

# backtest-honesty (in progress)

Not shipped in the plugin, and hidden from `npx skills` (`metadata.internal: true`). Feedback
welcome in issues.

**Purpose.** Check a backtest for look-ahead bias (signals using same-bar close or later data), survivorship bias (a universe of today's constituents), and missing transaction costs and slippage, citing file:line.

**Trigger idea.** backtest code in pandas or vectorbt-style libraries, or "the strategy returns look too good".

**Open questions before it can ship**

- How much of this overlaps with leakage-audit's temporal checks, and whether to merge them.
- Sensible default cost and slippage assumptions per asset class, or always asking.
- Handling corporate actions and delisted symbols.
