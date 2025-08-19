import subprocess
from pathlib import Path

DIST = Path("dist")


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd)


def main() -> None:
    DIST.mkdir(exist_ok=True)
    cmd = [
        "pyinstaller",
        "--clean",
        "--noconfirm",
        "--onefile",
        "--windowed",  # Hide console window; use Windows GUI subsystem
        "--name", "PromptOptimizer",
        "--icon", "po_app/assets/icon.ico",
        "--add-data", "po_app/assets;assets",
        # size optimizations:
        "--exclude-module", "pytest",
        "--exclude-module", "pytest_cov",
        "--exclude-module", "pytest_qt",
        "--exclude-module", "black",
        "--exclude-module", "flake8",
        # optional UPX (if installed in PATH)
        # "--upx-dir", "C:/Tools/upx",
        "po_app/main.py",
    ]
    run(cmd)


if __name__ == "__main__":
    main()

