.RECIPEPREFIX := >

.PHONY: install run lint test format

install:
>python -m pip install -e .[dev]

run:
>python -m uvicorn app.main:app --reload --host 0.0.0.0 --port $${API_PORT:-8000}

lint:
>python -m ruff check app tests

test:
>python -m pytest -q

format:
>python -m black app tests
