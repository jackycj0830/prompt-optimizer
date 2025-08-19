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

    def upsert(self, cfg: ModelConfig) -> None:
        self.repo.save_model(cfg)

    def enable(self, name: str, enabled: bool) -> None:
        self.repo.set_enabled(name, enabled)

