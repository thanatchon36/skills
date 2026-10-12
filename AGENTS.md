# AGENTS.md

Instructions for agents and contributors working on this repo. (There is deliberately no
`CLAUDE.md` at the root: Claude Code doesn't load one from a plugin root, and the validator warns
about it.)

## Layout

- `skills/<bucket>/<name>/SKILL.md`: the buckets are `workflow/`, `engineering/`, `data-ml/`, and
  `meta/`. These are shipped.
- `skills/in-progress/<name>/`: drafts. Never list them in `plugin.json`. Each one carries
  `metadata: { internal: true }` so `npx skills` hides it.
- `evals/<skill>/<case>/`: `claude plugin eval` cases. Tag every case with the skill name plus
  `trigger` or `near-miss`.
- `fixtures/`: test inputs the eval scaffolds copy in. `fixtures/leakage/EXPECTED.md` is the
  answer key.
- `docs/`: the mission, research, decisions, and eval results.

## Invariants (enforced by `scripts/lint_frontmatter.py`)

1. `name` equals the directory name, in kebab-case.
2. Every shipped skill is in `.claude-plugin/plugin.json` `skills` and linked from `README.md`, and
   nothing else is in either.
3. User-invoked skills (`mission-brief`, `ship-oss`, `launch-kit`, `ask-thanatchon`) set
   `disable-model-invocation: true` and have a short, human-facing description. Model-invoked
   skills have trigger phrases and "Not for" exclusions in the description.
4. At least 3 `trigger` and 3 `near-miss` eval cases per shipped skill.
5. The SKILL.md body is 250 lines or fewer. Detail goes in `references/`, deterministic work in
   `scripts/`.

When you add, rename, or change how a skill fits a flow, update `skills/meta/ask-thanatchon/SKILL.md`
so the router doesn't route to something stale. Also update the lineup in both READMEs.

## Writing a skill

Shape: a one-line purpose, then when NOT to use it, then a workflow with numbered gates ("do not
skip ahead"), then the output contract, the operating rules, and a done-check. Write instructions
to a capable engineer, with no marketing, hype, or emojis. Every skill must be useful to someone who
has never heard of the author.

A skill must never insert promotion (links, badges, "made with" lines, mentions of this repo or its
author) into anything it produces for the user. A skill that runs a third-party tool tells the user
what will run first, pins a version, and degrades gracefully without it.

## Checks before a commit

```sh
claude plugin validate . --strict
claude plugin validate .claude-plugin/plugin.json --strict
python3 scripts/lint_frontmatter.py
python3 skills/workflow/readme-that-converts/scripts/readme_lint.py README.md
```

Run the evals for the skill you touched (this uses model quota):

```sh
claude plugin eval . --tag <skill> --runs 1 --ablation none --scaffold --allow-tools Bash Write Edit \
  "WebFetch(domain:github.com)" "WebFetch(domain:codeload.github.com)" "WebFetch(domain:registry.npmjs.org)"
```

`--tag` values are OR'ed, so filter by the skill name alone. Use conventional commits, one per
skill change.

## Dev loop

`scripts/link-skills.sh` symlinks every skill (drafts included) into `~/.claude/skills` and
`~/.agents/skills`. It is for maintainers, not an installer. `scripts/list-skills.sh` shows what
ships.
