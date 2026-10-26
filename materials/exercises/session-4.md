# Session 4 guided practice: run the API and both services

Spend about 40 minutes in your group of three or four, in your **Backend repo**. You will add the supplied API files, run the API locally, start both services with Docker Compose, and diagnose a controlled connection fault. Docker Desktop (with the WSL backend on Windows) must be installed and running; check with `docker version`. The frontend page is supplied: you configure it, you do not edit it.

## Before you start

Be on an updated `main` with the `.venv` active, then branch:

```bash
git switch main
git pull --ff-only origin main
git switch -c session-4/your-name-api
```

Get the starter files from the `session-4-starter` folder of the [Sandbox](https://github.com/drweihungpan-lab/3R-sandbox) and follow its README to copy `api.py`, `Dockerfile`, `compose.yaml` and `.dockerignore`. These are the defaults `device_limit` and `model`; adjust the import in `api.py` if your group chose other names.

| Time | Activity | Checkpoint |
| --- | --- | --- |
| 0–10 min | Add the `api` extra, run the API, `curl` a CSV | JSON with three limit dates |
| 10–20 min | `docker compose up --build`, upload in the page | The page's table matches `limits.csv` |
| 20–35 min | The controlled connection fault | Found from the message and logs, fixed |
| 35–40 min | Record | Notes in the README |

## 1. Run the API locally — 10 minutes

In `setup.cfg`, add under `[options.extras_require]`:

```ini
api = fastapi; uvicorn; python-multipart
```

and add `httpx` to the `test` line. Then:

```bash
pip install -e '.[api,test]'
uvicorn device_limit.api:app --port 8000
```

In a second terminal at the same folder:

```bash
curl http://127.0.0.1:8000/health
curl -F file=@data/device_counts.csv http://127.0.0.1:8000/predict
```

Expect `{"status":"ok"}`, then three devices with limit dates. Send a CSV with the `daily_count` column removed and read the HTTP 422 message. Stop the server with `Ctrl+C` before the next step, because both use port 8000.

## 2. Run both services — 10 minutes

```bash
docker compose up --build
```

The first build downloads images and the Frontend repo and can take a few minutes. Open <http://localhost:8501>, upload `data/device_counts.csv`, and select **Send to backend**. Compare the table with your `limits.csv`. In another terminal, `docker compose ps` should show the backend as healthy. Stop with `Ctrl+C`, then `docker compose down`.

## 3. A controlled connection fault — 15 minutes

In `compose.yaml` change the frontend's `BACKEND_URL` from `http://backend:8000` to `http://backend:8001`, then run `docker compose up --build` again and upload. The page reports that it could not connect to the backend at that address.

1. Which part of the message names the wrong address?
2. Run `docker compose logs backend frontend`. Which service logged a problem, and which did not?
3. Why does `localhost:8000` inside the frontend container not reach the backend?

Restore the port, restart, and confirm the upload works.

## 4. Record — 5 minutes

Add a short note to your README: how to start both services, and what the fault looked like. Commit and push the branch, open a PR, and request a teammate's review.

## Checkpoint

Both services run together from your Backend repo. The local-versus-Docker comparison is part of the homework; keep your `limits.csv` and the API's JSON for it. Finish anything unfinished at home, in addition to the homework.
