# 08: Configure Docker Compose services

Published as [GitHub issue #9](https://github.com/drweihungpan-lab/3R-teaching/issues/9), labeled `ready-for-agent`.

Approved course-authoring task. Implementation owner: the course author or an assisting agent. Student participation is not a completion condition.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

Connect the supplied backend and frontend containers into a stack the instructor can launch for demonstrations.

## Acceptance criteria

- [ ] Build and start both services through Docker Compose.
- [ ] Configure frontend-to-backend communication using the backend service name and internal port.
- [ ] Handle backend readiness so frontend startup does not rely on an arbitrary delay.
- [ ] Document local versus container addresses, startup, shutdown, and common connection problems.
- [ ] Demonstrate the sample upload and visible processing results, or report verification limits.
- [ ] Do not add cloud hosting, databases, or production deployment infrastructure.

## Blocked by

- [#7: Add the backend Dockerfile](https://github.com/drweihungpan-lab/3R-teaching/issues/7)
- [#8: Add the frontend Dockerfile](https://github.com/drweihungpan-lab/3R-teaching/issues/8)

Dependencies and the parent relationship are also recorded natively on GitHub. Local task numbers are planning identifiers and may differ from GitHub issue numbers.
