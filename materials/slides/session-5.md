# Session 5: Final showcase and engineering review

- Demonstrate your group's working application and declared processing behavior.
- Explain the evidence behind the results and each person's contribution.
- Use your own Backend repo, dataset, and question in groups of three or four.
- The [final presentation checklist](../assessment/final-presentation.md) governs this briefing.

---

## Back at the bubble tea shop

**How would you prove to a customer that both shops make the same tea?**

---

## The device example: seven stages, pain to fix

- Stage 1 (Session 1): notebook copied as `v1`/`v2`/`v3`; which copy made the report? **Fix: Git.**
- Stage 2 (Session 1): helper files; works with pandas 1.5, crashes with pandas 2.x. **Fix: isolated environment and declared dependencies.**
- Stage 3 (Session 2): `requirements.txt`; rerunning a cell moves the date. **Fix: functions with inputs and outputs.**
- Stage 4 (Session 2): package; fails from another folder, and a cleanup quietly moves the date. **Fix: tests, and a Release others can install.**
- Stage 5 (Session 3): tests and CI; CI turns red on that cleanup, but only programmers get a prediction. **Fix: API and UI.**
- Stage 6 (Session 4): FastAPI and Streamlit; works only on a correctly set-up machine. **Fix: Docker.**
- Stage 7 (Session 4): Docker; local and Docker give the same limit date. Tell this story in your final presentation. ([Stage READMEs](https://github.com/drweihungpan-lab/3R-sandbox/tree/main/device-example))

---

## Our 170-minute showcase

- Opening brief: 10 minutes. Group slots: 145 minutes in total.
- Shared break: 10 minutes between group slots. Closing: 5 minutes.
- Let G be the actual number of groups; each slot is S = 145 / G minutes.
- Total: 10 + G * S + 10 + 5 = 170 minutes.
- Publish start/end times once G is known; keep fractional minutes or use seconds. Include startup and transitions inside slots.

---

## Use your group slot

- S / 2: live demo, including startup, CSV processing, and invalid-input rejection.
- S / 3: inspect environment, tests, CI, comparisons, and collaboration evidence.
- S / 6: questions, including individual explanations; every member speaks.
- These fractions sum to S. Open evidence promptly and keep transitions within your slot.

---

## Final-only pass/fail assessment

- Every engineering requirement and every student's participation requirement is mandatory; no weighted grades.
- Assessment happens only at this presentation. The result is final: no separate submission, resubmission, reassessment, or later retry.
- Homework and checkpoints were preparation. Modeling is optional; scientific correctness, conclusions, model complexity, and UI polish are not graded.
- Tests and comparisons must still check your declared processing behavior. See the [assessment policy](../../SYLLABUS.md#assessment-policy).

---

## Briefing: open the actual evidence

- Instructor demonstrates navigation using a completed example Backend repo; groups then show their own work.
- Open README evidence links: tested commit SHA, CI run, captures/logs, authored PRs, review permalinks, and the Release tag. A SHA identifies a code version.
- Instructor records repository, date, demonstrated SHA, members, and GitHub usernames in the checklist.
- For every mandatory row, inspect the actual artifact and record Pass/Fail, its URL/path, and an observation. Missing evidence fails that requirement.

---

## Inspect environment, configuration, and Releases

- Show Python 3.12 in an active venv and the installed package working locally.
- Open the dependency declarations in `setup.cfg`; explain how the environment supplies these packages.
- Open ignore rules and the shareable `.env.example`; verify local `.env`, credentials, and `.venv` stay out of tracked files/history.
- Show a tagged Release and install it from its git URL into a fresh virtual environment; run the command-line tool.

---

## Trace the working application

```text
CSV upload -> Frontend page -> HTTP request -> FastAPI
FastAPI -> package processing function -> result
result -> page -> visible table or chart
```

- HTTP carries requests and responses between programs; the processing function works without the API or the page.
- Instructor follows one request through the Frontend repo's client, your API module, and your package, checking inputs and returned results.
- State your dataset, question, and expected behavior briefly before tracing your own application.

---

## Show real startup and CSV results

- Run `docker compose up --build` live; show both services running, backend readiness, and relevant logs or health responses.
- Browser opens `http://127.0.0.1:8501`; the page calls `http://backend:8000` inside Compose. There, localhost means the page itself.
- Upload your group's CSV and show the results or a chart.
- Instructor inspects actual service communication and output, not only configuration. Stop standalone servers using the same ports first.

---

## Show validation and its test

- Demonstrate one invalid input rejected clearly; it must not appear as a successful result.
- Explain the rule: expected types, allowed bounds, or missing-value handling. Missing does not mean zero.
- Show the API error for the rejected input and open its corresponding passing validation test.
- Instructor checks the observed rejection against the group's declared rule.

---

## Inspect local tests and hosted CI

- In the active local environment, run `pytest`; show passing output.
- Open a successful GitHub Actions run for the demonstrated commit with the test job switched on. CI means automated checks on GitHub; a local pass alone is insufficient.
- Instructor opens tests for processing, invalid inputs, and agreement rules.
- Tests check declared behavior, not scientific validity. A workflow reporting success does not itself configure required checks.

---

## Demonstrate the two practical Rs

- Repeatability: agreement under the same conditions. Compare local run 1 with local run 2.
- Replicability: agreement under slightly different conditions. Compare a Release installed in a fresh environment, and a real Docker run, with the local run.
- Keep code and CSV unchanged; show successful comparisons, underlying captures, commands, logs, and environment details.
- Reproducibility means agreement under very different conditions in this course; independent simulation, cross-group reproduction, and new-data experiments are not required.
- Use the [glossary](../../GLOSSARY.md).

---

## Inspect agreement, field by field

- Exact: cleaned records, identifiers, dates, counts, types, structure, ordering, and nulls. Missing stays distinct from zero.
- Only derived decimals receive declared tolerances documented in tests.

```text
abs(actual - expected) <= max(1e-9, 1e-9 * abs(expected))
```

- The first output is the reference. Instructor opens outputs and diagnostics; matching charts alone are insufficient. Do not drop fields, round away differences, or widen tolerance to pass.

---

## Inspect collaboration and every member

- Open feature branches, descriptive commits, PRs, and meaningful teammate reviews in the Backend repo about behavior, tests, or clarity; show responses/follow-up to concerns.
- For EACH student: open at least one personally authored PR and at least one substantive review of a teammate's PR, with authorship and review permalinks.
- Each member explains their contribution, authored change, review reasoning, and any follow-up. Approval alone or “looks good” is insufficient.
- Instructor completes an individual evidence row for every member. Sandbox practice, generated template history, and instructor/agent work do not count.

---

## Questions follow the evidence

- Why does this input fail? Open the rejection and the test that establishes the rule.
- Which code and input produced these outputs? Open the commit and capture fingerprints, then explain environment differences.
- Which fields compare exactly, and why is a derived value allowed tolerance? Open the comparison and its tests.
- What did you change or ask a teammate to improve? Open your PR or review and explain the result.

---

## Shared break and remaining groups

- Take the reserved 10-minute break at the published slot boundary.
- Resume with the next group's live demo, evidence inspection, and questions using the same S allocation.
- Every group uses the same mandatory checklist; keep the reserved five-minute closing within the 170 minutes.

---

## Closing: connect the engineering evidence

- Use the final five minutes to connect environment, package and Release, API/UI, containers, tests, comparisons, and peer review.
- Pass requires every mandatory group row and every student's individual participation requirement to pass.
- Instructor records failed rows and reasons at the presentation; no averaging or complexity bonuses, and no later retry.
- The [final checklist](../assessment/final-presentation.md) and [syllabus](../../SYLLABUS.md#assessment-policy) remain the assessment reference.
