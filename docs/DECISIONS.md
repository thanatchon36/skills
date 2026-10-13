# Decisions

One line of rationale each. Newest at the bottom.

## Tagline

Candidates:

1. **Agent skills that take an open-source project from a one-page MISSION.md to a shipped public repo.**
2. From MISSION.md to a shipped repo: agent skills for open-source builders.
3. Write the brief. Your agent ships the repo, and stops before anything goes public.
4. Agent skills for shipping open source: brief, build, README, release, launch.

**Picked 1.** It states the angle exactly as the brief positions it, names the artifact a reader can
inspect (MISSION.md), and avoids a slogan that promises more than the skills do.

## Phase 0 and 1

- **Build in `~/github/skills` rather than a new `thanatchon-skills/` folder.** The session started
  there. The GitHub repo name comes from `gh repo create`, not the local folder name.
- **`MISSION.md` moved to `docs/mission/MISSION.md`** (the brief says to commit it there). The root
  copy was removed after a byte-for-byte comparison.
- **Only verdrift is a promoted showcase.** It is the only public repo with a full README and an
  install verified here. The others fail the "working install" bar (see
  `docs/research/promoted-repos.md`).
- **"More from me" lists gemini-candlestick and nvidia-gpu-operator-k8s-cluster only.** They have
  real READMEs. Title-only and off-topic repos would be noise for an engineering audience.
- **The case study does not claim verdrift's MISSION.md is public**, because it isn't in that repo.
  It links the real commits, CI run, and release, and uses this repo's brief as the readable example.
- **The brief's karpathy claim was corrected.** Only 2 of 4 principles have a "The test:" line, and
  the repo has no LICENSE file (recorded in the teardown).

## Docs vs brief

- **`plugin.json` `skills` adds to the default `skills/` scan** rather than replacing it (per the
  manifest reference). The default scan only reads one level deep, so the bucketed layout still
  ships exactly the listed skills. This is confirmed by the install test.
- **`npx skills` discovers `skills/<category>/<name>/`, which includes `in-progress/`.** Drafts carry
  `metadata: { internal: true }`, the CLI's supported way to hide a skill, and stay on `main`.
- **User-invoked skills can't be reached through the Skill tool**, so their should-trigger eval cases
  send the slash command and grade the outcome. Their near-miss cases check that natural phrasing
  does not load them.

## Evals and cost

- **Iterate with `--runs 1 --ablation none`, and run the final suite once with a `--max-cost-usd`
  ceiling.** Every eval run is billed model usage, so the full default (3 runs × 2 arms) is reserved
  for the final pass.
- **Eval runs paused at the account session limit** (hit 2026-10-12 ~18:15 ICT, resets 22:40 ICT).
  The `ship-oss` model-graded cases, and all `launch-kit` and `ask-thanatchon` cases, run in one
  batch after the reset. Authoring, validation, and install tests continue meanwhile, since they
  need no model calls.

- **Repo name is `thanatchon36/skills`, not `thanatchon36/thanatchon-skills`.** The owner chose the
  shorter name on 2026-10-13 and created the empty repo. Only the GitHub URL changes: the plugin
  name stays `thanatchon-skills` and the marketplace stays `thanatchon`, so the install is
  `/plugin install thanatchon-skills@thanatchon` as before.

- **No homepage URL on the GitHub repo.** The brief asks for one, but there is no project site and
  `author_links` is empty, so there is nothing true to put there. Set it when a site exists.

## eval-harness (2026-10-13)

The draft's three open questions, and how they were settled:

- **Where cases come from with no logs.** Use known failures first, then synthetic cases for the
  gaps, each marked `source: synthetic`, and say in the report that there were no logs.
  `evalset.py check` warns when every case is synthetic. Real inputs always come first when they
  exist.
- **Default graders and judge cost.** Use deterministic graders first (exact match, contains or
  regex, schema, code). Use an LLM judge only for what those can't decide: one pass/fail criterion
  per call, calibrated against about 10 hand-labeled outputs. The skill states the call count and
  waits for a yes before spending the user's quota.
- **Storage.** JSONL, one case per line, with `id`, `input`, `expected` or `criteria`, `source`,
  and `tags`. Results use the same ids, so `compare` can refuse two runs over different cases.
- **Significance.** `compare` reports an exact two-sided sign test on the flipped cases. It's the
  simplest test that fits paired pass/fail results, and it needs nothing outside the standard
  library. The skill treats p > 0.05 with no must-not-regress movement as "inconclusive".
- **Bucket.** `data-ml`, next to `leakage-audit`.
