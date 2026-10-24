# WSL and SSH for all students

Status: accepted

## Decision

1. **Windows students use WSL with Ubuntu 24.04 LTS for the whole course.** Every command in every session runs in the Ubuntu terminal. Mac students use the built-in Terminal. Linux students use their own terminal and do not need WSL. The course gives no PowerShell or Git Bash alternatives.
2. **GitHub access uses SSH everywhere** (`git@github.com:OWNER/REPO.git`). The course does not use HTTPS with personal access tokens.

Students set both up in [Session 0](../session-0.md), a self-paced step before Session 1.

## Why

Most students have never used a terminal. If three setups coexist (Mac Terminal, PowerShell, Git Bash), every exercise, slide and homework needs variants, and a failure cannot be diagnosed without first asking which setup the student has. With WSL, a Windows student types exactly the commands a Mac student types, and the materials, the instructor's demonstrations and later Docker work (Session 4, Docker Desktop's WSL backend) all describe one environment.

SSH asks the student for one setup, once. HTTPS requires creating and storing a personal access token, which expires, is easy to paste into the wrong place, and produces confusing authentication errors during the course. An SSH key is created once and then works without further prompts.

## Alternatives considered

| Alternative | Why not |
| --- | --- |
| PowerShell for Windows students | Different syntax for activation, paths and file copying; every command block needs a second version. |
| Git Bash for Windows students | Closer to Linux, but still not the same environment as Mac and Docker; path and Python behavior differ. |
| HTTPS with personal access tokens | Token creation, expiry and storage are a recurring source of failures for beginners. |

## Trade-offs accepted

- **WSL takes effort to install** and can fail, for example when virtualization is disabled on the computer. The Session 0 [troubleshooting section](../session-0.md#troubleshooting) covers this, and the check-in surfaces problems before class.
- **Some networks block SSH on port 22.** The fallback is SSH over port 443 through `ssh.github.com`, documented in the same troubleshooting section. Clone addresses stay `git@github.com:OWNER/REPO.git`.

In exchange the course has one command set and no token problems.

## Consequences

- Materials say "run in WSL" and use SSH clone URLs; they do not offer other paths.
- Changing either decision later would touch the setup docs and every session's materials, which is why it is recorded here.
