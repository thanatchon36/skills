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
