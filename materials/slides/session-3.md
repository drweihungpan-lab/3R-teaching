# Session 3: Validation, pytest, and automated CI

- Follow a CSV request through FastAPI into reusable processing.
- Explain accepted inputs, missing values, and useful errors.
- Read tests, diagnose a failure, and inspect automated checks.
- Use the supplied synthetic example; no model building is needed.

---

## Our 180-minute agenda

- 0–45: explanation — contracts, validation, fixtures, comparisons.
- 45–75: demonstration — requests, failure, correction, local and CI checks.
- 75–90: break — 15 minutes.
- 90–180: guided practice — trace 15, inspect 20, change 20, check 20, review 15.
- Timings are provisional; see the [syllabus](../../SYLLABUS.md).

---

## Follow the request across public boundaries

An API is a defined way for programs to exchange inputs and results.

```text
POST /process: two CSV file uploads
  backend/app/main.py: read uploads, decode UTF-8
  stat_core.process_csv: validate, join, summarize
  ProcessResult: check the result shape
  HTTP 200: return JSON
```

- `process_csv` accepts CSV contents, not paths or HTTP objects.
- Trace the [API](../../backend/app/main.py) and [public processing entry point](../../backend/stat_core/__init__.py).

---

## A contract tells callers what to expect

- Multipart means named file parts: `participants` and `laboratory`.
- FastAPI checks the upload fields; CSV validation checks their contents.
- Pydantic models describe and check result and error shapes.
- `ProcessResult` contains `counts`, `records`, `arm_summaries`, `visit_summaries`.
- `value: float | None` allows a number or unavailable value; JSON uses `null`.
- Read the [contract](../../docs/api.md); inspect `/docs` and `/openapi.json`.

---

## Validate meaning as well as type

- DM: participants. LB: laboratory observations.
- Join on `STUDYID` and `USUBJID`; preserve text `SUBJID` such as `001`.
- DM key: `(STUDYID, USUBJID)`; LB adds `LBSEQ` or `VISIT` for uniqueness.
- `AGE` must be a nonnegative integer in years.
- `LBORRES` and `LBSTRESN` must agree: finite, nonnegative numbers.
- Both result units: exactly `nmol/L`; no conversion.
- [Input rules](../../docs/api.md#input-rules-and-errors) also cover visits, dates, test names, and required columns.

---

## Missing values carry information

- Missing: both result cells empty, `LBSTAT=NOT DONE`, `LBREASND` nonempty.
- Observed: numeric results, empty status and reason; zero is observed.
- Output missing `value`, `change`, `percent_change` remain `null`.
- Means use observed values only; an all-missing group has `mean=null`.
- Unavailable baseline: null changes. Zero baseline: null percentage change.
- Omitted visits add no rows to the missing count.

---

## HTTP status and error location guide repair

- HTTP 200: processing succeeded; inspect the returned result.
- HTTP 422: invalid CSV, invalid UTF-8, or missing upload fields.
- HTTP 413: one upload exceeds `MAX_UPLOAD_BYTES`; default 5,242,880 bytes per file.
- Errors use `detail`, containing `file`, `row`, `field`, `message`.
- CSV header is line 1; file-level errors use `row=null`.
- CSV validation reports the first detected error; fix it and retry.
- Python callers receive `InvalidInputError.issues`; HTTP callers receive JSON.

---

## Test behavior callers can observe

A test compares a public result with a declared expectation.

- [Processing tests](../../backend/tests/test_processing.py): records, summaries, and missingness via `process_csv`.
- [Validation tests](../../backend/tests/test_validation.py): rejected inputs and error issues.
- [API tests](../../backend/tests/test_api.py): multipart requests, status codes, and response schemas.
- TestClient sends requests inside Python; no server is needed.
- Expect results independently of production helpers or internal call order.

---

## Fixtures provide reusable inputs

A pytest fixture provides named inputs or resources to a test.

- Read [conftest.py](../../backend/tests/conftest.py); pytest discovers it automatically.
- `supplied_csv`: unchanged synthetic DM and LB contents.
- `tiny_rows`: fresh DM and LB dictionaries so tests do not affect each other.
- `csv_text` turns those rows into CSV; `tiny_csv` supplies both CSV strings.
- `client` supplies TestClient; `uploads` names the two multipart files.

---

## Work out the expected answer independently

- Tiny inputs: Active participants have values 10 → 5 and 20 → 15 nmol/L.
- Baseline mean: 15; DAY 15 mean: 10 nmol/L.
- Changes: −5 nmol/L each; percentage changes: −50 and −25.
- A third participant has no LB rows but still counts in DM.
- Expected totals: 3 participants, 4 records, 4 observed, 0 missing.
- These worked literals let tests detect a wrong calculation.
- Engineering checks do not establish a clinical conclusion.

---

## Declare exact and approximate agreement

- Exact: identifiers, dates, order, units, counts, raw values, copied baselines, and nulls.
- Approximate: only calculated means, changes, and percentages.

```python
assert actual == pytest.approx(expected, rel=1e-9, abs=1e-9)
```

- Allowed difference: the larger of `1e-9 * abs(expected)` and `1e-9`.
- Absolute units: nmol/L for means/changes; percentage points for percentages.
- Relative tolerance has no unit. Preserve full precision.
- This is an engineering rule, not a clinical threshold.

---

## Connect checks to the course's three Rs

- Repeatability: agreement across runs under the same conditions.
- Repeated local runs also compare decimals exactly.
- Replicability: agreement under slightly different conditions, such as local versus Docker.
- Passing CI alone does not compare local and Docker outputs.
- Reproducibility: agreement under very different conditions, such as independent simulation; conceptual here.
- Session 4 compares outputs; read the [glossary](../../GLOSSARY.md) and [comparison rules](../../docs/testing.md#exact-and-approximate-comparisons).

---

## Demo: start from the working backend

Use Python 3.12 and the activated backend development environment from [setup](../../docs/setup.md). Run commands from the repository root.

```bash
python -m uvicorn app.main:app --app-dir backend \
  --host 127.0.0.1 --port 8000
```

- Keep this terminal running; use a second terminal for requests and tests.
- Open `http://127.0.0.1:8000/docs` to inspect schemas and try uploads.
- `GET /health` checks service availability, not data validity.

---

## Demo: send a valid multipart request

```bash
curl --fail-with-body http://127.0.0.1:8000/process \
  -F participants=@data/synthetic/dm.csv \
  -F laboratory=@data/synthetic/lb.csv
```

- HTTP 200: 24 participants, 96 records, 95 observed, 1 missing.
- Inspect `records`, `arm_summaries`, and `visit_summaries` as well as counts.
- Find `EDU-LPA-007` at DAY 30: null value, `NOT DONE`, `SPECIMEN NOT AVAILABLE`.
- Follow the request in [main.py](../../backend/app/main.py) into `process_csv`.

---

## Demo: reject an invalid age

Copy DM, then edit the first data row's `AGE` to `forty` in the copy.

```bash
cp data/synthetic/dm.csv /tmp/session-3-dm-invalid.csv
```

- In `/docs`: `POST /process` → Try it out.
- Upload the copy as `participants`; `data/synthetic/lb.csv` as `laboratory`.
- Execute: HTTP 422, `detail[0]`: `participants`, row 2, `AGE`.
- Message: `Expected a nonnegative integer.` Restore the age; retry for HTTP 200.
- Follow the [contract](../../docs/api.md); keep supplied data unchanged.

---

## Demo: run tests and read one public behavior

```bash
python -m pytest backend/tests
```

From [test_processing.py](../../backend/tests/test_processing.py), using the `tiny_csv` fixture:

```python
def test_worked_summaries_include_dm_participants_without_lab_rows(tiny_csv):
    result = process_csv(*tiny_csv)
```

- `*tiny_csv` passes the two CSV strings separately to `process_csv`.
- Read the literal counts and mean expectations in this test.
- Pytest discovers `test_` functions; a failed assertion identifies the mismatch.

---

## Demo: introduce one controlled failure

In a disposable teaching branch or copy, edit only this test's expected baseline mean: `[15.0, 10.0]` → `[16.0, 10.0]`.

```bash
python -m pytest \
  backend/tests/test_processing.py::test_worked_summaries_include_dm_participants_without_lab_rows \
  -q
```

- `::` selects this exact test; `-q` reduces routine output.
- Expect `1 failed`, `Obtained: 15.0`, `Expected: 16.0 ± 1.6e-08`.
- The input baseline values 10 and 20 support 15; the edited expectation is wrong.

---

## Demo: correct the expectation and check again

Restore `[15.0, 10.0]`, then repeat the exact command on the previous slide: expect `1 passed`.

```bash
python -m pytest backend/tests
git diff -- backend/tests/test_processing.py
```

- Confirm the full suite passes and the temporary edit is gone.
- Correct the expectation, rather than changing processing or tolerance.
- Keep the distributed example passing; see [failure and recovery](../../docs/testing.md#controlled-failure-and-recovery).

---

## Demo: inspect the same checks on GitHub

- PR Checks → Backend tests → Run backend tests.
- Actions → Backend CI: check branch and commit ID (SHA).
- Ubuntu/Python 3.12: install `./backend[dev]`, run `python -m pytest backend/tests`.
- Disposable teaching PR: push the wrong expectation, inspect failure, push correction.
- Verify the corrected commit succeeds; rerunning the old commit tests old code.
- Read the failed step: setup/install or pytest. [CI guide](../../docs/ci.md#inspect-a-failure-and-its-correction).

---

## Reporting a check is different from requiring it

- [Backend CI](../../.github/workflows/backend-tests.yml) runs for every PR, including documentation.
- Pushes to `main` and the authoring integration branch also trigger it.
- A workflow reports results; it does not itself block merging.
- An administrator must require PRs and `Backend tests` in a branch rule.
- Student workflow: feature branch → PR into `main` → peer review → checked merge.
- A dependency cache saves downloads; it does not lock package versions.

---

## Break, then 90 minutes of guided practice

- Take a 15-minute break before practice.
- 15 minutes: trace a request and its four result fields.
- 20 minutes: inspect missingness, units, keys, and fixtures.
- 20 minutes: use a disposable copy for the 15 → 16 → 15 failure and correction.
- 20 minutes: one small test or validation change on a feature branch; check behavior and the full suite.
- 15 minutes: inspect the corrected PR check; review a teammate's behavior, tests, or clarity.

---

## Checkpoint and next step

- Explain an accepted input, rejection, and missing value.
- Show local tests and the corrected commit's PR check.
- Explain why raw values compare exactly and calculated values use tolerance.
- Mandatory homework: about two hours on tests for your group's declared behavior and invalid inputs, plus peer review.
- Keep evidence for the final presentation. This checkpoint is preparation, not a separate assessed submission.
- Next: interface, containers, and local/Docker output comparison.
