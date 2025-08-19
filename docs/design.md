## 設計文檔（design.md）

### 1. 系統架構設計

- Monorepo（pnpm workspaces）
  - packages/core：核心業務與服務；與框架/平臺無關
  - packages/ui：Vue 3 組件庫 + i18n 插件
  - packages/web：Web SPA（Vite）
  - packages/desktop：Electron 桌面應用（主進程 + web-dist 渲染）
  - packages/extension：Chrome MV3 擴展（Vite 構建）
  - packages/mcp-server：MCP Server（HTTP/stdio）
  - node-proxy：Docker 場景下的 Node 代理
  - api/：Vercel Edge/Serverless 函數
  - middleware.js：Vercel 中間件（訪問密碼保護）

- 包依賴關係
  - core → 被 ui、desktop、web/extension、mcp-server 使用
  - ui → 被 web 與 extension 使用（desktop 渲染端也載入 web-dist）
  - mcp-server → 使用 core 封裝工具
  - api/node-proxy → 與核心解耦，作為部署/網絡輔助層

- 服務分層
  - Core 層：LLMService/Model/Template/History/Preference/Data 等服務
  - UI 層：組件 + composables（調用 core）
  - 平台層：desktop（IPC + FileStorage）、mcp-server（MCP 協議）、Vercel（middleware + api）、Docker（nginx + node）

### 2. 技術架構

- 前端
  - Vue 3、Element Plus、Tailwind（web/extension）；Vite 構建
  - i18n 插件（installI18n / installI18nOnly）
  - Vitest 單測

- 後端/服務
  - MCP：Express + @modelcontextprotocol/sdk；工具：optimize-user/system、iterate
  - Vercel Edge：/api/proxy（普通）、/api/stream（SSE）、/api/auth、/api/vercel-status
  - Docker：Nginx 靜態、Node（MCP + node-proxy）

- 數據存儲
  - 瀏覽器端：Dexie（IndexedDB）、LocalStorage（部分）
  - 桌面端：FileStorageProvider（用戶目錄 userData）
  - 統一抽象：StorageFactory + Providers

### 3. 模塊設計（各包職責）

- core
  - services/llm：消息/流式接口、模型列表拉取、錯誤
  - services/model：ModelManager、默認與進階參數、驗證、Electron 配置
  - services/template：TemplateManager、TemplateLanguageService、多語模板、靜態加載、Electron 代理
  - services/history：HistoryManager、迭代鏈管理、Electron 代理
  - services/prompt：optimize/iterate/test、流式版本、Electron 代理
  - services/storage：StorageFactory、Dexie/Local/Memory/File Provider
  - services/preference：PreferenceService、Electron 代理
  - services/data：聚合導出/導入
  - utils：environment（Vercel/Docker/Electron 檢測、代理 URL、env 掃描/校驗）、ipc-serialization
  - constants：storage-keys
  - index.ts：集中導出工廠、代理、工具、類型

- ui
  - plugins/i18n、components（MainLayout、PromptPanel、OutputPanel/Display、Template/Model 管理、HistoryDrawer、TextDiff、Updater 等）
  - composables：usePromptOptimizer/useModelManager/useTemplateManager/useHistoryManager/usePreferenceManager/useUpdater 等

- web
  - SPA 入口 main.ts；按 VITE_VERCEL_DEPLOYMENT 動態載入 @vercel/analytics；Vite 別名/環境變量配置

- desktop
  - 主進程 main.js：初始化 FileStorageProvider；創建 core 服務；映射大量 IPC；自動更新；退出前 flush
  - 構建：electron-builder（多平臺 targets、發布到 GitHub Releases）

- extension
  - MV3 manifest（public/manifest.json）；popup 應用（Vue + UI）；Vite 打包配置

- mcp-server
  - MCP Server 啟動（stdio/HTTP）；工具列表與調用處理器；每會話獨立 server 實例；SSE 事件流

- 代理與中間件
  - api/proxy、api/stream：CORS/SSE 支持、錯誤處理
  - api/auth：設置/清除 vercel_access_token Cookie
  - middleware.js：未認證返回內嵌認證頁
  - node-proxy：容器內代理（自動將 localhost → host.docker.internal）

### 4. 部署架構

- Vercel
  - vercel.json：工作區構建；/api/* 直通；其餘重寫到 /index.html；設 VITE_VERCEL_DEPLOYMENT
  - middleware.js：ACCESS_PASSWORD 密碼保護；/api/auth 完成驗證

- Docker
  - Dockerfile：多階段構建；複製 web dist、mcp dist、node-proxy；Nginx + supervisor 啟動多進程
  - docker-compose.yml：暴露 8081→80；健康檢查 / 與 /mcp；配置 API Keys、MCP 供應商、NGINX_PORT

- 桌面（Electron）
  - electron-builder：打包 Win/Mac/Linux；自動更新（公開倉庫）

### 5. 數據流設計

- Web 流程
  1) 使用者在 UI 提交請求 → composables 調用 core Prompt/LLM
  2) 直連（CORS OK）或經 /api/proxy、/api/stream 代理（CORS/SSE）
  3) 流式返回即時渲染；歷史/模板/偏好存 Dexie/LocalStorage

- 桌面流程
  1) Renderer UI → IPC → 主進程 core 服務（FileStorageProvider）
  2) 主進程直連供應商 API（無 CORS）；流式經 IPC 推送到 Renderer
  3) 本地文件持久化

- MCP 流程
  1) 客戶端（如 Claude Desktop）→ MCP 工具（HTTP/stdio）
  2) mcp-server 內調用 core；按會話回傳結果（HTTP/SSE 或 stdio）

- Docker/代理
  - node-proxy 修正 localhost；提供 CORS/超時/錯誤處理；Nginx 反向代理靜態與 /mcp

