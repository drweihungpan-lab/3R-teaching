# Session 2: A package other people can install

Today's goal: data in, data out, from the command line, installable from GitHub.

- Generate your group's Backend repo from a template.
- Run it on the device data and check the answer.
- Tag a Release and install a teammate's.

---

## Our 170-minute agenda

- 00–10: Back at the bubble tea shop; device example Stages 3 to 4.
- 10–60: Explanation — modules, packages, cookiecutter, the command-line tool.
- 60–70: Break — 10 minutes.
- 70–130: Explanation — versions, Releases, installing from git, a first look at CI.
- 130–170: Hands-on — generate, run, push, tag, install.

Unfinished practice continues at home, in addition to the homework.

---

## Back at the bubble tea shop

**Your best staff member is sick today. Can someone else still make your tea?**

---

## Device example, Stage 3: dependencies declared

- Last time, Stage 2 crashed on a newer pandas. Stage 3 adds `requirements.txt`, and the crash is gone.
- It is still a notebook plus helper files. Run once, in order:

```text
DEV-C reaches the limit on 2026-01-16
```

- Rerun one cell that updates the data in place, and no error appears:

```text
DEV-C reaches the limit on 2026-01-04
```

- The answer depends on which cells ran, and in what order.
- Today's tool for this pain: functions with inputs and outputs, in a package.

---

## Device example, Stage 4: an installable package

- The analysis is now the package `device_limit`: `predict_limit_dates(counts)` takes a table and returns dates.
- Run from another folder, it fails: `FileNotFoundError: 'data/device_counts.csv'`. The data path is relative to where you stand.
- A harmless-looking cleanup (drop days with zero measurements) moves `DEV-C` from 2026-01-16 to 2026-01-06, with no error or warning.
- Nothing checks the answer. Next session's tool: tests.
- Files: the `device-example` folder of the [Sandbox](https://github.com/drweihungpan-lab/3R-sandbox).

---

## Data in, data out

Your package will read a CSV and write a CSV. Same input, same output, every time.

```text
device_counts.csv  →  device_limit  →  limits.csv
(device_id, date,      predict the       (device_id,
 daily_count)          limit date        limit_date)
```

- The Stage 4 code is already inside the package you generate.
- Your job today is the packaging: build it, share it, install it.

---

## Give each processing step a home

- A module is a Python file with a clear responsibility.
- A package groups modules that can be imported together.
- Keep exploration in a notebook; give repeated work a function.
- Pass inputs in and return results; avoid hidden notebook state.
- Here, `predict_limit_dates` takes a table and returns dates; the command-line tool is a thin layer around it.

---

## A cookiecutter turns answers into a repository

A cookiecutter is a template folder plus a few questions. You answer; it writes every file with your answers filled in.

```text
template + answers  →  new repository
(course_template)      (device_limit/, setup.cfg, tests/, CI ...)
```

- The same answers always produce the same files: repeatability for project setup.
- You can change the template itself later and regenerate. That is a homework idea.
- Install the tool with `python -m pip install cookiecutter` inside a virtual environment.

---

## The five questions

- `package_name`: the Python name and the command, for example `device_limit`.
- `module_name`: the file holding the processing, for example `model`.
- `repo_name`: must match your GitHub repository and the folder you cloned.
- `author` and `author_email`: written into the package metadata.

Press Enter to keep the default shown in brackets. Everything else comes from the template.

---

## What you get

```text
your-repo/
├── data/             device_counts.csv, expected_limits.sha256
├── src/device_limit/
│   ├── __init__.py   the version, 0.1.0
│   ├── model.py      the processing functions
│   └── scripts/      the command-line tool
├── tests/            unit and integration tests (CI runs them in Session 3)
├── setup.cfg         metadata, dependencies, entry point
├── Makefile          lint and test shortcuts
└── .github/workflows/github_actions.yml
```

---

## setup.cfg describes the package

- `[metadata]`: name, author, and the version read from `__init__.py`.
- `[options]`: Python version and `install_requires` (click, numpy, pandas).
- `[options.extras_require]`: optional extras such as `test`, installed with `pip install '.[test]'`.
- `[options.entry_points]`: a line that creates the `device_limit` command.

An editable install, `pip install -e '.[test]'`, lets you change code and rerun without reinstalling.

---

## The command-line tool

```bash
device_limit --input data/device_counts.csv --output limits.csv
```

- `--input` must be an existing CSV with columns `device_id`, `date`, `daily_count`.
- `--output` is the file to write: one `limit_date` per device.
- A missing column stops the run with a clear message; it does not write a half answer.
- `--version` prints the package version.

The tool uses the `click` library; the processing itself does not know about the command line.

---

## Logs tell you what ran

The package logs one line when it reads a file:

```text
26/10/2026 09:31:17 (from load_counts) INFO: Read 1095 rows from data/device_counts.csv
```

- Set `LOGLEVEL=DEBUG` to see more, or `WARNING` to see less.
- Logs go to the terminal; the result goes to the output file.
- Prefer logging over `print` so you can change the detail without editing code.

---

## Check the answer: the reference checksum

A checksum is a short fingerprint of a file. If two files have the same SHA-256, they are byte-for-byte identical.

```bash
shasum -a 256 limits.csv
```

Compare the result with the value in `data/expected_limits.sha256`. Your classmates' output must match too: that is repeatability, checked by a machine.

---

## A Release is a version someone else can pin

Three steps, always in this order:

- Change `__version__` in `src/<package>/__init__.py`, through a reviewed pull request.
- After it is merged, tag the merge commit: `git tag v0.1.0`.
- Push the tag: `git push origin v0.1.0` (or `git push --tags`).

The tag is now a fixed point. Anyone who installs `v0.1.0` gets exactly that code, even after `main` moves on.

---

## Install a Release from its git URL

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install "git+https://github.com/ORG/REPO.git@v0.1.0"
device_limit --input data.csv --output limits.csv
```

- `@v0.1.0` pins the tag; without it you get whatever `main` is today.
- Use a fresh virtual environment so leftovers cannot hide a problem.
- This works because your repository is public: no account or token is needed.

See [why we install from git](../../docs/adr/0002-distribute-by-git-tag-not-registry.md).

---

## What about PyPI?

PyPI is the public index behind a plain `pip install pandas`. Mature packages are published there.

- Uploads are permanent: a name and version can never be reused or removed cleanly.
- Immature student packages and name clashes would stay public.
- TestPyPI is a safe practice index, but it needs accounts, two-factor setup and publisher configuration.

In this course a tagged Release on GitHub gives the same lesson without the permanence. You would move to PyPI when a package is stable and has a good name.

---

## CI: a first look

Continuous integration (CI) runs automated checks on every push.

- Your repo ships `.github/workflows/github_actions.yml`.
- It installs the package and runs the formatting and lint checks, then the command on the sample data.
- A green check reports success for one commit; it does not prove every requirement.
- The test job is commented out with `#`. In Session 3 you remove the `#` and it starts running your tests.
- Later, a repository rule can require the check before merging.

---

## Demo: generate the repository

Create an empty public repository on GitHub, then:

```bash
git clone git@github.com:ORG/REPO.git
cd REPO
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install cookiecutter
cookiecutter -f git@github.com:drweihungpan-lab/devops-python-package-template.git --directory course_template -o ..
```

Answer the five questions. Use the same `REPO` for `repo_name`. The `-o ..` writes the files into your clone, one folder up from where you stand.

---

## Demo: install it and run it

The generated files are now in your clone. Install it with its test tools:

```bash
pip install -e '.[test]'
device_limit --input data/device_counts.csv --output limits.csv
cat limits.csv
shasum -a 256 limits.csv
```

Expect three rows, DEV-A to DEV-C, and a SHA-256 that equals `data/expected_limits.sha256`.

---

## Demo: pull request, merge, tag

```bash
git switch -c feature/generate-package
git add .
git commit -m "Generate package from course template"
git push -u origin feature/generate-package
```

Open the pull request, watch the check run, ask a teammate for a review, then merge on GitHub.

```bash
git switch main
git pull --ff-only origin main
git tag v0.1.0
git push origin v0.1.0
```

---

## Hands-on: 40 minutes

- 10 minutes: create the repository, generate it, install it, and check the checksum.
- 10 minutes: open the pull request, get a review, merge.
- 5 minutes: tag `v0.1.0` and push the tag.
- 15 minutes: install a teammate's Release into a fresh environment and confirm their output matches the reference checksum.

Use [the exercise](../exercises/session-2.md) when stuck. Your Backend repo is where your pull request and review count as final evidence.

---

## Checkpoint and next step

Today's checkpoint: each group has a public Backend repo with a tagged Release that someone else installed and ran, matching the reference checksum.

- Mandatory homework is approximately two hours; details will be posted separately.
- Next session: tests with pytest, and switching on the test job in CI.

See the [syllabus](../../SYLLABUS.md) for the full course plan.
