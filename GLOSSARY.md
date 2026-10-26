# Repeatability, Reproducibility, and Replicability

The three principles use the following course-specific meanings. Terminology varies between disciplines; these definitions govern this course.

## Language

**Repeatability**:
Agreement between results from successive runs of the same process under the same conditions, using declared comparison criteria.
_Avoid_: Replicability or reproducibility for unchanged conditions.

**Reproducibility**:
Agreement between results under very different conditions, such as an independent simulation intended to reproduce the original result. This is the course convention, rather than a universal definition.
_Avoid_: Replicability for the independent simulation meaning used here.

**Replicability**:
Agreement between results from the same process under slightly different conditions, using declared comparison criteria.
_Avoid_: Reproducibility for small changes in execution conditions within this course.

## Teaching examples

**Device example**:
The running synthetic example of daily measurement counts for medical devices, used to predict when each device reaches its usage limit; it evolves through seven stages across the course.
_Avoid_: Time-series example, device demo

**Stage**:
One snapshot of the device example, each showing one engineering pain point that the next stage fixes.
_Avoid_: Version, step, level

## Course repositories

**Sandbox**:
The one class-wide public repository where all students practise Git, with `main` protected and each group working under its own branch prefix. It also holds the device example. Nothing in it counts as final-project evidence.
_Avoid_: Practice repo, demo repo

**Backend repo**:
A group's single repository, started in Session 1 and holding its processing package from Session 2 onward. Public, and containing only synthetic or non-sensitive data.
_Avoid_: Group repo, project repo

**Frontend repo**:
The one instructor-owned repository holding the CSV upload page. Groups run it from a pinned release and do not fork or edit it.
_Avoid_: UI repo

**Release**:
A version of a package fixed by a version tag, so anyone installing that tag gets identical code. Nothing is uploaded to a package registry.
_Avoid_: Deploy, publish
