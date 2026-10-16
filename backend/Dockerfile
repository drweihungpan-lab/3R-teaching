FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Build from the repository root; install only the declared runtime dependencies.
COPY backend/pyproject.toml backend/README.md ./
COPY backend/app/ ./app/
COPY backend/stat_core/ ./stat_core/
RUN python -m pip install --no-cache-dir .

# Shareable synthetic inputs for direct processing and later output comparisons.
COPY data/synthetic/dm.csv data/synthetic/lb.csv data/synthetic/README.md data/synthetic/data-dictionary.md ./data/synthetic/

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
