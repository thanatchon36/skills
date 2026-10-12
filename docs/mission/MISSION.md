# MISSION: Ship my agent-skills repo

You are Claude Code, starting in an empty directory. Research, build, test, and publish a public GitHub
repository of agent skills, packaged as a Claude Code plugin and installable in other agents too.

The repo has two jobs, in this order:
1. Be genuinely useful to engineers who have never heard of me.
2. Drive attention to my other open-source projects, honestly: by showcasing them where they fit, never
   by injecting promotion into anyone's work.

Run every phase autonomously. Stop only at the STOP GATES in section 9. When something is ambiguous,
choose the most reasonable option, record it in `docs/DECISIONS.md` with one line of rationale, and
keep going.

---

## 1. Config (edit before running)

```yaml
github_user: thanatchon36
repo_name: thanatchon-skills        # must NOT start with "claude-" or "anthropic-"; rename if you have a brand
plugin_name: thanatchon-skills
marketplace_name: thanatchon
router_skill: ask-thanatchon
promote:
  - repo: thanatchon36/verdrift     # flagship showcase
    hook: "Find every place your repo pins a Node, Python, or Go version, and see where they disagree."
  # Also run `gh repo list thanatchon36 --public --source` and add any repo that has a README
  # and a working install. List the rest under "More from me" only.
author_links:                       # fill in, or leave empty. Never invent links.
  x: ""
  linkedin: ""
  site: ""
license: MIT
readme_languages: [en, th]          # README.md + README.th.md
```

---

## 2. Reference teardown (Phase 0, do first)

Clone these into `/tmp/refs/` and read every `SKILL.md`, README, `plugin.json`, and `marketplace.json`:

- https://github.com/multica-ai/andrej-karpathy-skills
- https://github.com/mattpocock/skills
- https://github.com/thananon/9arm-skills

Write `docs/research/reference-teardown.md`: for each repo, its structure, install paths, how skills are
written, how the README sells, and how the author is promoted. End with a "steal / avoid" list.

What I already noticed (verify, don't trust blindly):

- **karpathy-skills**: one sharp idea expressed as four named principles, each with a one-line test. A
  "How to know it's working" section. The first line of the README is a callout to the author's *other*
  project plus a social link. Same content ships three ways: Claude Code plugin, a curl-able `CLAUDE.md`,
  and a Cursor rule. Bilingual README.
- **mattpocock/skills**: README organized as failure mode -> quote -> fix -> skill link. Small composable
  skills split into **user-invoked** (orchestrators) and **model-invoked** (reusable discipline).
  Author-branded entry points (`/ask-matt` router, `setup-matt-pocock-skills`). Install instructions for
  Claude Code, Codex, Copilot, Gemini, and `npx skills`. `plugin.json` lists each shipped skill directory
  explicitly. Newsletter call to action.
- **9arm-skills**: buckets (`engineering/`, `productivity/`, `misc/`, `personal/`, `in-progress/`,
  `deprecated/`). Opinionated skills with hard gates (for example, a post-mortem skill that refuses to
  draft without a repro, a known cause, and a validated fix). Descriptions spell out explicit triggers.
  `npx skills add` plus a symlink script for the author's own dev loop.

**Licensing:** karpathy-skills and mattpocock/skills are MIT. 9arm-skills shows no license, so treat it
as all rights reserved. Study all three for structure and ideas only; write every line of our skills
fresh. No copied passages.

---

## 3. Positioning: the hook

A skills repo with no audience does not collect stars on its own. The reference repos ride a famous name
or a large newsletter. Ours needs one angle nobody else owns:

> **Skills that take an open-source project from a one-page MISSION.md to a shipped public repo.**

verdrift was built this way. The skills are the workflow, verdrift is the proof, and this repo is the
second proof: commit this file as `docs/mission/MISSION.md` so readers can see the brief that produced it.

Secondary pillar: AI and data engineering discipline from my day job (AI engineering, GenAI, agentic
automation, AI governance, ML).

Draft one tagline plus three alternatives in `docs/DECISIONS.md`, pick one, and use it consistently in
the GitHub description, `plugin.json`, and the README's first line.

---

## 4. Promotion rules

**Do**

- **P1 Dogfood.** When a skill genuinely needs what a promoted repo does, use that repo as its
  deterministic engine (see `runtime-drift`). Pin to a release tag. Tell the user what will run before
  running it. Degrade gracefully (explain, then fall back to manual inspection) if Node or network is
  unavailable.
- **P2 Case study.** README section "Built with these skills": verdrift went from MISSION.md to a shipped
  repo. Link real artifacts only (the mission, commits, CI runs). No invented metrics.
- **P3 Callouts.** One-line callout to the flagship project at the top of the README, and a "More from me"
  section at the bottom listing each promoted repo with its one-line hook.
- **P4 Branded entry point.** The router skill (`router_skill` in config).
- **P5 Backlinks.** Propose a short "Agent skill" section in each promoted repo's README that points back
  here (STOP GATE B).
- **P6 Discoverability.** GitHub description, topics (`claude-code`, `agent-skills`, `claude-skills`,
  `skills`, `ai-agents`, `codex`, `cursor`, `llm`, `developer-tools`), a social-preview image brief,
  CHANGELOG, tagged release.

**Never**

- Insert promotional text, links, badges, or "made with" lines into anything a skill produces for the
  user: code, commits, PR bodies, docs, issues.
- Install or run a promoted tool silently, or recommend it when it doesn't fit the task.
- Add telemetry, analytics, or any phone-home.
- Fake stars, testimonials, download counts, or benchmarks.
- Name anything so it passes as an Anthropic product.

---

## 5. Skill lineup for v0.1

Ship these 7. Put the rest in `skills/in-progress/` (not shipped). Final names and descriptions go in
`PLAN.md`. Cut a skill if it can't meet the quality bar in section 8; never pad the count.

| Skill | Bucket | Invocation | Job |
|---|---|---|---|
| `mission-brief` | workflow | user | Interview me, one question at a time, until a project idea becomes a MISSION.md: goal, non-goals, target users, success criteria, phases, stop gates, license, definition of done. |
| `ship-oss` | workflow | user | Execute a MISSION.md: research -> build -> test -> docs -> publish. Task list, a verification loop per phase, hard stops before anything public or irreversible. |
| `readme-that-converts` | workflow | model | README discipline: the problem in the first sentence, copy-paste install on the first screen, a real output example, why it exists, limitations, roadmap. verdrift's README is the reference example. |
| `launch-kit` | workflow | user | Draft launch material for a repo: Show HN, X thread, LinkedIn, Reddit, Thai developer communities, plus topics and a social-preview brief. Writes drafts to `launch/`. Never posts. |
| `runtime-drift` | engineering | model | When a task touches Node/Python/Go version bumps, Dockerfiles, or CI matrices: run verdrift with `--format json`, interpret the findings, propose the minimal fix set. |
| `leakage-audit` | data-ml | model | Check ML pipelines (pandas, PySpark, scikit-learn) for target leakage, temporal leakage, train/test contamination, and preprocessing fit on the full dataset. Cite `file:line` for every finding. |
| `ask-thanatchon` | meta | user | Router: given the user's situation, recommend which skill or flow to use. |

In-progress candidates: `eval-harness` (build an LLM/RAG eval set before changing prompts or models),
`rag-triage` (retrieval vs ranking vs generation failures), `backtest-honesty` (look-ahead bias,
survivorship, costs and slippage), `model-card`.

---

## 6. Repo layout

```text
<repo_name>/
├── .claude-plugin/
│   ├── plugin.json          # lists each SHIPPED skill dir explicitly
│   └── marketplace.json
├── skills/
│   ├── workflow/            # mission-brief, ship-oss, readme-that-converts, launch-kit
│   ├── engineering/         # runtime-drift
│   ├── data-ml/             # leakage-audit
│   ├── meta/                # ask-thanatchon
│   └── in-progress/         # drafts, never listed in plugin.json
├── evals/                   # plugin eval cases
├── fixtures/                # test inputs (e.g. leaky vs clean pipelines)
├── scripts/                 # link-skills.sh, list-skills.sh, lint-frontmatter
├── docs/
│   ├── mission/MISSION.md   # this file
│   ├── research/
│   └── DECISIONS.md
├── launch/
├── .github/workflows/ci.yml
├── AGENTS.md
├── README.md
├── README.th.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

Notes:

- Read the current Claude Code docs before writing manifests: plugins reference, marketplace reference,
  skills, and plugin evals. Index: https://code.claude.com/docs/llms.txt. When the docs disagree with
  this brief, the docs win; note the difference in DECISIONS.md.
- `plugin.json` lists each shipped skill directory explicitly (mattpocock pattern), so `in-progress/`
  never ships.
- Put contributor and agent instructions in `AGENTS.md`. Do not put a `CLAUDE.md` at the plugin root:
  it isn't loaded as plugin context and the validator warns about it.
- No top-level `bin/` directory (claude.ai won't install a plugin that has one). Scripts live in
  `scripts/` or inside a skill folder.
- Check how `npx skills` discovers skills. If it would pick up `in-progress/`, find the supported way
  to exclude drafts, or keep drafts on a separate branch.

---

## 7. How to write a SKILL.md

- **Frontmatter.** `name` equals the directory name, kebab-case. `description` says what the skill does
  and when to use it, with explicit trigger phrases and its slash name, specific enough that it does not
  fire on unrelated tasks. User-invoked orchestrators disable model invocation (confirm the exact field
  name in the docs).
- **Size.** Body around 250 lines at most. Push detail into `references/*.md` and deterministic work into
  `scripts/`.
- **Shape.** One-line purpose -> when NOT to use -> workflow with numbered gates ("do not skip ahead")
  -> output contract -> operating rules -> done-check.
- **Voice.** Instructions to a capable engineer. No marketing, no emojis, no hype.
- **Test.** Every skill must be useful to someone who has never heard of me or my projects.

---

## 8. Quality bar (run after every skill and again at the end)

1. `claude plugin validate . --strict` passes.
2. Eval cases per skill (see the plugin evals docs): at least 3 prompts that should trigger, at least 3
   near-miss prompts that must not, plus outcome checks where feasible.
3. Local install test in a scratch directory: add the marketplace from the local path, install, and
   confirm exactly the shipped skills appear, namespaced under the plugin.
4. `runtime-drift` on verdrift's `examples/drifted` fixture reports the same 4 problems verdrift reports.
5. `leakage-audit` on a fixture you create with planted leaks finds every one, and reports nothing on the
   clean twin.
6. Every install command in the README was actually run, or is labeled "untested".
7. CI (`.github/workflows/ci.yml`): validate, frontmatter lint, markdown link check.

---

## 9. Phases and stop gates

- **Phase 0 Discover.** `gh auth status`, list my public repos, read the promoted READMEs, write the
  reference teardown. Output: `docs/research/`.
- **Phase 1 Plan.** `PLAN.md`: tagline, final lineup, descriptions, README outline. Continue without asking.
- **Phase 2 Build.** One skill at a time; run the quality bar after each. One conventional commit per skill.
- **Phase 3 Package and docs.** Manifests, `README.md`, `README.th.md` (natural Thai written for Thai
  developers, not a literal translation; keep code and commands in English), CHANGELOG, CONTRIBUTING,
  AGENTS.md, LICENSE.

  Target install block for the README (verify it works):
  ```
  /plugin marketplace add thanatchon36/<repo_name>
  /plugin install <plugin_name>@<marketplace_name>
  ```
  plus `npx skills@latest add thanatchon36/<repo_name>`, and Codex/Copilot/Gemini paths only if tested.

- **STOP GATE A.** Before `gh repo create --public`, the first push, any tag, or any release: show me the
  repo name, description, topics, skill list, and the README's first screen. Wait for "go".
- **Phase 4 Publish.** Create the repo, push, set description, topics, and homepage, tag `v0.1.0`,
  publish release notes.
- **STOP GATE B.** Before touching any other repo: show the proposed backlink diff for each promoted repo.
  Wait for approval per repo.
- **Phase 5 Launch kit.** Run our own `launch-kit` skill on this repo. Drafts go in `launch/`. Do not post
  anywhere.
- **Phase 6 Report.** What shipped, links, eval results, open TODOs, and the three highest-leverage next
  moves for growing stars.

---

## 10. Definition of done

- The public repo installs in Claude Code with two commands, and via `npx skills add`.
- 7 skills (or fewer, if some were cut for quality), each passing its evals. `validate --strict` clean.
  CI green.
- README first screen: the promise, the install, the flagship callout. Case-study section live.
- Backlinks proposed, and merged only where I approved.
- `launch/` drafts ready for me to post.
