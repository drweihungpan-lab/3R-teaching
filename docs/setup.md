# Local backend setup

Use Python 3.12. Run these commands from the repository root. No neighboring data repository or external service is required.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e './backend[dev]'
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` instead. The `dev` extra installs pytest and the HTTP test client; processing/service use alone needs only `python -m pip install -e ./backend`. An editable install makes changes under `backend/` available immediately; reinstall when dependency metadata changes. The distribution is named `three-r-backend`; the import packages are `stat_core` and `app`. Dependency ranges are declared in [backend/pyproject.toml](../backend/pyproject.toml). A resolved lockfile is not supplied; record installed versions alongside environment comparison evidence, for example with `python -m pip freeze`.

## Configuration

Defaults work without a `.env` file. To try local settings:

```bash
cp .env.example .env
```

Edit `.env` in the repository root, then restart the service. `python-dotenv` reads this exact file from the working directory when the application is created; exported environment variables take precedence. The reusable processing function does not load configuration.

| Setting | Default | Used for |
| --- | --- | --- |
| `LOG_LEVEL` | `INFO` | Processing log level: DEBUG, INFO, WARNING, ERROR or CRITICAL |
| `MAX_UPLOAD_BYTES` | `5242880` | Positive integer byte limit for each uploaded CSV; oversized files return 413 |

Invalid settings fail service startup with a clear error. `.env` is ignored by Git; `.env.example` is safe to share. These settings contain no credentials. Processing logs show counts and validation locations, not uploaded rows. The example uses synthetic data only.

## Run and check the API

```bash
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Keep this terminal running. In another terminal, from the same repository root:

```bash
curl --fail-with-body http://127.0.0.1:8000/health
curl --fail-with-body http://127.0.0.1:8000/process \
  -F participants=@data/synthetic/dm.csv \
  -F laboratory=@data/synthetic/lb.csv
```

The health response is `{"status":"ok"}`. Processing returns counts of 24 participants, 96 records, 95 observed and one missing, plus joined records and arm/visit summaries. Open <http://127.0.0.1:8000/docs> to upload the same two files interactively. The [API contract](api.md) documents every response field, validation rule and error format. If port 8000 is occupied, choose another `--port` and update the request address.

The `--app-dir backend` option makes `backend/app` importable when starting from the root. Keep the root as the working directory so `.env` resolves consistently. For a later container service, bind to `--host 0.0.0.0`; other containers use the Compose service address such as `http://backend:8000`, while host tools use the published localhost port. See [Compose](compose.md) for the container configuration.

## Call processing without HTTP

After the editable install, run from the repository root:

```bash
python - <<'PY'
from pathlib import Path
from stat_core import process_csv

result = process_csv(
    Path("data/synthetic/dm.csv").read_text(encoding="utf-8"),
    Path("data/synthetic/lb.csv").read_text(encoding="utf-8"),
)
print(result["counts"])
PY
```

Expected: `{'participants': 24, 'records': 96, 'observed': 95, 'missing': 1}`. For a source-only check without installing the package, prefix the command with `PYTHONPATH=backend` on macOS/Linux. The package uses the Python standard library for CSV processing and Pydantic for output schemas; pandas is not needed for this small example.

## Validation and downstream work

Try a copy of DM with AGE changed to `not-a-number`, or an LB copy with units changed to `mg/dL`. `/process` returns 422 with a file, CSV line, field and repair message. Missing results remain null; they never become zero. An unavailable baseline produces null changes, and zero baseline produces null percentage change. See [api.md](api.md) for full rules and worked values.

See [testing](testing.md) for the pytest suite and how to run it.
