# Verification evidence and limits

This is the single record of checks performed while authoring the course, as of October 2026. Other documents link here rather than repeating these results.

| Area | Recorded evidence |
| --- | --- |
| Processing, API, comparison seams | The full local suite passed **205 tests**, with one Starlette/httpx deprecation warning. Run `python -m pytest backend/tests` from the root; see [testing](testing.md) and [comparison commands](comparisons.md). |
| Live local API | Uvicorn on a temporary port received real multipart HTTP uploads: status 200; 24 participants, 96 records, 95 observed, one missing; eight arm/visit summaries; identifier `001` preserved. Direct processing and TestClient payloads agreed. Normal [setup](setup.md) uses port 8000. |
| Local Streamlit | Streamlit AppTest checks exercised actual HTTP uploads to the local backend, metrics 24/96/95/1, three tables and a chart, preserved missing values, and invalid AGE producing a located 422 error without stale results. This is AppTest evidence, not a browser screenshot; see [frontend](frontend.md). |
| Real Docker execution | [Actions run 38876609585](https://github.com/drweihungpan-lab/3R-teaching/actions/runs/38876609585) (commit `c5fc92a`) passed **Backend tests** and **Docker output comparison**. It built both real images, started Compose, checked API/UI health and frontend-to-backend service DNS/HTTP, compared two local captures and Docker output, compared a real multipart API upload, and uploaded evidence artifacts. The run identifies that commit only; rerun for later changes. |
| Synthetic data | DM/LB are byte-equal to the source at commit `d7f068da5eda2fda94e8588dae94ecc2b93ae2b0`. See [provenance](../data/synthetic/README.md) and [dictionary](../data/synthetic/data-dictionary.md). |
| Teaching assets | All five decks pass the converter's `--check-only` (exact source text/order, hyperlinks, geometry, XML/ZIP); Sessions 1–5 contain 33, 33, 23, 33, and 19 editable slides. Local Markdown links resolve. See [materials](../materials/README.md) and [slide checks](../materials/slides/README.md). |

## Remaining limits

Docker was unavailable on the authoring machine; container evidence comes from GitHub Actions. PowerPoint/LibreOffice rendering was unavailable: structural deck checks do not prove absence of rendered clipping or font substitution. Review decks in the classroom viewer before teaching.

Windows execution in WSL, fresh dependency downloads, and manual browser uploads have not been rehearsed. Student accounts, template-repository permissions, branch protection, peer participation, survey responses, and the classroom schedule require instructor setup or actual teaching; see [template permissions](template.md), [collaboration](collaboration.md), and the [final checklist](../materials/assessment/final-presentation.md). None of these authoring checks is a student assessment.
