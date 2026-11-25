# Session 2: venv and Git

**Today:** Share last week. One repo, one venv. Data in, data out. Git and branches.

```notes
Open warmly. Today builds directly on the Backend repo every group pushed in
Session 1. Nothing new is generated today: we use what you already have.
```

---

## Today's Plan

1. **Show-and-tell**
2. **Why cookiecutter**
3. **One repo, one venv**
4. **Data in, data out**
5. **Git, branches, pull requests**
6. **Hands-on**

```notes
No timings on purpose. Keep the Show-and-tell short and informal, and let
the difficulties feed the cookiecutter recap.
```

---

## Show-and-Tell

**What did you do in the Session 1 exercise?**

**What was difficult?**

Nothing to prepare. Just tell us.

```notes
Informal sharing, not a presentation. Ask several students, one at a time.
Write every difficulty on the board: you will come back to them in the next
few slides. Expect: SSH keys, cookiecutter not found, files in the wrong
folder, hyphens in package_name, CI red on first push.
```

---

## Back at the Bubble Tea Shop

**Your best staff member is sick today.**

**Can someone else still make your tea?**

```notes
Ask 2–3 students. Steer toward: only if the recipe is written down, in the
same place, in the same shape, every time. That is what a template gives
a repository.
```

---

## Why Cookiecutter? Readability

Every group's repo has the **same shape**.

`src/`, `tests/`, `setup.cfg`, `Makefile`: always in the same place.

**Open any repo and you already know where to look.**

```notes
Readability is about the structure, not the code. A newcomer, a reviewer,
or you in six months finds the processing in src/<package>/ and the tests
in tests/ without asking anyone.
```

---

## Why Cookiecutter? Shareability

A teammate can **review** your repo.

The instructor can **help** any group.

Same answers to the questions always produce **the same files**.

```notes
Shareability: because every repo looks the same, people can move between
them. Same answers produce the same files: that is repeatability for
project setup, in the course sense of the word.
```

---

## Why Cookiecutter? Maintenance

**Fix the template once.**

Every repo generated **afterwards** gets the fix.

No copying a fix by hand into thirty repos.

```notes
Maintenance here means improving the template so future repos are better.
We do not update repos that already exist from the template; that needs
extra tools (such as cruft) and is out of scope for this course.
```

---

## Pitfall: Hyphens in Names

```text
package_name = 3R-package-demo
→ from 3R-package-demo.3R-package-demo import hello_world
→ SyntaxError
```

`repo_name` may contain hyphens. **`package_name` must be a valid Python name.**

Use `device_limit`, not `3R-package-demo`.

```notes
Python names cannot start with a digit or contain "-". pip install may still
succeed, but the command fails the moment you run it. If any group hit this
in Show-and-tell, point at them (kindly).

This is the maintenance story in action: the right fix is a check in the
template itself that rejects an invalid package_name, so nobody hits it
again. That template change is coming.
```

---

## The Reference Backend Repo

My own Backend repo, **generated from the same template as yours.**

[3R-package-demo](https://github.com/drweihungpan-lab/3R-package-demo)

I show each step there first. You do it in yours.

```notes
Reference Backend repo: same template, same structure, package_name
device_limit. Its main branch is exactly the template output, like yours.

Instructor prep: main must be regenerated with package_name = device_limit,
and feature/data-in-data-out prepared, before this session.
```

---

## One Repo, One venv

```bash
cd 3R-package-demo
python3.12 -m venv .venv
source .venv/bin/activate
```

The venv lives **inside the repo folder**.

`.venv/` is in `.gitignore`: **never committed.**

```notes
A virtual environment is a separate Python with its own installed packages.
Show .gitignore live: grep venv .gitignore. The venv is rebuilt from the
package's declared dependencies, never copied or pushed. Do NOT copy a
.venv folder to another machine or repo: it appears to work, then breaks.
```

---

## Why One per Repo?

```text
repo A needs pandas 1.5
repo B needs pandas 2.2
one shared Python → one of them breaks
```

**Each repo gets its own Python and its own packages.**

```notes
Ask: "What happens if both repos install into the same Python?" The second
install silently replaces the first one's pandas. One repo, one venv means
installing for one project can never break another.
```

---

## Which Python Am I Using?

```bash
which python      # before: system Python
source .venv/bin/activate
which python      # after: .venv/bin/python
pip list          # only this repo's packages
```

**Activate in every new terminal.**

```notes
Run both before and after activation live. MOST COMMON MISTAKE: activation
does not install anything; it only chooses which Python and pip you use.
If a command is "not found", check which python first.
```

---

## Stage 3: Dependencies Declared

Stage 2 crashed on a newer pandas. Stage 3 adds `requirements.txt`.

```text
Run in order:        DEV-C reaches the limit on 2026-01-16
Rerun one cell:      DEV-C reaches the limit on 2026-01-04
```

**The answer depends on which cells ran.**

```notes
Still a notebook plus helper files. The tool for this pain: functions with
inputs and outputs, in a package. That is what the Reference Backend repo
shows next.
```

---

## Stage 4: An Installable Package

The analysis is now `device_limit`. Run from another folder:

```text
FileNotFoundError: 'data/device_counts.csv'
```

A harmless cleanup moves DEV-C from 2026-01-16 to 2026-01-06. **No warning.**

```notes
Two pains remain: the data path is relative to where you stand, and nothing
checks the answer. Session 3's tool: tests. Files: the device-example
folder of the Sandbox (https://github.com/drweihungpan-lab/3R-sandbox).
```

---

## On `main`: The Template

```bash
pip install -e '.[test]'
device_limit --message "hello"
```

```text
Hello world!: hello
```

It runs. **But it does not process any data yet.**

```notes
Inside the activated venv. This is what every group has right now. The
template gives the shape: the package, the command, the logs. The
processing is ours to write.
```

---

## Data In, Data Out

```text
device_counts.csv  →  device_limit  →  limits.csv
(device_id, date,      predict the       (device_id,
 daily_count)          limit date        limit_date)
```

**Same input, same output, every time.**

```notes
This is the shape of every Backend repo in the course: a CSV goes in, a CSV
comes out, from the command line. In Session 4 the same function sits
behind an API, and in Session 5 it runs on your own data.
```

---

## Another Version of the Code

```bash
git switch feature/data-in-data-out
pip install -e '.[test]'
```

**I just switched to another version of the code.**

How? We will see in a moment.

```notes
The hook for the Git part. Do not explain branches yet: let the question
hang. Reinstall because the branch adds pandas to install_requires; the
venv must match the code.
```

---

## Run It From the Command Line

```bash
device_limit --input data/device_counts.csv --output limits.csv
cat limits.csv
```

**Three rows: DEV-A, DEV-B, DEV-C.** One `limit_date` each.

```notes
Point out the processing (predict_limit_dates) does not know about the
command line; click is a thin layer around it.
```

---

## The Command-Line Tool

`--input`: an existing CSV with `device_id`, `date`, `daily_count`.

`--output`: the file to write.

A missing column **stops the run** with a clear message. No half answers.

```notes
Demo the failure too: remove a column from a copy of the CSV and run it.
The error message is part of the design. --version prints the package
version.
```

---

## Logs Tell You What Ran

```text
INFO: Read 1095 rows from data/device_counts.csv
```

Logs go to the **terminal**. The result goes to the **output file**.

`LOGLEVEL=DEBUG` shows more. `WARNING` shows less.

```notes
Prefer logging over print, so you can change the detail without editing
code. The logger comes from the template: you got it for free.
```

---

## Check the Answer: Checksum

```bash
shasum -a 256 limits.csv
```

Same SHA-256 means **byte-for-byte identical** files.

Compare with `data/expected_limits.sha256`.

```notes
A checksum is a short fingerprint of a file. Every student who runs the
branch must get the same value: repeatability, checked by a machine.
```

---

## Git: Three Places

```text
working folder  --commit-->  local repo  --push-->  GitHub
                                         <--pull--
                <------------- clone -------------
```

**You typed these commands last week.** Today they get names.

```notes
Draw this on the board too. Working folder: the files you edit. Local repo:
the history in .git/. GitHub: the shared copy everyone sees. Every command
today moves changes along one arrow.
```

---

## `git clone`: Get a Copy

```bash
git clone git@github.com:drweihungpan-lab/3R-package-demo.git
```

Copies the **whole history** from GitHub to your computer.

You do this **once** per repo.

```notes
Run it live in a scratch folder. Point out it is not a download of files
only: git log works immediately, because the history came too.
```

---

## `git commit`: Save a Snapshot

```bash
git status
git add README.md
git commit -m "Describe the device example in README"
```

A commit is a **snapshot with a message**. Say **what and why**.

```notes
git add chooses what goes into the next snapshot; git commit records it in
the local repo. Nothing is on GitHub yet. A good message lets a reviewer
understand the change without opening the files.
```

---

## `git push`: Share It

```bash
git push
```

Sends your new commits **from the local repo to GitHub**.

Now your teammates can see them.

```notes
Refresh the repo page on GitHub to show the new commit. If push is
rejected, someone else pushed first: that is what pull is for.
```

---

## `git pull`: Get Their Work

```bash
git pull
```

Brings a teammate's commits **from GitHub to your computer**.

**Pull before you start working.**

```notes
New for most students: last week only one person pushed. Demo: edit a file
on GitHub's web editor, commit there, then git pull locally and show it.
```

---

## Why Branches? (1/2)

**1. `main` must always work.** Others install it and use it.

**2. Work in progress stays isolated** until it is reviewed.

```notes
Back to the hook: feature/data-in-data-out is unfinished work. main is
still the working template. Switching branches is how I showed both
versions in the same folder.
```

---

## Why Branches? (2/2)

**3. Several people work at once** without overwriting each other.

**4. A pull request needs a branch.** Review happens there.

```notes
Each teammate works on their own branch. The pull request compares a
branch with main, and is the place to discuss and review the change
before it lands.
```

---

## Working With Branches

```bash
git switch -c feature/readme-update   # create and switch
git branch                            # list branches
git switch main                       # go back
```

**Name the branch after the change.**

```notes
-c creates the branch. A branch is just a movable label on a commit:
creating one is instant and free. Use the feature/ prefix in this course.
```

---

## From Branch to Pull Request

```bash
git push -u origin feature/data-in-data-out
```

Open the PR. A teammate **reviews**. Then **merge**.

```bash
git switch main
git pull
```

```notes
Open the PR live for feature/data-in-data-out. A meaningful review names a
specific line or behavior, not just "LGTM". After merge, everyone pulls
main to get the change.
```

---

## The Check on Your PR

Your repo ships `.github/workflows/github_actions.yml`.

GitHub runs it on **every push and pull request**.

**Green means one commit passed these checks, not that everything is right.**

```notes
Students will see this check on their own PR in the hands-on. Today: only
what it is. The test job is commented out with #; in Session 3 you switch
it on and add tests.
```

---

## Optional: A Merge Conflict

Two branches change **the same line**.

Git cannot choose, so **you** decide.

```text
<<<<<<< main
...
=======
...
>>>>>>> feature/readme-update
```

```notes
Optional, only if time allows. Make two branches edit the same README line,
merge one, then merge the other. Edit the file to keep the right text,
delete the markers, add, commit. A conflict is a signal to talk to your
teammate, not an error.
```

---

## Hands-On

1. **One venv** in your Backend repo. Install. Run the template command.
2. Branch, small change, commit, push.
3. PR, review, merge, `git pull`.

[Exercise](../exercises/session-2.md) has the steps.

```notes
Circulate constantly. Your Backend repo is where the PR and review count as
final evidence; the Sandbox does not count.

COMMON PROBLEMS:
  - venv not activated: which python shows the system Python
  - Pushing to main instead of the branch
  - Forgot git pull after merge: local main is behind
```

---

## Prepare for Session 3

**Today:** a reviewed, merged pull request in your Backend repo.

**Homework:** 2 hours + practice.

**Next:** tests, CI, and automatic Releases.

```notes
Session 3: once a PR is approved and merged, CI runs the tests and creates
the Release with semantic-release. Remind: Show-and-tell again at the start
of Session 3. Anyone may be asked.
```
