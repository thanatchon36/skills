# thanatchon-skills

Agent skills that take an open-source project from a one-page MISSION.md to a shipped public repo.

> Also from me: [verdrift](https://github.com/thanatchon36/verdrift). Find every place your repo pins a
> Node, Python, or Go version, and see where they disagree.

English | [ภาษาไทย](./README.th.md)

## Install

Claude Code:

```text
/plugin marketplace add thanatchon36/skills
/plugin install thanatchon-skills@thanatchon
```

Any agent supported by [skills.sh](https://skills.sh), including Claude Code, Cursor, Codex, and
others (this copies editable files into your project):

```sh
npx skills@latest add thanatchon36/skills
```

Use one route, not both, or you get every skill twice. Both commands above were tested from GitHub
on 2026-10-13 (Claude Code 2.1.296, skills 1.7.2), and each installs the same 7 skills.

Then, in Claude Code, run `/thanatchon-skills:ask-thanatchon` and describe what you're doing. It
tells you which skill to use.

## The problem

Coding agents can write the code. Shipping an open-source project is the other part: deciding scope,
writing a README a stranger can act on, picking a license, cutting a release, and announcing it.
Agents skip those steps, invent output and metrics, and make things public before anyone has looked.

These skills cover that part. They are small, they each say when not to use them, and the ones
that could publish anything stop and wait for you first.

## What's inside

### The main flow: idea to shipped repo

| You notice... | Skill | What it does |
| --- | --- | --- |
| The agent starts building before anyone has said what "done" means | [`/mission-brief`](./skills/workflow/mission-brief/SKILL.md) | Interviews you one question at a time, each with a recommended answer, and writes a `MISSION.md` with checkable success criteria, phases, and stop gates. |
| A long build drifts, skips verification, or pushes before you've looked | [`/ship-oss`](./skills/workflow/ship-oss/SKILL.md) | Executes the brief phase by phase. Each phase ends with checks it has actually run. It stops for an explicit "go" before repo creation, pushing, tagging, releasing, publishing, or touching other repos. |
| Launch posts that oversell, or the same text pasted everywhere | [`/launch-kit`](./skills/workflow/launch-kit/SKILL.md) | Drafts Show HN, an X thread, LinkedIn, Reddit, Thai developer community posts, GitHub topics, and a social-preview brief in `launch/`. Checks claims against the repo. Never posts. |

User-invoked: these run only when you type them.

### Standalone skills

These fire on their own when the task matches, or you can ask for them by name.

| You notice... | Skill | What it does |
| --- | --- | --- |
| People star the repo but never try it | [`readme-that-converts`](./skills/workflow/readme-that-converts/SKILL.md) | Writes or reviews a README: the problem in the first sentence, the install on the first screen, real output from a real run, and limitations. Ships a lint script. |
| `.nvmrc` says 22, the Dockerfile says 20, CI tests 18 | [`runtime-drift`](./skills/engineering/runtime-drift/SKILL.md) | Runs [verdrift](https://github.com/thanatchon36/verdrift) (pinned to v0.1.0, and it tells you before it runs) and proposes the smallest set of edits. Falls back to a manual checklist without Node 22 or network. |
| A model scores 0.99 offline and falls apart in production | [`leakage-audit`](./skills/data-ml/leakage-audit/SKILL.md) | Checks pandas, scikit-learn, and PySpark code for target leakage, temporal leakage, train/test contamination, and preprocessing fit on the full data. Each finding gets a `file:line`. |
| You're about to switch models or rewrite a prompt, and the only test is trying a few inputs | [`eval-harness`](./skills/data-ml/eval-harness/SKILL.md) | Builds a JSONL eval set from your real inputs and known failures, checks that the graders can fail, runs a baseline (after you say yes to the API calls), and compares the change case by case, with flips and a sign test. |
| You don't remember which skill fits | [`/ask-thanatchon`](./skills/meta/ask-thanatchon/SKILL.md) | A router over the skills above, and it says when you don't need one. |

## Example: `runtime-drift` on a drifted repo

Asked "Check this repo for Node and Python version mismatches... and list every problem with its
file and line", run against [`fixtures/runtime-drift/drifted`](./fixtures/runtime-drift/drifted), the
skill runs verdrift. These are the 4 problems verdrift reports:

```text
✗ .github/workflows/ci.yml:24  python 3.10 (setup-python python-version) is a YAML number, so the action receives "3.1". Quote it: '3.10'  yaml-number
✗ .github/workflows/ci.yml:8   node 18 (setup-node matrix.node) is outside ">=20" (package.json:5 engines.node)  outside-range
✗ Dockerfile:1                 FROM node:20-alpine disagrees with 22 (.nvmrc:1)  pin-mismatch
✗ api/Dockerfile:1             FROM python:3.10-slim is outside ">=3.11" (api/pyproject.toml:4 requires-python)  outside-range
```

The skill then returns one proposed edit per problem, each with a reason, and leaves the files
alone unless you asked for the fix.

## How it's tested

Every shipped skill has at least 3 prompts that should trigger it and 3 near-miss prompts that must
not, run with [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals). Where the outcome
is checkable, the graders check it:

- `runtime-drift` must report verdrift's 4 problems on the fixture above.
- `leakage-audit` must cite all 8 leaks planted in [`fixtures/leakage/leaky`](./fixtures/leakage/EXPECTED.md)
  at the right lines, and report 0 findings on the fixed twin.
- `readme-that-converts` must put real output from the fixture project in the README.
- `ship-oss` must build a small brief and stop at the gate without running `git push` or
  `gh repo create`.
- `eval-harness` must compare two fixture runs, report 24/30 vs 26/30, name the 3 regressed cases,
  and not recommend shipping.

Run the suite yourself (it uses your model quota):

```sh
claude plugin eval . --scaffold --allow-tools Bash Write Edit "WebFetch(domain:github.com)" "WebFetch(domain:codeload.github.com)" "WebFetch(domain:registry.npmjs.org)"
```

The latest results are in [`docs/evals.md`](./docs/evals.md).

## Built with these skills

- **verdrift** went from a brief to a shipped repo through this workflow: a thin end-to-end slice
  first ([`0a6f535`](https://github.com/thanatchon36/verdrift/commit/0a6f535)), then tests, rules,
  docs, and CI ([commit history](https://github.com/thanatchon36/verdrift/commits/main)), a green
  [CI run](https://github.com/thanatchon36/verdrift/actions/runs/38226583610), and the
  [v0.1.0 release](https://github.com/thanatchon36/verdrift/releases/tag/v0.1.0). Its brief isn't
  published.
- **This repo** is the second example, and its brief is public:
  [`docs/mission/MISSION.md`](./docs/mission/MISSION.md). The research and decisions it produced are in
  [`docs/research/`](./docs/research/) and [`docs/DECISIONS.md`](./docs/DECISIONS.md).

## How to know it's working

- The agent asks what "done" means before writing code, and the answer ends up in a file.
- Every "it works" in the agent's report points to a command it ran and its output.
- Nothing becomes public without a `STOP GATE` block you replied "go" to.
- READMEs and launch posts contain no numbers you can't trace back to the repo.

## Limitations

- These skills were tested with Claude Code. Through `npx skills` they install into other agents,
  but they haven't been tested there. Inside Claude Code the skills resolve bundled scripts with
  `${CLAUDE_SKILL_DIR}`, and other agents get a relative-path fallback in the text.
- `runtime-drift` covers Node, Python, and Go only (verdrift's scope), and needs Node 22+ and
  network access for the deterministic path.
- `leakage-audit` reads code statically. It can't see leaks in upstream SQL, feature stores, or
  notebooks you don't give it, and it says so rather than calling those clean.
- `eval-harness` writes the runner around your own entry point and asks before spending API quota.
  Without credentials, it stops before the baseline and says so. Its sign test assumes pass/fail
  results, not scores.
- `ship-oss` publishes to GitHub. Other forges and package registries are handled only as far as
  the brief and your tools allow.
- Eval scores come from a small number of runs and vary between runs. See `docs/evals.md`.

## Roadmap

Drafts in [`skills/in-progress/`](./skills/in-progress/) (not shipped): `rag-triage` (retrieval vs
ranking vs generation failures), `backtest-honesty` (look-ahead bias, survivorship, costs), and
`model-card`.

## Contributing

The most useful contribution is a transcript or prompt where a skill fired when it shouldn't have,
or didn't fire when it should have. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## More from me

- [verdrift](https://github.com/thanatchon36/verdrift): Find every place your repo pins a Node, Python,
  or Go version, and see where they disagree.
- [gemini-candlestick](https://github.com/thanatchon36/gemini-candlestick): a Gemini API competition
  project that simulates an investment board discussing candlestick charts and technical indicators.
- [nvidia-gpu-operator-k8s-cluster](https://github.com/thanatchon36/nvidia-gpu-operator-k8s-cluster):
  a step-by-step guide (in Thai) to running the NVIDIA GPU Operator on a Kubernetes cluster on AWS.

## License

[MIT](./LICENSE)
