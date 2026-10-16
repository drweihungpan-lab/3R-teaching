"""Join synthetic DM/LB records and report descriptive summaries."""

import logging
import math
from collections import defaultdict
from statistics import mean
from typing import Any

from .schemas import ArmSummary, Counts, ProcessResult, Record, VisitSummary
from .validation import (
    LABORATORY_FIELDS,
    PARTICIPANT_FIELDS,
    fail,
    read_csv,
    validate_laboratory,
    validate_participants,
)

logger = logging.getLogger(__name__)


def _counts(participants: int, records: list[Record]) -> dict[str, int]:
    observed = sum(record.value is not None for record in records)
    return dict(participants=participants, records=len(records), observed=observed,
                missing=len(records) - observed)


def process_csv(participants_csv: str, laboratory_csv: str) -> dict[str, Any]:
    """Process CSV contents into the JSON-compatible ProcessResult contract."""
    participants = validate_participants(read_csv(participants_csv, "participants", PARTICIPANT_FIELDS))
    laboratory = read_csv(laboratory_csv, "laboratory", LABORATORY_FIELDS)
    validate_laboratory(laboratory, participants)
    records = []
    for _, row in laboratory:
        participant = participants[(row["STUDYID"], row["USUBJID"])]
        records.append(Record(
            study_id=row["STUDYID"], participant_id=row["USUBJID"],
            subject_id=participant["SUBJID"], age=int(participant["AGE"]),
            sex=participant["SEX"], arm=participant["ARM"], sequence=int(row["LBSEQ"]),
            test_code=row["LBTESTCD"], test_name=row["LBTEST"], visit=row["VISIT"],
            study_day=int(row["LBDY"]), date=row["LBDTC"],
            value=float(row["LBSTRESN"]) if row["LBSTRESN"] else None,
            unit=row["LBSTRESU"], status=row["LBSTAT"] or None,
            reason=row["LBREASND"] or None,
        ))
    records.sort(key=lambda r: (r.study_id, r.participant_id, r.study_day, r.sequence))
    source_lines = {(row["STUDYID"], row["USUBJID"], int(row["LBSEQ"])): line
                    for line, row in laboratory}
    baselines = {(r.study_id, r.participant_id): r.value for r in records if r.visit == "BASELINE"}
    for record in records:
        record.baseline = baselines.get((record.study_id, record.participant_id))
        if record.value is not None and record.baseline is not None:
            record.change = record.value - record.baseline
            if record.baseline != 0:
                record.percent_change = record.change / record.baseline * 100
            if any(value is not None and not math.isfinite(value)
                   for value in (record.change, record.percent_change)):
                fail("laboratory", source_lines[(record.study_id, record.participant_id, record.sequence)],
                     "LBSTRESN", "Change or percent change exceeds the finite numeric range.")

    arm_participants: dict[tuple[str, str], int] = defaultdict(int)
    arm_records: dict[tuple[str, str], list[Record]] = defaultdict(list)
    visit_records: dict[tuple[str, str, int, str], list[Record]] = defaultdict(list)
    for (study, _), participant in participants.items():
        arm_participants[(study, participant["ARM"])] += 1
    for record in records:
        arm_records[(record.study_id, record.arm)].append(record)
        visit_records[(record.study_id, record.arm, record.study_day, record.visit)].append(record)
    arms = [ArmSummary(study_id=study, arm=arm,
                       **_counts(arm_participants[(study, arm)], arm_records[(study, arm)]))
            for study, arm in sorted(arm_participants)]
    visits = []
    for (study, arm, day, visit), group in sorted(visit_records.items()):
        values = [r.value for r in group if r.value is not None]
        visits.append(VisitSummary(
            study_id=study, arm=arm, study_day=day, visit=visit, unit="nmol/L",
            mean=mean(values) if values else None,
            **_counts(len(group), group),
        ))
    result = ProcessResult(counts=Counts(**_counts(len(participants), records)),
                           records=records, arm_summaries=arms, visit_summaries=visits)
    logger.info("Processed participants=%d records=%d observed=%d missing=%d",
                result.counts.participants, result.counts.records,
                result.counts.observed, result.counts.missing)
    return result.model_dump(mode="json")
