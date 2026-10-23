# Pre-course survey

## Before you begin

This survey helps the instructor understand your experience, plan the pace of the course, and arrange setup support. It also provides a starting point for comparing responses after the course. It is not graded and does not affect your pass/fail result. Assessment takes place at the final presentation, as described in the syllabus.

Allow about 10–15 minutes. Answer based on what you can do today, before studying the course materials. Unfamiliar tools and “not sure” answers are useful information. You may skip any question you do not wish to answer.

Write your responses in the blank cells or answer spaces. You can complete a copy of this Markdown file or a printed copy and return it privately through the instructor's existing course communication channel. No hosted survey service is needed. Do not commit completed responses to a shared repository.

Do not include your name, email, GitHub username, passwords, access tokens, private keys, or the contents of configuration files. For setup problems, describe the problem briefly without copying sensitive output.

**PAIR-01 — Optional comparison code:** Choose a random code of 8 letters or digits that does not come from personal details. Keep a private copy and use the same code on the post-course survey if you want your responses compared as a pair. Leave this blank if you do not want paired comparison.

Response: ____________________

## Prior experience

For each row, choose one experience code. Include coursework, personal work, and employment. Experience describes what you have done; the next section asks how confident you feel now.

| Code | Experience |
| --- | --- |
| 0 | I have not used this. |
| 1 | I have watched someone use it or read about it, but have not used it myself. |
| 2 | I have used it by following instructions or with help. |
| 3 | I have used it independently at least once. |
| 4 | I have used it independently on several tasks or projects. |

| ID | What have you used? | Response (0–4) |
| --- | --- | --- |
| EXP-01 | Python functions and pandas to clean, join, or summarize tables. | |
| EXP-02 | Git branches and commits to record changes. | |
| EXP-03 | GitHub pull requests and reviews of a teammate's code. | |
| EXP-04 | An isolated Python environment, such as `venv`, to install project dependencies. | |
| EXP-05 | Python modules and package installation, including a `pyproject.toml` file or an editable installation. | |
| EXP-06 | An API, such as FastAPI, to receive a request, validate input, and return a response. | |
| EXP-07 | Automated tests, such as pytest, to check processing behavior and invalid inputs. | |
| EXP-08 | Continuous integration (CI), such as GitHub Actions, to run checks when code changes. | |
| EXP-09 | Docker and Docker Compose to run connected services. | |
| EXP-10 | Streamlit to upload data and display results or a chart. | |

**EXP-11 — Optional context:** What experience would help the instructor understand your starting point? For example, have you mainly worked in notebooks, scripts, or shared projects?

Response: ____________________________________________________________

## Confidence today

For each row, answer: **How confident are you that you can do this today?** Choose one confidence code. Use 1 if the task is unfamiliar; use N if you cannot judge your confidence. These are self-reports, not demonstrations of skill.

| Code | Confidence |
| --- | --- |
| 1 | Not at all confident; I would need someone to walk me through it. |
| 2 | Slightly confident; I would need substantial help. |
| 3 | Moderately confident; I could do it with some help. |
| 4 | Confident; I could do it independently using documentation. |
| 5 | Very confident; I could do it independently and explain my choices. |
| N | Not sure; I cannot judge my confidence yet. |

| ID | Task | Response (1–5 or N) |
| --- | --- | --- |
| CONF-01 | Write a Python function that uses pandas to clean, join, or summarize tables. | |
| CONF-02 | Create an isolated Python environment and install a project's declared dependencies. | |
| CONF-03 | Explain which local settings belong in an ignored `.env` file and which examples can be shared in `.env.example`. | |
| CONF-04 | Make a change on a Git feature branch, write a descriptive commit, and open a pull request. | |
| CONF-05 | Review a teammate's pull request and give a useful comment about behavior, tests, or clarity. | |
| CONF-06 | Explain how reusable Python processing code is packaged and installed in editable mode. | |
| CONF-07 | Explain how an API receives data, rejects invalid input, and returns results. | |
| CONF-08 | Run pytest tests and use a failure message to investigate a problem. | |
| CONF-09 | Read a GitHub Actions check result and explain how it relates to local tests. | |
| CONF-10 | Launch connected backend and frontend services with Docker Compose and investigate a connection problem. | |
| CONF-11 | Trace uploaded CSV data from Streamlit through FastAPI to reusable processing code and back to displayed results. | |
| CONF-12 | Compare outputs from repeated local runs and from local and Docker runs, using exact checks for records and counts and a stated tolerance for calculated decimals. | |

## Understanding the three Rs

Different disciplines use these words differently. This course has its own definitions. Answer from your current understanding without looking up the glossary; “not sure” is a useful starting point. For each scenario, choose one answer from the same list:

| Code | Answer |
| --- | --- |
| A | Repeatability |
| B | Replicability |
| C | Reproducibility |
| N | Not sure |

**UNDER-01 —** You run the same processing code twice with the same input in the same local environment. You compare the outputs using declared criteria. Which principle is being checked?

Response (A, B, C, or N): ______

**UNDER-02 —** You run the same code and data in a local Python virtual environment and in Docker. You compare the outputs using declared criteria. Which principle is being checked?

Response (A, B, C, or N): ______

**UNDER-03 —** An independent simulation is built under very different conditions to investigate whether it agrees with the original result. Which principle does this illustrate under this course's terminology?

Response (A, B, C, or N): ______

## Tool and account readiness

Report the status of the computer and account you expect to use in class. This section helps arrange support; it is not an installation test or a request to finish setup while answering. If you have not checked something, choose U. Do not guess that a tool works just because it is installed.

For each row, choose one readiness code:

| Code | Readiness |
| --- | --- |
| R | Ready: I have checked that this works. |
| P | Partly ready: I have access or have installed it, but have not checked that it works. |
| H | Help needed: I do not have access, it is not installed, or I have tried and am blocked. |
| U | Unknown: I have not checked its status. |

| ID | Readiness check | Response (R, P, H, or U) |
| --- | --- | --- |
| READY-01 | I have a computer I can use during class and homework, with permission to install the course tools. | |
| READY-02 | I can use a terminal and a text editor to work with local Python files. | |
| READY-03 | I can run Python 3.12 on that computer and check its version. | |
| READY-04 | I can create a Python virtual environment with `venv` and install packages inside it with pip. | |
| READY-05 | Git is available on that computer, and `git --version` works. | |
| READY-06 | I have a GitHub account and can sign in to it. | |
| READY-07 | I can access GitHub repositories and create a repository from a template using my account. | |
| READY-08 | I can connect local Git to GitHub to clone a repository and push my own branch to a repository where I have write access. | |
| READY-09 | My account can use GitHub Actions in a repository where I have permission to enable workflows. | |
| READY-10 | Docker is installed and its engine can run on my computer; `docker info` succeeds. | |
| READY-11 | Docker Compose is available; `docker compose version` works. | |
| READY-12 | My network allows access to GitHub, Python package downloads, and container image downloads. | |

The course will use FastAPI, Pydantic, pytest, python-dotenv, and Streamlit as Python dependencies. Separate accounts for these packages are not required. Package installation will follow the supplied course setup instructions.

**READY-13 — Operating system:** Choose one: Windows / macOS / Linux / Other / Not sure. If useful, include the version. Do not include a device name or serial number.

Response: ____________________________________________________________

**READY-14 — Setup support:** If you chose H, P, or U, which question IDs need attention? Briefly describe any errors, installation restrictions, network limits, or access problems. If everything is ready, write “none.” Do not include credentials or raw configuration files.

Response: ____________________________________________________________

## What would help you learn?

**GOAL-01 —** What would you most like to be able to do by the end of this course?

Response: ____________________________________________________________

**GOAL-02 —** What concerns or practical support needs would you like the instructor to know about? You do not need to disclose personal or medical details.

Response: ____________________________________________________________

---

## Instructor notes — keep separate from student responses

Distribute the student sections above before teaching begins. Collect completed copies privately using an existing course channel; keep this answer key out of the student copy until responses are collected. Use readiness responses to offer setup help and experience responses to plan examples and pacing. No new survey service or student account is needed for collection.

### Stable items for the post-course survey

Repeat CONF-01 through CONF-12 and UNDER-01 through UNDER-03 with exactly the same question wording, IDs, answer options, and scales. Keep the confidence prompt and the explanation of N unchanged. Keep the three-R preamble and shared answer list unchanged. Store the survey phase (pre or post) separately from each question ID. If using paired responses, repeat PAIR-01 and let students supply their saved code without requesting their identity.

Keep the experience scale (0–4) separate from the confidence scale (1–5). Treat blank answers and N as missing or uncertain responses, never as zero or the lowest confidence rating. Compare paired responses only when the optional code matches uniquely; do not infer identities from other answers. Without a usable code, compare cohort summaries and report how many students answered each item. Confidence alone does not prove competence; interpret it alongside the understanding responses and the engineering evidence already required by the syllabus, without turning survey answers into assessment.

### Understanding guide

| ID | Course answer | Reason |
| --- | --- | --- |
| UNDER-01 | A — Repeatability | Successive runs of the same process under the same conditions are compared using declared criteria. |
| UNDER-02 | B — Replicability | The same process runs under slightly different conditions: a local virtual environment and Docker, with the same code and data. |
| UNDER-03 | C — Reproducibility | An independent simulation investigates agreement under very different conditions. |

These answers follow [GLOSSARY.md](../../GLOSSARY.md) and [SYLLABUS.md](../../SYLLABUS.md), rather than claiming universal terminology. Reproducibility is discussed conceptually; students are not required to build an independent simulation. The practical comparisons use exact agreement for cleaned records and counts and a declared numerical tolerance for calculated decimals. Use the understanding answers to identify topics to explain, not to award marks.
