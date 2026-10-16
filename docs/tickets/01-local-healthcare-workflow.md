# Draft 01: Run a minimal healthcare workflow locally

Publication status: proposed; awaiting approval of the breakdown. Draft numbers are not GitHub issue numbers.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

A student can install the supplied package in a Python 3.12 virtual environment, start the supplied FastAPI and Streamlit services locally, upload a small supplied synthetic lab CSV, and view a simple processed result. This is a thin working path across the framework, not a completed statistical project.

## Acceptance criteria

- [ ] Include a suitable small synthetic laboratory dataset with provenance and an explicit teaching-only label.
- [ ] Provide a complete working upload → API → reusable processing → displayed result path; no unfinished functions or mandatory model training.
- [ ] Declare request/response validation and a simple result contract; rejected input is visibly distinguishable from successful processing.
- [ ] Support editable package installation, type hints, and logging with processing logic separate from HTTP and presentation.
- [ ] Document local environment setup, starting both services, and a shareable configuration example; keep local settings ignored.
- [ ] Include focused processing and API behavior tests that pass locally. Do not add the declined course-level acceptance scenario.

## Blocked by

None (can start immediately).

When approved, publish as a ready-for-agent sub-issue of the parent, replacing draft dependencies with native GitHub blocking links where supported. Implementation is a later step.
