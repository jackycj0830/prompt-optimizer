# Prompt Optimizer Design

## 1. System Architecture

### 1.1 Monorepo & Layers
- pnpm workspace with `packages/*`
- Layers:
  - Core (packages/core): business services (LLM, model, prompt, template, history, preferences, storage, env, IPC safety)
  - UI (packages/ui): Vue components + i18n plugin; reusable UX layer
  - Apps: Web (packages/web), Desktop (packages/desktop), Extension (packages/extension)
  - Server: MCP Server (packages/mcp-server) exposing tools via stdio/HTTP
  - Infra: Vercel middleware + Edge functions (api/*); Docker + Nginx + node-proxy

### 1.2 Dependencies
- `@prompt-optimizer/ui` -> `@prompt-optimizer/core`
- Web/Extension -> UI (indirectly core)
- Desktop -> core (main process) and loads web build for renderer
- MCP Server -> core

### 1.3 Core Services
- LLMService: unify providers (OpenAI/Gemini/DeepSeek/Zhipu/SiliconFlow/custom)
- ModelManager: config, enable/disable, validate, init, import/export
- TemplateManager + TemplateLanguageService: CRUD, language switch, import/export
- PromptService: optimize, iterate, test; streaming handlers
- HistoryManager: records and iteration chains; import/export
- PreferenceService: updater channel/ignored versions
- DataManager: aggregate import/export
- Storage: Dexie (browser), File (desktop), Local, Memory
- Env & IPC: runtime detection + safe serialization

## 2. Technical Architecture

### 2.1 Frontend
- Vue 3 + TypeScript + Vite; Vitest
- Element Plus, Tailwind (web/extension), markdown-it, highlight.js, DOMPurify
- i18n plugin (`installI18n`, `installI18nOnly`)

### 2.2 Services
- MCP Server: Express + `@modelcontextprotocol/sdk`; tools: optimize-user/system, iterate; HTTP via StreamableHTTPServerTransport (SSE sessions) or stdio
- Vercel:
  - middleware.js: ACCESS_PASSWORD gate -> /api/auth sets HttpOnly cookie
  - api/proxy.js: generic proxy; api/stream.js: streaming proxy (TransformStream)
  - api/vercel-status.js: status
- Docker: Nginx static + `node-proxy` (SSE, localhost mapping, timeouts/logging)
- Desktop: Electron main creates core services and IPC handlers; renderer loads web build or dev server; electron-updater

### 2.3 Storage
- Browser: Dexie (IndexedDB) + LocalStorage
- Desktop: FileStorageProvider (userData), flush on close with timeout/emergency exit
- Import/export: JSON with schema validation

## 3. Modules Responsibilities

- core: services/*, utils/*, constants/*, index.ts re-exports; Electron proxies; env detection
- ui: plugin + components (PromptPanelUI, OutputPanelUI, ModelManagerUI, TemplateManagerUI, HistoryDrawerUI, TextDiffUI, etc.) + composables
- web: SPA entry, conditional @vercel/analytics, Vite aliases
- desktop: main.js IPC map; auto-update; build via electron-builder
- extension: MV3 manifest + popup (Vue + UI); Vite config for background filename
- mcp-server: tools registration; per-session server for HTTP/SSE; stdio mode
- proxy/middleware: Vercel api/* + middleware.js; Docker node-proxy

## 4. Deployment

- Vercel: vercel.json (workspace build, SPA rewrite, env), middleware, edge/serverless
- Docker: multi-stage build; copy web/mcp/node-proxy; Nginx + supervisor
- Desktop: electron-builder (nsis/dmg/AppImage/zip), auto-update channels

## 5. Data Flows

- Web/Extension: UI -> core (via UI) -> LLM -> (direct or /api/proxy|/api/stream) -> stream back -> history
- Desktop: Renderer -> IPC -> core in main -> providers; stream via IPC -> persist files
- MCP: Client (e.g., Claude Desktop) -> ListTools/CallTool -> core -> SSE/stdio back

## 6. Key Design Points
- Env abstraction (utils/environment.ts): Vercel/Docker/Electron detection, proxy URL, custom model env scanning/validation
- Storage abstraction (Dexie vs File)
- Safe IPC serialization for Electron
- Streaming UX: Edge/Node proxy + LLMService + UI
- Updater and logging for Desktop

