# Final presentation: student brief and instructor checklist

## What you will demonstrate

Work in groups of three or four, using your own GitHub repository. Choose your
dataset and question independently; no topic approval is required. Modeling is
optional. Explain your declared processing behavior in plain English, then show
that the application, tests, comparisons, and collaboration evidence support it.

Assessment is pass/fail. Every engineering requirement below is mandatory;
there are no weighted scores. Statistical analysis correctness, scientific
conclusions, UI polish, and model complexity are not graded. Tests must still
check the processing behavior you declare. An independent simulation,
cross-group reproduction, and new-data experiments are not required.

The final presentation is the only assessment. There is no separate submission,
resubmission, reassessment, or later retry during the final session. The result
at your presentation is final. Homework and earlier checkpoints are preparation.

## Prepare and present

Use the [group template guide](../../docs/template.md) and
[collaboration guide](../../docs/collaboration.md). Before the session, rehearse
the startup, CSV workflow, validation, tests, and comparisons on your chosen
code and inputs. Ensure the instructor can access your repository and evidence.
Finish edits before capturing comparisons; identify the demonstrated commit SHA.

Keep evidence links in your group's README for navigation during the presentation;
this is not a separate assessed submission. Link the tested commit, CI run,
comparison captures/logs, PRs, and review permalinks. Record commands, input paths
or hashes, environment details, and outcomes so the evidence can be inspected.
Retain any CI artifacts needed for the presentation before they expire.

During your slot:

1. State your dataset, question, and expected processing behavior briefly.
2. Run `docker compose up --build` live from the group repository. Show readiness,
   upload your CSV input through Streamlit, process it through FastAPI and your
   reusable package, and show visible results or a chart. Explain the service
   communication; a Compose file alone is not evidence of working containers.
3. Demonstrate a rejected invalid input and explain the validation rule and test.
4. Show passing local tests, the matching GitHub Actions run, and both output
   comparisons. Open the underlying outputs and explain the agreement rules.
5. Open the repository history, PRs, and substantive reviews. Every student
   explains their own contribution, authored PR, and review of a teammate's PR.

Use [Compose instructions](../../docs/compose.md) for readiness and communication
checks. The supplied example uses `http://backend:8000` from the frontend
container; `localhost` there means that frontend container. The host browser
opens `http://127.0.0.1:8501`. Show actual CSV results and service evidence,
not only slides or configuration screenshots. Stop standalone servers first
if they occupy the same host ports.

Use [testing instructions](../../docs/testing.md) for `python -m pytest backend/tests`
in the activated local environment. Open the GitHub Actions run for the
demonstrated commit; a local pass does not establish a hosted CI pass.

Follow [output comparison instructions](../../docs/comparisons.md), adapting input
paths and declared behavior to your dataset. Use unchanged code and the same
CSV bytes for two local runs, then compare local and real Docker outputs:

- Repeatability: compare local run 1 with local run 2 under the same conditions.
- Replicability: compare that local result with the same process in Docker.
- Compare cleaned records, identifiers, raw values, copied baselines, counts,
  types, structure, and ordering exactly. Preserve nulls; missing is not zero.
- Apply declared tolerances only to derived decimal values, documented in tests.
  In the supplied example, only `change`, `percent_change`, and visit-summary
  `mean` use `abs(actual - expected) <= max(1e-9, 1e-9 * abs(expected))`.
  The first output is the reference; raw values never gain this tolerance.
- Show both successful comparisons and their captures, code/input identity,
  environment details, commands, and logs. Explain a mismatch using the relevant
  test or comparison diagnostic; do not round away differences or widen a
  tolerance just to pass. Matching charts alone do not establish agreement.

See the [course glossary](../../GLOSSARY.md) for these course-specific R meanings.

## Three-hour schedule

Let `G` be the actual number of groups, each with three or four students. Reserve
10 minutes for the opening brief, 15 minutes for a shared break between group
slots, and 5 minutes for closing. Each group receives `S = 150 / G` minutes.
The total is `10 + 15 + 5 + G * (150 / G) = 180` minutes.

Within each slot, allocate `S / 2` to the live demo, `S / 3` to evidence inspection,
and `S / 6` to questions, including individual explanations. These fractions
sum to one slot. Publish start/end times once `G` is known; retain fractional
minutes or use seconds so rounding does not extend the session. Include startup
and transitions inside each slot. Put the break at a slot boundary and keep
the closing period within the reserved five minutes.

## Instructor: mandatory pass/fail evidence record

Record group/repository URL, date, demonstrated commit SHA, member names and
GitHub usernames. For each row record Pass or Fail and an evidence URL/path
plus a short observation. Missing evidence is a failure of that requirement.
Inspect the actual artifacts during the presentation rather than accepting a
claim that they exist. Use these rows for all groups without adding scores.

| Mandatory requirement | Evidence to inspect during the presentation |
| --- | --- |
| Isolated environment and package setup | Show Python 3.12 in an active `venv`, its interpreter path, dependency declarations in `backend/pyproject.toml`, and the installed reusable package working locally. |
| Configuration hygiene | Open ignore rules and a shareable `.env.example`; confirm local `.env`, credentials, and `.venv` are kept out of tracked files/history. Explain local versus container configuration without displaying secrets. |
| Separate package, API, and UI | Trace one CSV request from Streamlit through FastAPI to reusable processing functions. Show that processing is independent of HTTP and UI code; explain inputs and returned results. |
| Real Compose startup and service communication | Observe `docker compose up --build`, running frontend/backend services and backend readiness. Inspect frontend-to-backend HTTP communication over the Compose network, the configured service address, and relevant logs/health responses. |
| CSV upload and visible results | Observe the group's CSV upload in Streamlit and successful API/package processing. Inspect visible results or a chart and relate them to the declared behavior. |
| Input validation | Observe an invalid input rejected clearly, explain types/bounds/missingness rules, and open the corresponding passing API validation tests. Invalid input must not appear as a successful result. |
| Passing local tests and CI | Inspect passing local pytest output and a successful GitHub Actions run for the demonstrated commit. Open tests at the public processing/API/comparison boundaries to check declared behavior and invalid inputs. CI reporting alone does not configure required checks. |
| Repeatability | Inspect two same-input, same-code local captures under the same conditions and their successful comparison, with commands, environment details, and code/input identity. |
| Replicability | Inspect successful local versus real Docker comparison of the same code and input, with captures and execution logs. A simulated container or matching charts is insufficient. |
| Explicit agreement rules | Inspect exact records/raw values/baselines/counts/null handling and derived-only tolerances documented in tests. Missing values remain distinct from zero; comparisons cannot drop fields or round mismatches away. |
| Repository workflow and meaningful reviews | Open feature branches, descriptive commits, PRs, and teammate reviews addressing behavior, tests, or clarity. Inspect responses/follow-up where concerns were raised; approval alone or “looks good” is insufficient. |
| Every individual's participation | For EACH student, verify at least one personally authored PR and at least one substantive review of a teammate's PR, with authorship and review permalinks. Hear each student's explanation. Template history or instructor/agent work does not count. |

Copy this individual evidence row for every member; complete it during the slot:

| Student / GitHub username | Authored PR URL | Teammate's PR / review permalink | Explanation observed | Pass / Fail |
| --- | --- | --- | --- | --- |
| | | | | |

Award Pass only when every mandatory group requirement passes and every student
meets the individual participation requirement. Record any failed row and the
reason at the presentation. Do not average requirements, award complexity
bonuses, or offer a later retry. Apply the
[syllabus assessment policy](../../SYLLABUS.md#assessment-policy) consistently.
