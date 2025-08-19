# Prompt Optimizer Task Breakdown

## 1. Development Tasks (by module and priority)

### P0 (Must)
- Core
  - [ ] LLMService: test coverage for OpenAI/Gemini/DeepSeek/Zhipu/SiliconFlow/custom APIs incl. streaming
  - [ ] ModelManager: env scanning/validation (multi-custom models) and default init edge cases
  - [ ] PromptService: unify optimize/iterate/test streaming & non-streaming paths with tests
  - [ ] TemplateManager: language switch, CRUD, import/export and validation
  - [ ] HistoryManager: chain ops (createNewChain/addIteration/getChain/getAllChains) coverage
  - [ ] PreferenceService: ignored versions/prerelease channel persistence + import/export validation

- UI/Web
  - [ ] i18n init & switching (installI18n/Only)
  - [ ] Core UI flow components: PromptPanelUI/OutputPanelUI/ModelManagerUI/TemplateManagerUI/HistoryDrawerUI interaction tests
  - [ ] TextDiffUI/MarkdownRenderer edge cases (long text, code highlight)
  - [ ] Conditional @vercel/analytics on Vercel

- Desktop
  - [ ] Main IPC handlers coverage: prompt-*/model-*/template-*/history-*/data-*/config-*/logs-*/updater
  - [ ] FileStorageProvider flush timeout/emergency exit behavior
  - [ ] Updater channel switching and ignored versions

- MCP Server
  - [ ] ListTools/CallTool path and ParameterValidator coverage
  - [ ] HTTP session/SSE correctness and resource cleanup

- Infra/Proxy
  - [ ] Vercel middleware + /api/auth end-to-end
  - [ ] api/proxy and api/stream (SSE) against providers
  - [ ] node-proxy localhost mapping and timeout/error classes

### P1 (Should)
- Core
  - [ ] llmParams mapping per SDK hardened
  - [ ] DataManager extreme size handling and rollback

- UI/Web/Extension
  - [ ] Hotkeys, drag&drop, fullscreen consistency
  - [ ] MV3 background filename output and manifest sync

- Desktop
  - [ ] External links whitelist and UX

- MCP
  - [ ] Template defaults/switching behavior within tools

### P2 (Could)
- [ ] Finer telemetry/logging
- [ ] Proxy allowlist/throttling

## 2. Testing Tasks

### 2.1 Unit (Vitest)
- core
  - [ ] services/llm: messages, streaming, errors, model list
  - [ ] services/model: validate/init/CRUD/import-export
  - [ ] services/template: lang switch/CRUD/import-export
  - [ ] services/prompt: optimize/iterate/test (incl. streaming handlers)
  - [ ] services/history: chain ops & queries
  - [ ] utils/environment: env detection, proxy URL, custom env scanning/validation

### 2.2 Component/Integration
- ui/web
  - [ ] i18n plugin rendering (jsdom)
  - [ ] PromptPanelUI→PromptService→LLMService→OutputDisplay
  - [ ] node-proxy + api/stream mocked streaming rendering

### 2.3 E2E
- [ ] Web: run Vite or static build, verify optimize→history→export/import
- [ ] Desktop: start app, verify IPC calls and updater dialog/ignored versions
- [ ] MCP: HTTP mode tools and SSE stream with lightweight client

## 3. Deployment Tasks

### 3.1 Vercel
- [ ] Verify vercel.json (build/install, rewrite, VITE_VERCEL_DEPLOYMENT)
- [ ] Set ACCESS_PASSWORD and VITE_* API keys as needed
- [ ] Validate /api/proxy /api/stream /api/auth /api/vercel-status

### 3.2 Docker
- [ ] Build image (multi-stage Dockerfile) and run docker-compose.yml
- [ ] Validate / and /mcp healthchecks; node-proxy accessing local models
- [ ] Set VITE_*/MCP_*/ACCESS_* envs

### 3.3 Desktop
- [ ] electron-builder for Win/Mac/Linux; publish to Releases
- [ ] Auto-update end-to-end for stable/prerelease; logs and ignored versions

### 3.4 Extension
- [ ] Validate Vite outputs (background.js naming aligns with manifest)
- [ ] Chrome Web Store assets and version sync (scripts/sync-versions.js)

## 4. Documentation Tasks
- [ ] User docs: Getting started; Vercel/Docker/Desktop/Extension; MCP usage
- [ ] Dev docs: architecture, core services API, IPC channels, proxy/deploy guides
- [ ] Test docs: how to run unit/integration/E2E
- [ ] Release docs: version sync script; desktop packaging & publish; extension checklist

