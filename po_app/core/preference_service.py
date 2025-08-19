from typing import Any, Dict


class PreferenceService:
    def __init__(self, repo) -> None:
        self.repo = repo

    def get(self, key: str, default: Any = None) -> Any:
        return self.repo.get_preference(key, default)

    def set(self, key: str, value: Any) -> None:
        self.repo.set_preference(key, value)

