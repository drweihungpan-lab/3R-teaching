# Session 3 guided practice: tests and automated CI

Spend about 40 minutes in your group of three or four, in your **Backend repo**. You will switch on the test job in CI, add a validation with tests, and watch a controlled failing test turn CI red and green again. This is preparation for the final presentation, not a separate submission; rotate roles so every student authors a PR and reviews a teammate's.

## Before you start

Be in your Backend repo with the `.venv` from Session 2 active and `main` up to date:

```bash
git switch main
git pull --ff-only origin main
python -m pip install -e '.[test]'
git switch -c session-3/your-name-tests
```

| Time | Activity | Checkpoint |
| --- | --- | --- |
| 0–10 min | Switch on the test job, push, open a PR | Two checks appear on the PR |
| 10–25 min | Add a validation and tests | `make test-all` passes locally |
| 25–35 min | Controlled failure | A red check, then a green one |
| 35–40 min | Review and record | A teammate's review, CI link noted |

## 1. Switch on the test job — 10 minutes

Open `.github/workflows/github_actions.yml`. Find the `test-pytest` job, commented out with `# `. Select its lines and toggle the comment in your editor. Leave the OPTIONAL release job commented. Check the YAML spacing is unchanged, then:

```bash
git add .github/workflows/github_actions.yml
git commit -m "Switch on the pytest job"
git push -u origin session-3/your-name-tests
```

Open a PR. It now shows two checks: **test-formatting-linting** and **test-pytest**. Both should pass because the supplied tests already exist.

## 2. Add a validation and tests — 15 minutes

In `src/<package>/model.py`, make `load_counts` reject a negative `daily_count`. After the missing-column check add:

```python
    if (counts["daily_count"] < 0).any():
        raise ValueError(f"{label} has negative daily_count values")
```

In `tests/unit/test_model.py` add a fixture, a test that uses it, an approximate comparison, and an invalid-input test:

```python
@pytest.fixture
def counts():
    return load_counts(DATA)


def test_mean_daily_count_of_device_b_is_close_to_210(counts):
    mean = counts.loc[counts["device_id"] == "DEV-B", "daily_count"].mean()
    assert mean == pytest.approx(210, rel=0.02)


def test_negative_count_is_rejected(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("device_id,date,daily_count\nDEV-A,2025-01-01,-5\n", encoding="utf-8")
    with pytest.raises(ValueError, match="negative"):
        load_counts(bad)
```

Then format and check everything:

```bash
make format
make test-all
```

Commit and push. Why is the mean compared with a tolerance, while the limit dates are compared exactly? Explain it to a teammate.

## 3. A controlled failure — 10 minutes

In the pinned-dates test, change one expected date, for example `date(2026, 4, 1)` to `date(2026, 4, 2)`. Push and open the failing check on the PR. Find the line that shows the expected and actual dates. Restore the date, push again, and confirm the check turns green on the latest commit.

## 4. Review and record — 5 minutes

Ask a teammate to review the PR with a specific comment about the tests or clarity. Record the PR and the green CI run link in your group README. Merge after approval.

## Checkpoint

Passing local tests and passing CI in your Backend repo, with a review on the PR. Finish anything unfinished at home, in addition to the homework.
