from typing import Iterator, Iterable, Optional, Dict


class LLMService:
    """Unified interface to call different LLM providers with streaming support."""

    def __init__(self, client_factory):
        self._client_factory = client_factory

    def generate_stream(self, provider: str, model: str, prompt: str, **params) -> Iterator[str]:
        client = self._client_factory(provider)
        for chunk in client.stream(model=model, input=prompt, **params):
            yield chunk

    def generate(self, provider: str, model: str, prompt: str, **params) -> str:
        return "".join(self.generate_stream(provider, model, prompt, **params))

