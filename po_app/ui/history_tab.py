from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton


class HistoryTab(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.list = QListWidget(self)
        layout.addWidget(self.list)

        actions = QHBoxLayout()
        self.btn_export = QPushButton("Export", self)
        self.btn_clear = QPushButton("Clear", self)
        actions.addWidget(self.btn_export)
        actions.addWidget(self.btn_clear)
        layout.addLayout(actions)

        # TODO: connect signals to HistoryManager

