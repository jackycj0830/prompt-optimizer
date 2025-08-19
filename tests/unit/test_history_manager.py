"""Tests for HistoryManager append and list operations."""
from po_app.core.history_manager import HistoryManager
from tests.conftest import MemRepo


def test_history_append_and_list():
    repo = MemRepo()
    hm = HistoryManager(repo)

    hm.append("optimize", "in", "out", "m", "t")
    assert len(hm.list()) == 1

