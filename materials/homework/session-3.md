# Session 3 homework: tests your group can explain

Complete **120 minutes of mandatory homework** after [Session 3 guided practice](../exercises/session-3.md), in your group of three or four. Demonstrate tests for one small processing behavior and invalid-input handling relevant to your group's chosen dataset and question. Keep passing local and CI evidence and a meaningful teammate review in your group repository.

Choose your dataset and question independently; no topic approval is required. Modeling is optional and complexity earns no extra credit. Tests check declared engineering behavior, not the scientific validity of your conclusions. Assessment is pass/fail at the final presentation only; statistical analysis correctness is not graded. Homework prepares that evidence: there is no separate submission, resubmission, reassessment, or later retry. See the [syllabus](../../SYLLABUS.md).

## Preparation

Have your group repository, Python 3.12 virtual environment with backend development dependencies, Git, editor, GitHub access, and a teammate available for review. Reuse [setup](../../docs/setup.md), [testing guidance](../../docs/testing.md), and [CI guidance](../../docs/ci.md). Start from the group's agreed current `main`, preserve unrelated work, and activate `.venv` (`source .venv/bin/activate` on macOS/Linux; `.venv\Scripts\Activate.ps1` in PowerShell). All commands run from the group repository root.

Use a tiny shareable or synthetic fixture representing your own data; keep private data, `.env`, `.venv`, and generated outputs out of commits. Keep the supplied healthcare CSVs unchanged. Its public `process_csv` accepts CSV text with the [documented healthcare contract](../../docs/api.md), not arbitrary CSVs. For other datasets, test your group's existing public processing function; do not rename unrelated columns into healthcare fields. If adaptation is unfinished, test one small reusable preparation rule for your real data and record the remaining API/UI work.

| Minutes | Task | Evidence |
| --- | --- | --- |
| 0–15 | Prepare and plan participation | Branch; author/reviewer assignments |
| 15–35 | Declare behavior and fixtures | Own-data example, literal expectations, invalid case |
| 35–75 | Add and run focused tests | Processing and rejection results; explained failure/correction |
| 75–95 | Run the suite and inspect CI | Local output; passing check URL and commit |
| 95–115 | Review and respond | Meaningful review and response |
| 115–120 | Save evidence and self-check | Links and outstanding-work plan |

## 1. Prepare and assign participation — 15 minutes

Check `git status --short` and `python --version`, then create your own feature branch (replace `your-name` and `purpose`):

```bash
git switch -c homework-3/your-name-purpose
python -m pytest backend/tests
```

Save the baseline result. If imports or dependencies fail, repair setup before editing tests. Every student must author at least one PR and meaningfully review at least one teammate's PR by Session 5. Record each person's authored-PR link or planned small change/session and review link or assigned teammate/session in existing group notes. Rotate reviewers, for example A → B → C → A, including D for a group of four. One shared PR does not establish every member's authorship. Use separate small changes to avoid overlapping edits.

## 2. Declare behavior and inputs — 20 minutes

In your PR draft or existing notes, state your dataset/question, input version, public function, and one processing rule that matters to it. Declare a tiny valid input and independently worked expected output, plus an invalid input and expected rejection. Include relevant join keys, types, units, bounds, and missingness rules. Missing must stay distinct from zero.

Read [conftest.py](../../backend/tests/conftest.py), [processing tests](../../backend/tests/test_processing.py), and [validation tests](../../backend/tests/test_validation.py). A pytest fixture supplies reusable inputs. Define your fixture's records independently of production parsers/constants. Use literal expected values from the declared rule or a hand-worked example; do not compute expectations by calling the implementation being tested. For example, values 10 and 20 have mean 15, independently of your processing function.

Compare records, identifiers, counts, units, and nulls exactly. For calculated decimals, document and justify a tolerance in the test. The supplied example uses `pytest.approx(expected, rel=1e-9, abs=1e-9)`: it allows the larger of the relative and absolute limits. Absolute tolerance has the output's units; relative tolerance is dimensionless. Do not round results or widen tolerance to hide a failure. Apply a reasoned rule to your own data, rather than treating this engineering tolerance as a scientific threshold.

## 3. Add focused tests — 40 minutes

Add a small pytest case under `backend/tests` calling the public processing function and asserting the declared returned values, including a relevant missing-value or count rule. Add an invalid-input case through that same public function, checking the documented exception and useful error details. For the supplied function, inspect `InvalidInputError.issues`; do not call private validation helpers. If your change concerns HTTP handling, use the existing [API tests](../../backend/tests/test_api.py) as the pattern: assert status and response/error fields through `TestClient`, without starting a server. Avoid assertions about helper calls or code layout.

Run each selected test using its actual file and test name with `python -m pytest`, then the full suite below. If behavior needs a change, take one case at a time: observe its failure, explain the mismatch, make the smallest correction, and rerun it. Existing correct behavior may pass a new test immediately; retain the explained controlled failure/correction from guided practice rather than inventing a bug. Preserve actual output and explain what each test catches. Never leave a deliberately failing expectation in the final diff.

## 4. Verify locally and on the PR — 20 minutes

```bash
python -m pytest backend/tests
git diff --check
git diff
git status --short
```

Expect all collected tests to pass; totals can grow as tests are added. Record the command, actual summary, warnings, interpreter, and commit. Stage only your explicit changed paths with `git add`, commit descriptively, and push your branch with `git push -u origin HEAD`. Open a PR to your **group repository's `main`** describing the behavior, tests, expectations, and observed results.

Inspect **Checks → Backend tests → Run backend tests** for the current PR head commit. Save its successful run URL and SHA. A local pass or workflow file is not hosted CI evidence. Read setup/install logs if failure precedes pytest; fix actual failures and rerun affected checks. Required-check protection is a separate repository setting from CI reporting. Local and CI passes alone do not demonstrate local/Docker replicability under the [course glossary](../../GLOSSARY.md).

## 5. Review and respond — 20 minutes

Review a teammate's diff and have a teammate review yours. Rerun the focused test and check the expectation independently. Leave a specific comment on behavior, missingness, rejection details, fixture independence, tolerance, or clarity; approval alone is insufficient. For example, identify why an invalid type is rejected or whether a null could accidentally pass as zero. Respond to feedback, make needed edits, and rerun focused/full checks and CI for the new head commit before following the group's reviewed merge workflow.

If access, CI, or review is delayed, keep the PR open and record the missing step, owner, and next working session. Do not claim completion of an unperformed check or review; this plan does not replace the final evidence requirement.

## 6. Evidence and self-check — 5 minutes

Keep links in the PR or existing group notes: dataset/question and fixture; declared rule and literal expectations; processing and invalid-input test names; exact local command/output and explained failure/correction; successful CI URL/SHA; meaningful review and response; every person's authored-PR/review links or remaining participation plan.

- Can I explain how the tests exercise our own data-processing rule through a public interface?
- Are expectations independent, missingness preserved, invalid input rejected, and decimal tolerances justified?
- Can a teammate find passing local results and CI for the current commit, plus review feedback and my response?
- Does every student have authored-PR and review evidence, or a concrete plan before Session 5?

Retain this evidence for the final presentation alongside the later service-startup and output-comparison work. There is no separate homework hand-in.
