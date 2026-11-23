# Post-course survey

## Before you begin

This survey supports course evaluation: it helps the instructor compare responses before and after the course and improve future teaching. It is not graded and does not affect your pass/fail result. Assessment takes place at the final presentation, as described in the syllabus.

Allow about 10–15 minutes. Answer based on what you can do today, after the course. You may skip any question you do not wish to answer. For the confidence and understanding sections, answer without looking up course materials or your earlier responses.

Write your responses in the blank cells or answer spaces. You can complete a copy of this Markdown file or a printed copy and return it privately through the instructor's existing course communication channel. No hosted survey service is needed. Do not commit completed responses to a shared repository.

Do not include your name, email, GitHub username, passwords, access tokens, private keys, or the contents of configuration files. Describe difficulties briefly without copying sensitive output or identifying classmates.

**PAIR-01 — Optional comparison code:** Choose a random code of 8 letters or digits that does not come from personal details. Keep a private copy and use the same code on the post-course survey if you want your responses compared as a pair. Leave this blank if you do not want paired comparison.

For this post-course copy, enter the code you saved from the pre-course survey. If you did not provide a code, cannot find it, or no longer want paired comparison, leave this blank; do not create a replacement code or supply identifying details.

Response: ____________________

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

## Course feedback

These questions ask about your experience of the course. Honest feedback, including difficulties and suggestions, helps improve teaching. You may answer even if you left the comparison code blank.

**FEED-01 — Workload:** The course planned approximately two hours of mandatory homework after each of Sessions 1–4 (eight hours total), alongside 14 hours 10 minutes of classroom time. About how many hours did you spend outside class after each session? Include setup, homework, group work, and presentation preparation. Enter an estimate, 0 if none, or “not sure.”

| After session | Approximate hours outside class |
| --- | --- |
| 1 | |
| 2 | |
| 3 | |
| 4 | |

Overall, how manageable was the workload? Choose one: Very difficult to manage / Difficult to manage / Manageable / Easy to manage / Not sure. What made it manageable or difficult?

Response: ____________________________________________________________

**FEED-02 — Pacing:** For each session, choose one: Much too slow / A little too slow / About right / A little too fast / Much too fast / Did not attend / Not sure.

| Session | Pace |
| --- | --- |
| 1 — Environment and Git | |
| 2 — A package others can install | |
| 3 — Tests and CI | |
| 4 — API, containers, and Compose | |
| 5 — Final showcase and engineering review | |

Which topics or activities needed more or less time? You can comment on the balance of explanation, demonstrations, guided practice, breaks, or showcase time.

Response: ____________________________________________________________

**FEED-03 — Useful activities:** Which activities or materials helped you learn most, and why? For example: the device example, demonstrations, guided exercises, homework, pull requests and peer review, investigating failures, output comparisons, or the final showcase. “None” or “not sure” is also useful feedback.

Response: ____________________________________________________________

**FEED-04 — Remaining difficulties:** Which tasks or concepts are still difficult? Describe where you get stuck and what explanation, example, or practice would help. You may refer to a CONF or UNDER question ID. Write “none” or “not sure” if appropriate.

Response: ____________________________________________________________

**FEED-05 — Improvements:** What should the instructor change, add, remove, or keep for the next course? Please give a concrete example if possible.

Response: ____________________________________________________________

---

## Instructor notes — keep separate from student responses

Distribute the student sections above at the end of the course. Collect completed copies privately through an existing course channel. Keep this guide out of the student copy until responses are collected. No collection infrastructure or analytics application is required; a private manual comparison is sufficient.

### Comparing pre-course and post-course responses

Use [the pre-course survey](pre-course.md) as the matching instrument. CONF-01 through CONF-12 and UNDER-01 through UNDER-03 retain its exact wording, IDs, scales, answer options, confidence prompt, explanation of N, and three-R preamble. Store the survey phase (pre or post) separately from each question ID.

Match responses only when the optional PAIR-01 code occurs uniquely in each phase. Leave blank, missing, duplicate, or unmatched codes unpaired; do not infer identities from other answers or ask students to reveal their identities. Without a usable code, compare cohort summaries and report how many students answered each item. Report the number of usable pairs separately, since respondents may differ between phases.

For each matched confidence item, compare the pre and post ratings and describe whether confidence increased, stayed the same, or decreased. Keep the 1–5 confidence scale separate from the pre-course 0–4 experience scale. Treat blank answers and N as missing or uncertain responses, never as zero or the lowest confidence rating. Report how many usable pairs support each comparison; do not calculate a numeric change when either response is blank or N.

For each understanding item, compare selected answers against the course guide below and note changes in answers or uncertainty. Report blank and N responses separately from substantive answers. These three questions provide limited evidence about the course terminology; they do not demonstrate the full engineering workflow.

Confidence alone does not prove competence. Interpret confidence alongside understanding responses and the engineering evidence already required by the syllabus. A lower confidence rating may reflect greater awareness of a task's difficulty. Changes in this small, voluntary survey do not by themselves establish that the course caused a change in skill. Survey answers remain outside assessment and must not alter pass/fail decisions.

Summarize workload and pacing responses, useful activities, remaining difficulties, and suggested improvements to plan future teaching. Avoid identifying students or quoting details that reveal them in shared summaries.

### Understanding guide

| ID | Course answer | Reason |
| --- | --- | --- |
| UNDER-01 | A — Repeatability | Successive runs of the same process under the same conditions are compared using declared criteria. |
| UNDER-02 | B — Replicability | The same process runs under slightly different conditions: a local virtual environment and Docker, with the same code and data. |
| UNDER-03 | C — Reproducibility | An independent simulation investigates agreement under very different conditions. |

These answers follow [GLOSSARY.md](../../GLOSSARY.md) and [SYLLABUS.md](../../SYLLABUS.md), rather than claiming universal terminology. Reproducibility is discussed conceptually; students are not required to build an independent simulation. The practical comparisons use exact agreement for cleaned records and counts and a declared numerical tolerance for calculated decimals. Use the understanding answers to identify topics to explain, not to award marks.
