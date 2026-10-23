# Session 4 homework: rehearse the final engineering demonstration

Complete **120 minutes of mandatory homework** after [Session 4 practice](../exercises/session-4.md), in your group of three or four. Rehearse your full application and gather the evidence in the [final presentation brief](../assessment/final-presentation.md). Use your independently chosen dataset and question; no topic approval is required. Modeling is optional and complexity earns no extra credit.

Assessment is pass/fail at the final presentation only: **every mandatory engineering requirement must pass**, including each individual's participation. Statistical analysis correctness and scientific conclusions are not graded; tests must still check your declared processing behavior. Homework prepares evidence, with no separate assessed submission, resubmission, reassessment, or later retry during the final session. The presentation result is final.

## Preparation

Have your group's repository and adapted application, Git/GitHub access, Python 3.12 with an activated `.venv` and backend development dependencies, a running Docker engine with Compose v2, curl, browser, and a POSIX shell (bash/zsh; WSL on Windows). Finish installations/image downloads beforehand. Work from the repository root; stop standalone services occupying ports 8000/8501. See [setup](../../docs/setup.md), [Compose](../../docs/compose.md), and [collaboration](../../docs/collaboration.md).

Choose a small shareable or synthetic input representing your own question and declare expected processing, missingness, types, units, and rejection rules. The commands below are runnable for the supplied healthcare contract and unchanged `data/synthetic/dm.csv` and `lb.csv`; they do not accept arbitrary CSV schemas. For your adapted application, use its actual input paths, upload fields, capture entry point, and matching comparison/tests. Ensure the same input bytes are available inside its rebuilt image. Do not disguise unrelated data as healthcare columns. If adaptation is incomplete, record the gap and owner; a template demonstration does not establish your own application's readiness.

| Minutes | Task | Evidence |
| --- | --- | --- |
| 0–15 | Freeze the rehearsal version and inspect hygiene | SHA, interpreter, configuration checks |
| 15–40 | Launch and process CSVs through UI/API | Health, service communication, results, validation |
| 40–55 | Run tests and inspect CI | Actual local summary, hosted run URL/SHA |
| 55–85 | Compare repeated local and real Docker runs | Captures, hashes, metadata, comparison logs |
| 85–110 | Navigate final evidence and individual records | README links, PR/review records, explanations |
| 110–120 | Self-check and shut down | Missing evidence assigned; rehearsal notes |

## 1. Fix the version and check hygiene — 15 minutes

Start from the group's agreed current `main`; preserve unrelated work. Use feature branches → descriptive commits → PRs → meaningful teammate review → merge into the group's `main` for any corrections. Finish code/data changes before captures, record `git rev-parse HEAD`, and rebuild images after changes. Recapture and recheck evidence if the demonstrated version changes.

```bash
git status --short
git rev-parse HEAD
python --version
python -c 'import sys, stat_core; print(sys.executable); print(stat_core.__file__)'
git ls-files .env .venv
```

Confirm Python 3.12 in the active isolated environment and the installed reusable package. Inspect `backend/pyproject.toml`, `.gitignore`, and the shareable `.env.example`; tracked `.env`/`.venv` output should be empty. Inspect intended diffs/history for credentials or private data without displaying secrets. Defaults need no `.env`; keep local settings, environments, private inputs, and generated `outputs/` untracked. Do not publish secrets in logs/screenshots.

## 2. Rehearse startup, upload, and rejection — 25 minutes

```bash
docker compose config --quiet
docker compose up --build --wait --wait-timeout 120
docker compose ps
curl --fail-with-body http://127.0.0.1:8000/health
curl --fail-with-body --retry 20 --retry-all-errors --retry-delay 2 http://127.0.0.1:8501/_stcore/health
docker compose exec -T frontend python -c "import urllib.request; print(urllib.request.urlopen('http://backend:8000/health', timeout=5).read().decode())"
mkdir -p outputs
curl --fail-with-body http://127.0.0.1:8000/process -F participants=@data/synthetic/dm.csv -F laboratory=@data/synthetic/lb.csv --output outputs/api-result.json
```

Expect healthy backend, frontend `ok`, service HTTP `{"status":"ok"}`, and a successful API response saved in ignored `outputs/`. Open <http://127.0.0.1:8501>, select both CSVs, and **Process CSVs**. The supplied example yields 24 participants, 96 records, 95 observed, 1 missing, tables and a chart. Your own application must show its declared results, not these counts by assumption.

Trace browser → Streamlit → multipart `POST /process` → FastAPI → reusable processing → visible results. Explain host ports versus `http://backend:8000` inside Compose; frontend `localhost` means frontend itself. Demonstrate an invalid disposable input through the UI/API (example: DM `AGE=not-a-number` gives 422), inspect its useful error, and open the corresponding passing validation test. Keep original input bytes unchanged. Save health/status/logs and visible results; health alone does not demonstrate browser processing. For failures inspect `docker compose logs --tail=100 backend frontend` and [Compose recovery](../../docs/compose.md).

## 3. Verify tests and the hosted version — 15 minutes

```bash
PYTHONPATH=backend python -m pytest backend/tests
git diff --check
```

Expect **all collected tests to pass**; record the actual count, warnings, command, interpreter, and SHA. Open tests at public processing, API/validation, and comparison boundaries and explain their declared expectations. See [testing](../../docs/testing.md). Open the successful **Backend tests** and **Docker output comparison** jobs for the demonstrated commit in your group's GitHub Actions; retain the run URL/SHA and relevant artifacts before their seven-day expiry. A workflow file or local pass does not establish hosted success, and CI reporting does not itself configure required checks.

## 4. Rehearse both output comparisons — 30 minutes

Use the same checkout and exact CSV bytes throughout, with the real Compose stack still running:

```bash
PYTHONPATH=backend python -m stat_core.capture --participants data/synthetic/dm.csv --laboratory data/synthetic/lb.csv --output outputs/local-1.json
PYTHONPATH=backend python -m stat_core.capture --participants data/synthetic/dm.csv --laboratory data/synthetic/lb.csv --output outputs/local-2.json
PYTHONPATH=backend python -m stat_core.comparison outputs/local-1.json outputs/local-2.json
docker compose exec -T backend python -m stat_core.capture --participants data/synthetic/dm.csv --laboratory data/synthetic/lb.csv > outputs/docker.json
PYTHONPATH=backend python -m stat_core.comparison outputs/local-1.json outputs/docker.json
```

Both comparisons must report `Outputs agree` with exit code 0. Under the [course glossary](../../GLOSSARY.md), the first establishes repeatability under unchanged local conditions; the second establishes replicability under slightly different conditions (local virtual environment versus real Docker). Reproducibility is conceptual; no independent simulation is required. A simulated container, matching chart, or local-only test pass cannot replace the real Docker capture.

Inspect `result`, `input_sha256`, `source_sha256`, and `environment` in the captures. Code/input hashes must match; retain the SHA, exact commands, captures, comparison messages/exit codes, and Python/platform/dependency versions. Explain environment differences rather than requiring identical metadata. For own-data captures, preserve equivalent identity and environment evidence; record exact input paths and versions.

Compare keys, types, structure, list lengths/order, identifiers, demographics, raw cleaned values, copied baselines, counts, and nulls **exactly**; missing is never zero. Only supplied record `change`, record `percent_change`, and visit-summary `mean` allow `abs(actual - expected) <= max(1e-9, 1e-9 * abs(expected))`, first file as reference. Absolute units are nmol/L for change/mean and percentage points for percent change; relative tolerance is dimensionless. Document justified derived-only tolerances in your own tests. Never round, reorder, drop fields, fill nulls, or widen tolerance to hide disagreement. Follow [comparison rules and diagnostics](../../docs/comparisons.md) for mismatches and the controlled failure example; preserve genuine captures.

## 5. Gather and navigate every final evidence item — 25 minutes

In the group's README, link the demonstrated SHA and a compact evidence index: isolated interpreter/package/dependencies; configuration hygiene; package/API/UI separation; real Compose startup/readiness/service HTTP/logs; CSV upload and visible results; invalid-input rejection and its test; passing local tests and hosted CI; both comparison captures/logs, identity, metadata, and exact/tolerant rules. Keep generated evidence outside tracked source and accessible for the presentation. Use the [final checklist](../assessment/final-presentation.md) to inspect every mandatory row, not only screenshots of results.

For **each student**, record name/GitHub username, at least one personally authored PR URL, and a permalink to a substantive review of a teammate's PR. Open the branch/commit history, specific behavior/test/clarity comments, responses and follow-up, and matching CI run/SHA. Approval alone is insufficient. Each member rehearses explaining their contribution and review. Copied template history and instructor/agent work do not count as student participation. Complete missing small contributions through the [reviewed group workflow](../../docs/collaboration.md) before Session 5; one shared PR cannot establish everyone's authorship.

## 6. Self-check and stop — 10 minutes

- Can we launch both services, upload our own CSVs, explain visible results, and reject invalid input clearly?
- Can we open passing local/hosted checks for the demonstrated SHA and explain public-interface tests?
- Do both genuine comparisons pass with matching code/input hashes, recorded environments, and explicit agreement rules?
- Can the instructor inspect every final checklist row and each student's authored PR and meaningful teammate review?

Record any gap honestly with an owner and preparation time before Session 5; unfinished evidence is not a pass. Practise navigating within your allocated presentation slot. Save commands/results and evidence links, then run `docker compose down`. This rehearsal creates no separate homework hand-in or later assessment opportunity.
