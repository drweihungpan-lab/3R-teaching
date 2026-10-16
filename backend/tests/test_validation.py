"""Reject bad CSVs and domain inputs through process_csv, with useful locations."""

import pytest

from stat_core import InvalidInputError, process_csv


def assert_invalid(inputs, file, row, field, message=None):
    with pytest.raises(InvalidInputError) as caught:
        process_csv(*inputs)
    assert len(caught.value.issues) == 1  # Declared first-error behavior.
    issue = caught.value.issues[0].model_dump()
    assert {key: issue[key] for key in ("file", "row", "field")} == {
        "file": file, "row": row, "field": field,
    }
    assert isinstance(issue["message"], str) and issue["message"].strip()
    if message:
        assert message in issue["message"]


@pytest.mark.parametrize("file,index,first_field", [
    ("participants", 0, "STUDYID"), ("laboratory", 1, "STUDYID"),
])
@pytest.mark.parametrize("case,row,field", [
    ("empty", None, None), ("whitespace", None, None), ("nul", None, None),
    ("header_only", None, None), ("blank_header", 1, None), ("duplicate_header", 1, None),
    ("missing_header", 1, "STUDYID"), ("too_few_cells", 2, None),
    ("too_many_cells", 2, None), ("unclosed_quote", 2, None),
    ("invalid_quote_tail", 2, None),
])
def test_invalid_csv_structure(tiny_csv, file, index, first_field, case, row, field):
    header, first_row, *_ = tiny_csv[index].splitlines()
    bad = {
        "empty": "", "whitespace": " \n\t", "nul": tiny_csv[index] + "\x00",
        "header_only": header + "\n\n", "blank_header": header + ",\n" + first_row + ",\n",
        "duplicate_header": header + f",{first_field}\n" + first_row + ",duplicate\n",
        "missing_header": header.replace(first_field, "UNRECOGNIZED", 1) + "\n" + first_row,
        "too_few_cells": header + "\nshort,row\n",
        "too_many_cells": header + "\n" + first_row + ",extra\n",
        "unclosed_quote": header + '\n"unfinished',
        "invalid_quote_tail": header + '\n"quoted"tail,rest\n',
    }[case]
    inputs = list(tiny_csv)
    inputs[index] = bad
    assert_invalid(inputs, file, row, field)


@pytest.mark.parametrize("field", [
    "STUDYID", "DOMAIN", "USUBJID", "SUBJID", "AGE", "AGEU", "SEX", "ARM", "RFSTDTC", "RFENDTC",
])
def test_required_participant_headers(tiny_rows, csv_text, field):
    dm, lb = tiny_rows
    for participant in dm:
        del participant[field]
    assert_invalid((csv_text(dm), csv_text(lb)), "participants", 1, field)


@pytest.mark.parametrize("field", [
    "STUDYID", "DOMAIN", "USUBJID", "LBSEQ", "LBTESTCD", "LBTEST", "LBORRES", "LBORRESU",
    "LBSTRESN", "LBSTRESU", "VISIT", "LBDY", "LBDTC", "LBSTAT", "LBREASND",
])
def test_required_laboratory_headers(tiny_rows, csv_text, field):
    dm, lb = tiny_rows
    for record in lb:
        del record[field]
    assert_invalid((csv_text(dm), csv_text(lb)), "laboratory", 1, field)


@pytest.mark.parametrize("field", [
    "STUDYID", "DOMAIN", "USUBJID", "SUBJID", "AGE", "AGEU", "SEX", "ARM", "RFSTDTC", "RFENDTC",
])
def test_required_participant_cells(tiny_rows, csv_text, field):
    dm, lb = tiny_rows
    dm[0][field] = " "
    assert_invalid((csv_text(dm), csv_text(lb)), "participants", 2, field)


@pytest.mark.parametrize("field", [
    "STUDYID", "DOMAIN", "USUBJID", "LBSEQ", "LBTESTCD", "LBTEST", "LBORRESU", "LBSTRESU",
    "VISIT", "LBDY", "LBDTC",
])
def test_required_laboratory_cells(tiny_rows, csv_text, field):
    dm, lb = tiny_rows
    lb[0][field] = " "
    assert_invalid((csv_text(dm), csv_text(lb)), "laboratory", 2, field)


@pytest.mark.parametrize("field,value", [
    ("DOMAIN", "LB"), ("AGEU", "MONTHS"), ("SEX", "X"),
    ("AGE", "40.5"), ("AGE", "-1"), ("AGE", "forty"), ("AGE", "NaN"),
    ("AGE", "1e2"), ("AGE", "inf"), ("AGE", "9" * 5000),
    ("RFSTDTC", "20260101"), ("RFSTDTC", "2026-02-30"),
    ("RFENDTC", "2025-12-31"), ("RFENDTC", "2026-13-01"),
])
def test_invalid_participant_values(tiny_rows, csv_text, field, value):
    dm, lb = tiny_rows
    dm[0][field] = value
    assert_invalid((csv_text(dm), csv_text(lb)), "participants", 2, field)


@pytest.mark.parametrize("field,value", [
    ("DOMAIN", "DM"), ("LBTESTCD", "LDL"), ("LBTEST", "Different test"),
    ("LBORRESU", "mg/dL"), ("LBSTRESU", "mg/dL"),
    ("LBSEQ", "1.0"), ("LBSEQ", "-1"), ("LBSEQ", "2"), ("LBSEQ", "9" * 5000),
    ("LBDY", "1.5"), ("LBDY", "-1"), ("LBDY", "0"), ("VISIT", "DAY 7"),
    ("LBDTC", "2026-02-30"), ("LBDTC", "20260101"), ("LBDTC", "2026-01-02"),
])
def test_invalid_laboratory_values(tiny_rows, csv_text, field, value):
    dm, lb = tiny_rows
    lb[0][field] = value
    assert_invalid((csv_text(dm), csv_text(lb)), "laboratory", 2, field)


@pytest.mark.parametrize("field", ["LBORRES", "LBSTRESN"])
@pytest.mark.parametrize("value", ["NaN", "nan", "inf", "-inf", "Infinity", "1e309", "-1", "ten", "1,000"])
def test_invalid_results_are_not_silently_missing_or_nonfinite(tiny_rows, csv_text, field, value):
    dm, lb = tiny_rows
    lb[0][field] = value
    assert_invalid((csv_text(dm), csv_text(lb)), "laboratory", 2, field)


@pytest.mark.parametrize("updates,field", [
    ({"LBORRES": ""}, "LBSTRESN"),
    ({"LBSTRESN": ""}, "LBSTRESN"),
    ({"LBORRES": "11"}, "LBSTRESN"),
    ({"LBSTAT": "NOT DONE"}, "LBSTAT"),
    ({"LBREASND": "Unexpected reason"}, "LBSTAT"),
    ({"LBORRES": "", "LBSTRESN": ""}, "LBSTAT"),
    ({"LBORRES": "", "LBSTRESN": "", "LBSTAT": "DONE", "LBREASND": "No specimen"}, "LBSTAT"),
    ({"LBORRES": "", "LBSTRESN": "", "LBSTAT": "NOT DONE"}, "LBREASND"),
])
def test_contradictory_result_and_missingness_fields(tiny_rows, csv_text, updates, field):
    dm, lb = tiny_rows
    lb[0].update(updates)
    assert_invalid((csv_text(dm), csv_text(lb)), "laboratory", 2, field)


@pytest.mark.parametrize("key", ["STUDYID", "USUBJID"])
def test_unknown_composite_participant_key(tiny_rows, csv_text, key):
    dm, lb = tiny_rows
    lb[0][key] = "UNKNOWN"
    assert_invalid((csv_text(dm), csv_text(lb)), "laboratory", 2, "USUBJID", "No participant matches")


@pytest.mark.parametrize("key", ["USUBJID", "SUBJID"])
def test_duplicate_participant_keys(tiny_rows, csv_text, key):
    dm, lb = tiny_rows
    dm[1][key] = dm[0][key]
    assert_invalid((csv_text(dm), csv_text(lb)), "participants", 3, key, "Duplicate")


def test_duplicate_laboratory_record_and_visit(tiny_rows, csv_text):
    dm, lb = tiny_rows
    lb.insert(1, dict(lb[0]))
    # The duplicate violates both unique keys; the API reports the first error.
    assert_invalid((csv_text(dm), csv_text(lb)), "laboratory", 3, "LBSEQ", "Duplicate record key")


def test_laboratory_date_must_be_inside_participant_interval(tiny_rows, csv_text):
    dm, lb = tiny_rows
    dm[0]["RFENDTC"] = "2026-01-10"
    assert_invalid((csv_text(dm), csv_text(lb)), "laboratory", 3, "LBDTC", "within participant dates")


def test_finite_inputs_with_overflowing_percent_change_are_rejected(tiny_rows, csv_text):
    dm, lb = tiny_rows
    lb[0].update(LBORRES="1e-308", LBSTRESN="1e-308")
    lb[1].update(LBORRES="1e308", LBSTRESN="1e308")
    assert_invalid((csv_text(dm), csv_text(lb)), "laboratory", 3, "LBSTRESN", "finite numeric range")
