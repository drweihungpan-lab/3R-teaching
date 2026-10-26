# Session 5 instructor notes: final showcase and engineering review

Each group demonstrates its working application and shows the evidence in its own Backend repo. Use the [slides](../slides/session-5.md), the [final presentation checklist](../assessment/final-presentation.md), the [syllabus](../../SYLLABUS.md), and the [glossary](../../GLOSSARY.md).

## Prepare before the session

- Publish start and end times once the number of groups G is known. Each slot is S = 145 / G minutes; the brief is 10, the shared break 10, the closing 5, total 170.
- Print or open the checklist for every group and every student. Have the repository links, tested commit SHAs, and CI run links from each group's README ready.
- Confirm the room has Docker running, a stable network, and ports 8000 and 8501 free, and that each group can start its stack within its slot.
- Prepare a completed example Backend repo for the opening navigation demonstration.

## 170-minute run sheet

| Clock | Mode | Slides | Delivery |
| --- | --- | --- | --- |
| 0–10 | Brief | Back at the bubble tea shop; The device example: seven stages; Our 170-minute showcase; Use your group slot; Final-only pass/fail assessment; Briefing | Ask how to prove both shops make the same tea. Recap the seven stages, explain the slot allocation, and walk through opening the evidence. |
| 10–155 | Group slots | Inspect environment, configuration, and Releases; Trace the working application; Show real startup and CSV results; Show validation and its test; Inspect local tests and hosted CI; Demonstrate the two practical Rs; Inspect agreement, field by field; Inspect collaboration and every member; Questions follow the evidence | Each group uses S minutes: half for the live demo, a third for evidence inspection, a sixth for questions. Insert the shared break at the published boundary. |
| Break | Shared break | Shared break and remaining groups | 10 minutes at the published boundary. |
| 165–170 | Closing | Closing | Connect environment, Release, API and page, containers, tests, comparisons, and peer review. |

## Demo and inspection cues

- Environment: Python 3.12 in an active venv; the dependency declarations in `setup.cfg`; a tagged Release installed from its git URL into a fresh environment, and the command run.
- Application: an upload through the Frontend page reaches the group's API, which calls the package, and the result appears.
- Validation: one invalid input is rejected with a message, and the matching test passes.
- Tests and CI: local pytest passing, and a green GitHub Actions run with the test job switched on for the demonstrated commit.
- Practical Rs: local run 1 equals local run 2; a Release installed in a fresh environment and a real Docker run agree with the local run, with captures kept.
- Collaboration: for each student, an authored PR and a substantive review of a teammate's PR in the Backend repo, with permalinks. Sandbox practice does not count.

## Likely questions and bounded recovery

- A stack that does not start within the slot: inspect the logs once, record the failure honestly, and continue with the remaining evidence rows. Missing evidence fails that row; there is no retry.
- A Release that cannot be installed: check that the repository is public and the tag was pushed; do not fix it during the slot.
- A student without an authored PR or a review: record it as a failed individual row.

## Rehearsal checklist

- [ ] Slot times published; checklist ready per group and student.
- [ ] The example Backend repo opens each evidence item in order.
- [ ] Docker, network and ports checked on the demonstration machine.
