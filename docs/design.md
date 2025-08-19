# Prompt Optimizer 設計文檔

## 1. 系統架構設計

### 1.1 Monorepo 與分層
- 工作空間：pnpm + `pnpm-workspace.yaml`，所有包位於 `packages/*`。
- 分層結構：
  - Core（packages/core）：純業務核心（模型、提示詞、模板、歷史、偏好、存儲抽象、環境檢測、IPC 序列化工具等）。
  - UI（packages/ui）：Vue 組件庫與 i18n 插件，抽象可復用的界面與交互能力。
  - Apps：Web（packages/web）、Desktop（packages/desktop）、Extension（packages/extension）。
  - Server：MCP Server（packages/mcp-server），以 HTTP 或 stdio 暴露工具能力。
  - Infra：Vercel middleware + Edge Functions（api/*），Docker + Nginx + Node 代理。

### 1.2 包依賴關係
- `@prompt-optimizer/ui` 依賴 `@prompt-optimizer/core`。
- Web/Extension 依賴 `@prompt-optimizer/ui`（間接使用 core）。
- Desktop 直接依賴 `@prompt-optimizer/core`（主進程）並載入 web 打包產物作為渲染進程 UI。
- MCP Server 依賴 `@prompt-optimizer/core` 用於提示詞處理、模型/模板管理等。

### 1.3 服務分層（以 core 為中心）
- LLMService：統一對接不同模型供應商（OpenAI/Gemini/DeepSeek/智譜/SiliconFlow/自定義）。
- ModelManager：模型配置、啟停、校驗、初始化、導入/導出。
- TemplateManager & TemplateLanguageService：模板 CRUD、語言切換、導入/導出、類型化列表。
- PromptService：優化、迭代、測試；支持流式處理回調。
- HistoryManager：行為記錄與迭代鏈管理、導入/導出。
- PreferenceService：應用偏好（更新通道/忽略版本等）。
- DataManager：聚合導入/導出全量數據。
- Storage 抽象：DexieStorageProvider（瀏覽器 IndexedDB）、FileStorageProvider（桌面）、LocalStorage、Memory。
- Environment/IPC：環境判斷（Electron/Vercel/Docker/Browser）與安全序列化。

## 2. 技術架構

### 2.1 前端
- 框架：Vue 3 + TypeScript；Vite 構建；Vitest 單元/組件測試。
- UI：Element Plus、Tailwind（web/extension）；Markdown-it、highlight.js、DOMPurify。
- i18n：`installI18n` / `installI18nOnly`，支持延遲初始化與存儲持久化語言設置。

### 2.2 後端/服務
- MCP Server：Express + `@modelcontextprotocol/sdk`，提供三個工具（optimize-user/system、iterate），支持 stdio/HTTP；HTTP 模式使用 `StreamableHTTPServerTransport` 並帶會話管理（SSE）。
- Vercel：
  - middleware.js：訪問密碼保護（ACCESS_PASSWORD）→ 認證頁 → /api/auth 設置 HttpOnly cookie。
  - api/proxy.js：通用代理（CORS、安全 header 過濾）。
  - api/stream.js：流式代理（SSE），採用 TransformStream 逐塊轉發。
  - api/vercel-status.js：運行狀態探測。
- Docker：Nginx 提供靜態站點；`node-proxy`（HTTP 代理、SSE、localhost → host.docker.internal 映射、超時/錯誤分類、日誌）。
- Desktop：Electron 主進程 `main.js` 建構 core 服務與 IPC 處理器，渲染進程載入 web 構建產物或 dev server；electron-updater 自動更新。

### 2.3 數據存儲方案
- 瀏覽器：Dexie（IndexedDB）保存模型、模板、歷史、偏好；LocalStorage 保存輕量設置。
- 桌面：文件型存儲（userData 目錄）由 `FileStorageProvider` 管理，關閉/退出時 flush，帶超時與應急退出機制。
- 導入/導出：JSON；導入前由 zod/內部校驗器驗證結構、版本、類型。

## 3. 模塊設計（各包職責）

### 3.1 @prompt-optimizer/core
- 入口：`src/index.ts` 統一導出工廠、類、類型、工具。
- 功能域：model、llm、prompt、template、history、preference、data、storage、utils。
- 特色：Electron 代理（Electron*Proxy 類）隔離 IPC；環境檢測（isVercel/isDocker/isBrowser 等）。

### 3.2 @prompt-optimizer/ui
- 導出 UI 組件：PromptPanelUI、OutputPanelUI、ModelManagerUI、TemplateManagerUI、HistoryDrawerUI、OptimizationModeSelectorUI、TextDiffUI 等。
- 插件：i18n 安裝與初始化；Composable：usePromptOptimizer/useModelManager/useTemplateManager/useHistoryManager/usePreferenceManager/useUpdater 等。
- 從 core 透出必要工廠與類型，方便應用直接使用。

### 3.3 @prompt-optimizer/web
- SPA 應用入口（src/main.ts），載入 UI 組件/樣式，Vercel 環境動態載入 Analytics。
- Vite 別名與 preserveSymlinks 以支持本地 workspace 依賴熱更；服務端口 18181。

### 3.4 @prompt-optimizer/desktop
- Electron 主進程（main.js）：構建 core 服務、註冊大量 IPC channel（prompt-*, model-*, template-*, history-*, data-*, config-*、logs-*、更新相關）。
- 應用窗口載入 web-dist（生產）或本地 Vite（開發）。
- 自動更新：electron-updater，忽略版本偏好與詳細日誌。

### 3.5 @prompt-optimizer/extension
- Chrome MV3：public/manifest.json，src/main.ts 挂載 Vue UI；Vite 針對 MV3 打包（背景腳本文件名處理）。

### 3.6 @prompt-optimizer/mcp-server
- src/index.ts：創建 Server → 註冊工具 → 調用 core 服務；支持 HTTP(Express)/stdio 兩種傳輸。
- 會話管理：HTTP 模式下以 SSE 通知與 sessionId 管理跨請求鏈接。

## 4. 部署架構

### 4.1 Vercel
- vercel.json：強制安裝 @vercel/analytics（workspace）、輸出目錄 `packages/web/dist`、rewrite 到 index.html。
- middleware.js：訪問控制；api/* 維持原路由；其餘走 SPA。
- api/*：Edge/Serverless；SSE 需使用 Edge（stream.js）。

### 4.2 Docker
- Dockerfile：多階段構建（pnpm build + mcp:build）→ Nginx + Supervisor 啟動腳本（/start-services.sh）。
- docker-compose.yml：映射 8081→80；探活首頁與 /mcp；環境變量注入（模型 Key、MCP 默認 provider、訪問密碼）。
- 节点代理：`node-proxy` 提供 /api/proxy /api/stream 等透傳，並處理宿主機訪問與 SSE。

### 4.3 桌面應用
- electron-builder 配置：多平台目標（nsis/dmg/AppImage/zip）；自動更新通道。
- 開發：`pnpm run dev:desktop`（同時啟本地 web + 桌面應用）。

## 5. 數據流設計

### 5.1 Web/Extension 端到端流程
1) 用戶在 UI（PromptPanelUI/ModelSelectUI/TemplateSelectUI）中設置模型、模板與內容。
2) UI 通過 core（直接或經 UI re-export）創建/使用 ModelManager、TemplateManager、PromptService。
3) 需要代理時：請求走 `/api/proxy` 或 `/api/stream`（SSE）。
4) LLMService 將請求發送至選定模型（OpenAI/Gemini/自定義等），接受流式回調並更新 UI。
5) 結果寫入 HistoryManager，必要時更新迭代鏈。

### 5.2 桌面端流程
1) 主進程啟動時創建 FileStorageProvider、初始化 Model/Template/History/Preference/Data 等服務。
2) 渲染進程載入 web 構建產物；前端通過 IPC 調用主進程各類 handler（如 `prompt-optimizePromptStream`）。
3) 主進程使用 core 的 PromptService/LLMService 與外部 API 交互，流式回調通過 IPC 推送給渲染進程。
4) 關閉窗口/退出時 flush 本地文件存儲，設超時與應急退出保證可靠性。

### 5.3 MCP Server 流程
1) 客戶端（如 Claude Desktop）請求工具列表 → `ListTools` 返回三個工具。
2) `CallTool` 時校驗參數 → 讀取模板與默認 ID → 調用 PromptService 產生結果 → 返回純文本。
3) HTTP 模式採用 `StreamableHTTPServerTransport` + SSE 維持會話；stdio 模式直連標準輸入輸出。

## 6. 關鍵設計要點
- 環境抽象與可移植性：`utils/environment.ts` 定義 Electron/Vercel/Docker/Browser 判斷、代理 URL、環境變量掃描與驗證（含自定義多模型）。
- 儲存抽象：StorageProvider 切換（Dexie vs FileStorage），確保不同環境數據一致性。
- IPC 與序列化：`utils/ipc-serialization.ts` + Desktop `safeSerialize`，避免 Vue 響應式對象穿越 IPC。
- 流式體驗：Edge/Node 代理、LLMService 流式回調、UI 實時渲染，確保長輸出與大文本體驗。
- 自動更新與日誌：桌面端詳盡的 updater 事件、偏好選項、日誌導出，提升可維護性與可觀測性。

