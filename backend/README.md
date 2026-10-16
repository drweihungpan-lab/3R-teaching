# Three-R backend

Python 3.12 package for the course's synthetic participant and laboratory CSV example. `stat_core` validates and joins the inputs, preserves missing observations, calculates baseline/change values, and returns deterministic descriptive summaries. `app` exposes the same workflow with FastAPI.

From the repository root, inside a virtual environment:

```bash
python -m pip install -e './backend[dev]'
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Upload DM and LB files through `POST /process`, using multipart file fields `participants` and `laboratory`. `GET /health` checks service readiness, and `/docs` documents the schemas interactively. Python callers use `from stat_core import process_csv` with the two CSV strings.

The repository's `docs/setup.md` and `docs/api.md` contain installation, configuration, complete contracts, validation rules and worked examples. `data/synthetic/` contains the shareable teaching inputs. This is a descriptive engineering example, not a clinical analysis.
