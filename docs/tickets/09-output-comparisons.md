# 09: Add repeatability and local/Docker output comparisons

Published as [GitHub issue #10](https://github.com/drweihungpan-lab/3R-teaching/issues/10), labeled `ready-for-agent`.

Approved course-authoring task. Implementation owner: the course author or an assisting agent. Student participation is not a completion condition.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

Provide the instructor's tools and instructions for showing matching repeated local results and matching local/container results.

## Acceptance criteria

- [ ] Run the same processing code and sample inputs repeatedly in the local virtual environment and capture inspectable outputs.
- [ ] Capture comparable outputs from the Docker environment for the same data and code.
- [ ] Compare cleaned records and counts exactly and calculated decimal values within explicit, explained tolerances.
- [ ] Preserve missingness and use a stable record ordering or a documented canonical comparison.
- [ ] Demonstrate that material mismatches fail comparison and that missing values are not equivalent to zero.
- [ ] Document the course-specific meanings of repeatability and replicability and record relevant execution conditions.
- [ ] Do not add independent simulations, cross-group exercises, or a new end-to-end testing framework.

## Blocked by

- [#5: Add backend processing and API tests](https://github.com/drweihungpan-lab/3R-teaching/issues/5)
- [#9: Configure Docker Compose services](https://github.com/drweihungpan-lab/3R-teaching/issues/9)

Dependencies and the parent relationship are also recorded natively on GitHub. Local task numbers are planning identifiers and may differ from GitHub issue numbers.
