# AgriVision X

A starter monorepo for farm monitoring, satellite analysis, crop disease workflows, yield estimates, and alerts. The client, API, ML service, and MySQL database are separated so each can be developed independently.

## Requirements

* Node.js 20 or newer and npm
* Python 3.11 or newer
* MySQL 8.0 or newer

## Local Development

### 1. Set up MySQL

Make sure the MySQL server is installed and running locally.

Create the project database:

```sql
CREATE DATABASE agrivision_x;
```

The database schema is available in:

```text
database/schema.sql
```

Run the schema after creating the database.

### 2. Start the Backend

Go to the `server` directory:

```bash
cd server
```

Create a `.env` file using `.env.example` as a reference and configure your MySQL credentials.

Example:

```env
PORT=5000
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=agrivision_x
ML_SERVICE_URL=http://localhost:8000
JWT_SECRET=your_secret
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The API runs on:

```text
http://localhost:5000
```

### 3. Start the ML Service

Go to the `ml-service` directory:

```bash
cd ml-service
```

Create and activate a Python virtual environment:

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI service:

```bash
uvicorn main:app --reload --port 8000
```

The ML service runs on:

```text
http://localhost:8000
```

### 4. Start the Client

Go to the `client` directory:

```bash
cd client
```

Install dependencies:

```bash
npm install
```

Start the Vite development server:

```bash
npm run dev
```

The client runs on:

```text
http://localhost:5173
```

## Services

| Service    | Technology        | Port |
| ---------- | ----------------- | ---: |
| Client     | React + Vite      | 5173 |
| API        | Node.js + Express | 5000 |
| ML Service | Python + FastAPI  | 8000 |
| Database   | MySQL             | 3306 |

Configure client and API URLs using environment variables as needed.

## Data and Models

Place datasets in:

```text
data/
```

or:

```text
ml-service/datasets/
```

Trained model artifacts are not included in the repository.

Compatible trained model weights should be placed under:

```text
ml-service/trained_models/
```

before enabling inference.

Placeholder endpoints should not be treated as actual ML predictions until the corresponding models and inference pipelines are implemented.

## Project Structure

```text
AgriVision-X/
│
├── client/                 # React frontend
├── server/                 # Node.js + Express API
├── ml-service/             # Python ML service
├── database/               # MySQL schema and seed data
├── data/                   # Datasets and sample data
├── docs/                   # Architecture, API and ML documentation
├── .gitignore
└── README.md
```

## Important Note

AgriVision X is being developed as a modular system. The frontend, backend, ML service, and database can be developed and tested independently and integrated progressively.

The satellite analysis, crop segmentation, disease detection, yield prediction, weather integration, and alert workflows will use real data and trained models as they are implemented.

See the `docs/` directory for architecture, API, ML pipeline, and database documentation.
