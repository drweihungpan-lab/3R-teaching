# Draft 01: Build the local healthcare demonstration framework

Publication status: proposed; awaiting approval of the revised breakdown. Draft numbers are not GitHub issue numbers.

Implementation owner: the course author or an assisting implementation agent. This ticket creates course assets; it is not an assignment for students. Student exercises are authored deliverables, not actions students must complete to close this ticket.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

As the course author, implement the first runnable demonstration: a Python 3.12 package, FastAPI backend, and Streamlit frontend that accept the supplied synthetic laboratory CSV and display a simple processed result. Deliver working code, focused tests, configuration examples, and instructor setup notes for this narrow complete path.

## Acceptance criteria

- [ ] Include a suitable small synthetic laboratory dataset with provenance and an explicit teaching-only label.
- [ ] Provide a complete working upload → API → reusable processing → displayed result path; no unfinished functions or mandatory model training.
- [ ] Declare request/response validation and a simple result contract; rejected input is visibly distinguishable from successful processing.
- [ ] Support editable package installation, type hints, and logging with processing logic separate from HTTP and presentation.
- [ ] Document local environment setup, starting both services, and a shareable configuration example; keep local settings ignored.
- [ ] Include focused processing and API behavior tests that pass locally. Do not add the declined course-level acceptance scenario.
- [ ] Provide an instructor rehearsal procedure for the delivered behavior and record focused test results and any environment limits; do not wait for student participation to complete this authoring ticket.

## Blocked by

None (can start immediately).

When approved, publish as a ready-for-agent sub-issue of the parent, replacing draft dependencies with native GitHub blocking links where supported. No course implementation is performed while drafting or publishing these tickets.
