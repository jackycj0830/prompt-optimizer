"""Tests for TemplateManager CRUD and rendering."""
from po_app.core.template_manager import TemplateManager
from tests.conftest import MemRepo


def test_template_crud_and_render():
    repo = MemRepo()
    tm = TemplateManager(repo)

    tpl = {"id": "t1", "type": "user", "lang": "zh", "name": "N", "content": "Hello {{name}}"}
    tm.upsert(tpl)

    t = tm.get("t1")
    assert t.render({"name": "World"}) == "Hello World"

    tm.remove("t1")
    assert repo.fetch_all_templates() == []

