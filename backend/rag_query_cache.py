"""Simple opt-in query caching for RAG.

Constraints:
- Additive only: does not change API schema/behavior on cache miss.
- Default disabled unless explicitly enabled.
- Uses in-memory LRU+TTL (stdlib only).
"""

from __future__ import annotations

import os
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Optional


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass
class CacheEntry:
    value: Any
    expires_at: float


class TTLLRUCache:
    def __init__(self, maxsize: int, ttl_seconds: int):
        self.maxsize = max(1, int(maxsize))
        self.ttl_seconds = max(0, int(ttl_seconds))
        self._data: "OrderedDict[str, CacheEntry]" = OrderedDict()

    def _now(self) -> float:
        return time.time()

    def get(self, key: str) -> Optional[Any]:
        entry = self._data.get(key)
        if entry is None:
            return None

        if self.ttl_seconds > 0 and entry.expires_at < self._now():
            # expired: remove and treat as miss
            self._data.pop(key, None)
            return None

        # refresh LRU order
        self._data.move_to_end(key)
        return entry.value

    def set(self, key: str, value: Any) -> None:
        if self._data.get(key) is not None:
            self._data.pop(key, None)

        expires_at = self._now() + self.ttl_seconds if self.ttl_seconds > 0 else float("inf")
        self._data[key] = CacheEntry(value=value, expires_at=expires_at)
        self._data.move_to_end(key)

        # evict least-recently-used
        while len(self._data) > self.maxsize:
            self._data.popitem(last=False)


# Module-level singleton
RAG_QUERY_CACHE_ENABLED = _env_bool("RAG_QUERY_CACHE_ENABLED", True)
RAG_QUERY_CACHE_TTL_SECONDS = int(os.getenv("RAG_QUERY_CACHE_TTL_SECONDS", "1800"))
RAG_QUERY_CACHE_MAXSIZE = int(os.getenv("RAG_QUERY_CACHE_MAXSIZE", "1000"))

_query_cache: TTLLRUCache | None = None


def get_query_cache() -> Optional[TTLLRUCache]:
    global _query_cache
    if not RAG_QUERY_CACHE_ENABLED:
        return None
    if _query_cache is None:
        _query_cache = TTLLRUCache(
            maxsize=RAG_QUERY_CACHE_MAXSIZE,
            ttl_seconds=RAG_QUERY_CACHE_TTL_SECONDS,
        )
    return _query_cache


def make_cache_key(*parts: Any) -> str:
    # stable string key without importing hashlib unless needed
    # (cache correctness > cryptographic properties)
    return "|".join([str(p) if p is not None else "" for p in parts])

