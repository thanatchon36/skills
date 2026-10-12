---
name: leakage-audit
description: Audit Python ML training code (pandas, scikit-learn, PySpark) for data leakage, covering target leakage, temporal leakage, train/test contamination, and preprocessing fit on the full dataset, and report each finding with file:line, evidence, and a fix. Use when reviewing or writing code that splits data and trains or evaluates a model, when validation or test scores look too good to be true, when a model degrades in production after strong offline metrics, or when the user says "check for leakage", "is my split right", "audit this pipeline", or "/leakage-audit". Not for general code review, model tuning, or performance work without an evaluation question.
---

# leakage-audit

Find every place where information from the evaluation data, or from after the prediction time,
reaches training. Cite each finding at `file:line`.

## When NOT to use

- General code review, style, or performance work. Leakage is the only question here.
- Choosing models or tuning hyperparameters, unless the question is whether the selection itself
  leaks.
- Pipelines with no train/evaluate step (pure ETL, inference-only services). Say so and stop.
- Notebooks you can't read as text. Ask for a `.py` export (`jupyter nbconvert --to script`).

## Workflow

Do the steps in order. Do not skip ahead.

### 1. Map the pipeline

Read the training code end to end. Write down, with `file:line`:

- **Load**: where rows come from, and what one row is (a customer, an event, a day).
- **Label**: which column, and when its value becomes known.
- **Problem shape**: i.i.d. rows, time-ordered (forecasting, or "predict later from earlier"), or
  grouped (an entity has many rows).
- **Split**: the exact line(s) that separate training from evaluation data, including CV.
- **Fits**: every stateful fit (scalers, imputers, encoders, selectors, models, searches).
- **Evaluation**: every line that scores on held-out data.

To speed this up, list candidate lines with the bundled scanner:

```sh
python3 "${CLAUDE_SKILL_DIR}/scripts/find_candidates.py" <paths>
```

(Outside Claude Code: `scripts/find_candidates.py` next to this file.) It flags fits before the
first split, future-looking windows, test-set scoring, and post-outcome-sounding column names. It
finds candidates, not findings.

### 2. Gate: no split, no verdict

If you can't find where training and evaluation data separate (the split is in another repo, a SQL
view, or a notebook you weren't given), stop. Report what you mapped, and say the audit can't
conclude without the split. Never call a pipeline clean without having read its split.

### 3. Check each leak class

Work through `references/leak-catalog.md` class by class for every file in scope:

1. Target leakage
2. Temporal leakage (only if the problem is time-ordered, but decide that explicitly)
3. Train/test contamination (entity overlap, duplicates, test-set-driven selection)
4. Preprocessing fit on the full dataset

For each candidate, answer the catalog's confirming question by tracing data flow in the code:
which rows did this fit or aggregate see, and when is this value known? Then mark it:

- **confirmed**: the code shows evaluation rows or future values reaching training.
- **suspected**: the code gives a concrete signal of a leak (a post-outcome-sounding name, a join to
  an outcome table, a comment, an aggregate over the label) but the verdict hinges on a fact the code
  can't show, usually whether a value exists at prediction time. Say exactly what to check.
- **assumption, not a finding**: a plain input column with no such signal. "It might be built
  from future data upstream" is true of every column, so it is not a finding. Note it at most once,
  under Assumptions.
- **not a leak**: drop it. Use the catalog's "Not leakage" list.

### 4. Report

Use the output contract below. One finding per root cause and location. If the same fit leaks
into two places, report it once and mention both.

### 5. Fix (only when asked)

If the user asks for fixes, make the smallest change per finding (move the fit into a `Pipeline`,
switch to a group or time split, drop the column), then repeat steps 1 to 4 on the changed code
and show the new count. Expect test metrics to drop after a real fix, and say so up front, so a
lower score isn't read as a regression.

## Output contract

```text
Leakage audit: <N> findings (<C> confirmed, <S> suspected) in <files audited>

Pipeline: rows = <unit>; label = <column, known when>; shape = <iid | time-ordered | grouped>;
split = <file:line>

| # | Location | Class | Status | Evidence | Fix |
| 1 | churn_model.py:25 | preprocessing fit on full data | confirmed | StandardScaler.fit_transform(X) runs before train_test_split at :27 | fit the scaler inside a Pipeline on X_train |
...

Checked and clean: <classes with no findings, one line each with the reason>
Assumptions: <upstream inputs taken as point-in-time, if any; not counted as findings>
```

- If there are no findings, the first line is `Leakage audit: 0 findings`, followed by the
  pipeline map and the "checked and clean" lines. Don't pad it with style notes or
  "consider also" suggestions.
- Every finding cites the line where the leak happens. Add the related line (the split, the
  evaluation) in the evidence.

## Operating rules

- Read the code. Don't infer the split from file names, comments, or docstrings.
- Distinguish target construction from features: `shift(-1)` that builds the label is correct.
- A pandas statistic computed on the whole frame (`mean()`, `max()`, `quantile()`) is a fit.
- Don't run the training code to "check". Leakage is visible statically, and running it may cost
  hours or touch production data. Run the scanner only.
- Don't add comments, badges, or tool mentions to the user's code when fixing.

## Done-check

- [ ] The split location is cited, or the audit stopped at the gate.
- [ ] All four classes were checked for each file, and each is either a finding or listed under
      "Checked and clean" with a reason.
- [ ] Every finding has `file:line`, a class, a status, evidence, and a fix.
- [ ] Suspected findings say exactly what fact would confirm or clear them.
