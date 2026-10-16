# Repeatability, Reproducibility, and Replicability

A practical course for statistics students on the engineering framework behind repeatable data processing: isolated environments, collaborative Git workflows, reusable Python packages, tests, continuous integration (CI), APIs, and containers.

The emphasis is on understanding how the parts connect and practicing the workflow. Model complexity and UI design are not the focus.

## Start here

- [Syllabus](SYLLABUS.md): learning outcomes, five sessions, homework, and assessment requirements.
- [Course design](docs/course-design.md): agreed scope and teaching decisions.
- [Glossary](GLOSSARY.md): the course-specific meanings of the three Rs.
- [Setup](docs/setup.md): Python 3.12 environment, dependencies, and local backend commands.
- [Course materials](materials/README.md): slides, exercises, homework, instructor notes, surveys, and final checklist.
- [Verification](docs/verification.md): actual local and hosted evidence and remaining limits.
- [Specification](docs/specs/course-framework-and-teaching-materials.md): the course deliverables and agreed implementation boundaries; published as [GitHub issue #1](https://github.com/drweihungpan-lab/3R-teaching/issues/1).
- [Implementation tickets](docs/tickets/README.md): 37 approved course-authoring tasks published as GitHub issues, with dependencies and acceptance criteria.

## Course at a glance

| Item | Course requirement |
| --- | --- |
| Audience | 20 statistics students familiar with Python functions, pandas, and basic regression |
| Classroom time | Five three-hour sessions, 15 hours total |
| Homework | Mandatory; approximately two hours after each of Sessions 1–4, eight hours total |
| Groups | Three or four students, each group with its own GitHub repository |
| Language | English |
| Assessment | Pass/fail at the final presentation; all engineering requirements must be met |

## What students will practice

1. Set up an isolated Python environment and manage local configuration.
2. Make changes through feature branches, pull requests, peer review, and merges into `main`.
3. Trace reusable processing code through a Python package, FastAPI service, and Streamlit interface.
4. Run tests locally and interpret automated GitHub Actions checks.
5. Launch the application with Docker Compose and compare outputs across execution conditions.

The practical focus is **repeatability**—matching results under the same conditions—and **replicability**—matching results under slightly different conditions. Students will compare repeated local runs, then compare local virtual-environment and Docker runs using the same code and data. See the [glossary](GLOSSARY.md) for the terminology used in this course.

## Example and group projects

The supplied template provides a complete working healthcare cleaning and processing example using [synthetic data and provenance](data/synthetic/README.md) from [clinical-data-teaching](https://github.com/drweihungpan-lab/clinical-data-teaching). Students inspect the framework and make small changes through the full engineering workflow.

Groups select their own datasets and questions without mandatory topic approval. Modeling is optional. FastAPI, Streamlit, and Docker Compose are required. Each student must author at least one pull request and meaningfully review at least one teammate's pull request.

During the final presentation, groups will demonstrate their application, tests, passing CI, collaboration history, input validation, and output comparisons. Statistical analysis correctness is not graded. There is no separate submission, resubmission, or reassessment; see the [syllabus](SYLLABUS.md) for the complete requirements.

## Current status

The working example, synthetic datasets, backend tests, CI, Docker configuration, and teaching materials are implemented. The [materials index](materials/README.md) lists five Markdown slide sources, five editable PowerPoint decks, four exercises, four homework briefs, five instructor notes, two surveys, and the final checklist.

The [verification report](docs/verification.md) separates completed checks from classroom and platform limits. The specification and individual tickets retain their original planning context; the [ticket index](docs/tickets/README.md) explains current implementation status.

## Repository guide

| Area | Implementation and instructions |
| --- | --- |
| Processing and API | [Python package](backend/stat_core/), [FastAPI entry point](backend/app/main.py), [API contract](docs/api.md) |
| Frontend | [Streamlit app](frontend/app.py), [local startup and uploads](docs/frontend.md) |
| Tests and CI | [Tests](backend/tests/), [test commands](docs/testing.md), [CI guide](docs/ci.md), [workflow](.github/workflows/backend-tests.yml) |
| Containers | [Compose configuration](compose.yaml), [Compose startup](docs/compose.md), [backend image](docs/backend-container.md), [frontend image](docs/frontend-container.md) |
| Output comparisons | [Capture and comparison commands](docs/comparisons.md) |
| Data | [Synthetic inputs and provenance](data/synthetic/README.md), [data dictionary](data/synthetic/data-dictionary.md) |
| Group workflow | [Template setup and permissions](docs/template.md), [collaboration and PR guidance](docs/collaboration.md) |
| Teaching | [Complete materials index](materials/README.md), [syllabus](SYLLABUS.md) |
