# Contributing to ML Churn Prediction

Thank you for considering contributing to this project.

## Development Setup

1. Fork the repository
2. Clone your fork:
    
        git clone https://github.com/zhalamehdili/ml-churn-prediction.git
        cd ml-churn-prediction

3. Create virtual environment:
    
        python -m venv venv
        source venv/bin/activate   # On Windows: venv\Scripts\activate

4. Install dependencies:
    
        pip install -r requirements.txt

5. (Optional) Install dev tools:
    
        pip install black isort flake8 pytest pytest-cov

---

## Development Workflow

### 1. Create a feature branch

    git checkout -b feature/your-feature-name

### 2. Make changes

- Keep code clean and readable
- Use type hints where it makes sense
- Keep functions focused and small where possible

### 3. Format code

    black src/ tests/
    isort src/ tests/
    flake8 src/ tests/ --max-line-length=120 --exclude=venv,__pycache__

### 4. Run tests

    pytest tests/ -v
    # or with coverage
    pytest tests/ --cov=src --cov-report=term

### 5. Commit changes

Use clear commit messages:

    git add .
    git commit -m "Add feature: short description"

### 6. Push and create a Pull Request

    git push origin feature/your-feature-name

Then open a Pull Request on GitHub and describe the changes.

---

## Code Style

- Follow PEP 8 where practical
- Line length: 120 characters
- Use `black` + `isort` for formatting
- Use `flake8` to catch issues early

---

## Testing

- Add tests for new functionality
- Keep test coverage as high as possible
- Use `pytest` for all tests

Example:

    pytest tests/ -v --cov=src

---

## Reporting Issues

When opening an issue, include:

- What you were trying to do
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python version, etc.)

---

## Questions

If something is unclear, open an issue with the `question` label.