"""Behavior at the public CSV processing boundary, using independent oracles."""

import csv
import io

import pytest

from stat_core import ProcessResult, process_csv


def test_supplied_counts_and_arm_denominators(supplied_csv):
    # Literal expectations from data/synthetic/README.md, not output-derived counts.
    result = process_csv(*supplied_csv)
    assert result["counts"] == {"participants": 24, "records": 96, "observed": 95, "missing": 1}
    assert result["arm_summaries"] == [
        {"study_id": "EDU-LPA-001", "arm": "Investigational A", "participants": 12,
         "records": 48, "observed": 47, "missing": 1},
        {"study_id": "EDU-LPA-001", "arm": "Placebo", "participants": 12,
         "records": 48, "observed": 48, "missing": 0},
    ]
    assert set(result) == {"counts", "records", "arm_summaries", "visit_summaries"}
    assert ProcessResult.model_validate(result).model_dump(mode="json") == result


def test_worked_join_records_and_calculations(tiny_csv):
    result = process_csv(*tiny_csv)
    # Full literal raw records: the expected join does not call processing helpers.
    expected = [
        {"study_id": "TINY", "participant_id": "A", "subject_id": "001", "age": 40,
         "sex": "F", "arm": "Active", "sequence": 1, "test_code": "LPA",
         "test_name": "Lipoprotein(a)", "visit": "BASELINE", "study_day": 1,
         "date": "2026-01-01", "value": 10.0, "unit": "nmol/L", "status": None,
         "reason": None, "baseline": 10.0, "change": 0.0, "percent_change": 0.0},
        {"study_id": "TINY", "participant_id": "A", "subject_id": "001", "age": 40,
         "sex": "F", "arm": "Active", "sequence": 2, "test_code": "LPA",
         "test_name": "Lipoprotein(a)", "visit": "DAY 15", "study_day": 15,
         "date": "2026-01-15", "value": 5.0, "unit": "nmol/L", "status": None,
         "reason": None, "baseline": 10.0, "change": -5.0, "percent_change": -50.0},
        {"study_id": "TINY", "participant_id": "B", "subject_id": "002", "age": 50,
         "sex": "M", "arm": "Active", "sequence": 1, "test_code": "LPA",
         "test_name": "Lipoprotein(a)", "visit": "BASELINE", "study_day": 1,
         "date": "2026-01-01", "value": 20.0, "unit": "nmol/L", "status": None,
         "reason": None, "baseline": 20.0, "change": 0.0, "percent_change": 0.0},
        {"study_id": "TINY", "participant_id": "B", "subject_id": "002", "age": 50,
         "sex": "M", "arm": "Active", "sequence": 2, "test_code": "LPA",
         "test_name": "Lipoprotein(a)", "visit": "DAY 15", "study_day": 15,
         "date": "2026-01-15", "value": 15.0, "unit": "nmol/L", "status": None,
         "reason": None, "baseline": 20.0, "change": -5.0, "percent_change": -25.0},
    ]
    for actual, wanted in zip(result["records"], expected, strict=True):
        for field in ("change", "percent_change"):
            assert actual.pop(field) == pytest.approx(wanted.pop(field), rel=1e-9, abs=1e-9)
        assert actual == wanted


def test_supplied_raw_records_match_source_cells_exactly(supplied_csv):
    dm = list(csv.DictReader(io.StringIO(supplied_csv[0])))
    lb = list(csv.DictReader(io.StringIO(supplied_csv[1])))
    participants = {(row["STUDYID"], row["USUBJID"]): row for row in dm}
    source = {(row["STUDYID"], row["USUBJID"], int(row["LBSEQ"])): row for row in lb}
    result = process_csv(*supplied_csv)
    assert len(result["records"]) == 96
    assert [(r["study_id"], r["participant_id"], r["sequence"]) for r in result["records"]] == sorted(source)
    for record in result["records"]:
        row = source[(record["study_id"], record["participant_id"], record["sequence"])]
        participant = participants[(row["STUDYID"], row["USUBJID"])]
        raw = {key: value for key, value in record.items()
               if key not in {"baseline", "change", "percent_change"}}
        assert raw == {
            "study_id": row["STUDYID"], "participant_id": row["USUBJID"],
            "subject_id": participant["SUBJID"], "age": int(participant["AGE"]),
            "sex": participant["SEX"], "arm": participant["ARM"],
            "sequence": int(row["LBSEQ"]), "test_code": row["LBTESTCD"],
            "test_name": row["LBTEST"], "visit": row["VISIT"], "study_day": int(row["LBDY"]),
            "date": row["LBDTC"], "value": float(row["LBSTRESN"]) if row["LBSTRESN"] else None,
            "unit": row["LBSTRESU"], "status": row["LBSTAT"] or None,
            "reason": row["LBREASND"] or None,
        }


def test_supplied_missing_record_and_visit_counts(supplied_csv):
    result = process_csv(*supplied_csv)
    missing = [r for r in result["records"] if r["value"] is None]
    assert missing == [{
        "study_id": "EDU-LPA-001", "participant_id": "EDU-LPA-007", "subject_id": "007",
        "age": 57, "sex": "M", "arm": "Investigational A", "sequence": 3,
        "test_code": "LPA", "test_name": "Lipoprotein(a)", "visit": "DAY 30", "study_day": 30,
        "date": "2026-01-30", "value": None, "unit": "nmol/L", "status": "NOT DONE",
        "reason": "SPECIMEN NOT AVAILABLE", "baseline": 269.0, "change": None,
        "percent_change": None,
    }]
    assert [(s["arm"], s["visit"], s["participants"], s["records"], s["observed"], s["missing"])
            for s in result["visit_summaries"]] == [
        ("Investigational A", "BASELINE", 12, 12, 12, 0),
        ("Investigational A", "DAY 15", 12, 12, 12, 0),
        ("Investigational A", "DAY 30", 12, 12, 11, 1),
        ("Investigational A", "DAY 90", 12, 12, 12, 0),
        ("Placebo", "BASELINE", 12, 12, 12, 0),
        ("Placebo", "DAY 15", 12, 12, 12, 0),
        ("Placebo", "DAY 30", 12, 12, 12, 0),
        ("Placebo", "DAY 90", 12, 12, 12, 0),
    ]
    followup = result["records"][1]
    assert followup["baseline"] == 167.0
    assert followup["change"] == pytest.approx(-60.5, rel=1e-9, abs=1e-9)
    assert followup["percent_change"] == pytest.approx(-36.22754491017964, rel=1e-9, abs=1e-9)


@pytest.mark.parametrize("baseline_state", ["absent", "not_done", "zero"])
def test_unavailable_and_zero_baselines(tiny_rows, csv_text, baseline_state):
    dm, lb = tiny_rows
    if baseline_state == "absent":
        lb.pop(0)
    elif baseline_state == "not_done":
        lb[0].update(LBORRES="", LBSTRESN="", LBSTAT="NOT DONE", LBREASND="No specimen")
    else:
        lb[0].update(LBORRES="0", LBSTRESN="0")
    result = process_csv(csv_text(dm), csv_text(lb))
    records = [r for r in result["records"] if r["participant_id"] == "A"]
    if baseline_state == "zero":
        assert result["counts"] == {"participants": 3, "records": 4, "observed": 4, "missing": 0}
        assert [(r["value"], r["baseline"], r["percent_change"]) for r in records] == [
            (0.0, 0.0, None), (5.0, 0.0, None),
        ]
        assert [r["change"] for r in records] == pytest.approx([0.0, 5.0], rel=1e-9, abs=1e-9)
    else:
        assert [(r["baseline"], r["change"], r["percent_change"]) for r in records] == [
            (None, None, None)
        ] * len(records)
        assert [r["value"] for r in records] == ([5.0] if baseline_state == "absent" else [None, 5.0])
        assert result["counts"] == (
            {"participants": 3, "records": 3, "observed": 3, "missing": 0}
            if baseline_state == "absent" else
            {"participants": 3, "records": 4, "observed": 3, "missing": 1}
        )


@pytest.mark.parametrize("all_missing", [False, True])
def test_visit_means_use_only_observed_values(tiny_rows, csv_text, all_missing):
    dm, lb = tiny_rows
    for index in ([1, 3] if all_missing else [1]):
        lb[index].update(LBORRES="", LBSTRESN="", LBSTAT="NOT DONE", LBREASND="No specimen")
    result = process_csv(csv_text(dm), csv_text(lb))
    visit = result["visit_summaries"][1]
    if all_missing:
        assert visit.pop("mean") is None
    else:
        assert visit.pop("mean") == pytest.approx(15.0, rel=1e-9, abs=1e-9)
    assert visit == {
        "study_id": "TINY", "arm": "Active", "visit": "DAY 15", "study_day": 15,
        "participants": 2, "records": 2, "observed": 0 if all_missing else 1,
        "missing": 2 if all_missing else 1, "unit": "nmol/L",
    }
    assert result["records"][1]["baseline"] == 10.0
    assert result["records"][1]["change"] is None
    assert result["records"][1]["percent_change"] is None


def test_worked_summaries_include_dm_participants_without_lab_rows(tiny_csv):
    result = process_csv(*tiny_csv)
    assert result["counts"] == {"participants": 3, "records": 4, "observed": 4, "missing": 0}
    assert result["arm_summaries"] == [
        {"study_id": "TINY", "arm": "Active", "participants": 2,
         "records": 4, "observed": 4, "missing": 0},
        {"study_id": "TINY", "arm": "Control", "participants": 1,
         "records": 0, "observed": 0, "missing": 0},
    ]
    expected = [
        {"study_id": "TINY", "arm": "Active", "visit": "BASELINE", "study_day": 1,
         "participants": 2, "records": 2, "observed": 2, "missing": 0, "unit": "nmol/L"},
        {"study_id": "TINY", "arm": "Active", "visit": "DAY 15", "study_day": 15,
         "participants": 2, "records": 2, "observed": 2, "missing": 0, "unit": "nmol/L"},
    ]
    # (10 + 20)/2 = 15, (5 + 15)/2 = 10 nmol/L.
    for actual, wanted, mean in zip(result["visit_summaries"], expected, [15.0, 10.0], strict=True):
        assert actual.pop("mean") == pytest.approx(mean, rel=1e-9, abs=1e-9)
        assert actual == wanted


def test_composite_keys_separate_studies_and_their_baselines(tiny_rows, csv_text):
    dm, lb = tiny_rows
    # Both participant ID A and subject ID 001 are legal again in another study.
    dm.append(dict(dm[0], STUDYID="OTHER", AGE="70", ARM="Other arm"))
    lb.extend([
        dict(lb[0], STUDYID="OTHER", LBORRES="100", LBSTRESN="100"),
        dict(lb[1], STUDYID="OTHER", LBORRES="75", LBSTRESN="75"),
    ])
    result = process_csv(csv_text(dm), csv_text(lb))
    assert result["counts"] == {"participants": 4, "records": 6, "observed": 6, "missing": 0}
    assert [(r["study_id"], r["participant_id"], r["subject_id"], r["age"], r["arm"], r["baseline"])
            for r in result["records"]] == [
        ("OTHER", "A", "001", 70, "Other arm", 100.0),
        ("OTHER", "A", "001", 70, "Other arm", 100.0),
        ("TINY", "A", "001", 40, "Active", 10.0),
        ("TINY", "A", "001", 40, "Active", 10.0),
        ("TINY", "B", "002", 50, "Active", 20.0),
        ("TINY", "B", "002", 50, "Active", 20.0),
    ]
    assert result["records"][1]["change"] == pytest.approx(-25.0, rel=1e-9, abs=1e-9)
    assert result["records"][1]["percent_change"] == pytest.approx(-25.0, rel=1e-9, abs=1e-9)
    assert [(s["study_id"], s["arm"], s["participants"], s["records"])
            for s in result["arm_summaries"]] == [
        ("OTHER", "Other arm", 1, 2), ("TINY", "Active", 2, 4), ("TINY", "Control", 1, 0),
    ]
    assert [(s["study_id"], s["visit"]) for s in result["visit_summaries"]] == [
        ("OTHER", "BASELINE"), ("OTHER", "DAY 15"), ("TINY", "BASELINE"), ("TINY", "DAY 15"),
    ]


def test_repeated_and_reordered_inputs_have_identical_outputs(supplied_csv, csv_text):
    original = process_csv(*supplied_csv)
    assert process_csv(*supplied_csv) == original
    reversed_inputs = tuple(
        csv_text(list(reversed(list(csv.DictReader(io.StringIO(text))))))
        for text in supplied_csv
    )
    # Identical local executions should be exactly repeatable, including decimals.
    assert process_csv(*reversed_inputs) == original


def test_csv_normalization_and_extra_analysis_columns(tiny_rows, tiny_csv, csv_text):
    transformed = []
    for rows in tiny_rows:
        expanded = [dict(row, BASELINE="9999", CHANGE="9999", PCHG="9999") for row in reversed(rows)]
        fields = list(reversed(list(expanded[0])))
        padded = [{f" {key} ": f" {value} " for key, value in row.items()} for row in expanded]
        text = csv_text(padded, [f" {field} " for field in fields])
        transformed.append("\ufeff" + text.replace("\r\n", "\r\n\r\n"))
    assert process_csv(*transformed) == process_csv(*tiny_csv)


def test_fractional_increase_has_unrounded_percentage(tiny_rows, csv_text):
    dm, lb = tiny_rows
    lb[0].update(LBORRES="3", LBSTRESN="3")
    lb[1].update(LBORRES="4", LBSTRESN="4")
    record = process_csv(csv_text(dm), csv_text(lb))["records"][1]
    assert (record["value"], record["baseline"]) == (4.0, 3.0)
    assert record["change"] == pytest.approx(1.0, rel=1e-9, abs=1e-9)
    # A rise from 3 to 4 is one third of baseline, or 33 1/3 percent.
    assert record["percent_change"] == pytest.approx(33.333333333333336, rel=1e-9, abs=1e-9)
