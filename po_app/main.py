from PySide6.QtWidgets import QApplication
import sys

from po_app.ui.main_window import MainWindow
from po_app.utils.logs import setup_logging


def main() -> None:
    setup_logging()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

