from PySide6.QtWidgets import QMainWindow, QTabWidget

from .prompt_tab import PromptTab
from .models_tab import ModelsTab
from .templates_tab import TemplatesTab
from .history_tab import HistoryTab
from .settings_tab import SettingsTab


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Prompt Optimizer (Python)")
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        self.prompt_tab = PromptTab(self)
        self.models_tab = ModelsTab(self)
        self.templates_tab = TemplatesTab(self)
        self.history_tab = HistoryTab(self)
        self.settings_tab = SettingsTab(self)

        self.tabs.addTab(self.prompt_tab, "Prompt")
        self.tabs.addTab(self.models_tab, "Models")
        self.tabs.addTab(self.templates_tab, "Templates")
        self.tabs.addTab(self.history_tab, "History")
        self.tabs.addTab(self.settings_tab, "Settings")

