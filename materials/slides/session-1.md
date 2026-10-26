# Session 1: Environments and Git

Practise the workflow in the Sandbox, where mistakes are free.

- Isolate Python and keep local settings private.
- Use a feature branch, a pull request, and a teammate's review.
- Resolve a merge conflict on purpose.

---

## Our 170-minute route

- 00–10: Opening — a bubble tea question and why results must hold.
- 10–20: Device example — a messy notebook, Stages 1 to 2.
- 20–60: Explanation — the four repositories, environments, configuration.
- 60–70: Break — 10 minutes.
- 70–100: Explanation — Git, pull requests, reviews, and conflicts.
- 100–130: Demonstration — one change from branch to merged pull request.
- 130–170: Hands-on — 40 minutes in the Sandbox.

Unfinished practice continues at home, in addition to the homework.

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

## Device example: one analysis, seven stages

- The scenario: synthetic daily measurement counts for three medical devices. Each device can take 100,000 measurements in total.
- The task: predict the date each device reaches its limit.
- The same analysis will grow up over the course, in seven stages. Each stage shows one pain point; a later session's tool fixes it.
- Your instructor demonstrates; the files are public if you are curious: the `device-example` folder of the [Sandbox](https://github.com/drweihungpan-lab/3R-sandbox).

---

## Stage 1: one notebook, copied three times

```text
analysis_v1.ipynb  DEV-C reaches the limit on 2026-01-30
analysis_v2.ipynb  DEV-C reaches the limit on 2026-01-28
analysis_v3.ipynb  DEV-C reaches the limit on 2026-01-26
```

- Three copies, three dates. Last month's report named one of them.
- Which copy produced it? Nothing records that.
- Today's tool for this pain: Git.

---

## Stage 2: helper files, no declared dependencies

```text
Python 3.11 + pandas 1.5: DEV-C reaches the limit on 2026-01-30
Python 3.12 + pandas 2.x: AttributeError: 'DataFrame' object has no attribute 'append'
```

- The notebook now imports `loader.py` and `model.py`: reusable, but nothing says which packages and versions they need.
- The same files work on one laptop and crash on another.
- Today's tool for this pain: an isolated environment with declared dependencies.

---

## Four repositories, one job each

- **3R-teaching** (this course's materials): slides, exercises, notes.
- **Sandbox**: today's practice space for all 20 of you. `main` is protected and nothing here is graded.
- **Backend repo**: your group's own repository, created in Session 2. Your pull requests and reviews there are the evidence you show at the end.
- **Frontend repo**: one page the instructor provides; you run it, you do not edit it.

```text
Session 1: Sandbox  →  Session 2: Backend repo  →  Session 4: + Frontend repo
```

The words are defined in the [glossary](../../GLOSSARY.md).

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
- `python-dotenv` reads the `.env` file; exported variables take precedence.
- `.gitignore` does not untrack an already committed secret.

Example: `LOG_LEVEL=INFO` locally, `LOG_LEVEL=DEBUG` when investigating.

---

## Your repositories are public

Your group's Backend repo will be public, so anyone can install your package from its git URL without an account or token.

- Never commit real data, personal information, passwords or tokens.
- Use only synthetic or openly licensed data in the repository.
- `.env` stays out of Git; commit `.env.example` instead.
- If a secret is committed by mistake, tell the instructor; deleting the file later does not remove it from history.

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

## Branch rules protect main

In the Sandbox you cannot push to `main`. Every change arrives as a pull request that a teammate reviews first.

- Branch names: `group-N/short-topic`, for example `group-3/add-notes`.
- A review needs a specific comment about behavior or clarity.
- Session 2 adds automated checks (continuous integration). A repository rule can then *require* those checks before merging; today we only preview the idea.

```text
feature branch → commit → push → pull request → review → merge into main
```

---

## A meaningful review helps the next reader

Read **Files changed** and the purpose. Comment on behavior or clarity: “Which line of shared-notes.md is yours, and did you keep the other group's line?”

- Submit a review with an explanation; approval alone or “looks good” is insufficient.
- The author replies, corrects concerns, and pushes follow-up commits.
- The reviewer checks the update, then approves when satisfied.
- Merge through GitHub, then switch to `main` and `git pull --ff-only` before new work.

The same habit counts as evidence in your Backend repo from Session 2.

---

## Demo: clone the Sandbox and branch

You need your SSH key from Session 0 and your group number.

```bash
git clone git@github.com:drweihungpan-lab/3R-sandbox.git
cd 3R-sandbox
git switch -c group-3/add-notes
```

Open `practice/shared-notes.md` in your editor.

---

## Demo: edit, commit, push

Add one line under your group's heading in `practice/shared-notes.md`.

```bash
git status
git add practice/shared-notes.md
git commit -m "Add group 3 note"
git push -u origin group-3/add-notes
```

The push prints a link. Open it to create the pull request.

---

## Demo: review, merge, update main

Ask a teammate for a review with at least one specific comment. After approval, merge on GitHub.

```bash
git switch main
git pull --ff-only origin main
git branch -d group-3/add-notes
```

Then check that `git log --oneline` shows your merged change.

---

## Hands-on: 40 minutes in the Sandbox

- 10 minutes: clone, create your branch, add a note, push, and open a pull request.
- 10 minutes: review a teammate's pull request with one specific comment.
- 15 minutes: the conflict drill on the next slides.
- 5 minutes: write down what you did and where you stopped.

Use [the exercise](../exercises/session-1.md) when stuck. Nothing in the Sandbox is graded.

---

## Controlled conflict: the shared line

`practice/shared-notes.md` has one line every group edits: **Favourite tool this week**, currently `(undecided)`.

- Two groups change that line on different branches.
- The first pull request merges cleanly.
- The second now conflicts: Git cannot decide how overlapping edits combine.

Pick one line, edit it, and push your branch. Do not merge until your partner group has pushed theirs.

---

## Resolve deliberately, or abort the merge

Update your branch from `main` and look at the markers:

```bash
git fetch origin
git merge origin/main
git status
```

Open `practice/shared-notes.md`. `<<<<<<< HEAD` starts your line; `=======` separates the incoming line; `>>>>>>> origin/main` ends the block.

Agree on one line, remove all three markers, then:

```bash
git add practice/shared-notes.md
git commit -m "Resolve favourite tool line"
git push
```

If unsure before committing, `git merge --abort` returns to the pre-merge state.

---

## Your group owns the question and evidence

- Groups contain three or four students, with one public Backend repo per group, created next session.
- Choose your own dataset and question for the final project; topic approval is not required. Discussion with the instructor is available.
- Modeling is optional; complexity earns no additional credit. FastAPI, the Frontend page, and Docker Compose remain required.
- Each student authors at least one pull request and meaningfully reviews at least one teammate's pull request in the Backend repo, using their own account.

Decide your Backend repo name before Session 2.

---

## Prepare for the final presentation

Mandatory homework after Session 1 is approximately two hours, plus any unfinished practice. Details will be posted separately.

- Today's checkpoint: every student opened a pull request and gave a review in the Sandbox.
- Assessment is pass/fail, entirely at the final presentation. All engineering requirements must be met, including tests, CI, validation, and later output comparisons.
- Statistical analysis correctness is not graded. Tests still verify the processing behavior you declare.
- There is no separate submission, resubmission, or reassessment; the final result is final.

Use the [syllabus](../../SYLLABUS.md) for the full requirements. Next: generate your Backend repo and share an installable package.
