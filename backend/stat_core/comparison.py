"""Compare the declared processing contract; only derived decimals have tolerance."""

import argparse
import json
from pathlib import Path
import sys

from .capture import Capture
from .schemas import ArmSummary, Counts, ProcessResult, Record, VisitSummary

REL_TOL = ABS_TOL = 1e-9


def _row(expected, actual, fields, approximate, path):
    if set(expected) != set(fields) or set(actual) != set(fields):
        raise ValueError(f"{path}: fields differ from the processing schema")
    for field in fields:
        left, right = expected[field], actual[field]
        location = f"{path}.{field}"
        if type(left) is not type(right):
            raise ValueError(f"{location}: types or missingness differ")
        if field in approximate and left is not None:
            # Same reference-based rule as pytest.approx, including near zero.
            matches = abs(left - right) <= max(ABS_TOL, REL_TOL * abs(left))
        else:
            matches = left == right
        if not matches:
            raise ValueError(f"{location}: {left!r} != {right!r}")


def compare_results(expected: dict, actual: dict) -> None:
    """Raise ValueError on the first schema, ordering, or value mismatch."""
    ProcessResult.model_validate(expected, strict=True)
    ProcessResult.model_validate(actual, strict=True)
    if set(expected) != set(ProcessResult.model_fields) or set(actual) != set(expected):
        raise ValueError("result: fields differ from the processing schema")
    _row(expected["counts"], actual["counts"], Counts.model_fields, (), "counts")
    for name, schema, approximate in (
        ("records", Record, ("change", "percent_change")),
        ("arm_summaries", ArmSummary, ()),
        ("visit_summaries", VisitSummary, ("mean",)),
    ):
        if len(expected[name]) != len(actual[name]):
            raise ValueError(f"{name}: lengths differ")
        for index, (left, right) in enumerate(zip(expected[name], actual[name], strict=True)):
            _row(left, right, schema.model_fields, approximate, f"{name}[{index}]")


def compare_captures(expected: dict, actual: dict) -> None:
    """Require the same code/data; environment descriptions may differ."""
    for item in (expected, actual):
        Capture.model_validate(item, strict=True)
        if not item["source_sha256"] or set(item["input_sha256"]) != {"participants", "laboratory"}:
            raise ValueError("capture: source and input hashes are required")
    for field in ("format", "source_sha256", "input_sha256"):
        if expected[field] != actual[field]:
            raise ValueError(f"{field}: captures must use the same code and input bytes")
    compare_results(expected["result"], actual["result"])


def _reject_constant(value):
    raise ValueError(f"Nonfinite JSON value: {value}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expected", type=Path)
    parser.add_argument("actual", type=Path)
    args = parser.parse_args()
    try:
        captures = [json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_constant)
                    for path in (args.expected, args.actual)]
        compare_captures(*captures)
    except (OSError, ValueError) as exc:
        print(f"Comparison failed: {exc}", file=sys.stderr)
        return 1
    print("Outputs agree: same code/input hashes; exact records/counts/nulls; derived rel=abs=1e-9.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
