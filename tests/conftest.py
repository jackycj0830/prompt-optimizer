"""Global pytest configuration and shared fixtures for the Python refactor.

This file provides lightweight in-memory repositories and fake provider clients
used across unit and integration tests, avoiding external network or file I/O.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Iterator, List
import pathlib
import pytest

# --- In-memory repositories -------------------------------------------------

@dataclass
class _MemModel:
    name: str
    provider: str
    base_url: str | None
    api_key: str | None
    params: Dict[str, Any]
    enabled: bool = True


class MemRepo:
    def __init__(self) -> None:
        self.models: Dict[str, _MemModel] = {}
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.history: List[Dict[str, Any]] = []
        self.preferences: Dict[str, Any] = {}

    # models
    def fetch_all_models(self):
        return list(self.models.values())

    def save_model(self, cfg):
        self.models[cfg.name] = cfg

    def set_enabled(self, name: str, enabled: bool):
        self.models[name].enabled = enabled

    # templates
    def fetch_all_templates(self):
        return list(self.templates.values())

    def get_template(self, id_: str):
        if id_ not in self.templates:
            raise KeyError(id_)
        t = self.templates[id_]
        # minimal Template-like object
        class _T:
            def __init__(self, d):
                self.id = d["id"]
                self.type = d["type"]
                self.lang = d["lang"]
                self.name = d["name"]
                self.content = d["content"]

            def render(self, ctx: Dict[str, Any]) -> str:
                out = self.content
                for k, v in ctx.items():
                    out = out.replace(f"{{{{{k}}}}}", str(v))
                return out
        return _T(t)

    def save_template(self, tpl):
        # accepts dict or object with attributes
        if isinstance(tpl, dict):
            d = tpl
        else:
            d = {"id": tpl.id, "type": tpl.type, "lang": tpl.lang, "name": tpl.name, "content": tpl.content}
        self.templates[d["id"]] = d

    def delete_template(self, id_: str):
        self.templates.pop(id_, None)

    # history
    def add_history(self, type_: str, input_: str, output: str, model_name: str, template_id: str) -> None:
        self.history.append({
            "type": type_, "input": input_, "output": output,
            "model_name": model_name, "template_id": template_id,
        })

    def fetch_history(self):
        return list(self.history)

    # preferences
    def get_preference(self, key: str, default: Any = None) -> Any:
        return self.preferences.get(key, default)

    def set_preference(self, key: str, value: Any) -> None:
        self.preferences[key] = value

    # data
    def export_all(self):
        return {"models": self.fetch_all_models(), "templates": self.fetch_all_templates(),
                "history": self.fetch_history(), "preferences": self.preferences.copy()}

    def import_all(self, data):
        # minimal behavior: replace
        self.models = {m.name: m for m in data.get("models", [])}
        self.templates = {t["id"]: t for t in data.get("templates", [])}
        self.history = list(data.get("history", []))
        self.preferences = dict(data.get("preferences", {}))


# --- Fake provider clients --------------------------------------------------

class FakeClient:
    def __init__(self, chunks: list[str] | None = None):
        self._chunks = chunks or ["hello ", "world"]

    def stream(self, *, model: str, input: str, **params) -> Iterator[str]:
        for c in self._chunks:
            yield c


@pytest.fixture()
def mem_repo() -> MemRepo:
    return MemRepo()


@pytest.fixture()
def fake_client_factory():
    mapping: Dict[str, Any] = {
        "openai": FakeClient(["ok ", "from ", "openai"]),
        "gemini": FakeClient(["ok ", "from ", "gemini"]),
    }

    def _factory(provider: str):
        if provider not in mapping:
            raise KeyError(provider)
        return mapping[provider]

    return _factory


@pytest.fixture()
def tmp_db_path(tmp_path: pathlib.Path) -> pathlib.Path:
    return tmp_path / "test.db"

