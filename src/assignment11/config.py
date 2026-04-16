"""Assignment 11 config.

Loads environment variables from `.env` when available.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def load_env() -> None:
    """Load `.env` into the process environment if python-dotenv is installed."""
    try:
        from dotenv import load_dotenv
        # python-dotenv's find_dotenv() can be fragile in some runtimes;
        # explicitly point at repo-local `.env` if present.
        env_path = Path(".env")
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
        else:
            load_dotenv()
    except Exception:
        return


@dataclass(frozen=True)
class OpenAIConfig:
    api_key: str
    model: str = "gpt-4o-mini"
    judge_model: str = "gpt-4o-mini"


def get_openai_config() -> OpenAIConfig:
    """Read OpenAI config from env.

    Required:
        OPENAI_API_KEY

    Optional:
        OPENAI_MODEL (default: gpt-4o-mini)
        OPENAI_JUDGE_MODEL (default: gpt-4o-mini)
    """
    load_env()
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Put it in environment or a `.env` file."
        )
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"
    judge_model = (
        os.environ.get("OPENAI_JUDGE_MODEL", model).strip() or model
    )
    return OpenAIConfig(api_key=api_key, model=model, judge_model=judge_model)
