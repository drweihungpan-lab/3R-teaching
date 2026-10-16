# 02: Implement the backend API and Python processing package

Published as [GitHub issue #3](https://github.com/drweihungpan-lab/3R-teaching/issues/3), labeled `ready-for-agent`.

Approved course-authoring task. Implementation owner: the course author or an assisting agent. Student participation is not a completion condition.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

Build the complete reusable healthcare processing package and FastAPI service that later frontend and teaching tasks can call.

## Acceptance criteria

- [ ] Provide Python 3.12 package metadata, dependency declarations, and editable installation instructions.
- [ ] Implement documented participant/laboratory joins, missing-value handling, basic summaries, and baseline/change calculations appropriate to the example.
- [ ] Declare API request/response contracts and actionable invalid-input responses; validate required fields, join keys, duplicates, types, and units.
- [ ] Preserve unavailable values as missing rather than zero and define behavior when baseline is unavailable.
- [ ] Keep processing independent of HTTP presentation, with useful type hints and logging.
- [ ] Document service startup, configuration, example requests, and expected responses; provide a usable example configuration without committing local secrets.
- [ ] Deliver complete working backend code; frontend, formal test suite, CI, and containers have separate tickets.

## Blocked by

- [#2: Prepare synthetic healthcare data and dictionary](https://github.com/drweihungpan-lab/3R-teaching/issues/2)

Dependencies and the parent relationship are also recorded natively on GitHub. Local task numbers are planning identifiers and may differ from GitHub issue numbers.
