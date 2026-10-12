# Manual runtime-drift checklist

Use this when `scripts/verdrift.sh` exits 3 (no Node.js 22+, or no network). It covers the same
sources and rules as verdrift v0.1.0, but a manual pass can miss things. Say so in the report.

## 1. Find declarations

Search only files git tracks (`git ls-files`). Skip `node_modules/`, `vendor/`, virtualenvs, and
build output.

| Runtime | Where to look | Role |
| --- | --- | --- |
| Node | `.nvmrc`, `.node-version` | pin (the dedicated version file) |
| Node | `package.json` `engines.node` | range |
| Node | `package.json` `volta.node`, `devEngines.runtime` | pin |
| Python | `.python-version`, `runtime.txt` | pin (the dedicated version file) |
| Python | `pyproject.toml` `requires-python`, `tool.poetry.dependencies.python` | range |
| Go | `.go-version` | pin (the dedicated version file) |
| Go | `go.mod` `go` directive | range (a minimum) |
| Go | `go.mod` `toolchain` | pin |
| All | `.tool-versions`, `mise.toml` | pin |
| All | Dockerfile `FROM node:`/`python:`/`golang:` (resolve `ARG` defaults), Compose `image:` | pin |
| All | GitHub Actions `setup-node`/`setup-python`/`setup-go` inputs, `strategy.matrix`, job `container:` | ci |
| All | `.gitlab-ci.yml` `image:` | ci |

Useful searches:

```sh
git ls-files | grep -E '(^|/)(\.nvmrc|\.node-version|\.python-version|runtime\.txt|\.go-version|go\.mod|\.tool-versions|mise\.toml|package\.json|pyproject\.toml|Dockerfile[^/]*|(docker-)?compose\.ya?ml|\.gitlab-ci\.yml)$|^\.github/workflows/'
git grep -nE '^FROM\s+(node|python|golang):|(node|python|go)-version:|requires-python|"node"\s*:' -- ':!**/node_modules/**'
```

Record each declaration as `file:line`, runtime, role, and raw value.

## 2. Apply the rules

- **pin-mismatch**: two pins of one runtime name versions that can't both hold (`20` vs `22`,
  `20.11` vs `20.12`). Compare each pin with the dedicated version file when there is one. A shorter
  pin agrees with a longer one it prefixes (`20` and `20.11.1` agree). Ignore image suffixes such as
  `-alpine` and `-slim`.
- **outside-range**: a pin or CI version is excluded by a range in the same directory or above it.
  Use npm semver for `engines`, PEP 440 for `requires-python` (`<=3.12` excludes `3.12.5`), and
  "at least" for the go directive.
- **range-conflict**: two ranges for one runtime have no version in common.
- **yaml-number**: an unquoted CI version that YAML turns into a different number (`3.10` becomes
  `3.1`, `1.20` becomes `1.2`). Quote it.

CI versions are checked against ranges only, not against pins. Report moving values (`lts/*`,
`latest`, `${{ ... }}`, an `ARG` without a default) as skipped, with the reason.

## 3. Report

Use the same output contract as the skill. Add the line: "Manual pass; verdrift could not run:
<reason>. Re-run verdrift when Node.js 22+ is available to confirm."
