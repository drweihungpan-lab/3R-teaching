# 07: Add the frontend Dockerfile

Published as [GitHub issue #8](https://github.com/drweihungpan-lab/3R-teaching/issues/8), labeled `ready-for-agent`.

Approved course-authoring task. Implementation owner: the course author or an assisting agent. Student participation is not a completion condition.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

Create the runnable container image for the supplied Streamlit interface.

## Acceptance criteria

- [ ] Install declared frontend dependencies and start Streamlit on a documented port.
- [ ] Accept backend configuration through the environment rather than embedding a fixed local address.
- [ ] Keep local environments and secrets out of the build context.
- [ ] Document image build/start and the expected interface behavior.
- [ ] Report actual build/run verification or the environment limitation.
- [ ] Do not implement Compose orchestration in this task.

## Blocked by

- [#4: Implement the Streamlit frontend](https://github.com/drweihungpan-lab/3R-teaching/issues/4)

Dependencies and the parent relationship are also recorded natively on GitHub. Local task numbers are planning identifiers and may differ from GitHub issue numbers.
