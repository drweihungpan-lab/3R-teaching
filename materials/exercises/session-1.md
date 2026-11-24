# Session 1 guided practice: Create and push your Backend repo

## Goal

In this exercise, you'll create a GitHub repository for your group and use a **cookiecutter template** to generate a professional Python package structure. You'll commit that code and push it to GitHub. This becomes your **Backend repo** for the rest of the course — it holds the production code your team builds.

**Why cookiecutter?** It scaffolds a consistent, production-ready structure (source, tests, metadata, entry points) so your team starts from the same foundation. No copy-pasting boilerplate; just fill in your project name and author, and you're ready to code.

**Time estimate:** 70 minutes total (10 + 5 + 20 + 25 + 10).

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
   - **Repository name:** Your chosen Backend repo name (e.g., `3R-group-3-backend`).
   - **Description (optional):** Something like "Backend for Session 1 exercise" or leave blank.
   - **Visibility:** **Public** (you'll set permissions in Session 2 if needed).
   - **Initialize this repository with:** Leave all unchecked — do **NOT** add README, .gitignore, or license. We're starting empty.
4. Click **Create repository**.

### Copy the SSH clone URL

After creation, you'll see the repository page. Find the green **Code** button:
1. Click **Code** → select **SSH**.
2. Copy the SSH URL (it looks like `git@github.com:your-username/your-repo-name.git`).
3. **Share this URL** with your group — everyone will need it later.

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

## Step 3: Clone the cookiecutter template — 5 minutes

Everyone does this in their own terminal.

The **3R-cookiecutter** template is a blueprint for the package structure. We'll use it to generate your Backend repo.

```bash
# Clone the template to a temporary folder
git clone https://github.com/drweihungpan-lab/3R-cookiecutter.git temp-template

# Move into that folder
cd temp-template
```

You now have the cookiecutter template on your laptop. Let's explore it:

```bash
ls -la
```

You'll see files like `cookiecutter.json` (configuration), `{{cookiecutter.project_name}}/` (the template structure), and a `README.md` explaining what the template does.

---

## Step 4: Generate your Backend package — 20 minutes

You're still in `temp-template`. Run cookiecutter to generate your package:

### Option A: Interactive (recommended if you're new)

```bash
python -m cookiecutter .
```

You'll be prompted for:
- **project_name:** Name for your Python package (use lowercase, no spaces, e.g., `my_backend` or `eco_data`). This becomes the actual folder and module name.
- **author:** Your group name (e.g., `Group 3`).

### Option B: Non-interactive (faster if you know what you want)

```bash
python -m cookiecutter . --no-input \
  project_name="my_backend" \
  author="Group 3"
```

Replace `my_backend` and `Group 3` with your choices.

### What you'll get

After running cookiecutter, you'll see a **new folder** with your package name. For example, if you chose `my_backend`:

```
my_backend/
├── src/
│   └── my_backend/
│       ├── __init__.py        # Package initialization
│       ├── cli.py             # Command-line interface (empty for now)
│       └── process.py         # Processing logic (empty for now)
├── tests/
│   └── test_process.py        # Unit test (empty for now)
├── setup.cfg                  # Package metadata and configuration
├── pyproject.toml             # Python project config (modern standard)
├── README.md                  # Documentation template
├── requirements.txt           # Dependencies (empty for now)
└── .gitignore                 # Git ignore rules (pre-filled)
```

### Explore the structure

Look at two important files to understand the package:

1. **`setup.cfg`** — scroll to the `[metadata]` section. You'll see:
   ```
   name = my_backend
   author = Group 3
   version = 0.0.1
   ```
   This tells pip, GitHub, and other tools about your package.

2. **`setup.cfg` → `[options.entry_points]`** — this defines command-line commands your package exposes. For example, if you have an entry point named `cli`, users can run a command from the terminal.

Don't worry if these files look unfamiliar; you'll use them more in later sessions. For now, just notice they're there.

---

## Step 5: Commit and push to GitHub — 25 minutes

Now you've got the generated package. Time to push it to your GitHub repo.

### Move into your generated package folder

```bash
cd my_backend
```

(Replace `my_backend` with your actual package name.)

### Initialize Git

```bash
git init
```

This turns your folder into a Git repository (creates a hidden `.git` folder).

### Stage and commit

```bash
git add .
git commit -m "Initial commit: cookiecutter-generated package"
```

**What this does:**
- `git add .` stages all files in the folder.
- `git commit -m "..."` creates a commit with the message in quotes.

**Check your work:**
```bash
git log --oneline
```

You should see one commit with your message.

### Add your GitHub repo as the remote

This tells Git where to push (to your GitHub repo). Use the SSH URL you copied earlier:

```bash
git remote add origin git@github.com:your-github-username/your-repo-name.git
```

Replace:
- `your-github-username` with your actual GitHub username.
- `your-repo-name` with the GitHub repo name you created (e.g., `3R-group-3-backend`).

**Verify:**
```bash
git remote -v
```

You should see:
```
origin  git@github.com:your-github-username/your-repo-name.git (fetch)
origin  git@github.com:your-github-username/your-repo-name.git (push)
```

### Rename the branch to `main`

Some systems default to `master`; we use `main`:

```bash
git branch -M main
```

**Check:**
```bash
git branch
```

You should see `* main` (the `*` means you're on that branch).

### Push to GitHub

```bash
git push -u origin main
```

The `-u` flag sets this branch to track the remote, so future `git push` commands work without arguments.

**Expected output:**
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Writing objects: 100% (X/X), done.
...
To git@github.com:your-username/your-repo-name.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## Step 6: Verify on GitHub — 10 minutes

### Check your repository on GitHub

1. Go to your GitHub repo (e.g., `github.com/your-username/your-repo-name`).
2. You should see:
   - The folder structure: `src/`, `tests/`, etc.
   - Your files: `setup.cfg`, `pyproject.toml`, `README.md`, etc.
   - The commit message you pushed.

### Check the commit

Click on the commit hash (a short alphanumeric code near the top). You should see all the files you committed.

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
- Verify with `ssh -T git@github.com` before pushing.
- Ask the instructor if stuck.

### `cookiecutter` command not found
**Error:** `command not found: python -m cookiecutter`
- Install it: `pip install cookiecutter`
- Run again.

### Wrong folder pushed
**Error:** You pushed from the wrong directory, or you pushed an empty repo.
- Check where you are: `pwd`
- Check the remote: `git remote -v`
- Check the commit: `git log --oneline`
- If the repo on GitHub is empty or wrong, ask the instructor to help you delete it and try again.

### Nothing shows up on GitHub after push
- Refresh the GitHub page (browser cache can be slow).
- Check that push succeeded: `git log origin/main --oneline` should show your commit.
- If not, run `git push --all` and refresh again.

### "Cookiecutter already exists"
**Error:** When running cookiecutter, it says a file exists.
- You likely ran cookiecutter twice in the same `temp-template` folder.
- **Solution:** Use a fresh terminal, go back to your home folder, and start over with a new clone of `temp-template`.

---

## Checkpoint: What you've done

After this exercise, you have:
- ✅ Created a GitHub repository with your group's chosen name.
- ✅ Cloned the cookiecutter template to your laptop.
- ✅ Generated a professional Python package structure.
- ✅ Initialized Git, committed your code, and pushed to GitHub.
- ✅ Verified the files are visible and public on GitHub.

Your Backend repo is now ready for the rest of the course. All group members have access and can clone it to work on features together (more in Session 2).

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

