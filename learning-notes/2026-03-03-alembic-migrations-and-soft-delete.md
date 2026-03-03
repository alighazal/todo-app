## Alembic migrations & soft delete – notes

### Alembic basics in this project

- **Config & entrypoint**
  - `backend/alembic.ini` points to Postgres and sets `script_location = alembic`.
  - `backend/alembic/env.py`:
    - Adds the backend root to `sys.path` so `import app...` works.
    - Imports `Base` and `app.models.*` and exposes `target_metadata = Base.metadata`.
  - This lets Alembic compare **current DB schema** vs **SQLAlchemy models**.

- **Applying migrations**
  - From `infrastructure/` (Docker Compose):
    - `docker compose exec backend alembic upgrade head`
  - Alembic tracks applied migrations in the `alembic_version` table.

- **Autogenerating new migrations**
  - Typical flow:
    1. Change models in `app/models/` (e.g. add a column).
    2. Make sure the DB is up to date: `alembic upgrade head`.
    3. Generate migration:  
       `docker compose exec backend alembic revision --autogenerate -m "describe change"`.
    4. Review the generated file under `backend/alembic/versions/` and adjust if needed.
  - If the DB is behind, `alembic revision --autogenerate` fails with:  
    **"Target database is not up to date."**  
    → Fix by upgrading first.

- **Resetting the DB in dev**
  - To wipe everything in dev Postgres:
    - `docker compose exec db psql -U postgres -d todo_app`
    - In `psql`:
      ```sql
      DROP SCHEMA public CASCADE;
      CREATE SCHEMA public;
      GRANT ALL ON SCHEMA public TO postgres;
      GRANT ALL ON SCHEMA public TO public;
      ```
    - Then re-run `alembic upgrade head`.

### Adding `is_deleted` soft delete to users

- **Model change**
  - In `app/models/user.py`:
    - Added `is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")`.

- **Migration change**
  - Did **not** edit the initial migration.
  - Created a new migration `0002_add_is_deleted_to_users`:
    - `upgrade()`: `ALTER TABLE users ADD COLUMN is_deleted BOOLEAN NOT NULL DEFAULT false`.
    - `downgrade()`: drops the column.

