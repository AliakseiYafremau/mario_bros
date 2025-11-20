(You can pull the difficulties branch, regardless Ill keep working on it until its done but at least its midly understandable now and it partially works)

# Mario Bros game

You can find report in [`docs`](docs/index.md) folder.

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

## Build report

```bash
pip install -r dev_requirements.txt
mkdocs build
```

`report.pdf` will be generated.
