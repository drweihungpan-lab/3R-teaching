# Backend API and processing contract

The example processes the synthetic [participant and laboratory CSVs](../data/synthetic/README.md). It reports descriptive values only; it makes no clinical or treatment-effect inference.

## Python entry point

```python
from pathlib import Path
from stat_core import ProcessResult, process_csv

result = process_csv(
    Path("data/synthetic/dm.csv").read_text(encoding="utf-8"),
    Path("data/synthetic/lb.csv").read_text(encoding="utf-8"),
)
validated = ProcessResult.model_validate(result)
```

`process_csv(participants_csv: str, laboratory_csv: str) -> dict` takes CSV **contents**, not paths. It returns a JSON-compatible dictionary. Public Pydantic schemas are exported from `stat_core`; `ProcessResult` is the complete response. Invalid data raises `InvalidInputError`, with `.issues` containing `ValidationIssue` objects. Each issue has `file` (`participants` or `laboratory`), `row` (CSV line number, header = 1, or null for a file error), `field` (column name or null), and `message`. Validation stops at the first detected error; fix it and retry.

## HTTP endpoints

Run the service using [setup.md](setup.md). Interactive request/response schemas are at `/docs`; the machine-readable schema is `/openapi.json`.

- `GET /health` returns HTTP 200 and `{"status":"ok"}`. It checks that the service is running; it does not read input files.
- `POST /process` accepts `multipart/form-data` with two required file fields: `participants` (DM CSV) and `laboratory` (LB CSV). Use UTF-8, optionally with a UTF-8 byte-order mark. Filenames and MIME types are not used to decide whether contents are valid.

```bash
curl --fail-with-body http://127.0.0.1:8000/process \
  -F participants=@data/synthetic/dm.csv \
  -F laboratory=@data/synthetic/lb.csv
```

HTTP 200 returns `ProcessResult`, with exactly these four top-level fields:

| Field | Contents |
| --- | --- |
| `counts` | `participants`, `records`, `observed`, `missing` (integer counts) |
| `records` | One joined record per supplied laboratory row, including missing observations |
| `arm_summaries` | Counts by `study_id`, `arm`; includes participants with no supplied lab rows |
| `visit_summaries` | Counts and observed mean by `study_id`, `arm`, `visit` |

Each record has `study_id`, `participant_id` (USUBJID), `subject_id` (SUBJID, text retaining leading zeros), `age` (integer years), `sex`, `arm`, `sequence` (LBSEQ integer), `test_code`, `test_name`, `visit`, `study_day` (integer), `date` (ISO date string), `value` (LBSTRESN), `unit`, `status`, `reason`, `baseline`, `change`, and `percent_change`. Values and calculated numbers are floats or null; empty status/reason become null. `baseline` is the participant's observed BASELINE value; `change = value - baseline`; `percent_change = 100 * change / baseline`. Missing current value or unavailable baseline gives null change and percent change. Zero baseline gives null percent change but allows an absolute change. Baseline rows have zero change when observed.

Each arm summary has `study_id`, `arm`, `participants`, `records`, `observed`, `missing`. Each visit summary has `study_id`, `arm`, `visit`, `study_day`, `participants` (participants with a supplied row at that visit), `records`, `observed`, `missing`, `mean`, `unit`. Mean excludes missing values; an all-missing group has null mean. Arm participant counts use DM, never the number of lab rows. Visits with no supplied rows have no summary row; omitted schedule rows are not manufactured or counted as missing.

Records sort by study ID, participant ID, study day, sequence. Arm summaries sort by study ID and arm; visit summaries by study ID, arm, study day. Reordering CSV rows does not change output order or results. No timestamps or run identifiers are included.

For the supplied files, counts are `{"participants":24,"records":96,"observed":95,"missing":1}`. Both arms have 12 participants and 48 records; Investigational A has 47 observed and one missing, Placebo has 48 observed and none missing. Investigational A at DAY 30 has 12 scheduled records, 11 observed and one missing. The first record has `subject_id="001"`, `value=167.0`, `baseline=167.0`, `change=0.0`, `percent_change=0.0`. Its DAY 15 value is 106.5, change is -60.5, percent change is approximately -36.22754491017964. The missing DAY 30 record for `EDU-LPA-007` has null value/change/percent_change, baseline 269.0, status `NOT DONE`, reason `SPECIMEN NOT AVAILABLE`.

## Input rules and errors

All columns in the [data dictionary](../data/synthetic/data-dictionary.md) are required headers. Additional uniquely named columns are allowed and ignored, including supplied analysis-ready baseline/change columns. Column order may vary. Header and cell boundary whitespace is stripped. Empty/duplicate headers, malformed CSV, nonrectangular rows, empty files and files with no data rows are rejected. Blank lines between rows are ignored. Identifiers remain text; they must be nonempty.

- DM requires nonempty fields, `DOMAIN=DM`, integer nonnegative `AGE`, `AGEU=YEARS`, `SEX` of `F` or `M`, nonempty arm, and ISO dates with end on or after start. Participant key `(STUDYID, USUBJID)` and within-study `(STUDYID, SUBJID)` must each be unique. Study and participant identifiers are not restricted to the sample's literal IDs.
- LB requires `DOMAIN=LB`, `LBTESTCD=LPA`, `LBTEST=Lipoprotein(a)`, and both units exactly `nmol/L`. It must match a participant on **both** STUDYID and USUBJID. Both `(STUDYID, USUBJID, LBSEQ)` and `(STUDYID, USUBJID, VISIT)` must be unique.
- Visit/sequence/day combinations are BASELINE/1/1, DAY 15/2/15, DAY 30/3/30, DAY 90/4/90. LBDTC must equal the participant's start date plus study day minus one, and fall within their start/end dates. A subset of scheduled visits is allowed, including absence of a baseline row.
- Observed LBORRES and LBSTRESN must be equal finite nonnegative numbers; NaN, infinity, numeric overflow and incompatible strings are rejected. Observed status and reason must both be empty. Missing results require both result cells empty, `LBSTAT=NOT DONE` and a nonempty reason. A literal zero is observed, never missing. No unit conversion or imputation is performed.
- If a calculation cannot be represented as a finite JSON number, validation returns an error rather than emitting infinity/NaN.

HTTP 422 covers these rules, invalid UTF-8 and absent upload fields. For example, an invalid AGE produces:

```json
{"detail":[{"file":"participants","row":2,"field":"AGE","message":"Expected a nonnegative integer."}]}
```

The `ErrorResponse` schema describes this envelope. Missing upload fields have `row=null`. A file over configured `MAX_UPLOAD_BYTES` returns HTTP 413 with the same envelope. The limit applies per uploaded file; it is not a total HTTP request-body limit. The default is 5,242,880 bytes. The Python function has no upload size limit. Logs record processing counts or failure locations, not uploaded contents. See [setup.md](setup.md) for configuration.

For repeatability and replicability, compare record structure, strings, nulls and counts exactly. Compare calculated decimal fields with declared tolerances in the formal tests/output-comparison task; do not round the service's output or equate null with zero.
