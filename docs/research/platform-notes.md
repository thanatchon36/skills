# Platform notes

Facts from current docs and tools, checked 2026-10-12 with Claude Code 2.1.296 and skills CLI 1.7.2.

## Claude Code plugins (code.claude.com/docs)

- `plugin.json` `skills`: a path or array of paths. It **adds to** the default `skills/` scan rather
  than replacing it. The default scan reads only `skills/<name>/SKILL.md`, one level deep. Our skills
  sit two levels deep (`skills/<bucket>/<name>/`), so the default scan finds nothing, and only the
  listed directories ship. This is verified by the local install test, not assumed.
- Plugin names may not start with `claude-`, `anthropic-`, `anthropics-`, or `cc-plugin-`, and must
  not use `claude`/`anthropic` as a whole word. `thanatchon-skills` is clean.
- The marketplace name `thanatchon` is not reserved. For a GitHub source, Claude Code downloads into
  `<owner>-<repo>` (`thanatchon36-thanatchon-skills`), and that string must not collide with
  another registered marketplace's name.
- `claude plugin validate --strict` turns warnings (missing `version`/`description`/`author`,
  unknown keys) into failures.
- Skill frontmatter: `disable-model-invocation: true` makes a skill user-only (slash command). The
  combined `description` + `when_to_use` text is capped at 1,536 characters in the listing.
- `CLAUDE.md` at a plugin root is not loaded as plugin context, so maintainer guidance goes in
  `AGENTS.md`.

## Plugin evals (`claude plugin eval`)

- Cases live in `evals/<case>/prompt.md` with `graders/*.md`. The grader types are `regex`,
  `tool_used`, `tool_order`, `file_exists`, `llm`, and `baseline`. There are no custom-code graders.
- Each run starts in an empty workspace. Fixtures come from `context.add_dirs` (read-only) or a
  `scaffold_script` (only with `--scaffold`).
- By default, each case runs 3 times with the plugin and 3 times without. `tool_used: Skill` graders
  are excluded from the score in two-arm runs. A "must not fire" check needs `arm: both`,
  `min: 0`, `max: 0`.
- Every run is a real model call billed to the account. `--ablation none` and `--runs 1` cut the cost
  while iterating.
- A `disable-model-invocation` skill can't be reached through the Skill tool, so a trigger eval for a
  user-invoked skill sends the slash command itself and grades the outcome instead.

## `npx skills` (vercel-labs/skills 1.7.2)

- Discovers `skills/<name>/SKILL.md` and catalog layouts one or two category levels deep
  (`skills/<category>/<name>/SKILL.md`), plus anything declared in `.claude-plugin/plugin.json` or
  `marketplace.json`.
- That means `skills/in-progress/<name>/` **would** be discovered. The supported way to exclude it is
  frontmatter `metadata: { internal: true }`, which hides a skill unless `INSTALL_INTERNAL_SKILLS=1`
  is set. Every draft in `in-progress/` carries it.
