from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QHBoxLayout


class TemplatesTab(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.list = QListWidget(self)
        layout.addWidget(self.list)

        actions = QHBoxLayout()
        self.btn_add = QPushButton("Add", self)
        self.btn_edit = QPushButton("Edit", self)
        self.btn_delete = QPushButton("Delete", self)
        self.btn_import = QPushButton("Import", self)
        self.btn_export = QPushButton("Export", self)
        for b in (self.btn_add, self.btn_edit, self.btn_delete, self.btn_import, self.btn_export):
            actions.addWidget(b)
        layout.addLayout(actions)

        # TODO: connect signals to TemplateManager

