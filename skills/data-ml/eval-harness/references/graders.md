# Choosing graders

Use the cheapest grader that can decide the criterion. Deterministic graders cost nothing, give
the same answer every time, and can't be talked into passing. An LLM judge is for what they can't
decide.

| Criterion looks like | Grader | Example |
| --- | --- | --- |
| One right answer | exact match after normalizing (case, whitespace) | a category label, a yes/no |
| Must mention or must not mention | contains, or regex | "states the 30-day window": `30[- ]day` |
| Structured output | parse it and check the schema and the values | JSON with `intent` in an allowed set |
| A computable property | code | word count ≤ 120, the cited doc id exists, a SQL query runs |
| Retrieval quality (RAG) | hit@k, or recall@k against labeled relevant doc ids | the refund policy doc is in the top 5 |
| Tone, helpfulness, faithfulness to sources | LLM judge with a rubric | "the answer uses only facts from the retrieved passages" |

## Rules for an LLM judge

- One criterion per judge call, answered pass or fail, with a one-line reason. Don't ask for a
  1–10 score. Scores drift between runs, and nobody knows what a 6 means.
- Write the rubric as observable checks: "mentions that refunds take 5–7 business days" instead
  of "is accurate".
- Give the judge what it needs and nothing more: the input, the output, and the reference or
  retrieved passages when the criterion depends on them.
- Use a different, fixed model version for the judge, and record which one it is in the results.
- Calibrate before trusting it. Label about 10 outputs yourself, including some failures, run the
  judge on them, and report the agreement. If it disagrees with you on more than 2 of 10, rewrite
  the rubric before using it.
- Bound the cost. Run the judge only on criteria a deterministic grader can't decide, and give the
  user the judge call count (cases × judged criteria × runs) before running.

## Pairwise comparison

Asking "which output is better, A or B?" is useful for open-ended quality when both outputs pass
the hard criteria. Randomize which side each output is on, since judges favor one position. Count
wins, losses, and ties per case, and treat it as a separate report from the pass/fail set rather
than mixing the two.

## RAG: grade the stages separately

When a RAG answer is wrong, find out which stage failed before changing anything:

- **Retrieval**: was a relevant passage in the top k? Label relevant doc ids per case and compute
  recall@k. No relevant passage in the top k means that changing the prompt can't fix the case.
- **Generation**: given relevant passages, is the answer faithful to them and complete?

Report both numbers. A chunking or embedding change should move retrieval. A prompt change should
move generation and leave retrieval unchanged.

## Non-determinism

With temperature above 0, or with providers that aren't deterministic at 0, one run per case
isn't a measurement. Run each case 3 times. Either count a case as passing only if it passes
every run, which is strict and good for must-not-regress tags, or report the pass rate per case.
Use the same rule for the baseline and the candidate.
