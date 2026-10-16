# Session 1 mandatory homework: choose, change, and review

Spend approximately **120 minutes per student** before Session 2, coordinating with your group of three or four. Extend the [Session 1 exercise](../exercises/session-1.md): independently select a dataset and question, document your collaboration plan, and complete a small change through a reviewed PR in your group's repository. Topic approval is not required; instructor discussion is optional. Modeling is optional and complexity earns no extra credit.

## Preparation

Have your group's template-derived repository, individual GitHub accounts with write access, Python 3.12, Git, an editor, and the isolated `.venv` from the exercise. Everyone must be able to open the repository; give the instructor read access. If setup is incomplete, use [template setup](../../docs/template.md) and [backend setup](../../docs/setup.md). Commands below run from the repository root in a macOS/Linux shell; the setup guides give Windows equivalents.

Read the [collaboration guide](../../docs/collaboration.md) and supplied [PR template](../../.github/PULL_REQUEST_TEMPLATE.md). Keep local `.env`, `.venv/`, and credentials out of commits; share configuration through `.env.example`. Do not overwrite existing local settings or upload sensitive data. Select data you can lawfully share or provide clear permitted access instructions.

| Minutes | Task | Retained evidence |
| --- | --- | --- |
| 0–25 | Agree on dataset, question, and roles | README project note and named work/review plan |
| 25–35 | Verify environment and configuration | Interpreter, ignore checks, and local test outcome |
| 35–60 | Each make one small change | Feature branch and descriptive commit |
| 60–85 | Open PR and inspect CI | PR URL, current SHA, and passing CI run |
| 85–110 | Review a teammate and address feedback | Specific submitted review and author response |
| 110–120 | Preserve evidence and self-check | Updated participation table and honest remaining work |

## 1. Choose together and assign roles — 25 minutes

In the group's `README.md`, record the dataset's name, source URL/provider, version or access date, license/access restrictions, and how teammates obtain it. Explain what one row represents, relevant columns/units, and known missingness. State one plain-English question and a feasible first processing step, such as cleaning dates, joining tables, counting missing observations, or summarizing a measurement. Distinguish the chosen dataset from the supplied synthetic healthcare inputs; you do not need to adapt the application to new data tonight.

Agree on an explicit collaboration plan: name each student and GitHub username, their small change, its file/section, their teammate reviewer, and when they will exchange feedback before Session 2. For example, A reviews B, B reviews C, and C reviews A; with four members, extend the ring. Assign separate README headings to reduce conflicts. Rotate responsibility for coordinating the next session and maintaining evidence; these roles do not replace individual authorship and review.

Every student must author at least one PR and meaningfully review at least one teammate's PR **by the final showcase**, using their own account. Use this homework to make progress on both. An existing exercise PR can be continued if it still has a small unfinished change; otherwise open a new one. Keep unresolved access or scheduling problems visible in the plan, without inventing participation.

## 2. Check your environment — 10 minutes

Activate the existing environment and check it before editing:

```bash
source .venv/bin/activate
python --version
python -c 'import sys; print(sys.executable)'
git check-ignore .env .venv/
git ls-files -- .env .env.example
python -m pytest backend/tests
```

Expect Python 3.12.x inside this clone's `.venv`, both local paths ignored, only `.env.example` tracked, and passing tests. Investigate failures using the setup guide; record the actual outcome, not a promised pass. If `.env` is tracked, stop before staging and get help removing it from tracking and handling any exposed credentials. These tests check supplied application behavior; check documentation clarity and links manually.

## 3. Each make a small change — 25 minutes

With a clean working tree, start a new branch (replace `your-name` with your own unique identifier). If continuing your exercise PR, switch to its existing branch instead of creating another:

```bash
git switch main
git pull --ff-only origin main
git switch -c homework-1/your-name-project-note
```

Each student edits an agreed section of `README.md`: dataset provenance, question/first processing step, collaboration plan, or environment instructions. Keep the working FastAPI/Streamlit example intact; Docker Compose remains required later. Do not introduce application construction or model training as a prerequisite for this homework.

```bash
git diff --check
git diff -- README.md
git status --short
git add README.md
git diff --cached
git commit -m "Document dataset provenance and access instructions"
git push -u origin HEAD
```

Choose a commit message describing your actual change. Inspect staged content for unintended files or secrets. Check source links and factual statements; do not add artificial tests for prose. Preserve uncommitted work before switching branches; follow [update and merge](../../docs/collaboration.md#update-and-merge) if another change overlaps yours.

## 4. Open a PR and inspect CI — 25 minutes

In your **group repository**, open **Pull requests → New pull request**, base `main`, compare your feature branch. Fill in the supplied template with purpose, before/after content, actual local commands/results, and limits. Inspect **Files changed**, then request your assigned teammate. Drafts are useful while working; mark **Ready for review** when ready for a submitted review.

Open **Checks → Backend tests** and inspect the **Run backend tests** log under **Backend CI**. Match the run to your latest commit SHA and retain its URL and outcome. Wait for a passing result; pending is not passing. If CI fails or is absent, inspect the first failing step or Actions permissions using the [CI guide](../../docs/ci.md), correct the cause, and push to the same branch. Inspect the new run after every follow-up commit.

Copied workflow files report checks; they do not configure required checks or protection. A repository administrator follows [main protection setup](../../docs/template.md#administrator-protect-main-in-every-generated-repository). Keep actual local test results and hosted CI results distinct.

## 5. Review and respond — 25 minutes

Read your assigned teammate's PR purpose and diff. Check whether the data source is usable, the question fits the available columns, and the plan names real authors/reviewers. Leave a specific file/line comment explaining a concern or a verified strength, then submit an explained **Comment**, **Request changes**, or **Approve** review. For example: “The source page offers several versions; please name the download and access date so I can obtain the same input.” Approval alone or “looks good” is insufficient.

As author, reply to feedback, make any needed correction, and push to the same branch. The reviewer inspects the updated diff and latest CI before approving. Merge through GitHub only after current checks pass, meaningful teammate approval, and resolved discussions, following the collaboration guide. If time runs out, leave the PR open with a named next action; do not bypass review or claim missing evidence.

## 6. Preserve evidence and self-check — 10 minutes

Maintain the README participation table described in [individual participation evidence](../../docs/collaboration.md#preserve-individual-participation-evidence): name, GitHub username, authored PR URL, permalink to the submitted review on a teammate's PR, checked commit SHA, and CI run URL/outcome. Keep local command outcomes and unresolved work alongside it. Add evidence through a reviewed branch; after any new commit, inspect CI again and update the PR record for that SHA.

Record real activity as it happens. Copied template history and instructor/agent-authored PRs do not establish student participation. Each student should be able to open and explain their own contribution and review at the showcase.

- Can every teammate obtain the selected data and explain the question and first processing step?
- Does the plan name each person's change, reviewer, and next meeting, with any gaps explicit?
- Is your interpreter isolated, local configuration ignored, and staged content free of secrets?
- Can you open your PR, descriptive commit, passing CI for the current SHA, and meaningful teammate review with follow-up?
- Is each student's authored-PR/review requirement completed or explicitly planned before the final showcase?

This mandatory homework prepares retained evidence for [the final presentation](../../SYLLABUS.md#session-5-final-showcase-and-live-engineering-review). Assessment is pass/fail entirely at that presentation, with no separate submission, resubmission, or reassessment. Statistical analysis correctness is not graded. Completing this authoring material does not require students to perform the homework or create repositories now.
