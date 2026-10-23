# Compare processing outputs

Under the [course definitions](../GLOSSARY.md), **repeatability** means matching
successive runs under the same conditions. **Replicability** means matching the
same process under slightly different conditions: here, a local Python virtual
environment and Docker. Reproducibility under very different conditions is a
discussion topic; no independent simulation is required.

Use the unchanged [synthetic inputs](../data/synthetic/README.md) and the same
checkout for every capture. Finish code/data edits before capturing; rebuild
images after edits. The commands below run the actual public `process_csv`
function and preserve its stable order: records by study, participant, study day,
sequence; arm summaries by study/arm; visit summaries by study/arm/day/visit.

## Repeated local runs

From the repository root, activate the Python 3.12 environment from
[setup](setup.md). `PYTHONPATH=backend` explicitly selects this checkout even if
the environment is shared with another checkout.

```bash
PYTHONPATH=backend python -m stat_core.capture --participants data/synthetic/dm.csv --laboratory data/synthetic/lb.csv --output outputs/local-1.json
PYTHONPATH=backend python -m stat_core.capture --participants data/synthetic/dm.csv --laboratory data/synthetic/lb.csv --output outputs/local-2.json
PYTHONPATH=backend python -m stat_core.comparison outputs/local-1.json outputs/local-2.json
```

Expect `Outputs agree` and exit code 0. The supplied data yield 24 participants,
96 records, 95 observed results, and one missing result. Open the JSON files to
inspect all records and summaries. Omit `--output` to emit JSON to stdout.
Generated evidence stays in ignored `outputs/`.

Each capture separates `result` from metadata: SHA-256 hashes of exact CSV bytes
(including line endings) and backend `.py` sources, plus Python, platform, and
installed dependency versions. Source names are relative to the backend package
root, so different installation paths do not cause false mismatches. Hashes
must match; environment descriptions may differ and must be inspected when
reporting the conditions. There are no timestamps or random IDs in the result.
Hashes identify the files captured, not proof against a deliberately edited
evidence file. Preserve the capture and CI logs together.

## Local versus Docker

Keep the local captures above. With a working Docker engine and Compose v2,
follow [Compose setup](compose.md), then run from this same checkout:

```bash
docker compose build
docker compose up -d --wait --wait-timeout 120
curl --fail-with-body http://127.0.0.1:8000/health
curl --fail-with-body --retry 20 --retry-all-errors --retry-delay 2 http://127.0.0.1:8501/_stcore/health
docker compose exec -T frontend python -c "import urllib.request; print(urllib.request.urlopen('http://backend:8000/health', timeout=5).read().decode())"
docker compose exec -T backend python -m stat_core.capture --participants data/synthetic/dm.csv --laboratory data/synthetic/lb.csv > outputs/docker.json
PYTHONPATH=backend python -m stat_core.comparison outputs/local-1.json outputs/docker.json
```

The backend image already includes these exact CSVs and the capture module;
no host Python script or simulated container is used. Compose waits for backend
health and frontend startup; the frontend health request checks Streamlit
readiness. The command inside frontend checks that `backend` resolves and the
API responds over the Compose network. It does not exercise the browser UI.

Also check real multipart uploads through the published API:

```bash
curl --fail-with-body http://127.0.0.1:8000/process -F participants=@data/synthetic/dm.csv -F laboratory=@data/synthetic/lb.csv --output outputs/api-result.json
PYTHONPATH=backend python - <<'PY'
import json
from pathlib import Path
from stat_core.comparison import compare_results
local = json.loads(Path('outputs/local-1.json').read_text())
api = json.loads(Path('outputs/api-result.json').read_text())
compare_results(local['result'], api)
print('Real multipart API output agrees with the local processing result.')
PY
docker compose down
```

The API returns `ProcessResult`, so this comparison uses the result seam directly,
without pretending the HTTP response contains capture metadata.

## Agreement rules and failure diagnosis

Both public comparison functions validate the existing
[`ProcessResult` schema](../backend/stat_core/schemas.py), including finite
numbers and forbidden extra fields. Every field must be present, even optional
fields containing null. Keys, list lengths/order, types, identifiers, joined
demographics, raw cleaned values, copied baselines, counts, and nulls match
exactly. A boolean is not an integer; a missing value is never zero. Comparison
does not reorder, round, drop fields, or replace missing values to pass.

Only record `change`, record `percent_change`, and visit-summary `mean` use the
same rule as [the backend tests](testing.md):
`abs(actual - expected) <= max(1e-9, 1e-9 * abs(expected))`. The first file is the
reference. Absolute tolerance is in nmol/L for change/mean and percentage points
for percentage change; relative tolerance is dimensionless. This accommodates
tiny floating-point variation in the example, not a clinical threshold.

Mismatch, malformed capture, missing file, NaN, or Infinity gives a nonzero
exit code and an error on stderr. Errors identify the field, such as
`records[0].participant_id` or `counts.missing`. Different hashes mean code/data
conditions changed: recover the same checkout/inputs and rebuild before trying
again. A decimal outside tolerance requires investigating processing/dependency
changes; do not widen tolerance to disguise it. Public Python callers receive
`ValueError` on failure and `None` on success.

To demonstrate a controlled mismatch, copy `outputs/local-2.json` to an ignored
`outputs/changed.json`, change `result.counts.missing` from 1 to 0, and compare
against `outputs/local-1.json`. Expect exit code 1 with `counts.missing`. Restore
the original capture to recover. The focused
[comparison tests](../backend/tests/test_comparison.py) also demonstrate wrong
IDs/counts, raw/baseline perturbations, null versus zero, types, structure/order,
derived values inside/outside tolerance, differing hashes, and CLI failures.

## Evidence from CI

The [GitHub Actions workflow](../.github/workflows/backend-tests.yml) runs
**Docker output comparison** on pull requests and configured branch pushes. It
builds both real images, starts Compose, checks both health endpoints and
frontend-to-backend DNS/HTTP, captures local and container results, and compares
a real multipart API response. Its `output-comparison-evidence` artifact retains
captures, comparison outputs, health responses, Compose status, and logs for seven
days, including diagnostics after failure. A successful run supplies real Docker
evidence; passing local pytest alone does not.
