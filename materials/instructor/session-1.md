# Session 1 instructor notes: environments and Git

Delivery and rehearsal notes for 20 statistics students in groups of three or four. The session opens with introductions and an open bubble tea question, then teaches environments, configuration and Git, and ends with 40 minutes of practice in the class [Sandbox](https://github.com/drweihungpan-lab/3R-sandbox). Use the [slides](../slides/session-1.md), [guided exercise](../exercises/session-1.md), [syllabus](../../SYLLABUS.md), and [course definitions](../../GLOSSARY.md). There is no CI in Session 1.

## Prepare before class

- Collect the Session 0 check-ins first (see [Session 0 notes](session-0.md)). Every student needs Git, an SSH key connected to GitHub, Python 3.12, and a terminal; Windows students use WSL Ubuntu, so rehearse once there.
- Sandbox: add all 20 students as collaborators with write access, and confirm `main` is protected (a pull request with one approval is required). Check that a test student cannot push to `main` but can push a `group-N/...` branch and open a PR.
- Assign group numbers 1–5 in advance and put them on the board. The `practice/shared-notes.md` file has headings for groups 1–5; add headings if there are more groups.
- Rehearse the conflict drill once with two accounts: both change the **Favourite tool this week** line on different branches, merge the first PR, and confirm the second shows a conflict.
- Keep a spare branch with the finished drill in case the live one goes wrong. Never show an old result as if it were the live one.

## 170-minute run sheet

Slide titles are the actual Markdown headings.

| Clock | Mode | Slides | Delivery |
| --- | --- | --- | --- |
| 0–10 | Opening | Our 170-minute route; Your bubble tea shop | Introduce yourself, then ask students one at a time, at random, what they would take care of. Do not steer answers toward the three Rs. |
| 10–20 | Opening | Can we trust published biomedical research?; What are we trying to preserve? | Present the two cited figures; say aloud that a 2016 *Nature* survey ([Baker 2016](https://doi.org/10.1038/533452a)) found over half of 1,576 researchers failed to reproduce their own experiments. Read the course definitions. |
| 20–30 | Device example | Device example: one analysis, seven stages; Stage 1; Stage 2 | Demonstrate Stages 1 → 2 using the stage READMEs in the Sandbox's `device-example` folder. Name the tool that fixes each pain; do not teach it yet. |
| 30–60 | Explanation | Four repositories, one job each; A Python environment belongs to one project; Local configuration and shareable examples; Your repositories are public | Explain the four repository roles with the glossary, isolation versus pinned versions, `.env` versus `.env.example`, and the public-repo rule. |
| 60–70 | Break | | 10 minutes. |
| 70–100 | Explanation | Git records changes; GitHub hosts collaboration; Branch rules protect main; A meaningful review helps the next reader | Branch, staging, commit, push, PR, review, merge. Preview that a repository rule can require automated checks; do not teach CI yet. |
| 100–130 | Demonstration | Demo: clone the Sandbox and branch; Demo: edit, commit, push; Demo: review, merge, update main | Perform the whole path live with your own group number. Show the push message link and the refused push to `main`. |
| 130–170 | Hands-on | Hands-on: 40 minutes; Controlled conflict slides; Your group owns the question; Prepare for the final presentation | [Exercise](../exercises/session-1.md) §§1–4. Show the two conflict slides at 150. Close by 168 with the next-session preview. |

## Cues and expected observations

- `git push -u origin group-N/add-notes` prints a "Create a pull request" link. A push to `main` is rejected by branch protection.
- A merge conflict appears on the second PR; students resolve it locally with `git merge origin/main`.
- Common failures: pushing from `main` by mistake; cloning with HTTPS (use the SSH URL from the ADR); an SSH key not added to the account; a wrong group number in the branch name (harmless).

## Rehearsal checklist

- [ ] A test student can open and merge a PR through the review rule.
- [ ] The conflict drill produces a conflict and resolves cleanly.
- [ ] Group numbers are on the board and in the shared notes.
- [ ] Windows students have used the WSL terminal at least once.
