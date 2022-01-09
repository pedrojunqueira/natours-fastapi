<p align="center">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

# Application Architecture

![Application Architecture](https://github.com/pedrojunqueira/natours-fastapi/blob/master/natours/public/img/Diagram.jpg?raw=true)

## FastAPI back-end

### cheat sheet

#### run app locally

`uvicorn --app-dir=. natours.app:app --reload`

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

### Docker commands

#### build

`docker-compose up --build -d`

#### shut down

`docker-compose down`

#### start

`docker-compose up`

#### Check running containers

`docker ps`

#### attach to logs

`docker-compose logs -f -t`
