import platform
from pathlib import Path


def is_windows() -> bool:
    return platform.system().lower() == "windows"


def app_data_dir() -> Path:
    if is_windows():
        from os import getenv
        base = Path(getenv("APPDATA", str(Path.home() / "AppData" / "Roaming")))
        return base / "PromptOptimizer"
    return Path.home() / ".prompt-optimizer"

