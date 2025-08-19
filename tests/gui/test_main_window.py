"""pytest-qt GUI tests for MainWindow tabs and basic interactions."""
import pytest
from PySide6.QtWidgets import QApplication
from po_app.ui.main_window import MainWindow


@pytest.mark.parametrize("index", [0, 1, 2, 3, 4])
def test_main_window_tabs_switch(qtbot, index):
    """Ensure tabs exist and can be switched without errors."""
    app = QApplication.instance() or QApplication([])
    win = MainWindow()
    qtbot.addWidget(win)
    win.show()

    assert win.tabs.count() == 5
    win.tabs.setCurrentIndex(index)
    assert win.tabs.currentIndex() == index

