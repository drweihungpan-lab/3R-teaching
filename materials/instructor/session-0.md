# Session 0 instructor notes: setup and check-in

Session 0 is the self-paced setup that students complete at home before Session 1. It adds no classroom hours. Students follow the [Session 0 guide](../../docs/session-0.md) and post one comment on a pinned check-in issue in a separate public sandbox repository. The decision behind it is recorded in the [ADR](../../docs/adr/0001-wsl-and-ssh-for-all-students.md).

## Timeline

- **Several days before the deadline:** create the sandbox, pin the check-in issue and send the student message.
- **Deadline: 3 days before Session 1.** This leaves time to fix problems before class.
- **After the deadline:** read the check-ins, reply to failures, collect usernames and invite students to the sandbox for Session 1.

## Create the sandbox (once per term)

The sandbox is a public repository named `3R-sandbox`, separate from the authoring repository, so student activity never touches course materials or their issues. Create a new one each term; it can be deleted afterwards.

1. Create the public repository `3R-sandbox` under the course owner. Put the term in the description, for example `3R course sandbox, 2026 term`.
2. In **Settings → General → Features**, keep **Issues** on and turn off **Wiki**, **Projects** and **Discussions**.
3. Add no collaborators and no GitHub Actions workflows. With nobody else invited, only the owner can push.
4. Add a short README (welcome, one or two sentences on the purpose, links to the Session 0 guide, the sandbox rules and the check-in issue) and a `RULES.md` with the check-in rules. Anyone can read a public repository and comment on its issues without an invitation.
5. Open the issue below and pin it: on the issue page choose **Pin issue**. Pinned issues show at the top of the issue list.

Students get write access only in Session 1, after you collect usernames.

### Check-in issue text

Title: `Session 0 check-in`

```markdown
Welcome! Post **one comment** on this issue to show that your computer is ready for Session 1.

**Deadline: 3 days before Session 1** (the date is in your email).

## What to paste

Run these three commands in your terminal (Terminal on Mac, the Ubuntu window on Windows) and paste **all of their output** in a comment below:

    git --version
    python3.12 --version
    ssh -T git@github.com

Paste only the output of those three commands, nothing else.

## Never paste secrets

**Never paste a private key, a password or a token.** The three commands above never print one. This page is public.

## Example of a good comment

    git version 2.39.5 (Apple Git-154)
    Python 3.12.8
    Hi jane-chen! You've successfully authenticated, but GitHub does not provide shell access.

## Rules

- Comment on this issue; do not open a new issue.
- If you run the check again, edit your own comment instead of posting a new one.
- You do not push or change any files in Session 0.
- Stuck? Reply under your own comment and describe what you see.

Please read the [sandbox rules](https://github.com/drweihungpan-lab/3R-sandbox/blob/main/RULES.md) and the [Session 0 guide](https://github.com/drweihungpan-lab/3R-teaching/blob/main/docs/session-0.md).
```

## Message to students

```text
Subject: Required before Session 1: Session 0 setup (about 1 hour)

Hello everyone,

Before our first class, please set up your computer with Session 0. It is self-paced and takes about an hour; no experience is needed.

1. Follow the guide: https://github.com/drweihungpan-lab/3R-teaching/blob/main/docs/session-0.md
2. When you finish, post the output of three commands as a comment on the check-in issue: https://github.com/drweihungpan-lab/3R-sandbox/issues/1
3. Deadline: <DATE, 3 days before Session 1>

Never paste a private key, password or token anywhere. If you get stuck, reply under your own check-in comment and describe what you see. <Optional: I will also hold a drop-in help slot on DATE at TIME.>

See you in Session 1.
```

Replace the placeholders before sending, and confirm the check-in issue number if it is not `1`.

## Reading check-ins

A passing check-in has three lines:

| Line | Passing |
| --- | --- |
| `git --version` | `git version 2.x.x` (Mac may add `(Apple Git-...)`) |
| `python3.12 --version` | `Python 3.12.x` |
| `ssh -T git@github.com` | `Hi USERNAME! You've successfully authenticated, but GitHub does not provide shell access.` |

Scan the comments for these three lines. A missing comment, a missing line, `Permission denied (publickey)`, `command not found`, a Python version other than 3.12, or a timeout means the student needs a reply. Remove any comment that contains a private key, password or token right away, and tell the student to delete that key from GitHub (**Settings → SSH and GPG keys**) and create a new one.

## Replies to common failures

Each reply points to the matching entry in the guide's [troubleshooting section](../../docs/session-0.md#troubleshooting). Paste the short text, which matches the guide.

| Failure | Reply |
| --- | --- |
| WSL will not install, or virtualization is disabled | "Virtualization is probably off. Follow [WSL will not install](https://github.com/drweihungpan-lab/3R-teaching/blob/main/docs/session-0.md#wsl-will-not-install-or-virtualization-is-disabled) and reply with the exact error if it still fails." |
| `Permission denied (publickey)` | "GitHub does not recognize your key. Follow [Permission denied (publickey)](https://github.com/drweihungpan-lab/3R-teaching/blob/main/docs/session-0.md#permission-denied-publickey), then run `ssh -T git@github.com` again and edit your comment." |
| Connection timed out on port 22 | "Your network blocks SSH. Use the port-443 fix in [Port 22 is blocked](https://github.com/drweihungpan-lab/3R-teaching/blob/main/docs/session-0.md#port-22-is-blocked), then test again." |
| `python3.12: command not found` | "Follow [`python3.12` not found](https://github.com/drweihungpan-lab/3R-teaching/blob/main/docs/session-0.md#python312-not-found), then edit your comment with the new output." |
| Fingerprint question | "Compare the fingerprint as in [the fingerprint prompt](https://github.com/drweihungpan-lab/3R-teaching/blob/main/docs/session-0.md#the-first-connection-asks-are-you-sure-you-want-to-continue-connecting), then type `yes`." |
| Opened a new issue instead of commenting | Close it with a note pointing to the check-in issue. |

## Collect usernames and invite students

1. After the deadline, copy each comment author's GitHub username from the check-in issue; the username is also in the `Hi USERNAME!` line.
2. Compare with the class list and chase anyone missing.
3. Before Session 1, invite the usernames to `3R-sandbox` with write access (**Settings → Collaborators**), as the Session 1 plan requires. Do not invite anyone during Session 0, so nothing changes in the repository until Session 1.

## Optional drop-in help slot

Offer a 45-minute online or in-person slot a few days before the deadline for students who are stuck. Announce it in the student message. Students who cannot attend reply under their check-in comment instead.

## What Session 0 does not cover

Commit and push are taught in Session 1. Docker is installed before Session 4. The Session 1 sandbox exercise (conflicts, shared file) is a separate piece of work.
