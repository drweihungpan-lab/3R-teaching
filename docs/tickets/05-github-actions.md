# 05: Configure GitHub Actions CI

Published as [GitHub issue #6](https://github.com/drweihungpan-lab/3R-teaching/issues/6), labeled `ready-for-agent`.

Approved course-authoring task. Implementation owner: the course author or an assisting agent. Student participation is not a completion condition.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

Add automated backend checks that make passing and failing tests visible on pull requests and main.

## Acceptance criteria

- [ ] Run the existing backend test suite under Python 3.12 on PRs targeting main and pushes to main.
- [ ] Install declared backend and test dependencies in the workflow and configure caching against the actual dependency metadata.
- [ ] Use understandable job names and minimal required repository permissions.
- [ ] Document how to inspect a failure and its correction without leaving the default example broken.
- [ ] Explain that CI reporting does not itself configure required checks or branch protection.
- [ ] Verify the workflow as far as the available environment permits and state any limits.

## Blocked by

- [#5: Add backend processing and API tests](https://github.com/drweihungpan-lab/3R-teaching/issues/5)

Dependencies and the parent relationship are also recorded natively on GitHub. Local task numbers are planning identifiers and may differ from GitHub issue numbers.
