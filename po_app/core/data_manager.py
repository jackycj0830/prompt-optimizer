from typing import Dict, Any


class DataManager:
    def __init__(self, repo) -> None:
        self.repo = repo

    def export_all(self) -> Dict[str, Any]:
        return self.repo.export_all()

    def import_all(self, data: Dict[str, Any]) -> None:
        self.repo.import_all(data)

