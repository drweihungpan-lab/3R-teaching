# Draft 04: Run the healthcare stack in Docker and compare outputs

Publication status: proposed; awaiting approval of the breakdown. Draft numbers are not GitHub issue numbers.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

A student can start the complete example with Docker Compose, follow the same upload and processing workflow, and demonstrate repeatability locally and replicability between the local virtual environment and Docker using the same data and code.

## Acceptance criteria

- [ ] Supply separate backend and frontend images and Compose configuration with understandable networking and service readiness.
- [ ] Document container service names versus local addresses and show how the frontend reaches the backend.
- [ ] Run the full supplied healthcare example with visible results and actionable startup/connection error guidance.
- [ ] Provide a documented way to capture and compare repeated local outputs and local-versus-Docker outputs.
- [ ] Compare cleaned records and counts exactly; specify and explain numerical tolerances for calculated decimals in the relevant tests.
- [ ] Demonstrate that comparison rejects material mismatches and does not equate missing values with zero.
- [ ] Use the course meanings of repeatability and replicability; do not require cross-group reproduction, independent experiments, or an additional end-to-end acceptance framework.
- [ ] Keep multi-stage image optimization optional.

## Blocked by

- Draft 02: Process participant and lab data with explicit validation

When approved, publish as a ready-for-agent sub-issue of the parent, replacing draft dependencies with native GitHub blocking links where supported. Implementation is a later step.
