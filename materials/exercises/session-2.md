# Session 2 guided practice: venv, a branch, and a reviewed pull request

Start in class (60 minutes) and finish at home (about 2 hours). Everything happens in **your own Backend repo** from Session 1. You will set up one virtual environment, install the package the way the Dockerfile does, write your own function on a branch, open a pull request, and review a classmate's pull request.

**Deadline:** your PR approved and merged, and your review done, **before Session 3 starts**.

The [Reference Backend repo](https://github.com/drweihungpan-lab/device_analysis_demo) shows each step first. Replace `device_analysis` below with your own `package_name`.

## Before you start

```bash
cd YOUR-BACKEND-REPO
git switch main
git pull
```

> Your repo is public. Any data you add must be **synthetic**: never real data, personal information, or secrets.

| When | Activity | Checkpoint |
| --- | --- | --- |
| In class | 1. One venv, install like the Dockerfile | The template command runs |
| In class | 2. Branch, your own function and CLI | Your command runs on the branch |
| In class or at home | 3. Commit, push, open a PR, post the link | Link posted in the check-in issue |
| At home | 4. Review a classmate's PR | Approve, line comment, 👍 |
| At home | 5. Merge after approval, pull `main` | Your command runs on `main` |

## 1. One repo, one venv

```bash
python -m venv .venv
source .venv/bin/activate
which python
```

`which python` must end in `.venv/bin/python`. If it shows a system path, the venv is not active. Check that `.venv/` is listed in `.gitignore`; never commit it.

Install the same way the template's `Dockerfile` does: first the pinned dependencies, then the package.

```bash
pip install -r requirements.txt
pip install .
device_analysis --message "hello"
```

You see three log lines (INFO, WARNING, ERROR) and `Hello world!: hello`. Put `LOGLEVEL=DEBUG` in front of the command to see the fourth.

`pip install .` **copies** your package into `.venv`. If you edit the code later, run `pip install .` again, or the command keeps running the old copy.

## 2. Branch: your own function and CLI

```bash
git switch -c feature/your-change
```

Write **one function of your own choice** in your package and expose it through the command-line tool. Ideas: the mean or maximum of a column in a CSV, a count of rows per group, a unit conversion. Keep it small.

- The function goes in your module (for example `device_analysis.py`); the click option goes in `scripts/…_script.py`.
- After **every** code change, run `pip install .` again (or `make install`), then your command. Without the reinstall, the venv still runs the old copy.
- If it needs a library such as pandas, add it to `install_requires` in `setup.cfg`. Then update the pinned versions with `pip install pip-tools` (once) and `make update-requirements`, and install again: `pip install -r requirements.txt` and `pip install .`. Never edit `requirements.txt` by hand.
- If it reads a file, use **synthetic** data: a small CSV you make up, or `../3R-device-example/data/device_counts.csv` without copying it into your repo.
- Run your command and check the output by hand.

The Reference Backend repo's example is `feature/device-summary`: `device_analysis --input ../3R-device-example/data/device_counts.csv` prints the mean `daily_count` per device.

## 3. Commit, push, open a PR, post the link

```bash
git status
git diff
git add src/ setup.cfg requirements.txt
git commit -m "Add <what your function does>"
git push -u origin feature/your-change
```

On GitHub, open a pull request from your branch into `main`. In the description write what the function does and the exact command to run it.

Then go to the [Sandbox issues](https://github.com/drweihungpan-lab/3R-sandbox/issues), open **Session 2 check-in**, and post one comment with your PR link. **Do not merge yet.**

## 4. Review a classmate's PR

In the check-in issue, find the **nearest earlier comment without a 👍** and review that PR. If you posted first, review the **last** link.

On their PR:

1. Open **Files changed**.
2. Click a line and leave **at least one specific comment**: a question, a suggestion, or what you checked. Not just "LGTM".
3. Select **Review changes → Approve → Submit review**.

Then add a 👍 to their comment in the check-in issue, so nobody else picks the same PR.

## 5. Merge after approval

Wait until your PR is **approved**. Reply to the review comments, push a fix if needed, then merge on GitHub. You, the author, merge; the reviewer does not.

```bash
git switch main
git pull
pip install .
device_analysis --help
```

Run your new command on `main` and check it works.

## Checkpoint

Before Session 3 starts:

- Your PR in your Backend repo is approved and merged, and your command runs on `main`.
- You approved one classmate's PR with at least one line comment, and gave a 👍 on their check-in comment.

From now on, authored PRs and reviews in your Backend repo count as evidence for the final presentation.
