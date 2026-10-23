# Session 4 instructor notes: containers and output comparisons

Use the supplied working example with 20 students in groups of three or four.
The goal is to explain a connected system and retain evidence of agreement.
Follow the [syllabus](../../SYLLABUS.md) and
[course glossary](../../GLOSSARY.md). This provisional 180-minute plan uses
45 minutes explanation, 30 demonstration, 15 break, and 90 guided practice.
The checkpoint supports the final presentation; it is not a separate assessment.

Open with the slide “Back at the bubble tea shop” (about 2 minutes, taken from the first block). Ask students one at a time, at random, and leave the question open: do not explain it or connect it to today's topic. The questions continue the Session 1 bubble tea example; reword them before class if you like.

## Prepare before students arrive

- Have Git, Python 3.12, a virtual environment with backend and frontend dependencies,
  Docker with a running engine and Compose v2, curl, a browser, and two terminals.
  Use a POSIX shell (bash/zsh; WSL on Windows). Complete installs and image downloads
  before class: [backend setup](../../docs/setup.md), [frontend setup](../../docs/frontend.md).
  Activate the environment in each terminal; run commands at the repository root.
  With a shared environment, use `PYTHONPATH=backend` for captures/comparisons to
  select this checkout; do not reinstall editable packages across concurrent checkouts.
- Use only [synthetic DM and LB](../../data/synthetic/README.md):
  `data/synthetic/dm.csv` and `data/synthetic/lb.csv`. Keep their bytes and backend
  code fixed across captures. Record `git rev-parse HEAD`, `git status --short`,
  `python --version`, and `python -m pip freeze` beside the captured evidence.
- Check `docker compose version`, `docker compose config --quiet`, and available
  host ports 8000/8501. Stop only known old teaching servers. Build in advance with
  `docker compose build`; rebuild after code, dependency, or bundled-data changes.
  Images copy files; a checkout edit does not update an existing image.
- Open the [actual slide source](../slides/session-4.md), [guided exercise](../exercises/session-4.md),
  [Compose guide](../../docs/compose.md), [comparison commands](../../docs/comparisons.md),
  [frontend walkthrough](../../docs/frontend.md), and [API contract](../../docs/api.md).
  Keep logs and generated captures in ignored `outputs/`; no `.env` is required.

## Provisional run-sheet

Titles below are the actual headings in the [Session 4 slides](../slides/session-4.md).
For practice use the exercise's five phases below. The slide “Break, then 90 minutes
of guided practice” instead proposes 15/20/15/25/15; tell students this delivery uses
the exercise's 20/20/20/20/10 phases, still totaling 90 minutes.

| Clock | Minutes | Actual slide titles / exercise phase | Delivery and observation |
| --- | ---: | --- | --- |
| 0–10 | 10 | “Our 180-minute agenda”; “Trace the complete request” | Trace browser → Streamlit Python → multipart `POST /process` → FastAPI → `stat_core` → JSON → tables/chart. Ask which process makes the API request. |
| 10–20 | 10 | “An image is a recipe's built result”; “Read the two supplied Dockerfiles” | Read both Dockerfiles. Image is the built package; container is its running instance. A venv isolates packages; containers also isolate processes/network and share a host kernel. |
| 20–35 | 15 | “Compose connects two services”; “Addresses depend on who is calling”; “Started is different from ready” | Read ports and service names in Compose; distinguish listening, published addresses, and readiness. Ask students to name the caller before choosing an address. |
| 35–45 | 10 | “The course's three Rs”; “Decide agreement before comparing” | Same conditions twice = repeatability; same process locally/Docker = replicability. Independent simulation is conceptual reproducibility only. Declare exact fields and derived tolerance before running. |
| 45–53 | 8 | “Demo: launch the supplied stack”; “Demo: upload and inspect the results” | Start, check health, upload both files, inspect 24/96/95/1, missing observation, summaries and chart. |
| 53–60 | 7 | “Demo: isolate a connection problem”; “Demo: cause a recoverable local failure”; “Demo: restore the working connection” | Show wrong process-scoped local address and explicit restoration below. Explain how the exercise uses a disposable Compose override for the same diagnosis. |
| 60–75 | 15 | “Demo: capture repeated local outputs”; “Demo: capture the actual Docker run”; “Read the evidence and diagnose disagreement” | Run local twice, then real Docker capture; compare and inspect hashes/environment. |
| 75–90 | 15 | “Break, then 90 minutes of guided practice” | Break; leave commands and exercise visible. |
| 90–110 | 20 | Exercise “0–20 minutes: launch and inspect the working application” | Groups launch, check both health endpoints, upload DM/LB. Confirm counts and missingness. |
| 110–130 | 20 | Exercise “20–40 minutes: trace HTTP and recover a wrong address” | Trace code, check service DNS, apply disposable wrong `BACKEND_URL`, observe failure, restore base Compose frontend. |
| 130–150 | 20 | Exercise “40–60 minutes: capture twice locally and explain agreement” | Run local captures twice; require agreement and unchanged code/input hashes. Ask what null means. |
| 150–170 | 20 | Exercise “60–80 minutes: compare Docker and demonstrate a controlled failure” | Capture inside backend, compare to local; change only generated evidence count, observe exit 1, restore and observe exit 0. |
| 170–180 | 10 | Exercise “80–90 minutes: stopping point and recovery reference”; “Checkpoint and presentation preparation”; “Source map for rehearsal” | Partners explain conditions and evidence; check restored address, preserve captures/logs/SHA, then `docker compose down`. Point to existing presentation preparation. |

## Demo cues and expected observations

Start with `docker compose up --build --wait --wait-timeout 120`; use
`docker compose ps` and `docker compose logs --tail=100 backend frontend`.
Probe API `http://127.0.0.1:8000/health` (expect `{"status":"ok"}`) and Streamlit
`http://127.0.0.1:8501/_stcore/health` (expect `ok`); use the retry command in the
[comparison guide](../../docs/comparisons.md#local-versus-docker) for Streamlit.
Backend `service_healthy` gates frontend startup, not all later requests.

Browser destination is `http://127.0.0.1:8501`; host curl reaches API at port 8000.
Streamlit inside Compose uses `http://backend:8000`: Compose DNS resolves `backend`
on the shared network. Inside frontend, `localhost` refers to frontend itself.
The backend's own health probe legitimately uses its own localhost.
`0.0.0.0` is a listening address, not a browser destination; `EXPOSE` alone does
not publish a host port. Show the internal DNS/HTTP check:

```bash
docker compose exec -T frontend python -c "import urllib.request; print(urllib.request.urlopen('http://backend:8000/health', timeout=5).read().decode())"
```

Open the browser, upload DM as **Participants CSV (DM)** and LB as **Laboratory
CSV (LB)**, then select **Process CSVs**. Expect 24 participants, 96 joined
records, 95 observed, 1 missing; joined records, arm/visit summaries and observed
mean lipoprotein(a) chart in nmol/L. `EDU-LPA-007` at DAY 30 stays unavailable.
Synthetic descriptive values do not establish clinical benefit. A repeated chart
is inspection; formal agreement needs captures.

For the seven-minute local failure demo, stop Compose to free ports. Activate
the same prepared environment in terminals A and B. In A:

```bash
docker compose down
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Confirm host API health, and confirm port 8999 is unused (choose another unused
port if needed). In B, use a one-process override; no source or `.env` edits:

```bash
BACKEND_URL=http://127.0.0.1:8999 python -m streamlit run frontend/app.py --server.address 127.0.0.1 --server.port 8501
```

Reselect both files and process: expect **Could not connect to the backend** and
no successful tables/counts, while API health still succeeds. Stop B with Ctrl-C;
restore explicitly, including after an interrupted demo:

```bash
BACKEND_URL=http://127.0.0.1:8000 python -m streamlit run frontend/app.py --server.address 127.0.0.1 --server.port 8501
```

Reload, upload again and recover 24/96/95/1. Stop both local servers before
restarting Compose. During practice, follow the exercise's disposable override
instead: wrong `http://localhost:8000` inside frontend, then always restore with
`docker compose -f compose.yaml up -d --no-deps --force-recreate frontend`.
That recovery works even if the override shell was lost. Reload and re-upload;
require displayed `Backend: http://backend:8000` and original results.

For the comparison demo, keep inputs and code fixed and run:

```bash
PYTHONPATH=backend python -m stat_core.capture --participants data/synthetic/dm.csv --laboratory data/synthetic/lb.csv --output outputs/local-1.json
PYTHONPATH=backend python -m stat_core.capture --participants data/synthetic/dm.csv --laboratory data/synthetic/lb.csv --output outputs/local-2.json
PYTHONPATH=backend python -m stat_core.comparison outputs/local-1.json outputs/local-2.json
docker compose build
docker compose up -d --wait --wait-timeout 120
docker compose exec -T backend python -m stat_core.capture --participants data/synthetic/dm.csv --laboratory data/synthetic/lb.csv > outputs/docker.json
PYTHONPATH=backend python -m stat_core.comparison outputs/local-1.json outputs/docker.json
```

Expect `Outputs agree` and exit 0 for both comparisons. `-T` keeps terminal
formatting out of redirected JSON. Inspect `result`, `input_sha256`,
`source_sha256`, and `environment`: exact input bytes and backend source hashes
must agree; Python/platform/dependency versions may differ and must be recorded.
For multipart API evidence, use the [existing commands](../../docs/comparisons.md#local-versus-docker):
compare the API result with the capture's `result`, not the metadata wrapper.

Require exact keys, types, lengths/order, IDs, demographics, raw cleaned values,
copied baselines, counts and nulls. Null is neither zero nor an absent field.
Only record `change`, record `percent_change`, and visit-summary `mean` use
`abs(actual - expected) <= max(1e-9, 1e-9 * abs(expected))`, first file as reference.
Absolute units are nmol/L for change/mean and percentage points for percent change;
relative tolerance is dimensionless. This is an engineering rule, not a clinical
threshold. Never round, reorder, fill nulls or widen tolerance to obtain agreement.
Practice's changed `counts.missing` copy should fail with exit 1 and that field
name, then agree after restoration; it demonstrates altered-evidence detection,
not a fresh processing run.

## Likely questions and recovery

| Question / symptom | Explanation and next action |
| --- | --- |
| “Why containers if we have a venv?” | Containers also package user-space system files and isolate processes/network. Neither packaging method proves matching outputs; compare results. |
| “Can the browser use backend?” | Service DNS belongs to the Compose network. Use host port 8501 in the browser, service name from frontend Python. |
| API healthy but upload fails | Health proves availability, not CSV validity or frontend configuration. Check displayed address, frontend DNS/HTTP, then multipart response and logs. A 422 is input rejection; a connection error means the API was not reached. |
| Button disabled or old results disappear | Both uploads are required; changing uploads clears results. Reselect original DM/LB and process again. |
| Docker unavailable / engine stopped | Start the engine and confirm Compose v2. If unavailable, trace source and run local comparisons; label Docker/browser work unverified and rehearse later on a prepared machine. |
| Port occupied / unhealthy startup | Inspect `ps`, logs and known local servers on 8000/8501; stop the conflicting teaching process, check configuration, retry readiness. Do not add arbitrary sleeps. |
| Wrong address persists | Restart local Streamlit with the explicit correct override, or recreate frontend using base Compose as above. Compose explicitly sets its own `BACKEND_URL`; editing local `.env` does not override it. |
| Import fails / captures use another checkout | Activate Python 3.12 with prepared dependencies and run from root with `PYTHONPATH=backend`. Avoid shared editable-install changes. |
| Hashes differ / stale Docker output | Inspect SHA, dirty files and exact CSV bytes, including line endings. Recover intended code/data without discarding student work, rebuild and recapture. |
| Decimal disagrees / null versus zero | Inspect reported field and dependencies/processing; preserve declared tolerance and missingness. Retain originals and failure logs. |
| “Do we need an independent simulation?” | No. Reproducibility is conceptual here; practical evidence covers repeatability and replicability using the course definitions. |

## Rehearsal checklist

- [ ] Time the 45/30/15/90 plan; keep exercise phases and slide titles ready.
- [ ] Verify tools, environment, root directory, SHA, clean/fixed inputs, free ports,
  prebuilt images, and both service health endpoints on the delivery machine.
- [ ] Rehearse browser uploads, 24/96/95/1, missing DAY 30, chart and service DNS.
- [ ] Rehearse wrong local address and exercise override; restore each, re-upload,
  and confirm the working stack even after an interruption.
- [ ] Capture twice locally and once in real Docker; inspect hashes/environment,
  compare results, rehearse generated-count failure and recovery. Preserve actual
  commands, statuses, captures and logs; finish with `docker compose down`.

See [verification](../../docs/verification.md) for recorded checks and the remaining limits to rehearse on the delivery machine.
