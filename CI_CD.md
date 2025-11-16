# CI/CD Pipeline Documentation

This project uses GitHub Actions for continuous integration and deployment.

## Workflows

### 1. Run Tests (`test.yml`)

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main`

**What it does:**
- Checks out the code
- Sets up Python 3.10
- Starts a PostgreSQL test database
- Installs dependencies from `requirements.txt`
- Waits for Postgres to be ready
- Runs `pytest` with coverage
- Uploads the coverage report

**Environment:**
- OS: Ubuntu latest
- Python: 3.10
- PostgreSQL: 14 (Docker service)

---

### 2. Build and Push Docker Image (`docker-build.yml`)

**Triggers:**
- Push to `main`
- Push tags starting with `v`
- Pull requests to `main` (build only, no push)

**What it does:**
- Checks out the code
- Sets up Docker Buildx
- Logs in to Docker Hub (using GitHub secrets)
- Generates image tags and labels
- Builds the Docker image
- Pushes the image to Docker Hub (only for non-PR events)

**Image tags (examples):**
- `latest` – default branch image
- `main-<sha>` – specific commit
- `v1.0.0` – version tags

---

### 3. Code Quality (`code-quality.yml`)

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main`

**What it does:**
- Checks out the code
- Sets up Python 3.10
- Installs `black`, `isort`, and `flake8`
- Runs:
    - `black --check src/ tests/`
    - `isort --check-only src/ tests/`
    - `flake8 src/ tests/ --max-line-length=120`

**Tools:**
- **Black** – code formatter
- **isort** – import sorter
- **Flake8** – style and linting

---

## Required GitHub Secrets

These secrets must be configured in:

`Settings → Secrets and variables → Actions`

- `DOCKER_USERNAME` – your Docker Hub username  
- `DOCKER_PASSWORD` – your Docker Hub access token (recommended) or password  

They are used by the Docker build workflow to log in and push images.

---

## Development Workflow with CI/CD

1. Create a feature branch:
    
        git checkout -b feature/new-feature

2. Make changes and commit:
    
        git add .
        git commit -m "Describe the change"

3. Push and open a Pull Request:
    
        git push origin feature/new-feature

4. GitHub Actions will automatically:
    - Run tests
    - Run code quality checks
    - Build Docker image (no pushing on PRs)

5. When merged into `main`:
    - Tests run again
    - Docker image is built and pushed to Docker Hub

---

## Release Process

1. Create and push a version tag:
    
        git tag -a v1.0.0 -m "Release 1.0.0"
        git push origin v1.0.0

2. The Docker build workflow will:
    - Build the image
    - Tag it with `v1.0.0`, `v1.0`, and `v1`
    - Push it to Docker Hub

---

## Running Images from Docker Hub

Examples:

- Pull the latest image:
    
        docker pull zhalamehdili/ml-churn-prediction:latest

- Run the container:
    
        docker run -d -p 8000:8000 \
          -e DATABASE_URL=postgresql://user:pass@host:5432/db \
          zhalamehdili/ml-churn-prediction:latest

- Pull a specific version:
    
        docker pull zhalamehdili/ml-churn-prediction:v1.0.0

---

## Code Quality Standards

- **Black**
    - Line length: 120
    - Target: Python 3.10
- **isort**
    - Profile: `black`
    - Line length: 120
- **Flake8**
    - Max line length: 120
    - Ignored rules: `E203`, `W503`, `E501`
    - `__init__.py` can have unused imports (for package exports)

---

## Running Checks Locally

Before pushing:

    # Format code
    black src/ tests/

    # Sort imports
    isort src/ tests/

    # Lint
    flake8 src/ tests/ --max-line-length=120 --exclude=venv,__pycache__

    # Tests with coverage
    pytest tests/ -v --cov=src

---

## Troubleshooting

- If tests fail in CI:
    - Check logs in the **Actions** tab
    - Try running `pytest` locally
- If Docker build fails:
    - Try building locally:
      
            docker build -t test-image .
- If push to Docker Hub fails:
    - Re-check `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets