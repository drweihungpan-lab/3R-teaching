# Session 3 instructor notes: tests and automated CI

Students add tests to their Backend repo, switch on the commented-out `test-pytest` job, and watch a controlled failing test turn CI red and green. Use the [slides](../slides/session-3.md), [guided exercise](../exercises/session-3.md), and the [glossary](../../GLOSSARY.md).

## Prepare before class

- Every group needs its Session 2 Backend repo merged to `main` with the Release tagged. Fix any group that is behind during the first minutes.
- Rehearse the exercise on a freshly generated repo: switch on the job, add the validation and tests, run `make format` and `make test-all`, break one expected date, then restore it.
- `make test-all` includes the `black` check, so students must run `make format` after typing the new tests; a failing formatting check is a common surprise.
- Decide how you show the editor's comment toggle for YAML (VS Code `Ctrl+/` or `Cmd+/`). Leave the OPTIONAL release job commented.

## 170-minute run sheet

| Clock | Mode | Slides | Delivery |
| --- | --- | --- | --- |
| 0–10 | Opening | Back at the bubble tea shop; Device example, Stage 5 | A customer asks for −20% sugar: what do you do? Then show the "cleanup" PR failing CI. |
| 10–60 | Explanation | A test states what you expect; pytest finds and runs tests; Fixtures provide reusable inputs; Declare exact and approximate agreement; Invalid input must fail clearly; Connect checks to the course's three Rs | Expected values written in advance; collection rules; fixtures and `tmp_path`; exact versus `pytest.approx`; error messages. |
| 60–70 | Break | | 10 minutes. |
| 70–100 | Explanation | Switch on the test job; Reporting a check is different from requiring it | Show the commented job and un-comment it; explain commit-specific checks versus required rules. |
| 100–130 | Demonstration | Demo: add a validation and its test; Demo: a controlled failure | Perform the exercise live, including `make format`, a red PR check, and the green re-run. |
| 130–170 | Hands-on | Hands-on: 40 minutes; Checkpoint and next step | [Exercise](../exercises/session-3.md) §§1–4. |

## Cues and expected observations

- After un-commenting, the PR shows **test-formatting-linting** and **test-pytest**, both green.
- The new tests give `6 passed` in the generated repo after the exercise; the controlled failure shows `{'DEV-B': datetime.date(2026, 4, 1)} != {'DEV-B': datetime.date(2026, 4, 2)}`.
- Common failures: broken YAML indentation after toggling comments; forgetting `make format`; a test file edited but not saved; reading an old CI run instead of the latest commit's.

## Rehearsal checklist

- [ ] Switch on the job on a fresh generated repo; both checks pass.
- [ ] The validation and its tests pass `make test-all`.
- [ ] The failure and fix produce red then green on the same PR.
