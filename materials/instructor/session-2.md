# Session 2 instructor notes: a package other people can install

Delivery and rehearsal notes. Students generate their group's Backend repo from the course cookiecutter, run the command-line tool on the device data, merge through a reviewed PR, tag a Release, and install a teammate's Release from its git URL. Use the [slides](../slides/session-2.md), [guided exercise](../exercises/session-2.md), [ADR 0002](../../docs/adr/0002-distribute-by-git-tag-not-registry.md), and the [glossary](../../GLOSSARY.md). PyPI and TestPyPI appear only as a slide.

## Prepare before class

- The cookiecutter lives in `drweihungpan-lab/devops-python-package-template`, directory `course_template`. Confirm that the pull request adding it is merged to `main`, otherwise the clone command in the exercise fails. Check `cookiecutter -f git@github.com:drweihungpan-lab/devops-python-package-template.git --directory course_template -o ..` from a clean clone.
- The reference checksum is in `data/expected_limits.sha256` inside each generated repo. Run the whole path once yourself with [the rehearsal script](../../scripts/rehearse_session_2.sh).
- Each group needs one **empty, public** GitHub repository named as agreed in Session 1. Create them in the first minutes of hands-on if students have not.
- Make sure Actions are enabled for new repositories. The generated workflow runs on `push` and `pull_request` with Python 3.12; its test and release jobs are commented out on purpose.
- Have a pre-generated example Backend repo with a tagged Release available for demonstration and as a fallback for a group whose generation fails.

## 170-minute run sheet

| Clock | Mode | Slides | Delivery |
| --- | --- | --- | --- |
| 0–10 | Opening | Back at the bubble tea shop; Device example, Stage 3; Stage 4 | Ask the question, then show Stages 3 → 4 from the Sandbox's `device-example` folder. |
| 10–60 | Explanation | Data in, data out; Give each processing step a home; A cookiecutter turns answers into a repository; The five questions; What you get; setup.cfg describes the package; The command-line tool; Logs tell you what ran; Check the answer | Explain modules and packages, the template and its prompts, the layout, metadata and entry point, the tool's options, logging, and the checksum. |
| 60–70 | Break | | 10 minutes. |
| 70–100 | Explanation | A Release is a version someone else can pin; Install a Release from its git URL; What about PyPI? | Version → tag → pinned install. Say why it is not on PyPI: permanence, name clashes, accounts. |
| 100–110 | Explanation | CI: a first look | Very brief: automated checks on every push; the commented-out test job returns in Session 3. |
| 110–130 | Demonstration | Demo: generate the repository; Demo: install it and run it; Demo: pull request, merge, tag | Perform the full path live in front of the class. |
| 130–170 | Hands-on | Hands-on: 40 minutes; Checkpoint and next step | [Exercise](../exercises/session-2.md) §§1–4. |

## Cues and expected observations

- The generated repo shows three limit dates: DEV-A 2026-06-30, DEV-B 2026-04-01, DEV-C 2026-01-16. The output's SHA-256 equals the value in `data/expected_limits.sha256`.
- On first push, the PR shows one check, **test-formatting-linting**, which passes.
- `device_limit --version` prints `0.1.0` for the first Release.
- Common failures: running cookiecutter without `-o ..` (it nests the repo inside itself); a repository name that differs from `repo_name`; a private repository (the install then asks for credentials); a wrong or missing tag in the install URL; forgetting to push the tag; `shasum` not found (use `sha256sum` on Linux).

## Rehearsal checklist

- [ ] The cookiecutter PR is merged and the clone command works from a clean machine.
- [ ] Generate, install, run and compare the checksum on the demo machine.
- [ ] Push, tag, and install the Release from the git URL in a fresh environment.
- [ ] The lint check passes on the first PR.
