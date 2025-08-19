from pathlib import Path
import json
from typing import Any

APP_DIR = Path.home() / "AppData" / "Roaming" / "PromptOptimizer"
CONFIG_FILE = APP_DIR / "config.json"


def load_config() -> dict:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    return {}


def save_config(cfg: dict) -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def get(key: str, default: Any = None) -> Any:
    return load_config().get(key, default)


def set(key: str, value: Any) -> None:
    cfg = load_config()
    cfg[key] = value
    save_config(cfg)

