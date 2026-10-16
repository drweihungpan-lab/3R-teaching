"""Run from the repo root with uvicorn app.main:app --app-dir backend."""

import logging
import os
from pathlib import Path
from typing import Annotated, Any, Literal

from dotenv import load_dotenv
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from stat_core import ErrorResponse, InvalidInputError, ProcessResult, ValidationIssue, process_csv


def _read_upload(upload: UploadFile, file: Literal["participants", "laboratory"], limit: int) -> str:
    contents = upload.file.read(limit + 1)
    if len(contents) > limit:
        # The exception handler uses the same schema as other input errors.
        raise _UploadTooLarge([ValidationIssue(
            file=file, row=None, field=None,
            message=f"File exceeds MAX_UPLOAD_BYTES ({limit} bytes); upload a smaller CSV.",
        )])
    try:
        return contents.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise InvalidInputError([ValidationIssue(
            file=file, row=None, field=None,
            message="Save the CSV as UTF-8 and upload it again.",
        )]) from None


class _UploadTooLarge(InvalidInputError):
    """Separate the HTTP size limit from reusable processing validation."""


def create_app() -> FastAPI:
    """Read local settings once when constructing the service."""
    load_dotenv(Path.cwd() / ".env", override=False)
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        raise ValueError("LOG_LEVEL must be DEBUG, INFO, WARNING, ERROR or CRITICAL.")
    try:
        max_upload_bytes = int(os.getenv("MAX_UPLOAD_BYTES", "5242880"))
    except ValueError:
        raise ValueError("MAX_UPLOAD_BYTES must be a positive integer.") from None
    if max_upload_bytes <= 0:
        raise ValueError("MAX_UPLOAD_BYTES must be a positive integer.")
    logging.basicConfig(level=log_level, format="%(levelname)s %(name)s: %(message)s")
    logging.getLogger("stat_core").setLevel(log_level)
    service = FastAPI(title="Three-R synthetic healthcare API", version="0.1.0")

    @service.exception_handler(InvalidInputError)
    async def invalid_input(_request: Request, error: InvalidInputError) -> JSONResponse:
        status = 413 if isinstance(error, _UploadTooLarge) else 422
        return JSONResponse(status_code=status,
                            content=ErrorResponse(detail=error.issues).model_dump(mode="json"))

    @service.exception_handler(RequestValidationError)
    async def invalid_request(_request: Request, error: RequestValidationError) -> JSONResponse:
        issues = []
        for item in error.errors():
            file = "laboratory" if "laboratory" in item["loc"] else "participants"
            issues.append(ValidationIssue(file=file, row=None, field=None,
                                          message=f"Supply a CSV upload in the '{file}' field. {item['msg']}"))
        return JSONResponse(status_code=422,
                            content=ErrorResponse(detail=issues).model_dump(mode="json"))

    @service.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @service.post("/process", response_model=ProcessResult,
                  responses={422: {"model": ErrorResponse}, 413: {"model": ErrorResponse}})
    def process(
        participants: Annotated[UploadFile, File(description="Participant characteristics (DM) CSV")],
        laboratory: Annotated[UploadFile, File(description="Scheduled laboratory (LB) CSV")],
    ) -> dict[str, Any]:
        return process_csv(_read_upload(participants, "participants", max_upload_bytes),
                           _read_upload(laboratory, "laboratory", max_upload_bytes))

    return service


app = create_app()
