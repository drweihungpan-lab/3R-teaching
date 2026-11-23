# Session 1 guided practice: Create and push your Backend repo

Spend about 70 minutes in your group of three or four. You will create a GitHub repository, clone the cookiecutter template, generate your package structure, commit it, and push to your repository. This is your Backend repo for the rest of the course.

---

## Before you start

You need Session 0 finished: Git, an SSH key connected to GitHub, Python 3.12, and a terminal (Mac Terminal, or the Ubuntu terminal in WSL on Windows).

Your group needs:
- A chosen Backend repo name (for example, `3R-group-3-backend` or `3R-eco-data`).
- One person to create the GitHub repo (the others will push to it after).
- Everyone's GitHub username added to the repo as collaborators (or leave it public for now; you'll set permissions in Session 2).

Everything here is public: never paste a key, password, token, or personal data in any file.

---

## Setup — 10 minutes

### 1. One person: Create a GitHub repo

Go to GitHub and create a new, **empty** repository:
- **Name:** your chosen Backend repo name (for example, `3R-group-3-backend`).
- **Visibility:** Public.
- **Initialize:** Leave it empty. Do NOT add a README, .gitignore, or license yet.

Copy the SSH clone URL.

### 2. Everyone: Check SSH key

Verify your SSH key is working:

```bash
ssh -T git@github.com
```

You should see: `Hi <your-username>! You've successfully authenticated...`

If it fails, see the [Session 0 setup](../../docs/session-0.md) or ask the instructor.

---

## Clone the template — 5 minutes

```bash
# Clone the template to a temporary folder
git clone https://github.com/drweihungpan-lab/3R-cookiecutter.git temp-template
cd temp-template
```

You now have the cookiecutter template on your laptop.

---

## Generate your package — 20 minutes

Run cookiecutter to generate your Backend repo:

```bash
# Stay in the temp-template folder
python -m cookiecutter . --no-input \
  project_name="my_backend" \
  author="Group N"
```

Or run it interactively (you'll be prompted):

```bash
python -m cookiecutter .
```

You'll be asked:
- **project_name:** Name for your package (use `my_backend` or similar; keep it lowercase and no spaces).
- **author:** Your group name (for example, `Group 3`).

This generates a new folder with your package structure. For example, if you answered `my_backend`, you'll see:

```
my_backend/
├── src/
│   └── my_backend/
│       ├── __init__.py
│       ├── cli.py
│       └── process.py
├── tests/
│   └── test_process.py
├── setup.cfg
├── pyproject.toml
├── README.md
└── requirements.txt
```

Explore the files. Read `setup.cfg` and notice the `[metadata]` section and `[options.entry_points]`.

---

## Commit and push — 25 minutes

Navigate into your generated package folder:

```bash
cd my_backend
```

Initialize Git and commit:

```bash
git init
git add .
git commit -m "Initial commit: cookiecutter-generated package"
```

Add your GitHub repo as the remote (use the SSH URL you copied earlier):

```bash
git remote add origin git@github.com:your-github-username/3R-group-N-backend.git
```

Rename the branch to `main` (some systems create `master` by default):

```bash
git branch -M main
```

Push:

```bash
git push -u origin main
```

The `-u` flag sets this branch to track the remote, so future `git push` commands work without arguments.

---

## Verify — 10 minutes

1. **Check GitHub:** Open your repository on GitHub. You should see:
   - `src/my_backend/` with the Python code.
   - `tests/` with test files.
   - `setup.cfg` with your package metadata.
   - Other template files (`README.md`, `pyproject.toml`, etc.).

2. **Check the commit:** Click on the commit hash and verify the files are there.

3. **Verify public:** Click the repo Settings → scroll to "Danger Zone" if you need to change visibility to Public.

---

## Next steps

In Session 2, you will:

- Create a new branch for a feature.
- Make a change on that branch.
- Open a pull request.
- Have a teammate review it.
- Merge.
- Tag a Release and install it.

For now, congratulations: you have a Backend repo that's ready for the rest of the course.

---

## If you get stuck

**SSH key fails:** See Session 0 notes or ask the instructor to help you add it to GitHub.

**Cookiecutter not found:** Install it:
```bash
pip install cookiecutter
```

**Wrong folder pushed:** Check `git log --oneline` and `git remote -v` to see where you are and where it's pushing.

**Files not on GitHub:** Pull the latest on GitHub (refresh the page), or run `git push --all` to push all branches.

---

## Checkpoint

You have:
- Created a GitHub repository with your chosen name.
- Cloned the cookiecutter template.
- Generated your package structure.
- Committed and pushed to your Backend repo.
- Verified the files are public on GitHub.

Finish any unfinished steps at home, in addition to the homework. See the [glossary](../../GLOSSARY.md) for repository terms.

