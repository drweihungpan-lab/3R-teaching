# Session 4: An API, containers, and Compose

Put one function behind two interfaces, then run the whole system with one command.

- Add a FastAPI service to your Backend repo.
- Package it in a Docker image.
- Run it with the supplied frontend page using Docker Compose.

---

## Our 170-minute agenda

- 00–10: Back at the bubble tea shop; device example Stages 6 to 7.
- 10–60: Hour one — an API in front of the same function.
- 60–70: Break — 10 minutes.
- 70–130: Hour two — Dockerfile, images, containers, Compose.
- 130–170: Hands-on — run, trace, and fix a controlled fault.

Unfinished practice continues at home. The local-versus-Docker comparison is homework.

---

## Back at the bubble tea shop

**You open a second shop in Hsinchu Science Park. How do you make sure it tastes the same?**

---

## Device example, Stage 6: an API and a page

- A FastAPI endpoint returns each device's predicted limit date. A one-page Streamlit app shows it to someone who does not program.
- It works only on a correctly set-up machine: the right Python, the right packages, and two terminals running at once.

```text
terminal 1: uvicorn app.main:app   (API on port 8000)
terminal 2: streamlit run frontend/app.py   (page on port 8501)
```

---

## Device example, Stage 7: Docker

- Docker Compose starts the API and the page together, with one command.
- Compare the limit dates from a local run and a Docker run, exactly:

```text
local  DEV-C 2026-01-16
docker DEV-C 2026-01-16
MATCH: local and Docker limit dates are identical
```

- Same code and data, a slightly different environment, the same answer: replicability.
- Session 5 recaps all seven stages. Files: the `device-example` folder of the [Sandbox](https://github.com/drweihungpan-lab/3R-sandbox).

---

## One function, two interfaces

```text
command line:  device_limit --input a.csv --output b.csv  ─┐
                                                            ├→ predict_limit_dates
HTTP API:      POST /predict  (a CSV upload)              ─┘
```

- The processing code does not know who called it.
- The API turns a bad upload into a clear HTTP error, not a crash.
- Adding the API does not change what the command-line tool does.

---

## An API is a contract

API means a defined way for programs to communicate. This one has two endpoints.

```text
GET  /health    →  {"status": "ok"}
POST /predict   →  {"devices": [{"device_id": "DEV-A",
                                 "limit_date": "2026-06-30"}, ...]}
```

- The CSV goes in the multipart field named `file`.
- Anything wrong with the upload returns HTTP 422 and a message naming the file and the problem.
- The page you will run later relies on exactly this contract.

---

## Optional dependencies: the api extra

The command-line tool needs only click, numpy and pandas. The API needs more.

```ini
[options.extras_require]
api = fastapi; uvicorn; python-multipart
```

- `pip install .` stays small; `pip install '.[api]'` adds the web server.
- Add `httpx` to the `test` extra so you can test the API with FastAPI's test client.
- The starter files, with the exact lines, are in the Sandbox's `session-4-starter` folder.

---

## Run the API locally first

```bash
pip install -e '.[api,test]'
uvicorn device_limit.api:app --port 8000
curl -F file=@data/device_counts.csv http://127.0.0.1:8000/predict
```

- Visit `http://127.0.0.1:8000/docs` for the interactive page FastAPI generates.
- Send a CSV with a column missing and read the 422 message.
- Only then put it in a container: if it fails locally, it will fail in Docker.

---

## An image is a recipe's built result

- A Dockerfile describes how to assemble an image: Python, dependencies, code, and a startup command.
- An image is a packaged filesystem and defaults; a container is a running instance of it.
- A virtual environment isolates Python packages; containers also supply user-space system files and process/network isolation.
- Containers share a host kernel; packaging alone does not prove matching outputs.
- A build context is the directory Docker can copy from: here, your Backend repo's root.

---

## Read the Dockerfile

```text
FROM python:3.12-slim          start from a small Python image
COPY setup.cfg ... README.md   copy what pip needs to install
COPY src ./src
RUN pip install ".[api]"       install your package and the API extras
CMD uvicorn device_limit.api:app --host 0.0.0.0 --port 8000
```

- Each line is a layer; unchanged layers are reused from cache.
- `0.0.0.0` makes the server reachable from outside the container.
- The file `.dockerignore` keeps `.git`, `.venv` and tests out of the image.

---

## Compose connects two services

A service is a named application component. Compose builds and runs them together.

```text
compose.yaml
  backend:  build .                  (your Dockerfile)
    host 8000 -> container 8000
  frontend: build <3R-frontend git URL>#v1.0.0
    host 8501 -> container 8501
    BACKEND_URL=http://backend:8000
```

- The frontend is built straight from the Frontend repo's pinned tag: the same idea as installing a Release from its git URL.
- Do not edit the frontend; you only configure where it finds the backend.

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
- Inspect the logs instead of adding an arbitrary sleep.

---

## Demo: add the API and run it

Copy the starter files, add the `api` extra, then:

```bash
pip install -e '.[api,test]'
uvicorn device_limit.api:app --port 8000
```

In another terminal:

```bash
curl -F file=@data/device_counts.csv http://127.0.0.1:8000/predict
```

Expect the three limit dates from last session.

---

## Demo: run both services

```bash
docker compose up --build
```

- Open `http://localhost:8501` and upload `data/device_counts.csv`.
- The table shows the same three limit dates as your `limits.csv`.
- Stop with `Ctrl+C`, then `docker compose down`.

---

## Demo: a controlled connection fault

In `compose.yaml`, change the frontend's `BACKEND_URL` to `http://backend:8001`, then restart:

```bash
docker compose up --build
```

The page now says it could not connect to the backend at that address.

- Which line of the message names the wrong address?
- Fix the port, restart, and upload again.
- Check the logs of each service: `docker compose logs backend frontend`.

---

## The course's three Rs

- Repeatability: agreement across successive runs under the same conditions; run locally twice.
- Replicability: agreement under slightly different conditions; compare local Python with Docker.
- Reproducibility: agreement under very different conditions, such as independent simulation; discussed conceptually here.
- Keep code and CSV unchanged across captures. Record environment differences.
- The [course glossary](../../GLOSSARY.md) governs these meanings.

---

## Homework preview: compare local and Docker

Decide what must agree before you compare.

- The limit dates are whole days, so they are compared exactly.
- Run the command-line tool locally and send the same CSV to the API running in Docker.
- Compare the dates from `limits.csv` with the API's JSON, and write down the result.
- If they differ, record Python and library versions for both before changing anything.

Details of the homework will be posted separately.

---

## Hands-on: 40 minutes

- 10 minutes: copy the starter files, run the API locally, send a CSV with `curl`.
- 10 minutes: `docker compose up --build`, upload in the page, compare with `limits.csv`.
- 15 minutes: the controlled connection fault — find it from the page message and the logs, then fix it.
- 5 minutes: record what worked in your README.

Use [the exercise](../exercises/session-4.md) when stuck.

---

## Checkpoint and presentation preparation

Today's checkpoint: both services run together from your Backend repo.

- Mandatory homework is approximately two hours; includes the local-versus-Docker comparison.
- Prepare to demonstrate startup, an upload, your tests and CI, and Releases in Session 5.
- Keep links to your pull requests, reviews, and CI runs ready.

See the [syllabus](../../SYLLABUS.md) and the [final presentation checklist](../assessment/final-presentation.md).
