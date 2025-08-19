# Prompt Optimizer 任務分解文檔

## 1. 開發任務（按模塊與優先級）

### P0（必須）
- Core
  - [ ] LLMService：覆蓋 OpenAI/Gemini/DeepSeek/智譜/SiliconFlow/自定義 API 的消息與流式接口測試用例補齊
  - [ ] ModelManager：環境變量掃描/驗證（多自定義模型）與默認模型初始化的邊界測試
  - [ ] PromptService：optimize/iterate/test 流式與非流式路徑整合測試
  - [ ] TemplateManager：多語模板切換、CRUD、導入/導出與校驗測試
  - [ ] HistoryManager：迭代鏈（createNewChain/addIteration/getChain/getAllChains）完整覆蓋
  - [ ] PreferenceService：忽略版本/預發通道等偏好持久化與導入/導出驗證

- UI/Web
  - [ ] i18n 初始化與語言切換（installI18n/Only）
  - [ ] 主流程組件：PromptPanelUI/OutputPanelUI/ModelManagerUI/TemplateManagerUI/HistoryDrawerUI 互動測試
  - [ ] TextDiffUI、MarkdownRenderer 邊界案例（超長文本、代碼高亮）
  - [ ] Vercel 環境下 Analytics 條件加載驗證

- Desktop
  - [ ] 主進程 IPC handlers 覆蓋：prompt-*/model-*/template-*/history-*/data-*/config-*/logs-*/更新相關
  - [ ] FileStorageProvider flush 超時/應急退出機制驗證
  - [ ] 自動更新通道切換與忽略版本偏好

- MCP Server
  - [ ] ListTools/CallTool 流程與參數驗證（ParameterValidator）
  - [ ] HTTP 模式 session/SSE 正常工作與資源清理

- Infra/代理
  - [ ] Vercel middleware + /api/auth 密碼保護全鏈路
  - [ ] api/proxy 與 api/stream（SSE）在多供應商 API 下的兼容性
  - [ ] node-proxy 本地/容器跨網訪問與超時/錯誤分類

### P1（應該）
- Core
  - [ ] LLM 高級參數（llmParams）對不同 SDK 的映射測試加固
  - [ ] DataManager 全量導入/導出極端體量與回滾策略

- UI/Web/Extension
  - [ ] 快捷鍵、拖拽導入、全屏模式等交互一致性
  - [ ] 擴展構建（MV3 背景腳本輸出名）與 manifest 欄位同步

- Desktop
  - [ ] 外部鏈接安全白名單與錯誤提示體驗

- MCP
  - [ ] 多模板/默認模板切換在工具內的行為一致性

### P2（可以）
- [ ] 更細粒度的遙測/日誌（可選）
- [ ] 代理白名單與節流策略（可選）

## 2. 測試任務

### 2.1 單元測試（Vitest）
- core
  - [ ] services/llm：消息、流式、錯誤處理、模型列表
  - [ ] services/model：校驗/初始化/CRUD/導入導出
  - [ ] services/template：語言切換/CRUD/導入導出
  - [ ] services/prompt：optimize/iterate/test（含流式 handler）
  - [ ] services/history：鏈式操作與查詢
  - [ ] utils/environment：環境檢測、代理 URL、env 掃描與校驗

### 2.2 組件/集成測試
- ui/web
  - [ ] i18n 插件與組件渲染（jsdom）
  - [ ] 主流程組件交互：PromptPanelUI→PromptService→LLMService→OutputDisplay
  - [ ] node-proxy 與 api/stream 的流式回傳渲染（mock）

### 2.3 端到端（E2E）
- [ ] Web：啟動 Vite（或使用打包後靜態），驗證提示詞優化→歷史→導入導出
- [ ] Desktop：啟動應用，驗證 IPC 調用與自動更新對話框/忽略版本
- [ ] MCP：HTTP 模式下工具列表/調用與 SSE 事件流（可用輕量 HTTP 客戶端）

## 3. 部署任務

### 3.1 Vercel
- [ ] 檢查 vercel.json（build/install 命令、rewrite、環境變量 VITE_VERCEL_DEPLOYMENT）
- [ ] 設置 ACCESS_PASSWORD（如需）與 API Key（VITE_*）
- [ ] 驗證 /api/proxy /api/stream /api/auth /api/vercel-status

### 3.2 Docker
- [ ] 構建鏡像（Dockerfile 多階段）並運行 docker-compose.yml
- [ ] 驗證首頁與 /mcp 健康檢查；node-proxy 訪問本地模型
- [ ] 根據環境設置 VITE_*、MCP_*、ACCESS_* 變量

### 3.3 桌面
- [ ] electron-builder 打包（Win/Mac/Linux）；GitHub Releases 發布
- [ ] 自動更新測試（stable/prerelease）、日誌定位與版本忽略

### 3.4 擴展
- [ ] Vite 構建輸出校驗（background.js 命名與 manifest 匹配）
- [ ] Chrome Web Store 上架資料與版本同步（scripts/sync-versions.js）

## 4. 文檔任務
- [ ] 使用者文檔：快速開始、Vercel/Docker/桌面/擴展安裝、MCP 使用
- [ ] 開發者文檔：技術架構、核心服務 API、IPC 渠道一覽、代理與部署指南
- [ ] 測試文檔：如何運行單元/集成/E2E 測試
- [ ] 發布流程：版本同步腳本、桌面打包與發布、擴展上架清單

