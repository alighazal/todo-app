## Architecture & Tooling Summary

- **Overall stack**
  - Backend: **FastAPI** (Python) serving a JSON API.
  - Frontend: **React** SPA (planned with Vite) consuming the API.
  - Database: **Postgres** as the main relational datastore.
  - Orchestration: **Docker Compose** to run backend, frontend, and db together.

- **Repository structure (high level)**
  - `backend/` – FastAPI app, models, schemas, services, DB setup.
  - `frontend/` – React app, components, pages, hooks, types, styles.
  - `infrastructure/` – `docker-compose.yml`, env files, infra-related config.
  - `.cursor/plans/` – non-committed planning docs.

- **Dockerfiles (concepts)**
  - Backend uses `python:3.12-slim` to keep the image small but fully featured.
  - `PYTHONDONTWRITEBYTECODE=1`: prevents Python from writing `.pyc` files, reducing noise and disk writes.
  - `PYTHONUNBUFFERED=1`: disables output buffering so logs appear immediately in container logs.
  - Frontend uses a Node image (e.g. `node:22-alpine`), installs dependencies, and runs the dev server on port 3000.
  - Each service has a `.dockerignore` to avoid sending unnecessary files (like `node_modules`, venvs, `.git`, `.cursor`) into the Docker build context.

- **Docker Compose wiring**
  - `backend` service builds from `../backend`, exposes `8000:8000`, depends on `db`, and reads env from `infrastructure/env/backend.env`.
  - `frontend` service builds from `../frontend`, exposes `3000:3000`, depends on `backend`, and reads env from `infrastructure/env/frontend.env`.
  - `db` service uses `postgres:16`, exposes `5432:5432`, and reads env from `infrastructure/env/db.env`, with a named volume `todo-postgres-data` for persistence.

- **Frontend package manager & scaffolding**
  - Preferred generator for the React app: **Vite** (e.g. `npm create vite@latest . -- --template react-ts` in `frontend/`).
  - Before Docker can build the frontend image, the Vite app must exist with `package.json`, `vite.config.*`, and `src/` files.

- **npm vs npx**
  - `npm`: the **package manager** used to install/manage dependencies and run project scripts.
    - Examples: `npm install react`, `npm run dev`.
  - `npx`: the **package runner** used to execute CLI tools from npm without installing them globally (or to run local `node_modules/.bin` tools).
    - Examples: `npx create-vite@latest`, `npx eslint .`.

- **React core language / build variants (Vite templates)**
  - **TypeScript**: React app using TypeScript with Vite’s default tooling; safest, most common choice.
  - **TypeScript + React Compiler**: Same as above but enables the new (experimental) React Compiler for potential performance gains via auto‑memoization.
  - **TypeScript + SWC**: Uses the SWC compiler (Rust-based, very fast) instead of the default toolchain for transpilation.
  - **JavaScript**: React app with plain JavaScript, no type safety, otherwise similar structure to the TS template.
  - **JavaScript + React Compiler**: JS version of the React Compiler-enabled template.
  - **JavaScript + SWC**: Plain JS template using SWC for faster builds.
  - **RSC**: Template centered around React Server Components patterns (more advanced, mixes server/client components).
  - **React Router v7**: Preconfigured with React Router v7 for client-side routing.
  - **TanStack Router**: Uses TanStack Router instead of React Router, focusing on type-safe, data-aware routing.
  - **RedwoodSDK**: Integrates Redwood SDK for a more opinionated, full-stack oriented experience.
  - **Vike**: Uses Vike meta-framework on top of React/Vite to support flexible SSR/SPA patterns.

- **Docker persistence options**
  - **Named volumes** (what the Postgres service uses now)
    - Syntax: `todo-postgres-data:/var/lib/postgresql/data` plus a `volumes:` section defining `todo-postgres-data:`.
    - Data lives outside the container’s filesystem in Docker-managed storage and survives container rebuilds.
    - Great default for databases where you don’t need to inspect files directly.
  - **Bind mounts (host directories)**
    - Syntax: `./db-data:/var/lib/postgresql/data`.
    - Maps a real directory on the host into the container; you can see and manipulate the files directly.
    - Useful for source code hot-reload or when you need direct file inspection, but more OS/permission sensitive.
  - **tmpfs mounts (in-memory)**
    - Mounts that live only in RAM; data disappears when the container stops.
    - Good for ephemeral caches or sensitive data that should never hit disk, not for long-term DB storage.
  - **External / managed databases**
    - Instead of running Postgres in Docker, point your app at a database running on the host or a managed cloud service.
    - Makes the app containers stateless; persistence is handled entirely outside Docker.

