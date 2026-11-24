# Session 1 guided practice: Create and push your Backend repo

## Goal

In this exercise, you'll create a GitHub repository for your group and use a **cookiecutter template** to generate a professional Python package structure. You'll commit that code and push it to GitHub. This becomes your **Backend repo** for the rest of the course — it holds the production code your team builds.

**Why cookiecutter?** It scaffolds a consistent, production-ready structure (source, tests, metadata, entry points) so your team starts from the same foundation. No copy-pasting boilerplate; just fill in your project name and author, and you're ready to code.

**Time estimate:** 65 minutes total (10 + 5 + 5 + 15 + 15 + 10).

---

## Before you start

**Prerequisites** (all from Session 0):
- Git installed and configured.
- SSH key set up and added to GitHub (you can verify this below).
- Python 3.12+ installed.
- A terminal: Mac Terminal, or the Ubuntu terminal in WSL on Windows.

**Your group needs:**
- A chosen Backend repo name (examples: `3R-group-3-backend`, `3R-eco-data`, `group-4-backend`).
- **One person** will create the GitHub repo first (others will be added as collaborators or push to it later).
- Decide: Will you add everyone's GitHub usernames as collaborators, or leave it public for now? (You'll set up proper permissions in Session 2.)

**Security reminder:** This repo is public. Never paste SSH keys, GitHub tokens, passwords, or personal data in any file. If you do by accident, treat it as a security incident and ask the instructor immediately.

---

## Step 1: Create the GitHub repo — 10 minutes

One person in your group does this; the others can prepare while they wait.

### Create an empty repository on GitHub

1. Go to [github.com](https://github.com) and log in.
2. Click the **+** icon in the top-right corner → **New repository**.
3. Fill in:
   - **Repository name:** Your chosen Backend repo name (e.g., `3R-group-3-backend`). **Important:** Use the exact name you'll give to cookiecutter as `project_name` (lowercase, no spaces).
   - **Description (optional):** Something like "Backend for Session 1 exercise" or leave blank.
   - **Visibility:** **Public** (you'll set permissions in Session 2 if needed).
   - **Initialize this repository with:** Leave all unchecked — do **NOT** add README, .gitignore, or license. We're starting empty.
4. Click **Create repository**.

### Copy the SSH clone URL

After creation, you'll see the repository page. Find the green **Code** button:
1. Click **Code** → select **SSH**.
2. Copy the SSH URL (it looks like `git@github.com:your-username/your-repo-name.git`).
3. **Share this URL** with your group — everyone will need it for the next step.

---

## Step 2: Verify your SSH key — 5 minutes

Everyone in your group should check this now (while waiting for the repo to be created if needed).

Open your terminal and run:

```bash
ssh -T git@github.com
```

**Expected output:**
```
Hi <your-github-username>! You've successfully authenticated with the SSH key named "your-key-name".
```

**If it fails:**
- See [Session 0 setup notes](../../docs/session-0.md) for adding an SSH key to GitHub.
- Or ask the instructor for help now.

---

## Step 3: Clone your GitHub repo — 5 minutes

Everyone does this. Use the SSH URL you copied earlier:

```bash
# Clone your GitHub repo (the empty one you created)
git clone git@github.com:your-github-username/your-repo-name.git

# Move into that folder
cd your-repo-name
```

You now have an empty repository on your laptop with Git already initialized (the `.git` folder is inside). You can verify:

```bash
ls -la
git remote -v
```

You should see:
- A hidden `.git/` folder.
- When you run `git remote -v`, it shows `origin` pointing to your GitHub repo.

---

## Step 4: Clone the cookiecutter template — 5 minutes

You're inside your repo folder. Clone the **devops-python-package-template** as a temporary helper:

```bash
# Clone the template to a temporary folder
git clone https://github.com/drweihungpan-lab/devops-python-package-template.git temp-template
```

This template is a professional-grade package scaffold with:
- A proper `src/` layout for the Python package.
- Testing infrastructure.
- CI/CD setup (GitHub Actions, etc.).
- Semantic versioning support via commit conventions.

---

## Step 5: Generate your Backend package using cookiecutter — 15 minutes

You're still in your repo folder. Run cookiecutter to generate your package **directly into your repo folder**:

```bash
python -m cookiecutter -f temp-template/package_template/ -o .
```

The `-f` flag tells cookiecutter to use the template at that path. The `-o .` tells it to output to the current directory.

### Answer the prompts

You'll be asked six questions. Here are typical answers:

```
[1/6] package_name (example): my_backend
[2/6] module_name (demo_module): my_backend
[3/6] repo_name (): 3R-group-3-backend
[4/6] author (Jane Doe): Group 3
[5/6] author_email (jane.doe@example.com): group-3@example.com
[6/6] Select project_type:
    1 - application
    2 - library
Choose from [1/2] (1): 2
```

**What each means:**
- **package_name:** Name for your Python package (lowercase, no spaces). Use `my_backend` or similar.
- **module_name:** The module that users will import. Usually the same as package_name.
- **repo_name:** The name of your GitHub repository (e.g., `3R-group-3-backend`). This should match your actual repo.
- **author:** Your group name (e.g., `Group 3`).
- **author_email:** A contact email (can be a placeholder like `group@example.com`).
- **project_type:** Choose `2` for library (the default). You're building a backend package for others to use, so "library" fits.

### Clean up

After cookiecutter finishes, remove the temporary template folder:

```bash
rm -rf temp-template
```

### What you'll get

Your repo folder now has the complete package structure at the root:

```
3R-group-3-backend/  (your repo folder)
├── .git/
├── src/
│   └── my_backend/
│       ├── __init__.py
│       ├── config.py
│       └── main.py
├── tests/
│   ├── conftest.py
│   └── test_main.py
├── pyproject.toml
├── README.md
├── Makefile
├── .github/
│   └── workflows/  (CI/CD configs)
├── .gitignore
├── .pre-commit-config.yaml
└── ...
```

### Explore the structure

Look at a few key files to understand the package:

1. **`pyproject.toml`** — the modern Python project config file. You'll see your package metadata here.
2. **`src/my_backend/`** — this is where your actual Python code lives.
3. **`tests/`** — where you'll add unit tests.
4. **`.github/workflows/`** — GitHub Actions for CI/CD (runs tests, etc. automatically).

Don't worry if these look complex; you'll use them more in later sessions. For now, just explore and notice the structure.

---

## Step 6: Commit and push to GitHub — 15 minutes

You're still in your repo folder (where `.git/` lives). Now stage the generated package files and push them.

### Stage and commit

```bash
git add .
git commit -m "Initial commit: cookiecutter-generated package"
```

**What this does:**
- `git add .` stages all the generated package files.
- `git commit -m "..."` creates a commit with the message in quotes.

**Check your work:**
```bash
git log --oneline
```

You should see one commit with your message.

### Verify the remote

Since you cloned your repo earlier, Git already knows where to push:

```bash
git remote -v
```

You should see:
```
origin  git@github.com:your-github-username/your-repo-name.git (fetch)
origin  git@github.com:your-github-username/your-repo-name.git (push)
```

### Check your current branch

```bash
git branch
```

You should see `* main` (the `*` means you're on that branch). GitHub defaults to `main`, so no renaming needed.

### Push to GitHub

```bash
git push
```

Since you cloned the repo, Git already knows to push to `origin main`. No `-u` flag needed.

**Expected output:**
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Writing objects: 100% (X/X), done.
...
To git@github.com:your-username/your-repo-name.git
   <empty>..abc1234  main -> main
```

---

## Step 7: Verify on GitHub — 10 minutes

### Check your repository on GitHub

1. Go to your GitHub repo (e.g., `github.com/your-username/your-repo-name`).
2. You should see:
   - The folder structure: `src/`, `tests/`, `.github/`, etc.
   - Your files: `pyproject.toml`, `README.md`, `Makefile`, `.pre-commit-config.yaml`, etc.
   - The commit message you pushed.

### Check the commit

Click on the commit hash (a short alphanumeric code near the top). You should see all the files you committed.

### Check the GitHub Actions CI/CD

Look for a **Actions** tab (top menu). The devops template includes CI/CD workflows that run automatically on push. You should see:
- A workflow run starting (it may still be in progress or completed).
- Tests running to verify your package setup.

This is the beginning of automated testing and CI/CD — more details in later sessions.

### Verify visibility

If you need to confirm the repo is public:
1. Click **Settings** (top-right of the repo page).
2. Scroll to "Danger Zone" and check the **Visibility** setting.
3. It should say "Public" or have a green indicator.

---

## Troubleshooting

### SSH key fails
**Error:** `Permission denied (publickey)` or similar.
- See [Session 0 setup notes](../../docs/session-0.md) to add your SSH key.
- Verify with `ssh -T git@github.com` before cloning or pushing.
- Ask the instructor if stuck.

### `cookiecutter` command not found
**Error:** `command not found: python -m cookiecutter`
- Install it: `pip install cookiecutter`
- Run the cookiecutter command again.

### "Project directory already exists"
**Error:** When running cookiecutter, it says a folder or file already exists.
- You likely ran cookiecutter twice in the same repo.
- **Solution:** Delete the generated subfolder and temp-template, then try again:
  ```bash
  rm -rf your-package-name temp-template
  git clone https://github.com/drweihungpan-lab/devops-python-package-template.git temp-template
  python -m cookiecutter -f temp-template/package_template/ -o .
  ```

### Cookiecutter prompt asks for `.` but I want to output elsewhere
**Error:** You're not sure what to answer for one of the prompts.
- **repo_name:** This should match your GitHub repo name (e.g., `3R-group-3-backend`).
- **package_name:** This is the Python package name (e.g., `my_backend`). It becomes the folder and import name.
- **module_name:** Usually the same as package_name.
- **project_type:** Choose `2` for library (the default).
- If you get stuck, re-read the prompt description above and ask the instructor.

### Files aren't in the repo root after moving
**Error:** After running `mv 3R-group-3-backend/* .`, files are still in a subfolder.
- Verify the move worked: `ls -la` should show `src/`, `tests/`, `setup.cfg`, etc.
- If still in a subfolder, the move didn't work. Try:
  ```bash
  ls 3R-group-3-backend/
  ```
  If files are there, manually move them:
  ```bash
  mv 3R-group-3-backend/src .
  mv 3R-group-3-backend/tests .
  mv 3R-group-3-backend/setup.cfg .
  mv 3R-group-3-backend/pyproject.toml .
  mv 3R-group-3-backend/README.md .
  mv 3R-group-3-backend/requirements.txt .
  mv 3R-group-3-backend/.gitignore .
  rmdir 3R-group-3-backend
  ```

### Nothing shows up on GitHub after push
- Refresh the GitHub page (browser cache can be slow).
- Check that push succeeded: `git log origin/main --oneline` should show your commit.
- If not, run `git push` again and refresh.

### "fatal: not a git repository"
**Error:** When running git commands, you get this error.
- You're in the wrong folder. Make sure you're in the cloned repo folder, not `temp-template`.
- Run: `pwd` to see where you are, then `cd your-repo-name` to get back to the repo.
- Verify: `git remote -v` should show your GitHub repo.

---

## Checkpoint: What you've done

After this exercise, you have:
- ✅ Created a GitHub repository with your group's chosen name.
- ✅ Cloned your empty repo to your laptop (Git already initialized).
- ✅ Used cookiecutter to generate a professional Python package structure.
- ✅ Moved the generated files into the repo root.
- ✅ Committed your code and pushed to GitHub.
- ✅ Verified the files are visible and public on GitHub.

Your Backend repo is now ready for the rest of the course. All group members can clone it to work on features together (more in Session 2).

---

## Next steps

**In Session 2, you will:**
- Clone your Backend repo to a fresh folder (simulating a team member joining).
- Create a new branch for a feature.
- Make a code change on that branch.
- Open a pull request.
- Have a teammate review and approve it.
- Merge the PR.
- Tag and release your first version.

**At home:**
- Finish any unfinished steps (should not take long).
- If you haven't cloned your Backend repo to a second machine or folder yet, do that to practice.
- Read the [Git glossary](../../GLOSSARY.md) to review terminology (repo, commit, branch, pull request, etc.).

---

## Check in

After you've completed this exercise, **go to the [3R-sandbox repository](https://github.com/drweihungpan-lab/3R-sandbox)**, find the "Issues" tab, and open the **Session 1** check-in issue. Reply with:
1. Your group name.
2. Your Backend repo name and link (e.g., `3R-group-3-backend: https://github.com/your-username/3R-group-3-backend`).
3. A quick note: "✅ Done" or "❓ Stuck on [step name]" if you need help.

This helps the instructor track progress and know who needs follow-up.

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
