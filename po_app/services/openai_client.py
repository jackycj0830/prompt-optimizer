from typing import Iterator
import os
from openai import OpenAI


class OpenAIClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = base_url
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url) if self.api_key else OpenAI()

    def stream(self, model: str, input: str, **params) -> Iterator[str]:
        with self.client.responses.stream(model=model, input=input, **params) as stream:
            for event in stream:
                t = getattr(event, "type", "")
                if t == "response.output_text.delta":
                    yield event.delta
                elif t == "response.error":
                    raise RuntimeError(event.error)

