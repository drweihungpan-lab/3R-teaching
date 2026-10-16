# Run the backend in Docker

Use Docker with a running Docker engine. Run the commands below from the repository root. The image uses Python 3.12 slim and installs the backend package and its runtime dependencies from [pyproject.toml](../backend/pyproject.toml). No local Python environment is copied into it.

## Build and start

```bash
docker build --file backend/Dockerfile --tag three-r-backend:local .
docker run --detach --rm --name three-r-backend \
  --publish 127.0.0.1:8000:8000 three-r-backend:local
```

The final `.` is the build context: the repository files available to Docker. Keep it at the root because [backend/Dockerfile](../backend/Dockerfile) copies paths starting with `backend/` and `data/synthetic/`. The root [.dockerignore](../.dockerignore) excludes local environments, secrets, credentials, and caches from that context. The Dockerfile copies package metadata, `app`, `stat_core`, and the two supplied synthetic CSVs with their provenance/dictionary notes. It does not copy the backend tests or the rest of the repository into the image.

The default command is `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`. Binding to `0.0.0.0` lets requests reach the service inside the container. `EXPOSE 8000` describes that internal port; `--publish` makes it reachable on your computer at `http://127.0.0.1:8000`. If that host port is occupied, use `--publish 127.0.0.1:8001:8000` and change the curl/browser addresses to port 8001. The internal port stays 8000.

## Check readiness and process the samples

Starting a container does not mean the API is ready yet. Check it before uploading; if the first request cannot connect during startup, wait briefly and retry. Inspect startup errors with `docker logs three-r-backend`.

```bash
curl --fail-with-body http://127.0.0.1:8000/health
curl --fail-with-body http://127.0.0.1:8000/process \
  -F participants=@data/synthetic/dm.csv \
  -F laboratory=@data/synthetic/lb.csv
```

Health returns HTTP 200 with `{"status":"ok"}`. Processing returns HTTP 200 with `counts`, `records`, `arm_summaries`, and `visit_summaries`. Expected counts are:

```json
{"participants":24,"records":96,"observed":95,"missing":1}
```

The missing laboratory result remains null, not zero. The uploaded files in these curl commands come from your computer. The same synthetic samples are also available inside the image as `/app/data/synthetic/dm.csv` and `/app/data/synthetic/lb.csv`; processing does not automatically load them. The data are invented teaching inputs, not clinical evidence. See the [API contract](api.md) for every response field and input rule, and the [synthetic data notes](../data/synthetic/README.md) for provenance. Open <http://127.0.0.1:8000/docs> for interactive uploads.

For example, save a complete response outside the build context for later output comparison:

```bash
curl --fail-with-body http://127.0.0.1:8000/process \
  -F participants=@data/synthetic/dm.csv \
  -F laboratory=@data/synthetic/lb.csv \
  --output /tmp/three-r-container.json
```

Following the course [glossary](../GLOSSARY.md), comparing repeated runs under the same conditions demonstrates repeatability. Comparing this output with the same code and inputs in a local virtual environment supports replicability once agreement is verified. Compare counts, record structure, strings, and nulls exactly; use the declared test/comparison tolerances for calculated decimals. Building an image alone does not establish agreement.

## Configuration and cleanup

Defaults need no configuration file. Pass optional settings at startup, for example:

```bash
docker run --detach --rm --name three-r-backend-configured \
  --publish 127.0.0.1:8001:8000 \
  --env LOG_LEVEL=DEBUG --env MAX_UPLOAD_BYTES=5242880 \
  three-r-backend:local
```

`MAX_UPLOAD_BYTES` is a limit per uploaded file; the default is 5,242,880 bytes. An oversized file returns HTTP 413. Invalid CSV input or a missing upload returns HTTP 422 with the [documented error envelope](api.md). Invalid configuration prevents startup. See [local setup](setup.md) for setting details. To supply a local `.env`, add `--env-file .env` to `docker run`; Docker passes the values at runtime, and the file stays outside the image.

```bash
docker stop three-r-backend
# Only if you also started the optional configured example:
docker stop three-r-backend-configured
```

`--rm` removes each stopped container; the built image remains available. This task supplies the backend image. The frontend image and Compose configuration are separate tickets.

## Verification limits

Docker is not installed in the implementation environment, so the image build, Docker startup, published port, and curl requests against a container could not be executed there. Local checks use the shared Python 3.12 environment with `PYTHONPATH=backend`: the public processing function and FastAPI test client return the counts above. Package building, Dockerfile source paths/command, documentation links, and ignore rules are checked separately. These checks do not replace a real image build/run or establish local/container replicability. Dependency versions are ranges, not a lockfile; record the code revision and installed versions when collecting comparison evidence.
