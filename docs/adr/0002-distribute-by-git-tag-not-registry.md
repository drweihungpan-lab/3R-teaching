# Distribute student packages by git tag, not a package registry

Status: accepted

## Decision

Groups share their [backend repo](../../GLOSSARY.md#course-repositories) as a **release**: they bump the version, push a git tag such as `v0.1.0`, and others install it with `pip install git+https://github.com/OWNER/REPO.git@v0.1.0`. Nothing is uploaded to PyPI or TestPyPI. Group repositories are public, so the install needs no account or token.

## Why

Session 2's goal is a command-line package that someone else can install and run to get identical output. Version string in code, git tag and pinned install show that chain directly, and it needs no extra accounts. A registry would add account creation, two-factor setup and publisher configuration to a 40-minute hands-on block. It would also put immature student packages in a public index with permanent names and versions, where names collide and cannot be reused.

## Alternatives considered

| Alternative | Why not |
| --- | --- |
| PyPI | Uploads are permanent; students' unfinished packages and name clashes would stay public. |
| TestPyPI | Safe to practise on, but still needs accounts, 2FA and pending-publisher setup, and dependencies must come from a second index. |
| Private repos with `git+ssh://` | Fails wherever the SSH key is absent, including Docker builds and CI. |

## Consequences

- PyPI and TestPyPI appear as a slide: what you would do for a mature package.
- `python-semantic-release` stays in the template but dormant, with its job commented out; manual tagging is the Session 2 baseline. Switching it on later does not change how packages are installed.
- Compose in Session 4 builds the frontend from a git URL at a pinned tag, reusing the same idea.
- Group repositories must never hold real or sensitive data, since they are public.
