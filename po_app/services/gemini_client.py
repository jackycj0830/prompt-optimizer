from typing import Iterator


class GeminiClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def stream(self, model: str, input: str, **params) -> Iterator[str]:
        # TODO: integrate google-generativeai streaming
        yield "[stub-gemini-response]"

