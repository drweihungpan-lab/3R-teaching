# Session 1: Environments, Git, and CI

Make a small, explainable change to a complete working example.

- Isolate Python, keep local settings private, and run the checks.
- Use a feature branch, a pull request, and a teammate's review.
- Read automated results before merging.

---

## Our three-hour route

- 00–35: Opening — introductions, a bubble tea question, and why results must hold.
- 35–65: Explanation — environments, configuration, Git, and CI.
- 65–85: Demonstration — template to a checked draft PR.
- 85–100: Break — 15 minutes.
- 100–180: Guided practice — repeat the workflow; the conflict drill if time permits.

These flexible timings total 35 minutes opening, 30 explanation, 20 demonstration, 15 break, and 80 practice. Unfinished practice continues at home, in addition to the homework.

---

## Your bubble tea shop

At the student demo day, your bubble tea got great reviews.

Now you want to open a shop in front of NTHU. You already have the best location and the decor.

**What do you need to take care of so every customer gets the tea they loved?**

---

## Can we trust published biomedical research?

- An estimated **>50%** of preclinical biomedical research is irreproducible, costing about **US$28 billion a year** in the US. ([Freedman et al., PLoS Biol 2015](https://doi.org/10.1371/journal.pbio.1002165))
- Cancer biology: only **46%** of replications succeeded, and **74%** of planned experiments could not be done at all, partly because methods were not described in enough detail. ([Errington et al., eLife 2021](https://doi.org/10.7554/eLife.71601))

---

## What are we trying to preserve?

- Repeatability: matching results under the same conditions.
- Replicability: matching results under slightly different conditions, such as local Python versus Docker.
- Reproducibility: matching results under very different conditions, such as an independent simulation; conceptual here.

These are the [course definitions](../../GLOSSARY.md). Later comparisons require exact records/counts and declared tolerances for calculated decimals.

Keep your bubble tea answers in mind.

---

## Start with a working application

The supplied synthetic healthcare example already joins participant and laboratory CSVs, validates inputs, and produces summaries.

```text
Streamlit upload → FastAPI request → stat_core processing
                 ← counts, records, summaries ←
```

Today we inspect and make a small change. Later sessions trace packaging, tests, services, and Docker Compose. Model complexity and interface polish are not the goal.

---

## A Python environment belongs to one project

A virtual environment is a separate Python installation area for this project's packages. It avoids mixing them with global packages or another project.

- Create `.venv` with Python 3.12; activate it in each new terminal.
- Install declared dependencies, rather than copying another person's `.venv`.
- Activation chooses which Python runs; it does not install packages.
- A virtual environment alone does not lock dependency versions. Record versions with `python -m pip freeze` when comparing environments.

---

## Local configuration and shareable examples

Configuration is settings read at startup, rather than processing code.

- `.env` holds your local settings; Git ignores it and `.venv/`.
- `.env.example` is tracked and safe to share; never put secrets in it.
- `python-dotenv` reads the root `.env`; exported variables take precedence.
- Restart services after changes; `.gitignore` does not untrack an already committed secret.

Use `LOG_LEVEL=INFO` and `BACKEND_URL=http://127.0.0.1:8000` locally. See [configuration details](../../docs/setup.md#configuration).

---

## Git records changes; GitHub hosts collaboration

- A repository contains files and their recorded history.
- A feature branch names a line of work for one purpose.
- Staging selects the changes for the next commit; a commit records that snapshot with a message.
- A push sends local commits to GitHub. A pull request (PR) asks teammates to review a branch before merging.

```text
feature branch → commit → draft PR → review + checks → main
```

---

## CI reports; repository rules require

Continuous integration (CI) runs automated checks on proposed changes. This template runs **Backend CI → Backend tests**, including documentation PRs.

- A green check reports success for a particular commit; it does not prove every requirement.
- Copied workflow files do not protect `main` automatically.
- A group administrator separately requires PRs, teammate approval, conversation resolution, and **Backend tests** in branch protection.
- Check the merge box actually enforces the rule; inspect the latest commit's result.

See [group protection setup](../../docs/template.md#administrator-protect-main-in-every-generated-repository) and [CI guidance](../../docs/ci.md).

---

## Demo: create your group's repository

The instructor first publishes the completed framework on the template's default branch and enables **Template repository**.

- One member selects **Use this template → Create a new repository**; copy only the default branch, named `main`.
- Invite teammates with write access and the instructor with read access.
- Replace `OWNER/GROUP` below with your group's actual owner and name.

```bash
git clone git@github.com:OWNER/GROUP.git
cd GROUP
```

Follow [template setup](../../docs/template.md). Template updates do not synchronize automatically.

---

## Demo: prepare Python and check the baseline

Run from the group repository root on macOS/Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e './backend[dev]'
python -m pip install -r frontend/requirements.txt
test -e .env || cp .env.example .env
python -m pytest backend/tests
```

The working example has 175+ tests; the count may grow. Expect all tests to pass; read failures and warnings. On Windows, run in the WSL Ubuntu terminal: [Session 0](../../docs/session-0.md#step-2-windows-install-wsl-and-open-ubuntu).

---

## Demo: see the example work

In the activated environment at the root, start the API:

```bash
python -m uvicorn app.main:app --app-dir backend \
  --host 127.0.0.1 --port 8000
```

Keep it running. In a second terminal at the root:

```bash
source .venv/bin/activate
python -m streamlit run frontend/app.py \
  --server.address 127.0.0.1 --server.port 8501
```

Open `http://127.0.0.1:8501`; upload [dm.csv](../../data/synthetic/dm.csv) and [lb.csv](../../data/synthetic/lb.csv). Select **Process CSVs**: expect 24 participants, 96 records, 95 observed, one missing. Stop servers with Ctrl-C afterward.

---

## Demo: one small README change

With a clean working tree, start a feature branch:

```bash
git status
git switch main
git pull --ff-only origin main
git switch -c feature/group-purpose
```

In `README.md`, add a short group-purpose paragraph: who the project serves, your chosen dataset, and the question it will explore. Keep the synthetic example clearly labeled as the current demonstration.

Inspect the edit with `git diff`. The purpose is readable documentation; processing behavior should still pass its checks.

---

## Demo: record and publish the change

```bash
python -m pytest backend/tests
git diff --check
git diff -- README.md
git add README.md
git diff --cached
git commit -m "Document our group's dataset and question"
git push -u origin feature/group-purpose
```

Check README links and wording too. Stage only the intended file; confirm `.env` and `.venv` are absent. A descriptive message explains the purpose of the change.

---

## Demo: open a draft PR and inspect checks

- In the group repository, select **Compare & pull request**; base `main`, compare `feature/group-purpose`; choose **Create draft pull request**.
- Fill in the supplied PR template: purpose, before/after, actual commands, results, and limits.
- Open **Checks → Backend tests → Run backend tests**. Confirm the branch and commit SHA, the identifier of the version checked.
- Read failing logs at the first failed step; correct the cause and push to the same branch. A rerun of an older commit cannot check a new correction.

A draft signals work in progress. Mark ready for review and request a teammate when the change and evidence are ready.

---

## A meaningful review helps the next reader

Read **Files changed**, the purpose, and check evidence. Comment on behavior, tests, or clarity: “Which file contains your chosen dataset, and is the synthetic demo still distinguishable?”

- Submit a review with an explanation; approval alone or “looks good” is insufficient.
- The author replies, corrects concerns, and pushes follow-up commits.
- The reviewer checks the update and latest CI, then approves when satisfied.
- Merge the PR through GitHub only after passing required checks, teammate approval, and resolved discussions.

See [collaboration guidance](../../docs/collaboration.md). After merging, switch to `main` and pull with `--ff-only` before new work.

---

## Break, then 80 minutes of practice

Take a 15-minute break after the demonstration.

- First 45 minutes: create the group repository, prepare each environment, run the example and baseline checks.
- Next 30 minutes: each student makes a small purposeful change, opens a draft PR, and reviews a teammate's PR.
- Last 5 minutes: record evidence and your stopping point. Rehearse the controlled conflict below only if time permits.

Finish any unfinished practice at home, in addition to the homework. Use the setup and collaboration guides when stuck. Work in the group's repository and keep changes small enough to explain.

---

## Controlled conflict: seed a disposable file

A conflict means Git cannot decide how overlapping edits should combine. Rehearse locally after committing other work; use unused branch names and a new `conflict-demo.txt`.

```bash
git switch main
git pull --ff-only origin main
git switch -c practice/conflict-base
```

Create `conflict-demo.txt` in your editor with exactly one line: `Session plan: draft`.

```bash
git add conflict-demo.txt
git commit -m "Seed disposable conflict example"
git switch -c practice/conflict-a
```

---

## Controlled conflict: two feature branches

On `practice/conflict-a`, replace the line with `Session plan: test first`; save, then run:

```bash
git add conflict-demo.txt
git commit -m "Suggest testing first"
git switch practice/conflict-base
git switch -c practice/conflict-b
```

On `practice/conflict-b`, replace the original line with `Session plan: review first`; save, then run:

```bash
git add conflict-demo.txt
git commit -m "Suggest reviewing first"
git merge practice/conflict-a
git status
```

Expect a content conflict: both feature branches changed the same original line.

---

## Resolve deliberately, or abort the merge

Open `conflict-demo.txt`: `<<<<<<< HEAD` starts the current branch's `Session plan: review first`; `=======` separates the incoming `Session plan: test first`; `>>>>>>> practice/conflict-a` ends the block.

Agree on `Session plan: test, then review`. Replace the entire marked block with that line; save, then run:

```bash
git add conflict-demo.txt
git commit -m "Resolve plan: test then review"
git diff --check
python -m pytest backend/tests
```

If unsure before committing the resolution, `git merge --abort` returns to the pre-merge state. Keep this rehearsal local; switch back to `main` when done.

---

## Use the same recovery on real PRs

Commit your work first. On your real feature branch:

```bash
git fetch origin
git merge origin/main
```

If Git reports conflicts, use `git status`, discuss both intentions, edit out markers, stage the resolved files, and commit. Rerun relevant checks and push the feature branch.

Request another review when the change needs it; new commits may dismiss old approvals. Confirm CI belongs to the latest commit before the reviewed PR is merged into `main`.

---

## Your group owns the question and evidence

- Groups contain three or four students, with one repository per group.
- Choose your own dataset and question; topic approval is not required. Discussion with the instructor is available.
- Modeling is optional; complexity earns no additional credit. FastAPI, Streamlit, and Docker Compose remain required.
- Each student authors at least one PR and meaningfully reviews at least one teammate's PR using their own account.

Keep authored PR links, submitted review permalinks, and CI links with commit SHAs in the group README as real participation occurs.

---

## Prepare for the final presentation

Mandatory homework after Session 1 is approximately two hours, plus any unfinished guided practice: continue the PR/review workflow and document the group's dataset and question.

- Today's checkpoint is preparation: isolated environment, configuration hygiene, and visible branch/PR history.
- Assessment is pass/fail, entirely at the final presentation. All engineering requirements must be met, including tests, CI, validation, and later output comparisons.
- Statistical analysis correctness is not graded. Tests still verify the processing behavior you declare.
- There is no separate submission, resubmission, or reassessment; the final result is final.

Use the [syllabus](../../SYLLABUS.md) for the full requirements. Next: trace reusable processing modules and package metadata.
