# Synthetic healthcare teaching data

**Invented teaching study: EDU-LPA-001. Not SLN360 data or results.** All participants, values, dates, and arm assignments are invented. These files support the course's cleaning, joining, validation, and summary demonstrations; they provide no evidence about a real intervention.

| File | Records excluding header | Meaning |
| --- | --- | --- |
| [dm.csv](dm.csv) | 24 | One participant per row; 12 assigned to Placebo and 12 to Investigational A |
| [lb.csv](lb.csv) | 96 | Four scheduled Lipoprotein(a), or Lp(a), records per participant; 95 observed results and one unavailable result |

The [data dictionary](data-dictionary.md) defines every field, identifier, unit, visit, and missing-value convention. Both CSVs are included here unchanged, so learners need no neighboring repository, generator, download, or external data service.

## Provenance

Copied verbatim from [`drweihungpan-lab/clinical-data-teaching`](https://github.com/drweihungpan-lab/clinical-data-teaching/tree/d7f068da5eda2fda94e8588dae94ecc2b93ae2b0/data/synthetic), commit `d7f068da5eda2fda94e8588dae94ecc2b93ae2b0`, paths `data/synthetic/dm.csv` and `data/synthetic/lb.csv`. Field meanings and teaching caveats were checked against that commit's [source dictionary](https://github.com/drweihungpan-lab/clinical-data-teaching/blob/d7f068da5eda2fda94e8588dae94ecc2b93ae2b0/data/synthetic/data-dictionary.md) and [source README](https://github.com/drweihungpan-lab/clinical-data-teaching/blob/d7f068da5eda2fda94e8588dae94ecc2b93ae2b0/data/synthetic/README.md).

The source uses SDTM-style names for recognition, but deliberately omits many standard fields and artifacts. These CSVs do not claim full SDTM conformance, regulatory suitability, or production validation. Other source domains and analysis-ready files are not needed for this sample.

SHA-256 checksums of the unchanged inputs:

```text
3ea2c64e321996bd4797bcfc0bf7aa923ebf26ccd14e85cba876ffaa6804010e  dm.csv
3afbb67c1c60a7b4023cd7742cf6a407e11c388aca54851687978df4c9f3f870  lb.csv
```

## Intended cleaning and summary example

This describes the later processing example; this task supplies only inputs and documentation.

1. Read identifiers as text, preserving leading zeros in `SUBJID`. Parse ages, study days, sequences, and observed results as numbers; parse dates as ISO dates. Check required fields, unique participant and laboratory keys, expected units, and visit labels. Reject incompatible values explicitly.
2. Join each laboratory row to its participant's age, recorded sex, and arm using `STUDYID` and `USUBJID`. This is a many-to-one join: each laboratory record must match exactly one participant. The supplied data have no duplicate keys or unmatched records, so the join retains all 96 scheduled records.
3. Preserve empty results as missing. For `EDU-LPA-007` at `DAY 30`, retain the scheduled row, `LBSTAT=NOT DONE`, and `LBREASND=SPECIMEN NOT AVAILABLE`. Do not replace the result with zero, impute it, or drop the participant's other visits. The cleaned schedule still has 96 rows; an observed-only summary uses 95 values.
4. Summarize participant counts by arm and observed Lp(a) counts and means by arm and visit. Use `LBSTRESN` in `nmol/L`, with each mean's denominator equal to the observed count at that visit. A simple chart can show those means over study day. No statistical modeling or treatment-effect inference is required.

Expected counts (the denominator for participant summaries is 24 participants, not 96 laboratory rows):

| Visit | Study day | Scheduled records | Observed: Investigational A | Observed: Placebo | Observed total |
| --- | --- | --- | --- | --- | --- |
| BASELINE | 1 | 24 | 12 | 12 | 24 |
| DAY 15 | 15 | 24 | 12 | 12 | 24 |
| DAY 30 | 30 | 24 | 11 | 12 | 23 |
| DAY 90 | 90 | 24 | 12 | 12 | 24 |
| Total | — | 96 | 47 | 48 | 95 |

These counts support later exact comparisons of records and counts for repeatability and replicability under the [course definitions](../../GLOSSARY.md). Numerical tolerances for calculated means belong to the later processing and testing tasks.
