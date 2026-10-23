# Session 5: Final showcase and engineering review

- Demonstrate your group's working application and declared processing behavior.
- Explain the evidence behind the results and each person's contribution.
- Use your own repository, dataset, and question in groups of three or four.
- The [final presentation checklist](../assessment/final-presentation.md) governs this briefing.

---

## Back at the bubble tea shop

**How would you prove to a customer that both shops make the same tea?**

---

## Our 180-minute showcase

- Opening brief: 10 minutes. Group slots: 150 minutes in total.
- Shared break: 15 minutes between group slots. Closing: 5 minutes.
- Let G be the actual number of groups; each slot is S = 150 / G minutes.
- Total: 10 + G * S + 15 + 5 = 180 minutes.
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

- Instructor demonstrates navigation using the completed synthetic example; groups then show their own work.
- Open README evidence links: tested commit SHA, CI run, captures/logs, authored PRs, and review permalinks. A SHA identifies a code version.
- Instructor records repository, date, demonstrated SHA, members, and GitHub usernames in the checklist.
- For every mandatory row, inspect the actual artifact and record Pass/Fail, its URL/path, and an observation. Missing evidence fails that requirement.

---

## Inspect environment and configuration

- Show Python 3.12 in an active venv, its interpreter path, and the installed reusable package working locally.
- Open dependency declarations in [backend/pyproject.toml](../../backend/pyproject.toml); explain how the environment supplies these packages.
- Open ignore rules and shareable .env.example; verify local .env, credentials, and .venv stay out of tracked files/history.
- Explain local versus container settings without showing secrets. Instructor inspects files and execution, alongside the [setup guide](../../docs/setup.md).

---

## Trace the working application

```text
CSV upload -> Streamlit -> HTTP request -> FastAPI
FastAPI -> reusable stat_core processing -> result
result -> Streamlit -> visible records/summary/chart
```

- HTTP carries requests and responses between programs; reusable processing functions work without the API or UI.
- Instructor follows one request through [frontend](../../frontend/app.py), [API](../../backend/app/main.py), and [package](../../backend/stat_core/__init__.py), checking inputs and returned results.
- State your dataset, question, and expected behavior briefly before tracing your own application.

---

## Show real startup and CSV results

- Run `docker compose up --build` live; show frontend/backend running, backend readiness, and relevant logs or health responses.
- Browser opens `http://127.0.0.1:8501`; frontend calls `http://backend:8000` inside Compose. There, localhost means the frontend itself.
- Upload and process CSVs; show results or a chart. In the supplied example, upload DM and LB: 24 participants, 96 records, 95 observed, 1 missing.
- Instructor inspects actual service communication and output, not only configuration. Follow the [Compose guide](../../docs/compose.md); stop standalone servers using the same ports first.

---

## Show validation and its test

- Demonstrate one invalid input rejected clearly; it must not appear as a successful result.
- Explain the rule: expected types, allowed bounds, or missing-value handling. Missing does not mean zero.
- In the supplied example, show the API error and open its corresponding passing validation test.
- Instructor checks the observed rejection against the [API contract](../../docs/api.md) and the group's declared rule.

---

## Inspect local tests and hosted CI

- In the active local environment, run `python -m pytest backend/tests`; show passing output.
- Open a successful GitHub Actions run for the demonstrated commit. CI means automated checks on GitHub; a local pass alone is insufficient.
- Instructor opens tests at public processing, API, and comparison boundaries: expected outputs, invalid inputs, and agreement rules.
- Tests check declared behavior, not scientific validity. A workflow reporting success does not itself configure required checks; see [testing](../../docs/testing.md) and [CI](../../docs/ci.md).

---

## Demonstrate the two practical Rs

- Repeatability: agreement under the same conditions. Compare local run 1 with local run 2.
- Replicability: agreement under slightly different conditions. Compare local with real Docker execution of the same process.
- Keep code and CSV bytes unchanged; show successful comparisons, underlying captures, commands, logs, environment details, and code/input identity.
- Reproducibility means agreement under very different conditions in this course; independent simulation, cross-group reproduction, and new-data experiments are not required.
- Use the [glossary](../../GLOSSARY.md) and [capture/comparison commands](../../docs/comparisons.md).

---

## Inspect agreement, field by field

- Exact: cleaned records, identifiers, raw values, copied baselines, counts, types, structure, ordering, and nulls. Missing stays distinct from zero.
- Only derived decimals receive declared tolerances documented in tests. In the example: change, percent_change, and visit-summary mean.

```text
abs(actual - expected) <= max(1e-9, 1e-9 * abs(expected))
```

- The first output is the reference. Instructor opens outputs and diagnostics; matching charts alone are insufficient. Do not drop fields, round away differences, or widen tolerance to pass.

---

## Inspect collaboration and every member

- Open feature branches, descriptive commits, PRs, and meaningful teammate reviews about behavior, tests, or clarity; show responses/follow-up to concerns.
- For EACH student: open at least one personally authored PR and at least one substantive review of a teammate's PR, with authorship and review permalinks.
- Each member explains their contribution, authored change, review reasoning, and any follow-up. Approval alone or “looks good” is insufficient.
- Instructor completes an individual evidence row for every member. Template history and instructor/agent work do not count; see the [collaboration guide](../../docs/collaboration.md).

---

## Questions follow the evidence

- Why does this input fail? Open the rejection and the test that establishes the rule.
- Which code and input produced these outputs? Open the commit and capture fingerprints, then explain environment differences.
- Which fields compare exactly, and why is a derived value allowed tolerance? Open the comparison and its tests.
- What did you change or ask a teammate to improve? Open your PR or review and explain the result.

---

## Shared break and remaining groups

- Take the reserved 15-minute break at the published slot boundary.
- Resume with the next group's live demo, evidence inspection, and questions using the same S allocation.
- Every group uses the same mandatory checklist; keep the reserved five-minute closing within the three hours.

---

## Closing: connect the engineering evidence

- Use the final five minutes to connect environment, package, API/UI, containers, tests, comparisons, and peer review.
- Pass requires every mandatory group row and every student's individual participation requirement to pass.
- Instructor records failed rows and reasons at the presentation; no averaging or complexity bonuses, and no later retry.
- The [final checklist](../assessment/final-presentation.md) and [syllabus](../../SYLLABUS.md#assessment-policy) remain the assessment reference.
