"""Independent CSV inputs; never import production field lists or helpers."""

import csv
from copy import deepcopy
import io
from pathlib import Path

import pytest


DM_FIELDS = "STUDYID DOMAIN USUBJID SUBJID AGE AGEU SEX ARM RFSTDTC RFENDTC".split()
LB_FIELDS = (
    "STUDYID DOMAIN USUBJID LBSEQ LBTESTCD LBTEST LBORRES LBORRESU "
    "LBSTRESN LBSTRESU VISIT LBDY LBDTC LBSTAT LBREASND"
).split()

# Worked example: two Active participants have 10 -> 5 and 20 -> 15 nmol/L.
# A third participant has no supplied laboratory rows, but counts in DM.
DM_ROWS = [
    ["TINY", "DM", "A", "001", "40", "YEARS", "F", "Active", "2026-01-01", "2026-03-31"],
    ["TINY", "DM", "B", "002", "50", "YEARS", "M", "Active", "2026-01-01", "2026-03-31"],
    ["TINY", "DM", "C", "003", "60", "YEARS", "F", "Control", "2026-01-01", "2026-03-31"],
]
LB_ROWS = [
    ["TINY", "LB", "A", "1", "LPA", "Lipoprotein(a)", "10", "nmol/L", "10", "nmol/L", "BASELINE", "1", "2026-01-01", "", ""],
    ["TINY", "LB", "A", "2", "LPA", "Lipoprotein(a)", "5", "nmol/L", "5", "nmol/L", "DAY 15", "15", "2026-01-15", "", ""],
    ["TINY", "LB", "B", "1", "LPA", "Lipoprotein(a)", "20", "nmol/L", "20", "nmol/L", "BASELINE", "1", "2026-01-01", "", ""],
    ["TINY", "LB", "B", "2", "LPA", "Lipoprotein(a)", "15", "nmol/L", "15", "nmol/L", "DAY 15", "15", "2026-01-15", "", ""],
]


@pytest.fixture
def tiny_rows():
    return (
        [dict(zip(DM_FIELDS, row)) for row in deepcopy(DM_ROWS)],
        [dict(zip(LB_FIELDS, row)) for row in deepcopy(LB_ROWS)],
    )


@pytest.fixture
def csv_text():
    def encode(rows, fields=None):
        output = io.StringIO(newline="")
        writer = csv.DictWriter(output, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
        return output.getvalue()

    return encode


@pytest.fixture
def tiny_csv(tiny_rows, csv_text):
    return tuple(csv_text(rows) for rows in tiny_rows)


@pytest.fixture(scope="session")
def supplied_csv():
    directory = Path(__file__).resolve().parents[2] / "data" / "synthetic"
    return tuple((directory / name).read_text(encoding="utf-8") for name in ("dm.csv", "lb.csv"))


@pytest.fixture
def client_factory(monkeypatch):
    def make_client(limit=5242880):
        # Configure only the public environment boundary, never private helpers.
        monkeypatch.setenv("MAX_UPLOAD_BYTES", str(limit))
        monkeypatch.setenv("LOG_LEVEL", "WARNING")
        from app.main import create_app
        from fastapi.testclient import TestClient

        return TestClient(create_app())

    return make_client


@pytest.fixture
def client(client_factory):
    with client_factory() as service:
        yield service


@pytest.fixture
def uploads():
    def files(inputs):
        return {
            file: ("arbitrary.bin", text.encode("utf-8") if isinstance(text, str) else text,
                   "application/octet-stream")
            for file, text in zip(("participants", "laboratory"), inputs, strict=True)
        }

    return files
