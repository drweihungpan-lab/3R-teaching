# Draft 03: Use a group template with reviewed pull requests and CI

Publication status: proposed; awaiting approval of the breakdown. Draft numbers are not GitHub issue numbers.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

A group can create its own repository from the working example, make a small change on a feature branch, request a meaningful peer review, inspect automated tests, and merge into main with the collaboration evidence visible to the instructor.

## Acceptance criteria

- [ ] Prepare the repository for GitHub template use and document the instructor template-setting step and group repository creation workflow.
- [ ] Provide GitHub Actions checks for backend tests on pull requests and main; the default supplied example passes.
- [ ] Provide PR guidance covering change purpose, local test results, CI, and review comments on behavior, tests, or clarity.
- [ ] Document feature branch → PR → peer review → main without a develop branch, plus descriptive commits and merge-conflict practice.
- [ ] Explain required checks and branch protection separately from merely running CI; document setup for each generated repository rather than claiming protection is inherited.
- [ ] Make each student's authored PR and review of a teammate's PR inspectable without introducing automated grading.
- [ ] Keep a complete working application in the template and retain configuration hygiene.

## Blocked by

- Draft 01: Run a minimal healthcare workflow locally

When approved, publish as a ready-for-agent sub-issue of the parent, replacing draft dependencies with native GitHub blocking links where supported. Implementation is a later step.
