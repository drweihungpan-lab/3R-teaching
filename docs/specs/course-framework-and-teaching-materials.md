# Three-R course framework and teaching materials

## Problem Statement

The instructor needs a coherent, teachable framework for a 15-hour course for 20 statistics students. Students already know Python functions, pandas, and basic regression, but need practice using engineering tools together: isolated environments, Git collaboration, packaging, tests, CI, APIs, and containers.

The repository currently contains course planning documentation and agent conventions. It does not yet provide the working example, template, slides, exercises, surveys, or final-presentation checklist needed to deliver the course. Teaching every component from scratch would distract from the intended workflow focus and exceed the available classroom time.

## Solution

Provide a complete working healthcare data-cleaning and processing example, a reusable group repository template, and aligned teaching materials for five three-hour sessions. Students inspect the supplied framework and practice small changes through feature branches, pull requests, peer review, automated checks, and container execution. Groups apply the framework to independently chosen datasets and questions.

Use the course-specific definitions of repeatability and replicability. Demonstrate repeatability through repeated execution under the same local conditions and replicability through matching local virtual-environment and Docker outputs for the same data and code. Treat reproducibility as a conceptual topic rather than a required independent simulation.

Deliver plain-English teaching materials, including editable PowerPoint decks with Markdown sources, guided exercises, instructor notes, mandatory homework, and pre/post-course surveys. Assess all required engineering evidence during the final presentation using pass/fail criteria.

## User Stories

1. As an instructor, I want one coherent framework across all five sessions, so that students can connect each tool to the workflow.
2. As a student, I want a complete working example, so that I can learn the framework without first building a UI or statistical model.
3. As a student, I want a small healthcare cleaning example, so that the data-processing behavior is understandable while I learn engineering concepts.
4. As an instructor, I want synthetic data with clear provenance, so that the example can be shared and its teaching purpose understood.
5. As a student, I want the course definitions of the three Rs stated clearly, so that terminology is consistent across materials and assessment.
6. As a student, I want prerequisites and setup instructions, so that I can prepare my Python environment and tools.
7. As a student, I want to use an isolated virtual environment, so that project dependencies are separated from global installations.
8. As a student, I want a shareable configuration example and ignored local settings, so that I can configure my application without committing local configuration or credentials.
9. As a group member, I want to generate our own repository from the template, so that our work and collaboration evidence have a shared home.
10. As a group member, I want to select our own dataset and statistical question, so that the project reflects our interests.
11. As a group member, I want to discuss our selected topic with the instructor without a mandatory approval gate, so that we retain ownership of the project.
12. As a student, I want to make small changes on feature branches, so that I can practice an understandable collaboration workflow.
13. As a student, I want descriptive commits and pull requests, so that teammates can understand the purpose of my changes.
14. As a student, I want to practice handling merge conflicts, so that I can collaborate when changes overlap.
15. As a student, I want to author at least one pull request, so that I demonstrate participation in the workflow.
16. As a student, I want to review at least one teammate's pull request with comments on behavior, tests, or clarity, so that I practice meaningful code review.
17. As an instructor, I want to inspect each group's PRs and reviews, so that participation and collaboration are visible.
18. As a student, I want to trace processing logic into reusable modules, so that I understand how exploratory scripts become maintainable code.
19. As a student, I want editable package installation and dependency metadata, so that I understand how a local package is used.
20. As a student, I want examples of type hints and logging, so that I can interpret interfaces and execution behavior.
21. As a student, I want a clear boundary between processing logic and the API, so that I can explain their separate responsibilities.
22. As a student, I want request and response schemas, so that I understand the contract between the frontend and backend.
23. As a student, I want examples of missing-value handling and invalid-input rejection, so that validation behavior is explicit.
24. As a student, I want tests for declared processing behavior, so that I can verify changes without relying on visual inspection alone.
25. As a student, I want fixtures and numerical comparison examples, so that I can write reusable tests with appropriate decimal tolerances.
26. As a student, I want to inspect controlled failing and passing tests, so that I can interpret failures and verify corrections.
27. As a student, I want automated checks on pull requests, so that I can connect local tests to GitHub Actions.
28. As a student, I want to understand the difference between reporting CI results and requiring checks before merge, so that I understand how branch protection works.
29. As a student, I want an existing Streamlit upload interface, so that I can follow a CSV through the application without focusing on interface design.
30. As a student, I want to trace an HTTP request from Streamlit to FastAPI and the processing package, so that I understand the complete processing path.
31. As a student, I want supplied backend and frontend container configurations, so that I can learn to inspect and modify the framework.
32. As a student, I want to launch both services with Docker Compose, so that I can demonstrate the application as a connected system.
33. As a student, I want to understand service names, internal networking, and readiness, so that I can diagnose connection and startup problems.
34. As a student, I want to rerun the same input under the same local conditions and compare results, so that I can demonstrate repeatability.
35. As a student, I want to compare local and Docker outputs for the same code and data, so that I can demonstrate replicability under the course definition.
36. As a student, I want exact comparisons for records and counts and stated tolerances for calculated decimals, so that agreement has an explicit meaning.
37. As a group member, I want flexibility to use cleaning, processing, summaries, visualization, or optional modeling, so that our engineering work fits our chosen question.
38. As a student, I want mandatory homework aligned with each of the first four sessions, so that I can practice independently before the final presentation.
39. As an instructor, I want provisional timings and instructor notes, so that I can balance explanation, demonstrations, and practice.
40. As an instructor, I want editable PowerPoint decks and Markdown sources, so that I can present the course and maintain its content through Git.
41. As an instructor, I want a pre-course survey about experience, confidence, and readiness, so that I can prepare for the cohort.
42. As an instructor, I want a post-course survey with matching questions and feedback prompts, so that I can evaluate learning and improve the course.
43. As a student, I want the final engineering checklist in advance, so that I know what evidence must be demonstrated.
44. As an instructor, I want a presentation schedule that fits the actual groups within three hours, so that each group can demonstrate its work.
45. As a student, I want assessment focused on engineering requirements rather than model complexity or statistical analysis correctness, so that the criteria match the course goals.
46. As an instructor, I want a pass/fail decision based on every mandatory requirement at the final presentation, so that assessment is consistent and final.

## Implementation Decisions

- **Source of truth:** follow the syllabus, agreed course design, and course glossary. The latest explicit decisions supersede earlier proposals, especially terminology, project flexibility, and the final-only assessment policy.
- **Audience and workload:** design for 20 statistics students with the agreed prerequisites, 15 contact hours, and approximately eight hours of mandatory homework across the first four sessions.
- **Grouping:** groups contain three or four students and each group has its own GitHub repository. Do not hard-code the number of groups; adapt the showcase schedule to enrollment and grouping.
- **Completed template:** supply functional processing logic, API, UI, tests, CI, and container configuration. Exercises inspect, modify, and verify a complete example rather than require construction from scratch or completion of missing functions.
- **Technology scope:** use Python 3.12 with virtual environments, standard Python packaging metadata, type hints, logging, FastAPI, Pydantic, pytest, GitHub Actions, Streamlit, Docker, and Docker Compose.
- **Processing boundary:** keep reusable processing functions independent of HTTP handling and UI presentation. Teach functions and modules without requiring unnecessary class abstractions.
- **Healthcare example:** reuse suitable synthetic participant and laboratory data from the clinical-data-teaching repository. Document provenance, retain synthetic-data labeling, and keep the demonstration limited to understandable cleaning, joining, validation, summaries, and a simple visualization.
- **Missingness and validation:** preserve unavailable observations as missing rather than zero. Make input rules, join behavior, expected types, and units explicit. Do not silently convert incompatible values or disguise invalid input as a successful result.
- **API contract:** support the demonstrated CSV-processing workflow with understandable request and response schemas and visible validation errors. Exact endpoint names and payload details belong to subsequent implementation specifications.
- **Interface:** supply CSV upload and visible processing results or charts. FastAPI, Streamlit, and Docker Compose remain required for group projects; interface polish and model complexity are not priorities.
- **Container configuration:** provide separate backend and frontend services, document the difference between local addresses and container service names, and explain service readiness. Multi-stage build optimization is optional.
- **Configuration hygiene:** provide a shareable configuration example and appropriate ignore rules. Keep local settings and secrets out of version control.
- **Git workflow:** use feature branches, descriptive commits, pull requests, meaningful peer review, and merges into main. Do not introduce a separate develop branch.
- **Individual participation:** every student authors at least one PR and meaningfully reviews at least one teammate's PR. Preserve inspectable evidence in the group repository.
- **CI:** provide automated backend checks for pull requests and the main branch. Explain how required checks differ from a workflow merely reporting its result; do not imply copied workflow files alone configure branch protection.
- **Output comparisons:** use the same data and code for both practical Rs. Compare cleaned records and counts exactly, and calculated decimal values within a declared numerical tolerance documented in tests. Choose and explain concrete tolerances in the relevant implementation task rather than inventing a universal value here.
- **Project flexibility:** groups choose their dataset and question independently. Discussion with the instructor is available without mandatory prior approval. Modeling is optional and does not earn extra credit through complexity.
- **Session sequence:** environment/Git/CI foundations; modules/packaging/types/logging; API/validation/testing/CI; UI/containers/networking/output comparisons; final showcase and engineering review.
- **Timing:** provisionally allocate each of Sessions 1–4 to 45 minutes of explanation, 30 minutes of demonstration, 90 minutes of guided practice, and a 15-minute break. The final showcase has its own schedule within three hours. Timing may be adjusted as materials develop.
- **Teaching deliverables:** provide English slides in editable PowerPoint format with Markdown sources, guided exercises, instructor notes, mandatory homework, and final-presentation guidance aligned to the same working example.
- **Surveys:** provide pre-course experience, confidence, and setup-readiness questions; repeat relevant confidence and understanding questions after the course and add feedback prompts. Surveys are for course evaluation and are not graded.
- **Assessment:** use pass/fail without weighted scores. Require environment/configuration hygiene, working service startup and communication, visible results, PRs and peer reviews including individual participation, passing local tests and CI, input-validation evidence, repeatability, and replicability.
- **Assessment boundary:** statistical analysis correctness is not graded. Engineering tests and comparisons must still demonstrate the processing behavior the group declares.
- **Finality:** inspect all assessment evidence at the final presentation. There is no separate submission, resubmission, or reassessment, including a later retry during the final session. Earlier homework and checkpoints support preparation, not separate assessed submissions.
- **Delivery workflow:** this issue is a specification, not authorization to implement the course immediately. Decompose and create implementation tasks one at a time through the later ticket workflow. Do not create child tasks or application code as part of publishing this spec.

## Testing Decisions

- The user declined the additional proposed acceptance scenario. Do not introduce a separate course-level end-to-end acceptance scenario or testing framework in this specification.
- Retain the testing requirements already present in the syllabus: processing unit tests, API response and validation tests, local pytest execution, CI checks, and output comparisons for repeatability and replicability.
- Good tests assert visible behavior against declared expectations: returned values, missingness, rejected invalid inputs, response contracts, and output agreement. Avoid asserting internal helper calls or the chosen code organization.
- Include focused cases for processing behavior and API validation, using fixtures and numerical comparisons where appropriate. The detailed cases follow the final processing and API contracts in later tasks.
- Demonstrate a controlled test failure and its correction in teaching activities, while keeping the distributed example and its default CI passing.
- Keep exact structural comparisons distinct from tolerance-based calculated-value comparisons. A missing value must not be treated as equivalent to zero.
- Tests verify engineering behavior, not the scientific validity of a group's research conclusions.
- There is no existing application test suite in this repository to use as prior art. The supplied course example will establish the initial testing conventions.
- Review teaching artifacts for consistency with the syllabus, glossary, workload, commands, and final-only assessment policy. This is preparation of the materials, not an extra student assessment requirement.

## Out of Scope

- Implementing the template or generating teaching deliverables during this specification step.
- Creating implementation tickets or a backlog during this specification step.
- Teaching Python functions, pandas, or basic regression from scratch.
- Requiring students to build an application from nothing or fill intentionally unfinished application functions.
- Requiring model training, prediction, advanced statistics, or complex model architecture.
- Grading statistical analysis correctness, scientific conclusions, interface polish, or model complexity.
- Mandatory topic approval, cross-group reproduction, new-data experiments, or independent simulations.
- A universal definition of the three Rs beyond this course's explicitly documented terminology.
- Weighted grading, separate assessment submissions, resubmission, or reassessment.
- Production hosting, cloud deployment, authentication systems, databases, or production MLOps infrastructure.
- Mandatory multi-stage Docker optimization or a separate develop-branch workflow.
- A new course-level end-to-end acceptance scenario or additional testing framework.

## Further Notes

- This specification synthesizes the existing syllabus and course design rather than reopening the course interview.
- The README and syllabus currently exist locally but have not yet been committed. Publishing the issue does not commit or push them.
- The repository's issue tracker is GitHub Issues and the configured implementation-ready label is `ready-for-agent`.
- The specification should be used as the parent reference for later tasks, created one at a time when requested.
- Implementation details such as dependency versions, API payloads, numerical tolerance values, and final group presentation slots should be resolved in the relevant task without changing the agreed scope.
