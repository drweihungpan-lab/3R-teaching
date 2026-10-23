# Run the teaching application with Docker Compose

Use Docker with a running engine and the Compose v2 plugin (`docker compose`). Run all commands from the repository root. The supplied [Compose file](../compose.yaml) builds the [backend](../backend/Dockerfile) and [frontend](../frontend/Dockerfile) from the root context, using the existing [.dockerignore](../.dockerignore).

## Start and check readiness

```bash
docker compose version
docker compose config --quiet
docker compose up --build
```

Keep that terminal open for logs. In a second terminal at the repository root:

```bash
docker compose ps
curl --fail-with-body http://127.0.0.1:8000/health
```

Expect the backend to become `healthy` and health to return `{"status":"ok"}`. Compose probes `GET /health` inside the backend with Python's standard-library `urllib.request`; no curl installation is needed in the image. Each probe has a two-second request timeout, runs every five seconds, and has a three-second execution timeout. A five-second startup grace period and twelve retries allow startup to finish. The frontend starts only after `condition: service_healthy` is satisfied; no fixed startup sleep is used. This startup gate does not restart the frontend or guarantee later backend availability.

For detached operation, use `docker compose up --build --detach` instead. Inspect logs with:

```bash
docker compose logs --tail=100 backend frontend
```

## Which address goes where?

| Caller | Destination | Address |
| --- | --- | --- |
| Browser on your computer | Streamlit | <http://127.0.0.1:8501> |
| curl/browser on your computer | FastAPI | <http://127.0.0.1:8000> |
| Streamlit Python inside Docker | FastAPI | `http://backend:8000` |
| Backend health probe | Its own API | `http://127.0.0.1:8000/health` |

Compose creates a shared default network where the service name `backend` resolves to the backend container. Inside the frontend container, `localhost` means the frontend itself. Your host browser does not use Docker's service-name lookup. Host ports are bound to loopback; internal ports remain 8000 and 8501. See [individual backend](backend-container.md), [individual frontend](frontend-container.md), and [local frontend](frontend.md) instructions for running without Compose.

## Upload the synthetic samples

1. Open <http://127.0.0.1:8501> and confirm the page shows `Backend: http://backend:8000`.
2. Select [dm.csv](../data/synthetic/dm.csv) for **Participants CSV (DM)** and [lb.csv](../data/synthetic/lb.csv) for **Laboratory CSV (LB)** from your computer.
3. Select **Process CSVs**. Expect **24 participants, 96 joined records, 95 observed, 1 missing**, joined records, arm/visit summaries, and a mean lipoprotein(a) chart by study day and arm, with separate study panels.
4. Check that missing results remain unavailable, not zero. These are [synthetic teaching inputs](../data/synthetic/README.md), not clinical evidence.

Check the API independently of the browser using the same uploads:

```bash
curl --fail-with-body http://127.0.0.1:8000/process \
  -F participants=@data/synthetic/dm.csv \
  -F laboratory=@data/synthetic/lb.csv
```

Expect HTTP 200 and `counts` of `{"participants":24,"records":96,"observed":95,"missing":1}`. See the [API contract](api.md) for response fields and validation errors. Matching visible results alone does not establish repeatability or local/container replicability under the [course definitions](../GLOSSARY.md); formal output comparison belongs to the separate comparison task.

## Optional settings

No `.env` is required. If needed, copy [.env.example](../.env.example) to an ignored root `.env` and edit `LOG_LEVEL`, `MAX_UPLOAD_BYTES`, or `REQUEST_TIMEOUT`. Defaults are `INFO`, `5242880` bytes per uploaded file, and `30` seconds of HTTP connection/read inactivity. Exported shell values take precedence over `.env`; unset a shell value to use the file's value. See [setup](setup.md) and [frontend settings](frontend.md) for valid values.

Compose substitutes these three settings into the service environments. It explicitly sets `BACKEND_URL=http://backend:8000`, so the local address in `.env.example` cannot misdirect container requests. The `.env` file is not copied or mounted into either image. Apply setting changes by recreating services:

```bash
docker compose up --build --detach
```

## Troubleshoot connections

- **Engine or build failure:** check that Docker is running, `docker compose version` succeeds, and you are at the repository root. Read the build error and the Dockerfile instructions linked above.
- **Port already allocated:** stop earlier standalone containers or local API/Streamlit processes using ports 8000/8501. Alternatively, edit only the host side of the mappings in `compose.yaml`, for example `127.0.0.1:8001:8000` and `127.0.0.1:8502:8501`, then recreate services. Use the new host ports in curl/browser addresses; keep `http://backend:8000` internally.
- **Backend unhealthy / frontend waiting:** use `docker compose ps` and `docker compose logs --tail=100 backend`. Repair startup/configuration errors and rerun `docker compose up --build`. Increasing a delay does not repair a failed API.
- **Frontend cannot connect:** confirm the displayed backend address uses `backend`, not `localhost`. Check backend health, then run the command below from the frontend container. It exercises service-name lookup and the shared network; both services must belong to the same Compose project.

```bash
docker compose exec frontend python -c "import urllib.request; print(urllib.request.urlopen('http://backend:8000/health', timeout=2).read().decode())"
```

If this fails, inspect both services' logs and recreate them together with `docker compose down` followed by `docker compose up --build`. Avoid starting one service from a different directory or with a different project name. If a request times out after successful readiness, inspect backend logs before raising `REQUEST_TIMEOUT`.

## Shut down

```bash
docker compose down
```

This stops and removes this project's containers and default network. Built images and host CSVs remain. In attached mode, Ctrl-C stops the services; run `docker compose down` afterward to remove their containers and network.

## Recorded evidence

See [verification](verification.md) for the hosted run that built both images, started Compose, and compared outputs.
