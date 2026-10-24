# Session 2 guided practice: follow and change a Python package

Spend about 90 minutes in your group of three or four. You will follow the supplied synthetic healthcare example, run its installed package, and make one small logging change through a pull request (PR). A module is a Python file; a package groups related modules so other code can import them. All processing functions are already complete.

This classroom checkpoint prepares evidence for the final presentation. It is not a separate assessed submission. Every student must eventually author at least one PR and meaningfully review a teammate's PR; rotate author and reviewer roles during the course.

## Before you start

Have Python 3.12, Git, an editor, internet access for installation, and access to your group's GitHub repository from Session 1. Use the supplied working example in that repository. The two input files are invented teaching data, not clinical findings: [data provenance](../../data/synthetic/README.md) and [data dictionary](../../data/synthetic/data-dictionary.md). Keep the original CSVs unchanged.

All terminal commands below run from the **repository root**, the directory containing `backend/`, `data/`, and `docs/`. This is not `backend/` or `materials/exercises/`. In a terminal opened at your clone, check:

```bash
git rev-parse --show-toplevel
git status --short
```

Move to the root path printed by Git if necessary. Finish or save unrelated work before creating the exercise branch; do not discard it. The complete installation and activation reference is [docs/setup.md](../../docs/setup.md).

| Time | Activity | Checkpoint |
| --- | --- | --- |
| 0–15 min | Activate environment and install | Import resolves to this clone |
| 15–35 min | Trace modules and type hints | Explain data flow to a teammate |
| 35–50 min | Run the unchanged example | Counts and missingness match the reference |
| 50–70 min | Change one log message and rerun | Message changes; result stays identical |
| 70–90 min | Open and review a PR | Evidence and a useful peer review are visible |

## 1. Install the editable package — 15 minutes

Reuse your Session 1 `.venv`. If it does not exist, create it from the root:

```bash
python3.12 -m venv .venv
```

On macOS/Linux, activate it:

```bash
source .venv/bin/activate
```

On Windows, run the same commands in the WSL Ubuntu terminal ([Session 0](../../docs/session-0.md#step-2-windows-install-wsl-and-open-ubuntu)). If activation fails, use `.venv/bin/python` wherever the following commands say `python`, or ask the instructor for setup help.

```bash
python --version
python -m pip install -e './backend[dev]'
python -c 'import sys, stat_core; print(sys.executable); print(stat_core.__file__)'
```

Expect Python 3.12.x, an interpreter inside `.venv`, and a module path ending in your clone's `backend/stat_core/__init__.py`. `-e` means editable: imports use the source files in your checkout, so a saved change is available to a new Python process without another installation. A running service must restart to pick it up. Reinstall when dependency metadata changes.

Open [backend/pyproject.toml](../../backend/pyproject.toml). Find the distribution name `three-r-backend`, Python requirement, runtime dependencies, and `dev` extras (`pytest` and `httpx`). The distribution's installation name differs from its import names, `stat_core` and `app`. Dependency ranges describe allowed versions; they do not freeze one exact environment. `python -m pip freeze` shows the installed versions.

## 2. Follow the processing path — 20 minutes

Open the linked files in order and answer these questions with a teammate:

| File | Find and explain |
| --- | --- |
| [stat_core/__init__.py](../../backend/stat_core/__init__.py) | How does `from stat_core import process_csv` expose the reusable function? |
| [stat_core/processing.py](../../backend/stat_core/processing.py) | In `process_csv`, follow reading, validation, joining, baseline/change calculation, summaries, logging, and the returned dictionary. |
| [stat_core/validation.py](../../backend/stat_core/validation.py) | Find required headers and the participant key `(STUDYID, USUBJID)`. Why must both fields match before joining? |
| [stat_core/schemas.py](../../backend/stat_core/schemas.py) | Find `Record.value: float \| None` and `ProcessResult`. Which values may be missing? |
| [app/main.py](../../backend/app/main.py) | Find `POST /process`: it reads uploads and calls the same `process_csv` function. Where does HTTP handling stop and reusable processing begin? |

The function signature is `process_csv(participants_csv: str, laboratory_csv: str) -> dict[str, Any]`. It takes CSV **text**, not filenames. `str` means text, and `dict[str, Any]` describes a dictionary with text keys and values of different types. Type hints help readers and tools; they do not automatically validate CSV contents. The validation functions check inputs at runtime, and Pydantic schemas describe and validate result fields. `float | None` allows a number or an unavailable value. Python `None` becomes JSON `null`, not zero.

Trace one baseline and one later visit in `processing.py`: baseline is taken from the participant's `BASELINE` row; change is current value minus baseline. Missing current value or unavailable baseline leaves changes missing; a zero baseline leaves percentage change missing. Summaries use observed values only. See the worked examples in [docs/api.md](../../docs/api.md).

Find `logger = logging.getLogger(__name__)` and the final `logger.info(...)`. The logger's name identifies its module; its level controls which messages appear. The function reports aggregate counts without logging uploaded rows. The caller configures logging: the API does so at startup, and the next command does so for this standalone run. The processing function itself does not read `.env` or depend on FastAPI.

Checkpoint: explain aloud how the same package can serve a Python script and an HTTP endpoint without duplicating the data processing.

## 3. Capture the unchanged result — 15 minutes

Create your own branch, replacing `your-name` with a unique name:

```bash
git switch -c session-2/your-name-log-context
```

Run this command from the root. The multiline `python -c` form works in macOS shells and the WSL Ubuntu terminal. It saves local evidence in ignored `outputs/`; do not commit those files.

```bash
python -c '
import json
import logging
import sys
from pathlib import Path
from stat_core import process_csv

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
result = process_csv(
    Path("data/synthetic/dm.csv").read_text(encoding="utf-8"),
    Path("data/synthetic/lb.csv").read_text(encoding="utf-8"),
)
print(result["counts"])
missing = next(row for row in result["records"] if row["value"] is None)
fields = ("participant_id", "visit", "value", "baseline", "change", "percent_change", "status", "reason")
print(json.dumps({key: missing[key] for key in fields}))
Path("outputs").mkdir(exist_ok=True)
destination = Path("outputs") / ("session-2-" + sys.argv[1] + ".json")
destination.write_text(json.dumps(result, sort_keys=True, indent=2), encoding="utf-8")
print(destination)
' before
```

Expect these observations (log and printed output may appear in a different order):

```text
INFO stat_core.processing: Processed participants=24 records=96 observed=95 missing=1
{'participants': 24, 'records': 96, 'observed': 95, 'missing': 1}
{"participant_id": "EDU-LPA-007", "visit": "DAY 30", "value": null, "baseline": 269.0, "change": null, "percent_change": null, "status": "NOT DONE", "reason": "SPECIMEN NOT AVAILABLE"}
outputs/session-2-before.json
```

There are 24 participants and four scheduled rows each: 96 records. One scheduled observation is unavailable, leaving 95 observed values. The missing row remains in the output, and its known baseline remains 269.0. Read one observed row too: the first record has subject ID `001`, value/baseline 167.0, and change/percentage change 0.0. Those zeros are actual calculated values, unlike the missing result.

## 4. Add context to the log message — 20 minutes

In `backend/stat_core/processing.py`, change only the final log message's text as shown. Keep `logger.info`, the `%d` placeholders, all four count arguments, and the return value intact:

```diff
-    logger.info("Processed participants=%d records=%d observed=%d missing=%d",
+    logger.info("Processed synthetic healthcare participants=%d records=%d observed=%d missing=%d",
```

This tells a reader what the counts describe without including participant identifiers, measurements, CSV contents, or local configuration. Keep logging at `INFO`, so callers can still control visibility; do not add `basicConfig` inside the reusable function.

Save the file. Rerun the entire command from step 3, changing only its final argument from `before` to `after`. Use a new Python process; the editable installation needs no reinstall. Expect:

```text
INFO stat_core.processing: Processed synthetic healthcare participants=24 records=96 observed=95 missing=1
```

Counts and the missing-row display must stay the same, and the destination is now `outputs/session-2-after.json`. Compare the complete results:

```bash
python -c 'import json; from pathlib import Path; before = json.loads(Path("outputs/session-2-before.json").read_text(encoding="utf-8")); after = json.loads(Path("outputs/session-2-after.json").read_text(encoding="utf-8")); print("Processing result unchanged:", before == after); assert before == after, "Logging-only change altered processing output"'
git diff --check
git diff -- backend/stat_core/processing.py
```

Expect `Processing result unchanged: True`, no whitespace errors, and a one-line message change. Complete equality is appropriate for this logging-only edit in the same environment: no numeric calculation changed. This is a focused regression check, not the later local/Docker comparison activity. Follow the [course glossary](../../GLOSSARY.md) when describing repeatability and replicability; no Docker comparison is claimed here.

Before review, also run the supplied suite from the repository root: `python -m pytest backend/tests`. Follow [testing instructions](../../docs/testing.md) and record the actual result. You are changing working code, not implementing missing functions.

## 5. Record and review the change — 20 minutes

```bash
git status --short
git add backend/stat_core/processing.py
git commit -m "Clarify synthetic healthcare processing log context"
git push -u origin HEAD
```

In your **group repository**, open a PR from this feature branch to the group's `main`. Explain the change's purpose and placement, paste the before/after log lines and unchanged-result check, and state which checks actually ran. Inspect any CI result linked on the PR; the existence of a workflow does not mean its checks are required by branch protection. Do not commit `.venv`, `.env`, outputs, or unrelated edits.

Ask a teammate to review the diff and rerun the processing command in their own environment. The reviewer should leave a concrete comment about behavior, verification, or clarity: for example, explain why the message gives useful context, why the four counts still agree, and why no row data is exposed. Approval alone is not meaningful review. Address useful feedback and rerun the checks after any edit. If time expires before feedback is resolved, leave the PR open with a clear note about what remains.

Stop after you can show the source import path, explain the module/API boundary and one type hint, show 24/96/95/1 with JSON nulls preserved, and point to the small PR and peer-review evidence. Keep the evidence for Session 5; there is no separate submission, resubmission, or reassessment. Homework, decks, and the instructor's full session run sheet are separate materials.

## Instructor reference and recovery

Use this as a short answer/recovery reference for this activity, not a three-hour delivery plan.

| Observation | Explanation or recovery |
| --- | --- |
| `ModuleNotFoundError: stat_core` or an unexpected import path | Check the root, active interpreter, and `stat_core.__file__`; rerun the editable installation with that interpreter. Do not install globally. |
| `FileNotFoundError` for a CSV | Run from the root containing `data/synthetic/`, not from `backend/`. The package takes file contents; `Path.read_text` supplies them. |
| No INFO line | Confirm `logging.basicConfig` runs in the fresh standalone process. The reusable function does not configure logging. For API runs, see `LOG_LEVEL` and restart guidance in [setup](../../docs/setup.md). |
| Old message after saving | Confirm the saved file matches the printed import path and start a new process. Restart an already running API. An editable install does not reload existing imports. |
| Counts differ, null became zero, or full comparison fails | Inspect the diff and input paths. Undo only the exercise's unintended edits in the editor, keeping others' work. Restore the original message manually from the diff above if needed, then rerun. Do not use a hard reset. |
| Malformed CSV or validation error | Check against the unchanged supplied files and [API validation contract](../../docs/api.md). Keep synthetic inputs intact; do not weaken validation to make a run succeed. |
| Push/review unavailable | Keep the local commit and check output, record the access problem, and arrange review when access returns. Do not claim remote PR or CI evidence exists. |

The reference path is `process_csv` → CSV validation → composite-key join → baseline/change calculations → observed-only summaries → `ProcessResult` → aggregate log → JSON-compatible dictionary. The API handles uploads and HTTP responses around that same function. Expected counts are independently documented in the data dictionary and API contract; missing `EDU-LPA-007` DAY 30 has null value/change/percentage change and baseline 269.0.