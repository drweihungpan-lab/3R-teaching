# Course design decisions

The [syllabus](../SYLLABUS.md) is the single source for audience, workload, sessions, timing, and assessment; the [glossary](../GLOSSARY.md) defines the terms. This page records the teaching decisions behind them.

## Teaching approach

- One running example, the device example, is the course dataset: synthetic daily measurement counts for medical devices, with the task of predicting when each reaches its usage limit. It grows through seven stages from a notebook to a containerized application, and its Stage 4 processing code starts every group's package.
- Students receive working code and practise small changes through branches, pull requests, peer review, tests, CI, and Docker rather than building the application from scratch.
- The framework and engineering workflow are the teaching priority; UI development and model complexity are not. The Frontend repo is supplied and not edited.
- Reproducibility under the course convention is discussed conceptually rather than through a required independent simulation. Cross-group reproduction and new-data experiments are not required.
- Every session opens with one open bubble tea shop question. Session 1 also presents published reproducibility statistics before the definitions. Students' answers are not mapped to the three Rs for them.
- Packages are shared as tagged Releases installed from a git URL, not through a package registry; see [ADR 0002](adr/0002-distribute-by-git-tag-not-registry.md).
- Cookiecutter is taught as a tool students can customise, not hidden behind a template repository.

## Materials and workflow

- All slides, exercises, surveys, and repository instructions use plain English, with technical terms explained when introduced.
- Slides are editable PowerPoint files generated from Markdown sources kept in the repository.
- Every session has the same shape: 60 minutes, a 10-minute break, 60 minutes, then 40 minutes of hands-on practice.
- Pre-course and post-course surveys use matching questions to assess progress, plus readiness and feedback questions respectively.
- Groups use feature branches, pull requests, peer review, and merges into `main`; there is no separate `develop` branch.
- Final-presentation-only assessment supersedes earlier discussion of resubmission.
