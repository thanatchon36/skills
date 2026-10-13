---
name: eval-harness
description: Build a small, labeled eval set and a baseline score for an LLM or RAG feature before a prompt, model, or retrieval change, then compare the change against the baseline case by case. Use when someone is about to switch models, rewrite a system prompt, change chunking, retrieval, or reranking, or asks "is the new prompt better", "will a cheaper model get worse", "how do I test my LLM feature", "set up evals", or "/eval-harness"; also when results from two eval runs need comparing. Not for unit tests of ordinary code, classic ML metrics (accuracy, F1, AUC) in a training script, public benchmarks like MMLU, or latency and cost measurements alone.
---

# eval-harness

Judge an LLM change by how it does on a fixed set of real cases compared with the current system,
not by trying a few prompts and reading the output.

## When NOT to use

- Ordinary code with deterministic output. Write unit tests.
- Classic ML training code (accuracy, F1, AUC on a held-out split). If the score looks too good,
  that is a leakage question, not this one.
- Public benchmark runs (MMLU, HumanEval), or pure latency and cost measurement.
- An eval set already exists and covers the change. Use it: skip to step 6.

## Workflow

Do the steps in order. Do not skip ahead.

### 1. Pin the decision

Write down, in one line each:

- **Change**: what is being compared (model A vs model B, prompt v1 vs v2, chunk size 512 vs 1024).
- **Better means**: the behavior that must improve, in terms someone could grade.
- **Must not regress**: the behaviors that block shipping if they get worse (safety, policy,
  refusals, format). These become tags, and a regression in one of them is reported separately.
- **Entry point**: the function or command that turns one input into one output, at `file:line`.

If you can't name the entry point, ask for it. Don't write a new client for the model.

### 2. Gate: look for an existing eval

Search the repo for an eval set or test fixtures of inputs and outputs (`evals/`, `*.jsonl`,
`promptfoo`, `ragas`, `deepeval`, `pytest` files that call the model). If one exists and covers
the change, use it and go to step 6. If it exists but misses the change, extend it. Don't build a
second, competing set.

### 3. Collect cases

Take cases in this order, and record each case's `source`:

1. **real**: inputs from logs, tickets, or traffic. Sample across categories, not just the first
   N lines. Strip personal data (names, emails, phone numbers, card numbers) before writing a case,
   and say that you did.
2. **failure**: the inputs that prompted the change, plus logged inputs with bad outcomes
   (escalations, thumbs-down, retries).
3. **synthetic**: only to fill gaps the real data doesn't cover, such as policy edges, other
   languages, adversarial inputs, and empty or garbage input. Mark them, and keep them under half
   of the set.

Aim for at least 30 cases. With 30, one case moves the pass rate by about 3 points. With 10, it
moves it by 10, and almost any difference is noise. If there are no logs at all, say so in the
report, build the set from failures and synthetic cases, and plan to swap in real inputs later.

### 4. Write the expectations and graders

Write the set as JSONL, one case per line (default `evals/<feature>/cases.jsonl`):

```json
{"id": "refund-03", "input": "...", "criteria": ["states the 30-day window", "does not promise a refund for a used item"], "source": "real", "tags": ["refund", "policy"]}
```

Use `expected` when there is one right answer and `criteria` when there are several acceptable
ones. Pick the cheapest grader that can decide each criterion, following
`references/graders.md`: an exact match, contains or regex, a schema check, or code first, and an
LLM judge only for what those can't decide.

Then validate the file:

```sh
python3 "${CLAUDE_SKILL_DIR}/scripts/evalset.py" check evals/<feature>/cases.jsonl
```

(Outside Claude Code: `scripts/evalset.py` next to this file.) Fix every error. Report the
warnings rather than hiding them.

### 5. Gate: graders can fail

Before any real run, feed the graders two outputs per grader type, one that should pass and one
that should fail. Write them by hand, or take a known-bad output from the logs. A grader that
passes both is broken. Fix it before going further. For an LLM judge, also check it against about
10 outputs you labeled yourself, and report how often it agreed with you.

### 6. Run the baseline

Write a runner that calls the entry point from step 1 for each case and writes
`results/<label>.jsonl`, one `{"id", "pass", "tags"}` line per case. Keep raw outputs next to it
so failures can be read.

Before running, tell the user the number of calls (cases × runs, plus judge calls) and that it
uses their API key and quota. Wait for a yes. If credentials aren't available, stop here, hand
over the runner and the set, and say the baseline hasn't been run.

If the system is non-deterministic, run it 3 times and count a case as passing only if it passed
every run, or report the pass rate per case. Say which.

### 7. Run the candidate and compare

Run the change on the same cases with the same graders, then:

```sh
python3 "${CLAUDE_SKILL_DIR}/scripts/evalset.py" compare results/baseline.jsonl results/candidate.jsonl
```

Read the flips (cases that changed between pass and fail), not only the totals. A higher pass rate
with regressions in a must-not-regress tag is a "don't ship" until those are fixed or accepted.

## Output contract

Start the final message with this block, filled in, every time, including when you stopped before
running anything:

```text
Eval set: <N> cases (<r> real, <f> failure, <s> synthetic) in <path>
Redacted: <what personal data was removed or replaced, and how | none found>
Baseline: <pass>/<N> | not run (<reason>)
Candidate: <pass>/<N> | not run
Flips: <k> fixed, <m> regressed (sign test p=<p>)
Must-not-regress: <tag: before -> after, for each such tag>
Verdict: <ship | don't ship: reason | inconclusive: reason>
```

- If a line doesn't apply yet, keep it and say why (`Baseline: not run (waiting for your yes to
  the API calls)`, `Verdict: none yet`). Don't drop it.
- Quote the numbers from `evalset.py` output. Never estimate a pass rate.
- "Inconclusive" is the right verdict when the flips are few and split both ways (sign test
  p > 0.05) and nothing in a must-not-regress tag moved. Say what would settle it, usually more
  cases in the categories that flipped.
- List the regressed case ids, and for each one, one line on what went wrong in the output.

## Operating rules

- Never tune the change on the eval cases and then report the score on the same cases. If the
  prompt was edited while looking at failures, hold out at least a third of the set and report it
  separately.
- Don't change graders or expectations between the baseline and the candidate. If a grader was
  wrong, fix it and rerun both.
- Don't call a model or spend quota without the user's yes from step 6.
- Keep the set in the repo, diffable, one case per line. Never include secrets or unredacted
  personal data.

## Done-check

- [ ] The change, "better", and the must-not-regress tags are written down.
- [ ] `evalset.py check` passes, and its counts appear in the report.
- [ ] The final message starts with the output contract block, with every line present.
- [ ] Each grader type was shown to fail on a bad output.
- [ ] Baseline and candidate ran on identical cases and graders, or the report says what wasn't run.
- [ ] The verdict follows from the flips and the must-not-regress tags, not from the totals alone.
