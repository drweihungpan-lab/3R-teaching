# Create and run a group repository

Use this complete synthetic healthcare example as a starting point. Groups of
three or four choose their own dataset and question; prior topic approval is
not required. Modeling is optional. FastAPI, Streamlit, and Docker Compose remain
required. See the [syllabus](../SYLLABUS.md) and [collaboration guide](collaboration.md).

## Instructor: prepare the template

1. Confirm the completed framework is available on the source repository's default
   branch before inviting groups to copy it. An unmerged authoring PR is not included.
2. As a repository administrator, open **Settings → General** and select
   **Template repository**. Give students read access and share the repository URL.
3. Follow [GitHub's template instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository).
   These are instructions for the instructor; publishing this guide changes no settings.

## Students: create your group's own repository

1. One group member selects **Use this template → Create a new repository**.
   Choose the group's owner and name, and copy only the default branch; leave
   **Include all branches** unchecked. Ensure the new repository's default is `main`.
2. Invite all teammates with write access and the instructor with read access
   (including for a private repository). Confirm everyone can open it.
3. Clone the new group repository, then enter its directory. Replace `OWNER/GROUP`
   below with its actual owner and name:

```bash
git clone https://github.com/OWNER/GROUP.git
cd GROUP
```

The group owns this repository and opens its PRs there. Template creation copies
files into a new history; later template changes do not synchronize automatically.
See [GitHub's creation guide](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).

## Local setup and startup

Install Git and Python 3.12. From the new repository root, on macOS/Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e './backend[dev]'
python -m pip install -r frontend/requirements.txt
test -e .env || cp .env.example .env
python -m pytest backend/tests
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Copy `.env.example` only if `.env` does not already exist. Keep `.env` and `.venv`
out of commits. The local default is `BACKEND_URL=http://127.0.0.1:8000`; restart
services after configuration changes. PowerShell uses `py -3.12 -m venv .venv`,
`.venv\Scripts\Activate.ps1`, and `Copy-Item .env.example .env` instead.

Keep the API terminal running. In a second terminal at the repository root,
activate the same environment and run:

```bash
source .venv/bin/activate
python -m streamlit run frontend/app.py --server.address 127.0.0.1 --server.port 8501
```

Open <http://127.0.0.1:8000/health> (expect `{"status":"ok"}`) and
<http://127.0.0.1:8501>. Upload [dm.csv](../data/synthetic/dm.csv) as Participants
and [lb.csv](../data/synthetic/lb.csv) as Laboratory; select **Process CSVs**.
Expect 24 participants, 96 joined records, 95 observed, and one missing result.
See [backend setup](setup.md), [frontend](frontend.md), and [tests](testing.md).

For container startup, stop both local servers with Ctrl-C to free ports 8000/8501.
With a running Docker engine and Compose v2, use `docker compose up --build`.
The browser still uses port 8501; Compose sets `BACKEND_URL=http://backend:8000`
inside the frontend service. Follow [Compose readiness and shutdown](compose.md).

## Administrator: protect main in every generated repository

Copied [CI YAML](../.github/workflows/backend-tests.yml) reports results; required
checks and branch protection are repository settings and are not inherited.

1. In the new repository's **Actions** tab, confirm GitHub Actions is enabled and
   permitted to run the supplied workflow. Open the first feature-branch PR into
   `main` and wait for **Backend CI → Backend tests** to succeed there.
2. In **Settings → Branches → Add classic branch protection rule**, target `main`.
   Require a pull request before merging, at least one approving teammate review,
   and conversation resolution. Dismiss stale approvals when new commits are pushed.
3. Enable **Require status checks to pass before merging**, select **Backend tests**
   from GitHub Actions, and require the branch to be up to date. Save the rule.
   If the check is absent, first get a successful run in this repository and retry.
4. Apply the rule to administrators too (**Do not allow bypassing the above settings**);
   leave force pushes and deletions disabled. Inspect the PR merge box to confirm
   missing approval or a pending/failed required check prevents merging.

An administrator must repeat this setup for each group repository. Protection
availability depends on the repository's visibility and GitHub plan; arrange a
supported course repository if unavailable. See [GitHub's protection guide](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
and [CI reporting versus requiring checks](ci.md#reporting-versus-requiring-checks).
