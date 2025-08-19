from typing import Iterator
from tenacity import retry, stop_after_attempt, wait_exponential


class LLMService:
    """Unified interface to call different LLM providers with streaming support."""

    def __init__(self, client_factory):
        self._client_factory = client_factory

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
    def generate_stream(self, provider: str, model: str, prompt: str, **params) -> Iterator[str]:
        client = self._client_factory(provider)
        for chunk in client.stream(model=model, input=prompt, **params):
            yield chunk

    def generate(self, provider: str, model: str, prompt: str, **params) -> str:
        return "".join(self.generate_stream(provider, model, prompt, **params))

