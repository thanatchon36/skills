NOT READY: no v0.1.0 release yet, and the README's first screen has no real example (it starts at line 64). Post after both are fixed.

# X thread

1/ Coding agents write the code fine. They skip the rest of shipping: what "done" means, a README
a stranger can use, the release, the launch.

I wrote 7 agent skills for that part.
https://github.com/thanatchon36/skills

2/ /mission-brief asks one question at a time and writes a MISSION.md with checkable success
criteria.

/ship-oss runs it phase by phase and stops for an explicit "go" before any repo creation, push,
tag, or release.

3/ runtime-drift runs verdrift on a repo where .nvmrc, the Dockerfile, and CI disagree:

✗ Dockerfile:1  FROM node:20-alpine disagrees with 22 (.nvmrc:1)

It reports all 4 problems in the fixture, then proposes the smallest fix.

4/ leakage-audit checks pandas, scikit-learn, and PySpark code for target and temporal leakage.
Its eval: find all 8 leaks planted in a fixture, at the right lines, and report 0 on the fixed
twin.

5/ Limits: tested only with Claude Code so far. Other agents install via npx skills, untested.

Install:
/plugin marketplace add thanatchon36/skills
or
npx skills@latest add thanatchon36/skills
