# Poetry → PDM Migration Guide

This guide documents our migration from Poetry to PDM for the Python desktop refactor, and how contributors can adapt their workflows on Windows/macOS/Linux.

## Why we migrated
- Windows contributor friction with Poetry PATH/installation
- PEP 621 native metadata in pyproject.toml (no tool-specific sections)
- Simple install via `pipx install pdm`

## Summary of changes
- Moved from `[tool.poetry.*]` to PEP 621 `[project]` with dependencies and scripts
- Dev dependencies now live in `[project.optional-dependencies.dev]`
- Build backend changed from `poetry-core` to `pdm-backend`
- CI uses `pdm install`, `pdm run ...` instead of `poetry ...`

## What changed in pyproject.toml
- From:
  - `[tool.poetry.dependencies]`, `[tool.poetry.group.dev.dependencies]`
  - `[tool.poetry.scripts]`
  - `[build-system] poetry-core`
- To:
  - `[project] dependencies = [...]`
  - `[project.optional-dependencies].dev = [...]`
  - `[project.scripts] prompt-optimizer = "po_app.main:main"`
  - `[build-system] pdm-backend`

## CI changes (.github/workflows/python-ci.yml)
- Install PDM with pipx:
  - `python -m pip install -U pip pipx`
  - `pipx install pdm`
- Install & run:
  - `pdm install`
  - `pdm run pytest`
  - `pdm run python build.py`

## Local developer workflow
- Install PDM: `pipx install pdm`
- Install deps: `pdm install`
- Run tests: `pdm run pytest`
- Launch app: `pdm run python po_app/main.py` or `pdm run prompt-optimizer`
- Build EXE: `pdm run python build.py`

## Transition tips for Poetry users
- If you had a Poetry venv: deactivate/remove it before `pdm install` to prevent confusion
- You can keep using your system Python 3.12; PDM will manage a project venv (or configure PDM to use an existing venv)
- Scripts previously run via `poetry run <cmd>` now run via `pdm run <cmd>`

## Troubleshooting PDM on Windows
- `pdm: command not found`
  - Ensure `pipx install pdm` completed and open a new PowerShell (PATH refresh)
  - `pipx ensurepath` if needed
- SSL/cert or proxy issues
  - Set `HTTP_PROXY` / `HTTPS_PROXY` and try again
- Build/EXE issues
  - Use `pdm run python build.py` and check `dist/` artifacts and build_metrics.txt from CI

## Notes
- We kept black/flake8/pytest/pyinstaller in dev optional deps
- No changes to build.py/build.ps1 other than invoking via PDM (`pdm run ...`)

