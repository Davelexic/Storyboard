# Cinematic Reading Engine

This repository contains the early scaffolding for **Cinei-read**, an MVP
that enhances traditional ebooks with subtle cinematic effects.

## Project Structure
- `backend/` – FastAPI service for uploading EPUBs and generating
  Cinematic Markup.
- `client/` – React Native application for reading enhanced books.
- `legacy/` – Historical prototypes not used by the MVP.

Both backend and client currently contain placeholder implementations that
will be expanded in future commits.

## Database Migrations

The backend uses [Alembic](https://alembic.sqlalchemy.org/) for database
migrations. Typical commands run from the `backend` directory:

```bash
alembic revision --autogenerate -m "description"  # create a new migration
alembic upgrade head                                # apply migrations
```
