from loguru import logger
from pathlib import Path


def setup_logging() -> None:
    log_dir = Path.home() / "PromptOptimizerLogs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logger.add(log_dir / "app.log", rotation="5 MB", retention=5)
    logger.info("Logging initialized")

