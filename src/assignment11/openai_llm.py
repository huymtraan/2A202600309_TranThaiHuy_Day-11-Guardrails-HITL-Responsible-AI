"""OpenAI helper wrapper (async)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from openai import AsyncOpenAI

from assignment11.config import OpenAIConfig


@dataclass
class LLMResponse:
    text: str
    raw: Any | None = None


class OpenAIChatLLM:
    """Minimal async wrapper around OpenAI Chat Completions.

    Why:
        Keeps API interactions in one place so safety pipeline code stays
        provider-agnostic and easier to test/replace.
    """

    def __init__(self, config: OpenAIConfig):
        self._config = config
        self._client = AsyncOpenAI(api_key=config.api_key)

    async def chat(self, *, system: str, user: str, model: str | None = None) -> LLMResponse:
        """Send one system+user turn and return normalized text output."""
        resp = await self._client.chat.completions.create(
            model=model or self._config.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.2,
        )
        text = (resp.choices[0].message.content or "").strip()
        return LLMResponse(text=text, raw=resp)
