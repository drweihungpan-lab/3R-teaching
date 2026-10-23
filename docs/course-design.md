# Course design decisions

The [syllabus](../SYLLABUS.md) is the single source for audience, workload, sessions, timing, and assessment; the [glossary](../GLOSSARY.md) defines the three Rs. This page records the teaching decisions behind them.

## Teaching approach

- Students receive a complete, working healthcare example, including its UI and processing logic. They practice small changes through branches, pull requests, peer review, tests, CI, and Docker rather than building the application from scratch or filling in unfinished functions.
- The framework and engineering workflow are the teaching priority; UI development and model complexity are not.
- The example uses synthetic healthcare data from the `clinical-data-teaching` repository for simple cleaning, validation, processing, summaries, and visualization; model training is not required.
- Reproducibility under the course convention is discussed conceptually rather than through a required independent simulation. Cross-group reproduction and new-data experiments are not required.
- Session 1 opens with an open bubble tea shop question and published reproducibility statistics before the definitions. Sessions 2–5 each open with one open bubble tea question. Students' answers are not mapped to the three Rs for them.

## Materials and workflow

- All slides, exercises, surveys, and repository instructions use plain English, with technical terms explained when introduced.
- Slides are editable PowerPoint files generated from Markdown sources kept in the repository.
- Pre-course and post-course surveys use matching questions to assess progress, plus readiness and feedback questions respectively.
- Groups use feature branches, pull requests, peer review, and merges into `main`; there is no separate `develop` branch.
- Final-presentation-only assessment supersedes earlier discussion of resubmission.
