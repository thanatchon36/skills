# Reference teardown

Three public skills repos, read on 2026-10-12 from fresh clones. We used them for structure and ideas
only. No text from them is reused in this repo.

| Repo | Commit read | License |
| --- | --- | --- |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | `2c60614` | README and SKILL frontmatter say MIT, but the repo has no `LICENSE` file |
| [mattpocock/skills](https://github.com/mattpocock/skills) | `49dd158` | MIT (`LICENSE` present) |
| [thananon/9arm-skills](https://github.com/thananon/9arm-skills) | `a1fc303` | None. Treated as all rights reserved |

## 1. andrej-karpathy-skills

**Structure.** One skill (`skills/karpathy-guidelines/SKILL.md`), plus the same text as a root
`CLAUDE.md` and a Cursor rule (`.cursor/rules/karpathy-guidelines.mdc`, `alwaysApply: true`).
`EXAMPLES.md` holds worked before/after examples. `README.zh.md` is a full Chinese translation.

**Install paths.**
- Claude Code plugin: `/plugin marketplace add forrestchang/andrej-karpathy-skills`, then
  `/plugin install andrej-karpathy-skills@karpathy-skills`. The README still points at the old
  `forrestchang/` path after the repo moved to `multica-ai/`, so it depends on GitHub's redirect.
- A per-project `CLAUDE.md` you can download with `curl` (new file, or appended to an existing one).
- A Cursor project rule, with `CURSOR.md` explaining how to copy it.

**Manifests.** `plugin.json` lists one skill path explicitly. `marketplace.json` has one plugin entry
with `source: "./"` and an extra `id` key that Claude Code does not read.

**How skills are written.** Four named principles. Each has a bold one-line slogan and a short
bulleted list. Only two of the four end with an explicit "The test:" line (Simplicity First and
Surgical Changes). The brief's claim that every principle has a one-line test is not quite right.
There are no workflow steps, gates, or output contract. It is a behavioral overlay, not a procedure.

**How the README sells.** The title is followed by quotes from Karpathy's post (the problem), then a
principle-to-problem table (the solution), the principles in detail, install, and "How to Know It's
Working" (observable signals in diffs and PRs). It closes with a tradeoff note ("caution over speed").
The borrowed authority of a famous name does most of the selling.

**Author promotion.** The first block under the H1 is a callout to the author's other project
(Multica) plus an X profile link, repeated in the Chinese README. Nothing promotional appears in the
skill itself.

## 2. mattpocock/skills

**Structure.** Buckets under `skills/`: `engineering/`, `productivity/` (promoted and shipped), and
`misc/`, `in-progress/`, `deprecated/` (not shipped). 27 shipped skills. Each skill folder has a
`SKILL.md`, an `agents/openai.yaml` (Codex picker metadata and invocation policy), and sometimes
`scripts/` or extra reference `.md` files. Human-facing docs pages live in `docs/<bucket>/<skill>.md`.
Maintainer rules live in `CLAUDE.md` plus `.agents/*.md` (invocation rules, the canonical install
block, docs writing). Out-of-scope decisions are recorded in `.out-of-scope/`. Changesets drive releases.

**Install paths.** Claude Code installs from the official marketplace
(`claude plugin install mattpocock-skills@claude-plugins-official`). Codex and Copilot install from
the repo's own `marketplace.json`. Gemini uses `gemini skills install --path skills/<bucket>`. Every
other agent uses `npx skills@latest add mattpocock/skills`. The README explains which routes update
themselves, and warns not to install through two routes because you get every skill twice. Each
route records the date it was last verified.

**Manifests.** `plugin.json` lists each shipped skill directory explicitly, which keeps `in-progress/`
and `misc/` out of the plugin. `marketplace.json` has one entry with `source: "./"`.

**How skills are written.** Each skill is one of two kinds:
- **User-invoked**: frontmatter `disable-model-invocation: true`, plus
  `policy.allow_implicit_invocation: false` in `openai.yaml`. The description is a short, human-facing
  summary.
- **Model-invoked**: the description carries trigger phrases ("Use when the user says...").

Small primitives compose: `grill-me` is a single line, "Call the Skill tool with "grilling"".
Dependencies between skills are explicit Skill-tool calls, never `../other/FILE.md` links.
Discipline skills are phased, with completion criteria written as checklists (for example,
`diagnosing-bugs` blocks Phase 2 until a red-capable command has been run). Bodies run about
50 to 170 lines.

**How the README sells.** A newsletter image leads, then the tagline, then a short contrarian
positioning ("GSD, BMAD, Spec-Kit... take away your control"). A newsletter call to action
("~60,000 other devs") comes before install. Install is collapsible, one block per agent. "Why
These Skills Exist" is a sequence of failure modes, each written as quote, problem, fix, and skill
links. A reference list grouped by user-invoked and model-invoked closes the README.

**Author promotion.** A branded router (`/ask-matt`) and setup skill (`/setup-matt-pocock-skills`).
The newsletter image and call to action sit at the top. Author name and homepage go in
`plugin.json` (`homepage` is the newsletter URL). Docs are published on the author's site.

**Rules worth noting.**
- The router must be re-synced whenever a user-reachable skill changes ("a router that lies").
- Every shipped skill must appear in both the README and `plugin.json`, and nothing else may.
- Install commands are copied from one canonical source.

## 3. 9arm-skills

**Structure.** Buckets `engineering/`, `productivity/`, `misc/`, each with a `README.md` index. The
README and `CLAUDE.md` also describe `personal/`, `in-progress/`, and `deprecated/`, but those
directories do not exist in the repo yet. 6 skills, no bundled references except inline examples.

**Install paths.** `npx skills add thananon/9arm-skills`, and a `scripts/link-skills.sh` symlink
script for the author's own dev loop. `plugin.json` lists the skills explicitly, but there is no
`marketplace.json`, so the README offers no `/plugin install` route.

**How skills are written.** Opinionated and gated. `post-mortem` has a "Required inputs: refuse to
draft without these" checklist (reliable repro, known root cause, identified fix, validated fix),
and an output flow that requires explicit sign-off before posting to an external tracker.
Descriptions are long and list explicit trigger phrases, including the slash name. Skills reference
each other by relative path (`../../productivity/management-talk/SKILL.md`), which mattpocock
deliberately avoids. Style rules ("No hedging", "Blameless", "Mechanism over narrative") sit at the
end as operating rules.

**How the README sells.** It doesn't, much. A layout note, install, and a reference list with
one-line descriptions. The repo relies on the author's existing audience.

**Author promotion.** None in the README. The `qwen-agent` skill depends on the author's own
`claude-9arm` command, which makes it less useful to anyone outside that setup.

## Steal / avoid

**Steal**

1. **Explicit `skills` array in `plugin.json`** (mattpocock, 9arm) so drafts never ship.
2. **The user-invoked / model-invoked split**, with `disable-model-invocation: true` on
   orchestrators and short human-facing descriptions on those. Model-invoked skills get rich
   trigger phrases.
3. **Hard input gates that refuse to proceed** (9arm `post-mortem`). We use this for `ship-oss` stop
   gates and for `leakage-audit` refusing to call a pipeline "clean" without reading the split code.
4. **Completion criteria as checklists** (mattpocock `diagnosing-bugs`), so the agent can verify
   each phase itself.
5. **README as failure mode, then fix, then skill** (mattpocock). It sells the problem, not the author.
6. **"How to know it's working"** (karpathy): observable signals the reader can check.
7. **One callout line at the top for the author's other project** (karpathy): honest and skippable.
8. **A branded router skill** (mattpocock `/ask-matt`), plus the rule that it is updated whenever
   the lineup changes.
9. **Per-route install verification dates** and the "pick one install route" warning (mattpocock).
10. **The same content shipped through several channels** (karpathy). We ship the plugin plus
    `npx skills`, and add others only once they are tested.
11. **The dev-loop symlink script and list script** (mattpocock, 9arm).
12. **A bilingual README** (karpathy), done as a native rewrite rather than a literal translation.

**Avoid**

1. Advertising a bucket layout that doesn't exist (9arm lists `personal/`, `in-progress/`,
   `deprecated/` that are not in the repo).
2. No `LICENSE` file while claiming MIT (karpathy). Ship the file.
3. Install commands that rely on a GitHub redirect after a rename (karpathy README).
4. Unknown manifest keys (`id` in karpathy's `marketplace.json`). They fail `validate --strict`.
5. Skills that only work inside the author's private setup (9arm `qwen-agent`). Every skill must
   stand alone for a stranger.
6. Cross-skill relative file links (9arm). They break when skills are installed individually.
7. Leading the README with a newsletter or image when there is no audience yet. Lead with the
   problem and the install instead.
8. Leaning on a famous name for authority. We have none to borrow, so the proof has to be artifacts
   (a shipped repo, a CI run, a brief anyone can read).
