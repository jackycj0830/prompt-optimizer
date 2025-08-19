# Prompt Optimizer Requirements

## 1. Overview

Prompt Optimizer is a multi-platform AI prompt engineering tool built as a TypeScript/JavaScript pnpm monorepo. Core capabilities live in `packages/core`, UI components and i18n in `packages/ui`, and deliverables include Web SPA, Desktop (Electron), Chrome MV3 Extension, and an MCP Server, with Docker and Vercel deployment options.

## 2. Functional Requirements

### 2.1 Core Features
- User Prompt Optimization: rewrite vague user intents into precise, actionable prompts
- System Prompt Optimization: structure role/behavior rules for reliable controllability
- Iterative Refinement: targeted improvements based on explicit requirements
- A/B and Diff: show before/after with visual text diff
- Streaming: token-level live output while optimizing/testing

### 2.2 Model Management
- Providers: OpenAI, Google Gemini, DeepSeek, Zhipu, SiliconFlow, custom OpenAI-compatible endpoints
- Local/self-hosted: e.g., Ollama via custom API
- Advanced params via `llmParams` (temperature, max_tokens, top_p, etc.)
- Enable/disable, connectivity test, list models
- Environment scanning: discover `VITE_CUSTOM_API_*_suffix` groups and validate

### 2.3 Template Management
- Built-in templates for common scenarios
- Custom templates: CRUD, type categories (user/system/iterate)
- Multi-language support for built-ins (CN/EN)
- Import/export single or bulk

### 2.4 History & Iteration Chains
- Record all optimization/test runs with model/template/time
- Chain tracking for multi-iteration evolution
- Filter/search by dimensions
- Export/backup and restore

### 2.5 Data & Preferences
- One-click full export/import: models, templates, history, preferences
- Validate JSON schemas and data integrity on import
- Preferences: UI language, theme, updater options (e.g., allow prerelease)

### 2.6 UI
- Responsive layout, dark/light theme, i18n
- Markdown rendering, code highlight, fullscreen
- Copy, auto scroll, hotkeys, drag & drop import

## 3. Non-functional Requirements

- Performance: <200ms UI actions; smooth streaming; Desktop startup <5s; memory <500MB typical
- Security: API keys client-side only; optional Vercel password-gating; XSS protection; HTTPS; CORS/SSE headers
- Availability: Windows/macOS/Linux; modern browsers; Desktop offline (excluding API calls); auto update
- Maintainability: strong typing; monorepo layering; Vitest coverage (>80% core); version sync script; complete docs

## 4. Technical Requirements

- Platforms & deploy: Vercel (middleware + edge + SPA), Docker (Nginx + MCP + node-proxy), Desktop (electron-builder), Extension (MV3)
- APIs & protocols: OpenAI/Gemini SDKs; custom OpenAI-compatible; MCP (stdio/HTTP); SSE streaming
- Storage: Dexie (IndexedDB) in browser; file-based storage on Desktop; JSON import/export with validation

## 5. User Needs

- Individuals: quick optimization, multiple models, history; prefer Desktop/Extension or online Web
- Developers: system prompts, API optimizations, batch ops, MCP integration; prefer Web + MCP
- Teams: Docker/intranet, password access, export/auditing; prefer Docker + custom endpoints
- Researchers: detailed history, chain diffs, export for analysis; prefer full-featured Desktop

## 6. Constraints & Dependencies

- Frontend: Vue 3 + Vite + TS; Element Plus; Tailwind (web/extension)
- Services: MCP via Express; Vercel Edge/Serverless; no centralized backend
- Proxy: /api/proxy and /api/stream on Vercel; node-proxy in Docker (localhost→host.docker.internal)
- External: CORS/mixed-content limits; third-party API availability/rate limit

## 7. Acceptance Criteria

- Functionality: prompt optimization, templates, models, history, import/export, preferences
- Compatibility: works on Web/Desktop/Extension/MCP; browsers
- Performance: startup/response/streaming within targets; reasonable memory/CPU
- Security: key protection, password gate, safe inputs/outputs
- Deployment: Vercel one-click, Docker healthcheck ok, Desktop auto-update works

