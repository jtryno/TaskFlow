# TaskFlow

A simple task manager REST API built with FastAPI and SQLite. This project is focused on building a full CI/CD pipeline using GitHub Actions, with automated linting, testing, container scanning, and deployment to AWS EC2.

## Tech Stack

**Application:** Python, FastAPI, SQLAlchemy, SQLite

**CI/CD:** GitHub Actions, Docker, Trivy, GitHub Container Registry, AWS EC2

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /tasks | Create a new task |
| GET | /tasks | List all tasks |
| GET | /tasks/{id} | Get a single task by ID |
| PUT | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |

## Running Locally

1. Clone the repository

```
git clone https://github.com/jtryno/TaskFlow.git
cd TaskFlow
```

2. Create a virtual environment and install dependencies

```
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements-dev.txt
```

3. Start the server

```
uvicorn app.main:app --reload
```

4. Open the interactive API docs at http://localhost:8000/docs

## Project Structure

```
TaskFlow/
    app/
        main.py              FastAPI app and route definitions
        models.py            SQLAlchemy database model
        schemas.py           Pydantic request and response schemas
        crud.py              Database operations
        database.py          SQLite engine and session configuration
    tests/
        test_tasks.py        API endpoint tests (pytest)
    .github/workflows/
        pr.yml               PR pipeline (lint, test, build, scan)
    Dockerfile
    .dockerignore
    requirements.txt
    requirements-dev.txt
    setup.cfg
```

## CI/CD Pipeline

### PR Pipeline (live)

Every pull request against `main` triggers the following jobs in sequence:

1. **Lint** — flake8 and black enforce code style
2. **Test** — pytest runs the full test suite with coverage
3. **Build** — Docker image is built
4. **Scan** — Trivy scans the image for HIGH/CRITICAL vulnerabilities

### Deploy Pipeline (coming soon)

Merging to `main` will additionally:

5. **Push** the image to GitHub Container Registry
6. **Deploy** to an AWS EC2 instance

## Running Tests

```
pytest -v
```

## Status

The core API and test suite are complete (8 tests covering all 5 endpoints). The PR pipeline is live and enforcing lint, test, build, and scan gates on every pull request. Up next: deploy pipeline to push images to GHCR and deploy to AWS EC2.
