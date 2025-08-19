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
        self.model_select = QComboBox(self)
        self.template_select = QComboBox(self)
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

    def _on_optimize(self):
        provider = "openai"  # TODO: from selection
        model = self.model_select.currentText() or "gpt-4o-mini"
        text = self.input_text.toPlainText()
        # TODO: render template with TemplateManager
        prompt = text

        self.output_text.clear()
        self._thread = QThread(self)
        self._worker = _Worker(self.services.get("llm"), provider, model, prompt)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self.output_text.insertPlainText)
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(lambda m: self.output_text.append(f"\n[Error] {m}"))
        self._thread.start()

