"""CSV parsing and explicit rules for the supplied single-test example."""

import csv
import io
import logging
import math
import re
from datetime import date
from typing import Literal, NoReturn

from .errors import InvalidInputError
from .schemas import ValidationIssue

InputFile = Literal["participants", "laboratory"]
CsvRow = tuple[int, dict[str, str]]
PARTICIPANT_FIELDS = (
    "STUDYID DOMAIN USUBJID SUBJID AGE AGEU SEX ARM RFSTDTC RFENDTC"
).split()
LABORATORY_FIELDS = (
    "STUDYID DOMAIN USUBJID LBSEQ LBTESTCD LBTEST LBORRES LBORRESU "
    "LBSTRESN LBSTRESU VISIT LBDY LBDTC LBSTAT LBREASND"
).split()
VISITS = {"BASELINE": (1, 1), "DAY 15": (2, 15), "DAY 30": (3, 30), "DAY 90": (4, 90)}
logger = logging.getLogger(__name__)


def fail(file: InputFile, row: int | None, field: str | None, message: str) -> NoReturn:
    logger.warning("Rejected input file=%s row=%s field=%s: %s", file, row, field, message)
    raise InvalidInputError([ValidationIssue(file=file, row=row, field=field, message=message)])


def read_csv(contents: str, file: InputFile, required: list[str]) -> list[CsvRow]:
    if not isinstance(contents, str) or not contents.strip():
        fail(file, None, None, "Supply CSV text with a header and at least one data row.")
    if "\x00" in contents:
        fail(file, None, None, "CSV text must not contain NUL bytes.")
    reader = csv.reader(io.StringIO(contents.removeprefix("\ufeff"), newline=""), strict=True)
    try:
        headers = [cell.strip() for cell in next(reader, [])]
        if not headers or any(not header for header in headers):
            fail(file, 1, None, "Every column must have a nonempty header.")
        if len(headers) != len(set(headers)):
            fail(file, 1, None, "Column headers must be unique.")
        for field in required:
            if field not in headers:
                fail(file, 1, field, f"Add the required {field} column.")
        rows = []
        while True:
            line = reader.line_num + 1
            cells = next(reader, None)
            if cells is None:
                break
            if not cells:
                continue
            if len(cells) != len(headers):
                fail(file, line, None, "Row must contain exactly one cell per column header.")
            rows.append((line, dict(zip(headers, (cell.strip() for cell in cells)))))
    except csv.Error:
        fail(file, max(1, reader.line_num), None, "Malformed CSV; check quoting and field lengths.")
    if not rows:
        fail(file, None, None, "Supply at least one data row after the header.")
    return rows


def _required(row: dict[str, str], fields: list[str], file: InputFile, line: int) -> None:
    for field in fields:
        if not row[field]:
            fail(file, line, field, "This field must not be empty.")


def _expect(row: dict[str, str], field: str, expected: str, file: InputFile, line: int) -> None:
    if row[field] != expected:
        fail(file, line, field, f"Expected {expected}.")


def _integer(value: str, file: InputFile, line: int, field: str) -> int:
    if not re.fullmatch(r"[0-9]+", value):
        fail(file, line, field, "Expected a nonnegative integer.")
    try:
        return int(value)
    except ValueError:
        fail(file, line, field, "Integer is too long to represent.")


def _date(value: str, file: InputFile, line: int, field: str) -> date:
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        fail(file, line, field, "Expected an ISO date in YYYY-MM-DD form.")
    try:
        return date.fromisoformat(value)
    except ValueError:
        fail(file, line, field, "Expected a valid calendar date.")


def _number(value: str, file: InputFile, line: int, field: str) -> float:
    if not re.fullmatch(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", value):
        fail(file, line, field, "Expected a finite nonnegative number, or an empty missing result.")
    number = float(value)
    if not math.isfinite(number) or number < 0:
        fail(file, line, field, "Expected a finite nonnegative number.")
    return number


def validate_participants(rows: list[CsvRow]) -> dict[tuple[str, str], dict[str, str]]:
    participants = {}
    subject_keys = set()
    for line, row in rows:
        file = "participants"
        _required(row, PARTICIPANT_FIELDS, file, line)
        _expect(row, "DOMAIN", "DM", file, line)
        _expect(row, "AGEU", "YEARS", file, line)
        _integer(row["AGE"], file, line, "AGE")
        if row["SEX"] not in {"F", "M"}:
            fail(file, line, "SEX", "Expected F or M for this teaching example.")
        start = _date(row["RFSTDTC"], file, line, "RFSTDTC")
        end = _date(row["RFENDTC"], file, line, "RFENDTC")
        if end < start:
            fail(file, line, "RFENDTC", "End date must be on or after start date.")
        key = (row["STUDYID"], row["USUBJID"])
        if key in participants:
            fail(file, line, "USUBJID", "Duplicate participant key (STUDYID, USUBJID).")
        subject_key = (row["STUDYID"], row["SUBJID"])
        if subject_key in subject_keys:
            fail(file, line, "SUBJID", "Duplicate within-study subject key (STUDYID, SUBJID).")
        participants[key] = row
        subject_keys.add(subject_key)
    return participants


def validate_laboratory(rows: list[CsvRow], participants: dict[tuple[str, str], dict[str, str]]) -> None:
    record_keys = set()
    visit_keys = set()
    required = [field for field in LABORATORY_FIELDS
                if field not in {"LBORRES", "LBSTRESN", "LBSTAT", "LBREASND"}]
    for line, row in rows:
        file = "laboratory"
        _required(row, required, file, line)
        for field, expected in {"DOMAIN": "LB", "LBTESTCD": "LPA", "LBTEST": "Lipoprotein(a)",
                                "LBORRESU": "nmol/L", "LBSTRESU": "nmol/L"}.items():
            _expect(row, field, expected, file, line)
        key = (row["STUDYID"], row["USUBJID"])
        if key not in participants:
            fail(file, line, "USUBJID", "No participant matches this STUDYID and USUBJID; supply matching DM data.")
        sequence = _integer(row["LBSEQ"], file, line, "LBSEQ")
        day = _integer(row["LBDY"], file, line, "LBDY")
        if row["VISIT"] not in VISITS:
            fail(file, line, "VISIT", "Expected BASELINE, DAY 15, DAY 30 or DAY 90.")
        expected_sequence, expected_day = VISITS[row["VISIT"]]
        if sequence != expected_sequence:
            fail(file, line, "LBSEQ", "Sequence must match the scheduled visit (1, 2, 3, 4).")
        if day != expected_day:
            fail(file, line, "LBDY", "Study day must match the scheduled visit (1, 15, 30, 90).")
        record_key = (*key, sequence)
        if record_key in record_keys:
            fail(file, line, "LBSEQ", "Duplicate record key (STUDYID, USUBJID, LBSEQ).")
        visit_key = (*key, row["VISIT"])
        if visit_key in visit_keys:
            fail(file, line, "VISIT", "Duplicate visit key (STUDYID, USUBJID, VISIT).")
        record_keys.add(record_key)
        visit_keys.add(visit_key)
        observed_date = _date(row["LBDTC"], file, line, "LBDTC")
        participant = participants[key]
        start = date.fromisoformat(participant["RFSTDTC"])
        end = date.fromisoformat(participant["RFENDTC"])
        if (observed_date - start).days != day - 1 or not start <= observed_date <= end:
            fail(file, line, "LBDTC", "Date must match start date plus study day minus one, within participant dates.")
        if not row["LBORRES"] and not row["LBSTRESN"]:
            _expect(row, "LBSTAT", "NOT DONE", file, line)
            if not row["LBREASND"]:
                fail(file, line, "LBREASND", "Supply a reason for the missing result.")
        elif not row["LBORRES"] or not row["LBSTRESN"]:
            fail(file, line, "LBSTRESN", "Both result fields must be observed or both empty.")
        else:
            original = _number(row["LBORRES"], file, line, "LBORRES")
            standard = _number(row["LBSTRESN"], file, line, "LBSTRESN")
            if original != standard:
                fail(file, line, "LBSTRESN", "Original and standard results must agree; no unit conversion is supported.")
            if row["LBSTAT"] or row["LBREASND"]:
                fail(file, line, "LBSTAT", "Observed results require empty status and reason fields.")
