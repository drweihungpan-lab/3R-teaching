#!/usr/bin/env bash
# Rehearse the Session 2 student path on a clean machine.
#
#   generate a repo from the course cookiecutter -> lint checks pass -> the test
#   job is inert -> push and tag v0.1.0 -> pip install git+<url>@v0.1.0 into a fresh
#   venv -> run the command on the device CSV -> compare the SHA-256 with the
#   reference.
#
# Usage: scripts/rehearse_session_2.sh
#
# Environment:
#   TEMPLATE    cookiecutter source (default: the course template on GitHub)
#   TEMPLATE_REF  branch or tag to check out when TEMPLATE is a URL (default: main)
#   REMOTE_URL  a throwaway empty repository to push to and install from
#               (default: a local bare repository, so nothing is published)
#   PYTHON      Python 3.12 interpreter (default: python3.12)
#
# Needs: git, Python 3.12, and network access to install dependencies.

set -euo pipefail

TEMPLATE="${TEMPLATE:-git@github.com:drweihungpan-lab/devops-python-package-template.git}"
TEMPLATE_REF="${TEMPLATE_REF:-main}"
PYTHON="${PYTHON:-python3.12}"
REPO_NAME="rehearsal_repo"
TAG="v0.1.0"

fail() { echo "FAIL: $*" >&2; exit 1; }
step() { echo; echo "== $*"; }

command -v "$PYTHON" >/dev/null || fail "$PYTHON not found"
command -v git >/dev/null || fail "git not found"
"$PYTHON" -c 'import sys; sys.exit(sys.version_info[:2] != (3, 12))' \
  || fail "$PYTHON is not Python 3.12"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"

if [ -n "${REMOTE_URL:-}" ]; then
  REMOTE="$REMOTE_URL"
  INSTALL_URL="git+${REMOTE_URL}"
else
  git init -q --bare remote.git
  REMOTE="$WORK/remote.git"
  INSTALL_URL="git+file://$WORK/remote.git"
fi

step "Generate the Backend repo with cookiecutter"
"$PYTHON" -m venv tools
tools/bin/pip install -q cookiecutter 2>&1 | grep -v notice || true
checkout_args=()
case "$TEMPLATE" in
  http*|git@*) checkout_args=(--checkout "$TEMPLATE_REF") ;;
esac
tools/bin/cookiecutter --no-input ${checkout_args[@]+"${checkout_args[@]}"} "$TEMPLATE" \
  --directory course_template repo_name="$REPO_NAME" author="Rehearsal" \
  author_email="rehearsal@example.com" -o . >/dev/null \
  || fail "cookiecutter could not generate from $TEMPLATE"
cd "$REPO_NAME"

step "Install the package with its test tools and run the lint checks"
"$PYTHON" -m venv .venv
. .venv/bin/activate
pip install -q -e '.[test]' 2>&1 | grep -v notice || true
make test-formatting-linting >/dev/null || fail "the formatting/lint checks failed"
echo "lint checks passed"

step "Check the CI workflow: the lint job is active and the test job is inert"
"$WORK/tools/bin/python" - <<'PY' || fail "unexpected CI jobs"
import sys
import yaml

jobs = yaml.safe_load(open(".github/workflows/github_actions.yml"))["jobs"]
if list(jobs) != ["test-formatting-linting"]:
    sys.exit(f"active jobs are {list(jobs)}, expected only test-formatting-linting")
print("active jobs:", list(jobs))
PY

step "Run the command on the device CSV and compare the checksum"
device_limit --input data/device_counts.csv --output limits.csv >/dev/null
actual="$(shasum -a 256 limits.csv | cut -d' ' -f1)"
expected="$(cut -d' ' -f1 data/expected_limits.sha256)"
[ "$actual" = "$expected" ] || fail "checksum $actual does not equal reference $expected"
echo "checksum matches the reference"

step "Push to a throwaway remote and tag $TAG"
git init -q -b main . 2>/dev/null || true
git remote add origin "$REMOTE"
git add .
git -c user.name=Rehearsal -c user.email=rehearsal@example.com \
  commit -q -m "Generate package from course template"
git push -q origin HEAD:refs/heads/main
git tag "$TAG"
git push -q origin "$TAG"

step "Install the Release from its git URL into a fresh environment"
deactivate
cd "$WORK"
"$PYTHON" -m venv fresh
fresh/bin/pip install -q "$INSTALL_URL@$TAG" 2>&1 | grep -v notice || true
fresh/bin/device_limit --version | grep -q "0.1.0" || fail "installed version is not 0.1.0"
fresh/bin/device_limit --input "$REPO_NAME/data/device_counts.csv" --output installed.csv >/dev/null
installed="$(shasum -a 256 installed.csv | cut -d' ' -f1)"
[ "$installed" = "$expected" ] || fail "installed Release produced $installed, expected $expected"

echo
echo "PASS: generate -> lint -> tag -> install -> checksum all agree ($expected)"
