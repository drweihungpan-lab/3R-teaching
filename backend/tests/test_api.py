"""HTTP behavior via real multipart requests, without a network listener."""

import json

import pytest

from stat_core import ErrorResponse, ProcessResult, process_csv


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_supplied_upload_returns_processing_contract(client, supplied_csv, uploads):
    response = client.post("/process", files=uploads(supplied_csv))
    assert response.status_code == 200
    result = response.json()
    assert result["counts"] == {"participants": 24, "records": 96, "observed": 95, "missing": 1}
    assert result == process_csv(*supplied_csv)
    assert ProcessResult.model_validate(result).model_dump(mode="json") == result
    # A strict JSON decoder/encoder must never see NaN or Infinity.
    json.dumps(result, allow_nan=False)


@pytest.mark.parametrize("index", [0, 1])
def test_utf8_bom_and_unicode_are_accepted(client, tiny_rows, csv_text, uploads, index):
    dm, lb = tiny_rows
    dm[0]["ARM"] = "Étude α"
    inputs = [csv_text(dm), csv_text(lb)]
    inputs[index] = "\ufeff" + inputs[index]
    response = client.post("/process", files=uploads(inputs))
    assert response.status_code == 200
    assert response.json()["records"][0]["arm"] == "Étude α"
    assert response.json()["counts"] == {"participants": 3, "records": 4, "observed": 4, "missing": 0}


def test_invalid_age_returns_actionable_error(client, tiny_rows, csv_text, uploads):
    dm, lb = tiny_rows
    dm[0]["AGE"] = "forty"
    response = client.post("/process", files=uploads((csv_text(dm), csv_text(lb))))
    assert response.status_code == 422
    assert response.json() == {"detail": [{
        "file": "participants", "row": 2, "field": "AGE",
        "message": "Expected a nonnegative integer.",
    }]}


@pytest.mark.parametrize("case,file,row,field,message", [
    ("unknown_participant", "laboratory", 2, "USUBJID", "No participant matches"),
    ("duplicate_participant", "participants", 3, "USUBJID", "Duplicate participant key"),
    ("duplicate_record", "laboratory", 3, "LBSEQ", "Duplicate record key"),
    ("nonfinite_result", "laboratory", 2, "LBSTRESN", "finite nonnegative number"),
    ("calculation_overflow", "laboratory", 3, "LBSTRESN", "finite numeric range"),
])
def test_domain_errors_reach_http_clients(client, tiny_rows, csv_text, uploads, case, file, row, field, message):
    dm, lb = tiny_rows
    if case == "unknown_participant":
        lb[0]["USUBJID"] = "UNKNOWN"
    elif case == "duplicate_participant":
        dm[1]["USUBJID"] = "A"
    elif case == "duplicate_record":
        lb.insert(1, dict(lb[0]))
    elif case == "nonfinite_result":
        lb[0]["LBSTRESN"] = "NaN"
    else:
        lb[0].update(LBORRES="1e-308", LBSTRESN="1e-308")
        lb[1].update(LBORRES="1e308", LBSTRESN="1e308")
    response = client.post("/process", files=uploads((csv_text(dm), csv_text(lb))))
    assert response.status_code == 422
    payload = response.json()
    assert ErrorResponse.model_validate(payload).model_dump(mode="json") == payload
    assert len(payload["detail"]) == 1
    issue = payload["detail"][0]
    assert (issue["file"], issue["row"], issue["field"]) == (file, row, field)
    assert message in issue["message"]


@pytest.mark.parametrize("file,index", [("participants", 0), ("laboratory", 1)])
def test_upload_limit_counts_utf8_bytes(client_factory, tiny_rows, tiny_csv, csv_text, uploads, file, index):
    # Extra columns are allowed: Unicode text increases bytes but not characters.
    inputs = list(tiny_csv)
    inputs[index] = csv_text([dict(row, NOTE="é" * 400) for row in tiny_rows[index]])
    limit = len(inputs[index])
    # Only the selected file contains the large note; the other fits the limit.
    with client_factory(limit=limit) as client:
        response = client.post("/process", files=uploads(inputs))
    assert response.status_code == 413
    assert response.json() == {"detail": [{
        "file": file, "row": None, "field": None,
        "message": f"File exceeds MAX_UPLOAD_BYTES ({limit} bytes); upload a smaller CSV.",
    }]}


@pytest.mark.parametrize("file,index", [("participants", 0), ("laboratory", 1)])
@pytest.mark.parametrize("contents,message", [
    (b"\xff\xfe", "UTF-8"), (b"", "header"), (b"\x00", "NUL"),
    (b'"unfinished', "Malformed CSV"), (b"arbitrary\nvalue\n", "STUDYID"),
])
def test_invalid_upload_contents_use_error_envelope(client, tiny_csv, uploads, file, index, contents, message):
    inputs = list(tiny_csv)
    inputs[index] = contents
    response = client.post("/process", files=uploads(inputs))
    assert response.status_code == 422
    payload = response.json()
    assert ErrorResponse.model_validate(payload).model_dump(mode="json") == payload
    assert len(payload["detail"]) == 1
    issue = payload["detail"][0]
    assert issue["file"] == file
    assert message in issue["message"]
    if contents in (b"\xff\xfe", b"", b"\x00"):
        assert issue["row"] is None
        assert issue["field"] is None
    else:
        assert issue["row"] == 1
        assert issue["field"] == ("STUDYID" if contents == b"arbitrary\nvalue\n" else None)


@pytest.mark.parametrize("missing", [("participants",), ("laboratory",), ("participants", "laboratory")])
def test_missing_upload_fields(client, tiny_csv, uploads, missing):
    files = uploads(tiny_csv)
    for file in missing:
        del files[file]
    response = client.post("/process", files=files)
    assert response.status_code == 422
    payload = response.json()
    assert ErrorResponse.model_validate(payload).model_dump(mode="json") == payload
    assert [issue["file"] for issue in payload["detail"]] == list(missing)
    for issue in payload["detail"]:
        assert issue["row"] is None
        assert issue["field"] is None
        assert "Supply a CSV upload" in issue["message"]


@pytest.mark.parametrize("file", ["participants", "laboratory"])
def test_text_form_field_is_not_a_file_upload(client, tiny_csv, uploads, file):
    files = uploads(tiny_csv)
    contents = files.pop(file)[1].decode("utf-8")
    response = client.post("/process", files=files, data={file: contents})
    assert response.status_code == 422
    payload = response.json()
    assert ErrorResponse.model_validate(payload).model_dump(mode="json") == payload
    assert len(payload["detail"]) == 1
    assert payload["detail"][0]["file"] == file
    assert payload["detail"][0]["row"] is None
    assert payload["detail"][0]["field"] is None


@pytest.mark.parametrize("file", ["participants", "laboratory"])
def test_upload_limit_is_per_file_and_inclusive(client_factory, tiny_csv, uploads, file):
    # Each valid CSV is exactly limit bytes. Their combined size exceeds limit.
    limit = max(len(text.encode("utf-8")) for text in tiny_csv)
    padded = [text.encode("utf-8").ljust(limit, b"\n") for text in tiny_csv]
    with client_factory(limit=limit) as client:
        response = client.post("/process", files=uploads(padded))
        assert response.status_code == 200
        assert response.json()["counts"] == {"participants": 3, "records": 4, "observed": 4, "missing": 0}
        files = uploads(padded)
        files[file] = ("too-large.csv", files[file][1] + b"\n", "text/csv")
        response = client.post("/process", files=files)
    assert response.status_code == 413
    assert response.json() == {"detail": [{
        "file": file, "row": None, "field": None,
        "message": f"File exceeds MAX_UPLOAD_BYTES ({limit} bytes); upload a smaller CSV.",
    }]}


def test_openapi_exposes_required_uploads_and_result_schemas(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    operation = schema["paths"]["/process"]["post"]
    body_ref = operation["requestBody"]["content"]["multipart/form-data"]["schema"]["$ref"]
    body = schema["components"]["schemas"][body_ref.rsplit("/", 1)[1]]
    assert set(body["required"]) == {"participants", "laboratory"}
    for field in ("participants", "laboratory"):
        upload_schema = body["properties"][field]
        assert upload_schema["type"] == "string"
        # FastAPI versions declare binary uploads using either schema vocabulary.
        assert (upload_schema.get("format") == "binary"
                or upload_schema.get("contentMediaType") == "application/octet-stream")
    for status, expected in [("200", "ProcessResult"), ("422", "ErrorResponse"), ("413", "ErrorResponse")]:
        ref = operation["responses"][status]["content"]["application/json"]["schema"]["$ref"]
        assert ref == f"#/components/schemas/{expected}"
    assert client.get("/docs").status_code == 200
