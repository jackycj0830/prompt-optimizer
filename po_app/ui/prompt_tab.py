from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QComboBox, QLabel


class PromptTab(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
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

        # TODO: connect signals to services

