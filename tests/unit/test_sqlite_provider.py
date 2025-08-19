"""Smoke tests for SQLiteProvider interface (no real DB ops yet)."""
from po_app.storage.sqlite_provider import SQLiteProvider


def test_sqlite_provider_init(tmp_db_path):
    p = SQLiteProvider(str(tmp_db_path))
    # Ensure methods exist and return defaults
    assert p.fetch_all_models() == []
    assert p.fetch_all_templates() == []
    assert p.fetch_history() == []

