# Backend continuous integration

[Backend CI](../.github/workflows/backend-tests.yml) runs the existing
[backend test suite](testing.md) with Python 3.12 on a GitHub-hosted Ubuntu runner.
Every pull request runs it, regardless of its target branch. Pushes to `main` and
the temporary course-authoring integration branch `implement/course-framework`
also run it. This makes integration PR checks visible before changes reach
`main`; students continue to use feature branches and PRs into `main`.

The job is named **Backend tests**. It checks processing results, rejected inputs,
and API requests/responses. A second job, **Docker output
comparison**, compares local and container outputs; see [comparisons](comparisons.md).

## What the workflow does

After checkout and Python setup, it runs these commands from the repository root:

```bash
python -m pip install -e './backend[dev]'
python -m pytest backend/tests
```

The `dev` extra in [backend/pyproject.toml](../backend/pyproject.toml) declares
pytest and the API test client dependency alongside the backend dependencies.
The pip download cache is keyed against that metadata; changing dependencies
changes its key. A cache hit still runs installation. It does not lock dependency
versions or guarantee an identical environment. See the official
[setup-python caching documentation](https://github.com/actions/setup-python#caching-packages-dependencies).

The workflow grants only `contents: read`, does not retain checkout credentials,
and uses `pull_request`, so running tests needs no repository write access or
custom secrets. Both actions are pinned to release commit hashes. There are no
path filters, so a documentation PR still reports the same check. The ten-minute
timeout bounds a stuck job.

## Inspect a failure and its correction

Open a PR's **Checks** tab, choose **Backend tests**, and expand **Run backend
tests**. The repository's **Actions** tab also lists runs under **Backend CI**;
check the branch and commit before interpreting a result. A pytest failure shows
the test name, assertion, obtained value, and expected value. A failure during
checkout, setup, or installation needs attention in that earlier step instead.

For a controlled exercise in a disposable teaching branch or copy, follow the
[worked failure and recovery](testing.md#controlled-failure-and-recovery).
In `test_worked_summaries_include_dm_participants_without_lab_rows`, temporarily
change the baseline mean expectation in `[15.0, 10.0]` to `[16.0, 10.0]`, then run:

```bash
python -m pytest backend/tests/test_processing.py::test_worked_summaries_include_dm_participants_without_lab_rows -q
```

The actual demonstration produced `1 failed`, with `Obtained: 15.0` and
`Expected: 16.0 ± 1.6e-08`. The worked baseline values 10 and 20 have mean 15;
correct the expectation to `[15.0, 10.0]`, rerun the command (`1 passed`), then
run the full suite. Do not change processing behavior or tolerance to hide this
deliberately wrong expectation.

To observe this on GitHub, push the temporary failing expectation to a disposable
teaching PR, inspect its failed check, then push the correction to the same PR.
Confirm the corrected commit has a successful **Backend tests** check and keep
the earlier failed run as evidence. Re-running the old commit does not test the
correction. Merge only the corrected version; the supplied default example stays
passing.

## Reporting versus requiring checks

This workflow reports success or failure. Copying it into a repository does not
prevent someone from merging a failing PR. An administrator must separately
configure a branch ruleset or branch protection for `main`, require pull requests,
and enable required status checks. After the workflow has run, select the check
named **Backend tests** (from GitHub Actions) and save the rule. Apply an equivalent
rule to `implement/course-framework` if enforcing checks during course authoring.
See GitHub's [required status check documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging).

Repository settings, actor bypass permissions, and review requirements remain
separate from the workflow. If the job name
changes later, update any required-check rule to match it.

## What a passing run shows

A hosted run is the only check of GitHub's runner, action downloads, dependency
installation, cache, and check reporting together. Passing backend tests alone do
not demonstrate local/container replicability under the
[course definitions](../GLOSSARY.md); see [comparisons](comparisons.md).
