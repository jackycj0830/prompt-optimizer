"""Tests for ModelManager CRUD and enable/disable behavior."""
from po_app.core.model_manager import ModelManager, ModelConfig
from tests.conftest import MemRepo


def test_model_crud_and_enable():
    repo = MemRepo()
    mm = ModelManager(repo)

    cfg = ModelConfig(name="gpt-mini", provider="openai", base_url=None, api_key="k", params={})
    mm.upsert(cfg)
    assert len(mm.list()) == 1

    mm.enable("gpt-mini", False)
    assert not repo.models["gpt-mini"].enabled

