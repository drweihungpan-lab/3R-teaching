# Repeatability, Reproducibility, and Replicability

## Course overview

This practical course introduces the engineering framework and collaborative workflow used to make statistical data processing repeatable and portable. Students learn how environments, reusable Python packages, tests, code review, automated checks, APIs, and containers fit together.

The emphasis is on understanding and using the workflow. Building a sophisticated model or designing a polished interface is not the goal. One running example, the [device example](GLOSSARY.md), supports every session: synthetic daily measurement counts for medical devices, used to predict when each device reaches its usage limit. It grows through seven stages from a messy notebook to a containerized application. Groups apply the framework to their own datasets and questions in the final project.

The course uses four repositories (see [GLOSSARY.md](GLOSSARY.md) for the terms):

| Repository | Owner | Role |
| --- | --- | --- |
| This repository (3R-teaching) | Instructor | Materials only: syllabus, slides, exercises, instructor notes, glossary, decisions |
| **Sandbox** (`3R-sandbox`) | Instructor, class-wide | Session 1 Git practice, with `main` protected and a branch per group; also holds the device example's seven stage folders. Nothing in it counts as final-project evidence |
| **Backend repo** | Each group, public | Created in Session 2 from the course cookiecutter; holds the group's package, command-line tool, tests, API and container setup |
| **Frontend repo** | Instructor | One generic CSV-upload page. Groups build it from a pinned release in their Compose file and do not fork it |

## Audience and workload

- **Audience:** 20 statistics students familiar with Python functions, pandas, and basic regression.
- **Classroom time:** 14 hours 10 minutes across five sessions of 170 minutes each (see [session shape](#session-shape)).
- **Mandatory homework:** approximately two hours after each of Sessions 1–4, eight hours in total. Guided practice not finished in class is completed at home, in addition to this time. Homework content is to be defined.
- **Group size:** three or four students, with one public Backend repo per group.
- **Language:** English.

## The three Rs in this course

Terminology varies across disciplines. This course uses the definitions in [GLOSSARY.md](GLOSSARY.md).

| Principle | Course meaning | Course activity |
| --- | --- | --- |
| Repeatability | Matching results under the same conditions | Run the same pipeline twice using the same input and local environment |
| Replicability | Matching results under slightly different conditions | Install a teammate's Release into a fresh environment, and run the same code locally and in Docker, then compare outputs |
| Reproducibility | Matching results under very different conditions, such as an independent simulation | Discuss conceptually; an independent simulation is not required |

The practical focus is repeatability and replicability. Cleaned records and counts must match exactly. Calculated decimal values must agree within a stated numerical tolerance documented in the tests. Cross-group reproduction and new-data experiments are not required.

## Learning outcomes

By the end of the course, students should be able to:

1. Use an isolated Python environment and explain how configuration and dependencies affect execution.
2. Collaborate through feature branches, descriptive commits, pull requests, and meaningful peer reviews.
3. Generate a package from a template, explain how its modules, metadata, and command-line entry point fit together, tag a Release, and install a Release from a git URL.
4. Run tests for declared processing behavior and invalid inputs, and interpret local and CI failures.
5. Connect the processing package to a FastAPI service and launch it with the Frontend repo using Docker Compose, explaining how the services communicate.
6. Demonstrate repeatability and replicability with explicit output comparisons.

## Session shape

Every session has the same shape, 170 minutes in all:

| Block | Minutes | Content |
| --- | --- | --- |
| Instruction 1 | 60 | Explanation and demonstration, opened by the device-example segment |
| Break | 10 | |
| Instruction 2 | 60 | Explanation and demonstration |
| Hands-on | 40 | Guided practice in groups |

Guided practice not finished in the 40 minutes continues at home. Session 5 keeps the 170-minute length with a showcase schedule.

## Teaching approach and projects

The [device example](GLOSSARY.md) is the one dataset used in class. It is synthetic, generated with a fixed seed, and documented in the Sandbox. Its Stage 4 processing code is the basis of the package every group generates in Session 2, and the same data and predictions carry through the tests, the API, and the Docker comparison, so outputs can be compared across groups.

Each group will independently select its own dataset and statistical question for the final project. Topic approval is not required; groups may discuss their selected topic with the instructor. Cleaning, processing, summaries, visualization, and modeling are possible project activities. Modeling is optional, and complexity earns no additional credit.

FastAPI, the Frontend repo's Streamlit page, and Docker Compose are required parts of every group's application. Students author backend code only; the Frontend repo is supplied.

Each student must author at least one pull request in their group's Backend repo and review at least one teammate's pull request there. Reviews must address behavior, tests, or clarity rather than provide approval alone. The instructor will inspect this evidence in each group's repository. Practice in the Sandbox does not count.

Group repositories are public. They must never contain real or sensitive data or secrets.

## Session 0: Required self-paced setup (pre-course)

**Duration:** none in class. This is a pre-course requirement, separate from the five sessions.

Students complete the [Session 0 guide](docs/session-0.md) at home: a GitHub account, a terminal (Mac Terminal, or WSL with Ubuntu 24.04 LTS on Windows), Git, an SSH key connected to GitHub, Python 3.12 and VS Code. They then check in by commenting the output of three commands on a pinned issue in the Sandbox, by **3 days before Session 1**. Session 0 does not teach commit or push. See the [instructor notes](materials/instructor/session-0.md) and the [decision record](docs/adr/0001-wsl-and-ssh-for-all-students.md).

## Session 1: Environment isolation and modern Git

**Duration:** 170 minutes

**Core technologies:** Python 3.12, `venv`, Git, GitHub pull requests, `python-dotenv`.

### Topics

- Isolated virtual environments versus global package installations.
- Feature branches, descriptive commits, pull requests, and merge conflicts.
- The collaboration path: feature branch → pull request → peer review → merge into `main`.
- Configuration hygiene: `.gitignore`, local `.env` files, and shareable `.env.example` files.
- Public repositories and why no real or sensitive data belongs in them. A preview of "required checks" protecting `main`, which Session 2 introduces.

### Guided practice

In the Sandbox, create a branch named `group-N/topic`, make a change in the practice folder, open a pull request, review a teammate's pull request with a specific comment, and resolve the deliberate merge conflict. There is no CI in Session 1.

### Mandatory homework: approximately 2 hours

To be defined.

**Progress checkpoint:** every student has opened a pull request and given a review in the Sandbox, and the group has chosen its Backend repo name.

## Session 2: A package other people can install

**Duration:** 170 minutes

**Core technologies:** cookiecutter, `setup.cfg` packaging, `click`, Python logging, git tags, `pip install git+`, GitHub Actions (first look).

### Topics

- From scripts to modules: the device example's Stage 3 → Stage 4 story.
- What a cookiecutter template is and what its prompts change.
- Package metadata, dependencies, a command-line entry point with `--input` and `--output`, and the version string.
- A Release: version bump, git tag, and installing a pinned version with `pip install git+https://…@v0.1.0` ([decision record](docs/adr/0002-distribute-by-git-tag-not-registry.md)). PyPI and TestPyPI are discussed as what a mature package would use.
- A very quick look at CI: automatic lint and format checks on every push.

### Guided practice

Generate the group's Backend repo with the course cookiecutter, run the command-line tool on the device CSV, push, change the version, tag a Release, and install a teammate's Release into a fresh virtual environment. Check the output against the instructor's reference checksum.

### Mandatory homework: approximately 2 hours

To be defined.

**Progress checkpoint:** each group has a public Backend repo with a tagged Release that another group's member installed and ran, matching the reference checksum.

## Session 3: Defensive engineering with pytest and CI

**Duration:** 170 minutes

**Core technologies:** pytest, fixtures, `pytest.approx`, GitHub Actions.

### Topics

- Declared processing behavior and invalid-input handling as tests.
- Shared test fixtures and explicit numerical tolerances.
- Switching on the commented-out test job in the CI workflow; reading CI results.

### Guided practice

Add tests to the group's Backend repo, switch on the pytest job, observe a controlled failing test turn CI red, fix it, and verify green.

### Mandatory homework: approximately 2 hours

To be defined.

**Progress checkpoint:** passing local tests and passing CI in the Backend repo, plus visible review evidence.

## Session 4: FastAPI, containers, and service orchestration

**Duration:** 170 minutes

**Core technologies:** FastAPI, Pydantic, Docker, `python:3.12-slim`, Streamlit (supplied), Docker Compose.

### Topics

- Hour one: adding an API to the Backend repo as an optional install extra; request and response schemas as a contract; one processing function behind two interfaces (command line and API).
- Hour two: the Dockerfile, images and containers, container networking and service names such as `http://backend:8000`, readiness, and building the Frontend repo from a pinned release in Compose.
- Comparing outputs across repeated local runs and local/container environments (homework).

### Guided practice

Run `docker compose up --build` with the supplied Frontend repo, trace a CSV upload from the page to the API and back, and diagnose one controlled configuration or connection fault.

### Mandatory homework: approximately 2 hours

To be defined; includes preparing the local-versus-Docker output comparison for Session 5.

**Progress checkpoint:** both services run together from the Backend repo.

## Session 5: Final showcase and live engineering review

**Duration:** 170 minutes

**Format:** group demonstrations and questions about the workflow.

Each group will demonstrate its project and show the required evidence in its own Backend repo. Every student must be able to explain their contribution and participation in pull requests and reviews. Presentation timings will be arranged to fit the number of groups.

### Required demonstration and evidence

- Launch the backend and the Frontend repo's page with `docker compose up --build`.
- Upload the group's CSV data through the page, process it through FastAPI and the package, and display results.
- Explain the connection between the page, API, processing package, and container services.
- Show feature branches, descriptive commits, pull requests, and meaningful peer code reviews in the Backend repo.
- Show each student's required authored PR and review of a teammate's PR.
- Show tagged Releases and a successful install of a Release from its git URL.
- Show passing local tests and GitHub Actions checks.
- Demonstrate input validation and explain the relevant tests.
- Demonstrate matching repeated local runs and matching local/Docker outputs using the declared comparison criteria.
- Show environment and configuration hygiene, including appropriate ignore rules and a shareable configuration example.

## Assessment policy

Assessment is **pass/fail**. All engineering requirements above must be met; there are no weighted scores. Statistical analysis correctness is not graded. Students must still demonstrate that tests and output comparisons check the processing behavior they have declared.

All assessment takes place at the final presentation. There is no separate submission, resubmission, or reassessment. The final presentation result is final. Homework and session checkpoints support preparation for that presentation.

## Course materials and surveys

The [materials index](materials/README.md) links the Session 0 guide and instructor notes, the five editable PowerPoint decks and Markdown sources, four guided exercises, five instructor notes, surveys, and final checklist.

The [pre-course survey](materials/surveys/pre-course.md) covers prior experience, confidence, and setup readiness. The [post-course survey](materials/surveys/post-course.md) repeats relevant confidence and understanding questions and collects feedback. The surveys support course evaluation; they are not part of the pass/fail assessment.
