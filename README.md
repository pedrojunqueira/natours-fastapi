# FastAPI back-end

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

# Vue frontend

## Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

### Lints and fixes files

```
npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).
