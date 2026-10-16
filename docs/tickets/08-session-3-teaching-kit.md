# Draft 08: Teach Session 3: validation, pytest, and automated checks

Publication status: proposed; awaiting approval of the breakdown. Draft numbers are not GitHub issue numbers.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

The instructor can teach Session 3 and students can trace API processing, exercise invalid input, inspect a controlled failing test, correct it, and observe passing local tests and PR checks.

## Acceptance criteria

- [ ] Provide editable English PowerPoint slides, matching Markdown sources, instructor notes, and guided exercises using the completed framework.
- [ ] Explain FastAPI/Pydantic contracts, missingness, invalid types and bounds, fixtures, numerical tolerances, and local-to-CI execution.
- [ ] Include a controlled failure/correction exercise, with expected API responses and test outcomes; keep the distributed default example passing.
- [ ] Teach tests against declared external behavior without testing scientific conclusions or adding the declined course-level acceptance scenario.
- [ ] Include approximately two hours of mandatory homework demonstrating processing/validation tests, CI evidence, and peer review.
- [ ] Use the provisional session allocation and describe the checkpoint as preparation for the final presentation.
- [ ] Explain that CI reports results and branch protection determines whether passing checks are required to merge.

## Blocked by

- Draft 02: Process participant and lab data with explicit validation
- Draft 03: Use a group template with reviewed pull requests and CI

When approved, publish as a ready-for-agent sub-issue of the parent, replacing draft dependencies with native GitHub blocking links where supported. Implementation is a later step.
