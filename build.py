import os
import subprocess
from pathlib import Path

DIST = Path("dist")


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd)


def qt_hook_args() -> list[str]:
    """Best-effort collection of critical Qt/PySide6 runtime pieces.
    Works around cases where PyInstaller's default hooks miss some DLLs/plugins.
    """
    args: list[str] = []
    try:
        from PySide6.QtCore import QLibraryInfo
        from pathlib import Path as _P

        # Qt plugin dir (e.g. .../PySide6/plugins)
        plugins_dir = _P(QLibraryInfo.path(QLibraryInfo.PluginsPath))
        # Qt bin dir with Qt6*.dll and OpenSSL (name differs between versions)
        bin_key = getattr(QLibraryInfo, "BinariesPath", None) or getattr(QLibraryInfo, "LibraryExecutablesPath")
        bin_dir = _P(QLibraryInfo.path(bin_key))

        # Include commonly required plugin sub-folders
        for sub in ["platforms", "styles", "imageformats", "iconengines", "tls"]:
            p = plugins_dir / sub
            if p.exists():
                args += ["--add-data", f"{p}{os.pathsep}PySide6/plugins/{sub}"]

        # Explicitly include critical Qt/OpenSSL DLLs if present
        critical_dlls = [
            "Qt6Core.dll",
            "Qt6Gui.dll",
            "Qt6Widgets.dll",
            "libcrypto-3-x64.dll",
            "libssl-3-x64.dll",
        ]
        for dll in critical_dlls:
            fp = bin_dir / dll
            if fp.exists():
                args += ["--add-binary", f"{fp}{os.pathsep}."]
    except Exception as e:  # pragma: no cover - best-effort only
        print(f"[build.py] Qt inspection failed: {e}")
    return args


def main() -> None:
    DIST.mkdir(exist_ok=True)

    # Allow switching between onefile/onedir via env for debugging
    mode = os.environ.get("PO_BUILD_MODE", "onefile").lower()
    onefile = mode != "onedir"

    cmd = [
        "pyinstaller",
        "--clean",
        "--noconfirm",
        "--windowed",  # Hide console window; use Windows GUI subsystem
        "--name", "PromptOptimizer",
        "--icon", "po_app/assets/icon.ico",
        "--add-data", f"po_app/assets{os.pathsep}assets",
        # size optimizations:
        "--exclude-module", "pytest",
        "--exclude-module", "pytest_cov",
        "--exclude-module", "pytest_qt",
        "--exclude-module", "black",
        "--exclude-module", "flake8",
        # robust Qt collection（盡可能交給 PyInstaller hooks 處理）
        "--collect-all", "PySide6",
        "--collect-submodules", "PySide6",
        "--collect-data", "PySide6",
        "--collect-data", "shiboken6",
        "--collect-binaries", "PySide6",
        # 注意：部分 PyInstaller 版本沒有 --collect-qt-plugins 參數，改為下方自動偵測+--add-data
    ]

    # Add mode flag at the end (PyInstaller requires one of them)
    cmd.insert(3, "--onefile" if onefile else "--onedir")

    # Add best-effort explicit additions
    cmd += qt_hook_args()

    # optional UPX (if installed in PATH)
    # cmd += ["--upx-dir", "C:/Tools/upx"]

    cmd += ["po_app/main.py"]
    run(cmd)


if __name__ == "__main__":
    main()

