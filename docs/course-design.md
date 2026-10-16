# Course design decisions

## Current stage

The agreed course design has been synthesized into a specification and 37 approved course-authoring tickets, published on GitHub and indexed in `tickets/README.md`. Implementation will proceed one task at a time following their dependencies. Application code, repository scaffolding, slides, surveys, and exercises remain planned deliverables; they have not been implemented or validated.

## Scope

- Course title: Repeatability, Reproducibility, and Replicability.
- Primary practical focus: repeatability and replicability, using the course-specific definitions in `../GLOSSARY.md`.
- Repeatability exercise: rerun the same pipeline with the same input under the same conditions and compare results.
- Replicability exercise: run the same data and code in a local Python virtual environment and in Docker, then compare results.
- Comparison criteria: cleaned records and counts must match exactly; calculated decimal values must agree within a declared numerical tolerance specified in tests.
- Reproducibility under the course convention is conceptual rather than a required independent simulation.
- Cross-group reproduction and new-data experiments are not required.

## Audience and workload

- Twenty statistics students who already know Python functions, pandas, and basic regression.
- Five three-hour classroom sessions and approximately two hours of mandatory homework after each of Sessions 1–4.
- Groups of three or four, each with its own repository.
- Every student authors at least one pull request and reviews at least one teammate's pull request with meaningful comments.
- The instructor can inspect pull requests and reviews in each group's repository.

## Projects and teaching materials

- Groups choose their own datasets and statistical questions; prior topic approval is not required. Groups may discuss their chosen topics with the instructor.
- Modeling is optional; a tested, reproducible workflow is the broader learning objective, with the practical assessment centered on the first two Rs defined above.
- FastAPI, Streamlit, and Docker Compose are required, with starter code provided.
- The template contains a complete, working healthcare example, including its UI and processing logic. Students practice small changes through branches, pull requests, peer review, tests, CI, and Docker rather than building the application from scratch or filling unfinished functions.
- The framework and engineering workflow are the teaching priority; UI development and model complexity are not assessment priorities.
- The classroom example uses the synthetic healthcare data in the neighboring `clinical-data-teaching` repository for simple cleaning, validation, processing, summaries, and visualization.
- Include pre-course and post-course surveys with matching questions to assess progress, plus readiness and feedback questions respectively.
- All slides, exercises, surveys, and repository instructions use plain English, with technical terms explained when introduced.
- Slides are delivered as editable PowerPoint files with Markdown sources maintained in the repository.

## Classroom plan and collaboration

- Provisional allocation for each three-hour session: 45 minutes of explanation, 30 minutes of demonstration, 90 minutes of guided practice, and a 15-minute break. Adjust as the materials develop; the final showcase needs its own presentation schedule.
- Use feature branches, pull requests, peer review, and merges into `main`; do not introduce a separate `develop` branch.

## Provisional session sequence

| Session | Framework and workflow focus | Practice using the supplied working example |
| --- | --- | --- |
| 1 | Environment isolation, Git, configuration hygiene, and CI introduction | Create a group repository from the eventual template, use a virtual environment and local configuration, open a draft PR, and inspect checks |
| 2 | Modules, packaging, type hints, and logging | Trace processing code, install the package in editable mode, and make a small reviewed change |
| 3 | FastAPI, validation, pytest, and CI | Trace a request into processing logic, exercise invalid inputs, and inspect failing and passing tests locally and on a PR |
| 4 | Streamlit, Docker, and Compose | Trace UI-to-API communication, inspect service configuration, and compare local and container outputs |
| 5 | Final presentation and engineering review | Demonstrate the application and all required workflow evidence; make the final pass/fail decision |

The supplied example centers on simple healthcare cleaning and processing rather than mandatory model training. Detailed exercises, commands, and presentation schedules will be developed through later specifications and tasks.

## Assessment

- Assessment is pass/fail, without weighted scores.
- All required engineering evidence must be present: pull requests, meaningful peer reviews, tests, passing CI, repeatable runs, and matching local/Docker results under the declared comparison criteria.
- Each student must satisfy the individual pull-request and peer-review requirements recorded above.
- Statistical analysis correctness is not graded. This does not remove the engineering requirement to demonstrate tests and output comparisons against declared processing behavior.
- All assessment evidence is inspected during the final presentation in Session 5; there is no separate submission.
- The final presentation result is final: no resubmission or second assessment attempt, including a retry later in the final session.
- Earlier discussion of resubmission is superseded by this final-presentation-only assessment policy.
