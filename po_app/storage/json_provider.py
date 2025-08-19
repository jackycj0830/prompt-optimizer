from typing import Dict, Any


class JSONProvider:
    def __init__(self, path: str) -> None:
        self.path = path

    def export_all(self) -> Dict[str, Any]:
        # TODO: read JSON and validate
        return {}

    def import_all(self, data: Dict[str, Any]) -> None:
        # TODO: write JSON
        pass

