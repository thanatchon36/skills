# Contributing

Thanks for helping. The most useful contributions, in order:

1. **A mis-fire report.** A prompt where a skill fired and shouldn't have, or didn't fire and
   should have. Include the exact prompt, the agent and version, and what happened. These become
   eval cases.
2. **A wrong result.** For example, `leakage-audit` missing a leak or flagging clean code, or
   `runtime-drift` proposing a bad edit. A minimal file that reproduces it is ideal.
3. **A fix with an eval case** that fails before your change and passes after it.

## Setup

```sh
git clone https://github.com/thanatchon36/thanatchon-skills && cd thanatchon-skills
claude plugin validate . --strict
python3 scripts/lint_frontmatter.py
```

To try your changes in Claude Code without reinstalling, run `claude --plugin-dir .` from the
repo root, or use `scripts/link-skills.sh`.

## Rules for changes

[AGENTS.md](./AGENTS.md) lists the invariants (naming, manifest, invocation mode, eval counts) and
the checks to run. In short:

- Keep each `SKILL.md` body to 250 lines or fewer. Put detail in `references/`.
- Add or update eval cases under `evals/<skill>/`, with at least 3 trigger and 3 near-miss cases.
- Never add promotional text to what a skill produces for users.
- Use conventional commits (`feat(skill): ...`, `fix(skill): ...`, `docs: ...`).

New skills start in `skills/in-progress/` with `metadata: { internal: true }`. They move to a
shipped bucket once they pass their evals.
