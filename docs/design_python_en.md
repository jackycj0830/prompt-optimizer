# Prompt Optimizer Python Version - Design

## 1. Architecture
- Single-app layout: po_app/{core,ui,services,storage,utils,assets}/main.py
- Core: LLMService, ModelManager, TemplateManager(+language), PromptService, HistoryManager, PreferenceService, DataManager
- Services: provider adapters (OpenAI, Gemini, OpenAI-compatible)
- Storage: SQLite provider + JSON import/export

## 2. Tech Choices
- GUI: PySide6 (LGPL, complete widgets, good desktop UX)
- Async/Streaming: SDK streaming preferred; otherwise asyncio+httpx with QThread/QRunnable for UI separation
- Config/Security: DPAPI (Windows) or Fernet; %APPDATA%/PromptOptimizer; JSON with schema or preferences table

## 3. Mapping (TS → Python)
- LLMService → core/llm_service.py
- ModelManager → core/model_manager.py
- TemplateManager → core/template_manager.py
- PromptService → core/prompt_service.py
- HistoryManager → core/history_manager.py
- PreferenceService → core/preference_service.py
- DataManager → core/data_manager.py
- StorageFactory/Providers → storage/sqlite_provider.py, storage/json_provider.py

## 4. SQLite Schema (example)
- models, templates, history, preferences tables as in CN doc

## 5. Packaging
- PyInstaller spec and PowerShell script; add-data for assets; onefile default

