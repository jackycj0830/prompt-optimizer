from typing import Iterator
import os
import google.generativeai as genai


class GeminiClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        genai.configure(api_key=self.api_key)

    def stream(self, model: str, input: str, **params) -> Iterator[str]:
        gmodel = genai.GenerativeModel(model)
        stream = gmodel.generate_content(input, stream=True, **params)
        for chunk in stream:
            if chunk.text:
                yield chunk.text

