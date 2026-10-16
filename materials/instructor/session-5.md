# Session 5 instructor notes: final showcase and engineering review

Deliver the final showcase in 180 minutes using the [actual slide source](../slides/session-5.md) and [final presentation brief/checklist](../assessment/final-presentation.md). These notes implement [issue #37](https://github.com/drweihungpan-lab/3R-teaching/issues/37) under the [specification](../../docs/specs/course-framework-and-teaching-materials.md), [syllabus](../../SYLLABUS.md#assessment-policy), and [course glossary](../../GLOSSARY.md).

## Prepare before the session

- Confirm the actual group count `G`, three or four students per group, repository access, member names/GitHub usernames, and presentation order. Open each group's README evidence links before class; preserve access to CI artifacts before expiry.
- Prepare Python 3.12, an active venv with installed backend/development and frontend dependencies, Git, Docker with a running engine and Compose v2, browser, editor, curl, and two terminals. Follow [setup](../../docs/setup.md), [frontend setup](../../docs/frontend.md), and [Compose](../../docs/compose.md); install/rehearse before the timed session.
- Have unchanged [DM](../../data/synthetic/dm.csv) and [LB](../../data/synthetic/lb.csv), their [provenance](../../data/synthetic/README.md), and [dictionary](../../data/synthetic/data-dictionary.md). Prepare an ignored invalid DM copy with first data-row `AGE=not-a-number`; keep originals ready. Groups use their own data and declared rules.
- Bookmark [API](../../docs/api.md), [tests](../../docs/testing.md), [CI](../../docs/ci.md), [comparisons](../../docs/comparisons.md), and [collaboration](../../docs/collaboration.md). Open the demonstrated SHA, matching CI run, captures/logs, and individual PR/review permalinks in tabs.
- Copy the checklist's group record and individual row for every member into the instructor record. Prepare a roster linking each student to a personally authored PR and a substantive review of a teammate's PR; verify authorship and follow-up, not just search results.
- Rehearse the supplied example for briefing navigation. Label instructor/agent artifacts and saved rehearsal output with source, SHA, environment, and date; they never count as students' participation or as an unseen classroom demonstration.

## Adaptive 180-minute run sheet

Use `S = 150 / G` minutes per group. Publish exact start/end times using fractional minutes or seconds; startup and transitions belong inside slots. Put the 15-minute break after `k` complete slots, with `1 <= k < G`, chosen before class.

| Period | Minutes from start | Delivery cue |
| --- | --- | --- |
| Opening | 0–10 | State the same brief and mandatory checklist for everyone; demonstrate evidence navigation briefly. |
| First `k` groups | 10 to `10 + k*S` | Each group: `S/2` demo, `S/3` evidence inspection, `S/6` questions/individual explanations. |
| Shared break | `10 + k*S` to `25 + k*S` | Stop at a slot boundary; announce the exact return time. |
| Remaining groups | `25 + k*S` to 175 | Repeat the same slot fractions and checklist for every group. |
| Closing | 175–180 | Connect the engineering evidence and complete final decisions/reasons. |

Check: `10 + G*S + 15 + 5 = 180`; `S/2 + S/3 + S/6 = S`. For example, `G=6` gives 25-minute slots: demo 12m30s, evidence 8m20s, questions 4m10s. This is an example, not a fixed group count. Reserve speaking time for every member and give consistent time cues.

## Map actual slides to the showcase activity

The activity is the group's live presentation and the checklist evidence record, including its individual rows. There is no Session 5 exercise or homework. Titles below match the slide source; keep technical slides available as inspection prompts during each slot.

| Actual slide title | Instructor cue / checklist activity |
| --- | --- |
| Session 5: Final showcase and engineering review | Introduce group-owned datasets/questions; explain the engineering focus. |
| Our 180-minute showcase | Publish `G`, slot times, break boundary, and closing time. |
| Use your group slot | Announce demo/evidence/questions fractions and transitions. |
| Final-only pass/fail assessment | Read finality and every-mandatory-row rules from the brief. |
| Briefing: open the actual evidence | Model navigation; record repository, date, SHA, members, usernames. |
| Inspect environment and configuration | Inspect active interpreter, package/dependencies, ignore rules and safe configuration. |
| Trace the working application | Follow one CSV request through UI → HTTP API → reusable processing → results. |
| Show real startup and CSV results | Observe live Compose readiness, service communication, upload and visible results. |
| Show validation and its test | Observe rejection; open the corresponding passing API test. |
| Inspect local tests and hosted CI | Observe local pytest; inspect successful hosted checks for demonstrated code. |
| Demonstrate the two practical Rs | Inspect same-condition local runs, then local/real-Docker captures. |
| Inspect agreement, field by field | Open exact fields, nulls, derived tolerances and comparison diagnostics. |
| Inspect collaboration and every member | Open each authored PR/review and hear each person's explanation. |
| Questions follow the evidence | Ask about rejection, identity, agreement, and review reasoning using actual artifacts. |
| Shared break and remaining groups | Take the published break; resume with the same brief and slot allocation. |
| Closing: connect the engineering evidence | Record final Pass/Fail and reasons against all mandatory rows. |

## Demo and inspection cues: expected observations

Use the example in rehearsal; apply the same inspection to each group's declared behavior rather than demanding the example's counts from other datasets. Commands run from the demonstrated repository root with the prepared local venv active.

```bash
docker compose version
docker compose config --quiet
docker compose up --build
```

Keep logs open; in the second terminal run `docker compose ps` and `curl --fail-with-body http://127.0.0.1:8000/health`. Expect running frontend/backend, a healthy backend, and `{"status":"ok"}`. Open `http://127.0.0.1:8501`; inspect frontend configuration and actual HTTP/log evidence for `http://backend:8000`. Inside the frontend, localhost means that container. A Compose file or health response alone does not prove CSV processing.

Upload original DM/LB and select **Process CSVs**. Expect 24 participants, 96 records, 95 observed, one missing, tables and a chart. Follow [frontend](../../frontend/app.py) → [API](../../backend/app/main.py) → [stat_core](../../backend/stat_core/__init__.py); ask which functions can run without HTTP/UI. Missing `EDU-LPA-007` DAY 30 stays null, not zero; subject `001` stays text.

Upload the invalid DM copy with original LB. Expect clear HTTP 422: participants, CSV row 2, AGE, “Expected a nonnegative integer.” Invalid input must not appear as successful output. Open the corresponding [API validation test](../../backend/tests/test_api.py) and explain the rule. This planned valid/invalid demonstration is part of the slot, not an assessment retry.

For environment/configuration rows, inspect `python --version`, `python -c "import sys, stat_core; print(sys.executable); print(stat_core.__file__)"`, installed package use, [dependency metadata](../../backend/pyproject.toml), ignore rules, and `.env.example`. Confirm local `.env`, credentials, and `.venv` stay out of tracked files/history; never display secrets.

Run `python -m pytest backend/tests` locally; inspect passing output and tests at public processing/API/comparison boundaries. Open the successful **Backend tests** GitHub Actions run and confirm the demonstrated commit identity. Inspect logs, not just a green badge; reporting success does not configure required branch checks.

Follow the [capture/comparison commands](../../docs/comparisons.md#repeated-local-runs): two unchanged-code/input local captures must yield `Outputs agree` and exit 0. Inspect the real Docker capture and its successful local comparison, commands/logs and environments. Compare capture SHA-256 code/input hashes as well as the demonstrated Git SHA; a Git SHA alone does not establish unchanged CSV bytes or a clean checkout. Rebuild images after preparation edits, before capturing evidence.

Open the underlying JSON and [comparison tests](../../backend/tests/test_comparison.py). Records, identifiers, raw values, copied baselines, counts, types, structure/order and nulls compare exactly. Only derived `change`, `percent_change`, and visit-summary `mean` use `abs(actual - expected) <= max(1e-9, 1e-9 * abs(expected))`, with the first output as reference. Do not drop fields, round differences away, or widen tolerance to pass.

Repeatability is agreement under the same conditions; replicability is agreement under slightly different conditions (local venv versus Docker). Reproducibility under very different conditions is conceptual here; independent simulations, cross-group reproduction and new-data experiments are not required.

For collaboration, open feature branches, descriptive commits, PRs, substantive teammate reviews and responses/follow-up. Each member must explain their own contribution, authored PR, review reasoning and follow-up. Approval alone or “looks good” fails the meaningful-review requirement; template history and instructor/agent work do not count.

## Likely questions, failures, and bounded recovery

Use these diagnostic prompts during rehearsal and, if time permits, inside the current slot. They do not grant extra time, a later retry, reassessment, or an exception to missing-evidence failures.

| Question / failure | Response or diagnostic action |
| --- | --- |
| Docker absent, daemon stopped, build fails | Check engine/Compose and build logs in preparation. During assessment inspect what actually runs; configuration or saved instructor logs cannot replace required live startup. |
| Port busy, backend unhealthy, frontend cannot connect | Stop standalone servers using the ports before presenting. Inspect `docker compose ps`, logs and health; verify `http://backend:8000` inside Compose and host browser port 8501. Follow the existing Compose guide within the slot. |
| Wrong input, 422, or 413 | Read file/row/field; check chosen files, declared rule and per-file upload limit. Use original files in rehearsal; explain the planned invalid case. Never weaken validation to hide a failure. |
| Null versus zero; unexpected counts | Open the record and declared behavior: missing is unavailable, zero is observed. Check input identity and join/denominator rules against tests. Statistical conclusions are not graded. |
| Local pass but CI pending/failing or wrong SHA | Inspect run identity and setup/test logs. A local pass cannot substitute for successful hosted checks; record unverified evidence as missing at the presentation. |
| Hash or comparison mismatch | Inspect diagnostic field, captures, code/input hashes and environment differences. Correct conditions and recapture in preparation; never edit evidence or tolerance to manufacture agreement. |
| “Do charts or CI prove replicability?” | Open real local/Docker outputs and successful comparison logs. Charts and pytest alone do not establish that comparison. |
| Missing PR/review, inaccessible repo, silent member | Check roster links and access before class. During the slot inspect actual authorship/review substance and hear each member; record unmet rows, without inventing participation. |
| “Can we submit later or gain credit for a complex model?” | No. All evidence is assessed at the final presentation only; every mandatory group and individual requirement must pass. No separate submission, resubmission, reassessment, later retry, weighted scores or complexity bonuses. |

At each presentation, record Pass/Fail, URL/path and a short observation for every checklist row and each student. Missing evidence fails that requirement. Pass requires all mandatory requirements; statistical correctness, scientific conclusions, model complexity and UI polish are not graded. Tests still must establish declared processing behavior. Record failed rows and reasons at the presentation; closing introduces no additional assessment opportunity.

## Concise instructor rehearsal checklist

- Confirm access, actual `G`, three/four-person roster, exact timetable, break boundary, timer and individual speaking plan.
- Time startup → readiness → upload → API/package trace → results → planned invalid rejection; verify original data and stop port conflicts.
- Open interpreter/package/configuration evidence, passing local tests and matching successful hosted run by SHA; retain accessible artifacts.
- Navigate both comparisons, hashes, exact/null fields and derived-only tolerances without changing code/data; inspect real Docker logs.
- Open every student's authored PR, teammate review and follow-up; rehearse evidence questions and recording all mandatory rows.
- Rehearse five-minute closing and finality wording; check slide titles, links and command references against the brief.

Authoring evidence: [testing guide](../../docs/testing.md#actual-verification) records issue #5's earlier local 175-pass run; [comparison PR #58](https://github.com/drweihungpan-lab/3R-teaching/pull/58) at `c5fc92a` has [remote run 38876609585](https://github.com/drweihungpan-lab/3R-teaching/actions/runs/38876609585), recorded in coordination verification as successful backend tests and real Docker comparisons. These are historical implementation evidence, not this document's checks, current student evidence, or classroom delivery. This document receives content/link/command/timing checks only; backend tests are not rerun. Docker and LibreOffice are unavailable locally; no local container execution, rendered deck inspection, student participation or classroom rehearsal is claimed.
