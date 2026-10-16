# Draft 02: Process participant and lab data with explicit validation

Publication status: proposed; awaiting approval of the breakdown. Draft numbers are not GitHub issue numbers.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

A student can upload the supplied participant and laboratory CSVs, obtain a validated join, and inspect cleaned observations, summaries, and a simple chart. The complete example demonstrates understandable data cleaning rather than model training.

## Acceptance criteria

- [ ] Reuse suitable synthetic participant and laboratory data from clinical-data-teaching, documenting provenance, used fields, and expected behavior.
- [ ] Validate join keys, duplicate observations, required fields, numeric input, and units under an explicitly documented contract.
- [ ] Preserve unavailable values as missing rather than zero and make observed and missing counts visible.
- [ ] Show participant-level baseline/change values and visit summaries where supported by the supplied data; document missing-baseline behavior.
- [ ] Return stable, inspectable results through the API and display summaries or a chart in Streamlit.
- [ ] Extend focused processing/API tests for the declared valid and invalid cases, including missingness and join failures.
- [ ] Explain how groups can replace or adapt the data-processing example without requiring a particular statistical model.

## Blocked by

- Draft 01: Run a minimal healthcare workflow locally

When approved, publish as a ready-for-agent sub-issue of the parent, replacing draft dependencies with native GitHub blocking links where supported. Implementation is a later step.
