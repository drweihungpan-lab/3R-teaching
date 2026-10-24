# Session 1 guided practice: environment, branch, and first PR

Work in groups of three or four for 80 minutes. Finish any unfinished steps at home, in addition to the Session 1 homework. Inspect the complete synthetic healthcare application and make a small README change; no application construction is needed. Choose your own dataset and question without prior approval; modeling is optional. FastAPI, Streamlit, and Docker Compose remain required for the final project.

Prerequisites: Python 3.12, Git, an editor, internet for dependencies, individual GitHub accounts, and the instructor's completed template URL. The instructor must first publish the completed framework on the template's default branch and enable **Template repository**; see [template setup](../../docs/template.md). One group member needs permission to create a repository and invite teammates; everyone needs write access. Use synthetic inputs today, not patient data.

Commands below use macOS/Linux shells from the repository root. Windows users run the same commands in the WSL Ubuntu terminal ([Session 0](../../docs/session-0.md#step-2-windows-install-wsl-and-open-ubuntu)); see [setup](../../docs/setup.md) and [template setup](../../docs/template.md).

| Minutes | Activity | Expected observation |
| --- | --- | --- |
| 0–15 | Create and clone group repository | Teammates can open their own group's repository |
| 15–30 | Prepare environment and settings | Python 3.12, ignored local settings, passing tests |
| 30–45 | Run and inspect supplied application | Healthy API and 24/96/95/1 displayed counts |
| 45–60 | Make and commit README change | One small diff on a feature branch |
| 60–75 | Open draft PR, inspect CI, exchange feedback | Check for current commit and specific reviewer comment |
| 75–80 | Inspect conflict guidance and record evidence | Clear stopping point and recovery plan |

## 1. Create your group's repository — 15 minutes

One member opens the instructor's template URL on GitHub and selects **Use this template → Create a new repository**. Choose the group's owner and name, leave **Include all branches** unchecked, and create it with default branch `main`. Under **Settings → Collaborators** (or the organization's access settings), invite all teammates with write access and the instructor with read access. Each teammate accepts and checks access. This creates a new history; later template edits do not synchronize automatically.

Each student clones the **new group repository**, replacing `OWNER/GROUP` and `GROUP` with its actual names:

```bash
git clone git@github.com:OWNER/GROUP.git
cd GROUP
git remote -v
git status --short
```

Expect `origin` to name the group repository and no changed files. Find `backend/`, `frontend/`, and `data/synthetic/`; you already have the working example. Do not clone the instructor repository as your group's project.

## 2. Prepare an isolated environment — 15 minutes

An environment keeps this project's installed packages separate from global Python. From the root:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python --version
python -c 'import sys; print(sys.executable)'
python -m pip install --upgrade pip
python -m pip install -e './backend[dev]'
python -m pip install -r frontend/requirements.txt
test -e .env || cp .env.example .env
git check-ignore .env .venv/
git ls-files -- .env .env.example
python -m pytest backend/tests
```

Expect Python 3.12.x and an executable inside your clone's `.venv`. `-e` makes backend source edits available to new Python processes; `[dev]` includes pytest and the API test client. Expect tests to pass; inspect any warning rather than hiding it. Dependencies use version ranges, not a lockfile; `python -m pip freeze` records installed versions.

Open `.env.example`, `.env`, and `.gitignore`. The copy command preserves an existing `.env`. `git check-ignore` should list `.env` and `.venv/`; `git ls-files` should list only `.env.example`. The example is shareable; local settings stay untracked. Check `BACKEND_URL=http://127.0.0.1:8000`, `LOG_LEVEL=INFO`, and `MAX_UPLOAD_BYTES=5242880`. Keep credentials out of all commits. Restart services after settings change; exported environment variables override `.env`.

## 3. Inspect the running example — 15 minutes

In the activated terminal at the root, start the API:

```bash
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Keep it running. In a second terminal, enter the same repository root and activate the same environment:

```bash
source .venv/bin/activate
python -m streamlit run frontend/app.py --server.address 127.0.0.1 --server.port 8501
```

Open <http://127.0.0.1:8000/health>: expect `{"status":"ok"}`. Open <http://127.0.0.1:8501>, upload [dm.csv](../../data/synthetic/dm.csv) as **Participants CSV (DM)** and [lb.csv](../../data/synthetic/lb.csv) as **Laboratory CSV (LB)**, then select **Process CSVs**. Expect 24 participants, 96 joined records, 95 observed, and one missing result, plus tables and a chart. Missing means unavailable, not zero. Explain to a teammate: Streamlit sends the files to FastAPI, which calls the reusable processing package. See [frontend reference](../../docs/frontend.md).

Practical three Rs: **repeatability** means matching runs under the same conditions; **replicability** means matching the same process under slightly different conditions, such as local versus Docker. **Reproducibility** means agreement under very different conditions, such as an independent simulation; it is conceptual here. Later comparisons check records/counts exactly and calculated decimals within declared tolerances. Seeing the page today does not establish local/Docker agreement; see the [glossary](../../GLOSSARY.md).

## 4. Make one small change — 15 minutes

Stop both services with Ctrl-C. Use either terminal at the root. Each student chooses a unique name in place of `your-name`:

```bash
git switch main
git pull --ff-only origin main
git switch -c session-1/your-name-group-question
```

In the existing `README.md`, add a short section titled `Group question — Your Name`: give one candidate dataset, a plain-English question, and one sentence explaining what the supplied application already does. A provisional question is fine; no approval or model is required. Use a distinct heading per author to reduce overlapping edits. Keep the rest of the working framework intact.

```bash
git diff --check
git diff -- README.md
git status --short
git add README.md
git diff --cached
git commit -m "Document group dataset and initial processing question"
git push -u origin HEAD
```

Expect only the intended README addition in the staged diff, with no `.env`, `.venv`, or data changes. Check any added links and factual statements manually. Existing backend tests check the application; they do not verify the clarity of your question. Do not invent tests for a README edit.

## 5. Inspect the draft PR and review — 15 minutes

In the **group repository**, select **Compare & pull request** (or **Pull requests → New pull request**), base `main`, and your feature branch as compare. Fill in the supplied PR template: purpose, before/after README content, actual local commands/results, and limits. Use the create-button dropdown to select **Create draft pull request**. Inspect **Files changed** for your intended diff.

Open **Checks → Backend tests** and its **Run backend tests** log (also available under **Actions → Backend CI**). Match the run's commit SHA to your latest commit, inspect installation/test steps, and record the result and run URL in the PR. A pending check is not a pass. A failed check needs its first failing step investigated; see [CI reference](../../docs/ci.md). Docs PRs run this check too. Reporting a check does not require it before merging: an administrator must separately configure [main protection](../../docs/template.md#administrator-protect-main-in-every-generated-repository).

Pair with a teammate and open each other's draft PR. Leave a specific file/line comment about the dataset/question or explanation, for example: “Please distinguish your proposed dataset from today's synthetic inputs so a new teammate knows which files run now.” Explain why it matters; approval alone or “looks good” is insufficient. The author replies and addresses feedback, then commits/pushes any correction to the same branch and checks CI for the new SHA.

Drafts allow comments; when ready for formal review, mark the PR **Ready for review**, request the teammate, and have them submit an explained **Comment**, **Request changes**, or **Approve** review. Every student must eventually author at least one PR and meaningfully review at least one teammate's PR using their own account. Preserve PR/review permalinks, commit SHA, and CI run URL in the group's README as described in [collaboration evidence](../../docs/collaboration.md#preserve-individual-participation-evidence).

## 6. Stop and explain — 5 minutes

Read [Update and merge](../../docs/collaboration.md#update-and-merge) together. If two branches edit the same line, Git may need a human to combine their intentions. Identify the inspect (`git status`), edit/remove conflict markers, stage, commit, and rerun-check steps. This is conflict inspection through the reference; do not deliberately break shared `main`. A live conflict drill can wait until there is time for supervised recovery.

Stop with an isolated environment, ignored settings, observed app counts, a small descriptive commit, a draft/open PR, inspected CI, and specific teammate feedback. Leave unresolved work explicit in the PR; merging is not required in this practice. Later, merge only after current checks pass, meaningful teammate approval, and resolved discussions, following the collaboration guide. Keep evidence accessible for Session 5.

This is preparation, not a separate assessed submission. Assessment is pass/fail entirely at the final presentation, with no separate submission, resubmission, or reassessment. Homework, slide production, and the instructor's full run sheet are separate materials.

## Instructor reference and recovery

| Symptom | Explanation or next step |
| --- | --- |
| Template button, access, or push missing | Confirm completed default-branch template, accepted invitations, owner permissions, and SSH access to GitHub (`ssh -T git@github.com` answers `Hi USERNAME!`; see the Session 0 [SSH step](../../docs/session-0.md#step-5-mac-create-an-ssh-key-and-add-it-to-github) and [troubleshooting](../../docs/session-0.md#troubleshooting)); follow [template setup](../../docs/template.md). Keep local work if access is delayed; do not claim PR/CI evidence. |
| Wrong Python or missing import | Check `sys.executable`, activate `.venv` at the root, and repeat installs with that interpreter; see [setup](../../docs/setup.md). |
| `.env` appears tracked | Stop before staging; `git ls-files` distinguishes tracking from ignore rules. Ask for help removing it from tracking and handling any exposed credentials. Do not overwrite local settings. |
| Port occupied or frontend cannot connect | Stop an old service or choose a free backend port, update `BACKEND_URL`, and restart both services; see [frontend](../../docs/frontend.md). |
| Unexpected counts or validation error | Restore the supplied upload selections, not modified source files; consult [API contract](../../docs/api.md) and synthetic data references. Expected counts are 24/96/95/1. |
| CI fails, stalls, or is absent | Inspect the latest SHA and first failing step; check Actions is enabled and permitted. Preserve the failure and correction evidence; [CI](../../docs/ci.md) separates local and hosted results. |
| Pull or merge conflicts | Preserve local work; inspect status before editing. Follow [collaboration recovery](../../docs/collaboration.md#update-and-merge) with the instructor; do not force-push or discard teammates' work. |