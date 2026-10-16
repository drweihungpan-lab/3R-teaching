# 06: Add the backend Dockerfile

Published as [GitHub issue #7](https://github.com/drweihungpan-lab/3R-teaching/issues/7), labeled `ready-for-agent`.

Approved course-authoring task. Implementation owner: the course author or an assisting agent. Student participation is not a completion condition.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

Create the runnable container image for the healthcare API service.

## Acceptance criteria

- [ ] Use a Python 3.12 slim base and install the declared package/runtime dependencies.
- [ ] Run the backend on the documented internal port with appropriate container binding.
- [ ] Keep local environments, secrets, and caches out of the build context.
- [ ] Document an image build, service start, and sample API request with expected behavior.
- [ ] Report actual build/run verification or the environment limitation.
- [ ] Do not implement the frontend image or Compose orchestration in this task; multi-stage optimization is optional.

## Blocked by

- [#3: Implement the backend API and Python processing package](https://github.com/drweihungpan-lab/3R-teaching/issues/3)

Dependencies and the parent relationship are also recorded natively on GitHub. Local task numbers are planning identifiers and may differ from GitHub issue numbers.
