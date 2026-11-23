# Session 1: Environments and Git

Practise where mistakes are free.

- Isolate Python; keep local settings private.
- Branch, pull request, teammate's review.
- Resolve a merge conflict on purpose.

```notes
Today runs in the class Sandbox, where nothing is graded and mistakes cost
nothing. Introduce yourself first, then set the three outcomes above.
```

---

## Our 170-minute route

- 00-20: Opening, and why results must hold.
- 20-60: Environments and configuration.
- 60-70: Break.
- 70-130: Git, reviews, live demo.
- 130-170: Hands-on in the Sandbox.

```notes
Finer breakdown, which matches the run sheet in the instructor notes:
  00-10  Opening: a bubble tea question and why results must hold
  10-20  Device example: a messy notebook, Stages 1 to 2
  20-60  Explanation: the four repositories, environments, configuration
  60-70  Break, 10 minutes
  70-100 Explanation: Git, pull requests, reviews, conflicts
  100-130 Demonstration: one change from branch to merged pull request
  130-170 Hands-on: 40 minutes in the Sandbox

Say out loud that unfinished practice continues at home, in addition to
the homework.
```

---

## Your bubble tea shop

Your bubble tea got great reviews at the demo day.

Now you open a shop near NTHU.

**How does every customer get the tea they loved?**

```notes
You already have the best location and the decor; the question is only about
keeping the result the same every time.

Ask students one at a time, at random. Do not steer answers toward the three
Rs, and do not map their answers for them. Keep a few answers on the board;
you will return to them two slides from now.
```

---

## Can we trust published research?

- **>50%** of preclinical biomedical research is irreproducible, about **US$28 billion** a year. ([Freedman 2015](https://doi.org/10.1371/journal.pbio.1002165))
- Cancer biology: only **46%** of replications succeeded. ([Errington 2021](https://doi.org/10.7554/eLife.71601))

```notes
The Freedman figure is for the United States.

In the cancer biology project, 74% of the planned experiments could not be
done at all, partly because the methods were not described in enough detail.
That is the detail worth dwelling on: not fraud, just under-described work.

Say aloud that a 2016 Nature survey (Baker 2016, doi 10.1038/533452a) found
over half of 1,576 researchers had failed to reproduce their own experiments.
```

---

## What are we trying to preserve?

- Repeatability: the same conditions.
- Replicability: slightly different conditions.
- Reproducibility: very different conditions.

These are the [course definitions](../../GLOSSARY.md).

```notes
Read the definitions from the glossary, with an example for each:
  Repeatability  - you, same machine, same data, next week
  Replicability  - a teammate, local Python versus Docker
  Reproducibility - an independent simulation; conceptual in this course

Later comparisons in this course require exact records and counts, plus a
declared tolerance for calculated decimals.

Point back at the bubble tea answers on the board and let students see that
they already named most of these without the vocabulary.
```

---

## Device example: seven stages

- Synthetic daily measurement counts, three devices.
- Each device stops at 100,000 measurements.
- Predict when each reaches its limit.
- Seven stages, one pain point each.

```notes
This is the course's running example. The same analysis grows up over the
five sessions; each stage shows exactly one pain point, and a later session's
tool fixes it.

You demonstrate; students watch. The files are public if they are curious:
the device-example folder of the Sandbox at
https://github.com/drweihungpan-lab/3R-sandbox

Demonstrate Stages 1 and 2 now using the stage READMEs. Name the tool that
fixes each pain, but do not teach it yet.
```

---

## Stage 1: one notebook, copied three times

```text
analysis_v1.ipynb  DEV-C reaches the limit on 2026-01-30
analysis_v2.ipynb  DEV-C reaches the limit on 2026-01-28
analysis_v3.ipynb  DEV-C reaches the limit on 2026-01-26
```

- Three copies, three dates.
- Last month's report named one. Which?
- Today's tool for this pain: Git.

```notes
Nothing in the folder records which copy produced the published number. The
file names look like a history but carry no information about what changed
or why.

Ask the room which copy they would trust. There is no way to tell.
```

---

## Stage 2: no declared dependencies

```text
Python 3.11 + pandas 1.5: DEV-C reaches the limit on 2026-01-30
Python 3.12 + pandas 2.x: AttributeError: 'DataFrame' object has no attribute 'append'
```

- Reusable helpers, but nothing declares their packages.
- Works on one laptop, crashes on another.
- Today's tool: an isolated environment.

```notes
The notebook now imports loader.py and model.py. That is real progress for
reuse, but nothing in the project says which packages and which versions
those files need.

DataFrame.append was removed in pandas 2.0. The code did not change; the
environment did.
```

---

## Four repositories, one job each

- **3R-teaching**: slides, exercises, notes.
- **Sandbox**: today's practice space; nothing graded.
- **Backend repo**: your group's evidence, from Session 2.
- **Frontend repo**: provided; you run it, not edit it.

```text
Session 1: Sandbox  ->  Session 2: Backend repo  ->  Session 4: + Frontend repo
```

```notes
The Sandbox is shared by all 20 of you, and its main branch is protected.

The Backend repo is your group's own public repository, created next session.
Your pull requests and reviews there are the evidence you show at the end.

The Frontend repo is one page the instructor provides. You run it; you do
not edit it.

All four words are defined in the glossary at GLOSSARY.md.
```

---

## One environment per project

A virtual environment is a separate Python area for this project's packages.

- Create `.venv` with Python 3.12.
- Activate it in every new terminal.

```notes
"Separate area" is the whole idea: this project's packages do not mix with
your global packages or with another project's.

Activation is per terminal. A new terminal, or a new VS Code panel, starts
deactivated, and that is the single most common confusion in this session.
```

---

## Isolation is not version locking

- Activation chooses which Python runs; it installs nothing.
- Install from declared dependencies, never a copied `.venv`.
- Record versions with `python -m pip freeze` before comparing.

```notes
These three are the traps.

Students expect activation to install things. It does not; it only decides
which python and pip you are talking to.

Copying a teammate's .venv folder appears to work and then breaks, because
the paths inside it point at their machine.

A virtual environment on its own does not pin versions. Isolation and
version locking are two different jobs, and only pip freeze does the second.
```

---

## Local settings stay local

- `.env` holds your settings; Git ignores it.
- `.env.example` is tracked; keep secrets out.
- `python-dotenv` reads `.env`; exported variables win.

Example: `LOG_LEVEL=INFO` locally, `LOG_LEVEL=DEBUG` when investigating.

```notes
Configuration means settings that are read at startup, rather than
processing code.

Git also ignores .venv/, for the same reason: it belongs to one machine.

.env.example is the shareable shape of the file: the same keys, with safe
placeholder values and no real secrets.

Precedence matters when debugging: a variable already exported in the shell
takes priority over the .env file.
```

---

## Your repositories are public

- Never commit real data, passwords or tokens.
- Use synthetic or openly licensed data only.
- `.gitignore` does not untrack a committed secret.
- Committed a secret? Tell the instructor.

```notes
Your group's Backend repo will be public, so anyone can install your package
from its git URL without an account or token. That is deliberate, and it is
also the reason for these rules.

Be blunt about the last point. Deleting a file in a later commit does not
remove it from history; the secret is still fetchable. Tell the instructor
immediately so the credential can be rotated.
```

---

## Git records, GitHub hosts

- A repository holds files and their history.
- A branch names one line of work.
- A commit records a snapshot with a message.

```notes
Git is the tool that records changes. GitHub is the website that hosts the
repository and the collaboration around it. Keep the two words separate all
session.

Staging is the step students forget: git add selects which changes go into
the next commit, so a commit is a chosen snapshot, not everything you
touched.
```

---

## From branch to merged main

- A push sends your commits to GitHub.
- A pull request asks teammates to review first.

```text
feature branch  ->  commit  ->  draft PR  ->  review + checks  ->  main
```

```notes
A pull request, PR for short, is a request to merge a branch. It is where
the review conversation happens.

Trace the diagram left to right with a finger. Every change in this course
takes this path, with no exceptions, including the instructor's.
```

---

## Branch rules protect main

You cannot push to `main` in the Sandbox.

Every change arrives as a reviewed pull request.

- Branch names: `group-N/short-topic`.
- A review needs one specific comment.

```notes
Example branch name: group-3/add-notes.

A review comment should be about behavior or clarity, something the author
can act on.

Preview, do not teach: Session 2 adds automated checks, called continuous
integration. A repository rule can then require those checks to pass before
merging. Today we only name the idea.
```

---

## What a real review looks like

Read **Files changed** and the purpose. Comment on behavior or clarity.

- Approval alone, or "looks good", is not a review.
- Explain what you checked.

```notes
A worked example of a specific comment: "Which line of shared-notes.md is
yours, and did you keep the other group's line?"

That comment is useful because it names a file, a line and a risk. "Looks
good" names nothing and helps nobody.

This same habit is the evidence in your Backend repo from Session 2 onward,
so practise it today while it is free.
```

---

## The review loop closes

- The author replies and pushes follow-up commits.
- The reviewer checks the update, then approves.
- Merge on GitHub, then `git pull --ff-only` on `main`.

```notes
A review is a loop, not a verdict. The author answers each concern, pushes
more commits to the same branch, and the pull request updates itself.

The last step is the one people skip: after a merge, switch to main and pull
before starting new work, or your next branch starts from a stale main.
```

---

## Demo: clone the Sandbox and branch

You need your SSH key and your group number.

```bash
git clone git@github.com:drweihungpan-lab/3R-sandbox.git
cd 3R-sandbox
git switch -c group-3/add-notes
```

Open `practice/shared-notes.md`.

```notes
The SSH key is from Session 0. Use the SSH URL, not HTTPS; see ADR 0001.

Use your own group number live, not the 3 on the slide.

Type the commands rather than pasting them, and say what each one does.
```

---

## Demo: edit, commit, push

Add one line under your group's heading.

```bash
git status
git add practice/shared-notes.md
git commit -m "Add group 3 note"
git push -u origin group-3/add-notes
```

The push prints a link. Open it to create the pull request.

```notes
Read git status out loud before and after git add, so the staging step is
visible rather than magic.

Also show the refused push: try pushing this change directly to main and let
the room see branch protection reject it.
```

---

## Demo: review, merge, update main

Ask for a review with one specific comment. Merge after approval.

```bash
git switch main
git pull --ff-only origin main
git branch -d group-3/add-notes
```

Then `git log --oneline` shows your merged change.

```notes
Have a real teammate or a second account leave the review live, so students
see the approval arrive and the merge button unlock.

Deleting the merged branch is housekeeping: the work is in main now.

Finish on git log --oneline so the merge appears in the recorded history.
```

---

## Hands-on: 40 minutes

- 10 min: branch, note, push, PR.
- 10 min: review a teammate's PR.
- 15 min: conflict drill.
- 5 min: note where you stopped.

[The exercise](../exercises/session-1.md) helps when stuck.

```notes
Nothing in the Sandbox is graded. The checkpoint for today is that every
student has opened one pull request and given one review.

The exercise covers sections 1 to 4. Show the two conflict slides at the
150-minute mark, not before.

Circulate rather than watching the clock. Common failures: pushing from main
by mistake, cloning over HTTPS, an SSH key not added to the account, and a
wrong group number in a branch name, which is harmless.
```

---

## Controlled conflict: the shared line

Every group edits one line: **Favourite tool this week**.

- Two groups change it on different branches.
- The first pull request merges cleanly.
- The second one conflicts.

```notes
The line lives in practice/shared-notes.md and currently reads "(undecided)".

Instructions for the room: pick one line, edit it, push your branch, and do
not merge until your partner group has pushed theirs.

A conflict is not an error. It is Git refusing to guess how two overlapping
edits combine, which is exactly the behavior you want.
```

---

## Resolve the conflict

Update your branch from `main`:

```bash
git fetch origin
git merge origin/main
git status
```

`<<<<<<< HEAD` is yours; `>>>>>>> origin/main` is theirs.

```notes
Open practice/shared-notes.md in the editor and read the markers aloud:
  <<<<<<< HEAD        starts your version
  =======             separates the two versions
  >>>>>>> origin/main ends the incoming version

git status names the conflicted file. Read it before touching anything.
```

---

## Agree, then finish the merge

Keep one line. Remove all three markers.

```bash
git add practice/shared-notes.md
git commit -m "Resolve favourite tool line"
git push
```

Unsure before committing? `git merge --abort` restores the pre-merge state.

```notes
Resolving is a decision between people, not a Git command. The two groups
agree on one line first; the commands only record that decision.

Leaving a marker behind is the classic mistake. Search the file for < and >
before committing.

merge --abort is the safety net: it returns the branch to exactly its
pre-merge state, so nobody needs to panic.
```

---

## Your group, your question

- Three or four students, one public Backend repo.
- Choose your own dataset and question; no approval needed.
- Modeling is optional; complexity earns no extra credit.

```notes
The Backend repo is created next session, one per group.

Topic approval is not required, and discussion with the instructor is
available if a group wants it.

Still required regardless of topic: FastAPI, the provided Frontend page, and
Docker Compose. Say this clearly, because "modeling is optional" is
sometimes heard as "the engineering is optional".
```

---

## Everyone authors and reviews

Each student authors one pull request and meaningfully reviews a teammate's, from their own account.

Decide your Backend repo name before Session 2.

```notes
"From their own account" is literal. One student pushing on behalf of the
group is the failure mode this requirement exists to prevent.

Meaningfully reviews means the specific-comment standard from earlier, not
a rubber stamp.

Ask each group to agree on a repository name before they leave.
```

---

## Prepare for the final presentation

- Pass or fail, decided entirely at the final presentation.
- All engineering requirements must be met.
- No resubmission; the final result is final.

Full requirements: the [syllabus](../../SYLLABUS.md).

```notes
Mandatory homework after this session is about two hours, plus any unfinished
practice. Details are posted separately.

Engineering requirements include tests, CI, validation and the later output
comparisons.

Statistical analysis correctness is not graded. Tests still have to verify
the processing behavior you declare.

There is no separate submission, resubmission or reassessment.

Close by minute 168 with the preview: next session you generate your Backend
repo and share an installable package.
```
