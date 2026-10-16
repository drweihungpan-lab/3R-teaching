# Backend tests

The suite checks the declared [processing and API contract](api.md). It checks
engineering behavior, not clinical conclusions or the course's final assessment.

## Run locally

Use Python 3.12 and the backend development dependencies from [setup](setup.md).
From the repository root, with that virtual environment active:

```bash
python -m pytest backend/tests
```

[backend/pytest.ini](../backend/pytest.ini) puts the local backend on Python's
import path. To explicitly select this checkout when sharing an environment:

```bash
PYTHONPATH=backend python -m pytest backend/tests
```

There is no server, network listener, database, or Docker prerequisite for this
suite. HTTP tests send real multipart requests through FastAPI's in-process
`TestClient`. They configure `MAX_UPLOAD_BYTES` and `LOG_LEVEL` through environment
variables, so a personal `.env` cannot change the tested upload limit.

## Fixtures and coverage

[conftest.py](../backend/tests/conftest.py) reads the unchanged
[synthetic inputs](../data/synthetic/README.md) and supplies a small independent
example. It defines its own CSV fields and records, without importing production
parsers, field lists, or calculation helpers.

- [Processing tests](../backend/tests/test_processing.py) check exact supplied
  counts (24 participants, 96 records, 95 observed, one missing), all raw source
  records, joined demographics, leading zeros, and visit counts. The worked inputs
  contain values 10 → 5 and 20 → 15 nmol/L: their baseline mean is 15, follow-up
  mean is 10, changes are both −5 nmol/L, and percentage changes are −50 and −25.
  A third participant has no laboratory rows and still contributes to the DM
  denominator. Other cases cover observed-only and all-missing means, absent and
  NOT DONE baselines, zero baselines, fractional percentages, composite study and
  participant keys, output order, repeated runs, whitespace/BOM handling, column
  reordering, and ignoring supplied analysis columns.
- [Validation tests](../backend/tests/test_validation.py) call public `process_csv`
  and inspect `InvalidInputError.issues`. They cover malformed CSV, missing or
  duplicate headers, row widths, required cells, numeric types and bounds,
  nonfinite values and overflow, units/test names, scheduled visits/dates,
  unknown and duplicate keys, mismatched result fields, and contradictory
  observation status/reason fields. Duplicate lab rows violate record and visit
  uniqueness together; the declared first-error behavior reports the record key.
- [API tests](../backend/tests/test_api.py) check health, successful processing,
  public response schemas, documentation, validation envelopes and locations,
  invalid UTF-8/CSV, missing uploads and text fields in place of files. They check
  inclusive per-file limits, both upload fields, and UTF-8 byte counts rather than
  character counts. Arbitrary filenames/MIME types do not override CSV contents.

Expected counts come from the source data README; worked values are literals,
not calculations made by the code under test. Raw-record comparisons read the
input CSV cells independently. HTTP-to-Python equality also checks that the API
preserves processing output; the processing tests provide the independent oracle.

## Exact and approximate comparisons

Identifiers, raw values, joined demographics, dates, order, units, counts, and
nulls compare exactly. Baselines are copied raw observations and also compare
exactly. Missing is never equated to zero.

Only calculated means, changes, and percentages use
`pytest.approx(expected, rel=1e-9, abs=1e-9)`. Agreement allows the larger of
`1e-9 * abs(expected)` and `1e-9` absolute difference. The absolute tolerance is
in nmol/L for means/changes and percentage points for percentage changes; the
relative tolerance is dimensionless. This allows tiny floating-point differences
while detecting meaningful changes in these teaching examples. It is an
engineering comparison rule, not a clinical threshold. No output is rounded to
make it pass. Exact equality across identical local runs is additionally checked
as evidence of repeatability under the [course definitions](../GLOSSARY.md).

## Controlled failure and recovery

On a disposable teaching branch, change the worked summary test's baseline mean
expectation from `15.0` to `16.0`, then run:

```bash
python -m pytest backend/tests/test_processing.py::test_worked_summaries_include_dm_participants_without_lab_rows -q
```

The observed exercise failed with `Obtained: 15.0`, `Expected: 16.0 ± 1.6e-08`
and `1 failed`. Restore the expectation to `15.0` and repeat the command:
`1 passed`. Then run the full suite. The committed tests contain the correct
expectation. This demonstrates reading a failure without changing the processing
contract or distributing a deliberately failing application.

## Actual verification

Issue #5 was checked on macOS with Python 3.12.1 and pytest 9.1.1 using the shared
temporary environment, from the issue worktree's repository root:

```bash
PYTHONPATH=backend /private/tmp/3r-implementation.eIFtRw/venv/bin/python -m pytest backend/tests -q
/private/tmp/3r-implementation.eIFtRw/venv/bin/python -m pytest backend/tests
```

Both commands: **175 passed, 1 warning** (14 processing, 131 validation, 30 API cases).
Before this change, the same suite target did not exist: pytest collected no
tests and exited with code 4. Tests were added against existing behavior; no
backend implementation defect or production-code fix was needed. The controlled
failure/recovery above was also executed, not merely proposed.

The shared environment emits a `StarletteDeprecationWarning` about TestClient's
httpx integration. Requests pass; the warning is left visible. Docker is not
installed, so no container execution or local/container replicability result is
claimed. CI execution belongs to its separate task and was not run here.
