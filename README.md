# Repeatability, Reproducibility, and Replicability

A practical course for statistics students on the engineering framework behind repeatable data processing: isolated environments, collaborative Git workflows, reusable Python packages, tests, continuous integration (CI), APIs, and containers.

The emphasis is on understanding how the parts connect and practicing the workflow. Model complexity and UI design are not the focus. One running example, the device example, supports every session.

This repository holds course materials only. The course uses four repositories; the [syllabus](SYLLABUS.md#course-overview) lists their roles.

## Start here

- [Session 0](docs/session-0.md): required self-paced setup (GitHub account, terminal, SSH) before Session 1.
- [Syllabus](SYLLABUS.md): audience, workload, learning outcomes, five sessions, homework, and assessment. This is the single source for course facts.
- [Glossary](GLOSSARY.md): the course-specific meanings of the three Rs, the device example, and the repository terms.
- [Course materials](materials/README.md): slides, exercises, homework, instructor notes, surveys, and final checklist.
- [Course design](docs/course-design.md): teaching decisions not covered by the syllabus.
- [Collaboration guide](docs/collaboration.md): branches, pull requests, and peer review.
- [Decisions](docs/adr): WSL and SSH for all students; distributing packages by git tag.

## Repository guide

| Area | Where |
| --- | --- |
| Teaching | [Materials index](materials/README.md), [syllabus](SYLLABUS.md), [slide maintenance](materials/slides/README.md) |
| Session 2 rehearsal | [scripts/rehearse_session_2.sh](scripts/rehearse_session_2.sh): generate, tag, install, and compare the checksum on a clean machine |
| Slide builder | [scripts/build_slides.py](scripts/build_slides.py) |
