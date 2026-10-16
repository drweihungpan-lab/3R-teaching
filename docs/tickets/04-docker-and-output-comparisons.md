# Draft 04: Implement Docker execution and first-two-R demonstration tools

Publication status: proposed; awaiting approval of the revised breakdown. Draft numbers are not GitHub issue numbers.

Implementation owner: the course author or an assisting implementation agent. This ticket creates course assets; it is not an assignment for students. Student exercises are authored deliverables, not actions students must complete to close this ticket.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

As the course author, containerize the working example and implement the comparison tools and demonstration instructions needed to show repeatability locally and replicability between a local virtual environment and Docker. Deliver runnable services, output comparison behavior, tests, and instructor troubleshooting notes.

## Acceptance criteria

- [ ] Supply separate backend and frontend images and Compose configuration with understandable networking and service readiness.
- [ ] Document container service names versus local addresses and show how the frontend reaches the backend.
- [ ] Run the full supplied healthcare example with visible results and actionable startup/connection error guidance.
- [ ] Provide a documented way to capture and compare repeated local outputs and local-versus-Docker outputs.
- [ ] Compare cleaned records and counts exactly; specify and explain numerical tolerances for calculated decimals in the relevant tests.
- [ ] Demonstrate that comparison rejects material mismatches and does not equate missing values with zero.
- [ ] Use the course meanings of repeatability and replicability; do not require cross-group reproduction, independent experiments, or an additional end-to-end acceptance framework.
- [ ] Keep multi-stage image optimization optional.
- [ ] Provide an instructor rehearsal procedure for the delivered behavior and record focused test results and any environment limits; do not wait for student participation to complete this authoring ticket.

## Blocked by

- Draft 02: Complete the healthcare cleaning and validation demonstration

When approved, publish as a ready-for-agent sub-issue of the parent, replacing draft dependencies with native GitHub blocking links where supported. No course implementation is performed while drafting or publishing these tickets.
