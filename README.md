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
        deploy.yml           Deploy pipeline (build, push to GHCR, deploy to EC2)
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

### Branch Protection

The `main` branch is protected with the following rules:

- All changes must go through a pull request
- Status checks (`lint`, `test`, `build`, `scan`) must pass before merging
- Force pushes and branch deletion are blocked

### Deploy Pipeline (live)

Merging to `main` triggers the deploy pipeline:

1. **Build & Push** — Docker image is built and pushed to GitHub Container Registry
2. **Deploy** — SSH into the EC2 instance, pull the latest image, and restart the container

## Running Tests

```
pytest -v
```

## Infrastructure

- **AWS EC2** — Amazon Linux 2023 instance running Docker
- **Elastic IP** — Static public IP for consistent access
- **Security Group** — Port 8000 open for API access, port 22 for SSH (key-based auth only)
- **GHCR** — Docker images stored in GitHub Container Registry

## Status

The full CI/CD pipeline is complete and live. Pull requests are gated by lint, test, build, and scan checks with branch protection enforcing all must pass. Merging to `main` automatically builds, pushes, and deploys the latest image to EC2.
