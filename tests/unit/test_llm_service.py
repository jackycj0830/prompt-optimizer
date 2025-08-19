"""Tests for LLMService covering normal and streaming behavior.

- Initializes with a fake client factory
- Verifies generate() concatenates streamed chunks
- Verifies generate_stream() yields tokens in order
- Checks error when provider not found
"""
from po_app.core.llm_service import LLMService
import pytest


def test_generate_concatenates_chunks(fake_client_factory):
    svc = LLMService(fake_client_factory)
    out = svc.generate(provider="openai", model="m", prompt="p")
    assert out == "ok from openai"


def test_generate_stream_yields_tokens(fake_client_factory):
    svc = LLMService(fake_client_factory)
    tokens = list(svc.generate_stream(provider="gemini", model="m", prompt="p"))
    assert tokens == ["ok ", "from ", "gemini"]


def test_unknown_provider_raises(fake_client_factory):
    svc = LLMService(fake_client_factory)
    with pytest.raises(KeyError):
        _ = list(svc.generate_stream(provider="nope", model="m", prompt="p"))

