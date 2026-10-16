# Session 2 instructor notes: from scripts to reusable modules

Use this provisional 180-minute delivery plan with the [Session 2 slides](../slides/session-2.md) and [guided exercise](../exercises/session-2.md). It is an instructor preparation resource for GitHub issue #31, locally planned as [ticket 32](../../docs/tickets/32-session-2-instructor-notes.md). Teach students to locate responsibilities, run the supplied package, and explain evidence from a small logging change.

Follow the [syllabus](../../SYLLABUS.md), [course specification](../../docs/specs/course-framework-and-teaching-materials.md), and [glossary](../../GLOSSARY.md). Students know functions, pandas, and basic regression. Work in groups of three or four; rotate keyboard, tracing, and review roles. The checkpoint prepares evidence for Session 5. All pass/fail assessment takes place at the final presentation; there is no separate assessed submission, resubmission, reassessment, or later final-session retry. Every student must eventually author one PR and meaningfully review a teammate's PR.

## Resolve the two logging activities before teaching

The actual slides and exercise illustrate two different small edits. Say this explicitly before the demonstration and again when practice starts:

> I will demonstrate adding a DEBUG message counting visit summaries. In your guided exercise, follow section 4: change the existing INFO message's wording. Your PR contains that one-line INFO edit. Both examples show that a useful log can change while the complete processing result stays unchanged.

Keep the teacher's DEBUG example in a separate demonstration checkout. Open an unchanged student example at the handover. The slide titles beginning “Practice:” supply the teacher's DEBUG example and discussion prompts; their edit, branch name, snapshot filenames, and activity subdivisions do not replace the guided exercise. During student work, project the exercise itself. Do not ask students to make both edits or combine their evidence.

Find slides by their exact Markdown titles below. PowerPoint conversion can split a source section across multiple slides, so slide numbers are unreliable. Rehearse the title-to-deck mapping in the presentation software available to you.

## Preparation: tools, data, and starting state

- Have Python 3.12, Git, an editor, two terminals, and a browser ready. Check group GitHub access and installation internet access before class. Docker is not needed for this session. Reserve container comparison for Session 4.
- Prepare a clean instructor demonstration checkout and an unchanged reference checkout. Use [setup](../../docs/setup.md) and exercise [§1](../exercises/session-2.md#1-install-the-editable-package--15-minutes) to create/activate `.venv` and run `python -m pip install -e './backend[dev]'` in each private environment. Start all commands at the repository root. Do not point several editable installations in one shared environment at different checkouts.
- Verify `python --version` and `python -c 'import sys, stat_core; print(sys.executable); print(stat_core.__file__)'`. Expect Python 3.12.x, the intended environment's interpreter, and this checkout's `backend/stat_core/__init__.py`. Keep installation finished before class; narrate or repeat the short command during the demo if downloads would consume the slot. Windows alternatives are in exercise §1 and setup; rehearse them on a Windows host if needed.
- Open [public imports](../../backend/stat_core/__init__.py), [processing](../../backend/stat_core/processing.py), [validation](../../backend/stat_core/validation.py), [schemas](../../backend/stat_core/schemas.py), [API](../../backend/app/main.py), and [package metadata](../../backend/pyproject.toml). Bookmark the [API contract](../../docs/api.md) and [.env.example](../../.env.example). Defaults work without a local `.env`.
- Use only the supplied [DM](../../data/synthetic/dm.csv) and [LB](../../data/synthetic/lb.csv) files; keep them unchanged. Read [provenance](../../data/synthetic/README.md) and the [data dictionary](../../data/synthetic/data-dictionary.md). These are invented teaching data, not clinical evidence. No neighboring repository, download, or database is needed.
- Check `git status --short` in both checkouts. Keep unrelated work intact. Start the demonstration from the original final INFO message and no added DEBUG call. Prepare ignored `.venv/` storage for the slide snapshots; student evidence instead goes in ignored `outputs/`.
- In the second terminal, open the same root and activate the same demo environment. Check that port 8000 is available. If using another port, update both the server and curl address. Have the direct-processing fallback below ready.

## Run sheet: 180 minutes

Elapsed times start at the beginning of class. Explanation is 0–45 (45 minutes), demonstration 45–75 (30), break 75–90 (15), and guided practice 90–180 (90). Practice follows the exercise's 15 + 20 + 15 + 20 + 20 minutes. Keep debrief and evidence review inside those blocks.

| Elapsed | Mode | Actual slide title(s) | Instructor action and observable checkpoint |
| --- | --- | --- | --- |
| 0–5 | Explanation | “Session 2: From scripts to reusable modules”; “Our 180-minute agenda” | State the small-change goal and the two logging activities. Ask what hidden notebook state could make reruns disagree. |
| 5–12 | Explanation | “Give each processing step a home”; “Processing, API, and UI do different jobs” | Explain a module as a file with one job and a package as related importable modules. Ask which layer owns uploads and which owns calculations. UI flow is conceptual here. |
| 12–20 | Explanation | “Find the actual backend modules”; “Follow one call through processing” | Trace public import → `process_csv` → validation/join/calculation/summaries → returned dictionary. Use exercise §2's file table; ask students to point at the boundary rather than copy code. |
| 20–26 | Explanation | “Preserve the healthcare meaning” | State 24/96/95/1; explain the two-field join and missing-versus-zero distinction using the dictionary. Ask why the observed denominator is 95 rather than 96. |
| 26–33 | Explanation | “Read a type hint as an interface description”; “Validation checks values while the program runs” | Read `str`, `dict[str, Any]`, and `float \| None` aloud. A hint describes; runtime checks reject incompatible data. Ask whether a hint alone prevents an invalid age. |
| 33–40 | Explanation | “Packaging describes what gets installed”; “Declare dependencies instead of relying on your laptop” | Locate distribution/import names, Python requirement, runtime dependencies, and `dev` extra. Explain that allowed ranges do not freeze exact versions. |
| 40–45 | Explanation | “Logging makes execution visible” | Distinguish diagnostic DEBUG from normal-progress INFO. The caller chooses visibility. Ask why row contents and identifiers should not enter routine logs. |
| 45–50 | Demonstration | “Demo: install inside an isolated environment” | Show the prepared install and actual interpreter/import paths. Save time by using the already prepared environment if the network stalls. |
| 50–55 | Demonstration | “Demo: run the package without a web server” | Run the slide command, show counts, and identify the four result keys. Contrast CSV text with a filename. See demo steps below. |
| 55–61 | Demonstration | “Demo: trace the API wrapper”; “Demo: find who configures the logs” | Start Uvicorn, send the multipart request, point out the same result shape. Show `.env.example` and caller logging configuration. Stop Uvicorn with Ctrl-C when finished. |
| 61–70 | Demonstration | “Demo: save the result before editing”; “Practice: add one diagnostic message”; “Practice: run again and compare the complete result” | Save the untouched slide baseline, add the teacher-only DEBUG call, run in a fresh process at DEBUG, and compare snapshots. Expect eight summaries and `cmp` exit 0. |
| 70–75 | Demonstration | “Practice: explain the evidence”; “Checkpoint: explain the framework in plain English” | Repeat the DEBUG run; then show that INFO hides DEBUG. Explain exact equality here and the later comparison criteria. Open the unchanged exercise checkout and repeat the INFO-only student instruction. |
| 75–90 | Break | “Break: 15 minutes” | Leave reference materials and snapshots available. Resume on time; students need the whole 90-minute practice block. |
| 90–105 | Practice | “Practice: trace first, then start a branch” (orientation only) | Project exercise [§1](../exercises/session-2.md#1-install-the-editable-package--15-minutes). Students activate/install and check import paths. Use the exercise's branch step later in §3. Circulate for environment/root mistakes. |
| 105–125 | Practice | “Find the actual backend modules”; “Read a type hint as an interface description” | Follow exercise [§2](../exercises/session-2.md#2-follow-the-processing-path--20-minutes). Rotate the person explaining the processing/API boundary, join key, and nullable value. |
| 125–140 | Practice | “Demo: save the result before editing” (principle only) | Follow exercise [§3](../exercises/session-2.md#3-capture-the-unchanged-result--15-minutes). Create each author's uniquely named branch and `outputs/session-2-before.json`. Confirm counts and missing-row details before editing. |
| 140–160 | Practice | “Practice: add one diagnostic message”; “Practice: run again and compare the complete result” (teacher example only) | Project exercise [§4](../exercises/session-2.md#4-add-context-to-the-log-message--20-minutes): change the INFO text, rerun §3 with `after`, compare full results. Require `Processing result unchanged: True` before proceeding. |
| 160–180 | Practice | “Practice: open a PR and give meaningful review”; “Checkpoint: explain the framework in plain English” | Follow exercise [§5](../exercises/session-2.md#5-record-and-review-the-change--20-minutes). Inspect the one-line diff, commit/push to the group repo, and review. During the last five minutes ask another group member to explain the evidence; leave unresolved PRs open with a note. |

## Demo cues and expected observations

### 1. Trace and run the unchanged package

Use the exact standalone command under “Demo: run the package without a web server” or [setup's direct call](../../docs/setup.md#call-processing-without-http). Read both CSVs with UTF-8 and pass their contents to `process_csv`. The result has `counts`, `records`, `arm_summaries`, and `visit_summaries`.

Expect `{'participants': 24, 'records': 96, 'observed': 95, 'missing': 1}` and eight visit summaries (two arms × four visits). Show exercise §3's detailed observation: missing `EDU-LPA-007`, `DAY 30`, has null value/change/percentage change, baseline 269.0, status `NOT DONE`, reason `SPECIMEN NOT AVAILABLE`. Its scheduled row remains present. The first record retains subject ID `001`, value/baseline 167.0, and calculated change/percentage change 0.0. Distinguish those actual zeros from missing values.

Point to the composite `(STUDYID, USUBJID)` join. Baseline comes from the participant's BASELINE record; means use observed values only. The reusable function knows neither HTTP uploads nor UI controls.

### 2. Wrap the same operation with HTTP

Run the slide's Uvicorn and multipart curl commands, also documented in [setup](../../docs/setup.md#run-and-check-the-api). Upload field names are `participants` and `laboratory`. Expect HTTP 200 and the same four result keys/counts; `/health` reports `{"status":"ok"}`. Explain that a healthy server does not prove input validity. The API reads uploads and maps validation errors to HTTP responses; processing still owns calculations.

`create_app()` reads root `.env` once, with exported environment variables taking precedence. Settings are `LOG_LEVEL` and `MAX_UPLOAD_BYTES` (default 5,242,880 bytes per file). Restart after changes. The direct Python caller must configure its own logging; setting `.env` does not configure `process_csv` by itself. Keep input-validation and API-testing detail for Session 3.

If a live service is unavailable, continue with the direct call and trace `app/main.py` on screen. If useful, the following in-process fallback checks the HTTP contract without binding a port. It is not a live-network or browser demonstration:

```bash
python - <<'PY'
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from stat_core import process_csv

dm = Path("data/synthetic/dm.csv").read_bytes()
lb = Path("data/synthetic/lb.csv").read_bytes()
with TestClient(app) as client:
    health = client.get("/health")
    response = client.post("/process", files={
        "participants": ("dm.csv", dm, "text/csv"),
        "laboratory": ("lb.csv", lb, "text/csv"),
    })
print("Health:", health.status_code, health.json())
print("Processing:", response.status_code, response.json()["counts"])
print("Matches direct call:", response.json() == process_csv(dm.decode("utf-8"), lb.decode("utf-8")))
PY
```

Expect health 200, processing 200 with 24/96/95/1, and `Matches direct call: True`. This uses `httpx` from the `dev` extra via FastAPI's TestClient.

### 3. Teacher-only DEBUG example

In the separate demo checkout, run “Demo: save the result before editing” first. It writes `.venv/session-2-before.json`; keep that original snapshot. Insert exactly the call on “Practice: add one diagnostic message” after the existing final INFO call and before `return`, inside `process_csv`:

```python
    logger.debug(
        "Built visit summaries=%d",
        len(result.visit_summaries),
    )
```

Run the slide's fresh-process DEBUG command and `cmp .venv/session-2-before.json .venv/session-2-after.json`. Expect `DEBUG:stat_core.processing:Built visit summaries=8`; `cmp` is silent and returns exit code 0. Rerun once with the same input/environment, keeping the original baseline, to illustrate repeatability. Run again in a fresh process with `logging.INFO` instead of `logging.DEBUG`: the new DEBUG line disappears, the existing INFO line remains, and saved JSON still matches. Logging goes to standard error, separately from the JSON redirected from standard output. Do not redirect both streams into the snapshot.

### 4. Student INFO exercise handover

Open the unchanged example and project exercise §4, rather than the slide's DEBUG patch. Students keep the existing `logger.info` level and four `%d` arguments, changing only its text to:

```text
Processed synthetic healthcare participants=%d records=%d observed=%d missing=%d
```

Use exercise §3's command twice, first with `before`, then after saving the edit with `after`. It writes `outputs/session-2-before.json` and `outputs/session-2-after.json`. Expect the new INFO line with counts 24/96/95/1, the same missing-row display, and exercise §4's comparison reporting `Processing result unchanged: True`. The exercise's Python JSON comparison works without the Unix `cmp` utility. Keep both outputs local and ignored.

Both examples are logging-only regression checks: compare the complete result, not just its counts. Repeating unchanged code/input/environment demonstrates repeatability; comparing before/after a log edit checks that processing behavior was preserved. Neither proves local/Docker replicability. The course uses replicability for the same process under slightly different conditions and reproducibility for very different conditions such as independent simulation. Later local/Docker comparisons use exact records/counts and declared tolerances for calculated decimals. Exact equality is appropriate for these logging edits in one environment; do not invent a universal tolerance here.

## Facilitation, likely questions, and recovery

Ask different students to explain the boundary and evidence, rather than letting one keyboard driver answer everything. During review, ask “What would this comparison miss if we checked only counts?” and “Which observed line proves you imported your own saved edit?” Use the exercise's stopping point: import path, boundary/type explanation, preserved counts/nulls, small PR, and meaningful peer-review evidence. Retain it for Session 5. An approval click alone is not a meaningful review.

| Likely question | Plain-English answer / teaching move |
| --- | --- |
| Why move notebook code into modules? | Explicit inputs and returned results make repeated processing callable without hidden cell state. Keep exploration in the notebook. |
| Why does pip install `three-r-backend` but Python import `stat_core`? | The distribution name identifies what is installed; the import name identifies code exposed by that distribution. This one also supplies `app`. |
| Does editable mean Python reloads everything? | A new process sees saved source edits. Restart a running service; reinstall when package metadata/dependencies change. |
| Does `str` guarantee valid CSV or `float \| None` check an age? | Hints describe expected values for readers/tools. Runtime CSV validation and Pydantic models check actual inputs and result shapes. |
| Why no pandas, classes, or model training here? | The supplied standard-library processing already solves this small example. Focus on boundaries and workflow; modeling is optional. |
| Why did DEBUG disappear at INFO? | The caller's threshold hides diagnostic messages. It does not remove summaries or change returned data. The student INFO text edit remains visible at INFO. |
| Why log aggregates, not upload rows? | Counts help locate progress without copying participant identifiers or measurements into routine logs. The synthetic example teaches that habit. |
| Is a dependency range a reproducible environment? | It permits multiple versions. Record resolved versions with `python -m pip freeze`; later comparisons need declared conditions. |
| Is passing CI enough to prevent an unsafe merge? | A workflow reports its results; required checks depend on branch protection. Inspect what is actually configured in the group repository. |

| Common failure | Recovery within the timebox |
| --- | --- |
| Import fails or points at another checkout | Check root, `sys.executable`, and `stat_core.__file__`. Activate the intended private environment and rerun its editable install. Avoid global installation. If setup consumes the slot, pair with a working group member and record the unresolved setup issue. |
| Dependency download fails | Use the preinstalled demo environment; students can pair while access is repaired. Explain what the installation command would do; do not report it succeeded on their machine. |
| CSV path fails / function rejects a filename | Return to the root; use `Path(...).read_text(encoding="utf-8")` to supply contents. Verify original DM/LB paths, not a group's unrelated dataset. |
| No INFO/DEBUG message or old wording | Use a fresh process; check saved file/import path and caller logging level. A direct call needs `basicConfig`; an API process needs restart. Keep logging configuration outside `process_csv`. |
| Demo snapshot missing / malformed JSON | Ensure `.venv/` exists and the baseline was captured before editing. Keep stderr separate from stdout. For student work use exercise §3's `outputs/` command, not slide snapshot paths. |
| Counts/nulls differ or comparison fails | Inspect input paths and the source diff. Correct only unintended exercise edits in the editor; preserve unrelated work. Restore the original message manually if needed and establish a new clearly labelled untouched baseline before trying again. Never overwrite the original baseline to force a match or use a hard reset. |
| DEBUG demo accidentally used for student practice | Return to the unchanged student checkout. Show the exercise §4 one-line INFO diff and use its filenames. Keep the teacher's DEBUG output labelled separately. |
| HTTP bind denied, port occupied, or request fails | Choose a free port and update curl, or use the checked in-process fallback. Connection refused means check startup/port first. For 422 check multipart names and contract; for 413 inspect the actual upload limit. Keep inputs/validation intact. |
| Git branch already exists / worktree has other edits | Inspect `git status --short`; finish or save existing work without discarding it. Use the exercise's unique author name, or resume the intended existing branch after checking it. |
| Push, PR, or review access unavailable | Keep the local commit and check evidence; record the access problem and arrange review when access returns. Do not claim PR/CI evidence exists. Leave unfinished review open with its next action; this is preparation, not an extra assessment deadline. |

Student PRs target their **group repository's `main`**, as in the exercise. That classroom workflow is separate from the course-authoring integration branch. Inspect only the intended processing-file diff; keep `.env`, environments, output evidence, and unrelated files out of commits. If the checkout includes the formal backend suite, use its documented command before review; otherwise do not invent tests or report an absent suite as passing.

## Concise rehearsal checklist

- [ ] Locate every run-sheet title in the actual deck, including any continuation slides; open exercise §§1–5 alongside it.
- [ ] Confirm clean demo/reference states, interpreter/import paths, prepared editable environment, GitHub access, and unchanged synthetic inputs.
- [ ] Run direct processing and identify all four result keys, 24/96/95/1, eight summaries, preserved `001`, and the null/269.0 missing-row example.
- [ ] Rehearse live HTTP startup/upload where permitted; keep the in-process fallback available and label which route actually ran.
- [ ] Capture an untouched demo baseline, add DEBUG, compare full results, repeat, and check INFO hides DEBUG. Keep snapshots out of Git.
- [ ] Switch to the unchanged student example; rehearse exercise §3 → §4 INFO edit → `after` → full JSON equality. State clearly that students make only that INFO edit.
- [ ] Fit the handover before minute 75 and keep practice checkpoints at 105/125/140/160/180. Prepare pairing recovery for installation trouble.
- [ ] Rehearse the one-line PR diff and meaningful review prompt; restate final-presentation-only assessment and course glossary meanings.

## Author verification and practical limits

This documentation task uses content, command, and link checks rather than adding artificial tests. Processing/API/result-comparison boundaries are the supplied public interfaces. Rehearsal uses Python 3.12 in the shared temporary environment with `PYTHONPATH=backend`; it does not change the shared environment's editable-install target. Logging edits are exercised only in disposable copies, never in this issue's application source.

The standalone slide calls/snapshot comparisons, teacher DEBUG visibility at DEBUG versus INFO, exercise §3/§4 before/after commands, complete-result equality, and the in-process API fallback were checked against the supplied backend. Expected counts, missingness, identifiers, and eight summaries agreed. Timing, actual slide titles, exercise section references, relative file links, and whitespace were checked.

Installation guidance is sourced from setup and the exercise's recorded author verification: editable installation was checked there in a disposable environment with existing dependencies using `--no-deps --no-build-isolation`; fresh dependency downloads were not rehearsed here. Live Uvicorn/curl behavior is supported by the shared implementation `verification.md` record: port 18000 returned HTTP 200 and 24/96/95/1 with eight summaries; setup and slides use port 8000. The backend-contract record separately documents TestClient checks. Those shared authoring records are outside the published repository; portable commands and behavior are documented in [setup](../../docs/setup.md) and the [API contract](../../docs/api.md).

Docker is unavailable; no container run or local/Docker comparison is claimed. No LibreOffice/PowerPoint renderer is available, so source-title/link checks do not verify rendered layout or clipping. Windows/PowerShell execution, fresh installation downloads, and student GitHub permissions/peer reviews were not exercised. Check these delivery conditions on the teaching machines before class.
