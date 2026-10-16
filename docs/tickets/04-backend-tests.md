# 04: Add backend processing and API tests

Published as [GitHub issue #5](https://github.com/drweihungpan-lab/3R-teaching/issues/5), labeled `ready-for-agent`.

Approved course-authoring task. Implementation owner: the course author or an assisting agent. Student participation is not a completion condition.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

Implement the focused pytest suite that checks the declared processing and API behavior.

## Acceptance criteria

- [ ] Cover expected joins, summaries, baseline/change behavior, missing observations, and missing baselines.
- [ ] Cover declared validation rules and API success/error responses, including malformed input and duplicate or unknown identifiers.
- [ ] Use fixtures and documented numerical tolerances where appropriate; compare counts and structural fields exactly.
- [ ] Test external behavior rather than helper calls or code organization.
- [ ] Document running the suite locally and record actual results.
- [ ] Do not add a separate course-level end-to-end acceptance framework or evaluate scientific conclusions.

## Blocked by

- [#3: Implement the backend API and Python processing package](https://github.com/drweihungpan-lab/3R-teaching/issues/3)

Dependencies and the parent relationship are also recorded natively on GitHub. Local task numbers are planning identifiers and may differ from GitHub issue numbers.
