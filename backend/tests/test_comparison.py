"""Output agreement through the public comparison and command-line interfaces."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

from stat_core import process_csv


def test_matching_results_allow_only_tiny_derived_differences(tiny_csv):
    from stat_core.comparison import compare_results

    expected = process_csv(*tiny_csv)
    actual = deepcopy(expected)
    actual["records"][1]["change"] = -5.000000001
    actual["records"][1]["percent_change"] = -50.00000001
    actual["visit_summaries"][1]["mean"] = 10.000000001
    compare_results(expected, actual)


@pytest.mark.parametrize("section,index,field,value", [
    ("records", 0, "participant_id", "wrong-id"),
    ("records", 0, "value", 10.000000001),
    ("records", 0, "baseline", 10.000000001),
    ("records", 0, "change", None),
    ("records", 0, "change", 0.000001),
    ("records", 1, "percent_change", -49.0),
    ("records", 0, "status", ""),
    ("arm_summaries", 0, "observed", 3),
    ("visit_summaries", 0, "mean", 16.0),
    ("counts", None, "missing", 1),
    ("counts", None, "missing", False),
    ("counts", None, "records", 4.0),
    ("records", 0, "value", "10"),
    ("records", 0, "change", float("nan")),
    ("visit_summaries", 0, "mean", float("inf")),
])
def test_material_value_type_and_missingness_mismatches_fail(tiny_csv, section, index, field, value):
    from stat_core.comparison import compare_results

    expected = process_csv(*tiny_csv)
    actual = deepcopy(expected)
    row = actual[section] if index is None else actual[section][index]
    row[field] = value
    with pytest.raises(ValueError):
        compare_results(expected, actual)


@pytest.mark.parametrize("mutation", ["missing-field", "extra-field", "length", "order"])
def test_result_structure_is_exact(tiny_csv, mutation):
    from stat_core.comparison import compare_results

    expected = process_csv(*tiny_csv)
    actual = deepcopy(expected)
    if mutation == "missing-field":
        del actual["records"][0]["baseline"]
    elif mutation == "extra-field":
        actual["records"][0]["unexpected"] = 1
    elif mutation == "length":
        actual["records"].pop()
    else:
        actual["records"].reverse()
    with pytest.raises(ValueError):
        compare_results(expected, actual)


def test_capture_records_raw_input_hashes_and_execution_conditions(tmp_path, tiny_csv):
    from stat_core.capture import capture
    from stat_core.comparison import compare_captures

    paths = [tmp_path / name for name in ("dm.csv", "lb.csv")]
    for path, text in zip(paths, tiny_csv, strict=True):
        path.write_bytes(text.encode("utf-8"))
    first = capture(*paths)
    second = capture(*paths)
    assert first["result"]["counts"] == {"participants": 3, "records": 4, "observed": 4, "missing": 0}
    assert first["result"]["visit_summaries"][0]["mean"] == 15.0
    assert first["input_sha256"]["participants"] == hashlib.sha256(paths[0].read_bytes()).hexdigest()
    assert "stat_core/processing.py" in first["source_sha256"]
    assert first["environment"]["python"]
    assert first["environment"]["platform"]
    assert first["environment"]["dependencies"]["pydantic"]
    assert first == second
    second["environment"]["platform"] = "a Docker runner"
    compare_captures(first, second)


@pytest.fixture
def captured_sample(tmp_path):
    from stat_core.capture import capture

    root = Path(__file__).resolve().parents[2] / "data" / "synthetic"
    return capture(root / "dm.csv", root / "lb.csv")


@pytest.mark.parametrize("field", ["source_sha256", "input_sha256"])
def test_changed_code_or_raw_input_hash_fails(captured_sample, field):
    from stat_core.comparison import compare_captures

    actual = deepcopy(captured_sample)
    key = next(iter(actual[field]))
    actual[field][key] = "0" * 64
    with pytest.raises(ValueError, match=field):
        compare_captures(captured_sample, actual)


def test_missing_is_never_zero_even_for_derived_fields(captured_sample):
    from stat_core.comparison import compare_captures

    actual = deepcopy(captured_sample)
    missing = next(row for row in actual["result"]["records"] if row["value"] is None)
    missing["change"] = 0.0
    with pytest.raises(ValueError, match="missingness"):
        compare_captures(captured_sample, actual)


def test_cli_captures_stdout_and_file_then_reports_mismatches(tmp_path):
    root = Path(__file__).resolve().parents[2]
    command = [sys.executable, "-m", "stat_core.capture", "--participants",
               str(root / "data/synthetic/dm.csv"), "--laboratory", str(root / "data/synthetic/lb.csv")]
    first = subprocess.run(command, capture_output=True, text=True, check=True)
    path = tmp_path / "nested" / "capture.json"
    subprocess.run([*command, "--output", str(path)], capture_output=True, text=True, check=True)
    assert json.loads(first.stdout) == json.loads(path.read_text())
    original = tmp_path / "original.json"
    original.write_text(first.stdout)
    compare = [sys.executable, "-m", "stat_core.comparison", str(original), str(path)]
    passed = subprocess.run(compare, capture_output=True, text=True)
    assert passed.returncode == 0
    assert "Outputs agree" in passed.stdout
    changed = json.loads(first.stdout)
    changed["result"]["counts"]["missing"] = 0
    path.write_text(json.dumps(changed))
    failed = subprocess.run(compare, capture_output=True, text=True)
    assert failed.returncode == 1
    assert "counts.missing" in failed.stderr


@pytest.mark.parametrize("contents", ["{", "null", "{}", '{"result": NaN}', '{"result": Infinity}'])
def test_cli_rejects_invalid_capture_json(tmp_path, contents):
    path = tmp_path / "bad.json"
    path.write_text(contents)
    failed = subprocess.run([sys.executable, "-m", "stat_core.comparison", str(path), str(path)],
                            capture_output=True, text=True)
    assert failed.returncode == 1
    assert "Comparison failed" in failed.stderr
