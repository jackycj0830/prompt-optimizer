"""End-to-end prompt workflow test with mock provider.

Covers: input -> template render -> LLM stream -> history write.
"""
from po_app.core.llm_service import LLMService
from po_app.core.template_manager import TemplateManager
from po_app.core.history_manager import HistoryManager
from tests.conftest import MemRepo, FakeClient


def test_prompt_workflow_end_to_end(monkeypatch):
    repo = MemRepo()
    # seed template
    repo.save_template({"id": "t1", "type": "user", "lang": "en", "name": "n", "content": "Hello {{input}}"})

    # fake client factory always returns FakeClient
    def factory(_):
        return FakeClient(["Hi ", "there"])  # streamed output

    llm = LLMService(factory)
    tm = TemplateManager(repo)
    hm = HistoryManager(repo)

    tpl = tm.get("t1")
    prompt = tpl.render({"input": "World"})

    text = "".join(llm.generate_stream("openai", model="m", prompt=prompt))
    hm.append("optimize", "World", text, "m", "t1")

    assert text == "Hi there"
    assert len(repo.fetch_history()) == 1

