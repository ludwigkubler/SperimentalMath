"""Routing Engine - intelligently routes LLM requests to the best available provider."""

from __future__ import annotations

import logging
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

from .providers.base import BaseProvider, ProviderStatus, RateLimitError
from .providers.ollama import OllamaProvider
from .providers.groq import GroqProvider
from .providers.mistral import MistralProvider
from .providers.cerebras import CerebrasProvider
from .providers.google import GoogleProvider
from .providers.openrouter import OpenRouterProvider
from .providers.sambanova import SambaNovaProvider
from .providers.together import TogetherProvider      # sec_router_providers_v1
from .providers.fireworks import FireworksProvider    # sec_router_providers_v1
from .providers.deepinfra import DeepInfraProvider    # sec_router_providers_v1
from .providers.claude_max import ClaudeMaxProvider   # sec_claude_max_v1

log = logging.getLogger(__name__)

PROVIDER_CLASSES = {
    "ollama_local": OllamaProvider,
    "ollama_remote": OllamaProvider,
    "groq": GroqProvider,
    "mistral": MistralProvider,
    "cerebras": CerebrasProvider,
    "google": GoogleProvider,
    "openrouter": OpenRouterProvider,
    "sambanova": SambaNovaProvider,
    "together": TogetherProvider,      # sec_router_providers_v1
    "fireworks": FireworksProvider,    # sec_router_providers_v1
    "deepinfra": DeepInfraProvider,    # sec_router_providers_v1
    "claude_max": ClaudeMaxProvider,   # sec_claude_max_v1
}


class TaskType(str, Enum):
    CODING = "coding"
    REASONING = "reasoning"
    REVIEW = "review"
    DOCS = "docs"
    SECURITY = "security"
    CONVERSATION = "conversation"
    GENERAL = "general"


class RoutingStrategy(str, Enum):
    QUALITY_FIRST = "quality_first"
    SPEED_FIRST = "speed_first"
    LOCAL_FIRST = "local_first"
    ROUND_ROBIN = "round_robin"


# Default task-to-provider routing chains
# Strategy: claude_max for HIGH-VALUE reasoning (proposer/critic/judge),
# free providers for cheap tasks (test_gen=coding, paper=docs, novelty queries).
# This keeps Claude budget for places where quality matters most.
DEFAULT_TASK_ROUTING: dict[str, list[str]] = {
    "coding": ["ollama_remote", "mistral", "groq", "openrouter", "claude_max", "ollama_local"],
    "reasoning": ["claude_max", "sambanova", "cerebras", "groq", "google", "ollama_remote", "ollama_local"],
    "review": ["claude_max", "mistral", "openrouter", "groq", "ollama_remote", "ollama_local"],
    "docs": ["groq", "mistral", "ollama_local", "ollama_remote", "claude_max"],
    "security": ["claude_max", "cerebras", "google", "groq", "ollama_remote", "ollama_local"],
    "conversation": ["cerebras", "groq", "google", "sambanova", "ollama_remote", "claude_max"],
    "general": ["groq", "cerebras", "ollama_remote", "ollama_local", "claude_max"],
}

# Default model selection per provider+task
DEFAULT_MODEL_MAP: dict[str, dict[str, str]] = {
    # sec_local_model_mix_v2 — 2026-05-19 (post-benchmark)
    # Benchmark report: audit/fixes/20260519_local_model_benchmark.md
    # Key changes from v1:
    #   - reasoning: qwen3:8b -> glm4:latest (2.6x faster wall clock, same quality)
    #   - conversation/general (ollama_remote): qwen3:8b -> glm4:latest
    #   - deepseek-r1:8b NOT used (wraps output in <think> tags, no parseable JSON)
    "ollama_local": {
        "coding": "qwen2.5-coder:3b",
        "reasoning": "qwen3:8b",         # 3070 Ti local — qwen3:8b OK for slower-but-fine
        "review": "qwen2.5-coder:3b",
        "docs": "gemma3:4b",
        "security": "qwen2.5-coder:3b",
        "conversation": "gemma3:4b",
        "general": "gemma3:4b",
    },
    "ollama_remote": {
        "coding": "qwen2.5-coder:7b",    # benchmark winner: 17.7s, 68 tok/s, score 100
        "reasoning": "glm4:latest",      # NEW: 40.7s judge vs 107s for qwen3:8b
        "review": "qwen2.5-coder:7b",
        "docs": "gemma3:4b",
        "security": "qwen2.5-coder:7b",
        "conversation": "glm4:latest",   # NEW: 2.6x faster than qwen3:8b
        "general": "glm4:latest",        # NEW
    },
    "groq": {
        "coding": "llama-3.3-70b-versatile",
        "reasoning": "llama-3.3-70b-versatile",
        "review": "llama-3.3-70b-versatile",
        "docs": "llama-3.1-8b-instant",
        "security": "llama-3.3-70b-versatile",
        "conversation": "llama-3.3-70b-versatile",
        "general": "llama-3.3-70b-versatile",
    },
    "mistral": {
        "coding": "codestral-latest",
        "reasoning": "mistral-large-latest",
        "review": "codestral-latest",
        "docs": "mistral-small-latest",
        "security": "mistral-large-latest",
        "conversation": "mistral-large-latest",
        "general": "mistral-large-latest",
    },
    "cerebras": {
        "coding": "qwen-3-235b-a22b-instruct-2507",
        "reasoning": "qwen-3-235b-a22b-instruct-2507",
        "review": "qwen-3-235b-a22b-instruct-2507",
        "docs": "llama3.1-8b",
        "security": "qwen-3-235b-a22b-instruct-2507",
        "conversation": "qwen-3-235b-a22b-instruct-2507",
        "general": "qwen-3-235b-a22b-instruct-2507",
    },
    "google": {
        "coding": "gemini-2.5-flash",
        "reasoning": "gemini-2.5-flash",
        "review": "gemini-2.5-flash",
        "docs": "gemini-2.5-flash",
        "security": "gemini-2.5-flash",
        "conversation": "gemini-2.5-flash",
        "general": "gemini-2.5-flash",
    },
    "openrouter": {
        "coding": "google/gemma-3-27b-it:free",
        "reasoning": "meta-llama/llama-3.3-70b-instruct:free",
        "review": "google/gemma-3-27b-it:free",
        "docs": "google/gemma-3-27b-it:free",
        "security": "nvidia/llama-3.1-nemotron-70b-instruct:free",
        "conversation": "meta-llama/llama-3.3-70b-instruct:free",
        "general": "meta-llama/llama-3.3-70b-instruct:free",
    },
    "sambanova": {
        "coding": "Meta-Llama-3.3-70B-Instruct",
        "reasoning": "DeepSeek-R1",
        "review": "Meta-Llama-3.3-70B-Instruct",
        "docs": "Meta-Llama-3.3-70B-Instruct",
        "security": "DeepSeek-R1",
        "conversation": "Meta-Llama-3.3-70B-Instruct",
        "general": "Meta-Llama-3.3-70B-Instruct",
    },
    "claude_max": {                                # sec_claude_max_v1
        "coding": "sonnet",       # Sonnet 4.6: fast + great code
        "reasoning": "opus",      # Opus 4.7: max quality math/proof
        "review": "sonnet",
        "docs": "sonnet",
        "security": "opus",
        "conversation": "sonnet",
        "general": "sonnet",
    },
}

# Task-specific optimal parameters
TASK_PARAMETERS: dict[str, dict[str, float]] = {
    "coding": {"temperature": 0.1, "top_p": 0.9},
    "reasoning": {"temperature": 0.5, "top_p": 0.95},
    "review": {"temperature": 0.2, "top_p": 0.9},
    "docs": {"temperature": 0.3, "top_p": 0.9},
    "security": {"temperature": 0.1, "top_p": 0.9},
    "conversation": {"temperature": 0.7, "top_p": 0.9},
    "general": {"temperature": 0.4, "top_p": 0.9},
}


class RoutingEngine:
    """Routes LLM requests to the best available provider based on task type and availability."""

    def __init__(self, config_path: str | Path | None = None):
        self.providers: dict[str, BaseProvider] = {}
        self.task_routing: dict[str, list[str]] = dict(DEFAULT_TASK_ROUTING)
        self.model_map: dict[str, dict[str, str]] = dict(DEFAULT_MODEL_MAP)
        self.default_strategy = RoutingStrategy.QUALITY_FIRST
        self._round_robin_idx = 0
        # Adaptive routing state
        self._feedback_store = None
        self._quality_cache: dict[str, tuple[float, list[dict]]] = {}
        self._quality_cache_ttl: float = 300.0  # 5 min

        if config_path:
            self._load_config(config_path)

    def set_feedback_store(self, store) -> None:
        """Attach a FeedbackStore to enable adaptive quality-based routing."""
        self._feedback_store = store
        log.info("RoutingEngine: adaptive routing enabled via FeedbackStore")

    async def _adaptive_reorder(self, chain: list[str], task_type: str) -> list[str]:
        """Reorder a provider chain by historical quality, if data available."""
        if not self._feedback_store or not chain:
            return chain
        try:
            import time as _t
            now = _t.monotonic()
            cached = self._quality_cache.get(task_type)
            if cached and (now - cached[0]) < self._quality_cache_ttl:
                stats = cached[1]
            else:
                stats = await self._feedback_store.get_model_quality_stats(
                    agent_type=task_type, min_samples=3, recent_days=30
                )
                self._quality_cache[task_type] = (now, stats)
            if not stats:
                return chain
            model_q = {s["model_used"]: s["avg_quality"] for s in stats}

            def score(provider_name: str) -> float:
                model = self._select_model(provider_name, task_type)
                return model_q.get(model, 5.0)  # neutral default

            reordered = sorted(chain, key=score, reverse=True)
            if reordered != chain:
                log.debug(
                    "Adaptive reorder for %s: %s → %s", task_type, chain, reordered
                )
            return reordered
        except Exception as e:
            log.debug("Adaptive reorder failed: %s", e)
            return chain

    def _load_config(self, path: str | Path) -> None:
        path = Path(path)
        if not path.exists():
            log.warning(f"Provider config not found: {path}")
            return

        with open(path) as f:
            cfg = yaml.safe_load(f) or {}

        # Load providers
        for name, pcfg in cfg.get("providers", {}).items():
            if not pcfg.get("enabled", True):
                continue
            cls = PROVIDER_CLASSES.get(name)
            if cls:
                try:
                    self.providers[name] = cls(pcfg)
                    log.info(f"Loaded provider: {name} ({cls.__name__})")
                except Exception as e:
                    log.error(f"Failed to load provider {name}: {e}")

        # Load routing config
        routing_cfg = cfg.get("routing", {})
        if "default_strategy" in routing_cfg:
            try:
                self.default_strategy = RoutingStrategy(routing_cfg["default_strategy"])
            except ValueError:
                pass
        if "task_routing" in routing_cfg:
            self.task_routing.update(routing_cfg["task_routing"])
        if "model_map" in routing_cfg:
            self.model_map.update(routing_cfg["model_map"])

    def register_provider(self, name: str, provider: BaseProvider) -> None:
        self.providers[name] = provider
        log.info(f"Registered provider: {name}")

    def _get_chain(self, task_type: str, strategy: RoutingStrategy | None = None) -> list[str]:
        """Get ordered provider chain for a task type."""
        strategy = strategy or self.default_strategy
        chain = self.task_routing.get(task_type, self.task_routing.get("general", []))

        if strategy == RoutingStrategy.LOCAL_FIRST:
            local = [p for p in chain if p in self.providers and self.providers[p].is_local]
            cloud = [p for p in chain if p in self.providers and not self.providers[p].is_local]
            return local + cloud
        elif strategy == RoutingStrategy.SPEED_FIRST:
            # Groq and Cerebras are fastest, then local
            speed_order = ["groq", "cerebras", "ollama_local", "ollama_remote", "mistral", "openrouter", "sambanova", "google"]
            return [p for p in speed_order if p in chain and p in self.providers]
        elif strategy == RoutingStrategy.ROUND_ROBIN:
            available = [p for p in chain if p in self.providers]
            if available:
                self._round_robin_idx = (self._round_robin_idx + 1) % len(available)
                rotated = available[self._round_robin_idx:] + available[:self._round_robin_idx]
                return rotated
            return chain

        # quality_first = default chain order
        return [p for p in chain if p in self.providers]

    def _select_model(self, provider_name: str, task_type: str) -> str:
        """Select the best model for a provider+task combination."""
        provider_models = self.model_map.get(provider_name, {})
        model = provider_models.get(task_type)
        if model:
            return model
        # Fallback to general
        model = provider_models.get("general")
        if model:
            return model
        # Fallback to first configured model
        provider = self.providers.get(provider_name)
        if provider and provider.models_config:
            return provider.models_config[0]
        return ""

    async def route(
        self,
        prompt: str,
        task_type: str = "general",
        system: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 4096,
        strategy: RoutingStrategy | None = None,
        preferred_provider: str | None = None,
        **kwargs,
    ) -> tuple[str, str, str]:
        """Route a request to the best provider.

        Returns: (response_text, provider_name, model_used)
        """
        chain = self._get_chain(task_type, strategy)

        # Adaptive reorder by historical quality (quality_first only)
        effective_strategy = strategy or self.default_strategy
        if effective_strategy == RoutingStrategy.QUALITY_FIRST:
            chain = await self._adaptive_reorder(chain, task_type)

        # If preferred provider is specified and available, try it first
        if preferred_provider and preferred_provider in self.providers:
            if preferred_provider not in chain:
                chain = [preferred_provider] + chain
            else:
                chain.remove(preferred_provider)
                chain = [preferred_provider] + chain

        errors = []
        for provider_name in chain:
            provider = self.providers.get(provider_name)
            if not provider:
                continue
            if provider.status in (ProviderStatus.DISABLED, ProviderStatus.NO_KEY):
                continue
            if provider.status == ProviderStatus.RATE_LIMITED:
                log.debug(f"Skipping {provider_name}: rate limited")
                continue

            model = self._select_model(provider_name, task_type)
            if not model:
                continue

            try:
                log.info(f"Routing to {provider_name}/{model} for task={task_type}")
                # Apply task-specific temperature if caller didn't override
                task_temp = temperature
                if temperature == 0.2:  # default = not explicitly set
                    task_params = TASK_PARAMETERS.get(task_type, {})
                    task_temp = task_params.get("temperature", temperature)
                result = await provider.generate(
                    model=model,
                    prompt=prompt,
                    system=system,
                    temperature=task_temp,
                    max_tokens=max_tokens,
                    **kwargs,
                )
                return result, provider_name, model
            except RateLimitError as e:
                log.warning(f"{provider_name}: {e}")
                errors.append(str(e))
                continue
            except (ConnectionError, RuntimeError) as e:
                log.warning(f"{provider_name}: {e}")
                errors.append(str(e))
                continue

        raise RuntimeError(
            f"All providers failed for task={task_type}. "
            f"Chain: {chain}. Errors: {'; '.join(errors)}"
        )

    async def route_chat(
        self,
        messages: list[dict],
        task_type: str = "general",
        strategy: RoutingStrategy | None = None,
        preferred_provider: str | None = None,
        **kwargs,
    ) -> tuple[str, str, str]:
        """Route a chat request. Returns (response, provider_name, model)."""
        chain = self._get_chain(task_type, strategy)
        if preferred_provider and preferred_provider in self.providers:
            chain = [preferred_provider] + [p for p in chain if p != preferred_provider]

        for provider_name in chain:
            provider = self.providers.get(provider_name)
            if not provider or provider.status in (ProviderStatus.DISABLED, ProviderStatus.NO_KEY, ProviderStatus.RATE_LIMITED):
                continue

            model = self._select_model(provider_name, task_type)
            if not model:
                continue

            try:
                task_temp = kwargs.get("temperature", 0.2)
                if task_temp == 0.2:
                    task_params = TASK_PARAMETERS.get(task_type, {})
                    task_temp = task_params.get("temperature", task_temp)
                kwargs["temperature"] = task_temp
                result = await provider.chat(model=model, messages=messages, **kwargs)
                return result, provider_name, model
            except (RateLimitError, ConnectionError, RuntimeError) as e:
                log.warning(f"{provider_name}: {e}")
                continue

        raise RuntimeError(f"All providers failed for chat task={task_type}")

    async def health_check_all(self) -> dict[str, bool]:
        """Check health of all registered providers."""
        results = {}
        for name, provider in self.providers.items():
            try:
                results[name] = await provider.health_check()
            except Exception:
                results[name] = False
        return results

    def get_available_providers(self) -> list[str]:
        """List providers that are ready to serve."""
        return [
            name for name, p in self.providers.items()
            if p.status == ProviderStatus.READY
        ]

    def get_all_metrics(self) -> dict[str, dict]:
        """Get metrics for all providers."""
        return {name: p.to_dict() for name, p in self.providers.items()}

    def to_dict(self) -> dict:
        return {
            "strategy": self.default_strategy.value,
            "providers": {name: p.to_dict() for name, p in self.providers.items()},
            "task_routing": self.task_routing,
            "available": self.get_available_providers(),
        }
