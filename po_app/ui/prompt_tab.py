from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QComboBox, QLabel
from PySide6.QtCore import QObject, QThread, Signal


class _Worker(QObject):
    progress = Signal(str)
    finished = Signal()
    error = Signal(str)

    def __init__(self, llm_service, provider: str, model: str, prompt: str) -> None:
        super().__init__()
        self.llm = llm_service
        self.provider = provider
        self.model = model
        self.prompt = prompt

    def run(self):
        try:
            for chunk in self.llm.generate_stream(self.provider, self.model, self.prompt):
                self.progress.emit(chunk)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class PromptTab(QWidget):
    def __init__(self, parent=None, services=None) -> None:
        super().__init__(parent)
        self.services = services or {}
        layout = QVBoxLayout(self)

        controls = QHBoxLayout()
        self.provider_select = QComboBox(self)
        self.provider_select.addItems(["openai", "gemini", "compatible"])
        self.model_select = QComboBox(self)
        self.template_select = QComboBox(self)
        controls.addWidget(QLabel("Provider:"))
        controls.addWidget(self.provider_select)
        controls.addWidget(QLabel("Model:"))
        controls.addWidget(self.model_select)
        controls.addWidget(QLabel("Template:"))
        controls.addWidget(self.template_select)
        layout.addLayout(controls)

        self.input_text = QTextEdit(self)
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        layout.addWidget(QLabel("Input"))
        layout.addWidget(self.input_text)
        layout.addWidget(QLabel("Output"))
        layout.addWidget(self.output_text)

        actions = QHBoxLayout()
        self.btn_optimize = QPushButton("Optimize", self)
        self.btn_iterate = QPushButton("Iterate", self)
        actions.addWidget(self.btn_optimize)
        actions.addWidget(self.btn_iterate)
        layout.addLayout(actions)

        self.btn_optimize.clicked.connect(self._on_optimize)
        self._load_initial_data()

    def _load_initial_data(self):
        # load provider/model/template lists
        prefs = self.services.get("prefs")
        provider = prefs.get("provider", "openai") if prefs else "openai"
        idx = self.provider_select.findText(provider)
        if idx >= 0:
            self.provider_select.setCurrentIndex(idx)

        models = self.services.get("models").list() if self.services.get("models") else []
        self.model_select.clear()
        for m in models:
            self.model_select.addItem(m.name)

        templates = self.services.get("templates").list() if self.services.get("templates") else []
        self.template_select.clear()
        for t in templates:
            self.template_select.addItem(t.id)

    def _on_optimize(self):
        provider = self.provider_select.currentText() or "openai"
        model = self.model_select.currentText() or "gpt-4o-mini"
        text = self.input_text.toPlainText()

        tpl_id = self.template_select.currentText()
        tpl_mgr = self.services.get("templates")
        if tpl_mgr and tpl_id:
            tpl = tpl_mgr.get(tpl_id)
            prompt = tpl.render({"input": text})
        else:
            prompt = text

        self.output_text.clear()
        self._thread = QThread(self)
        self._worker = _Worker(self.services.get("llm"), provider, model, prompt)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self.output_text.insertPlainText)
        self._worker.finished.connect(self._on_stream_finished)
        self._worker.error.connect(lambda m: self.output_text.append(f"\n[Error] {m}"))
        self._thread.start()

    def _on_stream_finished(self):
        # write history
        history = self.services.get("history")
        tpl_id = self.template_select.currentText()
        model = self.model_select.currentText()
        if history:
            history.append("optimize", self.input_text.toPlainText(), self.output_text.toPlainText(), model, tpl_id)
        self.output_text.append("\n[Done]")

