# Eval results

**Status: complete.** 42 of 43 cases passed all 3 runs. One case, `runtime-drift/reports-all-four`,
passed 1 of 3. The reason is explained under Notes.

## Run

| | |
| --- | --- |
| Date | 2026-10-13, in two runs: all skills, then `runtime-drift` and `ship-oss` again with `--tag`, because their first runs hit the account's session limit |
| Claude Code | 2.1.296 |
| Command | `claude plugin eval . --runs 3 --ablation none --scaffold -j 6 --allow-tools Bash Write Edit "WebFetch(domain:github.com)" "WebFetch(domain:codeload.github.com)" "WebFetch(domain:registry.npmjs.org)" --trust-plugin --no-publish` |
| Runs per case | 3, with-skill arm only (`--ablation none`, so there is no baseline comparison) |
| Pass rule | Every grader passes (threshold 1.0) |
| Cost | $22.41 in total ($15.86 + $6.55), including the runs that hit the session limit |

Runs that ended with "You've hit your session limit" are left out of this page. Every case has 3
complete runs.

## Results

| Skill | Case | Kind | Passed |
| --- | --- | --- | --- |
| ask-thanatchon | ci-docker-versions | trigger | 3/3 |
| ask-thanatchon | idea-to-brief | trigger | 3/3 |
| ask-thanatchon | model-too-good | trigger | 3/3 |
| ask-thanatchon | no-fit | trigger | 3/3 |
| ask-thanatchon | recommend-tool | near-miss | 3/3 |
| ask-thanatchon | what-is-plugin | near-miss | 3/3 |
| ask-thanatchon | which-skill-generic | near-miss | 3/3 |
| launch-kit | drafts-all-channels | trigger | 3/3 |
| launch-kit | nothing-to-launch | trigger | 3/3 |
| launch-kit | refuses-unverified-claim | trigger | 3/3 |
| launch-kit | hn-advice | near-miss | 3/3 |
| launch-kit | release-tweet | near-miss | 3/3 |
| launch-kit | topics-question | near-miss | 3/3 |
| leakage-audit | clean-twin-zero | trigger | 3/3 |
| leakage-audit | finds-all-eight | trigger | 3/3 |
| leakage-audit | forecast-split-question | trigger | 3/3 |
| leakage-audit | add-docstrings | near-miss | 3/3 |
| leakage-audit | model-choice-question | near-miss | 3/3 |
| leakage-audit | refactor-cli-arg | near-miss | 3/3 |
| mission-brief | asks-one-question | trigger | 3/3 |
| mission-brief | draft-on-request | trigger | 3/3 |
| mission-brief | no-args-asks-idea | trigger | 3/3 |
| mission-brief | brief-sections-question | near-miss | 3/3 |
| mission-brief | feature-plan | near-miss | 3/3 |
| mission-brief | notes-to-readme | near-miss | 3/3 |
| readme-that-converts | review-only | trigger | 3/3 |
| readme-that-converts | rewrite-wall-of-text | trigger | 3/3 |
| readme-that-converts | write-from-scratch | trigger | 3/3 |
| readme-that-converts | api-reference | near-miss | 3/3 |
| readme-that-converts | changelog-entry | near-miss | 3/3 |
| readme-that-converts | contributing-doc | near-miss | 3/3 |
| runtime-drift | concept-question | near-miss | 3/3 |
| runtime-drift | library-upgrade | near-miss | 3/3 |
| runtime-drift | node-bump-applied | trigger | 3/3 |
| runtime-drift | python-where-declared | trigger | 3/3 |
| runtime-drift | reports-all-four | trigger | **1/3** |
| runtime-drift | release-version | near-miss | 3/3 |
| ship-oss | adds-default-gate | trigger | 3/3 |
| ship-oss | builds-then-stops-at-gate | trigger | 3/3 |
| ship-oss | no-mission | trigger | 3/3 |
| ship-oss | ci-workflow | near-miss | 3/3 |
| ship-oss | oss-checklist-question | near-miss | 3/3 |
| ship-oss | semver-question | near-miss | 3/3 |

## eval-harness (after v0.1.0)

Run on 2026-10-13 with the same command plus `--tag eval-harness --tag ask-thanatchon --keep-temp`,
3 runs per case. That run cost $7.49, and the `build-from-logs` re-run cost $3.39. All 7
`ask-thanatchon` cases passed 3/3 again after the router gained the new skill.

| Skill | Case | Kind | Passed |
| --- | --- | --- | --- |
| eval-harness | compare-results | trigger | 3/3 |
| eval-harness | build-from-logs | trigger | 3/3 (after a fix; 0/3 before) |
| eval-harness | rag-chunking | trigger | 3/3 |
| eval-harness | unit-tests | near-miss | 3/3 |
| eval-harness | sklearn-metrics | near-miss | 3/3 |
| eval-harness | latency-script | near-miss | 3/3 |
| eval-harness | metric-concept | near-miss | 3/3 |

`build-from-logs` failed 3/3 on the first run:

- Two runs left out the output contract block.
- No run said in its report that it had replaced the card number in the logs, although every run
  did replace it (with the public test number `4111 1111 1111 1111`, checked in the kept
  workspaces).

The fix was in the skill: the contract block is now required at the top of the final message,
with a new `Redacted:` line. The redaction grader was widened to accept that new line, along
with "replaced" as a verb. After the fix, it passed 3/3.

## Notes

- **`reports-all-four` (1/3):** all 3 runs ran verdrift and reported each of the 4 problems at the
  right file and line, and none of them edited a file. Two runs failed one grader: their final
  message didn't contain "4 problems", which the skill's output contract requires in its summary
  line (`Runtime drift: <N> problems (...)`). The traces weren't kept, so the exact wording is
  unknown. This is a contract miss, not a wrong finding. The grader was left unchanged, and the
  miss is an open TODO.
- Earlier development runs had real failures. These were fixed in the skill:
  - The `leakage-audit` clean twin was flagged as a suspected leak.
  - The `runtime-drift` manual fallback counted one problem twice.
  - `mission-brief` asked compound questions.

  These were fixed in the eval, because the eval was wrong:
  - The `mission-brief` rubric required a recommended answer for a yes/no confirmation question.
  - The `launch-kit` prompts didn't say the repo wasn't public yet, so the skill correctly stopped
    at its readiness gate.
  - The `ship-oss` gate grader only accepted the literal "STOP GATE" and missed "Gate A".
- With three runs per case, a 3/3 doesn't rule out a flaky skill.
- `runtime-drift` takes its deterministic path only when the run can reach GitHub and npm (the
  `WebFetch` grants above). Without them it falls back to the manual checklist, so its output
  differs.
