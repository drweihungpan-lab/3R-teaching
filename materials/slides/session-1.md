# Session 1: From Jupyter to Production

**Today:** Isolate Python. Declare dependencies. Generate a package. Push to GitHub.

```notes
Hands-on course. Introduce yourself. This is not "listen and I'll tell you
everything" — this is "you will build." Emphasize the three outcomes below.
```

---

## This Course Is Hands-On

Work along with me. Listen + code, don't just listen.

**Session 0 setup is a prerequisite:** Git, SSH, Python 3.12, terminal.

If something is broken, let me know now.

```notes
10 minutes total here. This is the opening. Emphasize: you will code along,
not just listen. If setup is broken, offer help after. Let them ask questions.
```

---

## Mandatory Homework + Checklist

After Sessions 1–4: **2-hour homework** plus unfinished practice.

At the start of the next session: **I will ask someone to show their work.**

Anyone. Be ready.

```notes
This establishes accountability. Homework is not optional. You will check
their work, and they know this upfront.
```

---

## Your Repositories Are Public

Never commit:
- Real data
- Personal information
- Passwords or tokens

Your Backend repo will be public. Plan accordingly.

```notes
This is a hard rule. No exceptions. Explain why: you need to share your
package, so it must be public. Keep secrets out from the start.
```

---

## Final Assessment

**Pass/fail at Session 5.** No resubmission. Everyone presents.

Work alone or in a group (up to 3).

**Use AI, but explain every line you write.**

```notes
Final and clear. Assessment is at the end, not mid-course. If they don't
understand something, they learn it now. AI is a tool, not a shortcut to
avoid understanding.
```

---

## 170 Minutes Ahead

- **0–35:** Opening, bubble tea, five sessions, why Jupyter fails.
- **35–50:** venv, requirements.txt, cookiecutter.
- **50–60:** Break.
- **60–100:** Package structure + git.
- **100–170:** 70-minute hands-on.

```notes
Then homework: 2 hours tonight, plus unfinished practice.

This is a visual timeline. Each session builds one layer. By Session 5 it all
comes together: venv (Session 1) + git (Session 2) + tests (Session 3) + API +
Docker (Session 4) + your own data (Session 5).
```

---

## Your Bubble Tea Shop

Rave reviews at demo day. Now opening in front of NTHU.

**How do you ensure every customer gets the same tea?**

```notes
Ask 4 students, one at a time, random. Do NOT steer toward "three Rs". Keep
to 5 minutes. Write a few answers on the board — you'll return to them.

The question is about keeping results the same every time.
```

---

## The Five-Session Stack

**A visual journey from notebook to deployed application:**

```
Session 1: Environments + Packages
   Isolated Python (venv)
   Declared dependencies (requirements.txt)
   Package template (cookiecutter)
         ↓
Session 2: Collaboration + Release
   Branches, pull requests, reviews
   Version tags (Release)
   Install from git URL
         ↓
Session 3: Validation + CI
   Tests (pytest)
   Automated checks (GitHub Actions)
   Required checks before merge
         ↓
Session 4: API + Containers
   API layer (FastAPI)
   Container images (Docker)
   Service orchestration (Compose)
         ↓
Session 5: Final Showcase
   Your data, all five layers
```

**Your device example** (synthetic medical device predictions) will follow this path through all five sessions.

```notes
Each session adds one layer. By Session 5 students see the complete stack
applied to both the device example and their own data.

Point out: Session 1 is foundations (Python isolation), Session 2 adds
collaboration (branches, reviews), Session 3 adds safety (tests, checks),
Session 4 adds deployment (API, containers), Session 5 showcases all.
```

---

## Why Jupyter Isn't Enough

**Send your notebook to a colleague.**

Same data. Same Python file. Same computer.

**Do they get the same numbers?**

```notes
Pause 20 seconds. Collect answers.
```

---

## Notebooks Don't Track Versions

Different package versions break the results.

Different Python versions cause crashes.

Cells can be edited or run out of order.

**Nothing records which version produced which result.**

```notes
Ask: "What else?" Listen for 1–2 minutes. Then synthesize into the three
solutions below.
```

---

## Three Solutions

**1. Isolated environment:** One Python, declared versions.

**2. Package structure:** Reusable code, entry points.

**3. Version control:** History of which code produced results.

Build all three today.

```notes
You just asked students to name these. Connect their answers to these three
solutions.
```

---

## Stage 1: One Notebook, Three Copies

```
analysis_v1.ipynb  →  Result: 2026-01-30
analysis_v2.ipynb  →  Result: 2026-01-28
analysis_v3.ipynb  →  Result: 2026-01-26
```

**Three notebooks. Three dates. Last month named one. Which?**

Nothing records it.

```notes
Show the stage READMEs from device-example in the Sandbox.
```

---

## Stage 2: Helpers Without Versions

```
Python 3.11 + pandas 1.5  →  Result: 2026-01-30
Python 3.12 + pandas 2.x  →  AttributeError
```

Same code. Same machine. Different result.

```notes
This is what happens when you don't declare dependencies.
The tool that fixes it: venv + requirements.txt.
```

---

## Solution 1: Virtual Environments

**One project = one isolated Python installation.**

```bash
python3.12 -m venv .venv
source .venv/bin/activate    # Mac/Linux
```

- Create fresh for each project.
- Activate in every new terminal.
- **Do NOT copy `.venv` folders.**
- Never commit it to Git.

```notes
"Separate area" is the whole idea. This project's packages don't mix with
yours globally or with another project's.

MOST COMMON MISTAKE: Activation doesn't install packages. It only chooses
which Python and pip you use. Say this aloud.
```

---

## Solution 2: Declared Dependencies

**A `requirements.txt` file lists exact packages + versions.**

```txt
pandas==2.0.3
numpy==1.24.0
scikit-learn==1.3.0
click==8.1.7
```

Others reproduce your environment:

```bash
pip install -r requirements.txt
```

**Same packages. Same versions. Same results.** This is **repeatability**.

```notes
Never copy `.venv`. It appears to work then breaks.

Use `pip freeze` to record exact versions before comparing environments
across machines.
```

---

## Solution 3: Package Structure

**Cookiecutter generates a package from a template.**

```bash
cookiecutter https://github.com/drweihungpan-lab/3R-cookiecutter
```

Creates: `setup.cfg`, `src/my_backend/`, `tests/`, docs.

30 minutes of boilerplate, automated.

```notes
The template is at the GitHub link. You'll run it in hands-on to generate
your Backend repo. It ensures consistency across the class and saves time.
```

---

## Inside the Package: `setup.cfg`

```ini
[metadata]
name = my-backend
version = 0.1.0
author = Your Name

[options]
install_requires =
    pandas>=2.0
    click>=8.1

[options.entry_points]
console_scripts =
    my-backend=my_backend.cli:main
```

**What this says:** "When someone `pip install my-backend`, install pandas and click, and create a command called `my-backend`."

```notes
Take 10 minutes here. Walk through each section and what it means for
consumers of your package.
```

---

## Inside the Package: `src/my_backend/`

```
src/
  my_backend/
    __init__.py      ← Marks this as a package
    cli.py           ← Command-line interface
    process.py       ← Processing logic
```

When someone installs your package, they can `import my_backend` from anywhere.

**Standard structure.** Any Python developer recognizes it immediately.

```notes
This is what `pip install .` creates. The src/ layout is industry-standard
and keeps tests separate from installed code.
```

---

## Inside the Package: `tests/`

```
tests/
  test_process.py    ← Tests for processing logic
  test_cli.py        ← Tests for the command line
```

You'll write these in Session 3. For now, know they go here.

Each test documents the behavior you promise. Session 3 teaches validation.

```notes
Tests live separately from your code. Session 3 (pytest + GitHub Actions)
will validate them automatically before merging.
```

---

## Generated Package Structure

**Here's what cookiecutter creates:**

```
my-backend-repo/
├── .git/
├── .gitignore
├── src/
│   └── my_backend/
│       ├── __init__.py
│       ├── cli.py
│       └── process.py
├── tests/
│   ├── test_cli.py
│   └── test_process.py
├── setup.cfg
├── README.md
└── pyproject.toml
```

This is **your Backend repo for the rest of the course.**

Session 2 will teach you branches, pull requests, and how to collaborate on it.

```notes
Walk through the structure. Each section has a purpose. This becomes the
home for your group's code for Sessions 2–5.
```

---

## Your First Backend Repo

**Timeline:**

1. **10 min:** SSH key, create repo.
2. **30 min:** Cookiecutter, commit, push.
3. **30 min:** Verify public.

[Exercise](../exercises/session-1.md) has detailed steps. Ask if stuck.

```notes
70 minutes is a large block. Circulate constantly.

COMMON PROBLEMS:
  - SSH key not in GitHub: they can't push
  - Cookiecutter not installed: `pip install cookiecutter`
  - Pushing to wrong repo: local folder but push to template instead
  - Generated folder in wrong place: `find . -name 'src' -type d`

The exercise covers all of these.
```

---

## Prepare for Session 2

**Today:** Backend repo created and pushed.

**Homework:** 2 hours + practice.

**Next:** Branches, pull requests, reviews, Releases.

Install and verify a teammate's Release.

[Syllabus](../../SYLLABUS.md) has requirements.

```notes
Close by minute 168. Preview Session 2: now that you have a package structure,
learn how teammates collaborate (branches, reviews), mark a version
(Release), and install a Release to verify it works.
```
