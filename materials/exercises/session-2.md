# Session 2 guided practice: generate, tag, and install a package

Spend about 40 minutes in your group of three or four. You will generate your group's **Backend repo** from the course cookiecutter, run the command-line tool on the device data, merge it through a reviewed pull request, tag a **Release**, and install a teammate's Release in a fresh environment. A module is a Python file; a package groups related modules so other code can install and import them.

This is preparation for the final presentation, not a separate submission. From now on, your authored PRs and reviews in the Backend repo count as evidence: every student must author at least one PR and review a teammate's.

## Before you start

Python 3.12, Git, an SSH key, and an editor from Session 0. One member creates an **empty, public** repository on GitHub (no README, no license) named as your group agreed. Everyone in the group uses that name as `REPO`. The data are synthetic; never put real data or secrets in a public repo.

| Time | Activity | Checkpoint |
| --- | --- | --- |
| 0–10 min | Clone, generate, install, run | The checksum equals the reference |
| 10–20 min | Pull request, review, merge | CI shows a green check |
| 20–25 min | Tag and push the Release | `v0.1.0` appears on GitHub |
| 25–40 min | Install a teammate's Release | Their output matches the reference |

## 1. Clone, generate, install, run — 10 minutes

```bash
git clone git@github.com:ORG/REPO.git
cd REPO
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install cookiecutter
cookiecutter -f git@github.com:drweihungpan-lab/devops-python-package-template.git --directory course_template -o ..
```

Answer the five questions. Use `REPO` for `repo_name`; keep the defaults for `package_name` and `module_name` unless your group agrees otherwise. The `-o ..` writes the files into your clone. Then:

```bash
pip install -e '.[test]'
device_limit --input data/device_counts.csv --output limits.csv
cat limits.csv
shasum -a 256 limits.csv
cat data/expected_limits.sha256
```

The two SHA-256 values must be equal. If they differ, stop and ask: do not edit the reference.

## 2. Pull request, review, merge — 10 minutes

```bash
git switch -c feature/generate-package
git add .
git commit -m "Generate package from course template"
git push -u origin feature/generate-package
```

Open the PR. Watch the check named **test-formatting-linting** run and turn green. A teammate reviews it with a specific comment (for example, what the `--input` option accepts), you reply, and the teammate approves. Merge on GitHub, then:

```bash
git switch main
git pull --ff-only origin main
```

## 3. Tag the Release — 5 minutes

The version is already `0.1.0` in `src/<package>/__init__.py`.

```bash
git tag v0.1.0
git push origin v0.1.0
```

Check that the tag appears under **Releases/Tags** on GitHub.

## 4. Install a teammate's Release — 15 minutes

Pick another member's repository. In a new folder, with a new environment:

```bash
mkdir try-release && cd try-release
python3.12 -m venv .venv
source .venv/bin/activate
pip install "git+https://github.com/ORG/THEIR-REPO.git@v0.1.0"
device_limit --version
curl -O https://raw.githubusercontent.com/ORG/THEIR-REPO/v0.1.0/data/device_counts.csv
device_limit --input device_counts.csv --output limits.csv
shasum -a 256 limits.csv
```

Their output must match the reference checksum. If installation fails, read the error: a wrong tag, a private repository, or a typo in the URL are the usual causes.

## Checkpoint

Your group has a public Backend repo with a tagged Release that someone else installed and ran, matching the reference checksum. Finish anything unfinished at home, in addition to the homework.

Optional, if you finish early: change `__version__` to `0.1.1` through a PR, merge, and tag `v0.1.1`. Notice that `@v0.1.0` still installs the old code.
