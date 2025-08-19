from typing import Any, Dict, List


class SQLiteProvider:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        # TODO: init schema if not exists

    # models
    def fetch_all_models(self) -> List[Any]:
        return []

    def save_model(self, cfg: Any) -> None:
        pass

    def set_enabled(self, name: str, enabled: bool) -> None:
        pass

    # templates
    def fetch_all_templates(self) -> List[Any]:
        return []

    def get_template(self, id_: str) -> Any:
        raise KeyError(id_)

    def save_template(self, tpl: Any) -> None:
        pass

    def delete_template(self, id_: str) -> None:
        pass

    # history
    def add_history(self, type_: str, input_: str, output: str, model_name: str, template_id: str) -> None:
        pass

    def fetch_history(self) -> List[Any]:
        return []

    # preferences
    def get_preference(self, key: str, default: Any = None) -> Any:
        return default

    def set_preference(self, key: str, value: Any) -> None:
        pass

    # data
    def export_all(self) -> Dict[str, Any]:
        return {"models": [], "templates": [], "history": [], "preferences": {}}

    def import_all(self, data: Dict[str, Any]) -> None:
        pass

