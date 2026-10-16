# Draft 03: Prepare the reusable course template and Git/CI demonstration

Publication status: proposed; awaiting approval of the revised breakdown. Draft numbers are not GitHub issue numbers.

Implementation owner: the course author or an assisting implementation agent. This ticket creates course assets; it is not an assignment for students. Student exercises are authored deliverables, not actions students must complete to close this ticket.

## Parent

https://github.com/drweihungpan-lab/3R-teaching/issues/1

## What to build

As the course author, prepare the working example for use as a GitHub template and implement passing CI plus PR/review guidance. Deliver a reusable framework and an instructor demonstration procedure for repository creation, branch changes, review, checks, and merging.

## Acceptance criteria

- [ ] Prepare the repository for GitHub template use and document the instructor template-setting step and group repository creation workflow.
- [ ] Provide GitHub Actions checks for backend tests on pull requests and main; the default supplied example passes.
- [ ] Provide PR guidance covering change purpose, local test results, CI, and review comments on behavior, tests, or clarity.
- [ ] Document feature branch → PR → peer review → main without a develop branch, plus descriptive commits and merge-conflict practice.
- [ ] Explain required checks and branch protection separately from merely running CI; document setup for each generated repository rather than claiming protection is inherited.
- [ ] Make each student's authored PR and review of a teammate's PR inspectable without introducing automated grading.
- [ ] Keep a complete working application in the template and retain configuration hygiene.
- [ ] Provide an instructor rehearsal procedure for the delivered behavior and record focused test results and any environment limits; do not wait for student participation to complete this authoring ticket.

## Blocked by

- Draft 01: Build the local healthcare demonstration framework

When approved, publish as a ready-for-agent sub-issue of the parent, replacing draft dependencies with native GitHub blocking links where supported. No course implementation is performed while drafting or publishing these tickets.
