# Architecture

AgriVision X is divided into four deployable concerns:

- `client/`: React single-page application served by Vite; communicates with the JSON API.
- `server/`: Express API, MySQL connection pool, authentication/upload middleware boundaries, and adapters for external data services.
- `ml-service/`: FastAPI inference boundary and preprocessing/model modules. The health check is live; model-backed routes return HTTP 501 until trained weights and request schemas are supplied.
- `database/`: MySQL 8 schema and intentionally empty seed script.

MySQL is installed and managed separately from this project. Create the `agrivision_x` database, then apply `database/schema.sql`; configure the API connection with the `DB_*` values in `server/.env`. The client, API, and ML service run directly in their respective directories. Datasets and model artifacts are excluded from version control.
