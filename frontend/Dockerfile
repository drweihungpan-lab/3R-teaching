FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BACKEND_URL=http://backend:8000

WORKDIR /app

# Build from the repository root; cache dependencies separately from UI changes.
COPY frontend/requirements.txt ./frontend/requirements.txt
RUN python -m pip install --no-cache-dir -r frontend/requirements.txt

COPY frontend/app.py ./frontend/app.py

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "frontend/app.py", "--server.address", "0.0.0.0", "--server.port", "8501", "--server.headless", "true"]
