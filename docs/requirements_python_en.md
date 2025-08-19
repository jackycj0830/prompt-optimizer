# Prompt Optimizer Python Version - Requirements

## 1. Overview
Refactor the TS monorepo into a pure Python desktop app targeting Windows, packaged as a standalone EXE. Migrate core features (prompt optimization, models, templates, history, preferences, data import/export) using Python SDKs and local storage.

## 2. Functional Requirements
- PromptService: user/system/iterate optimization; streaming output
- ModelManager: support OpenAI, Gemini, DeepSeek, OpenAI-compatible endpoints (incl. local proxy/Ollama)
- TemplateManager: CRUD, categories (user/system/iterate), i18n, import/export JSON
- HistoryManager: records with chains, search/filter/export
- Data/Preference: one-click export/import; UI language/theme/updater prefs
- UI: PySide6 tabs (Prompt/Models/Templates/History/Settings)

## 3. Non-functional
- Startup ≤ 3.5s (first ≤ 5s); memory ≤ 400MB; UI latency < 150ms; first token < 2s
- Packaging: PyInstaller (default), Nuitka optional; onefile/onedir; UPX optional
- Windows 10/11 x64; Python 3.12+; Poetry-managed dependencies
- Security: local key storage via DPAPI or Fernet

## 4. Dependencies
pyside6, openai, google-generativeai, httpx, tenacity, sqlalchemy, aiosqlite, cryptography, pydantic, loguru; dev: pytest, pytest-qt, pytest-cov, pyinstaller, black, flake8

## 5. Examples
- PySide6 main window skeleton
- OpenAI streaming generator snippet
- PyInstaller command for onefile build

