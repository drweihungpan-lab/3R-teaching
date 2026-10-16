# Session 2 homework: a small change your group can explain

This is **120 minutes of mandatory homework** after [Session 2 guided practice](../exercises/session-2.md), for each student working within their group of three or four. Apply one small, documented processing or logging change relevant to your group's chosen dataset and question. Explain where it belongs, check its behavior, and put it through a feature branch, pull request (PR), and meaningful teammate review.

Your group chooses its dataset and question independently; no topic approval is required. Modeling is optional and complexity earns no extra credit. Keep this change small enough to explain and check in two hours. You are extending working code, not completing missing application functions or building the whole project tonight.

Keep the evidence for the final presentation in Session 5. Homework is preparation, not a separate assessed submission. Assessment is pass/fail at that presentation, with no separate submission, resubmission, or reassessment. Statistical analysis correctness is not graded; engineering checks must still demonstrate your declared processing behavior. See the [syllabus and assessment policy](../../SYLLABUS.md).

## Preparation

Have your group's GitHub repository, chosen dataset and question, Python 3.12 environment, Git, editor, and permission to push branches and review PRs ready. Reuse the editable package installation from the [guided exercise](../exercises/session-2.md) and [setup instructions](../../docs/setup.md). Keep the supplied [synthetic CSVs](../../data/synthetic/README.md) unchanged as a working reference. Have a small, shareable example of your own data available for checks; do not commit private data or credentials.

All commands below run from your **group repository root**, containing `backend/`, `data/`, and `docs/`. Activate `.venv` with `source .venv/bin/activate` on macOS/Linux or `.venv\Scripts\Activate.ps1` on Windows PowerShell. If setup needs repair, follow the linked setup guide before changing code.

| Time | Task | Evidence to keep |
| --- | --- | --- |
| 0–15 min | Prepare and plan participation | Environment/import path; author and reviewer plan |
| 15–35 min | Choose the change and declare behavior | Dataset/question, module choice, valid and invalid examples |
| 35–50 min | Capture the working baseline | Exact command, input description, result and log |
| 50–80 min | Make one change and check it | Small diff; actual before/after checks |
| 80–110 min | Publish and review the PR | PR link, useful review, response to feedback |
| 110–120 min | Organize final evidence and self-check | Evidence links and remaining participation plan |

## 1. Prepare and assign roles — 15 minutes

Check your location, interpreter, source import, and current work:

```bash
git rev-parse --show-toplevel
git status --short
python --version
python -c 'import sys, stat_core; print(sys.executable); print(stat_core.__file__)'
```

Expect Python 3.12.x, an interpreter inside your environment, and `stat_core` imported from this clone's `backend/stat_core/__init__.py`. Save or finish unrelated work without discarding it. Create your own branch, replacing `your-name` and `short-purpose` with meaningful, unique values:

```bash
git switch -c homework-2/your-name-short-purpose
```

Every individual must have authored at least one PR and meaningfully reviewed a teammate's PR **by the final presentation**. A group PR or a shared keyboard does not demonstrate authorship for every member. In your group's existing project notes or PR description, record a row for every person: name, authored PR link or planned change/session, and reviewed PR link or assigned teammate/session. Rotate roles from the classroom exercise. For example, A reviews B, B reviews C, and C reviews A; in a group of four, include D in the rotation. Use separate small changes or branches to avoid editing the same lines simultaneously. One group change tonight does not satisfy everyone's individual requirement; make any remaining work explicit.

## 2. Choose a change and explain its placement — 20 minutes

Write a short change note in your PR description or existing project documentation:

- State your dataset, its source, and your question. Identify one processing step that matters to that question.
- Describe one small change: for example, log the observed/missing counts for the variable your question uses, or trim surrounding whitespace in one category before summarizing it. A log must report something the running code actually processed; merely renaming the healthcare example after your dataset is not enough.
- Name the module/function you will edit and explain why. A module is a Python file; a package groups modules for import. Explain one relevant type hint, including whether a missing value is allowed.
- Declare a tiny valid input and expected output or log message, plus an invalid input and expected rejection. State identifiers/join keys, required columns, types, units where relevant, and the missing-value rule. Calculate expected values independently from the input, rather than copying whatever your code currently returns.

Use the existing boundaries as your guide:

| Responsibility | Supplied source to inspect | Placement rule |
| --- | --- | --- |
| Reusable processing and aggregate logs | [stat_core/processing.py](../../backend/stat_core/processing.py) | Data rules belong in the processing package so scripts and the API use the same behavior. |
| CSV input rules | [stat_core/validation.py](../../backend/stat_core/validation.py) | Reject invalid data explicitly; do not hide it by converting errors to zero. |
| Return fields and type hints | [stat_core/schemas.py](../../backend/stat_core/schemas.py), [public exports](../../backend/stat_core/__init__.py) | Keep the public result contract clear and explain any intentional change. |
| Uploads and HTTP responses | [app/main.py](../../backend/app/main.py), [API contract](../../docs/api.md) | HTTP handling wraps processing; avoid copying processing rules into the endpoint or UI. |
| Dependencies and configuration | [pyproject.toml](../../backend/pyproject.toml), [setup](../../docs/setup.md) | Explain existing dependencies; let the caller configure logging rather than adding `basicConfig` inside reusable code. |

Use your group's existing processing function if its dataset differs from the healthcare example. The supplied `process_csv(participants_csv, laboratory_csv)` accepts CSV **text**, not paths, and requires the documented DM/LB healthcare columns, units, and visits. It does not accept an arbitrary CSV. Do not rename your columns to healthcare fields just to force it through. If your group has not yet connected its data to the package, choose one small preparation rule for your actual data in a reusable function within the package; leave full API/UI adaptation for the later project work. Keep the supplied example working. Record the actual public function and command you use for your group check.

Checkpoint: a teammate can explain the purpose, location, expected behavior, and input rules before you edit.

## 3. Capture the baseline — 15 minutes

Run your group's existing processing command on the small example and record the exact command, input version, expected and actual result, and log if relevant. If you are introducing a small preparation function, record the current processing step it will replace and its result. Keep generated run evidence locally in ignored `outputs/`; put concise, shareable observations in the PR.

Also run this supplied reference check from the root. The multiline `python -c` form follows the guided exercise and saves a complete result for comparison:

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
assert result["counts"] == {"participants": 24, "records": 96, "observed": 95, "missing": 1}
print(result["counts"])
Path("outputs").mkdir(exist_ok=True)
destination = Path("outputs") / ("homework-2-" + sys.argv[1] + ".json")
destination.write_text(json.dumps(result, sort_keys=True, indent=2), encoding="utf-8")
print(destination)
' before
```

Expect counts of 24 participants, 96 records, 95 observed, and one missing, followed by `outputs/homework-2-before.json`. Inspect the missing record: `EDU-LPA-007` at `DAY 30` has null value/change/percentage change and baseline 269.0. These expectations come from the [API worked examples](../../docs/api.md) and [data dictionary](../../data/synthetic/data-dictionary.md). This reference run checks the supplied example; it is not evidence that your own dataset was processed.

## 4. Make and check one small change — 30 minutes

Make the declared change in your branch. For a processing change, first show that the small expected-behavior check fails against the old behavior, then implement just enough to pass it. Check the public processing function's returned result or public API response, not its private helper calls or module layout. For logging, capture the old and new message and verify that results stay unchanged. Use aggregate counts or useful context without logging row contents or identifiers; keep the logger configurable by the caller.

Rerun your own-data command and invalid-input example. Record the actual outputs. An unchanged input rule must still reject the invalid case. If you intentionally changed a rule, explain the new expectation and check both a newly accepted case and a still-invalid case. Missing values must remain distinct from zero. For the healthcare reference, invalid AGE text is rejected; missing results require the documented status/reason, joins use both `STUDYID` and `USUBJID`, and units must be `nmol/L`. The [API contract](../../docs/api.md) gives the complete rules and the `InvalidInputError.issues` / HTTP 422 error formats.

Rerun the entire reference command in step 3 with only its final argument changed from `before` to `after`, then compare:

```bash
python -c 'import json; from pathlib import Path; before = json.loads(Path("outputs/homework-2-before.json").read_text(encoding="utf-8")); after = json.loads(Path("outputs/homework-2-after.json").read_text(encoding="utf-8")); print("Reference result unchanged:", before == after); assert before == after, "Inspect whether the processing change intentionally affects the reference"'
git diff --check
git diff
```

For a logging change or an isolated own-data preparation rule, expect `Reference result unchanged: True`. If your declared processing change intentionally affects the reference result, an equality failure is information to investigate: identify the affected fields, verify their independently worked expected values, and confirm unaffected fields still agree. Do not simply remove the assertion and claim success. The fixed count assertion in step 3 is for an unchanged reference contract; a deliberate count change requires documented new expectations too.

This exact comparison is a focused check in the same environment. It does not replace tests of your own data, nor demonstrate local/Docker replicability. Later comparisons use the [course glossary](../../GLOSSARY.md) and documented criteria: records/counts exactly, calculated decimals within the declared tolerance. Do not invent a tolerance or equate null with zero.

Run the supplied backend suite too: `python -m pytest backend/tests` from the repository root; follow [backend setup](../../docs/setup.md) and [testing instructions](../../docs/testing.md). Record the actual result alongside the processing check above and your declared own-data checks. Session 3 develops the testing workflow further. After source edits, use a fresh Python process; restart any running API. An editable install needs reinstalling only when dependency metadata changes.

## 5. Publish a PR and review a teammate — 30 minutes

Inspect `git status --short`, then stage only the source and documentation files for your change. Use `git add` with those explicit paths; do not stage `.venv`, `.env`, outputs, private data, or unrelated work. Commit with a message describing the actual change, then push:

```bash
git commit -m "Describe your small processing or logging change"
git push -u origin HEAD
```

Open a PR in your **group repository**, from your feature branch to the group's `main`. Include the dataset/question, purpose, module-placement explanation, declared behavior/input rules, small diff, exact commands and observed results, and any unavailable checks. Link the relevant source files. Inspect the actual CI result if available; a copied workflow file does not itself make checks required by branch protection.

Review a teammate's PR and have a teammate review yours. Read the diff, rerun the supplied command and the group's small example, and leave a concrete comment about behavior, input rules, verification, or clarity. For example: “The example's two missing values remain null and the new log reports two missing observations; please explain why this count matters to our question in the PR.” Approval alone is not meaningful review. Verify the comment against the actual change rather than copying this example.

Respond to feedback, make any needed edits, and rerun affected checks. Follow your group's reviewed merge workflow. If review or access is delayed, keep the PR open, record what is pending, and assign an owner and next session to finish it. Do not claim a review, merge, or passing CI result that has not happened.

## 6. Keep evidence and self-check — 10 minutes

Keep a concise record in the PR or existing group notes: dataset/question and input version; module and type-hint explanation; branch/commit and PR link; expected versus observed behavior; exact commands and actual results; meaningful review link and your response; and remaining work. Refresh every individual's authored-PR/review links or planned owner/session. Retain local run outputs for the final presentation without committing generated files.

- Can I explain why this small change matters to our chosen question and belongs in this module?
- Does the package import from this environment and checkout, and can I explain the editable installation and relevant dependency declaration?
- Can I show the intended behavior, preserved missingness, invalid-input handling, and what the checks actually establish?
- Can a teammate rerun the commands, understand the PR, and find a meaningful review and response?
- Does every person have an authored PR and meaningful review, or an explicit plan to complete both before Session 5?

Stop with these evidence links and any remaining work recorded. There is no separate homework hand-in or reassessment. FastAPI, Streamlit, Docker Compose, passing tests/CI, and the final output-comparison evidence remain requirements for the final presentation; this two-hour change prepares part of that evidence.
