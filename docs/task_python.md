# Prompt Optimizer Python 版本開發任務分解（task_python.md）

## 1. 開發階段規劃

### Phase 1：核心服務移植
- [ ] 依賴/環境
  - 選型落地：PySide6、OpenAI/Gemini、httpx/asyncio、SQLAlchemy/aiosqlite、cryptography
  - 建立 Poetry 或 requirements.txt + venv
- [ ] 存儲層
  - 建表/遷移腳本（models/templates/history/preferences）
  - Repository 接口與 SQLiteProvider 實現
- [ ] 業務核心
  - LLMService：統一抽象 + streaming adapter；重試/超時/取消
  - ModelManager：CRUD/啟停/健康檢查/默認參數
  - TemplateManager：CRUD/多語/導入導出
  - PromptService：optimize/iterate/test
  - HistoryManager：寫入/查詢/迭代鏈
  - PreferenceService/DataManager：偏好與全量導入導出

### Phase 2：GUI 界面開發
- [ ] 主窗口 + 分頁（提示、模板、模型、歷史、設置）
- [ ] Prompt Workflow：輸入區、模板選擇、模型選擇、流式輸出區、差異對比
- [ ] 模型管理面板：列表、編輯、測試連通
- [ ] 模板管理面板：列表、分類、編輯器、導入導出
- [ ] 歷史抽屜：鏈式視圖、搜尋/篩選、導出
- [ ] 設置面板：API Key/代理/語言/主題/自動更新偏好
- [ ] 國際化（可選）：簡中/英文切換

### Phase 3：集成測試與性能優化
- [ ] 單元測試（pytest）：core/services/utils/storage
- [ ] 集成測試：API 調用、流式渲染、數據持久化
- [ ] GUI 測試：pytest-qt 事件與交互；關鍵工作流冒煙
- [ ] 性能：啟動時間、首 token 時延、內存（profiling）
- [ ] 穩定性：錯誤處理、重試、導入回滾、資源釋放

### Phase 4：打包與發布
- [ ] PyInstaller 打包（onefile）
- [ ] 體積/啟動優化（排除冗餘、UPX 可選）
- [ ] 安裝/分發腳本（PowerShell）
- [ ] 兼容性驗證：Windows 10/11、缺省環境（無 Python）
- [ ] 文檔與發版：使用手冊、CHANGELOG、發布頁

## 2. 技術任務細分

### 2.1 依賴與環境
- [ ] 建立 pyproject.toml 或 requirements.txt
- [ ] 補充開發指令（Makefile/PowerShell）與 pre-commit（格式化/靜態檢查）

### 2.2 業務重寫
- [ ] llm_service.py：provider 工廠 + stream/generate
- [ ] model_manager.py：ModelConfig + repository + 驗證
- [ ] template_manager.py：模板 CRUD + 語言切換 + JSON 導入導出
- [ ] prompt_service.py：optimize/iterate/test + 歷史寫入
- [ ] history_manager.py：鏈式結構 + 查詢/篩選
- [ ] preference_service.py：UI/更新偏好 + 加密存/讀
- [ ] data_manager.py：全量導入導出 + schema 校驗

### 2.3 GUI 與交互
- [ ] MainWindow + QTabWidget 結構
- [ ] PromptTab：輸入/模板/模型/輸出（流式）
- [ ] TemplatesTab：列表/編輯/導入導出
- [ ] ModelsTab：列表/編輯/測連通
- [ ] HistoryTab：鏈式視圖/搜尋/導出
- [ ] SettingsTab：API Key/代理/語言/主題/更新
- [ ] 通用組件：Toast、Confirm、FilePicker、Diff Viewer

### 2.4 存儲與配置
- [ ] SQLiteProvider + schema 初始化
- [ ] JSON 匯入匯出 + 版本標記
- [ ] Key 加密（DPAPI/Fernet）與配置文件位置

### 2.5 API 集成與錯誤
- [ ] OpenAI、Gemini、兼容 OpenAI provider 工廠
- [ ] 超時/取消、HTTP 錯誤分類、重試（tenacity）
- [ ] Streaming adapter（generator/async generator）

### 2.6 打包與分發
- [ ] PyInstaller spec/命令行
- [ ] 資產打包（icon、內置模板、i18n）
- [ ] 體積優化（剔除測試/開發依賴；UPX 可選）
- [ ] 發版腳本（PowerShell + GitHub Releases）

## 3. 測試策略

### 3.1 單元測試（pytest）
- llm_service：正常/流式/錯誤/取消/重試
- model_manager：CRUD/校驗/啟停/默認
- template_manager：CRUD/導入導出/語言
- prompt_service：optimize/iterate/test + 歷史寫入
- history_manager：鏈式操作與查詢
- utils：config/crypto/schema 校驗

### 3.2 GUI 測試（pytest-qt）
- 主流程：PromptTab 交互與流式輸出更新
- 導入導出：模板/模型/歷史
- 邊界：長文本、滾動、自動複製

### 3.3 集成測試
- 模擬 provider：mock OpenAI/Gemini/兼容 API
- 數據持久化：SQLite 寫入/查詢/回滾
- 打包前冒煙：臨時構建 + 關鍵流程

### 3.4 打包測試
- Windows 10/11 虛擬機：首次啟動、運行時資源、是否缺失 VC++ 依賴
- 離線環境：無網情況下啟動、非 API 功能可用

## 4. 交付物要求

- 三份文檔（requirements_python/design_python/task_python）保持一致結構與細節。
- 代碼示例：核心類（LLM/Model/Prompt/History）與 GUI 主窗體骨架。
- 遷移對照表（TS → Python）：見設計文檔 §3。
- 打包配置：PyInstaller 命令與 spec；資產清單；發版腳本。
- 測試：pytest/pytest-qt 配置與基本用例。

