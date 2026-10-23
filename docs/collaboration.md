# Branches, pull requests, and peer review

Work in your [group's own repository](template.md). The course workflow is a
feature branch → pull request (PR) → teammate review → merge into `main`.
There is no `develop` branch. Each student authors at least one PR and meaningfully
reviews at least one teammate's PR, using their own GitHub account.

## Make one understandable change

From the repository root, with a clean working tree:

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/explain-missing-results
```

Make a small change with a clear purpose. Activate the [Python environment](template.md)
and run `python -m pytest backend/tests`. For documentation changes, also check
the commands, links, and consistency with the [syllabus](../SYLLABUS.md).
Inspect `git diff` and `git status` before staging. Stage only the intended files:

```bash
git add <changed-paths>
git diff --cached
git commit -m "Explain why missing laboratory results stay unavailable"
git push -u origin feature/explain-missing-results
```

Replace `<changed-paths>` with actual paths; the branch and commit above are examples.
Never commit `.env`, credentials, or the virtual environment. A descriptive commit
explains the change, rather than saying only “update” or “fix”.

## Open and explain the PR

On GitHub, select **Compare & pull request** in the group repository. Set the base
to `main`, give the PR a descriptive title, and fill in the supplied
[PR template](../.github/PULL_REQUEST_TEMPLATE.md). A draft is useful while working;
mark it ready when the change and evidence are ready for review.

Explain the purpose and visible before/after behavior. Record exact local check
commands, outcomes, and limits; for a documentation change, link/content checks
are appropriate. Link the **Backend tests** run for the latest commit from the
PR's **Checks** tab. A local pass and a hosted CI pass are separate evidence.
Request a teammate as reviewer. Do not merge while checks fail or review is pending.

## Review with evidence

The reviewer reads the purpose and **Files changed**, inspects test expectations,
and runs relevant checks when practical. Ask whether behavior matches the stated
intent, invalid inputs remain clear, missing results stay missing, and documentation
is usable. For example: “AGE now accepts decimals: which validation case checks
the declared rule?” or “This setup command omits the frontend dependencies.”

Leave specific comments tied to files/lines or behavior, then submit a review
using **Comment**, **Request changes**, or **Approve**, with a short explanation.
Approval alone or “looks good” does not meet the meaningful-review requirement.
The author replies, makes corrections, and pushes follow-up commits to the same
branch. The reviewer checks the updated diff and CI, then approves when satisfied.
Do not resolve an outstanding concern without addressing it.

## Update and merge

If `main` has advanced, update your feature branch (commit your work first):

```bash
git fetch origin
git merge origin/main
```

If conflicts appear, inspect `git status`, edit the affected files to preserve
both intended changes, remove conflict markers, stage those files, and commit
the resolution. Rerun relevant checks and push. Request another review if behavior
changed; stale approvals may be dismissed. Once the latest **Backend tests**
passes, teammate approval is present, and discussions are resolved, merge the
PR into `main` through GitHub. Then switch to `main` and pull with `--ff-only`.
Repository rules must be [configured separately](template.md#administrator-protect-main-in-every-generated-repository).

## Preserve individual participation evidence

Keep a small table in the group's README with each student's name, GitHub username,
authored PR URL, and a permalink to their submitted review on a teammate's PR.
Add the relevant CI run link and commit SHA so the instructor can inspect the
version actually checked. Record real activity as it occurs; copied template
history and instructor/agent-authored PRs are not student participation.

At the final presentation, the instructor opens those links and verifies PR
authorship, the teammate's PR author, review content and follow-up, and CI for
the final commit. In GitHub search, replace `OWNER/GROUP` and `USERNAME`:

```text
repo:OWNER/GROUP is:pr author:USERNAME
repo:OWNER/GROUP is:pr reviewed-by:USERNAME
```

These [search filters](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests)
locate evidence; inspect the actual review to judge its substance. Keep closed
and merged PRs accessible. Each student should explain their own contribution.
Assessment is pass/fail, entirely at the final presentation, with no separate
submission, resubmission, or reassessment. Homework is preparation. Authoring this
guide requires no actual student repositories or manufactured participation.
