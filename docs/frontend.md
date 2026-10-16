# Local Streamlit frontend

The supplied interface sends two CSV files to FastAPI and displays the returned results. All joining, validation, baseline/change calculations and summaries happen in the backend. The frontend does not import `stat_core`. This is a complete teaching example; students can inspect and modify it without finishing missing UI code.

## Install and start

Use Python 3.12 and run commands from the repository root. Follow [backend setup](setup.md) to create and activate a virtual environment and install the backend. In that same environment, install the frontend dependencies:

```bash
python -m pip install -r frontend/requirements.txt
```

Keep the backend running in one terminal:

```bash
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

In a second terminal, activate the same environment, return to the repository root and start Streamlit:

```bash
python -m streamlit run frontend/app.py --server.address 127.0.0.1 --server.port 8501
```

Open <http://127.0.0.1:8501>. The browser connects to Streamlit; the Streamlit Python process sends HTTP requests to FastAPI. The frontend dependencies are declared in [requirements.txt](../frontend/requirements.txt). Version ranges are supplied rather than a resolved lockfile; record installed versions with `python -m pip freeze` when comparing environments.

## Configuration

Defaults work without a `.env` file. If you do not already have one, copy [.env.example](../.env.example) to `.env` in the repository root and edit the frontend settings:

```dotenv
BACKEND_URL=http://127.0.0.1:8000
REQUEST_TIMEOUT=30
```

`BACKEND_URL` is the API base address without `/process`. `REQUEST_TIMEOUT` is a finite, positive number of seconds for HTTP connection/read inactivity, not a total processing deadline. The frontend loads the root `.env` relative to `frontend/app.py`; exported environment variables take precedence. Restart Streamlit after changing settings. Keep `.env` out of Git.

If the backend uses a different port, update `BACKEND_URL`. For later Docker Compose use, the frontend service addresses the backend service as `http://backend:8000`; `localhost` inside a frontend container refers to that frontend container. The browser still uses the frontend's published host port. Container setup is a separate task.

## Demonstrate the supplied data

1. Select [data/synthetic/dm.csv](../data/synthetic/dm.csv) under **Participants CSV (DM)** and [data/synthetic/lb.csv](../data/synthetic/lb.csv) under **Laboratory CSV (LB)**. These are [synthetic teaching data](../data/synthetic/README.md), not real patient records.
2. Select **Process CSVs**, which becomes available after both files are selected. Streamlit sends `POST /process` with multipart fields `participants` and `laboratory`, as described in the [API contract](api.md).
3. Check the four displayed counts: **24 participants, 96 joined records, 95 observed, 1 missing**. Inspect the joined records: the first `subject_id` remains `001`; its baseline and value are 167.0 with zero change. The missing DAY 30 observation for `EDU-LPA-007` stays unavailable, not zero.
4. Inspect the two arm summaries and eight visit summaries. Both arms contain 12 participants. Investigational A at DAY 30 has 11 observed results and one missing result.
5. Inspect the simple mean chart: study day on the horizontal axis, observed mean lipoprotein(a) in nmol/L on the vertical axis, with a line for each arm and separate panels for studies. It plots the backend's visit means, without recomputing them. An all-missing group has no mean. These descriptive values do not establish treatment effects or clinical benefit.
6. Process the same uploads again to demonstrate the same visible results. Selecting or removing an upload clears the previous display; select **Process CSVs** again to obtain results for the current files. The separate output-comparison task supplies formal repeatability and replicability evidence.

## Demonstrate errors

Use a copy of DM, change an `AGE` cell to `not-a-number`, and upload it with the original LB. The page shows HTTP 422 with the file (`participants`), CSV row (header = 1), field (`AGE`), and backend repair message. Restore the original file and process again. Do not edit the repository's sample data. Oversized uploads rejected by the API show HTTP 413 with the same location details; `MAX_UPLOAD_BYTES` is a backend setting documented in [setup.md](setup.md).

For a connection demonstration, point `BACKEND_URL` to an unused local port, restart Streamlit, and submit both files. The message asks you to start the API and check the address. Restore the correct address and restart. A request that exceeds `REQUEST_TIMEOUT` asks you to check API readiness and retry or increase the timeout. A non-JSON response reports its HTTP status and asks you to check that the address points to FastAPI. Invalid configuration shows a repair message before uploads are enabled. Failed requests show no result tables or success counts.

Streamlit also has its own upload size limit. For this small example the backend's default per-file limit is 5 MiB, below Streamlit's default. A browser-side upload rejection happens before an HTTP request reaches FastAPI.
