# Session 4 instructor notes: an API, containers, and Compose

Hour one adds a FastAPI service to the Backend repo; hour two adds the Dockerfile and runs both services with Docker Compose, using the supplied Frontend repo. Use the [slides](../slides/session-4.md), [guided exercise](../exercises/session-4.md), and the [glossary](../../GLOSSARY.md). The local-versus-Docker comparison is homework.

## Prepare before class

- Students need Docker Desktop (WSL backend on Windows) running; check `docker version` in the first minutes. Large first builds need network access: pre-pull `python:3.12-slim` on the classroom machines if the network is slow.
- The Frontend repo must be published with the tag `v1.0.0` that `compose.yaml` pins to. Confirm `docker compose build` works from a clean machine.
- The starter files are in the Sandbox's `session-4-starter` folder (`api.py`, `Dockerfile`, `compose.yaml`, `.dockerignore`, README). They assume the default package names; students with other names must edit the import.
- Rehearse the full path on a fresh repo: copy the files, add the `api` extra, run the API with `curl`, then `docker compose up --build`, an upload, the controlled fault, and the fix. Free ports 8000 and 8501 on every machine.

## 170-minute run sheet

| Clock | Mode | Slides | Delivery |
| --- | --- | --- | --- |
| 0–10 | Opening | Back at the bubble tea shop; Device example, Stage 6; Stage 7 | Second shop, same tea? Then Stages 6 → 7. |
| 10–60 | Explanation | One function, two interfaces; An API is a contract; Optional dependencies: the api extra; Run the API locally first | Hour one. Keep the API short: two endpoints and the 422 behaviour. |
| 60–70 | Break | | 10 minutes. |
| 70–100 | Explanation | An image is a recipe's built result; Read the Dockerfile; Compose connects two services; Addresses depend on who is calling; Started is different from ready | Hour two. Stress service names inside Compose versus `localhost`. |
| 100–130 | Demonstration | Demo: add the API and run it; Demo: run both services; Demo: a controlled connection fault | Perform all three live, including the wrong `BACKEND_URL` port and reading the logs. |
| 130–170 | Hands-on | The course's three Rs; Homework preview; Hands-on: 40 minutes; Checkpoint | Show the two practical-R slides briefly, then [exercise](../exercises/session-4.md) §§1–4. |

## Cues and expected observations

- `curl -F file=@data/device_counts.csv http://127.0.0.1:8000/predict` returns three devices with the dates from Session 2; a CSV missing `daily_count` returns HTTP 422 naming the file and the column.
- The page at <http://localhost:8501> shows the same table as `limits.csv`. With the wrong port, it reports that it could not connect to the backend at the configured address.
- Common failures: port 8000 still held by a local `uvicorn`; Docker not running; a first build that appears stuck; the API extra missing from `setup.cfg`; editing the frontend by mistake.

## Rehearsal checklist

- [ ] The Frontend repo tag exists and builds from its git URL.
- [ ] `docker compose up --build` shows both services and a healthy backend.
- [ ] The fault and its fix work as written.
- [ ] The homework preview matches the comparison you will assign.
