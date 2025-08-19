from PySide6.QtWidgets import QMainWindow, QTabWidget

from .prompt_tab import PromptTab
from .models_tab import ModelsTab
from .templates_tab import TemplatesTab
from .history_tab import HistoryTab
from .settings_tab import SettingsTab

from po_app.core.llm_service import LLMService
from po_app.storage.sqlite_provider import SQLiteProvider
from po_app.core.template_manager import TemplateManager
from po_app.core.history_manager import HistoryManager


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Prompt Optimizer (Python)")
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        # init services
        self.repo = SQLiteProvider(db_path="prompt_optimizer.db")
        self.llm = LLMService(client_factory=self._client_factory)
        self.templates = TemplateManager(self.repo)
        self.history = HistoryManager(self.repo)

        services = {"llm": self.llm, "templates": self.templates, "history": self.history}

        self.prompt_tab = PromptTab(self, services=services)
        self.models_tab = ModelsTab(self)
        self.templates_tab = TemplatesTab(self)
        self.history_tab = HistoryTab(self)
        self.settings_tab = SettingsTab(self)

        self.tabs.addTab(self.prompt_tab, "Prompt")
        self.tabs.addTab(self.models_tab, "Models")
        self.tabs.addTab(self.templates_tab, "Templates")
        self.tabs.addTab(self.history_tab, "History")
        self.tabs.addTab(self.settings_tab, "Settings")

    def _client_factory(self, provider: str):
        if provider == "openai":
            from po_app.services.openai_client import OpenAIClient
            return OpenAIClient()
        if provider == "gemini":
            from po_app.services.gemini_client import GeminiClient
            return GeminiClient()
        if provider == "compatible":
            from po_app.services.compatible_client import CompatibleOpenAIClient
            return CompatibleOpenAIClient()
        raise KeyError(provider)

