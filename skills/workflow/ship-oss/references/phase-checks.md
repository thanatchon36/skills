# Phase checks

Each phase ends with checks you run yourself. A phase is done when every check has evidence: a
command and its output, a file path, or a link. "It should work" is not evidence.

## Discover

- [ ] Prior art: at least the two or three closest existing projects, with what they do and don't do.
- [ ] License of everything you will build on or borrow ideas from. Unlicensed means all rights
      reserved: study it, don't copy it.
- [ ] Platform facts that the build depends on (API shapes, manifest schemas, CLI flags), read from
      current docs, with the date read. When the docs and the mission disagree, follow the docs and
      record the difference.
- [ ] Output: a research note in `docs/research/`.

## Plan

- [ ] `PLAN.md`: deliverables, the order to build them in, and how each will be verified.
- [ ] Every success criterion in the mission maps to a check in the plan.
- [ ] Ambiguities resolved and logged in `docs/DECISIONS.md`.

## Build

- [ ] A thin end-to-end slice first (input to output, one path), then widen.
- [ ] Tests for behavior that matters, and they were run: show the command and the pass count.
- [ ] A real run against an example input in the repo, with the output captured for the README.
- [ ] The linter and type checker the project uses are clean.
- [ ] One conventional commit per meaningful unit (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).

## Docs

- [ ] README written to the project's standard. If the `readme-that-converts` skill is available,
      call the Skill tool with it.
- [ ] Every command in the README was run in this session, or is labeled "(untested)".
- [ ] `LICENSE` file present with the license the mission names. `CHANGELOG.md` has the first
      version. `CONTRIBUTING.md` explains setup and the most useful kind of contribution.
- [ ] Links resolve (relative links checked; external links spot-checked).

## Package

- [ ] Manifests validate with the ecosystem's own validator (`npm pack --dry-run`,
      `python -m build` plus `twine check`, `claude plugin validate --strict`, ...).
- [ ] A clean install into a scratch directory from the local build works, and the installed
      command runs.
- [ ] CI config exists and has been run locally where possible (`act`, or the same commands by hand).

## Publish (after the gate)

- [ ] Create, push, tag, and release exactly as approved.
- [ ] CI is green on the pushed commit: `gh run watch`, or `gh run list` with the run URL.
- [ ] Install from the public source in a clean directory, and the installed command runs.
- [ ] Metadata set: description, topics, homepage.

## Report

- [ ] What shipped, with links (repo, release, CI run, package page).
- [ ] Each success criterion with its evidence, or marked not met with the reason.
- [ ] Open TODOs, cut scope, and the decisions log.
