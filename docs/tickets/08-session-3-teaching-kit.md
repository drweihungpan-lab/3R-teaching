# Draft 08: Create the Session 3 teaching materials

Publication status: proposed; awaiting approval of the revised breakdown. Draft numbers are not GitHub issue numbers.

Implementation owner: the course author or an assisting implementation agent. This ticket creates course assets; it is not an assignment for students. Student exercises are authored deliverables, not actions students must complete to close this ticket.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

As the course author, produce a complete teachable Session 3 kit covering FastAPI, Pydantic validation, pytest, and CI. Deliver editable PowerPoint slides with Markdown sources, a timed instructor run sheet, a controlled failing-test demonstration with recovery instructions, guided exercises and expected results, and a two-hour homework brief.

## Acceptance criteria

- [ ] Provide editable English PowerPoint slides, matching Markdown sources, instructor notes, and guided exercises using the completed framework.
- [ ] Explain FastAPI/Pydantic contracts, missingness, invalid types and bounds, fixtures, numerical tolerances, and local-to-CI execution.
- [ ] Include a controlled failure/correction exercise, with expected API responses and test outcomes; keep the distributed default example passing.
- [ ] Teach tests against declared external behavior without testing scientific conclusions or adding the declined course-level acceptance scenario.
- [ ] Include approximately two hours of mandatory homework demonstrating processing/validation tests, CI evidence, and peer review.
- [ ] Use the provisional session allocation and describe the checkpoint as preparation for the final presentation.
- [ ] Explain that CI reports results and branch protection determines whether passing checks are required to merge.
- [ ] Include an author rehearsal checklist with exact demo steps, expected observations, timing estimates, and recovery guidance; completion of the ticket means the kit is authored and checked, not that students have completed the activities.

## Blocked by

- Draft 02: Complete the healthcare cleaning and validation demonstration
- Draft 03: Prepare the reusable course template and Git/CI demonstration

When approved, publish as a ready-for-agent sub-issue of the parent, replacing draft dependencies with native GitHub blocking links where supported. No course implementation is performed while drafting or publishing these tickets.
