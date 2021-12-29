## Natours - FASTAPI

### cheat sheet

#### run app locally

`uvicorn --app-dir=./back_end natours.app:app --reload`

#### pytest

`python -m pytest tests/`

#### time tests

`python -m pytest tests -v --durations=0`

#### coverage

% coverage per file

`python -m pytest --cov=natours`

missing coverage

`python -m pytest --cov-report term-missing --cov=natours tests/`

#### linter

`black .`

`isort **/*.py`
