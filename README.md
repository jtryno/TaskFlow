# TaskFlow

A simple task manager REST API built with FastAPI and SQLite. This project is focused on building a full CI/CD pipeline using GitHub Actions, with automated linting, testing, container scanning, and deployment to AWS EC2.

## Tech Stack

**Application:** Python, FastAPI, SQLAlchemy, SQLite

**CI/CD Pipeline (coming soon):** GitHub Actions, Docker, Trivy, GitHub Container Registry, AWS EC2

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
        main.py          FastAPI app and route definitions
        models.py        SQLAlchemy database model
        schemas.py       Pydantic request and response schemas
        crud.py          Database operations
        database.py      SQLite engine and session configuration
    tests/
    .github/workflows/
    requirements.txt
    requirements-dev.txt
    setup.cfg
    Dockerfile
```

## Planned CI/CD Pipeline

The pipeline will run through GitHub Actions with the following stages:

1. **Lint** using flake8 and black to enforce code style
2. **Test** using pytest with coverage reporting
3. **Build** a Docker image
4. **Scan** the image for vulnerabilities using Trivy
5. **Push** the image to GitHub Container Registry
6. **Deploy** to an AWS EC2 instance

Pull requests will trigger linting, testing, building, and scanning. Merging to main will additionally push the image and deploy to production.

## Status

Currently building out the core API. The CI/CD pipeline, Docker setup, and deployment configuration are up next.
