# Session 1 instructor notes: Environments and packages

Delivery and rehearsal notes for 20 statistics students in groups of three or four. The session opens with introductions and class rules, then teaches environment isolation, package structure, and cookiecutter, and ends with 70 minutes of hands-on practice creating and pushing each group's Backend repo. Use the [slides](../slides/session-1.md), [guided exercise](../exercises/session-1.md), [syllabus](../../SYLLABUS.md), and [course definitions](../../GLOSSARY.md).

---

## Prepare before class

- Collect the Session 0 check-ins first (see [Session 0 notes](session-0.md)). Every student needs Git, an SSH key connected to GitHub, Python 3.12, and a terminal; Windows students use WSL Ubuntu.
- Verify that you have:
  - The cookiecutter template at `https://github.com/drweihungpan-lab/3R-cookiecutter.git` (or your own fork of it).
  - The device-example folder in the Sandbox, with Stage 1 and Stage 2 READMEs readable.
  - A terminal ready to demonstrate: clone, cookiecutter, commit, push (you will not do this live; you will show the structure visually instead).
- Ask students to decide on their Backend repo names in advance (or they can choose during the hands-on). Group naming convention: `3R-group-N-backend` or similar.
- Rehearse once: clone the template, run cookiecutter with test inputs, see the generated structure. This helps you answer questions about the layout.

---

## 170-minute run sheet

Slide titles are the actual Markdown headings. Each slide face carries speaker notes that you should present from (Presenter View or notes pane).

| Clock | Mode | Slides | Delivery |
| --- | --- | --- | --- |
| 0–10 | Opening | Welcome to 3R; Class rules | Introduce yourself. Walk through the 7 rules (hands-on, S0 prereq, mandatory homework with show-and-tell, unfinished continues, public repos, pass/fail final-only, AI encouraged). Check if anyone's setup is broken; offer help after. |
| 10–15 | Opening | Your bubble tea shop | Ask 4 students at random, one at a time. Do not steer toward the three Rs. Write 2–3 answers on the board; return to them in 2 slides. Keep to 5 minutes total. |
| 15–25 | Overview | How the five sessions build on each other | Show the visual stack. Point out that each session adds a layer, and the device example will climb the stack alongside. By Session 5 students see it containerized. |
| 25–35 | Device example | Why is Jupyter not enough? | Pause 20 seconds and ask students for answers. Collect 4–5 concerns on the board (different versions, missing packages, edited cells, out-of-order runs, no history). Then synthesize into the three needs: isolation, package structure, version control. |
| 35–50 | Device example | Device example: Stages 1 to 2 | Show the stage READMEs from the Sandbox device-example folder. Demonstrate or walk through Stages 1 and 2. Name the tool that fixes each pain (Git, then venv + requirements) but do not teach it yet. |
| 50–60 | Break | | 10 minutes. |
| 60–75 | Explanation | A Python environment belongs to one project; Declared dependencies in requirements.txt | Show the venv creation command. Explain isolation and that activation chooses which Python, not installing. Show requirements.txt format. Explain pip freeze. |
| 75–90 | Explanation | Cookiecutter: a template for packages | Explain what cookiecutter does (generates project structure from a template). Show the template URL. Explain that you will run it in hands-on, not here. |
| 90–105 | Explanation | Inside the package template; Generated package structure | Show and explain: setup.cfg (metadata, entry point), src/ (modules), tests/. Display the folder tree as a visual. This is standard Python structure. |
| 105–120 | Explanation | Git: clone, modify, push | Show the commands: clone template → generate folder → commit → push. Emphasize: no branches, no PR, no review yet. That comes in Session 2. |
| 120–170 | Hands-on | Hands-on: 70 minutes | [Exercise](../exercises/session-1.md). Allocate: 10 min setup (GitHub repo creation, SSH check, template clone), 20 min generation (run cookiecutter, explore files), 25 min commit/push, 10 min verification and buffer. Circulate constantly. |

---

## Cues and expected observations

**Setup phase (first 10 min of hands-on):**
- Students create a blank GitHub repo. Remind them: empty, public, SSH clone URL.
- SSH key check: `ssh -T git@github.com` should print a success message. If it fails, the student's key is not added to GitHub; help them do that (or tell them to add it and come back).
- Template clone: `git clone https://github.com/drweihungpan-lab/3R-cookiecutter.git temp-template`.

**Generation phase (20 min):**
- Running cookiecutter: `python -m cookiecutter .` (interactive) or with `--no-input` and defaults.
- Students may ask: "What do I answer?" → Answer: "Use `my_backend` for the project name and your group name for author."
- Generated folder structure appears. Students may lose it; have them `find . -name 'src' -type d` to locate it.

**Commit/push phase (25 min):**
- In the generated folder: `git init`, `git add .`, `git commit`, `git remote add origin [SSH URL]`, `git branch -M main`, `git push -u origin main`.
- Common error: pushing to the template repo instead of their own. Check `git remote -v` to see where it's going.
- Pushing from wrong directory: they're still in temp-template. Have them `cd my_backend` first.

**Verification (10 min buffer):**
- Open GitHub and check: files there? Public? Commit shows the right files? Good.
- If push failed, diagnose: SSH? Remote URL? Branch name? Help one-on-one.

---

## Rehearsal checklist

- [ ] Cookiecutter template is available and cloneable.
- [ ] You have rehearsed: clone → cookiecutter generate → see the folder structure.
- [ ] Device-example Stages 1 and 2 READMEs are ready to show (Sandbox, device-example folder).
- [ ] You have a terminal and GitHub account ready if a student's SSH fails during hands-on.
- [ ] You have asked groups to choose Backend repo names in advance (or they will choose during hands-on).
- [ ] Your setup check (`ssh -T git@github.com`) works from your terminal.

---

## Session 1 to 2 transition

By the end of Session 1, every student should have:
- An isolated Python environment (venv) working.
- A Backend repo on GitHub with the cookiecutter-generated package.
- Pushed code to their repo (successfully).

In Session 2, they will learn how to:
- Create branches and open pull requests.
- Review each other's code meaningfully.
- Merge collaboratively.
- Tag a Release and install it.

The Backend repo they created today is their sandbox for all five sessions.

