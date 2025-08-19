from typing import Iterator
import os
import httpx


class CompatibleOpenAIClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None, timeout: int = 60) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
        self.timeout = timeout
        self._client = httpx.Client(base_url=self.base_url, headers={"Authorization": f"Bearer {self.api_key}"}, timeout=timeout)

    def stream(self, model: str, input: str, **params) -> Iterator[str]:
        # OpenAI-compatible chat/completions streaming (SSE-like)
        payload = {"model": model, "stream": True, "messages": [{"role": "user", "content": input}], **params}
        with self._client.stream("POST", "/chat/completions", json=payload) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if not line:
                    continue
                if line.startswith(b"data: "):
                    data = line[6:]
                    if data == b"[DONE]":
                        break
                    try:
                        import json
                        obj = json.loads(data)
                        delta = obj.get("choices", [{}])[0].get("delta", {}).get("content")
                        if delta:
                            yield delta
                    except Exception:
                        continue

