"""Upload CSVs over HTTP and display the backend's descriptive results."""

import math
import os
from pathlib import Path
from urllib.parse import urlsplit

import altair as alt
from dotenv import load_dotenv
import pandas as pd
import requests
import streamlit as st


def show_results(result: dict) -> None:
    for column, (key, label) in zip(st.columns(4), (
        ("participants", "Participants"), ("records", "Joined records"),
        ("observed", "Observed"), ("missing", "Missing"),
    )):
        column.metric(label, result["counts"][key])
    st.subheader("Joined records")
    st.dataframe(result["records"], hide_index=True)
    st.subheader("Arm summaries")
    st.dataframe(result["arm_summaries"], hide_index=True)
    st.subheader("Visit summaries")
    st.dataframe(result["visit_summaries"], hide_index=True)
    st.subheader("Mean lipoprotein(a) by visit")
    st.caption(
        "Observed values only, in nmol/L. Missing values remain missing; "
        "an all-missing visit has no mean."
    )
    chart = alt.Chart(pd.DataFrame(result["visit_summaries"])).mark_line(point=True).encode(
        x=alt.X("study_day:Q", title="Study day"),
        y=alt.Y("mean:Q", title="Mean lipoprotein(a) (nmol/L)", scale=alt.Scale(zero=False)),
        color=alt.Color("arm:N", title="Arm"),
        column=alt.Column("study_id:N", title="Study"),
        tooltip=["study_id:N", "arm:N", "visit:N", "mean:Q", "unit:N", "observed:Q", "missing:Q"],
    )
    st.altair_chart(chart, width="stretch")


def main() -> None:
    st.set_page_config(page_title="Synthetic healthcare explorer", layout="wide")
    st.title("Synthetic healthcare explorer")
    st.caption(
        "Synthetic teaching data only. These descriptive results do not establish "
        "clinical benefit or treatment effects."
    )
    load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)
    backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").strip().rstrip("/")
    try:
        address = urlsplit(backend_url)
        if address.scheme not in {"http", "https"} or not address.hostname or address.query or address.fragment:
            raise ValueError
        address.port  # Reject invalid or out-of-range ports before the request.
    except ValueError:
        st.error("Set BACKEND_URL to an HTTP(S) API base address, such as http://127.0.0.1:8000.")
        return
    try:
        request_timeout = float(os.getenv("REQUEST_TIMEOUT", "30"))
        if not math.isfinite(request_timeout) or request_timeout <= 0:
            raise ValueError
    except ValueError:
        st.error("Set REQUEST_TIMEOUT to a finite, positive number of seconds, such as 30.")
        return
    st.caption(f"Backend: {backend_url}")
    st.write("Upload both CSVs, then select Process CSVs.")
    participants = st.file_uploader("Participants CSV (DM)", type=["csv"])
    laboratory = st.file_uploader("Laboratory CSV (LB)", type=["csv"])
    submitted = st.button(
        "Process CSVs", type="primary",
        disabled=participants is None or laboratory is None,
    )
    if submitted and participants is not None and laboratory is not None:
        try:
            with st.spinner("Processing CSVs…"):
                response = requests.post(
                    f"{backend_url}/process",
                    files={
                        "participants": (participants.name, participants.getvalue(), "text/csv"),
                        "laboratory": (laboratory.name, laboratory.getvalue(), "text/csv"),
                    },
                    timeout=request_timeout,
                )
        except requests.Timeout:
            st.error(
                "The backend request timed out. Check that the API is ready, "
                "then retry or increase REQUEST_TIMEOUT in the repository-root .env file."
            )
            return
        except requests.ConnectionError:
            st.error(
                "Could not connect to the backend. Start the API and check BACKEND_URL "
                "in the repository-root .env file, then try again."
            )
            return
        try:
            payload = response.json()
        except requests.exceptions.JSONDecodeError:
            st.error(
                f"Backend returned a non-JSON response (HTTP {response.status_code}). "
                "Check BACKEND_URL points to the FastAPI service and inspect its logs."
            )
            return
        if response.status_code != 200:
            st.error(f"Backend rejected the request (HTTP {response.status_code}).")
            details = payload.get("detail", []) if isinstance(payload, dict) else []
            if isinstance(details, list):
                for issue in details:
                    if not isinstance(issue, dict):
                        continue
                    location = [str(issue.get("file") or "Upload")]
                    if issue.get("row") is not None:
                        location.append(f"row {issue['row']}")
                    if issue.get("field"):
                        location.append(str(issue["field"]))
                    st.error(f"{' · '.join(location)}: {issue.get('message', 'Invalid input.')}")
            st.info("Check the CSVs and backend logs, fix the reported problem, then try again.")
            return
        if (
            not isinstance(payload, dict)
            or not isinstance(payload.get("counts"), dict)
            or not {"participants", "records", "observed", "missing"} <= payload["counts"].keys()
            or any(not isinstance(payload.get(key), list) for key in (
                "records", "arm_summaries", "visit_summaries"
            ))
        ):
            st.error("Backend response does not match the API contract. Check BACKEND_URL and API version.")
            return
        show_results(payload)


if __name__ == "__main__":
    main()
