## 需求文檔（requirements.md）

### 1. 功能需求

- 提示詞優化（Prompt Optimization）
  - 支持兩類優化：
    - 系統提示詞優化（system）：優化 AI 角色、行為規則與約束
    - 用戶提示詞優化（user）：優化任務描述與上下文表達
  - 迭代優化（iterate）：在已有提示詞上，基於具體「改進需求」進行定向迭代（保持核心意圖）
  - 流式回傳：支持流式/SSE 回傳過程，前端實時展示（api/stream.js）
  - MCP 工具（packages/mcp-server）：
    - optimize-user-prompt
    - optimize-system-prompt
    - iterate-prompt

- 模型管理（Model Manager）
  - 內建/支持供應商：OpenAI、Google Gemini、DeepSeek、Zhipu（智譜）、SiliconFlow、自定義 OpenAI 兼容 API
  - 模型配置：API Key、Base URL、自定義模型名、高級參數（llmParams）
  - 多組自定義模型環境變量掃描與校驗：VITE_CUSTOM_API_KEY_XXX / _BASE_URL_XXX / _MODEL_XXX（核心在 core/utils/environment.ts）
  - 能力：新增、更新、刪除、導入/導出、驗證、初始化狀態檢查、獲取已啟用與全部模型

- 模板管理（Template Manager）
  - 內置提示詞模板，多語言支持與語言切換（TemplateLanguageService）
  - CRUD：創建/讀取/更新/刪除
  - 類型化列出（listTemplatesByType）、導入/導出單個/批量數據、模板校驗

- 歷史記錄（History Manager）
  - 記錄優化/測試行為，支持「迭代鏈」管理與查詢
  - 增/刪/清空/查詢/導入/導出/校驗

- 偏好設置（Preference Service）
  - 通用應用設置（如更新通道、忽略版本），提供導入/導出/校驗

- 數據管理（Data Manager）
  - 聚合一鍵導出/導入所有業務數據（模型、模板、歷史、偏好）

- 測試與對比
  - 提示詞測試（testPrompt）：系統+用戶提示詞對指定模型的效果測試
  - 對比展示：原始/優化內容對照、文本差異（UI 組件 TextDiff）

- UI 與國際化
  - @prompt-optimizer/ui：基於 Vue 3 + Element Plus 的組件與 i18n 插件（installI18n / installI18nOnly）
  - 現有中/英文；可擴展更多語言

- 平台形態
  - Web SPA（packages/web）
  - 桌面應用 Electron（packages/desktop）
  - 瀏覽器擴展 Chrome MV3（packages/extension）
  - MCP 服務（packages/mcp-server，HTTP/stdio）

- 代理與訪問控制
  - Vercel Edge 代理：/api/proxy（普通）、/api/stream（SSE）
  - Docker 代理：node-proxy（容器內訪問宿主機、本地模型）
  - Vercel 密碼保護：middleware.js + /api/auth（HttpOnly Cookie）

### 2. 非功能需求

- 性能
  - 流式回傳降低感知延遲；代理層對流式/非流式設不同超時（STREAM_TIMEOUT=300s，PROXY_TIMEOUT=120s）
  - Docker 健康檢查同時探測 Web 首頁與 /mcp

- 安全性
  - Vercel 訪問密碼（ACCESS_PASSWORD）；嚴格 Cookie 屬性（HttpOnly、SameSite=Strict、prod 下 Secure）
  - Electron 主進程安全策略：contextIsolation=true、nodeIntegration=false；外部 URL 協議白名單
  - 代理設置 CORS，Edge 函數顯式設置允許頭
  - 數據只在客戶端本地存儲（瀏覽器 IndexedDB/LocalStorage；桌面本地文件）

- 可用性/穩定性
  - Electron 自動更新（electron-updater），支持忽略版本與詳細日誌
  - 退出/關閉前嘗試保存（flush）且設應急退出計時，避免卡死
  - 代理、MCP 服務具備詳細日誌與錯誤輸出

### 3. 技術需求

- 支持平台與部署
  - Web（Vercel/Nginx 靜態）
  - Docker（Nginx + Node 多進程）
  - 桌面（Electron：Win/Mac/Linux）
  - 瀏覽器擴展（Chrome MV3）
  - MCP（HTTP/stdio）

- 開發/運行環境
  - Node：^18 || ^20 || ^22；包管理：pnpm
  - 前端：Vue 3、Vite、Vitest
  - MCP：Express + @modelcontextprotocol/sdk
  - 桌面：Electron 37 + electron-builder
  - 存儲：Dexie（瀏覽器 IndexedDB）、FileStorageProvider（桌面）

- API 集成
  - openai、@google/generative-ai SDK
  - 自定義 OpenAI 兼容 API（可配置 Base URL/Model/Key）
  - 多自定義模型環境變量命名規則與驗證（core/utils/environment.ts）

### 4. 用戶需求

- 一般用戶
  - 在 Web/桌面/擴展中輸入需求並獲得優化提示詞；可選模板；實時查看流式輸出；查看歷史

- 高級用戶/工程師
  - 連接內部/本地模型（Ollama/代理）；批量導入/導出模型、模板、歷史；使用 MCP 將能力集成到其他 AI 客戶端

- 運維/部署人員
  - 一鍵部署（Vercel/Docker），配置訪問密碼與 API Key，監控健康檢查

- 桌面重度用戶
  - 無 CORS 限制直連本地/內網 API；自動更新；可視化日誌查看/清理

