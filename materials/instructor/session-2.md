# Session 2 instructor notes: venv, Git and a reviewed pull request

Delivery and rehearsal notes. Students set up one virtual environment in their own Backend repo, see why an editable install matters, add their own function on a branch, open a pull request, and review a classmate's. Use the [slides](../slides/session-2.md), [guided exercise](../exercises/session-2.md) and the [glossary](../../GLOSSARY.md). Slide titles below are the Markdown headings.

## Prepare before class

- The Reference Backend repo is [device_analysis_demo](https://github.com/drweihungpan-lab/device_analysis_demo): package `device_analysis`, command `device_analysis --message`, `hello_world` logging at four levels. Its `main` must stay the template output.
- Clone `3R-device-example` next to it, so `../3R-device-example/data/device_counts.csv` exists (columns `device_id`, `date`, `daily_count`). Do not copy the CSV into the repo.
- Rehearse the `feature/device-summary` change on a local branch: replace `hello_world` with a mean `daily_count` per device, replace `--message` with `--input`, add `pandas` to `install_requires`. Expected means: DEV-A 174.00, DEV-B 209.94, DEV-C 254.77. Keep it as a fallback; do it live in class.
- Open a Sandbox issue titled **Session 2 check-in** and pin it. Students post their PR link there.
- Arrange a second account or a student to review your demo PR live.

## 170-minute run sheet

| Clock | Mode | Slides | Delivery |
| --- | --- | --- | --- |
| 0–5 | Opening | Show-and-Tell; Today's Plan | Short: two or three students. Write difficulties on the board. |
| 5–17 | Cookiecutter | Back at the Bubble Tea Shop; Why Not Just Copy a Repo?; Why Cookiecutter? ×3; Pitfall: Hyphens in Names | Finish what Session 1 started. Tie board difficulties to the slides. |
| 17–20 | Concept | Three Ways Results Should Agree | Course definitions from the glossary; the venv protects replicability. |
| 20–35 | venv | The Reference Backend Repo; One Repo, One venv; Why One per Repo?; Which Python Am I Using?; On `main`: The Template | Live in `device_analysis_demo`. Install with `pip install .` (no `-e`) on purpose. |
| 35–50 | pip + CLI | What Does `pip install .` Do?; You Already Have It: `make install`; `setup.cfg` or `requirements.txt`?; Update `requirements.txt`; Why a Command-Line Tool?; Where the Command Comes From; Logs Tell You What Ran | Show `ls .venv/bin`, `make help`, the CI workflow's `make install-test`, the Dockerfile `ENTRYPOINT`, and the `console_scripts` entry in `setup.cfg`. |
| 50–60 | Break | | 10 minutes. |
| 60–75 | Git | Git: Three Places; `git clone`; `git commit`; `git push`; `git pull` | Names for last week's commands; demo `pull` after a web edit. |
| 75–95 | Branches | Why Branches? ×2; How a Branch Works; Working With Branches; On the Branch: Mean per Device; Pitfall: The Old Code Still Runs; `pip install -e .` | Create `feature/device-summary` live, make the change, show the stale `Hello world`, then fix with `-e`. |
| 95–110 | Pull requests | From Branch to Pull Request; Code Review on GitHub; optional CI and conflict slides | Push, open the PR, review it live, author merges, `git pull`. Skip the optional slides if short of time. |
| 110–170 | Hands-on | Hands-On; Prepare for Session 3 | [Exercise](../exercises/session-2.md) §§1–4 in class; §§5–6 at home. |

## Check-in and review rules

- Each student posts one comment with their PR link in **Session 2 check-in**.
- Each student reviews the nearest earlier link without a 👍; the first poster reviews the last link.
- A review is **Approve plus at least one line comment**, then a 👍 on that check-in comment.
- The author merges only after approval. Deadline: before Session 3 starts.

## Cues and expected observations

- After `pip install .`, editing `device_analysis.py` changes nothing: the command still prints `Hello world!`. `--input` fails with `No such option`. After `pip install -e .` the edit shows and pandas is installed.
- Common failures: venv not activated (`which python` shows the system Python); a stale install; pushing to `main`; forgetting `git pull` after merge; a student merging before approval; two students reviewing the same PR (check the 👍s).

## Rehearsal checklist

- [ ] `device_analysis_demo` `main` installs with `pip install .` and runs `device_analysis --message hello`.
- [ ] The stale-output and `pip install -e .` sequence behaves as above.
- [ ] The mean-per-device command prints the three expected means.
- [ ] The Session 2 check-in issue exists and is pinned in the Sandbox.
