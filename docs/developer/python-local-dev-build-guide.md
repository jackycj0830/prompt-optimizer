# Python 重構項目本地開發與構建指南

## 前置要求
- Python 3.12 或更高版本
- Poetry 包管理工具（如未安裝，請先執行 `pip install poetry`）
- Windows 環境（用於 EXE 打包）

## 開發環境設置
1. 安裝項目依賴：
   ```bash
   poetry install
   ```
   這將創建虛擬環境並安裝 pyproject.toml 中定義的所有運行時和開發依賴。

2. 運行測試套件：
   ```bash
   poetry run pytest
   ```
   執行完整的測試套件，包括單元測試、集成測試和 GUI 測試，並生成覆蓋率報告。

3. 啟動應用程序（開發模式）：
   ```bash
   poetry run python po_app/main.py
   ```
   或使用配置的腳本：
   ```bash
   poetry run prompt-optimizer
   ```

## 構建可執行文件
1. 構建單文件 EXE（默認）：
   ```bash
   poetry run python build.py
   ```
   產出：`dist/PromptOptimizer.exe`（獨立可執行文件，包含所有依賴）

2. 構建目錄模式 EXE（便於調試和熱修復）：
   ```powershell
   .\build.ps1 -OneDir
   ```
   產出：`dist/PromptOptimizer/` 目錄，包含主執行文件和依賴庫

## 驗證構建結果
- 檢查 `dist/` 目錄中的輸出文件
- 在沒有 Python 環境的 Windows 機器上測試 EXE 文件
- 確認應用程序能正常啟動並顯示主界面

