# Repeatability, Reproducibility, and Replicability

## Course overview

This practical course introduces the engineering framework and collaborative workflow used to make statistical data processing repeatable and portable. Students learn how environments, reusable Python packages, tests, code review, automated checks, APIs, and containers fit together.

The emphasis is on understanding and using the workflow. Building a sophisticated model or designing a polished interface is not the goal. A complete healthcare example will support demonstrations and guided exercises; groups will apply the framework to their own datasets and questions.

The working application template and [teaching materials](materials/README.md) are supplied in this repository. See [setup](docs/setup.md) to run the example and [verification](docs/verification.md) for completed checks and remaining limits. Classroom activities describe how students will use these materials.

## Audience and workload

- **Audience:** 20 statistics students familiar with Python functions, pandas, and basic regression.
- **Classroom time:** 15 hours across five three-hour sessions.
- **Mandatory homework:** approximately two hours after each of Sessions 1–4, eight hours in total. Guided practice not finished in class is completed at home, in addition to this time.
- **Group size:** three or four students, with one GitHub repository per group.
- **Language:** English.

## The three Rs in this course

Terminology varies across disciplines. This course uses the definitions in [GLOSSARY.md](GLOSSARY.md).

| Principle | Course meaning | Course activity |
| --- | --- | --- |
| Repeatability | Matching results under the same conditions | Run the same pipeline twice using the same input and local environment |
| Replicability | Matching results under slightly different conditions | Run the same code and data locally in a virtual environment and in Docker, then compare outputs |
| Reproducibility | Matching results under very different conditions, such as an independent simulation | Discuss conceptually; an independent simulation is not required |

The practical focus is repeatability and replicability. Cleaned records and counts must match exactly. Calculated decimal values must agree within a stated numerical tolerance documented in the tests. Cross-group reproduction and new-data experiments are not required.

## Learning outcomes

By the end of the course, students should be able to:

1. Use an isolated Python environment and explain how configuration and dependencies affect execution.
2. Collaborate through feature branches, descriptive commits, pull requests, and meaningful peer reviews.
3. Explain how reusable processing code is packaged and connected to an API and user interface.
4. Run tests for declared processing behavior and invalid inputs, and interpret local and CI failures.
5. Launch a FastAPI and Streamlit application with Docker Compose and explain how the services communicate.
6. Demonstrate repeatability and replicability with explicit output comparisons.

## Teaching approach and projects

The supplied example uses [synthetic healthcare data](data/synthetic/README.md) from the [clinical-data-teaching repository](https://github.com/drweihungpan-lab/clinical-data-teaching). It illustrates joining participant and laboratory records, handling missing values, validating inputs, producing summaries, and displaying a simple chart. Model training is not required.

Each group will independently select its own dataset and statistical question. Topic approval is not required; groups may discuss their selected topic with the instructor. Cleaning, processing, summaries, visualization, and modeling are possible project activities. Modeling is optional, and complexity earns no additional credit.

The template contains a complete working example. Students will inspect it, make small changes, and verify those changes through the full workflow. FastAPI, Streamlit, and Docker Compose are required parts of every group's application.

Each student must author at least one pull request and review at least one teammate's pull request. Reviews must address behavior, tests, or clarity rather than provide approval alone. The instructor will inspect this evidence in each group's repository.

## Session 0: Required self-paced setup (pre-course)

**Duration:** none in class. This is a pre-course requirement, separate from the five sessions and 15 classroom hours.

Students complete the [Session 0 guide](docs/session-0.md) at home: a GitHub account, a terminal (Mac Terminal, or WSL with Ubuntu 24.04 LTS on Windows), Git, an SSH key connected to GitHub, Python 3.12 and VS Code. They then check in by commenting the output of three commands on a pinned issue in a public sandbox repository, by **3 days before Session 1**. Session 0 does not teach commit or push. See the [instructor notes](materials/instructor/session-0.md) and the [decision record](docs/adr/0001-wsl-and-ssh-for-all-students.md).

## Session 1: Environment isolation, modern Git, and CI foundations

**Duration:** 3 hours

**Core technologies:** Python 3.12, `venv`, Git, GitHub template repositories, `python-dotenv`, GitHub Actions.

### Topics

- Isolated virtual environments versus global package installations.
- Feature branches, descriptive commits, pull requests, and merge conflicts.
- The collaboration path: feature branch → pull request → peer review → merge into `main`.
- Configuration hygiene: `.gitignore`, local `.env` files, and shareable `.env.example` files.
- Continuous integration: automated checks on changes and the role of required checks in protecting `main`.

### Guided practice

Create a group repository from the supplied template, prepare a local environment, configure local environment variables, and make a small change on a feature branch. Open a draft pull request and inspect automated status checks.

### Mandatory homework: approximately 2 hours

Practice the branch and pull-request workflow in the group repository. Inspect a teammate's change and document the group's chosen dataset and question. First finish any guided practice not completed in class; this is in addition to the two hours.

**Progress checkpoint:** a group repository with environment isolation, configuration hygiene, and a visible branch/PR workflow. This is preparation for the final presentation, not a separate submission.

## Session 2: From scripts to modules—Python packaging and maintainable code

**Duration:** 3 hours

**Core technologies:** `pyproject.toml`, editable installation, type hints, Python logging.

### Topics

- Moving exploratory processing steps into reusable functions and modules.
- Separating processing logic from the interface and API.
- Reading type hints and using logging to understand execution.
- Package metadata, dependency declarations, and editable installation.

### Guided practice

Trace the supplied healthcare processing code in `backend/stat_core/`. Inspect `backend/pyproject.toml`, install the package in editable mode, and make a small processing or logging change through a reviewed pull request.

### Mandatory homework: approximately 2 hours

Apply a small, documented change relevant to the group's chosen data-processing question. Explain where the processing logic belongs and record the change through the repository workflow.

**Progress checkpoint:** the package runs inside the virtual environment, and the group can explain how modules, dependencies, and the editable installation connect.

## Session 3: Defensive engineering—FastAPI, pytest, and automated CI

**Duration:** 3 hours

**Core technologies:** FastAPI, Pydantic, pytest, fixtures, `pytest.approx`, GitHub Actions.

### Topics

- Request and response schemas as a contract between the UI and backend.
- Input validation, missing values, invalid types, and appropriate bounds.
- Testing processing behavior separately from API responses.
- Shared test fixtures and explicit numerical tolerances.
- Connecting local test execution to automated PR checks.

### Guided practice

Follow a request from `backend/app/main.py` into `stat_core`. Exercise valid and invalid inputs, inspect the supplied tests, and make a small test or validation change. Observe a controlled failing test, correct the issue, and verify passing local and CI runs.

### Mandatory homework: approximately 2 hours

Demonstrate tests for the group's declared processing behavior and invalid-input handling. Review the CI result and complete peer review of the related change.

**Progress checkpoint:** a working FastAPI backend with passing local tests and passing PR checks, plus visible validation and review evidence.

## Session 4: Containers, service orchestration, and output comparison

**Duration:** 3 hours

**Core technologies:** Docker, `python:3.12-slim`, Streamlit, HTTP requests, Docker Compose.

### Topics

- Reading the supplied Dockerfiles and understanding images and containers.
- Following CSV uploads and HTTP requests from Streamlit to FastAPI.
- Container networking and service names such as `http://backend:8000`.
- Service readiness and startup behavior.
- Comparing outputs across repeated local runs and local/container environments.

### Guided practice

Launch the supplied backend and frontend with `docker compose up --build`. Trace the service configuration and diagnose a controlled configuration or connection problem. Compare repeated local outputs, then compare local and Docker outputs under the declared criteria.

Multi-stage image optimization is an optional extension rather than a core requirement.

### Mandatory homework: approximately 2 hours

Prepare the group's full application and engineering evidence for the final presentation. Rehearse startup, CSV processing, tests, output comparisons, and navigation to PR and peer-review records.

**Progress checkpoint:** both services run together, and the group has evidence for repeatability and replicability.

## Session 5: Final showcase and live engineering review

**Duration:** 3 hours

**Format:** group demonstrations and questions about the workflow.

Each group will demonstrate its project and show the required evidence in its own repository. Every student must be able to explain their contribution and participation in pull requests and reviews. Presentation timings will be arranged to fit the number of groups.

### Required demonstration and evidence

- Launch the backend and frontend with `docker compose up --build`.
- Upload the group's CSV data through Streamlit, process it through FastAPI and the reusable package, and display results or a chart.
- Explain the connection between the interface, API, processing package, and container services.
- Show feature branches, descriptive commits, pull requests, and meaningful peer code reviews.
- Show each student's required authored PR and review of a teammate's PR.
- Show passing local tests and GitHub Actions checks.
- Demonstrate input validation and explain the relevant tests.
- Demonstrate matching repeated local runs and matching local/Docker outputs using the declared comparison criteria.
- Show environment and configuration hygiene, including appropriate ignore rules and a shareable configuration example.

## Assessment policy

Assessment is **pass/fail**. All engineering requirements above must be met; there are no weighted scores. Statistical analysis correctness is not graded. Students must still demonstrate that tests and output comparisons check the processing behavior they have declared.

All assessment takes place at the final presentation. There is no separate submission, resubmission, or reassessment. The final presentation result is final. Homework and session checkpoints support preparation for that presentation.

## Provisional classroom timing

Sessions 1–4 will initially allocate 45 minutes to explanation (including a 10-minute [device example](GLOSSARY.md) segment in Sessions 2–4), 30 minutes to demonstration, 90 minutes to guided practice, and 15 minutes to a break. Session 1 instead opens with about 35 flexible minutes for introductions and a motivating example, followed by a 10-minute device-example segment, 20 minutes of explanation, 20 of demonstration, a 15-minute break, and 80 of guided practice. This allocation may change as the materials develop. Session 5 uses a separate showcase schedule.

## Course materials and surveys

The [materials index](materials/README.md) links the Session 0 guide and instructor notes, the five editable PowerPoint decks and Markdown sources, four guided exercises, four homework briefs, five instructor notes, surveys, and final checklist. [Template instructions](docs/template.md) explain repository setup and permissions.

The [pre-course survey](materials/surveys/pre-course.md) covers prior experience, confidence, and setup readiness. The [post-course survey](materials/surveys/post-course.md) repeats relevant confidence and understanding questions and collects feedback. The surveys support course evaluation; they are not part of the pass/fail assessment.
