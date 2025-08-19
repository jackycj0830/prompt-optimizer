from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, QLabel
from PySide6.QtCore import Qt


class SettingsTab(QWidget):
    def __init__(self, parent=None, services=None) -> None:
        super().__init__(parent)
        self.services = services or {}
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.cmb_provider = QComboBox(self)
        self.cmb_provider.addItems(["openai", "gemini", "compatible"])
        self.txt_base_url = QLineEdit(self)
        self.txt_api_key = QLineEdit(self)
        self.txt_api_key.setEchoMode(QLineEdit.Password)

        form.addRow("Provider", self.cmb_provider)
        form.addRow("Base URL (for Compatible)", self.txt_base_url)
        form.addRow("API Key", self.txt_api_key)
        layout.addLayout(form)

        self.btn_save = QPushButton("Save", self)
        layout.addWidget(self.btn_save, alignment=Qt.AlignLeft)

        self.btn_save.clicked.connect(self._on_save)
        self._load()

    def _load(self):
        prefs = self.services.get("prefs")
        if not prefs:
            return
        provider = prefs.get("provider", "openai")
        idx = self.cmb_provider.findText(provider)
        if idx >= 0:
            self.cmb_provider.setCurrentIndex(idx)
        self.txt_base_url.setText(prefs.get("base_url", ""))
        self.txt_api_key.setText(prefs.get("api_key", ""))

    def _on_save(self):
        prefs = self.services.get("prefs")
        if not prefs:
            return
        prefs.set("provider", self.cmb_provider.currentText())
        prefs.set("base_url", self.txt_base_url.text().strip())
        prefs.set("api_key", self.txt_api_key.text().strip())

