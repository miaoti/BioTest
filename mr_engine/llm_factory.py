"""
B1: Multi-Model Routing Factory & Config

Provides a single `get_llm()` entry point that returns a LangChain
BaseChatModel configured from environment variables / .env file.
Supports Google Gemini, OpenAI, Anthropic, and local vLLM.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from langchain_core.language_models import BaseChatModel

logger = logging.getLogger(__name__)

# Resolve .env relative to project root (one level above this file's package)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_ENV_FILE = _PROJECT_ROOT / ".env"


class LLMSettings(BaseSettings):
    """LLM configuration loaded from environment or .env file."""

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm_model: str = "gemini-1.5-pro"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 4096

    # Provider API keys (optional — only the one matching llm_model is required)
    google_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None

    # Local vLLM
    vllm_base_url: Optional[str] = None

    @model_validator(mode="after")
    def _check_required_key(self) -> "LLMSettings":
        """Validate that the API key for the chosen provider is present."""
        model = self.llm_model.lower()

        if model.startswith("vllm/"):
            if not self.vllm_base_url:
                raise ValueError(
                    f"LLM_MODEL={self.llm_model} requires VLLM_BASE_URL to be set"
                )
            # vLLM uses OpenAI-compatible endpoint — key is optional
            return self

        # Map model name prefixes/keywords to required keys
        checks: list[tuple[list[str], str, Optional[str]]] = [
            (["gemini", "google"], "GOOGLE_API_KEY", self.google_api_key),
            (["gpt", "o1", "o3", "openai"], "OPENAI_API_KEY", self.openai_api_key),
            (["claude", "anthropic"], "ANTHROPIC_API_KEY", self.anthropic_api_key),
            (["llama", "mixtral", "gemma", "qwen", "kimi", "allam", "groq/compound"], "GROQ_API_KEY", self.groq_api_key),
        ]

        for keywords, env_name, key_value in checks:
            if any(kw in model for kw in keywords):
                if not key_value:
                    raise ValueError(
                        f"LLM_MODEL={self.llm_model} requires {env_name} to be set"
                    )
                return self

        # Unknown provider — let init_chat_model handle it
        logger.warning(
            "Could not determine provider for model '%s'; "
            "proceeding without API key validation",
            self.llm_model,
        )
        return self


def get_llm_settings() -> LLMSettings:
    """Load LLM settings from environment / .env file."""
    return LLMSettings()


def get_llm(settings: Optional[LLMSettings] = None) -> BaseChatModel:
    """
    Factory: return a configured LangChain BaseChatModel.

    Args:
        settings: Pre-built settings. If None, loads from environment.

    Returns:
        A ready-to-use LangChain chat model instance.
    """
    if settings is None:
        settings = get_llm_settings()

    model_name = settings.llm_model
    kwargs: dict = {
        "temperature": settings.llm_temperature,
        "max_tokens": settings.llm_max_tokens,
    }

    # ── Local vLLM (OpenAI-compatible) ──
    if model_name.lower().startswith("vllm/"):
        from langchain_openai import ChatOpenAI

        actual_model = model_name[5:]  # strip "vllm/" prefix
        llm = ChatOpenAI(
            model=actual_model,
            base_url=settings.vllm_base_url,
            api_key=settings.openai_api_key or "not-needed",
            **kwargs,
        )
        logger.info("Initialized vLLM model '%s' at %s", actual_model, settings.vllm_base_url)
        return llm

    # ── Google Gemini ──
    model_lower = model_name.lower()
    if any(kw in model_lower for kw in ("gemini", "google")):
        from langchain_google_genai import ChatGoogleGenerativeAI

        llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=settings.google_api_key,
            **kwargs,
        )
        logger.info("Initialized Google GenAI model '%s'", model_name)
        return llm

    # ── OpenAI ──
    if any(kw in model_lower for kw in ("gpt", "o1", "o3", "openai")):
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            model=model_name,
            api_key=settings.openai_api_key,
            **kwargs,
        )
        logger.info("Initialized OpenAI model '%s'", model_name)
        return llm

    # ── Anthropic ──
    if any(kw in model_lower for kw in ("claude", "anthropic")):
        from langchain_anthropic import ChatAnthropic

        llm = ChatAnthropic(
            model=model_name,
            api_key=settings.anthropic_api_key,
            **kwargs,
        )
        logger.info("Initialized Anthropic model '%s'", model_name)
        return llm

    # ── Groq ──
    if any(kw in model_lower for kw in ("llama", "mixtral", "gemma", "qwen", "kimi", "allam", "meta-llama", "groq/compound", "deepseek")):
        from langchain_groq import ChatGroq

        llm = ChatGroq(
            model=model_name,
            api_key=settings.groq_api_key,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )
        logger.info("Initialized Groq model '%s'", model_name)
        return llm

    # ── Fallback: try init_chat_model ──
    from langchain.chat_models import init_chat_model

    llm = init_chat_model(model_name, **kwargs)
    logger.info("Initialized model '%s' via init_chat_model", model_name)
    return llm
