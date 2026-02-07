# FirstRound-Backend

Python backend for FirstRound. Connects to MongoDB and serves the frontend at `http://localhost:3000` (CORS enabled).

## Setup

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Backend runs at **http://localhost:5000**. Frontend at **http://localhost:3000** can call it.

## Connect from frontend

- Base URL: `http://localhost:5000`
- Health: `GET http://localhost:5000/api/health`
- DB check: `GET http://localhost:5000/api/health/db`

Example (fetch): `fetch('http://localhost:5000/api/health')`

## Structure

- `config/` – MongoDB connection (`config/config.py`)
- `model/` – Data models
- `service/` – Business logic
- `routes/` – API routes (e.g. `routes/health.py`)
- `app.py` – Server startup