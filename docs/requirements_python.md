# Prompt Optimizer Python 版本需求文檔（requirements_python.md）

## 1. 概述

將現有 TypeScript/JavaScript monorepo（Web/Electron/Extension/MCP）重構為「純 Python 桌面應用」，以 Windows 平台為首要目標，支持一鍵打包為獨立 EXE。核心能力需完整移植（提示詞優化、模型管理、模板管理、歷史記錄、偏好與數據導入導出），並在 Python 生態中落地。

---

## 2. 功能需求重新定義

### 2.1 核心功能移植（Python 方案）
- 提示詞優化（Prompt Optimization）
  - 用戶/系統/迭代優化能力移植為 `PromptService`（Python 類），支持同步與流式兩種調用。
  - 流式回傳：基於 OpenAI Python SDK streaming、或 asyncio + SSE/分塊讀取方式實現增量輸出。
- 模型管理（Model Manager）
  - 支持 OpenAI、Google Gemini、DeepSeek 及 OpenAI 兼容端點（含本地代理/Ollama）。
  - 本地保存多組模型配置（名稱、base_url、api_key、默認參數），提供啟用/禁用與健康檢查。
- 模板管理（Template Manager）
  - 內置與自定義模板管理（CRUD、分類：user/system/iterate），支持中英文模板。
  - 導入/導出 JSON；模板語言切換。
- 歷史記錄（History Manager）
  - 記錄優化輸入/輸出、模型、模板、時間；支持「迭代鏈」串接。
  - 搜索/篩選與導出。
- 數據與偏好（Data/Preference）
  - 一鍵導出/導入（模型、模板、歷史、偏好）。
  - 偏好含 UI 語言、主題、更新偏好等。

### 2.2 UI 框架選擇與理由
- 候選：Tkinter（穩定、功能有限）、PySide6（LGPL、完善控件、跨平台）、PyQt6（GPL/商業）、wxPython、Kivy。
- 推薦：PySide6
  - 理由：
    - 控件完善、桌面體驗好、跨平台；授權友好（LGPL）。
    - 文檔齊全，社區活躍；與設計稿/原 Vue 組件映射容易。
    - 信號/槽模型便於事件流與狀態變更管理。

### 2.3 API 集成適配（Python SDK）
- OpenAI：`openai`（>=1.40），提供 responses API 與流式接口。
- Gemini：`google-generativeai`（>=0.7）。
- DeepSeek：可走 OpenAI 兼容協議（`openai` 客戶端 + 自定義 base_url）。
- 代理/自定義：支持自定義 base_url、headers；可選環境變量加載。

示例（OpenAI 流式）：
```python
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
with client.responses.stream(
    model="gpt-4o-mini",
    input="Optimize my prompt",
) as stream:
    for event in stream:
        if event.type == "response.output_text.delta":
            yield event.delta  # 增量輸出
```

---

## 3. 非功能需求調整

### 3.1 性能
- 啟動時間：≤ 3.5s（首次啟動 ≤ 5s）。
- 內存：常規場景 ≤ 400MB。
- 響應：UI 交互 < 150ms；流式首 token < 2s（視網絡與供應商）。

### 3.2 打包要求
- 打包工具：
  - 首選 PyInstaller（成熟、維護好、社群大）。
  - 可選 Nuitka（需要更小體積/性能時）。
- 配置：
  - 單文件（--onefile）與資料夾模式（--onedir）均支持；默認 onefile。
  - 體積控制：排除測試與開發依賴、UPX（可選）、strip 符號。
  - 資產打包：圖標、內置模板 JSON、國際化文件。

### 3.3 兼容性與依賴管理
- 平台：Windows 10/11（x64）。
- Python：3.10 或 3.11（建議 3.11）。
- 依賴管理：Poetry 或 pip + requirements.txt；建議 Poetry 鎖定版本。

### 3.4 安全
- API Key 僅本地保存；使用 Windows DPAPI 或簡易加密（Fernet）保護。
- 配置存放：`%APPDATA%/PromptOptimizer/config.json`（或 SQLite preferences 表）。

---

## 4. 技術約束

### 4.1 Python 版本
- 建議 Python 3.11（兼顧性能與依賴支持），最低 3.8。

### 4.2 依賴清單（初版建議）
```text
pyside6>=6.6
openai>=1.40
google-generativeai>=0.7
httpx>=0.27
tenacity>=8.2
sqlalchemy>=2.0
aiosqlite>=0.20
cryptography>=42
pydantic>=2.8
pyyaml>=6.0
loguru>=0.7
```
（測試）
```text
pytest>=8.2
pytest-qt>=4.4
pytest-cov>=5.0
```
（打包）
```text
pyinstaller>=6.6
```

### 4.3 部署與分發策略
- 輸出：單一 EXE（默認）；備選 onedir（便於熱修復）。
- 分發：GitHub Releases；可選企業內網共享。
- 自動更新：第一版可手動更新；後續加入「檢查更新」提示與下載。

---

## 5. 代碼與配置示例

### 5.1 目錄（單體應用建議）
```
/po_app
  /core        # 業務核心：llm, model, template, history, data, prefs
  /ui          # PySide6 GUI（視圖）
  /services    # 基礎服務與外部 SDK 適配
  /utils       # 工具、加密、配置、日誌
  /assets      # 模板、圖標、i18n
  main.py      # 程序入口
```

### 5.2 PySide6 主窗體骨架
```python
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

class MainWindow(QMainWindow):
    def __init__(self, app_state):
        super().__init__()
        self.setWindowTitle("Prompt Optimizer")
        self.tabs = QTabWidget()
        # TODO: add PromptTab, TemplatesTab, ModelsTab, HistoryTab, SettingsTab
        self.setCentralWidget(self.tabs)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = MainWindow(app_state={})
    win.show()
    sys.exit(app.exec())
```

### 5.3 PyInstaller 打包命令
```powershell
# Windows PowerShell
pyinstaller --noconfirm --onefile --noconsole ^
  --name PromptOptimizer ^
  --icon assets/icon.ico ^
  --add-data "assets;assets" ^
  main.py
```

---

## 6. 驗收標準（Python 版）
- 功能：提示詞優化/模板/模型/歷史/數據導入導出/偏好可用。
- 性能：啟動/流式/內存達標；UI 不卡頓。
- 安全：API Key 僅本地加密保存；無敏感信息明文落盤。
- 兼容：Windows 10/11 正常運行；依賴可復現安裝。
- 打包：EXE 一鍵打包成功；首次啟動≤5s；體積可控且資產完整。

