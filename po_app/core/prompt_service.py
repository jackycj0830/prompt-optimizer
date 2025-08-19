from .llm_service import LLMService
from .template_manager import TemplateManager
from .history_manager import HistoryManager


class PromptService:
    def __init__(self, llm: LLMService, templates: TemplateManager, history: HistoryManager):
        self.llm = llm
        self.templates = templates
        self.history = history

    def optimize_user_prompt(self, text: str, template_id: str, model_id: str) -> str:
        tpl = self.templates.get(template_id)
        prompt = tpl.render({"input": text})
        out = self.llm.generate(provider="openai", model=model_id, prompt=prompt)
        self.history.append("optimize", text, out, model_id, template_id)
        return out

