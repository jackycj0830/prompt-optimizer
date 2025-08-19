"""GUI integration tests for Settings and Prompt tabs (simplified).

Note: These tests validate that SettingsTab saves preferences and PromptTab
reads provider/model/template lists. Streaming is not executed here.
"""
import pytest
from PySide6.QtWidgets import QApplication
from po_app.ui.main_window import MainWindow


def _ensure_app():
    return QApplication.instance() or QApplication([])


def test_settings_saves_and_prompt_loads(qtbot):
    _ensure_app()
    win = MainWindow()
    qtbot.addWidget(win)
    win.show()

    # simulate settings save
    win.settings_tab.cmb_provider.setCurrentText("openai")
    win.settings_tab.txt_api_key.setText("sk-test")
    win.settings_tab._on_save()

    # prompt tab should have provider defaulted to 'openai'
    assert win.prompt_tab.provider_select.currentText() == "openai"

