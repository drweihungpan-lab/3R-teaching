# Session 1 guided practice: branches, pull requests, and a merge conflict

Spend about 40 minutes in your group of three or four, in the class [Sandbox](https://github.com/drweihungpan-lab/3R-sandbox). You will make a change on a branch, open a pull request (PR), review a teammate's PR, and resolve a merge conflict on purpose. Nothing in the Sandbox is graded and none of it counts as final-project evidence. Your group's own Backend repo, created in Session 2, is where authored PRs and reviews are counted.

## Before you start

You need Session 0 finished: Git, an SSH key connected to GitHub, Python 3.12, and a terminal (Mac Terminal, or the Ubuntu terminal in WSL on Windows). Know your group number `N`. Everything here is public: never paste a key, password, token, or personal data.

| Time | Activity | Checkpoint |
| --- | --- | --- |
| 0–10 min | Clone, branch, edit, push, open a PR | A PR from `group-N/...` is open |
| 10–20 min | Review a teammate's PR | A review with one specific comment |
| 20–35 min | The conflict drill | The conflict is resolved and merged |
| 35–40 min | Record what you did | A note of where you stopped |

## 1. Clone, branch, edit, push, open a PR — 10 minutes

```bash
git clone git@github.com:drweihungpan-lab/3R-sandbox.git
cd 3R-sandbox
git switch -c group-N/add-notes
```

Replace `N` with your group number. In an editor open `practice/shared-notes.md` and add one line under your group's heading. Then:

```bash
git status
git add practice/shared-notes.md
git commit -m "Add group N note"
git push -u origin group-N/add-notes
```

The push prints a link. Open it and create the pull request. You cannot push to `main`; if Git refuses, you are on `main`: switch to your branch.

## 2. Review a teammate's PR — 10 minutes

Open a teammate's PR and read **Files changed**. Submit a review with at least one specific comment about behavior or clarity, for example "Which line is yours, and did you keep the other group's line?". "Looks good" alone is not a review. The author replies. When satisfied, the reviewer approves and the author merges on GitHub.

```bash
git switch main
git pull --ff-only origin main
git branch -d group-N/add-notes
```

## 3. The conflict drill — 15 minutes

`practice/shared-notes.md` has a line under **Favourite tool this week**, currently `(undecided)`. Pair up with another group.

1. Each group creates a new branch from the latest `main` (`group-N/favourite-tool`) and changes that one line to a different tool.
2. Both groups push and open PRs. Merge the first PR.
3. The second PR now shows a conflict. Update your branch:

```bash
git fetch origin
git merge origin/main
git status
```

Open `practice/shared-notes.md`. `<<<<<<< HEAD` starts your line, `=======` separates the incoming one, `>>>>>>> origin/main` ends the block. Agree on one line, delete all three markers, then:

```bash
git add practice/shared-notes.md
git commit -m "Resolve favourite tool line"
git push
```

The PR is now mergeable. If you get stuck before committing, `git merge --abort` returns you to the state before the merge.

## 4. Record what you did — 5 minutes

Write down the links to your PR and your review, and where you stopped. Decide your Backend repo name and who creates it before Session 2.

## Checkpoint

You have opened a PR, reviewed a teammate's PR with a specific comment, and resolved a merge conflict. Finish anything unfinished at home, in addition to the homework. See the [glossary](../../GLOSSARY.md) for repository terms.
