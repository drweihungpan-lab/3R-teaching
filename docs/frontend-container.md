# Run the frontend in Docker

Use Docker with a running Docker engine and run these commands from the repository root. The [frontend Dockerfile](../frontend/Dockerfile) uses Python 3.12 slim and installs the declared [frontend dependencies](../frontend/requirements.txt). It copies only the requirements and Streamlit application into the image.

## Build and start both images

```bash
docker build --file backend/Dockerfile --tag three-r-backend:local .
docker build --file frontend/Dockerfile --tag three-r-frontend:local .
docker network create three-r-network
docker run --detach --rm --name three-r-backend \
  --network three-r-network --network-alias backend \
  --publish 127.0.0.1:8000:8000 three-r-backend:local
```

The final `.` is the repository-root build context for both Dockerfiles. The existing [.dockerignore](../.dockerignore) excludes local environments, `.env` files, secrets, credentials, and caches. Keep private settings out of the image; pass them at runtime with `--env` or `--env-file .env`.

Starting a container does not guarantee readiness. Check the API before starting the frontend; if it is still starting, wait briefly and retry. See [backend container instructions](backend-container.md) for processing requests and backend settings.

```bash
curl --fail-with-body http://127.0.0.1:8000/health
# Continue when health returns {"status":"ok"}.
docker run --detach --rm --name three-r-frontend \
  --network three-r-network \
  --publish 127.0.0.1:8501:8501 \
  --env BACKEND_URL=http://backend:8000 --env REQUEST_TIMEOUT=30 \
  three-r-frontend:local
```

Open <http://127.0.0.1:8501>. Streamlit listens on `0.0.0.0:8501` inside the container with headless mode enabled. `EXPOSE 8501` documents the internal port; `--publish` makes it reachable from your computer. If host port 8501 is occupied, publish `127.0.0.1:8502:8501` and open port 8502 instead. Use unused container names, or stop containers from earlier examples before reusing their names. Create the network once; reuse it for subsequent runs.

## Backend address and visible behavior

The browser connects to Streamlit on your computer's published port. The Streamlit Python process sends uploads to FastAPI using `BACKEND_URL`. On this shared Docker network, the alias `backend` resolves to the backend container, so the API address is `http://backend:8000`, without `/process`. `localhost` inside the frontend container refers to the frontend itself. Changing the backend's published host port does not change its internal port 8000.

The image defaults `BACKEND_URL` to `http://backend:8000`; override it with `--env BACKEND_URL=...` for another reachable HTTP(S) API. `REQUEST_TIMEOUT` defaults to 30 seconds of connection/read inactivity and must be finite and positive. Recreate the frontend container after changing environment settings. Exported container environment values take precedence over `.env` settings; a host `.env` is not automatically loaded into the container.

Upload [dm.csv](../data/synthetic/dm.csv) and [lb.csv](../data/synthetic/lb.csv) from your computer, then select **Process CSVs**. Expect **24 participants, 96 joined records, 95 observed, 1 missing**, joined records, arm/visit summaries, and a mean lipoprotein(a) chart. Missing values remain unavailable rather than zero. These are synthetic teaching data, not evidence of clinical benefit. The image does not bundle the CSVs; the browser uploads your selected files. See [frontend instructions](frontend.md) for the detailed demonstration and validation errors.

If processing cannot connect, check the shared network, backend alias, readiness, and `BACKEND_URL`. Inspect startup errors with:

```bash
docker logs three-r-backend
docker logs three-r-frontend
```

## Cleanup and verification limits

```bash
docker stop three-r-frontend three-r-backend
docker network rm three-r-network
```

`--rm` removes the stopped containers; built images remain available. Compose orchestration is a separate task ([issue #9](https://github.com/drweihungpan-lab/3R-teaching/issues/9)).

Docker is absent in the implementation environment, so image builds, container startup, networking, and browser uploads against containers were not executed. Verification is limited to Dockerfile source/dependency/command checks, documentation links and command syntax, and review of the existing ignore rules. These checks do not establish local/container replicability. Dependencies use version ranges rather than a lockfile; record the code revision and installed versions when collecting comparison evidence.
