## Todo App – FastAPI, React, Postgres

This project is a learning-focused **Todo application** with a clear separation of concerns:
- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite (TypeScript)
- **Database**: Postgres
- **Orchestration**: Docker Compose

### Repository layout

- `backend/`
  - `app/` – FastAPI application code (currently a basic `/hello` endpoint).
  - `requirements.txt` – Python dependencies (FastAPI, Uvicorn, etc.).
  - `Dockerfile` – Backend container (installs `requirements.txt` and runs Uvicorn).
- `frontend/`
  - Vite React app (initialized with `create-vite`) and `Dockerfile` for the frontend container.
- `infrastructure/`
  - `docker-compose.yml` – Runs backend, frontend, and Postgres together.
  - `env/` – Environment files for each service (`backend.env`, `frontend.env`, `db.env`).
- `learning-notes/`
  - Markdown notes capturing concepts learned (Docker, React tooling, etc.).

### Running the stack

From the project root:

```bash
cd infrastructure
docker compose up --build
```

Services:
- **Backend**: `http://localhost:8000`
- **Frontend**: `http://localhost:3000`
- **Postgres**: `localhost:5432` (internal DB name `todo_app`)

### Local development (backend only)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open `http://localhost:8000/docs` in your browser.

### Project goals

- Practice **modern full-stack architecture** with FastAPI, React, and Postgres.
- Learn **Docker & Docker Compose** for local development workflows.
- Maintain **learning notes** in `learning-notes/` to document concepts and decisions.

