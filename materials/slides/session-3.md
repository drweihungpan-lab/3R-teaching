# Session 3: Tests and automated CI

Protect the behavior you declared, and let GitHub check it for you.

- Write tests for expected results and for invalid input.
- Switch on the test job already waiting in your CI workflow.
- Read a red check, fix it, and see it turn green.

---

## Our 170-minute agenda

- 00–10: Back at the bubble tea shop; device example Stage 5.
- 10–60: Explanation — what a test is, pytest, fixtures, tolerances, invalid input.
- 60–70: Break — 10 minutes.
- 70–130: Demonstration — add tests, switch on CI, a controlled failure.
- 130–170: Hands-on — in your Backend repo.

Unfinished practice continues at home, in addition to the homework.

---

## Back at the bubble tea shop

**A customer orders a tea with −20% sugar. What do you do?**

---

## Device example, Stage 5: tests and CI

- Stage 4's package gains tests. One test pins the expected limit date for each device on the fixed synthetic data.
- CI runs the tests on every push and pull request.
- The same "cleanup" as last session (drop zero-count days) now arrives as a pull request:

```text
FAILED test_limit_dates_are_pinned_for_the_fixed_synthetic_data
3 failed, 3 passed   CI: red
```

- The check catches exactly the bug that slipped through before. `main` stays green.
- Stage 5 also runs from any folder: the data path no longer depends on where you stand.
- Files: the `device-example` folder of the [Sandbox](https://github.com/drweihungpan-lab/3R-sandbox).

---

## A test states what you expect

A test calls your code with a known input and checks the result.

```python
def test_limit_dates_are_pinned_for_the_fixed_synthetic_data():
    assert predict_limit_dates(load_counts(DATA)) == EXPECTED_LIMIT_DATES
```

- The expected values are written down in advance, from an independent source.
- A passing test says the behavior still holds. It does not prove the statistics are right.
- Test behavior callers can observe, not how the function is built inside.

---

## pytest finds and runs tests

- Files named `test_*.py` and functions named `test_*` are collected automatically.
- `pytest` prints a dot per pass and an `F` per failure, then a summary.
- A failing line shows the expected and actual values side by side.
- Your repo has `tests/unit` and `tests/integration`; `make test-pytest` runs both.

```bash
pytest -q
pytest tests/unit -k pinned
```

---

## Fixtures provide reusable inputs

A fixture builds an input once and hands it to every test that asks for it.

```python
@pytest.fixture
def counts():
    return load_counts(DATA)

def test_pinned_dates(counts):
    assert predict_limit_dates(counts) == EXPECTED_LIMIT_DATES
```

- The test names the fixture as an argument; pytest supplies it.
- Use `tmp_path` for files a test creates, so nothing leaks between tests.

---

## Declare exact and approximate agreement

- Exact: identifiers, dates, order, counts, and copied baselines.
- Approximate: only calculated decimals such as means.

```python
assert mean == pytest.approx(210, rel=0.02)
```

- `rel=0.02` allows a 2% difference. Say why that is acceptable in a comment or the test name.
- The limit dates in this course are whole days, so they are compared exactly.
- This is an engineering rule, not a statistical threshold.

---

## Invalid input must fail clearly

Test the bad cases as deliberately as the good ones.

```python
def test_negative_count_is_rejected(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("device_id,date,daily_count\nDEV-A,2025-01-01,-5\n")
    with pytest.raises(ValueError, match="negative"):
        load_counts(bad)
```

- The error message should say what is wrong and where.
- The command-line tool turns the error into a readable message, not a stack trace.

---

## Connect checks to the course's three Rs

- Repeatability: agreement across runs under the same conditions.
- Replicability: agreement under slightly different conditions, such as a Release installed on another machine, or local versus Docker.
- Reproducibility: agreement under very different conditions, such as an independent simulation; conceptual here.
- Passing CI alone does not compare local and Docker outputs. Session 4 does that.

Read the [glossary](../../GLOSSARY.md) for the definitions.

---

## Switch on the test job

Open `.github/workflows/github_actions.yml`. The `test-pytest` job is commented out with `# `.

- Select its lines and toggle the comment in your editor (`Ctrl+/` or `Cmd+/`).
- Leave the OPTIONAL release job commented.
- Commit and push on a branch; the pull request now shows two checks.

```text
test-formatting-linting   passes
test-pytest               passes
```

---

## Reporting a check is different from requiring it

A green check reports one commit's result. A repository rule can *require* it before merging.

- Look at the merge box: does it block when a check fails?
- Required checks and approvals are set in the repository's branch protection settings.
- Check the latest commit: new commits start new check runs.

See GitHub's [protected branches guide](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

---

## Demo: add a validation and its test

In `src/<package>/model.py`, `load_counts` rejects a negative `daily_count`:

```python
if (counts["daily_count"] < 0).any():
    raise ValueError(f"{path} has negative daily_count values")
```

Add the test from the earlier slide, then run:

```bash
make format
make test-all
```

---

## Demo: a controlled failure

Change one expected date in a test, for example `date(2026, 4, 1)` to `date(2026, 4, 2)`, and push.

```text
FAILED tests/unit/test_model.py::test_limit_dates_are_pinned_for_the_fixed_synthetic_data
{'DEV-B': date(2026, 4, 1)} != {'DEV-B': date(2026, 4, 2)}
```

- The pull request shows the red check; the log shows the same message.
- Restore the date, push again, and the check turns green.

---

## Hands-on: 40 minutes

- 10 minutes: switch on the test job in a branch, open a pull request, see both checks.
- 15 minutes: add the validation and its test, plus one fixture test of your own.
- 10 minutes: the controlled failure — break, read the red check, fix.
- 5 minutes: request a teammate's review and record the CI link.

Use [the exercise](../exercises/session-3.md) when stuck.

---

## Checkpoint and next step

Today's checkpoint: passing local tests and passing CI in the Backend repo, with a review on the pull request.

- Mandatory homework is approximately two hours; details will be posted separately.
- Next session: put an API in front of the same function, containerize it, and run it with the supplied frontend.

See the [syllabus](../../SYLLABUS.md).
