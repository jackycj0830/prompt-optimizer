# Prompt Optimizer 需求文檔

## 1. 項目概述

Prompt Optimizer 是一個多平台的 AI 提示詞優化工具，幫助用戶編寫更高質量的提示詞以提升 AI 輸出效果。項目採用 TypeScript/JavaScript monorepo 架構（pnpm 工作空間），核心能力在 `packages/core`，UI 能力在 `packages/ui`，最終形態包含 Web 應用、桌面應用（Electron）、瀏覽器擴展（Chrome MV3）以及 MCP 服務器，並提供 Docker 與 Vercel 部署方案。

## 2. 功能需求

### 2.1 核心功能

#### 2.1.1 提示詞優化
- 用戶提示詞優化：將模糊需求重寫為清晰、可執行的提示詞。
- 系統提示詞優化：構建角色/行為邏輯明確、可控的系統提示詞。
- 迭代優化：基於具體改進需求對既有提示詞做針對性升級。
- 對比測試：展示優化前/後結果差異（文本 diff、視覺對比）。
- 流式輸出：優化過程/測試支持流式 token 顯示。

#### 2.1.2 模型管理
- 多供應商支持：OpenAI、Google Gemini、DeepSeek、智譜 AI、SiliconFlow、自定義 OpenAI 兼容 API。
- 本地/自託管模型：支持 Ollama 等（通過自定義 API）。
- 高級參數：`temperature`、`max_tokens`、`top_p` 等自由配置（以 `llmParams` 形式）。
- 模型啟停與健康檢查：啟用/禁用、測試連通性、獲取模型列表。
- 環境變量掃描：通過統一規則自動掃描 `VITE_CUSTOM_API_*_suffix` 變量組。

#### 2.1.3 模板管理
- 內置模板：提供多種場景的內置優化模板。
- 自定義模板：創建、編輯、刪除、分類（用戶優化/系統優化/迭代）。
- 多語種支持：內置模板語言切換（中文/英文等）。
- 導入/導出：單個模板導出、批量數據導入/導出。

#### 2.1.4 歷史記錄
- 記錄優化歷史：包含輸入、輸出、模型、模板、時間等。
- 迭代鏈管理：同一提示詞的多輪演化追蹤（鏈式結構）。
- 搜索/篩選：按模型、時間、模板等維度檢索。
- 導出/備份：歷史數據導出備份與恢復。

#### 2.1.5 數據管理與偏好
- 全量數據導出/導入：模型、模板、歷史、偏好的一鍵導出/導入。
- 類型識別與驗證：導入前檢驗數據結構與完整性。
- 偏好設置：UI 語言、主題、更新偏好（如是否允許預發版）。

### 2.2 前端 UI 功能
- 響應式布局；主題明暗切換；多語言（i18n）。
- Markdown 渲染；代碼高亮；全屏展示。
- 一鍵複製；自動滾動；快捷鍵；拖拽導入。

## 3. 非功能需求

### 3.1 性能
- UI 交互響應：< 200ms。
- 流式顯示：長文本輸出過程平滑，不卡頓。
- 桌面應用啟動：< 5s；內存：< 500MB（常規場景）。
- 併發：支持多請求並行與合理的取消/超時處理。

### 3.2 安全
- API Key 僅保存在客戶端（Web/桌面/擴展），不經第三方中轉（除顯式選擇代理）。
- Web 部署可選密碼訪問保護（Vercel middleware + /api/auth cookie）。
- 嚴格輸入驗證與錯誤處理；避免 XSS（例如 UI 使用 DOMPurify）。
- HTTPS 部署；SSE/代理時設置 CORS 安全頭。

### 3.3 可用性與可靠性
- 多平台兼容：Windows/macOS/Linux、Chrome/Edge/Safari/Firefox（現代特性）。
- 離線可用：桌面端在無網環境可啟動與瀏覽歷史（API 調用除外）。
- 自動更新：桌面端支持 electron-updater（可選穩定/預發通道偏好）。
- 錯誤恢復：網絡錯誤可重試；導入前校驗、導入失敗回滾。

### 3.4 可維護性
- Monorepo 分層清晰（core/ui/apps/server）；強類型（TypeScript）。
- 單元/集成測試（Vitest）；>80% 目標覆蓋（核心模塊）。
- 嚴格代碼規範、統一版本同步腳本（scripts/sync-versions.js）。
- 完整開發/部署/使用文檔。

## 4. 技術需求

### 4.1 平台與部署
- Web：Vercel（Edge Functions + Middleware + SPA rewrite）或任意靜態服務器。
- Docker：Nginx 靜態站點 + MCP HTTP 服務 + Node 代理（支援 SSE）。
- 桌面：Electron（electron-builder 打包，多平台發行）。
- 擴展：Chrome MV3（Vite 構建，public/manifest.json）。

### 4.2 API 與協議
- OpenAI SDK、Google Generative AI SDK 等；自定義 OpenAI 兼容端點。
- MCP（Model Context Protocol）：工具集（optimize-user-prompt / optimize-system-prompt / iterate-prompt）通過 stdio 或 HTTP 提供。
- SSE：支持流式內容（api/stream.js、node-proxy、LLMService 流式回調）。

### 4.3 數據存儲
- 瀏覽器：IndexedDB（Dexie）/ localStorage。
- 桌面：文件型存儲（FileStorageProvider，userData 目錄）。
- 數據導入導出：JSON（含結構與版本字段，導入前驗證）。

## 5. 用戶需求

### 5.1 個人用戶
- 場景：日常對話、創作靈感、學習研究。
- 需求：易用界面、快速優化、多模型選擇、歷史管理。
- 偏好：桌面或擴展快速呼出；Web 在線即可用。

### 5.2 開發者
- 場景：系統提示詞設計、API 調用優化、批量/流程化處理。
- 需求：高級參數、模板化、可導出、MCP 集成到工具鏈。
- 偏好：Web + MCP；可自建代理以繞過 CORS。

### 5.3 企業/團隊
- 場景：私有部署、權限控制、定制化。
- 需求：Docker/內網部署、訪問密碼、可審計的歷史與導出。
- 偏好：Docker（含 MCP）、自定義模型端點。

### 5.4 研究人員
- 場景：提示詞工程研究、跨模型對比、實驗追蹤。
- 需求：詳盡歷史、鏈式迭代、差異對比、數據導出。

## 6. 約束與依賴

- 前端：Vue 3 + Vite + TypeScript；UI 組件庫（Element Plus）、Tailwind（web/extension）。
- 後端/服務：MCP（Express + MCP SDK）、Vercel Edge/Serverless；無中心化業務後端。
- 代理：Vercel api/proxy.js、api/stream.js；Docker 下 node-proxy（localhost→host.docker.internal 自動映射）。
- 受限條件：CORS/混合內容限制、第三方 API 可用性與限流。

## 7. 驗收標準

- 功能：提示詞優化/模板/模型/歷史/數據導入導出/偏好完整可用。
- 兼容：Web/桌面/擴展/MCP 均可運行；主流瀏覽器兼容。
- 性能：啟動/響應/流式體驗達標；內存、CPU 在合理區間。
- 安全：API Key 不泄露；訪問控制有效；輸入輸出安全。
- 部署：Vercel 一鍵可用；Docker 健康檢查通過；桌面可自動更新。
