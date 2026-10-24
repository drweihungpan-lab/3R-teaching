# Session 3 instructor notes: validation, pytest, and automated CI

Teach students to trace a request, explain missingness and rejection, read a test failure, and connect the correction to its PR check. Use the complete synthetic example. Follow the [syllabus](../../SYLLABUS.md#session-3-defensive-engineeringfastapi-pytest-and-automated-ci).

Open with the slide “Back at the bubble tea shop” (about 2 minutes, taken from the first block). Ask students one at a time, at random, and leave the question open: do not explain it or connect it to today's topic. The questions continue the Session 1 bubble tea example; reword them before class if you like.

## Prepare before class

Have Python 3.12 with backend development dependencies, Git, an editor, two terminals, a browser, curl (or `/docs`), and GitHub access to a disposable teaching PR and each group's repository. Follow [setup](../../docs/setup.md) before class; check Python, imports, repository root, permissions, and a recent passing **Backend tests** check. Students work in groups of three or four and rotate driving/review roles. Docker is not needed today.

Keep [dm.csv](../../data/synthetic/dm.csv) and [lb.csv](../../data/synthetic/lb.csv) unchanged; read their [provenance](../../data/synthetic/README.md) and [dictionary](../../data/synthetic/data-dictionary.md). Prepare an ignored copy at `outputs/session-3-invalid-dm.csv` with only the first data row's `AGE` changed to `not-a-number`, following [exercise §3](../exercises/session-3.md#3-locate-an-invalid-age--15-minutes). Keep original DM ready for recovery. Do not commit generated outputs or local settings.

Open the [slide source](../slides/session-3.md), [exercise](../exercises/session-3.md), [API contract](../../docs/api.md), [testing guide](../../docs/testing.md), and [CI guide](../../docs/ci.md). Bookmark the exact test below and prepare a disposable teaching branch/PR for the wrong expectation and correction. Capture the failed and corrected run URLs and commit SHAs during rehearsal; hosted runners may take longer than the live slot. Label saved evidence as rehearsal evidence when using it in class.

## Provisional 180-minute run sheet

Slide titles below are the actual headings in the slide source. The exercise's five sections total 90 minutes; use their timings for practice. The slide agenda's trace/inspect/change/check/review split describes teaching themes rather than a second activity schedule.

| Minutes | Mode | Actual slide titles / activity | Instructor action and observation |
| --- | --- | --- | --- |
| 0–10 | Device example | “Device example, Stage 5: tests and CI” | Demonstrate Stage 5 with the [device example steps](#device-example-stage-5-about-10-minutes) below. Name the tool the stage shows; the session teaches it. |
| 10–18 | Explain | “Follow the request across public boundaries”; “A contract tells callers what to expect” | Trace uploads → API → `process_csv` → `ProcessResult` → JSON. Ask which layer knows HTTP and which accepts CSV text. |
| 18–28 | Explain | “Validate meaning as well as type”; “Missing values carry information”; “HTTP status and error location guide repair” | Work through keys, units, AGE, null versus zero, and file/row/field errors against the API contract. |
| 28–40 | Explain | “Test behavior callers can observe”; “Fixtures provide reusable inputs”; “Work out the expected answer independently”; “Declare exact and approximate agreement” | Read the tiny fixture and calculate mean 15 independently. Distinguish public behavior from internal calls. |
| 40–45 | Explain | “Connect checks to the course's three Rs”; “Reporting a check is different from requiring it” | Ask what CI proves and what requires a separate comparison or branch rule. |
| 45–55 | Demo | “Demo: start from the working backend”; “Demo: send a valid multipart request”; “Demo: reject an invalid age” | Show health, valid counts, missing record, AGE rejection, and original-file recovery. |
| 55–65 | Demo | “Demo: run tests and read one public behavior”; “Demo: introduce one controlled failure”; “Demo: correct the expectation and check again” | Execute focused pass → fail → pass; explain obtained versus expected; run full suite after correction. |
| 65–75 | Demo | “Demo: inspect the same checks on GitHub” | Inspect failed and corrected PR checks by SHA; use labeled rehearsal runs if queues are slow. |
| 75–90 | Break | “Break, then 90 minutes of guided practice” | Keep reference tabs available; return at minute 90. |
| 90–100 | Practice | Exercise §1 “Prepare the group feature branch” | Check root, interpreter, clean scope, and unique feature branch; avoid spending practice on preventable setup. |
| 100–120 | Practice | Exercise §2 “Send and trace a valid request” | Pairs explain all four result fields and point to the HTTP/processing boundary. |
| 120–135 | Practice | Exercise §3 “Locate an invalid AGE” | Locate row 2/AGE in the response and recover using original DM. |
| 135–155 | Practice | Exercise §4 “Read tests and create a controlled failure” | Read fixtures, run the focused test, change 15 to 16, and save the assertion failure. |
| 155–180 | Practice | Exercise §5 “Inspect PR checks, recover, and review”; “Checkpoint and next step” | Inspect failed check, restore 15, add the useful explanatory comment, run focused/full checks, push, and review the corrected SHA. Reserve the last few minutes for evidence gaps and homework reminder. |

Totals: device example 10 + explanation 35 + demonstration 30 + break 15 + practice 90 = 180 minutes. If hosted checks lag, continue local interpretation and peer review; record the outstanding remote result.

## Device example: Stage 5 (about 10 minutes)

The slide follows “Back at the bubble tea shop”. This is a demonstration; students do not run it. Prepare a clone of the [device example](https://github.com/drweihungpan-lab/3R-device-example) and its pull request from `demo/cleanup-drops-zero-days` into `main` before class (open it as a **draft**, never merge it), plus a Python 3.12 environment:

```bash
python3.12 -m venv .venv312
.venv312/bin/python -m pip install -e 'stage-5-tests-ci/backend[dev]'
```

**Steps ([folder](https://github.com/drweihungpan-lab/3R-device-example/tree/main/stage-5-tests-ci), about 10 minutes).**

1. Remind students of Stage 4: the cleanup moved the dates and nothing noticed.
2. On `main`, run `python -m pytest stage-5-tests-ci/backend`: `6 passed`. Show the Actions tab: `main` is green.
3. Open `backend/tests/test_model.py` and read the pinned `EXPECTED_LIMIT_DATES` (2026-06-30, 2026-04-01, 2026-01-16).
4. Open the prepared pull request: CI is **red**, with `test_limit_dates_are_pinned_for_the_fixed_synthetic_data` failing (3 failed, 3 passed). The diff is the same cleanup as Stage 4. Explain that the test, not a person, caught it. Use a rehearsal run if hosted checks are slow, and label it as one.
5. Show that Stage 5 runs from any folder (`python -m device_limit` from a different directory prints the same dates).

Name what this session teaches: pytest and CI. If time runs short, show the README's expected output instead of running everything.

## Demo cue card and expected observations

From the repository root with the prepared environment active, start the API in terminal 1:

```bash
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

In terminal 2:

```bash
curl --fail-with-body http://127.0.0.1:8000/health
curl --fail-with-body http://127.0.0.1:8000/process \
  -F participants=@data/synthetic/dm.csv \
  -F laboratory=@data/synthetic/lb.csv
curl --fail-with-body http://127.0.0.1:8000/process \
  -F participants=@outputs/session-3-invalid-dm.csv \
  -F laboratory=@data/synthetic/lb.csv
```

Health: HTTP 200, `{"status":"ok"}`. Valid processing: HTTP 200, `counts={"participants":24,"records":96,"observed":95,"missing":1}`, plus `records`, `arm_summaries`, and `visit_summaries`. Subject `001` remains text. `EDU-LPA-007` at DAY 30 has null value/change/percent_change, baseline 269.0, `NOT DONE`, and `SPECIMEN NOT AVAILABLE`. Missing means unavailable; it contributes no observed value to a mean.

Invalid AGE: HTTP 422, `detail[0]` has `file="participants"`, `row=2`, `field="AGE"`, `message="Expected a nonnegative integer."`. Curl exits 22 and retains the body. The header is line 1. Validation reports the first detected error; fix and retry. Re-upload original DM with original LB: HTTP 200 and 24/96/95/1 again. Trace [main.py](../../backend/app/main.py) → public [stat_core](../../backend/stat_core/__init__.py), then [validation](../../backend/stat_core/validation.py) and [schemas](../../backend/stat_core/schemas.py).

For the controlled test, open [test_processing.py](../../backend/tests/test_processing.py) and its [fixtures](../../backend/tests/conftest.py). On the disposable teaching branch, run:

```bash
python -m pytest backend/tests/test_processing.py::test_worked_summaries_include_dm_participants_without_lab_rows -q
```

Expect `1 passed`. In this test only, change `[15.0, 10.0]` → `[16.0, 10.0]`; repeat the command. Expect `1 failed`, `Obtained: 15.0`, `Expected: 16.0 ± 1.6e-08`. Baseline values 10 and 20 independently support mean 15; follow-up values 5 and 15 support mean 10. Three DM participants count even though only two have the four LB rows.

For hosted failure evidence, commit/push the wrong expectation to the disposable draft PR in the teaching/group repository. Keep it unmerged. Open **Checks → Backend tests → Run backend tests**, confirm the PR head SHA, and retain the failure URL/SHA. Restore `[15.0, 10.0]`; students add the explanatory comment specified in exercise §5 so the final diff remains useful. Rerun the focused command (`1 passed`), then:

```bash
python -m pytest backend/tests
git diff --check
git diff -- backend/tests/test_processing.py
```

Expect the full current suite to pass; do not teach a fixed total because comparison work can add tests. Commit/push the correction to the same PR. Verify **Backend tests** succeeds for the **new PR head SHA**, preserving both run links. Rerunning the failed SHA still tests the wrong expectation. CI runs Python 3.12 on Ubuntu, installs `./backend[dev]`, and runs `python -m pytest backend/tests`; inspect setup/install logs before attributing failures to pytest. Never change production calculations or widen tolerance to hide the wrong expectation. Follow [CI failure/recovery](../../docs/ci.md#inspect-a-failure-and-its-correction) and exercise §5 for the student commit commands.

## Questions and recovery prompts

| Likely question or failure | Answer / next action |
| --- | --- |
| “Why validate if we have types?” | Schemas describe fields and types; CSV rules also enforce units, keys, dates, and consistent observation status. An API is the agreement between caller and service. |
| “Why not fill null with zero?” | Zero is an observed value. Missing requires empty result cells, `NOT DONE`, and a reason. Filling it changes means. Missing baseline gives null changes; zero baseline permits absolute change but gives null percentage change. Omitted visits create no extra rows. |
| “Which comparisons are exact?” | Identifiers, raw values, copied baselines, dates, order, units, counts, and nulls. Only calculated means, changes, percentages use `pytest.approx(expected, rel=1e-9, abs=1e-9)`: larger of relative allowance and absolute allowance. Absolute units are nmol/L or percentage points; relative tolerance is unitless. Preserve precision. Identical local reruns also compare decimals exactly. |
| “Do these tests prove the three Rs?” | Use the [course glossary](../../GLOSSARY.md): same-condition agreement is repeatability; local/Docker agreement is replicability, practiced in Session 4. CI alone proves neither comparison. Independent simulation is the conceptual reproducibility example. |
| Connection refusal / busy port / import failure | Keep the server terminal running. Check root and active interpreter against setup; use another port and update all URLs if necessary. TestClient tests need no listening server. On Windows the commands run in the WSL Ubuntu terminal; `/docs` is the browser alternative. |
| 422 or 413 | A returned HTTP response means the service was reached. Read `detail` and repair the indicated input. 413 is the configured **per-file** byte limit (`MAX_UPLOAD_BYTES`), not a connection error or combined-file limit. Check local configuration; defaults allow supplied inputs. |
| Unexpected counts or failure does not appear | Confirm original input paths, exact test selector, and the one baseline literal changed. Restore 15 manually while preserving unrelated work; inspect the diff. Do not reset the repository or weaken validation. |
| “Green means merge is protected?” | The workflow reports a result. An administrator separately requires **Backend tests** in branch rules; review requirements and bypass permissions are separate. Check the current head SHA. |
| No GitHub access, reviewer, or available runner | Keep local evidence and commits; record remote/review work as outstanding. Use labeled rehearsal logs to explain the flow. Do not claim unseen checks or participation passed. |

Ask reviewers for a concrete comment about the independently worked mean, the DM denominator, test behavior, or clarity; approval alone is insufficient. Every student must author a PR and meaningfully review a teammate's PR across the course. Keep valid/invalid HTTP observations, local failure/correction output, hosted run URLs/SHAs, and review evidence accessible in the group PR.

The checkpoint is preparation. Remind students of approximately two hours of mandatory homework on declared processing behavior, invalid-input tests, CI, and peer review. Assessment is pass/fail at the final presentation only, with all engineering requirements met; no weighted scores, separate submission, resubmission, or reassessment, including a later retry during that session. Statistical correctness and model complexity are not graded; engineering tests must check the declared behavior.

## Concise rehearsal checklist

- Verify Python/root/imports, untouched source CSVs, disposable branch, GitHub permissions, and prepared browser tabs.
- Time health → valid → invalid AGE → recovered requests; locate counts, nulls, and error fields aloud.
- Rehearse focused 15 → 16 → 15 and full passing suite; preserve output and confirm only intended teaching changes remain.
- Verify failed and corrected hosted run links against their SHAs; keep labeled fallback evidence and check the corrected PR head.
- Rehearse one meaningful review comment; reserve practice time for review and identifying evidence gaps.
- Check links and timing, stop the API with Ctrl+C, and leave the failing PR version unmerged.

See [verification](../../docs/verification.md) for recorded checks and the remaining limits to rehearse on the delivery machine.
