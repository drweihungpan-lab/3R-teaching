"""Input errors do not depend on HTTP or FastAPI."""

from .schemas import ValidationIssue


class InvalidInputError(ValueError):
    def __init__(self, issues: list[ValidationIssue]) -> None:
        self.issues = issues
        super().__init__("; ".join(issue.message for issue in issues))
