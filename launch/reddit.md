NOT READY: the README's first screen has no real example (it starts at line 64), and this draft describes the 7 skills of v0.1.0, not the 8 in v0.2.0 (eval-harness is missing). Fix both before posting.

# Reddit

Post to one subreddit at a time, a day or more apart. Read each sidebar first. Self-promotion
rules change and differ between communities.

## 1. r/ClaudeAI

- **Why:** the main install route is a Claude Code plugin.
- **Rule to check:** the self-promotion and flair rules. Some days or threads may be required.
- **Title:** I wrote Claude Code skills that stop before anything goes public (MIT)
- **Post:**

  I'm the author. This is a plugin with 7 skills for the non-code half of an open-source project.
  /mission-brief writes a MISSION.md through an interview, /ship-oss executes it and stops for
  "go" before creating a repo, pushing, tagging, or releasing, and /launch-kit drafts posts and
  never posts. There are also three standalone skills: README writing, runtime-version drift, and
  ML data leakage.

  Install: `/plugin marketplace add thanatchon36/skills`, then
  `/plugin install thanatchon-skills@thanatchon`.

  Each skill has trigger and near-miss evals run with `claude plugin eval`, and the results are
  in docs/evals.md. I'm looking for prompts where a skill misfires.

  https://github.com/thanatchon36/skills

## 2. r/datascience

- **Why:** leakage-audit is useful there on its own, and the post can lead with it.
- **Rule to check:** the self-promotion rules. Some data subreddits require a weekly thread.
- **Title:** An agent skill that audits pandas/sklearn/PySpark code for data leakage, with file:line
- **Post:**

  I'm the author. leakage-audit is an agent skill that maps your pipeline and checks it for four
  kinds of leakage: target leakage, temporal leakage, train/test contamination, and preprocessing
  fit before the split. Each finding cites a file:line. If it can't find where the split happens,
  it says so instead of giving a verdict.

  Its eval plants 8 leaks across three scripts. The skill must find all 8 at the right lines, and
  report 0 findings on the fixed version. It reads code statically, so it can't see leaks in
  upstream SQL or a feature store.

  https://github.com/thanatchon36/skills (one skill in a larger plugin)

## 3. r/opensource

- **Why:** the main flow is about shipping open-source projects.
- **Rule to check:** whether self-made project posts are allowed and how to flair them.
- **Title:** Agent skills for the non-code half of releasing an open-source project
- **Post:** lead with the problem (agents skip scope, the README, the release, and the launch),
  then the three-skill flow and the gates. Mention the MIT license and that the brief for this
  repo is public at docs/mission/MISSION.md.
