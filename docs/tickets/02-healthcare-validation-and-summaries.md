# Draft 02: Complete the healthcare cleaning and validation demonstration

Publication status: proposed; awaiting approval of the revised breakdown. Draft numbers are not GitHub issue numbers.

Implementation owner: the course author or an assisting implementation agent. This ticket creates course assets; it is not an assignment for students. Student exercises are authored deliverables, not actions students must complete to close this ticket.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

As the course author, extend the runnable demonstration to join synthetic participant and laboratory data, preserve missing values, validate inputs, and display summaries and a chart. Deliver the complete simple healthcare example that subsequent slides and exercises will reference.

## Acceptance criteria

- [ ] Reuse suitable synthetic participant and laboratory data from clinical-data-teaching, documenting provenance, used fields, and expected behavior.
- [ ] Validate join keys, duplicate observations, required fields, numeric input, and units under an explicitly documented contract.
- [ ] Preserve unavailable values as missing rather than zero and make observed and missing counts visible.
- [ ] Show participant-level baseline/change values and visit summaries where supported by the supplied data; document missing-baseline behavior.
- [ ] Return stable, inspectable results through the API and display summaries or a chart in Streamlit.
- [ ] Extend focused processing/API tests for the declared valid and invalid cases, including missingness and join failures.
- [ ] Explain how groups can replace or adapt the data-processing example without requiring a particular statistical model.
- [ ] Provide an instructor rehearsal procedure for the delivered behavior and record focused test results and any environment limits; do not wait for student participation to complete this authoring ticket.

## Blocked by

- Draft 01: Build the local healthcare demonstration framework

When approved, publish as a ready-for-agent sub-issue of the parent, replacing draft dependencies with native GitHub blocking links where supported. No course implementation is performed while drafting or publishing these tickets.
