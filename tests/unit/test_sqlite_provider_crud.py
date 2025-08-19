"""Basic CRUD tests for SQLiteProvider using a temporary DB."""
import pathlib
from po_app.storage.sqlite_provider import SQLiteProvider
from po_app.core.model_manager import ModelConfig


def test_sqlite_crud(tmp_path: pathlib.Path):
    db = tmp_path / "t.db"
    repo = SQLiteProvider(str(db))

    # models
    cfg = ModelConfig(name="m1", provider="openai", base_url=None, api_key="k", params={})
    repo.save_model(cfg)
    models = repo.fetch_all_models()
    assert any(m["name"] == "m1" for m in models)

    repo.set_enabled("m1", False)
    models = repo.fetch_all_models()
    assert any(not m["enabled"] and m["name"] == "m1" for m in models)

    # templates
    repo.save_template({"id": "t1", "type": "user", "lang": "en", "name": "n", "content": "Hi {{name}}"})
    tpl = repo.get_template("t1")
    assert tpl.render({"name": "X"}) == "Hi X"

    # history
    repo.add_history("optimize", "in", "out", "m1", "t1")
    hist = repo.fetch_history()
    assert len(hist) == 1

    # preferences
    repo.set_preference("lang", "en")
    assert repo.get_preference("lang") == "en"

