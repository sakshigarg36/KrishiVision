# API

The Express API defaults to `http://localhost:5000/api`; set `VITE_API_URL` in the Vite environment to override it. `GET /api/health` returns `{ "status": "ok" }`.

Route groups are mounted under `/api/auth`, `/api/fields`, `/api/analysis`, `/api/disease`, `/api/yield`, and `/api/alerts`. Their route shapes are defined in `server/src/routes/`. Domain handlers intentionally return HTTP 501 until persistence, auth, validation, and provider behavior are implemented.

The FastAPI service defaults to `http://localhost:8000`, exposes `GET /health`, and mounts `/ndvi`, `/segmentation`, `/disease`, and `/yield` routes. Inference endpoints return HTTP 501 when real inputs and model weights are not configured.
