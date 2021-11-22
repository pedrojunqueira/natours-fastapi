## Natours - FASTAPI

### cheat sheet

#### run app locally

`uvicorn --app-dir=. natours.app:app`

#### pytest

`python -m pytest tests/`

#### coverage

% coverage per file

`python -m pytest --cov=natours`

missing coverage

`python -m pytest --cov-report term-missing --cov=natours tests/`
