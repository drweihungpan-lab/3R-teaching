### 3R COURSE · SESSION 2
# Session 2: venv and Git

**Today:** Share last week. Finish cookiecutter. One repo, one venv. Git, branches, review.

```notes
Open warmly. Today builds directly on the Backend repo every group pushed in
Session 1. Nothing new is generated today: we use what you already have.
```

---

### WARM-UP
## Show-and-Tell

**What did you do in the Session 1 exercise?**

**What was difficult?**

Nothing to prepare. Just tell us.

```notes
Keep this short: two or three students, a few minutes in total. Informal
sharing, not a presentation. Write every difficulty on the board: you will
come back to them in the cookiecutter slides. Expect: SSH keys, cookiecutter
not found, files in the wrong folder, hyphens in package_name.
```

---

### COURSE FORMAT
## Today's Plan

1. **Finish cookiecutter**
2. **The three Rs**
3. **venv, pip, and the CLI**
4. **Git and branches**
5. **Pull requests and review**
6. **Hands-on**

```notes
No timings on purpose. The cookiecutter part closes what Session 1 started;
the three Rs slide explains why the venv matters; then the Git part, which
ends in a pull request that a classmate reviews.
```

---

### ANALOGY
## Back at the Bubble Tea Shop

**Your best staff member is sick today.**

**Can someone else still make your tea?**

```notes
Ask 2–3 students. Steer toward: only if the recipe is written down, in the
same place, in the same shape, every time. That is what a template gives
a repository.
```

---

### FAILURE MODES · COPYING
## Why Not Just Copy a Repo?

1. **Old names** stay in `setup.cfg`, imports and the entry point.
2. **Their `.git`** comes along: you push to their repo.
3. A copied **`.venv`** breaks.
4. **Template fixes** never arrive.

```notes
The tempting shortcut: copy a friend's repo folder and rename it. Walk
through each card.

1. Their package name is still in setup.cfg, in every import and in the
   console_scripts entry point. Missing one of them breaks the command.
2. The hidden .git folder is copied too, with their history and their
   remote. git push then goes to THEIR repo, or is rejected.
3. A .venv contains absolute paths to the original folder. It looks fine,
   then fails with confusing errors.
4. When the template is fixed, a copied repo never hears about it.

Cookiecutter avoids all four: it asks for your names and writes fresh files.
```

---

### TEMPLATES · READABILITY
## Why Cookiecutter? Readability

Every group's repo has the **same shape**.

`src/`, `tests/`, `setup.cfg`, `Makefile`: always in the same place.

> [!TIP] **Open any repo and you already know where to look.**

```notes
Readability is about the structure, not the code. A newcomer, a reviewer,
or you in six months finds the processing in src/<package>/ and the tests
in tests/ without asking anyone.
```

---

### TEMPLATES · SHAREABILITY
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

### TEMPLATES · MAINTENANCE
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

### FAILURE MODES
## Pitfall: Hyphens in Names

```text
package_name = device-analysis-demo
→ from device-analysis-demo import hello_world
→ SyntaxError
```

`repo_name` may contain hyphens.

> [!CAUTION] `package_name` **must be a valid Python name.**

Use `device_analysis`, not `device-analysis-demo`.

```notes
Python names cannot start with a digit or contain "-". pip install may still
succeed, but the command fails the moment you run it. If any group hit this
in Show-and-tell, point at them (kindly).

This is the maintenance story in action: the right fix is a check in the
template itself that rejects an invalid package_name, so nobody hits it
again. That template change is coming.
```

---

### THE THREE RS
## Three Ways Results Should Agree

1. **Repeatability:** same conditions. Run twice on your laptop.
2. **Replicability:** slightly different. A classmate's laptop and venv.
3. **Reproducibility:** very different. Independent re-implementation.

> [!TIP] **Today's venv protects replicability.**

```notes
Course definitions, from GLOSSARY.md:
- Repeatability: agreement between results from successive runs of the
  same process under the same conditions.
- Replicability: agreement from the same process under slightly different
  conditions, such as another machine or a fresh environment.
- Reproducibility: agreement under very different conditions, such as an
  independent re-implementation of the analysis.

Terminology varies between disciplines; in this course these meanings
govern. The venv is what lets a classmate's laptop run the same code with
the same declared packages: replicability.
```

---

### REFERENCE REPO
## The Reference Backend Repo

My own Backend repo, **generated from the same template as yours.**

[device_analysis_demo](https://github.com/drweihungpan-lab/device_analysis_demo)

I show each step there first. You do it in yours.

```notes
Reference Backend repo: same template, same structure. Package name
device_analysis, command device_analysis. Its main branch is the template
output, like yours: hello_world with a --message option.

Instructor prep: clone 3R-device-example next to it, so that
../3R-device-example/data/device_counts.csv exists. Rehearse the
mean-per-device change on a local branch and keep it as a fallback.
```

---

### ENVIRONMENTS
## One Repo, One venv

```bash
cd device_analysis_demo
python -m venv .venv
source .venv/bin/activate
```

The venv lives **inside the repo folder**.

> [!CAUTION] **Never commit** `.venv/`. It is listed in `.gitignore`.

```notes
A virtual environment is a separate Python with its own installed packages.
Show .gitignore live: grep venv .gitignore. The venv is rebuilt from the
package's declared dependencies, never copied or pushed. Do NOT copy a
.venv folder to another machine or repo: it appears to work, then breaks.
```

---

### ENVIRONMENTS · ISOLATION
## Why One per Repo?

```text
repo A needs pandas 1.5
repo B needs pandas 2.2
one shared Python → one of them breaks
```

> [!TIP] **Each repo gets its own Python and its own packages.**

```notes
Ask: "What happens if both repos install into the same Python?" The second
install silently replaces the first one's pandas. One repo, one venv means
installing for one project can never break another.
```

---

### ENVIRONMENTS · CHECK
## Which Python Am I Using?

```bash
which python      # before: system Python
source .venv/bin/activate
which python      # after: .venv/bin/python
pip list          # only this repo's packages
```

> [!WARNING] **Activate in every new terminal.**

```notes
Run both before and after activation live. MOST COMMON MISTAKE: activation
does not install anything; it only chooses which Python and pip you use.
If a command is "not found", check which python first.
```

---

### TEMPLATE ANATOMY
## On `main`: The Template

```bash
pip install .
device_analysis --message "hello"
```

```text
Hello world!: hello
```

It runs. **But it does not process any data yet.**

```notes
Inside the activated venv. Note: pip install . copies the package into
the venv. Remember this; it comes back in the
branch demo.

This is what every group has right now. The template gives the shape: the
package, the command, the logs. The processing is ours to write.
```

---

### PACKAGING · PIP INSTALL
## What Does `pip install .` Do?

```text
pip install .
→ reads setup.cfg
→ installs click (install_requires)
→ copies device_analysis into .venv
→ creates the device_analysis command
```

**One command** turns the folder into an installed package.

> [!TIP] **`setup.cfg` is the recipe; pip follows it.**

```notes
The "." means "the package in this folder". pip reads setup.cfg (and
pyproject.toml for the build tool), installs every library listed under
install_requires, copies the package into the venv's site-packages, and
writes a small launcher script into .venv/bin.

Show it live: ls .venv/bin shows device_analysis; pip show device_analysis
shows the version and where it was installed. After this, import
device_analysis works from any folder while the venv is active.
```

---

### TEMPLATE ANATOMY · MAKEFILE
## You Already Have It: `make install`

```bash
make help          # list the targets
make install       # pip install .
make install-dev   # pip install -e .[test,dev]
```

The template's `Makefile` **names the commands**, so everyone types the same thing.

> [!TIP] **CI runs the same targets:** `make install-test`.

```notes
Open the Makefile live. Each target is a name for one or more commands;
make help lists them with their descriptions. make install is exactly
pip install . (a copy). make install-dev is the editable install plus the
test and dev tools: the one you want while developing. Remember the
difference; it comes back in the branch demo.

Open .github/workflows/github_actions.yml: CI calls make install-test and
make test-... . The same names on your laptop and in CI means "it works on
my machine" and "it works in CI" run the same commands.
```

---

### PACKAGING · DEPENDENCIES
## `setup.cfg` or `requirements.txt`?

```text
setup.cfg          click          any version
requirements.txt   click==8.1.3   exact pin
```

`pip install .` reads **`setup.cfg` only**.

`pip install -r requirements.txt` installs **the exact pins**.

```notes
A common misunderstanding: pip install . does NOT read requirements.txt.
It installs what install_requires in setup.cfg asks for, at whatever
version is newest today.

requirements.txt pins every package, including the packages your packages
need, to one exact version. CI and the Dockerfile install it first
(pip install -r requirements.txt), then the package, so every run gets the
same versions. That is repeatability and replicability for dependencies.

setup.cfg says what the package needs; requirements.txt records the exact
versions we tested with.
```

---

### PACKAGING · DEPENDENCIES
## Update `requirements.txt`

```bash
pip install pip-tools        # once per venv
make update-requirements    # pip-compile setup.cfg
git add setup.cfg requirements.txt
```

Run it **after you change `install_requires`**.

> [!WARNING] **Never edit it by hand.** It is generated.

```notes
make update-requirements runs pip-compile from pip-tools, so install
pip-tools once in the venv first. pip-compile reads setup.cfg,
resolves the newest versions that fit, and writes them all pinned into
requirements.txt, with a comment saying which package needed each one.

Commit setup.cfg and requirements.txt in the same PR, so the reviewer sees
both. In the branch demo we add pandas to install_requires: that is
exactly when to run it.
```

---

### COMMAND LINE · WHY
## Why a Command-Line Tool?

1. **Anyone can run it.** No notebook, no Python prompt.
2. **Same command** on any laptop and in CI.
3. **Docker calls it:** `ENTRYPOINT ["device_analysis"]`.
4. **Options are the interface:** `--input`, `--help`, `--version`.

```notes
A function is only usable by someone who writes Python around it. A
command is usable by anyone with a terminal: a teammate, a script, a CI
job, a container. That is replicability in practice: the same command,
typed the same way, on a different machine.

Show the template's Dockerfile: its ENTRYPOINT is the command, so running
the container runs the tool. The options are the contract: --help documents
them for free. In Session 4 the same function also gets an API; the CLI
stays.
```

---

### COMMAND LINE · ENTRY POINT
## Where the Command Comes From

```text
[options.entry_points]
console_scripts =
    device_analysis =
        device_analysis.scripts.
        device_analysis_script:device_analysis_cli
```

`pip install` reads this and **creates the command**.

Name on the left. **Python function** on the right.

```notes
In the real setup.cfg the right-hand side is one line:
device_analysis.scripts.device_analysis_script:device_analysis_cli
module path, a colon, then the function. Open the script live: a small
click function that reads the options and calls the processing function.
The processing does not know about the command line; click is a thin
layer around it. Change the entry point, and you must reinstall.
```

---

### COMMAND LINE · LOGGING
## Logs Tell You What Ran

```text
INFO: This is INFO level log message
WARNING: This is WARN level log message
ERROR: This is ERROR level log message
```

Logs go to the **terminal**, beside the result.

`LOGLEVEL=DEBUG` shows more. `LOGLEVEL=ERROR` shows less.

```notes
hello_world logs at four levels: DEBUG, INFO, WARNING, ERROR. The default
level is INFO, so DEBUG is hidden. Each real line also starts with a
timestamp and the function name. Demo:
  LOGLEVEL=DEBUG device_analysis --message hi    # four log lines
  LOGLEVEL=ERROR device_analysis --message hi    # one log line
Prefer logging over print, so you can change the detail without editing
code. The logger comes from the template: you got it for free.
```

---

### GIT · MENTAL MODEL
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

### GIT · CLONE
## `git clone`: Get a Copy

```bash
git clone git@github.com:drweihungpan-lab/device_analysis_demo.git
```

Copies the **whole history** from GitHub to your computer.

You do this **once** per repo.

```notes
Run it live in a scratch folder. Point out it is not a download of files
only: git log works immediately, because the history came too.
```

---

### GIT · COMMIT
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

### GIT · PUSH
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

### GIT · PULL
## `git pull`: Get Their Work

```bash
git pull
```

Brings a teammate's commits **from GitHub to your computer**.

> [!TIP] **Pull before you start working.**

```notes
New for most students: last week only one person pushed. Demo: edit a file
on GitHub's web editor, commit there, then git pull locally and show it.
```

---

### BRANCHES · WHY
## Why Branches? (1/2)

1. `main` **must always work.** Others install it and use it.
2. **Work in progress stays isolated** until it is reviewed.

```notes
main is the working template. The change we are about to make is
unfinished work: it lives on a branch until someone has reviewed it.
```

---

### BRANCHES · WHY
## Why Branches? (2/2)

3. **Several people work at once** without overwriting each other.
4. **A pull request needs a branch.** Review happens there.

```notes
Each teammate works on their own branch. The pull request compares a
branch with main, and is the place to discuss and review the change
before it lands.
```

---

### BRANCHES · MENTAL MODEL
## How a Branch Works

```text
A --- B --- C              <-- main
             \
              D --- E      <-- feature/device-summary
```

A branch is a **label on a commit**.

A new commit **moves the label** forward.

> [!TIP] **Merging moves `main` to include D and E.**

```notes
Draw it on the board. Commits are the snapshots; a branch is only a name
pointing at one of them. git switch -c creates a new label on the current
commit, which is why it is instant and free. Committing on the branch moves
only that label; main stays at C. After the PR is merged, main includes D
and E, and git pull brings that to everyone's computer.
```

---

### BRANCHES · COMMANDS
## Working With Branches

```bash
git switch -c feature/device-summary  # create and switch
git branch                            # list branches
git switch main                       # go back
```

> [!TIP] **Name the branch after the change.**

```notes
-c creates the branch. Use the feature/ prefix in this course. Create
feature/device-summary live in device_analysis_demo: it is the branch for
the next three slides.
```

---

### SOLUTION · DATA IN, DATA OUT
## On the Branch: Mean per Device

```bash
device_analysis --input ../3R-device-example/data/device_counts.csv
```

```text
DEV-A  174.00
DEV-B  209.94
DEV-C  254.77
```

**A CSV goes in. One mean `daily_count` per device comes out.**

```notes
Live demo on feature/device-summary in device_analysis_demo:
- In device_analysis.py, replace hello_world with a function that reads the
  CSV with pandas and returns the mean daily_count per device_id.
- In the CLI script, replace --message with --input.
- In setup.cfg, add pandas to install_requires.
The CSV has columns device_id, date, daily_count. It stays in the
3R-device-example folder; do not copy it into the repo.

The processing function does not know about the command line; click is a
thin layer around it. Exact formatting of the output depends on how you
print it.
```

---

### PITFALL · STALE INSTALL
## Pitfall: The Old Code Still Runs

```bash
device_analysis --message "hello"
```

```text
Hello world!: hello
```

I changed the code. **The venv still runs the copy from `pip install .`**

```notes
Show this deliberately. Run the old command: it still prints Hello world,
although hello_world no longer exists in the folder. Running with --input
fails with "No such option: --input" for the same reason.

pip install . (without -e) copied the package into .venv at install time.
Editing the folder afterwards changes nothing in the venv.
```

---

### SOLUTION · REINSTALL
## Reinstall After Every Change

```bash
make update-requirements
pip install -r requirements.txt
pip install .
device_analysis --input ../3R-device-example/data/device_counts.csv
```

`pip install .` copies **today's code** into the venv.

> [!TIP] **Edit, reinstall, run.**

```notes
Now the mean per device appears. Because we added pandas to
install_requires, first regenerate requirements.txt so it pins pandas,
then install in the same order as the Dockerfile: the pinned dependencies,
then the package. For a code-only change, pip install . alone is enough
(or make install).

The venv must match the code. If the output looks old, the first question
is: did I reinstall?

Some developers use pip install -e . (an editable install) so edits apply
without reinstalling. We do not need it in this course; reinstalling keeps
your venv the same as the Docker image.
```

---

### PULL REQUESTS
## From Branch to Pull Request

```bash
git add src/ setup.cfg requirements.txt
git commit -m "Report mean daily count per device"
git push -u origin feature/device-summary
```

Open the PR on GitHub: **compare your branch with `main`.**

```notes
Push the branch live, then open the PR from the banner GitHub shows. Write
a title and a short description: what changed and how to run it. Point
out the Files changed tab: it is where the review happens next.
```

---

### PULL REQUESTS · REVIEW
## Code Review on GitHub

1. Open **Files changed**.
2. Click a line: leave a **comment**.
3. **Review changes → Approve.**
4. The **author merges.**
5. Everyone: `git switch main && git pull`.

```notes
Demo on the PR you just opened, with a student or a second account as the
reviewer. A meaningful review names a specific line or behaviour, not just
"LGTM": for example, "what happens if daily_count is missing?".

The reviewer approves; the author, not the reviewer, merges. After merge,
everyone switches to main and pulls to get the change. Show git log: main
now includes the branch's commits, as in the branch diagram.
```

---

### OPTIONAL · CONTINUOUS INTEGRATION
## Optional: The Check on Your PR

Your repo ships `.github/workflows/github_actions.yml`.

GitHub runs it on **every push and pull request**.

> [!WARNING] **Green means one commit passed these checks,** not that everything is right.

```notes
Optional, only if time allows. Students will see this check on their own
PR in the hands-on. Today: only what it is. The test job is commented out
with #; in Session 3 you switch it on and add tests.
```

---

### OPTIONAL · CONFLICTS
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

### HANDS-ON
## Hands-On

1. **venv**, then install like the Dockerfile.
2. **Branch:** your own function and CLI.
3. **Push, open a PR,** post the link.
4. **Review** one PR. Merge after approval.

[Exercise](../exercises/session-2.md) steps.

```notes
60 minutes. Circulate constantly. Work happens in each student's own
Backend repo; the Sandbox only holds the "Session 2 check-in" issue where
PR links are posted. Any data in the repo must be synthetic.

Review rule: review the nearest earlier link in the check-in issue that
has no thumbs-up yet (the first poster reviews the last link). A review is
Approve plus at least one line comment; then add a thumbs-up to that
check-in comment. Merge your own PR only after it is approved.

COMMON PROBLEMS:
  - venv not activated: which python shows the system Python
  - Stale output after editing: forgot to rerun pip install .
  - Install order, as in the Dockerfile: pip install -r requirements.txt,
    then pip install .
  - Pushing to main instead of the branch
  - Forgot git pull after merge: local main is behind
```

---

### NEXT SESSION
## Prepare for Session 3

**Today:** a pull request in your Backend repo, link posted.

**At home:** review, get approved, merge. Before Session 3.

**Next:** tests, CI, and automatic Releases.

```notes
The exercise is finished at home (about 2 hours): review, approval and
merge must all be done before Session 3 starts. Session 3: once a PR is
approved and merged, CI runs the tests and creates the Release with
semantic-release. Remind: Show-and-tell again at the start of Session 3.
Anyone may be asked.
```
