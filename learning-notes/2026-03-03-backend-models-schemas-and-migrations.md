## Backend models, schemas & migrations

- **ORM models (database representation)**
  - Live under `backend/app/models/` and use **SQLAlchemy ORM** (`Base` from `app.db.base`).
  - Represent the core tables in the todo domain:
    - `User` → `users` table (auth/profile).
    - `Project` → `projects` table (grouping of todos).
    - `ProjectMember` → `project_members` table (many-to-many user↔project with roles).
    - `Todo` → `todos` table (individual tasks, with rich-text `description` as notes).
  - Relationships (e.g. `Project.todos`, `User.owned_projects`, `ProjectMember.project`) capture navigation between tables at the Python layer.

- **Pydantic schemas (API contracts)**
  - Will live under `backend/app/schemas/` and define **request/response shapes** for FastAPI.
  - Decouple DB structure from API:
    - Example: expose `email` but never `hashed_password`.
    - Separate models like `TodoCreate`, `TodoUpdate`, `TodoRead` let the API control which fields are writable vs. read-only.

- **Alembic migrations (schema evolution)**
  - Alembic is the **migration engine** that keeps Postgres schema in sync with the ORM models.
  - Key pieces:
    - `backend/alembic.ini` – config file with `script_location = alembic` and `sqlalchemy.url` pointing at the Postgres instance.
    - `backend/alembic/env.py` – wires Alembic to `Base.metadata` and imports `app.models.*` so it “knows” about all tables.
    - `backend/alembic/versions/` – versioned migration scripts (e.g. `0001_initial_schema.py`) describing how to create or alter tables, indexes, and types.
  - Common workflow:
    1. Change/add SQLAlchemy models in `app/models/`.
    2. Generate a migration: `alembic revision --autogenerate -m "describe change"`.
    3. Inspect and adjust the generated script under `alembic/versions/`.
    4. Apply it: `alembic upgrade head` (e.g. via `docker compose exec backend alembic upgrade head`).

- **Enums and Postgres types (lesson learned)**
  - For fields like `Todo.status` and `Todo.priority`, use **Python enums** in the model and **Postgres enum types** at the DB level.
  - SQLAlchemy’s Postgres `Enum` type can auto-create the enum in Postgres, but:
    - Re-running migrations or manually creating the type can cause `DuplicateObject` errors (“type ... already exists”).
    - Safer patterns:
      - Let Alembic create the enum once and avoid recreating it.
      - Or wrap `CREATE TYPE` in a `DO $$ ... IF NOT EXISTS ... $$;` block and set `create_type=False` on the SQLAlchemy `Enum` used in migrations.
  - Big idea: **Alembic migrations are the source of truth for schema changes**; keep the database state and the version history aligned to avoid surprises.

