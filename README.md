# Cinematic Reading Engine

[![CI](https://github.com/OWNER/Storyboard/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/Storyboard/actions/workflows/ci.yml)

This repository contains the early scaffolding for **Cinei-read**, an MVP
that enhances traditional ebooks with subtle cinematic effects.

## Project Structure
- `backend/` – FastAPI service for uploading EPUBs and generating
  Cinematic Markup.
- `client/` – React Native application for reading enhanced books.
- `model/` – Legacy prototype code (to be refactored).
- `storyboard.py` – Original experiment script (to be revisited).

Both backend and client currently contain placeholder implementations that
will be expanded in future commits.

## Database Migrations

The backend uses [Alembic](https://alembic.sqlalchemy.org/) for database
migrations. Typical commands run from the `backend` directory:

```bash
alembic revision --autogenerate -m "description"  # create a new migration
alembic upgrade head                                # apply migrations
```

## Testing

Run the test suite and verify Python syntax with:

```bash
pytest
python -m py_compile $(git ls-files '*.py')
```

The CI workflow executes these commands on every push.
