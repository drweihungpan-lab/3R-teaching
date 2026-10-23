# Session 1 instructor notes: environments, Git, and CI

Delivery and rehearsal notes for 20 statistics students in groups of three or four. The session opens with introductions and an open bubble tea question, then students inspect a complete application and make a small README change. Use the [slides](../slides/session-1.md), [guided exercise](../exercises/session-1.md), [syllabus](../../SYLLABUS.md), and [course definitions](../../GLOSSARY.md).

## Prepare before class

- Provide Python 3.12, Git, an editor, browser, internet/dependency access, individual GitHub accounts, and authenticated Git push access. Use the repository root for all commands. Follow [setup](../../docs/setup.md) and [template startup](../../docs/template.md#local-setup-and-startup); install both backend development and frontend dependencies. Windows equivalents need a separate rehearsal.
- Publish the completed framework on the template's default branch and enable **Template repository**, following [instructor template preparation](../../docs/template.md#instructor-prepare-the-template). Share its actual URL. An authoring PR into integration is not yet a student-ready default branch.
- Arrange one repository creator per group, accepted teammate invitations with write access, and instructor read access. Copy only the default branch into a new group repository with `main`; template updates do not synchronize. Check Actions permissions and protection availability for the chosen owner/plan. An administrator must configure [main protection](../../docs/template.md#administrator-protect-main-in-every-generated-repository) separately in every generated repository, after its first successful check.
- Use only the bundled synthetic [DM](../../data/synthetic/dm.csv) and [LB](../../data/synthetic/lb.csv); read their [provenance](../../data/synthetic/README.md). No patient data or neighboring repository is needed. Prepare two terminals in the same clone and environment, with ports 8000/8501 free.
- Preinstall dependencies for a clean demonstration clone and keep a checked baseline available if downloads are slow. Show `python --version` and `python -c 'import sys; print(sys.executable)'`: expect 3.12.x and that clone's `.venv`. Activation is needed in each terminal; it does not install packages. Version ranges are not a lockfile; `python -m pip freeze` records installed versions.
- Follow exercise §2's non-overwriting copy, `test -e .env || cp .env.example .env`. Inspect `git check-ignore .env .venv/` and `git ls-files -- .env .env.example`: local settings/environment ignored, only `.env.example` tracked. Check local `BACKEND_URL=http://127.0.0.1:8000`, `LOG_LEVEL=INFO`, and `MAX_UPLOAD_BYTES=5242880`. Exported variables override `.env`; restart services after edits. Never stage credentials.
- Optionally prepare an unused local conflict rehearsal clone with the slide drill's committed base and two branches; preserve the original clean baseline. Keep an earlier, clearly labeled CI run ready in case the live run is still pending. Never present an old run as checking the new commit.

## Provisional 180-minute run sheet

Slide titles below are the actual Markdown headings, not proposed slides. Exercise section numbers refer to the linked guided exercise.

### Flexible opening: about 35 minutes

The opening times are guides, not fixed limits. If the opening runs long, students finish unfinished guided practice at home, in addition to the two-hour homework.

- **Introduce yourself (about 5 minutes).** No slide.
- **Get to know students (about 10 minutes).** No slide. Ask random students informal questions: name, major, year, and their favorite bubble tea shop near campus.
- **Your bubble tea shop (about 12 minutes).** Read the scene, then ask students one at a time, at random, what they would need to take care of. Do not explain, steer answers toward the three Rs, or ask students to match them; leave space for imagination.
- **Can we trust published biomedical research? (about 5 minutes).** Present the two cited figures. Say aloud, without adding a slide, that in a 2016 *Nature* survey of 1,576 researchers across all sciences, more than half reported failing to reproduce their own experiments ([Baker 2016](https://doi.org/10.1038/533452a)). Freedman's figure is an estimate; present it as one.
- **What are we trying to preserve? (about 3 minutes).** Read the course definitions and the closing line, “Keep your bubble tea answers in mind.” Do not map students' answers to the definitions.

### Explanation, demonstration, and practice

| Clock | Mode | Actual slide titles | Delivery and activity reference |
| --- | --- | --- | --- |
| 35–45 | Explanation | Start with a working application; A Python environment belongs to one project | Trace Streamlit → FastAPI → `stat_core`; explain isolation versus pinned versions. Exercise §§2–3. |
| 45–51 | Explanation | Local configuration and shareable examples | Show ignored local settings versus tracked example; ignore rules do not remove tracked secrets. Exercise §2. |
| 51–58 | Explanation | Git records changes; GitHub hosts collaboration | Explain branch, staging, commit, push, draft PR, review, merge. Exercise §§4–5. |
| 58–62 | Explanation | CI reports; repository rules require | Read commit-specific checks versus separately configured merge rules. Exercise §5 and CI reference. |
| 62–65 | Explanation | A meaningful review helps the next reader; Your group owns the question and evidence; Prepare for the final presentation | Explain individual PR/review evidence and final-only assessment. Exercise §§5–6. |
| 65–69 | Demonstration | Demo: create your group's repository; Demo: prepare Python and check the baseline | Show template/collaborator steps, interpreter, settings and baseline checks in the preinstalled clone. Exercise §§1–2. |
| 69–73 | Demonstration | Demo: see the example work | Start services with the canonical commands; health response, upload selections, counts, tables/chart. Exercise §3. |
| 73–78 | Demonstration | Demo: one small README change; Demo: record and publish the change | Show both slides as one step: clean tree, branch, small diff, intended staging, descriptive commit and push. Exercise §4. |
| 78–85 | Demonstration | Demo: open a draft PR and inspect checks; A meaningful review helps the next reader | Use supplied PR template; show latest SHA/log and a specific comment plus author response. Exercise §5. |
| 85–100 | Break | Break, then 80 minutes of practice | Full 15-minute break. |
| 100–115 | Practice | Demo: create your group's repository | Exercise §1: create/clone group repository; verify remote and accepted access. |
| 115–130 | Practice | Demo: prepare Python and check the baseline | Exercise §2: each student checks interpreter, installs, ignore rules and baseline tests. |
| 130–145 | Practice | Demo: see the example work | Exercise §3: each student inspects uploads and explains counts/missingness. |
| 145–160 | Practice | Demo: one small README change; Demo: record and publish the change | Exercise §4: unique branch and author heading, candidate dataset/question, intended diff. |
| 160–175 | Practice | Demo: open a draft PR and inspect checks; A meaningful review helps the next reader | Exercise §5: draft PR, current CI result, specific peer feedback and response. |
| 175–180 | Practice | Use the same recovery on real PRs; Prepare for the final presentation | Exercise §6: inspect recovery, record evidence/stopping point, explain next steps. |

Totals: opening about 35, explanation 30, demonstration 20, break 15, practice 80 = 180 minutes. Follow the exercise's detailed 15/15/15/15/15/5 practice allocation; the slide “Break, then 80 minutes of practice” has a broader 45/30/5 outline. The controlled conflict demonstration (four slides) is optional: show it only if time permits, otherwise students inspect recovery in §6. Leave incomplete PR/CI work explicit rather than compressing recovery or claiming completion; students finish unfinished practice at home.

## Demo observations and questions

Use exercise §§2–5 and the [collaboration guide](../../docs/collaboration.md) for the setup and workflow commands. Baseline command: `python -m pytest backend/tests`; expect a pass, inspect warnings, and do not promise an invariant test count. The application is already complete.

| Observe or ask | Expected explanation/evidence |
| --- | --- |
| Does the app work before our README edit? | `/health` returns `{"status":"ok"}`. Streamlit receives DM as Participants and LB as Laboratory; **Process CSVs** shows 24 participants, 96 joined records, 95 observed, one missing, tables and a chart. Missing is unavailable, not zero. |
| Why two terminals? | Uvicorn and Streamlit are separate running processes using the same environment; Ctrl-C stops each. The frontend calls the API, which calls reusable processing. |
| Why not copy `.venv` or commit `.env`? | Recreate packages from declared dependencies; keep machine settings private, sharing only safe examples. Ignoring an already tracked file does not untrack it. |
| Why tests for a README PR? | Supplied CI runs on documentation PRs too. Backend tests check application behavior; manually inspect README wording, links and intended diff. Do not create artificial documentation tests. |
| What does green CI prove? | That named job passed for that SHA, not that the question is clear or every final requirement is met. Inspect **Checks → Backend tests → Run backend tests**, including install failures; see [CI](../../docs/ci.md). The workflow also includes **Docker output comparison**; container concepts are taught later. |
| Why can someone still merge without checks? | Reporting and enforcement are separate. Inspect the merge box after the administrator requires checks, approving review and resolved conversations; template copying does not copy protection. |
| What counts as meaningful review? | Comment on a specific behavior, test or clarity issue and explain why: “Distinguish your proposed dataset from the synthetic inputs so teammates know which files run now.” Author responds/updates; reviewer submits an explained review after **Ready for review**. Approval alone or “looks good” is insufficient. |
| Does seeing matching counts establish the Rs? | No. Repeatability compares same-condition runs; replicability compares the same process under slightly different conditions, here local versus Docker. Later compare records/counts exactly and calculated decimals with declared tolerances; see [output comparisons](../../docs/comparisons.md). |
| Must the topic or model be approved? | Groups choose their dataset/question independently; instructor discussion is available, approval not required. Modeling is optional and complexity earns no extra credit. FastAPI, Streamlit and Docker Compose remain required. |

## Controlled conflict and safe recovery

This drill is optional in the run sheet; use it only if time permits. Follow the four conflict/recovery slides and [Update and merge](../../docs/collaboration.md#update-and-merge). Use unused branch names and a new `conflict-demo.txt`, in the local rehearsal clone only. Start with `git status` clean and all other work committed; never practice against shared student `main`.

1. Seed `practice/conflict-base` with exactly `Session plan: draft`. Branch `practice/conflict-a`, change it to `Session plan: test first`, and commit. From the base, branch `practice/conflict-b`, change it to `Session plan: review first`, and commit. The slides contain the exact branch/add/commit commands.
2. On B, `git merge practice/conflict-a` must report a content conflict. Inspect `git status` and the file: `<<<<<<< HEAD` begins B's “review first”, `=======` separates A's “test first”, and `>>>>>>> practice/conflict-a` ends it. Explain both intentions before choosing text.
3. Demonstrate the escape route first: before committing a resolution, `git merge --abort` returns to the pre-merge B state; both branches' committed suggestions remain. Confirm with `git status`. This relies on starting clean: abort is not a backup for unrelated uncommitted edits. If unexpected work is present, stop, preserve it in a safe copy and ask for help; do not reset, force-push or overwrite it.
4. Retry the same merge. In the editor replace the entire marked block with `Session plan: test, then review`. Remove every marker, save, inspect the diff, run `git add conflict-demo.txt` and `git commit -m "Resolve plan: test then review"`. Then `git diff --check` and `python -m pytest backend/tests`; expect a clean resolved file and passing existing checks. Keep the branches local and return to `main` after the rehearsal.
5. On a real feature branch, commit work first, then `git fetch origin` and `git merge origin/main`. Resolve deliberately, rerun relevant checks and push that feature branch; obtain renewed review if needed. Confirm latest SHA, passing required checks, approval and resolved discussions before a GitHub merge.

## Common failures and recovery

| Symptom | Next action |
| --- | --- |
| Template button absent, invite/push denied | Recheck completed default branch, template setting, owner permissions, accepted invitations and Git authentication in [template setup](../../docs/template.md). Keep local commits; record missing hosted evidence. Do not create substitute participation. |
| Wrong Python, missing import, install fails | Inspect executable and root directory; activate the correct `.venv` in each terminal and follow canonical installs. Read the first install error; separate network/download problems from imports. Use prepared instructor baseline for demonstration while students recover. |
| `.env` tracked or settings ignored | Stop before staging; inspect `git ls-files` and exported variables. Preserve local settings, obtain help removing tracked secrets and rotating any exposed credentials; an ignore rule cannot remove history. Restart services after repair. |
| Port busy or UI cannot connect | Stop old processes with Ctrl-C; check API health first. If choosing a free API port, update `BACKEND_URL` and restart services; follow [frontend troubleshooting](../../docs/frontend.md). |
| Counts wrong or validation error | Reselect the bundled DM/LB in the correct upload fields; keep original data intact. Inspect the file/row/field message using the [API contract](../../docs/api.md). Never replace missing values with zero to make counts match. |
| No CI, pending CI, or failing CI | Check Actions permission, branch/SHA and first failing step. Pending is not passing; retain the run URL and exact limit. Correct the cause and push to the same branch; an old rerun cannot verify a new commit. A prepared run is historical evidence only. |
| Pull refuses or a merge conflicts | Inspect status and preserve work before following recovery above. Do not discard changes or force-push. A conflicted merge can be aborted before its resolution commit; keep both intentions. |
| Time runs out before review/merge | Keep the draft/open PR and record outstanding checks/feedback. Merging is not required in this practice. Students finish unfinished practice at home, in addition to the approximately two-hour mandatory Session 1 homework described in the syllabus. |

## Rehearsal checklist and evidence boundary

- [ ] Confirm completed default-branch template, actual URL, account permissions, Actions availability and administrator protection plan; do not infer settings from copied YAML.
- [ ] Rehearse clean setup, non-overwriting `.env` handling, both terminals, health and synthetic uploads; read baseline test output/warnings and check staged files exclude local settings/environment.
- [ ] Rehearse small README diff → descriptive commit → draft PR → latest-SHA checks → specific teammate feedback → author response → explained review. Record what remains pending.
- [ ] Rehearse the prepared conflict twice: abort preserves committed branches, then manual resolution preserves both intentions. Confirm no markers and a clean status; keep the drill local.
- [ ] Check the 180-minute plan with the actual slides/exercise; preserve the break. Keep current and historical run links clearly labeled if hosted checks take longer than the demo.
- [ ] Explain [individual evidence](../../docs/collaboration.md#preserve-individual-participation-evidence): each student authors at least one PR and meaningfully reviews at least one teammate's PR under their own account. Preserve authored PR/review permalinks, CI URLs and SHAs in the group README; copied template or instructor history does not count.
- [ ] State assessment accurately: pass/fail only at the final presentation; every engineering requirement must be met, including individual participation, environment/configuration hygiene, services/results, tests/CI, validation and both practical Rs. No weighted scores, separate submission, resubmission, reassessment or later retry. Statistical analysis correctness is not graded; tests still verify declared processing behavior. Today's checkpoint and homework are preparation.

Existing author evidence, not a new rehearsal by this document: the [guided exercise's author verification](../exercises/session-1.md#instructor-reference-and-recovery) records Python 3.12.1 baseline checks, API/Streamlit health and real HTTP multipart counts 24/96/95/1 on alternate ports. UI automation in prior course-authoring verification used Streamlit AppTest, not browser interaction. [Hosted run 38876609585](https://github.com/drweihungpan-lab/3R-teaching/actions/runs/38876609585), commit `c5fc92a37ec660492c7238f55f88b023a9200775`, separately passed **Backend tests** and **Docker output comparison**, including real image builds, Compose startup/health, frontend-to-backend service DNS/HTTP, multipart upload and local/Docker comparisons. This historical source-repository run does not verify a future group repository or this notes commit.

Local Docker and LibreOffice are unavailable; no local container execution or rendered deck inspection is claimed. Fresh student installations/downloads, template creation/invitations/protection, actual student PR/review participation, Windows commands and browser uploads remain delivery rehearsal items. This documentation change uses timing, content, command and local-link checks; it does not rerun unchanged backend tests or claim those unrehearsed steps occurred.
