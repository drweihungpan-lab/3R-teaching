# Session 3 guided practice: requests, validation, tests, and CI

Work for about 90 minutes in your group of three or four. Follow the complete synthetic healthcare example, diagnose one deliberately wrong test expectation, and review its correction through a pull request (PR). This checkpoint prepares evidence for Session 5; it is not a separate assessed submission. Rotate roles: every student must eventually author a PR and meaningfully review a teammate's PR.

## 1. Prepare the group feature branch — 10 minutes

Have Python 3.12, Git, an editor, a browser, and access to your group's repository from Sessions 1–2. Run all commands from the repository root containing `backend/`, `data/`, and `docs/`. Follow [docs/setup.md](../../docs/setup.md) if `.venv` does not exist; activate it with `source .venv/bin/activate` on macOS/Linux or `.venv\Scripts\Activate.ps1` in Windows PowerShell. Use that interpreter in both terminals below.

```bash
git rev-parse --show-toplevel
git status --short
python --version
python -m pip install -e './backend[dev]'
```

Expect Python 3.12.x. Save unrelated work without discarding it, start from the group's current agreed `main`, and replace `your-name` with a unique name:

```bash
git switch -c session-3/your-name-test-evidence
```

Keep the original [dm.csv](../../data/synthetic/dm.csv) and [lb.csv](../../data/synthetic/lb.csv) unchanged. These are invented teaching data, not clinical findings; consult the [data dictionary](../../data/synthetic/data-dictionary.md). Installation needs internet access. Docker is not needed for this activity.

## 2. Send and trace a valid request — 20 minutes

Start the API in the first terminal using the [setup command](../../docs/setup.md#run-and-check-the-api):

```bash
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Keep it running. In a second terminal at the same root, send the supplied files:

```bash
curl --fail-with-body http://127.0.0.1:8000/health
curl --fail-with-body http://127.0.0.1:8000/process \
  -F participants=@data/synthetic/dm.csv \
  -F laboratory=@data/synthetic/lb.csv
```

In PowerShell use `curl.exe` and put the entire request on one line, removing the trailing backslashes. Alternatively open <http://127.0.0.1:8000/docs>, expand `POST /process`, choose **Try it out**, select the two files under `participants` and `laboratory`, and **Execute**. The request is multipart: two named file uploads, not a JSON object containing filenames.

Expect health HTTP 200 with `{"status":"ok"}` and processing HTTP 200 with `counts` equal to `{"participants":24,"records":96,"observed":95,"missing":1}`. Inspect `records`, `arm_summaries`, and `visit_summaries` too. Subject `001` retains its leading zeros. `EDU-LPA-007` at DAY 30 has null value/change/percent_change, baseline 269.0, and status `NOT DONE`. Null means unavailable, not zero.

Follow these exact source paths with a teammate:

| Path | What to explain |
| --- | --- |
| [backend/app/main.py](../../backend/app/main.py) | `POST /process` receives `participants` and `laboratory`, reads/decode-checks uploads, then calls `process_csv`. HTTP handling belongs here. |
| [backend/stat_core/__init__.py](../../backend/stat_core/__init__.py) and [processing.py](../../backend/stat_core/processing.py) | The public import exposes `process_csv`; it takes CSV text, validates, joins on study/participant, calculates changes, and returns summaries. |
| [validation.py](../../backend/stat_core/validation.py) and [schemas.py](../../backend/stat_core/schemas.py) | CSV rules reject invalid cells; `ProcessResult` describes the successful response, and `ErrorResponse` describes errors. Pydantic schemas specify fields/types; CSV rules enforce the data contract. |

Checkpoint: explain the boundary between HTTP uploads and reusable processing without HTTP. Use [docs/api.md](../../docs/api.md) as the response reference; a healthy service alone does not prove processing is correct.

## 3. Locate an invalid AGE — 15 minutes

Create a copy with only the first participant's AGE changed. This multiline Python command works from the root in a shell supporting the shown quoting; if needed, use the editor to copy DM to the same ignored output path and change AGE in CSV line 2.

```bash
python -c '
import csv
from pathlib import Path
with Path("data/synthetic/dm.csv").open(newline="", encoding="utf-8") as source:
    rows = list(csv.reader(source))
rows[1][rows[0].index("AGE")] = "not-a-number"
Path("outputs").mkdir(exist_ok=True)
with Path("outputs/session-3-invalid-dm.csv").open("w", newline="", encoding="utf-8") as target:
    csv.writer(target).writerows(rows)
'
curl --fail-with-body http://127.0.0.1:8000/process \
  -F participants=@outputs/session-3-invalid-dm.csv \
  -F laboratory=@data/synthetic/lb.csv
```

Expect HTTP 422 (curl exits 22 while retaining the response body):

```json
{"detail":[{"file":"participants","row":2,"field":"AGE","message":"Expected a nonnegative integer."}]}
```

The header is CSV line 1, so row 2 is the first participant. Find the AGE integer check in `validate_participants`, then follow `InvalidInputError` back to the API exception handler. Validation stops at the first error. Upload the original DM again: expect HTTP 200 and 24/96/95/1. Do not weaken validation or overwrite the original input to recover.

## 4. Read tests and create a controlled failure — 20 minutes

Open [conftest.py](../../backend/tests/conftest.py), [test_processing.py](../../backend/tests/test_processing.py), and [test_api.py](../../backend/tests/test_api.py). A fixture supplies reusable example inputs. The tiny example has baseline values 10 and 20 (mean 15), follow-up values 5 and 15 (mean 10), and a third DM participant without lab rows who still counts in arm participants. API tests send multipart requests using `TestClient` without starting a server. These tests observe public processing/API behavior, not private helper calls.

Run the focused test from [docs/testing.md](../../docs/testing.md#controlled-failure-and-recovery) before editing:

```bash
python -m pytest backend/tests/test_processing.py::test_worked_summaries_include_dm_participants_without_lab_rows -q
```

Expect `1 passed`. Inside that test only, change the baseline mean literal in `[15.0, 10.0]` to `[16.0, 10.0]`. Rerun the same command: expect `1 failed`, `Obtained: 15.0`, and `Expected: 16.0 ± 1.6e-08`. Save this output. The deliberately incorrect expectation fails; the calculation remains correct.

Calculated means/changes/percentages use `pytest.approx(..., rel=1e-9, abs=1e-9)`; counts, identifiers, raw values, and nulls compare exactly. The wrong mean exceeds the tolerance. Explain why widening it or calculating expectations with production helpers would conceal errors. These checks establish engineering behavior, not clinical validity or local/Docker replicability under the [course glossary](../../GLOSSARY.md).

## 5. Inspect PR checks, recover, and review — 25 minutes

In your **group repository only**, commit the temporary wrong expectation on this disposable feature branch:

```bash
git diff --check
git diff -- backend/tests/test_processing.py
git add backend/tests/test_processing.py
git commit -m "Demonstrate controlled summary expectation failure"
git push -u origin HEAD
```

Open a **draft PR to the group's `main`** explaining the deliberate failure; keep it unmerged. In **Checks → Backend tests → Run backend tests**, verify the branch/commit and read the failed assertion. [docs/ci.md](../../docs/ci.md) describes the same workflow: Python 3.12, `python -m pip install -e './backend[dev]'`, then `python -m pytest backend/tests`. A setup/install failure is different from an assertion failure. Preserve the failed run URL.

Restore `[15.0, 10.0]` in the editor. Add a short comment beside the expectation explaining that the baseline mean uses the two observed values, while DM arm participants also include someone without laboratory rows. This leaves a small, useful clarification in the final PR diff. Rerun the focused command (expect `1 passed`), then:

```bash
python -m pytest backend/tests
git diff --check
git add backend/tests/test_processing.py
git commit -m "Restore correct mean and explain the worked denominator"
git push
```

Expect **all tests passing** (205 in the completed supplied framework), with the existing Starlette TestClient deprecation warning in the authoring environment. Inspect the **new commit's** successful **Backend tests** check; rerunning the old commit does not test the correction. CI reports results; a separate required-check rule controls whether failure prevents merging. Do not merge the failing version.

Ask a teammate to inspect the final diff and rerun the focused test. They should leave a concrete review explaining the independently worked mean, the DM denominator, or why the tolerance catches the wrong expectation; approval alone is insufficient. Address useful feedback and rerun affected checks. Put valid/invalid HTTP observations, local fail/pass output, both hosted run links/SHAs, and review evidence in the PR description. Keep `.venv`, `.env`, outputs, and unrelated edits out of commits.

Stop when you can trace the request, show 24/96/95/1 and the AGE error location, explain the failed/corrected assertion, and point to passing local/remote checks plus meaningful review evidence. Stop the local API with Ctrl+C. Keep the PR open if review or CI remains unresolved, recording what remains. There is no separate submission, resubmission, or reassessment; homework, decks, and the instructor run sheet are separate tasks.

## Instructor reference and recovery

If imports fail, check the repository root, active Python, and editable installation against [setup](../../docs/setup.md). If port 8000 is busy, select another `--port` and update every request URL. Connection refusal means the service is not listening; a 422 with file/row/field is a processed validation failure. Check `.env` limits if uploads return 413. Use `/docs` if curl is unavailable.

For unexpected counts or errors, inspect input paths and the diff against [the API contract](../../docs/api.md); select original CSVs again. For unexpected test results, confirm the exact test name and only the baseline literal changed. Manually restore 15.0 and rerun focused/full checks, preserving unrelated work; do not reset the repository. The reference answer is mean 15, not 16, and three DM participants versus four lab rows. Never adjust processing or tolerance to hide the deliberate failure.

If GitHub access, a teammate, or runner capacity is unavailable, retain the local commit and evidence and record the outstanding remote/review step; do not claim it passed. Check the PR head SHA and earlier CI installation logs before diagnosing a hosted failure. A green check alone does not prove peer review or required-check protection.

Author verification: local HTTP health/valid/invalid/recovered requests, focused pass/fail/pass in a disposable copy, and the full 175-test suite were exercised with Python 3.12 using `PYTHONPATH=backend` and the shared environment without reinstalling it. File links and commands were checked against the references above. This authoring PR's hosted check is separate evidence from the student PR exercise: student GitHub permissions, deliberately failed/corrected student hosted runs, and peer participation have not been rehearsed. Windows/PowerShell and browser upload interactions were not executed. Docker is unavailable; no container agreement is claimed.
