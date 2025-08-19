from typing import Iterator


class OpenAIClient:
    def __init__(self, api_key: str, base_url: str | None = None) -> None:
        self.api_key = api_key
        self.base_url = base_url

    def stream(self, model: str, input: str, **params) -> Iterator[str]:
        # TODO: integrate openai Responses streaming
        yield "[stub-openai-response]"

