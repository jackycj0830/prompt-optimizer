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
        "--name",
        "PromptOptimizer",
        "--icon",
        "po_app/assets/icon.ico",
        "--add-data",
        "po_app/assets;assets",
        "po_app/main.py",
    ]
    run(cmd)


if __name__ == "__main__":
    main()

