# Orders service

## Commands
- Install: `pip install -e ".[dev]"`
- Lint: `ruff check .`
- Types: `pyright`
- Tests: `pytest -q`
- Types and tests together: `./sensors.sh check`

## Layers
- `shop/routes/` handles HTTP and calls services.
- `shop/services/` holds the business rules and calls repositories.
- `shop/repositories/` is the only layer that touches the database.
- Routes never import from repositories.

## Conventions
- Money is an integer number of pence. Never use floats for money.
- Raise `AppError` from `shop/errors.py`. Do not raise bare exceptions.
- To add a new resource, use the add-resource skill.

## Do not edit
- `migrations/`
- `pyproject.toml`
- Existing tests, unless the task says to. Fix the code, not the test.
