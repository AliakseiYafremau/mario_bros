# Mario Bros game

You can find documentation in [`docs` folder](docs/index.md).

## Setup project

```bash
python -m venv .venv
source .venv/bin/activate # for Linux
pip install -r requirements.txt
```

## Run

```bash
python -m game.main
```

## Development

### Install dependencies

Create and activate a virtual environment as described in the "Setup project" section, then install dev dependencies:

```bash
pip install -r dev_requirements.txt
```

### Build report

To generate pdf-report use:
```bash
mkdocs build
```

To setup report as a site use:
```bash
mkdocs serve
```
The report will be available at http://127.0.0.1:8000/


### Lint, format and type check

```bash
ruff check --fix # to lint
ruff format # to format
mypy game # to type checking
```

> [!IMPORTANT]
> You should install all project dependencies to use `mypy`
