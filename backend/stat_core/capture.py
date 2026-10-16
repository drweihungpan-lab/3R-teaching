"""Capture real processing output and the conditions needed to compare runs."""

import argparse
import hashlib
from importlib.metadata import distributions
import json
from pathlib import Path
import platform
import sys
from typing import Annotated, Literal

from pydantic import Field

from .processing import process_csv
from .schemas import ProcessResult, Schema

Digest = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]


class Environment(Schema):
    python: str
    platform: str
    dependencies: dict[str, str]


class Capture(Schema):
    format: Literal["three-r-capture-1"]
    source_sha256: dict[str, Digest]
    input_sha256: dict[str, Digest]
    environment: Environment
    result: ProcessResult


def capture(participants: Path, laboratory: Path) -> dict:
    """Hash the exact input bytes and backend Python sources used by this run."""
    inputs = {"participants": participants.read_bytes(), "laboratory": laboratory.read_bytes()}
    root = Path(__file__).resolve().parent.parent
    sources = sorted(path for package in ("stat_core", "app")
                     for path in (root / package).rglob("*.py"))
    return {
        "format": "three-r-capture-1",
        "source_sha256": {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sources},
        "input_sha256": {name: hashlib.sha256(raw).hexdigest() for name, raw in inputs.items()},
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "dependencies": {dist.metadata["Name"].lower(): dist.version for dist in distributions()},
        },
        "result": process_csv(inputs["participants"].decode("utf-8"), inputs["laboratory"].decode("utf-8")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--participants", type=Path, required=True)
    parser.add_argument("--laboratory", type=Path, required=True)
    parser.add_argument("--output", type=Path, help="Write JSON here instead of stdout")
    args = parser.parse_args()
    try:
        payload = json.dumps(capture(args.participants, args.laboratory), indent=2,
                             sort_keys=True, allow_nan=False) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(payload, encoding="utf-8")
        else:
            sys.stdout.write(payload)
    except (OSError, ValueError) as exc:
        print(f"Capture failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
