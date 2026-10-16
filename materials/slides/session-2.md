# Session 2: From scripts to reusable modules

- Follow the supplied healthcare processing package.
- Read its dependencies, type hints, and logs.
- Make one small logging change through a reviewed PR.
- Start with the working example; keep its results unchanged.

---

## Our 180-minute agenda

- 0–45: explanation — modules, boundaries, packaging, types, logs.
- 45–75: demonstration — install, trace, run, save a baseline.
- 75–90: break — 15 minutes.
- 90–180: guided practice — change, check, and review.
- Practice: trace 15 + edit 20 + check 25 + explain 15 + review 15.

---

## Give each processing step a home

- A module is a Python file with a clear responsibility.
- A package groups modules that can be imported together.
- Keep exploration in a notebook; give repeated work a function.
- Pass inputs in and return results; avoid hidden notebook state.
- Here, `stat_core.process_csv` is the reusable entry point.

---

## Processing, API, and UI do different jobs

```text
UI: choose files and display results
    -> API: accept uploads and report HTTP errors
        -> processing: validate, join, calculate, summarize
        <- result dictionary
    <- JSON response
```

- API means a defined way for programs to communicate.
- UI means the screen a person uses.
- UI flow is conceptual here; the supplied frontend is explored in Session 4.

---

## Find the actual backend modules

```text
backend/
  pyproject.toml          package and dependency metadata
  stat_core/__init__.py  public imports
  stat_core/processing.py  process_csv
  stat_core/validation.py  CSV and domain checks
  stat_core/schemas.py   result and error shapes
  stat_core/errors.py    InvalidInputError
  app/main.py           create_app and HTTP endpoints
```

- Trace from [public imports](../../backend/stat_core/__init__.py).

---

## Follow one call through processing

```text
stat_core.process_csv(participants_csv, laboratory_csv)
  read_csv + validate_participants
  read_csv + validate_laboratory
  join laboratory rows to participants
  calculate baseline, change, percent_change
  build counts, arm_summaries, visit_summaries
  return ProcessResult.model_dump(mode="json")
```

- These steps live in [processing.py](../../backend/stat_core/processing.py).
- The caller supplies CSV contents, not filenames or uploads.

---

## Preserve the healthcare meaning

- DM: 24 participants; LB: 96 laboratory records.
- Join on both `STUDYID` and `USUBJID`.
- Keep subject identifiers as text, including leading zeros.
- Preserve the unavailable result: 95 observed, 1 missing.
- Missing is not zero; means use observed values only.
- These are invented teaching data, not clinical evidence.
- See the [data dictionary](../../data/synthetic/data-dictionary.md).

---

## Read a type hint as an interface description

From `backend/stat_core/processing.py`:

```python
def process_csv(
    participants_csv: str,
    laboratory_csv: str,
) -> dict[str, Any]:
```

- `str`: CSV text comes in; `dict`: a dictionary comes back.
- `Any`, imported from `typing`, allows different value types.
- A hint helps readers and tools; it does not check data itself.

---

## Validation checks values while the program runs

From `backend/stat_core/schemas.py`:

```python
value: float | None
records: list[Record]
```

- `None` means unavailable; `list[Record]` means many records.
- CSV checks reject invalid ages, units, keys, and dates.
- Pydantic models check the declared result shape.
- Python raises `InvalidInputError`; the API maps it to HTTP 422.
- Read the [contract](../../docs/api.md) for exact rules and errors.

---

## Packaging describes what gets installed

Actual entries from [pyproject.toml](../../backend/pyproject.toml):

```toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"
[project]
name = "three-r-backend"
version = "0.1.0"
requires-python = ">=3.12"
```

- Metadata means the package's name, version, and requirements.
- Distribution name: `three-r-backend`; import name: `stat_core`.
- Package discovery includes both `stat_core*` and `app*`.

---

## Declare dependencies instead of relying on your laptop

- A dependency is another package our code needs.
- Runtime: FastAPI, Pydantic, python-dotenv, python-multipart, Uvicorn.
- The `dev` extra is an optional group: pytest and httpx for checks.
- Example range: `pydantic>=2.9,<3` allows 2.x versions from 2.9.
- A range is not a lockfile; record resolved versions for comparisons.
- This small CSV example uses the standard library, not pandas.

---

## Logging makes execution visible

Existing module setup in `backend/stat_core/processing.py`:

```python
import logging
logger = logging.getLogger(__name__)
```

- The logger's name is `stat_core.processing`.
- DEBUG: diagnostic detail; INFO: normal progress.
- WARNING: concern; ERROR: failure; CRITICAL: severe failure.
- The caller configures visibility; processing emits messages.
- Log counts and locations, never uploaded rows or identifiers.

---

## Demo: install inside an isolated environment

Run from the repository root with Python 3.12 and Git available:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e './backend[dev]'
python -c 'import stat_core; print(stat_core.__file__)'
```

- The printed path should end in `backend/stat_core/__init__.py`.
- Editable means imports use this checkout's source files.
- Start a new process after edits; reinstall after metadata changes.
- Windows activation and setup help: [setup.md](../../docs/setup.md).

---

## Demo: run the package without a web server

Use the activated environment, from the repository root:

```bash
python - <<'PY'
from pathlib import Path
from stat_core import process_csv

result = process_csv(
    Path("data/synthetic/dm.csv").read_text(encoding="utf-8"),
    Path("data/synthetic/lb.csv").read_text(encoding="utf-8"),
)
print(result["counts"])
PY
```

- Expected counts: participants 24, records 96, observed 95, missing 1.

---

## Demo: trace the API wrapper

In `backend/app/main.py`, `create_app()` registers `/process`.
It reads uploads, calls `process_csv`, and returns `ProcessResult`.

```bash
python -m uvicorn app.main:app --app-dir backend \
  --host 127.0.0.1 --port 8000
```

In another terminal at the repository root:

```bash
curl --fail-with-body http://127.0.0.1:8000/process \
  -F participants=@data/synthetic/dm.csv \
  -F laboratory=@data/synthetic/lb.csv
```

- Result keys: `counts`, `records`, `arm_summaries`, `visit_summaries`.
- HTTP handles transport; the processing package owns calculations.

---

## Demo: find who configures the logs

- `create_app()` reads root `.env`; environment variables win.
- Actual settings: `LOG_LEVEL` and `MAX_UPLOAD_BYTES`.
- Defaults work; see [.env.example](../../.env.example).
- Restart the service after changing its settings.
- Direct Python callers configure logging themselves.
- With INFO enabled, the existing processing message is:

```text
INFO stat_core.processing: Processed participants=24
  records=96 observed=95 missing=1
```

- Wrapped here for readability; the real message is one line.

---

## Demo: save the result before editing

The existing `.venv/` directory is ignored by Git.
Save a sorted JSON snapshot there; logs use standard error.

```bash
python - <<'PY' > .venv/session-2-before.json
import json
from pathlib import Path
from stat_core import process_csv

dm = Path("data/synthetic/dm.csv").read_text(encoding="utf-8")
lb = Path("data/synthetic/lb.csv").read_text(encoding="utf-8")
print(json.dumps(process_csv(dm, lb), sort_keys=True))
PY
```

- Keep this baseline; do not overwrite it after the change.

---

## Break: 15 minutes

- Leave the baseline and virtual environment in place.
- Return ready to explain where processing ends and HTTP begins.

---

## Practice: trace first, then start a branch

First 15 minutes: work in your group repository.

```bash
git status --short
git switch -c feature/session-2-summary-log
```

- Start from the group's current default branch and clean worktree.
- Find `process_csv` and its existing final `logger.info` call.
- Explain its input, four result keys, and callers to a teammate.
- Target: one DEBUG message giving the number of visit summaries.

---

## Practice: add one diagnostic message

Next 20 minutes: in `backend/stat_core/processing.py`,
insert this after the existing INFO call, before the return.
Indent it four spaces inside `process_csv`:

```python
logger.debug(
    "Built visit summaries=%d",
    len(result.visit_summaries),
)
```

- `%d` is an integer placeholder; logging formats the value.
- Reuse the module logger and the already computed result.
- Do not put logging configuration inside the processing function.

---

## Practice: run again and compare the complete result

Next 25 minutes: enable DEBUG in this new Python process:

```bash
python - <<'PY' > .venv/session-2-after.json
import json
import logging
from pathlib import Path
from stat_core import process_csv

logging.basicConfig(level=logging.DEBUG)
dm = Path("data/synthetic/dm.csv").read_text(encoding="utf-8")
lb = Path("data/synthetic/lb.csv").read_text(encoding="utf-8")
print(json.dumps(process_csv(dm, lb), sort_keys=True))
PY
cmp .venv/session-2-before.json .venv/session-2-after.json
```

- Expect `DEBUG:stat_core.processing:Built visit summaries=8`.
- `cmp`: no output and exit code 0 means identical saved results.

---

## Practice: explain the evidence

Next 15 minutes: discuss with a teammate.

- Run the previous Python block again: same input, same environment.
- The saved result must still match; the DEBUG message stays separate.
- At INFO level, the new DEBUG message should disappear.
- No message? Check log level, insertion point, and imported file path.
- Import fails? Check environment, editable install, and working folder.
- A changed result needs investigation before review.
- This logging change uses exact JSON equality, with no tolerance.

---

## Practice: open a PR and give meaningful review

Final 15 minutes: inspect and publish only the small source change.

```bash
git diff --check
git diff -- backend/stat_core/processing.py
git add backend/stat_core/processing.py
git commit -m "Log visit summary count at debug level"
git push -u origin feature/session-2-summary-log
```

- Open a pull request to the group repository's `main` on GitHub.
- Describe the message, DEBUG output, and identical JSON evidence.
- A teammate checks placement, clarity, and absence of row data.
- Inspect available PR checks; address review before merging.
- Keep an authored PR and a meaningful teammate review per student.

---

## Checkpoint: explain the framework in plain English

- Module: one file's job; package: reusable imports plus metadata.
- Processing owns calculations; API owns HTTP; UI owns interaction.
- Editable install connects the environment to your source checkout.
- Type hints describe values; validation checks them; logs explain runs.
- Repeatability: agreement under the same conditions.
- Replicability: same process under slightly different conditions.
- Reproducibility: very different conditions, such as independent simulation.
- Local/Docker comparison comes later; decimals need declared tolerances.
- Course meanings and next session: [glossary](../../GLOSSARY.md), [syllabus](../../SYLLABUS.md).
