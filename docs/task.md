## 任務分解文檔（task.md）

### 1. 開發任務

- P0 核心與可用性
  - core
    - LLMService：
      - 供應商接入一致化（OpenAI/Gemini/DeepSeek/Zhipu/SiliconFlow/自定義兼容）
      - 超時/重試/錯誤封裝；流式回調（onToken/onReasoningToken/onComplete/onError）
      - 模型列表拉取與結構統一
    - environment：
      - Vercel/Docker/Electron 檢測；代理 URL；Vercel/Docker 狀態探測
      - 多自定義模型環境變量掃描與校驗（CUSTOM_API_PATTERN、SUFFIX_PATTERN、MAX_SUFFIX_LENGTH）
    - StorageProviders：Dexie/Local/Memory/File 的行為一致性、flush 機制
    - Prompt/Template/History/Preference/Data 服務：CRUD、導入/導出/驗證與類型完善
  - ui
    - i18n 插件安裝流程（installI18n/Only、initializeI18nWithStorage）
    - PromptPanel/OutputPanel/TemplateManager/ModelManager/HistoryDrawer/Updater 組件打磨
    - 流式渲染與錯誤處理、文案與空狀態
  - web
    - 入口集成 UI 與 i18n；VITE_VERCEL_DEPLOYMENT 下的 @vercel/analytics
    - 直連/代理選擇與狀態提示；Vite 別名與 env 加載
  - desktop
    - 主進程：
      - FileStorageProvider 初始化與 core 服務構建
      - IPC handlers 完整映射（模型/模板/歷史/偏好/Prompt/LLM/流式）
      - 自動更新（檢查/下載/安裝/忽略版本）與日誌；關閉/退出前 flush 與應急退出
    - 渲染端：加載 web-dist、與 IPC 通道聯調
  - mcp-server
    - 工具列表（ListTools）與工具調用（CallTool）處理器
    - HTTP 會話管理（SSE 雙通道）與 stdio 模式
    - 參數驗證與錯誤輸出
  - 代理與中間件
    - api/proxy、api/stream：CORS、SSE、錯誤與狀態碼
    - api/auth + middleware.js：ACCESS_PASSWORD 登入/登出流程與 Cookie 設置校驗

- P1 體驗與生態
  - 模板語言切換體驗與自定義語言包
  - 高級 LLM 參數（llmParams）可視化與供應商映射
  - 歷史迭代鏈 UI 與文本差異對比
  - MCP 文檔與示例完善

- P2 生產優化
  - 更完善的日誌（前端開發模式、桌面專屬面板）
  - 代理多上游/故障轉移策略
  - 領域化模板預設與場景化向導

### 2. 測試任務

- 單元測試（Vitest）
  - core：LLMService/ModelManager/TemplateManager/PromptService/HistoryManager/PreferenceService/DataManager
  - utils：environment、ipc-serialization、storage providers 行為
  - ui：composables 與關鍵組件（jsdom 測基礎交互）
  - mcp-server：工具 handler 單測（參數缺失/非法、模型未啟用等）

- 集成測試
  - web + api/proxy：模擬上游，驗證非流式/流式（SSE）
  - desktop：最小化啟動，IPC → core 回路、關閉/退出時 flush 路徑
  - mcp-server：HTTP 端到端（Express + MCP SDK）

- 端到端（E2E）
  - Web：從輸入到優化、流式展示、歷史寫入的完整路徑
  - Docker：容器啟動後 / 與 /mcp 健康；通過 node-proxy 訪問本地模型
  - MCP：用腳本/工具以 HTTP/stdio 調用三個工具，校驗結果

- 性能與可靠性
  - 流式首字延遲、吞吐；超時/中斷/重試
  - Electron 關閉/退出 flush 成功率與耗時

### 3. 部署任務

- Vercel
  - 設置環境變量：ACCESS_PASSWORD、VITE_*_API_KEY、VITE_VERCEL_DEPLOYMENT
  - 驗證 middleware 密碼保護、/api/* 行為、SPA 重寫
  - 代理流式端點在主要供應商的兼容性驗證

- Docker
  - 構建/推送鏡像；或使用 linshen/prompt-optimizer:latest
  - docker-compose.yml：端口/環境變量/健康檢查校驗
  - node-proxy 與宿主本地模型（Ollama）互通驗證

- 桌面（Electron）
  - electron-builder 打包與 GitHub Releases 發佈
  - 自動更新全流程測試（含忽略版本、預發版）
  - 圖標/簽名（視情況）與日誌路徑檢視

- MCP 服務
  - Docker 中 /mcp 暴露；Claude Desktop services.json 示例校驗
  - （可選）npm 發佈 @prompt-optimizer/mcp-server

### 4. 文檔任務

- 用戶文檔
  - 快速開始、部署（Vercel/Docker/桌面/擴展）
  - MCP 使用指南與外部客戶端集成示例
  - FAQ：CORS、混合內容、代理策略與常見供應商注意事項

- 開發者文檔
  - 系統架構與模塊說明（requirements/design/task 對應）
  - 新供應商接入與 LLMService 擴展點
  - 測試/調試指南（Vitest/E2E/代理調試）
  - 版本同步：scripts/sync-versions.js 與需同步文件清單

- 維護運營
  - 發佈流程、CHANGELOG、擴展/桌面版本同步
  - 監控與日誌（桌面端查看/清理、MCP/代理服務日誌級別）
  - 安全檢查清單（Vercel Cookie、安全 Header、Electron 安全）

