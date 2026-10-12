# Promoted repos audit

Source: `gh repo list thanatchon36 --visibility=public --source`, run on 2026-10-12 (29 repos). The bar
for a showcase is a README that explains the project, plus an install that works.

| Repo | README | Install verified | Decision |
| --- | --- | --- | --- |
| [verdrift](https://github.com/thanatchon36/verdrift) | Yes, full | Yes. `npx --yes github:thanatchon36/verdrift#v0.1.0 examples/drifted --format json` ran here and reported 4 problems, exit 1 | **Flagship showcase**, and the engine for `runtime-drift` |
| [gemini-candlestick](https://github.com/thanatchon36/gemini-candlestick) | Yes, full | No. It needs a Gemini API key and a Telegram bot. The README's license section points to competition rules, not an OSS license | "More from me" only |
| [nvidia-gpu-operator-k8s-cluster](https://github.com/thanatchon36/nvidia-gpu-operator-k8s-cluster) | A step-by-step guide (Thai), not an installable project | n/a | "More from me" only |
| [mahaeyong](https://github.com/thanatchon36/mahaeyong) | An index of Dhamma talks, not software | n/a | Left out. Off-topic for an engineering audience |
| 25 others | Title-only README or none | n/a | Left out |

## verdrift facts used elsewhere (all verifiable)

- Release `v0.1.0`, published 2026-10-12: https://github.com/thanatchon36/verdrift/releases/tag/v0.1.0
- 10 commits on `main`, starting with "Thin end-to-end path: discover, parse, and compare runtime
  versions" (`0a6f535`), then tests, scoping rules, docs, and CI.
- CI on `main` is green (run `38226583610`, "Add CI badge").
- The `examples/drifted` fixture produces exactly 4 problems: `yaml-number` (ci.yml:24),
  `outside-range` (ci.yml:8), `pin-mismatch` (Dockerfile:1), `outside-range` (api/Dockerfile:1).
- verdrift's own MISSION.md is **not** published in its repo. The case study therefore links the
  commits, CI, and release, and points to this repo's `docs/mission/MISSION.md` as the readable
  example of a brief.
