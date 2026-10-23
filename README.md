# Repeatability, Reproducibility, and Replicability

A practical course for statistics students on the engineering framework behind repeatable data processing: isolated environments, collaborative Git workflows, reusable Python packages, tests, continuous integration (CI), APIs, and containers.

The emphasis is on understanding how the parts connect and practicing the workflow. Model complexity and UI design are not the focus.

## Start here

- [Syllabus](SYLLABUS.md): audience, workload, learning outcomes, five sessions, homework, and assessment. This is the single source for course facts.
- [Glossary](GLOSSARY.md): the course-specific meanings of the three Rs.
- [Course materials](materials/README.md): slides, exercises, homework, instructor notes, surveys, and final checklist.
- [Setup](docs/setup.md): Python 3.12 environment, dependencies, and local backend commands.
- [Course design](docs/course-design.md): teaching decisions not covered by the syllabus.
- [Verification](docs/verification.md): recorded local and hosted checks and remaining limits.
- [Specification](https://github.com/drweihungpan-lab/3R-teaching/issues/1): the original planning document, kept as GitHub issue #1.

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
| Teaching | [Materials index](materials/README.md), [syllabus](SYLLABUS.md) |
