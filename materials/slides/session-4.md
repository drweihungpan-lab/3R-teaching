# Session 4: Containers and output comparisons

- Follow CSV uploads through the supplied Streamlit and FastAPI services.
- Explain container addresses, startup, and recoverable connection failures.
- Compare repeated local runs and local/Docker results using declared rules.
- Use the complete synthetic example; focus on engineering workflow.

---

## Back at the bubble tea shop

**You open a second shop in Hsinchu Science Park. How do you make sure it tastes the same?**

---

## Our 180-minute agenda

- 0–45: explanation — request flow, images, networking, readiness, agreement.
- 45–75: demonstration — launch 8, diagnose/recover 7, compare outputs 15 minutes.
- 75–90: break — 15 minutes.
- 90–180: guided practice — trace 15, run 20, recover 15, compare 25, review 15 minutes.
- Timings are provisional; see the [syllabus](../../SYLLABUS.md).

---

## Trace the complete request

HTTP is the request/response protocol connecting these programs. Multipart means one request contains named file parts.

```text
Browser -> Streamlit Python: upload DM and LB
Streamlit -> FastAPI: POST /process
  multipart fields: participants, laboratory
FastAPI -> stat_core.process_csv: validate, join, summarize
FastAPI -> Streamlit: JSON result
Streamlit -> Browser: counts, records, summaries, chart
```

- Streamlit displays backend results; it does not import `stat_core`.
- Trace [frontend code](../../frontend/app.py), [API code](../../backend/app/main.py), and the [contract](../../docs/api.md).

---

## An image is a recipe's built result

- A Dockerfile describes how to assemble an image: Python, dependencies, code, and a startup command.
- An image is a packaged filesystem and defaults; a container is a running instance of it.
- A virtual environment isolates Python packages; containers also supply user-space system files and process/network isolation.
- Containers share a host kernel; packaging alone does not prove matching outputs.
- A build context is the directory Docker can copy from: here, the repository root.

---

## Read the two supplied Dockerfiles

- Both start from `python:3.12-slim`, a small Python base image.
- [Backend Dockerfile](../../backend/Dockerfile): copies `app`, `stat_core`, and package metadata; installs the package and includes synthetic CSVs.
- Backend starts Uvicorn, the API server, on `0.0.0.0:8000`.
- [Frontend Dockerfile](../../frontend/Dockerfile): installs `frontend/requirements.txt`, copies `frontend/app.py`, and starts Streamlit on `0.0.0.0:8501`.
- `0.0.0.0` listens on all container interfaces; it is not the browser destination.
- `EXPOSE` documents an internal port. Compose publishes a port to the host.

---

## Compose connects two services

A service is a named application component. Compose builds and runs the supplied services together.

```text
compose.yaml
  backend: root context, backend/Dockerfile
    host 127.0.0.1:8000 -> container 8000
  frontend: root context, frontend/Dockerfile
    host 127.0.0.1:8501 -> container 8501
    BACKEND_URL=http://backend:8000
```

- Read [compose.yaml](../../compose.yaml): `ports` maps host to container ports.
- These host bindings accept connections from this computer only.

---

## Addresses depend on who is calling

- Browser on host → Streamlit: `http://127.0.0.1:8501`.
- Host curl → API: `http://127.0.0.1:8000`.
- Streamlit inside Compose → API: `http://backend:8000`.
- Backend health probe → itself: `http://127.0.0.1:8000/health`.
- DNS means looking up an address by name. Compose resolves service name `backend` on its shared network.
- `localhost` means the caller's own network environment. Inside frontend, it points to frontend; the host browser cannot resolve Compose service names.
- See [address and troubleshooting guide](../../docs/compose.md).

---

## Started is different from ready

- `GET /health` returning `{"status":"ok"}` says the API is available, not that uploaded data are valid.
- The backend healthcheck probes that endpoint inside its container.
- Frontend `depends_on` uses `condition: service_healthy`: wait for backend health before starting frontend.
- This startup gate does not guarantee later backend availability or restart frontend after a later failure.
- Check Streamlit readiness separately at `/_stcore/health`; inspect logs instead of adding an arbitrary sleep.

---

## The course's three Rs

- Repeatability: agreement across successive runs under the same conditions; run locally twice.
- Replicability: agreement for the same process under slightly different conditions; compare local Python with Docker.
- Reproducibility: agreement under very different conditions, such as independent simulation; discussed conceptually here.
- Keep code and CSV bytes unchanged across captures. Record environment differences.
- The [course glossary](../../GLOSSARY.md) governs these meanings; terminology varies by discipline.

---

## Decide agreement before comparing

- Exact: structure, types, list order, identifiers, raw cleaned values, copied baselines, counts, and nulls.
- A missing value is `null`, never zero; a missing field is not a null field.
- Only record `change`, `percent_change`, and visit-summary `mean` use tolerance in both comparisons.

```text
abs(actual - expected) <= max(1e-9, 1e-9 * abs(expected))
```

- First file is the reference. Relative tolerance has no unit; absolute tolerance is nmol/L for change/mean, percentage points for percentage change.
- This engineering rule is not a clinical threshold. See [comparison rules](../../docs/comparisons.md).

---

## Demo: launch the supplied stack

Use a running Docker engine and Compose v2. All commands start at the repository root; activate Python 3.12 from [setup](../../docs/setup.md) for later local captures.

```bash
docker compose version
docker compose config --quiet
docker compose up --build
```

In a second terminal at the same root:

```bash
docker compose ps
curl --fail-with-body http://127.0.0.1:8000/health
```

- Expect backend `healthy`. Keep the first terminal open for logs.

---

## Demo: upload and inspect the results

- Open `http://127.0.0.1:8501`; displayed backend should be `http://backend:8000`.
- Upload [dm.csv](../../data/synthetic/dm.csv) as Participants CSV (DM) and [lb.csv](../../data/synthetic/lb.csv) as Laboratory CSV (LB).
- Select Process CSVs: expect 24 participants, 96 joined records, 95 observed, 1 missing.
- Inspect joined records, arm/visit summaries, and the observed mean chart in nmol/L.
- `EDU-LPA-007` at DAY 30 stays unavailable. Synthetic descriptive results do not establish clinical benefit.
- Repeating a chart is useful inspection; use captured outputs for formal agreement evidence. See [frontend walkthrough](../../docs/frontend.md).

---

## Demo: isolate a connection problem

First check the API independently of Streamlit:

```bash
curl --fail-with-body http://127.0.0.1:8000/process \
  -F participants=@data/synthetic/dm.csv \
  -F laboratory=@data/synthetic/lb.csv
docker compose logs --tail=100 backend frontend
docker compose exec frontend python -c \
  "import urllib.request; print(urllib.request.urlopen('http://backend:8000/health', timeout=2).read().decode())"
```

- Host health succeeds but internal request fails: inspect service name, port, and shared Compose project.
- A 422 response means input rejection; a connection error means the request could not reach the API.

---

## Demo: cause a recoverable local failure

Stop Compose to free ports, then start the local backend in terminal A. Use the activated environment with frontend dependencies from [local setup](../../docs/frontend.md).

```bash
docker compose down
python -m uvicorn app.main:app --app-dir backend \
  --host 127.0.0.1 --port 8000
```

In terminal B, first confirm port 8999 is unused; if occupied, choose another unused port. Apply this override to this one process only:

```bash
BACKEND_URL=http://127.0.0.1:8999 \
python -m streamlit run frontend/app.py \
  --server.address 127.0.0.1 --server.port 8501
```

- Submit both files: expect “Could not connect to the backend.” No source or `.env` edits are needed.

---

## Demo: restore the working connection

Stop the failing Streamlit process with Ctrl-C in terminal B; restart with the correct address:

```bash
BACKEND_URL=http://127.0.0.1:8000 \
python -m streamlit run frontend/app.py \
  --server.address 127.0.0.1 --server.port 8501
```

- Upload again: expect 24/96/95/1 and visible results. The original shell and `.env` settings were never changed.
- Stop both local servers with Ctrl-C before restarting Compose on those ports.
- Compose explicitly sets `http://backend:8000`; changing local `.env` cannot override that service setting.
- Restore by restarting the process with the right address; do not commit a broken configuration.

---

## Demo: capture repeated local outputs

Use the same checkout, unchanged CSVs, and activated Python environment. Backslashes continue one shell command across readable lines.

```bash
PYTHONPATH=backend python -m stat_core.capture \
  --participants data/synthetic/dm.csv \
  --laboratory data/synthetic/lb.csv \
  --output outputs/local-1.json
PYTHONPATH=backend python -m stat_core.capture \
  --participants data/synthetic/dm.csv \
  --laboratory data/synthetic/lb.csv \
  --output outputs/local-2.json
PYTHONPATH=backend python -m stat_core.comparison \
  outputs/local-1.json outputs/local-2.json
```

- Expect `Outputs agree`, exit code 0. Captures call the public `process_csv`; generated `outputs/` is ignored.

---

## Demo: capture the actual Docker run

Stop local servers first; keep the two local captures. Rebuild after code, dependency, or bundled data changes: these images copy files and do not live-update from the checkout.

```bash
docker compose build
docker compose up -d --wait --wait-timeout 120
curl --fail-with-body http://127.0.0.1:8000/health
curl --fail-with-body --retry 20 --retry-all-errors \
  --retry-delay 2 http://127.0.0.1:8501/_stcore/health
docker compose exec -T backend python -m stat_core.capture \
  --participants data/synthetic/dm.csv \
  --laboratory data/synthetic/lb.csv > outputs/docker.json
PYTHONPATH=backend python -m stat_core.comparison \
  outputs/local-1.json outputs/docker.json
```

- Expect `Outputs agree`, exit code 0. `-T` disables terminal formatting for redirected JSON. Full [capture/API commands](../../docs/comparisons.md) include a multipart result comparison.

---

## Read the evidence and diagnose disagreement

- Each capture has `result` plus metadata: Python, platform, dependency versions, and SHA-256 hashes of code and exact CSV bytes.
- A hash is a file fingerprint. Code/data hashes must agree; inspect expected environment differences separately.
- Results preserve stable ordering; comparison does not sort, round, or replace nulls to force agreement.
- Nonzero exit and a field such as `counts.missing` locate a disagreement. Hash mismatch: recover matching code/data and rebuild.
- Derived decimal outside tolerance: investigate processing/dependencies; keep the declared tolerance.
- Keep captures and logs together; a chart or passing unrelated test alone does not establish agreement.

---

## What has actually been verified?

- [Remote Docker CI run 38876609585](https://github.com/drweihungpan-lab/3R-teaching/actions/runs/38876609585) completed successfully for commit `c5fc92a37ec660492c7238f55f88b023a9200775`.
- Its Docker output comparison job builds real images, checks readiness and service DNS/HTTP, compares local/container captures, and compares multipart API results.
- This is evidence for that commit and environment; rerun for later changes. The [workflow](../../.github/workflows/backend-tests.yml) retains available evidence for seven days.
- Docker is absent on the slide-authoring host: local captures can be checked there; container execution and browser behavior cannot be claimed from those checks.
- PowerPoint rendering is also unverified here. Markdown is maintained for the [editable converter](README.md).

---

## Break, then 90 minutes of guided practice

- Take a 15-minute break before practice.
- 15 minutes: trace uploads, HTTP, `stat_core`, and each caller's address.
- 20 minutes: launch the supplied stack, upload both CSVs, inspect health and logs.
- 15 minutes: repeat the temporary local address failure and recovery; restore a working stack.
- 25 minutes: capture twice locally and once in Docker; compare and explain exact fields, nulls, and tolerance.
- 15 minutes: review a teammate's commands and evidence; explain code/data hashes and any environment differences.
- Use the supplied framework and your group's declared behavior; UI polish and model complexity are not priorities.

---

## Checkpoint and presentation preparation

- Explain images versus containers, internal versus published ports, and startup readiness.
- Show working uploads, restored configuration, and matching comparison outputs; retain commands, conditions, captures, and logs.
- Finish the demonstration with `docker compose down`; host CSVs and built images remain.
- Mandatory homework: about two hours rehearsing application startup, validation, tests, comparisons, and navigation to PR/review evidence.
- Every student needs an authored PR and meaningful peer review. Prepare for the final presentation's pass/fail engineering checks.
- This checkpoint is preparation, not a separate assessed submission. Final presentation has no resubmission or reassessment; see [assessment policy](../../SYLLABUS.md#assessment-policy).

---

## Source map for rehearsal

- [Course specification](../../docs/specs/course-framework-and-teaching-materials.md), [syllabus](../../SYLLABUS.md), and [three-R glossary](../../GLOSSARY.md).
- [Local frontend and recovery](../../docs/frontend.md), [Compose operation](../../docs/compose.md), and [output capture/comparison commands](../../docs/comparisons.md).
- [Backend image](../../backend/Dockerfile), [frontend image](../../frontend/Dockerfile), and [service configuration](../../compose.yaml).
- [Synthetic input provenance](../../data/synthetic/README.md) and [API contract](../../docs/api.md).
- [Session 4 authoring ticket](../../docs/tickets/16-session-4-markdown-slides.md) and [supported slide Markdown](README.md).
