from typing import Iterator


class CompatibleOpenAIClient:
    def __init__(self, api_key: str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url

    def stream(self, model: str, input: str, **params) -> Iterator[str]:
        # TODO: integrate OpenAI-compatible streaming via httpx
        yield "[stub-compatible-response]"

