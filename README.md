# Repeatability, Reproducibility, and Replicability

A practical course for statistics students on the engineering framework behind repeatable data processing: isolated environments, collaborative Git workflows, reusable Python packages, tests, continuous integration (CI), APIs, and containers.

The emphasis is on understanding how the parts connect and practicing the workflow. Model complexity and UI design are not the focus.

## Start here

- [Syllabus](SYLLABUS.md): learning outcomes, five sessions, homework, and assessment requirements.
- [Course design](docs/course-design.md): agreed scope and teaching decisions.
- [Glossary](GLOSSARY.md): the course-specific meanings of the three Rs.
- [Specification](docs/specs/course-framework-and-teaching-materials.md): the course deliverables and agreed implementation boundaries; published as [GitHub issue #1](https://github.com/drweihungpan-lab/3R-teaching/issues/1).
- [Ticket drafts](docs/tickets/): proposed implementation slices and dependencies, awaiting approval before publication as GitHub issues.

## Course at a glance

| Item | Plan |
| --- | --- |
| Audience | 20 statistics students familiar with Python functions, pandas, and basic regression |
| Classroom time | Five three-hour sessions, 15 hours total |
| Homework | Mandatory; approximately two hours after each of Sessions 1–4 |
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

The planned template will provide a complete working healthcare cleaning and processing example using synthetic data from [clinical-data-teaching](https://github.com/drweihungpan-lab/clinical-data-teaching). Students will inspect the framework and make small changes through the full engineering workflow.

Groups will select their own datasets and questions. Modeling is optional. FastAPI, Streamlit, and Docker Compose are required. Each student must author at least one pull request and meaningfully review at least one teammate's pull request.

During the final presentation, groups will demonstrate their application, tests, passing CI, collaboration history, input validation, and output comparisons. Statistical analysis correctness is not graded. There is no separate submission, resubmission, or reassessment; see the [syllabus](SYLLABUS.md) for the complete requirements.

## Current status

This repository currently contains basic course documentation and agent configuration. The application template, datasets, tests, CI workflow, Docker setup, slides, exercises, and pre/post-course surveys are planned deliverables and are not yet implemented here.

Implementation will be specified and divided into tasks one at a time through `to-spec` and `to-ticket`. There are no application installation or startup steps at this stage.

## Repository guide

```text
.
├── README.md                  # Course introduction and navigation
├── SYLLABUS.md                # Sessions, homework, and assessment
├── GLOSSARY.md                # Course terminology
├── AGENTS.md                  # Guidance for coding agents
├── .gitignore                 # Local environments, secrets, and generated files
└── docs/
    ├── course-design.md       # Agreed course design
    └── agents/                # Issue-tracker and domain-document conventions
```
