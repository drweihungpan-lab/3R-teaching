# Synthetic healthcare data dictionary

**Invented teaching study: EDU-LPA-001. Not SLN360 data or results.** Provenance and input checksums are in the [README](README.md). All records are synthetic. Names resemble SDTM conventions without claiming full conformance.

CSV files have a header row. Identifiers and categories are text; empty fields mean unavailable or not applicable, never zero. Dates use ISO `YYYY-MM-DD`. Numeric types below describe intended interpretation when reading CSV, not changes to the raw files.

## Shared identifiers

| Field | Type | Definition and values |
| --- | --- | --- |
| `STUDYID` | Text | Invented study identifier, always `EDU-LPA-001` in both files |
| `DOMAIN` | Text | File domain: `DM` for participant characteristics, `LB` for laboratory records |
| `USUBJID` | Text | Participant identifier shared across files, `EDU-LPA-001` through `EDU-LPA-024` |

`STUDYID` and `USUBJID` have different roles even though their values coincide for the first participant. The participant key is (`STUDYID`, `USUBJID`). Join LB to DM on those two fields; `DOMAIN` is not a join field because it differs between files.

## dm.csv: participant characteristics

One row per participant, 24 rows. The three shared fields above are followed by:

| Field | Type | Definition and values |
| --- | --- | --- |
| `SUBJID` | Text | Within-study identifier `001`–`024`; retain leading zeros |
| `AGE` | Integer | Invented age in years, 37–70 in this sample |
| `AGEU` | Text | Age unit, always `YEARS` |
| `SEX` | Text | Synthetic recorded sex: `F` or `M`; only these invented categories appear (8 F, 16 M) |
| `ARM` | Text | Assigned teaching arm, `Placebo` or `Investigational A`, 12 participants each |
| `RFSTDTC` | Date | Day-1 start, `2026-01-01`, for every participant |
| `RFENDTC` | Date | Day-90 end, `2026-03-31`, for every participant |

No DM fields are empty. The file contains participant characteristics and assignment, not administration or safety records.

## lb.csv: scheduled laboratory observations

One row per participant and scheduled visit, 96 rows. The three shared fields above are followed by:

| Field | Type | Definition and values |
| --- | --- | --- |
| `LBSEQ` | Integer | Laboratory record sequence within participant: 1, 2, 3, 4 in visit order |
| `LBTESTCD` | Text | Test code, always `LPA` |
| `LBTEST` | Text | Test name, always `Lipoprotein(a)`; abbreviated Lp(a) in prose |
| `LBORRES` | Decimal or missing | Recorded laboratory result; empty for the unavailable observation |
| `LBORRESU` | Text | Recorded result unit, always `nmol/L` (nanomoles per liter), including the not-done row |
| `LBSTRESN` | Decimal or missing | Numeric result in the standard unit; equals `LBORRES` for observed rows, empty for the unavailable observation |
| `LBSTRESU` | Text | Standard result unit, always `nmol/L`; no unit conversion is needed |
| `VISIT` | Text | Scheduled visit label: `BASELINE`, `DAY 15`, `DAY 30`, or `DAY 90` |
| `LBDY` | Integer | Study day: 1, 15, 30, or 90; baseline is day 1, not day 0 |
| `LBDTC` | Date | Laboratory observation date; the scheduled date is retained for the not-done record |
| `LBSTAT` | Text or empty | `NOT DONE` for the one unavailable result; empty for observed results |
| `LBREASND` | Text or empty | `SPECIMEN NOT AVAILABLE` for that unavailable result; empty otherwise |

The record key is (`STUDYID`, `USUBJID`, `LBSEQ`). In this single-test sample, (`STUDYID`, `USUBJID`, `VISIT`) is also unique. Every LB participant appears once in DM.

## Visits and unavailable observations

| `LBSEQ` | `VISIT` | `LBDY` | `LBDTC` |
| --- | --- | --- | --- |
| 1 | BASELINE | 1 | 2026-01-01 |
| 2 | DAY 15 | 15 | 2026-01-15 |
| 3 | DAY 30 | 30 | 2026-01-30 |
| 4 | DAY 90 | 90 | 2026-03-31 |

Each participant has all four scheduled rows. Only `EDU-LPA-007`, `LBSEQ=3`, at `DAY 30` has no observed value: both result fields are empty, `LBSTAT` is `NOT DONE`, and the reason is `SPECIMEN NOT AVAILABLE`. The identifiers, visit, date, and units remain populated. There are 95 observed results and one unavailable result, not an absent schedule row or a zero concentration.

For later summaries, use observed values only and report the observed denominator: day 30 has 23 observed participants (11 Investigational A, 12 Placebo); each other visit has 24 (12 per arm). Preserve missingness in cleaned records and perform no imputation. The [README](README.md) describes the intended join, cleaning, summary, and count checks.
