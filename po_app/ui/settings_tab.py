from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton


class SettingsTab(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.txt_openai = QLineEdit(self)
        self.txt_gemini = QLineEdit(self)
        self.txt_proxy = QLineEdit(self)
        form.addRow("OpenAI Key", self.txt_openai)
        form.addRow("Gemini Key", self.txt_gemini)
        form.addRow("Proxy", self.txt_proxy)
        layout.addLayout(form)
        self.btn_save = QPushButton("Save", self)
        layout.addWidget(self.btn_save)

        # TODO: bind to PreferenceService/config

