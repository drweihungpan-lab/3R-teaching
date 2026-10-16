# Session 4 guided practice: connected services and comparable outputs

Spend 90 minutes inspecting the supplied working example in your group. Follow the
[course definitions](../../GLOSSARY.md): repeatability uses unchanged conditions;
replicability uses the same process with slightly different conditions (local Python
versus Docker). Reproducibility is discussion only; no independent simulation is required.

## Before practice

Have Git, Python 3.12, an activated environment with backend dependencies from
[setup](../../docs/setup.md), Docker with a running engine and Compose v2, curl,
a browser, and a POSIX shell (bash/zsh). Use the repository root for every command.
On Windows use WSL for these shell commands. Complete installations and image downloads
before class; stop old local services using ports 8000/8501. No `.env` is required.
Use the supplied [synthetic CSVs](../../data/synthetic/README.md), not patient data.
Keep code and CSV bytes unchanged throughout captures; rebuild images after any edits.
The command reference is [output comparisons](../../docs/comparisons.md).

## 0–20 minutes: launch and inspect the working application

```bash
docker compose version
docker compose config --quiet
docker compose up --build --wait --wait-timeout 120
docker compose ps
curl --fail-with-body http://127.0.0.1:8000/health
curl --fail-with-body --retry 20 --retry-all-errors --retry-delay 2 http://127.0.0.1:8501/_stcore/health
```

Expect both services running, backend healthy, API `{"status":"ok"}`, and frontend
health `ok`. The backend health check gates frontend startup; it cannot guarantee
that a later request succeeds. Open <http://127.0.0.1:8501> and check the displayed
`Backend: http://backend:8000`. Upload `data/synthetic/dm.csv` under **Participants
CSV (DM)** and `data/synthetic/lb.csv` under **Laboratory CSV (LB)**; select **Process CSVs**.
Expect **24 participants, 96 joined records, 95 observed, 1 missing**, tables, and
the mean lipoprotein(a) chart by study day and arm, with separate study panels.
Find the unavailable DAY 30 observation for `EDU-LPA-007`; it remains missing, not zero.
The chart shows descriptive synthetic values, not evidence of clinical benefit.

## 20–40 minutes: trace HTTP and recover a wrong address

Inspect [frontend/app.py](../../frontend/app.py), [API handling](../../backend/app/main.py),
and [compose.yaml](../../compose.yaml). Explain the path: browser → Streamlit Python
→ multipart `POST /process` → FastAPI → `stat_core` → returned tables/chart.
The browser uses host port 8501; host curl uses port 8000. Compose DNS resolves
`backend` inside the shared network. Inside frontend, `localhost` means frontend itself.

```bash
docker compose exec -T frontend python -c "import urllib.request; print(urllib.request.urlopen('http://backend:8000/health', timeout=5).read().decode())"
```

Expect `{"status":"ok"}`. Now change only a disposable override, leaving the real
Compose file and local `.env` untouched. Keep this shell open until restoration:

```bash
exercise_tmp=$(mktemp -d)
python -c 'from pathlib import Path; import sys; Path(sys.argv[1]).write_text("services:\n  frontend:\n    environment:\n      BACKEND_URL: http://localhost:8000\n")' "$exercise_tmp/wrong.yaml"
docker compose -f compose.yaml -f "$exercise_tmp/wrong.yaml" up -d --no-deps --force-recreate frontend
```

Reload the browser, reselect both files, and process. Expect the displayed wrong
address and **Could not connect to the backend**, with no successful results.
Check host API health and rerun the service-DNS command above: both should still work.
Explain why a healthy API does not repair the frontend's wrong destination.
Restore explicitly, even if the demonstration failed or was interrupted:

```bash
docker compose -f compose.yaml up -d --no-deps --force-recreate frontend
```

Reload and upload again: the address must be `http://backend:8000`, with the original
counts and chart. If the shell was lost, this same restoration command still works.
The override remains only in the disposable directory and is not loaded automatically.

## 40–60 minutes: capture twice locally and explain agreement

Use the activated Python 3.12 environment; these commands select this checkout even
if another checkout shares your environment. They call processing directly, without HTTP.

```bash
PYTHONPATH=backend python -m stat_core.capture --participants data/synthetic/dm.csv --laboratory data/synthetic/lb.csv --output outputs/local-1.json
PYTHONPATH=backend python -m stat_core.capture --participants data/synthetic/dm.csv --laboratory data/synthetic/lb.csv --output outputs/local-2.json
PYTHONPATH=backend python -m stat_core.comparison outputs/local-1.json outputs/local-2.json
```

Expect `Outputs agree` and exit code 0: evidence of repeatability. Inspect `result`,
`input_sha256`, `source_sha256`, and `environment` in each JSON. Hashes cover exact
CSV bytes and backend Python sources; record Python, platform, and dependency versions.
Keys, types, list lengths/order, identifiers, demographics, raw cleaned values, copied
baselines, counts, and nulls must match exactly. Missing is never equivalent to zero.
Only record `change`, record `percent_change`, and visit-summary `mean` use
`abs(actual - expected) <= max(1e-9, 1e-9 * abs(expected))`, with the first file as reference.
Absolute units are nmol/L for change/mean and percentage points for percent change;
relative tolerance is dimensionless. Do not round, reorder, fill nulls, or widen tolerance.

## 60–80 minutes: compare Docker and demonstrate a controlled failure

With the restored stack running, capture inside the real backend container:

```bash
docker compose exec -T backend python -m stat_core.capture --participants data/synthetic/dm.csv --laboratory data/synthetic/lb.csv > outputs/docker.json
PYTHONPATH=backend python -m stat_core.comparison outputs/local-1.json outputs/docker.json
```

Expect `Outputs agree` and exit code 0: replicability under the course convention.
Code/input hashes must match; environment descriptions may differ. Record those
differences and the checkout SHA (`git rev-parse HEAD`) beside your evidence.
For a controlled mismatch, edit only a generated copy, never the code or sample CSVs:

```bash
cp outputs/local-2.json outputs/changed.json
python -c 'import json; from pathlib import Path; p=Path("outputs/changed.json"); d=json.loads(p.read_text()); d["result"]["counts"]["missing"]=0; p.write_text(json.dumps(d))'
PYTHONPATH=backend python -m stat_core.comparison outputs/local-1.json outputs/changed.json
echo $?
cp outputs/local-2.json outputs/changed.json
PYTHONPATH=backend python -m stat_core.comparison outputs/local-1.json outputs/changed.json
```

Expect a `counts.missing` mismatch and exit code **1**, then restored agreement and
exit code **0**. This deliberately altered evidence demonstrates detection, not a
new processing run. Keep the original captures and comparison messages in ignored `outputs/`.

## 80–90 minutes: stopping point and recovery reference

Stop when both services process the uploads, the wrong address has been restored,
both comparisons agree, and the changed-count failure has been explained and recovered.
Tell a partner which conditions stayed fixed and which changed. Preserve actual
commands, results, environment metadata, and SHA; label skipped work as unverified.
This checkpoint prepares for the final presentation; it is not a separate assessment.
Finish with `docker compose down` to remove this project's containers/network.

If startup fails, inspect `docker compose logs --tail=100 backend frontend` and
`docker compose ps`; check engine, occupied ports, and backend health before retrying.
For hash mismatches restore the same code/inputs and rebuild; for numerical mismatches
inspect dependency/processing differences. See [Compose recovery](../../docs/compose.md),
[frontend behavior](../../docs/frontend.md), and [comparison rules](../../docs/comparisons.md).

Verification boundary: local authoring checks execute capture/comparison and the
controlled count failure/recovery. Docker is absent on the authoring host. Existing
[CI run 38876609585](https://github.com/drweihungpan-lab/3R-teaching/actions/runs/38876609585)
verified real builds, both service health endpoints, service DNS/HTTP, repeated local,
local/Docker, and multipart API agreement. It does not verify this classroom's browser
upload/chart or temporary wrong-address exercise; rehearse those on a Docker machine.
For prior test evidence, report “all tests pass” with the run's actual count (205 in
that run); counts can change. No unchanged full-suite rerun is needed for this brief.
