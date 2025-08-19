# Prompt Optimizer Python 版本設計文檔（design_python.md）

## 1. 架構重新設計

### 1.1 從 Monorepo 到單體應用
- 現狀：TS Monorepo（core/ui/web/desktop/extension/mcp-server）
- 目標：Python 單體桌面應用，結構清晰、可打包。

建議目錄：
```
po_app/
  core/          # 業務核心：llm、model、template、prompt、history、preference、data
  ui/            # PySide6 視圖與組件
  services/      # SDK 適配層與外部系統（OpenAI/Gemini/DeepSeek、自定義兼容）
  storage/       # SQLite/JSON providers + repository
  utils/         # env/config/security/logging
  assets/        # 模板、國際化、圖標
  main.py        # 程序入口（QApplication、主窗體）
```

### 1.2 模塊劃分與職責
- core/
  - llm_service.py：統一 LLM 調用（stream/non-stream），錯誤分類、重試、取消。
  - model_manager.py：模型配置 CRUD、啟用/禁用、健康檢查、默認參數。
  - template_manager.py + template_language.py：模板 CRUD、語言切換、導入/導出。
  - prompt_service.py：optimize/iterate/test（接入 llm_service 與模板）。
  - history_manager.py：歷史與迭代鏈；查詢/篩選；導入/導出。
  - preference_service.py：偏好（語言、主題、更新渠道）。
  - data_manager.py：全量導入/導出聚合。
- ui/
  - 主窗體、分頁（提示、模板、模型、歷史、設置）、通用對話框、Toast/通知。
  - MVVM 思路：View（Qt Widgets）、ViewModel（簡單狀態類/Signal）、Model（core）。
- services/
  - openai_client.py、gemini_client.py、compatible_client.py（OpenAI 協議）
  - streaming_adapters.py：將供應商流事件標準化為 Python 生成器/async 生成器。
- storage/
  - sqlite_provider.py：sqlite3/aiosqlite，表：models/templates/history/preferences/meta
  - json_provider.py：導入/導出 JSON 的 schema 驗證、版本註記。
- utils/
  - config.py：讀寫 `%APPDATA%/PromptOptimizer/config.json`（或 SQLite preferences）
  - crypto.py：Fernet/DPAPI 保護 API Key
  - env.py：檢測 OS/資源路徑
  - logs.py：loguru 統一日誌

## 2. 技術架構選型

### 2.1 GUI 框架對比
- Tkinter：
  - 優：內置、零外部依賴；
  - 劣：控件老舊、複雜 UI 成本高。
- PyQt5/6：
  - 優：生態成熟、控件豐富；
  - 劣：授權（GPL/商業）；發佈時合規性要注意。
- PySide6（推薦）：
  - 優：LGPL 許可；API 與 Qt6 同步；控件完善；跨平台好；
  - 劣：體積較大（可透過打包優化）。
- wxPython：
  - 優：原生控件；
  - 劣：打包體積與兼容性需要更多驗證。
- Kivy：
  - 優：跨平台、可觸控；
  - 劣：桌面傳統體驗相對弱。

結論：選 PySide6。

### 2.2 異步處理與流式
- 選型：優先 `asyncio` + `httpx`（或使用 SDK 自帶流式）。
- UI 與異步：使用 `QThread`/`QRunnable` 將網絡請求移出 UI 主線程；或 `asyncqt` 將事件循環與 Qt 整合。
- 流式設計：
  - LLMService 提供同步 blocking generator 與 async generator 兩種接口；
  - UI 層以計時器/信號槽異步消費流事件，增量更新文本框。

### 2.3 配置與安全
- API Key 存儲：
  - 優先 DPAPI（Windows）；備選 cryptography.Fernet（用機器綁定或主密鑰）。
- 偏好與配置：
  - SQLite preferences 表；或 JSON + schema 驗證（pydantic）。
- 導入/導出：
  - JSON，必含 type/version，導入前校驗，失敗回滾。

## 3. 模塊設計映射（TS → Python）

| TS/JS 模塊 | Python 類/模塊 | 核心職責 |
|---|---|---|
| LLMService | core/llm_service.py: `LLMService` | 統一呼叫、流式回傳、錯誤分類、取消/超時 |
| ModelManager | core/model_manager.py: `ModelManager` | 模型配置 CRUD、啟停、校驗、默認參數 |
| TemplateManager/Language | core/template_manager.py, template_language.py | 模板 CRUD、多語言、導入/導出 |
| PromptService | core/prompt_service.py: `PromptService` | 用戶/系統/迭代優化、測試調用 |
| HistoryManager | core/history_manager.py: `HistoryManager` | 歷史與迭代鏈、查詢、導入導出 |
| PreferenceService | core/preference_service.py: `PreferenceService` | UI/更新偏好、本地存儲 |
| DataManager | core/data_manager.py: `DataManager` | 聚合導入/導出、版本控制 |
| StorageFactory/Providers | storage/sqlite_provider.py, json_provider.py | SQLite 實現與 JSON 兼容方案 |
| utils/environment | utils/env.py | OS/路徑/運行環境檢測 |
| ipc-serialization | N/A（本地應用） | 省略，改為直接傳值 |

### 3.1 LLMService 代碼草案
```python
# core/llm_service.py
from typing import Iterator, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

class LLMService:
    def __init__(self, client_factory):
        self._client_factory = client_factory

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
    def generate_stream(self, provider: str, model: str, prompt: str, **params) -> Iterator[str]:
        client = self._client_factory(provider)
        for chunk in client.stream(model=model, input=prompt, **params):
            yield chunk

    def generate(self, provider: str, model: str, prompt: str, **params) -> str:
        return "".join(self.generate_stream(provider, model, prompt, **params))
```

### 3.2 ModelManager 草案
```python
# core/model_manager.py
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ModelConfig:
    name: str
    provider: str
    base_url: str
    api_key: str
    params: Dict
    enabled: bool = True

class ModelManager:
    def __init__(self, repo):
        self.repo = repo

    def list(self) -> List[ModelConfig]:
        return self.repo.fetch_all_models()

    def upsert(self, cfg: ModelConfig):
        self.repo.save_model(cfg)

    def enable(self, name: str, enabled: bool):
        self.repo.set_enabled(name, enabled)
```

### 3.3 PromptService 草案
```python
# core/prompt_service.py
from .llm_service import LLMService

class PromptService:
    def __init__(self, llm: LLMService, templates, history):
        self.llm = llm
        self.templates = templates
        self.history = history

    def optimize_user_prompt(self, text: str, template_id: str, model_id: str):
        tpl = self.templates.get(template_id)
        prompt = tpl.render({"input": text})
        out = self.llm.generate(provider=tpl.provider, model=model_id, prompt=prompt)
        self.history.append("optimize", text, out, model_id, template_id)
        return out
```

## 4. 數據存儲設計

### 4.1 SQLite 結構（示例）
```sql
-- models
CREATE TABLE models (
  name TEXT PRIMARY KEY,
  provider TEXT NOT NULL,
  base_url TEXT,
  api_key TEXT,
  params TEXT,
  enabled INTEGER DEFAULT 1
);

-- templates
CREATE TABLE templates (
  id TEXT PRIMARY KEY,
  type TEXT,   -- user/system/iterate
  lang TEXT,   -- zh/en
  name TEXT,
  content TEXT
);

-- history
CREATE TABLE history (
  id TEXT PRIMARY KEY,
  chain_id TEXT,
  type TEXT,
  model_name TEXT,
  template_id TEXT,
  input TEXT,
  output TEXT,
  created_at INTEGER
);

-- preferences
CREATE TABLE preferences (
  key TEXT PRIMARY KEY,
  value TEXT
);
```

### 4.2 Repository 接口
```python
class Repository:
    def fetch_all_models(self): ...
    def save_model(self, cfg): ...
    def set_enabled(self, name: str, enabled: bool): ...
    # templates/history/preferences 同理
```

## 5. 打包與配置

### 5.1 PyInstaller spec（示例）
```python
# build.spec
block_cipher = None

a = Analysis(['po_app/main.py'],
             datas=[('po_app/assets', 'assets')],
             hiddenimports=['pyside6'],
             noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          name='PromptOptimizer',
          icon='po_app/assets/icon.ico',
          console=False,
          debug=False)
```

### 5.2 構建腳本（PowerShell）
```powershell
python -m pip install -U pip
pip install -r requirements.txt
pyinstaller --clean --noconfirm --onefile --name PromptOptimizer `
  --icon po_app/assets/icon.ico `
  --add-data "po_app/assets;assets" `
  po_app/main.py
```

## 6. 風險與備選
- 體積：PySide6 體積偏大 → 可考慮 Nuitka 或 onedir 分發；精簡依賴。
- 流式體驗：SDK 差異 → 提供兼容層；回退為非流式。
- Key 安全：DPAPI 限 Windows → 多方案容錯（Fernet + 主密鑰）。
- 自動更新：首版手動 → 後續實現檢查更新 + 下載器（HTTP + 校驗）。

