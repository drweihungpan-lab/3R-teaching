"""Public JSON schemas shared by Python callers and the HTTP service."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

Count = Annotated[int, Field(ge=0)]


class Schema(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)


class Counts(Schema):
    participants: Count
    records: Count
    observed: Count
    missing: Count


class Record(Schema):
    study_id: str
    participant_id: str
    subject_id: str
    age: Count
    sex: str
    arm: str
    sequence: int
    test_code: str
    test_name: str
    visit: str
    study_day: int
    date: str
    value: float | None
    unit: str
    status: str | None
    reason: str | None
    baseline: float | None = None
    change: float | None = None
    percent_change: float | None = None


class ArmSummary(Counts):
    study_id: str
    arm: str


class VisitSummary(Counts):
    study_id: str
    arm: str
    visit: str
    study_day: int
    mean: float | None
    unit: str


class ProcessResult(Schema):
    counts: Counts
    records: list[Record]
    arm_summaries: list[ArmSummary]
    visit_summaries: list[VisitSummary]


class ValidationIssue(Schema):
    file: Literal["participants", "laboratory"]
    row: int | None
    field: str | None
    message: str


class ErrorResponse(Schema):
    detail: list[ValidationIssue]
