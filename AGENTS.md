# Contributor Guide (Agents)
This is the only AGENTS.md file for this repository. Do not look for others.

## Special Task Triggers (single-word commands)
If the user task message is exactly one of the following words, open the referenced file; otherwise ignore this section.

- EffectsGuide → open `CINEMATIC_READING_EFFECTS_GUIDE.md`
- Tier4 → open `Enhancing Narrative with Tier 4 Effects.md`
- SystemDesign → open `INTELLIGENT_ANALYSIS_SYSTEM.md`
- Immersion → open `Enhancing Ereader Immersion_ Subtle Effects.md`
- README → open `README.md`

These are documentation aids only; do not treat them as executable tasks.

## Agent Dev Environment Tips (ChatGPT-5/Codex-style sandbox)
- No network: assume zero outbound network. Avoid commands that need internet or remote services.
- Do not create or modify OS/global configs. Operate within the repo only.
- Prefer deterministic, local-only actions: file edits, static analysis, unit tests.
- Do not run destructive DB operations against non-ephemeral stores. Tests should use the repo’s fixtures.

## Repository Layout (orientation)
- Backend (Python/FastAPI, SQLAlchemy): `backend/`
- Client (JS/React Native or web tooling with Jest): `client/`
- Backend tests: `backend/tests/`
- Project docs: root `README.md` and design docs in repository root

## Local Development Setup (no network assumptions)
If your environment supports Python and Node locally without network installs:

Python (backend):
1) Create venv and install deps from `backend/requirements.txt` if available offline.
2) Run API (from `backend/`):
   - Windows CMD: `set PYTHONPATH=.` then `python -m uvicorn app.main:app --reload --port 8000`
   - Unix/PS: `export PYTHONPATH=.` then `uvicorn app.main:app --reload --port 8000`

Node (client):
1) From `client/`, use your local Node toolchain. If dependencies are already present, you can run linters/tests; otherwise skip network installs.

## Linting
- Python: If available, run `flake8` (or `ruff`) on `backend/`. If not available offline, ensure style parity and zero syntax errors.
- JavaScript: From `client/`, run `npm run lint` if dependencies are present; otherwise perform static checks only (no edits that break ESLint config).

## Testing
- Backend: From repo root or `backend/`, run `pytest -q`. Ensure tests do not depend on network. Use fixtures in `backend/tests/conftest.py`.
- Client: From `client/`, run `npm test -- --watchAll=false` if node_modules is available offline. If e2e tests require device/emulator or network, skip them.

Guidelines:
- Tests requiring network must be skipped or mocked in sandbox environments.
- If you add tests, keep them deterministic and self-contained.

## Database & Migrations (Alembic)
- Models live under `backend/app/models/`. If you change models, add a migration in `backend/alembic/versions/` using Alembic.
- Typical commands (only if Alembic/SQLAlchemy are usable offline):
  - Create: `alembic revision --autogenerate -m "describe change"`
  - Apply: `alembic upgrade head`
- Never run migrations against non-ephemeral databases in sandbox.

## Documentation Updates
- Major behavior changes: update `README.md` with user-facing guidance.
- Engine/effects changes: update `CINEMATIC_READING_EFFECTS_GUIDE.md` and/or `Enhancing Narrative with Tier 4 Effects.md`.
- System architecture/analysis pipeline changes: update `INTELLIGENT_ANALYSIS_SYSTEM.md`.

## CHANGELOG.md
- If `CHANGELOG.md` exists, append a single-line, timestamped summary per change. If it doesn’t exist and your change is significant, create it.
- If errors were encountered during development, indent follow-up bullet lines beneath the entry with brief notes.

## DEVELOPMENT.md
- If you introduce components that require manual startup or env vars, document exact steps/commands in `DEVELOPMENT.md`. Mirror any environment steps in project scripts where appropriate.
- If environment variables are needed, add `.env.template` at the project root or under `backend/` as appropriate, and list the variables (no secrets). If Python needs them, consider adding `python-dotenv` to `backend/requirements.txt` (only if offline install feasible next session).

## Pull Request (PR) Requirements
- All modified code must pass tests locally (backend `pytest`, client `npm test` if available).
- No linter errors (Python/JS) where linters are available.
- Update docs relevant to your change.
- Keep PRs scoped: one logical change set per PR; include rationale and affected modules.
- Do not introduce network dependencies without documenting them and updating setup instructions.

## Safety & Accessibility (Effects Engine)
- Respect the Cognitive Load Governor, Tier hierarchy, and diegesis rules in all effect changes.
- For Tier 3 and Tier 4 additions, include accessibility fallbacks and validation metadata in the registries.

## Quick Commands Reference (if tools available offline)

Backend:
```
cd backend
set PYTHONPATH=. && python -m uvicorn app.main:app --reload --port 8000
pytest -q
```

Client:
```
cd client
npm run lint
npm test -- --watchAll=false
```

Alembic (optional/offline only):
```
cd backend
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

## What Not To Do
- Do not attempt network installs or remote API calls.
- Do not add placeholder code that breaks tests or style.
- Do not bypass the Tier 4 budget/validation process when editing registries.

End of document


