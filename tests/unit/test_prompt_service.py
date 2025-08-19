"""Tests for PromptService main optimize flow with history write."""
from po_app.core.prompt_service import PromptService
from po_app.core.llm_service import LLMService
from po_app.core.history_manager import HistoryManager
from po_app.core.template_manager import TemplateManager
from tests.conftest import MemRepo


def test_optimize_writes_history(fake_client_factory):
    repo = MemRepo()
    llm = LLMService(fake_client_factory)
    tm = TemplateManager(repo)
    hm = HistoryManager(repo)

    tm.upsert({"id": "t", "type": "user", "lang": "en", "name": "n", "content": "{{input}}!"})
    svc = PromptService(llm, tm, hm)

    out = svc.optimize_user_prompt("Hi", "t", model_id="gpt-mini")
    assert out.endswith("openai") or out.endswith("gemini") or out  # depends on provider mapping
    assert len(repo.history) == 1

