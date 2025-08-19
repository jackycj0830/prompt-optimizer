from typing import Any, Dict, List
import sqlite3
from contextlib import contextmanager
import json


SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS models (
      name TEXT PRIMARY KEY,
      provider TEXT NOT NULL,
      base_url TEXT,
      api_key TEXT,
      params TEXT,
      enabled INTEGER DEFAULT 1
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS templates (
      id TEXT PRIMARY KEY,
      type TEXT,
      lang TEXT,
      name TEXT,
      content TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      chain_id TEXT,
      type TEXT,
      model_name TEXT,
      template_id TEXT,
      input TEXT,
      output TEXT,
      created_at INTEGER DEFAULT (strftime('%s','now'))
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS preferences (
      key TEXT PRIMARY KEY,
      value TEXT
    );
    """,
]


class SQLiteProvider:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._init_schema()

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_schema(self) -> None:
        with self._conn() as conn:
            cur = conn.cursor()
            for ddl in SCHEMA:
                cur.execute(ddl)

    # models
    def fetch_all_models(self) -> List[Any]:
        with self._conn() as conn:
            cur = conn.execute("SELECT name, provider, base_url, api_key, params, enabled FROM models")
            rows = cur.fetchall()
        out = []
        for name, provider, base_url, api_key, params, enabled in rows:
            out.append({
                "name": name,
                "provider": provider,
                "base_url": base_url,
                "api_key": api_key,
                "params": json.loads(params) if params else {},
                "enabled": bool(enabled),
            })
        return out

    def save_model(self, cfg: Any) -> None:
        with self._conn() as conn:
            conn.execute(
                "REPLACE INTO models (name, provider, base_url, api_key, params, enabled) VALUES (?,?,?,?,?,?)",
                (
                    cfg.name, cfg.provider, getattr(cfg, "base_url", None), getattr(cfg, "api_key", None),
                    json.dumps(getattr(cfg, "params", {}) or {}), 1 if getattr(cfg, "enabled", True) else 0,
                ),
            )

    def set_enabled(self, name: str, enabled: bool) -> None:
        with self._conn() as conn:
            conn.execute("UPDATE models SET enabled=? WHERE name=?", (1 if enabled else 0, name))

    # templates
    def fetch_all_templates(self) -> List[Any]:
        with self._conn() as conn:
            cur = conn.execute("SELECT id, type, lang, name, content FROM templates")
            return [
                {"id": i, "type": t, "lang": l, "name": n, "content": c}
                for (i, t, l, n, c) in cur.fetchall()
            ]

    def get_template(self, id_: str) -> Any:
        with self._conn() as conn:
            cur = conn.execute("SELECT id, type, lang, name, content FROM templates WHERE id=?", (id_,))
            row = cur.fetchone()
            if not row:
                raise KeyError(id_)
            i, t, l, n, c = row
            class _T:
                def __init__(self):
                    self.id, self.type, self.lang, self.name, self.content = i, t, l, n, c
                def render(self, ctx: Dict[str, Any]) -> str:
                    out = self.content
                    for k, v in ctx.items():
                        out = out.replace(f"{{{{{k}}}}}", str(v))
                    return out
            return _T()

    def save_template(self, tpl: Any) -> None:
        if isinstance(tpl, dict):
            d = tpl
        else:
            d = {"id": tpl.id, "type": tpl.type, "lang": tpl.lang, "name": tpl.name, "content": tpl.content}
        with self._conn() as conn:
            conn.execute(
                "REPLACE INTO templates (id, type, lang, name, content) VALUES (?,?,?,?,?)",
                (d["id"], d["type"], d["lang"], d["name"], d["content"]),
            )

    def delete_template(self, id_: str) -> None:
        with self._conn() as conn:
            conn.execute("DELETE FROM templates WHERE id=?", (id_,))

    # history
    def add_history(self, type_: str, input_: str, output: str, model_name: str, template_id: str) -> None:
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO history (chain_id, type, model_name, template_id, input, output) VALUES (?,?,?,?,?,?)",
                (None, type_, model_name, template_id, input_, output),
            )

    def fetch_history(self) -> List[Any]:
        with self._conn() as conn:
            cur = conn.execute(
                "SELECT id, chain_id, type, model_name, template_id, input, output, created_at FROM history ORDER BY id DESC"
            )
            return [
                {
                    "id": i, "chain_id": c, "type": t, "model_name": m,
                    "template_id": tid, "input": inp, "output": out, "created_at": ts,
                }
                for (i, c, t, m, tid, inp, out, ts) in cur.fetchall()
            ]

    # preferences
    def get_preference(self, key: str, default: Any = None) -> Any:
        with self._conn() as conn:
            cur = conn.execute("SELECT value FROM preferences WHERE key=?", (key,))
            row = cur.fetchone()
            if not row:
                return default
            try:
                return json.loads(row[0])
            except Exception:
                return row[0]

    def set_preference(self, key: str, value: Any) -> None:
        with self._conn() as conn:
            conn.execute(
                "REPLACE INTO preferences (key, value) VALUES (?,?)",
                (key, json.dumps(value)),
            )

    # data
    def export_all(self) -> Dict[str, Any]:
        return {
            "models": self.fetch_all_models(),
            "templates": self.fetch_all_templates(),
            "history": self.fetch_history(),
            "preferences": {"k": self.get_preference("k")},
        }

    def import_all(self, data: Dict[str, Any]) -> None:
        for m in data.get("models", []):
            class _MC: pass
            obj = _MC(); obj.name=m["name"]; obj.provider=m["provider"]; obj.base_url=m.get("base_url"); obj.api_key=m.get("api_key"); obj.params=m.get("params", {}); obj.enabled=m.get("enabled", True)
            self.save_model(obj)
        for t in data.get("templates", []):
            self.save_template(t)
        for pkey, pval in (data.get("preferences", {}) or {}).items():
            self.set_preference(pkey, pval)
        for h in data.get("history", []):
            self.add_history(h.get("type","optimize"), h.get("input",""), h.get("output",""), h.get("model_name",""), h.get("template_id",""))

