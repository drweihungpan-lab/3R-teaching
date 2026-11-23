# Session 1: From Jupyter to a shareable package

Learn to isolate Python, declare dependencies, generate a package template, and push your code.

- Understand why notebooks alone don't work for reproducible work.
- Create an isolated environment with requirements.
- Use cookiecutter to generate a package structure.
- Clone, generate, and push your first Backend repo.

```notes
This is a hands-on course, not a lecture. Introduce yourself first, then set
the three outcomes above. Emphasize: "This is not 'listen and I'll tell you
everything'; this is 'you will build'."
```

---

## Our 170-minute route

- 00–10: Opening — introductions and class rules.
- 10–15: Bubble tea shop — a question for the five sessions.
- 15–25: Course overview — how the five sessions build on each other.
- 25–35: Device example — why Jupyter is not enough.
- 35–50: Environments and packages — `venv`, `requirements.txt`, cookiecutter.
- 50–60: Break — 10 minutes.
- 60–80: Template walkthrough — `setup.cfg`, entry point, `src/`, `tests/`.
- 80–100: Generated structure — a visual and git concepts.
- 100–170: Hands-on — 70 minutes to create and push your Backend repo.

Unfinished practice continues at home, in addition to the homework.

---

## Welcome to 3R: Repeatability, Reproducibility, Replicability

Hi. I'm [your name], and this is a **hands-on course**, not a lecture you listen to. Bring your laptop and expect 60 minutes of practice every session. You'll learn a workflow used in real statistical engineering: environments, packages, tests, reviews, automation, and containers. By the end you'll have a working application and the confidence to build one again.

Before we dive in, the **class rules**:

1. **This is hands-on.** Listening alone will not get you through. Work along, ask questions, and use the break if you're stuck.
2. **Session 0 setup is a prerequisite.** Git, SSH key, Python 3.12, a terminal. If it isn't working, tell me now.
3. **Homework is mandatory** after Sessions 1–4, about two hours each. **At the start of the next session I will ask someone to show their work** — anyone, so be ready.
4. **Unfinished in-class practice continues at home**, on top of the homework.
5. **Your repositories are public.** Never commit real data, personal information, passwords, or tokens.
6. **Pass/fail, decided at the final presentation** in Session 5. Work alone or in a group of up to three. No resubmission, no retry. Everyone presents.
7. **Use AI assistants freely to learn**, but you must be able to explain every line you present. Code you cannot explain counts as not yours.

Questions?

```notes
Take about 10 minutes here. If a student's setup is broken, offer to help
after the opening. Emphasize "everyone presents" and "you must explain the
code" — they will use AI, and you want them to treat it as a learning tool,
not a shortcut to avoid understanding.
```

---

## Your bubble tea shop

Your bubble tea got great reviews at the demo day.

Now you open a shop in front of NTHU. You already have the best location and the decor.

**How does every customer get the tea they loved?**

```notes
Ask 4 students, one at a time, at random. Do not steer answers toward the
three Rs. Keep it to 5 minutes total. Write a few answers on the board; you
will return to them in two slides.

The question is about keeping the result the same every time, and that is
exactly what this course teaches.
```

---

## How the five sessions build on each other

```
Session 1: Environments + Packages
  ├─ Isolated Python (venv)
  ├─ Declared dependencies (requirements.txt)
  └─ Package template (cookiecutter)
         ↓
Session 2: Collaboration + Release
  ├─ Branches, pull requests, reviews
  ├─ Version tags (Release)
  └─ Install from git URL
         ↓
Session 3: Validation + CI
  ├─ Tests (pytest)
  ├─ Automated checks (GitHub Actions)
  └─ Required checks before merge
         ↓
Session 4: API + Containers
  ├─ API layer (FastAPI)
  ├─ Container images (Docker)
  └─ Service orchestration (Compose)
         ↓
Session 5: Final showcase
  └─ Demonstrate all five layers on your own data
```

Your **device example** (synthetic data for medical device predictions) will follow this same path through all five sessions, growing one stage per session. By Session 5 you will see it containerized and running.

```notes
This is a visual stack. Each session adds a layer. By Session 5 students see
the complete stack applied to both the device example and their own data.

Point out: Session 1 is foundations (Python isolation), Session 2 adds
collaboration (branches, reviews), Session 3 adds safety (tests, checks),
Session 4 adds deployment (API, containers), Session 5 showcases all of it.
```

---

## Why is Jupyter not enough?

**Think for a moment:** You send your colleague your notebook. They run it on their laptop. Same data, same Python file. Do they get the same numbers?

[Pause 20 seconds. Then invite answers.]

**What could go wrong?**

- Different versions of pandas, numpy, scikit-learn...
- Different Python version.
- Packages they don't have installed.
- They edited a cell you didn't see.
- They ran cells out of order.
- The notebook doesn't record which version produced which result.

A notebook is **discovery and exploration**. For work that others must reproduce — and work you must reproduce yourself in three months — you need:

1. **Isolated environment**: One project, one Python installation, declared versions.
2. **Package structure**: Reusable code, entry points, metadata.
3. **Version control**: History of exactly what code produced each result.

Today you'll build that stack.

```notes
This is a think-aloud with students, not a lecture at them. Listen to their
answers for 1–2 minutes, then synthesize into the three needs above.

The device example will show why each layer matters by showing what breaks
when you skip it.
```

---

## Device example: Stages 1 to 2

### Stage 1: One notebook, copied three times

```
analysis_v1.ipynb  →  DEV-C reaches limit on 2026-01-30
analysis_v2.ipynb  →  DEV-C reaches limit on 2026-01-28
analysis_v3.ipynb  →  DEV-C reaches limit on 2026-01-26
```

Three notebooks. Three dates. Last month's report named one of them. **Which one?** Nothing records it.

### Stage 2: Helper files, no declared dependencies

```
Python 3.11 + pandas 1.5  →  DEV-C reaches limit on 2026-01-30
Python 3.12 + pandas 2.x  →  AttributeError: 'DataFrame' object has no attribute 'append'
```

The notebook now imports `loader.py` and `model.py`. Reusable, but nothing says which packages and versions they need. Same files, different machines, different answers.

```notes
Show the stage READMEs from the device-example folder of the Sandbox.
Demonstrate or talk through Stages 1 and 2.

Name the tool that fixes each pain, but do not teach it yet:
  Stage 1 pain: "which copy?" → Tool: Git (records history)
  Stage 2 pain: "version crash" → Tool: venv + requirements (isolation +
    declared versions)

This builds to the three needs you just asked students to name.
```

---

## A Python environment belongs to one project

A virtual environment is a separate Python installation area, just for this project.

```bash
python3.12 -m venv .venv
source .venv/bin/activate    # Mac/Linux
# or:
.venv\Scripts\activate        # Windows
```

- Create `.venv` fresh for each project; activate it in every new terminal.
- Install declared dependencies into it, rather than copying someone else's `.venv`.
- Activation chooses which Python runs; it does not install packages.
- Never commit `.venv`; use `.gitignore`.

```notes
"Separate area" is the whole idea: this project's packages do not mix with
your global packages or with another project's.

Activation is per terminal. A new terminal, or a new VS Code panel, starts
deactivated, and that is the single most common confusion students face.

Activation does NOT install things; it only decides which Python and pip you
are talking to. This is the second-most common misconception.
```

---

## Declared dependencies in requirements.txt

A `requirements.txt` file lists the exact packages and versions your code needs.

```txt
pandas==2.0.3
numpy==1.24.0
scikit-learn==1.3.0
click==8.1.7
```

Others can then reproduce your environment:

```bash
pip install -r requirements.txt
```

Same packages, same versions, same results. This is **repeatability**.

```notes
Never copy a .venv folder. It appears to work and then breaks, because the
paths inside point to their machine.

pip freeze records the exact versions you have; use it before comparing
environments across machines.
```

---

## Cookiecutter: a template for packages

Cookiecutter is a tool that generates a project structure from a template. Instead of creating files by hand, you answer prompts and it fills in the template.

```bash
cookiecutter https://github.com/drweihungpan-lab/3R-cookiecutter
```

You'll be prompted:

```
project_name [My Project]:
author [Your Name]:
```

Then it generates a folder with the Python package structure, tests, documentation, and CI configuration — everything you need to push a real package.

```notes
The template is at https://github.com/drweihungpan-lab/3R-cookiecutter. You
will clone the template in the hands-on and run cookiecutter to generate your
Backend repo.

This saves about 30 minutes of manual folder creation and boilerplate, and it
ensures consistency across the class.
```

---

## Inside the package template

Once cookiecutter generates your folder, here's what matters:

### `setup.cfg` — Package metadata and dependencies

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

This says: "When you `pip install my-backend`, install pandas and click, and create a command called `my-backend` that runs the `main` function."

### `src/my_backend/` — Your modules

```
src/
  my_backend/
    __init__.py      # Marks this as a package
    cli.py           # Command-line interface
    process.py       # Processing logic
```

When someone installs your package, they can `import my_backend` from anywhere.

### `tests/` — Validation

```
tests/
  test_process.py    # Tests for processing logic
  test_cli.py        # Tests for the command line
```

You'll write these in Session 3. For now, know they go here.

```notes
Take 10–15 minutes here. Walk through each section:

setup.cfg: explain install_requires (the packages others need when they pip
  install you) and entry_points (the command-line tool they get).

src/my_backend/: explain that when you `pip install .`, this becomes an
  installed package, so `import my_backend` works from anywhere.

tests/: explain that tests document the behavior you promise, and you
  validate it with pytest in Session 3.

The structure is standard across Python projects. Any Python developer will
recognize it immediately. That familiarity is part of the goal.
```

---

## Generated package structure

Here's what cookiecutter creates:

```
my-backend-repo/              ← your new repo folder
├── .git/                      ← Git history
├── .gitignore                 ← Git ignore rules
├── src/
│   └── my_backend/            ← your package name
│       ├── __init__.py
│       ├── cli.py
│       └── process.py
├── tests/
│   ├── __init__.py
│   └── test_process.py
├── setup.cfg                  ← install dependencies, entry point, metadata
├── pyproject.toml             ← build backend
├── README.md                  ← documentation
└── requirements.txt           ← dev dependencies
```

This is the standard structure. Any Python developer will recognize it immediately.

```notes
Show this as a visual. It is a lot of folders for one first package, but the
structure is exactly what GitHub, PyPI, and mature projects use. Session 2
will explain the Release and install path; Session 3 will fill in the tests.
For now, students just need to see the shape.
```

---

## Git: clone, modify, push

Today you'll practice the simplest Git path:

```bash
git clone https://github.com/drweihungpan-lab/3R-cookiecutter.git temp
cd temp
# (run cookiecutter inside this folder to generate your package)
# (move the generated folder to become your Backend repo)
cd my-backend-repo
git init
git add .
git commit -m "Initial commit from cookiecutter"
git remote add origin git@github.com:your-github/3R-group-N-backend.git
git branch -M main
git push -u origin main
```

No branches, no pull requests, no reviews — just you, your code, and your repo. Session 2 adds the collaboration layer (branches, PRs, reviews).

```notes
Walk through this slowly. The key steps:
  1. Clone the template (a temporary folder)
  2. Run cookiecutter inside it to generate your Backend repo
  3. Initialize Git in the generated folder
  4. Commit and push to your new GitHub repo

You have already created a blank GitHub repo (in the hands-on setup); this is
the step where you push code to it.

Point out: no branches, no PR, no review. Just clone → generate → commit →
push. Session 2 will add the collaboration discipline.
```

---

## Hands-on: 70 minutes

You will:

1. Create a new GitHub repository called `3R-group-N-backend` (or your chosen name). Make it empty and public.
2. Clone the cookiecutter template to your laptop.
3. Run cookiecutter to generate your package folder (answer the prompts with your group info).
4. Initialize Git in the generated folder, commit the template, and push to your new repo.
5. Verify the push succeeded and the repo is public on GitHub.

You'll have this Backend repo for the rest of the course. Session 2 will teach you how to collaborate on it with branches and pull requests.

**Setup time (10 min):** SSH key check, create the GitHub repo, clone the template.

**Generation and push (30 min):** Run cookiecutter, explore the generated files, commit, push.

**Verification and buffer (30 min):** Check that the repo is public and the files are there. Ask questions if stuck.

Use [the exercise](../exercises/session-1.md) if you need step-by-step guidance.

```notes
70 minutes of hands-on is a big block. Circulate constantly. Common
difficulties:

  - SSH key not added: `git@github.com` will refuse them. Check in Session 0
    notes if needed.
  - Cookiecutter not installed: `pip install cookiecutter` or use the template
    URL directly in `python -m cookiecutter`.
  - Pushing to wrong repo: they create a local folder, commit, but then push
    to the template repo instead of their own. Check the git remote.
  - Generated folder in wrong place: they unzip or generate inside the temp
    folder and can't find it. Have them `find . -name 'src' -type d` to locate
    it.

The exercise walkthrough covers all of these in steps.
```

---

## Prepare for Session 2

Mandatory homework after Session 1 is approximately two hours, plus any unfinished practice. Details will be posted separately.

- Today's checkpoint: your Backend repo is created, public, and pushed with the generated template.
- Next session: you'll learn branches, pull requests, meaningful reviews, and how to tag a Release.
- You can then install a teammate's Release from git and verify it works.

The [syllabus](../../SYLLABUS.md) has the full course requirements. Next: collaborate and release.

```notes
Close by minute 168. Preview Session 2: now that you have a package structure,
you will learn how teammates collaborate on it safely (branches, reviews), how
to mark a version (Release), and how to install a teammate's Release to verify
it works.
```

