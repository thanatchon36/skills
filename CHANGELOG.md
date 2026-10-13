# Changelog

## 0.1.0 (2026-10-13)

First release. Seven skills:

- `mission-brief` (user-invoked): turn an idea into a MISSION.md by interview.
- `ship-oss` (user-invoked): execute a MISSION.md, with phase checks and stop gates.
- `launch-kit` (user-invoked): launch drafts in `launch/`. Never posts.
- `readme-that-converts`: write or review a README, with a lint script.
- `runtime-drift`: Node, Python, and Go version drift via verdrift v0.1.0, with a manual fallback.
- `leakage-audit`: data leakage audit for pandas, scikit-learn, and PySpark code.
- `ask-thanatchon` (user-invoked): a router over the skills.

Also: eval suites for every skill, fixtures (a drifted repo, leaky and clean ML pipelines, and a
small CLI project), and CI that runs validation, the frontmatter lint, and a link check.
