# Verification evidence and limits

This report consolidates actual course-authoring evidence as of 16 October 2026. Earlier author-verification sections describe checks performed for those individual changes; their original 175-test results and local Docker limits remain historical facts.

| Area | Actual evidence |
| --- | --- |
| Processing, API, comparison seams | After issue #10, the full local suite passed **205 tests**, with one Starlette/httpx deprecation warning. Run `python -m pytest backend/tests` from the root; see [testing](testing.md) and [comparison commands](comparisons.md). Issue #38 changes documentation and one deck, so it does not repeat the unchanged suite. |
| Live local API | Parent verification launched uvicorn on temporary port 18000 and sent real multipart HTTP uploads: status 200; 24 participants, 96 records, 95 observed, one missing; eight arm/visit summaries; identifier `001` preserved. Direct processing and TestClient payloads agreed. Normal [setup](setup.md) uses port 8000. |
| Local Streamlit | Parent Streamlit AppTest checks exercised actual HTTP uploads to the local backend, metrics 24/96/95/1, three tables and a chart, preserved missing values, and invalid AGE producing a located 422 error without stale results. This is AppTest evidence, not a browser screenshot; see [frontend](frontend.md). |
| Real Docker execution | [Actions run 38876609585](https://github.com/drweihungpan-lab/3R-teaching/actions/runs/38876609585) passed **Backend tests** and **Docker output comparison**. It built both real images, started Compose, checked API/UI health and frontend-to-backend service DNS/HTTP, compared two local captures and Docker output, compared a real multipart API upload, and uploaded evidence artifacts. The parent downloaded the artifact and confirmed comparison success. |
| Recent integration CI | [Successful integration run 38922198115](https://github.com/drweihungpan-lab/3R-teaching/actions/runs/38922198115) checks integration commit `5fb8b91`; [previous successful run 38921935222](https://github.com/drweihungpan-lab/3R-teaching/actions/runs/38921935222) checks `02c32b3`. Links identify the checked commits rather than promising future branch results. See [CI](ci.md). |
| Synthetic data | Parent checks found DM/LB byte-equal to the source at commit `d7f068da5eda2fda94e8588dae94ecc2b93ae2b0` and confirmed source commit/blob identity remotely. See [provenance](../data/synthetic/README.md) and [dictionary](../data/synthetic/data-dictionary.md). |
| Teaching assets | Five Markdown sources and five editable decks, four exercises, four homework briefs, five instructor notes, two surveys, and a final checklist are indexed in [materials](../materials/README.md). Issue #38 checks local file links and anchors, inventory, course facts, and all five decks using the existing converter's `--check-only`. The Session 2 status sentence and its deck are updated together. |

## Navigation checks for issue #38

Temporary documentation checks passed for **553 local Markdown file links**, including **47 heading anchors** (fenced examples and inline syntax examples excluded). All five existing-converter `--check-only` runs passed exact source text/order, hyperlink, geometry, and XML/ZIP checks: Sessions 1–5 contain 33, 33, 23, 35, and 19 editable slides respectively. Independent artifact checks found no empty slides or out-of-bounds shapes. Inventory and course facts were checked against the syllabus and glossary; `git diff --check` passed. No application code or testing framework was added.

## Remaining limits

Docker is unavailable locally; actual container evidence comes from GitHub Actions. PowerPoint/LibreOffice rendering is unavailable: source text/order, links, editable objects, geometry, and XML/ZIP checks do not prove absence of rendered clipping or font substitution. Review decks in the classroom viewer before teaching; see [slide checks](../materials/slides/README.md).

Windows/PowerShell execution and manual browser upload interactions have not been rehearsed. Streamlit AppTest and real HTTP checks cover the recorded local behavior. Student accounts, template-repository permissions, branch protection, peer participation, survey responses, and the classroom schedule require instructor setup or actual teaching; see [template permissions](template.md), [collaboration](collaboration.md), and the [final checklist](../materials/assessment/final-presentation.md). None of these authoring checks is an additional student assessment.
