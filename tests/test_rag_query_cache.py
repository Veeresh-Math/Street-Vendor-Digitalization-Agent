"""
Tests for the RAG query cache module (TTLLRUCache).
"""

import time
import pytest
from backend.rag_query_cache import TTLLRUCache, get_query_cache, make_cache_key


class TestTTLLRUCache:
    """Tests for the TTLLRUCache class."""

    def test_set_and_get(self):
        cache = TTLLRUCache(maxsize=10, ttl_seconds=60)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

    def test_get_missing_key(self):
        cache = TTLLRUCache(maxsize=10, ttl_seconds=60)
        assert cache.get("nonexistent") is None

    def test_lru_eviction(self):
        cache = TTLLRUCache(maxsize=3, ttl_seconds=60)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        # Adding a 4th should evict "a" (least recently used)
        cache.set("d", 4)
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.get("c") == 3
        assert cache.get("d") == 4

    def test_lru_refresh_on_get(self):
        cache = TTLLRUCache(maxsize=3, ttl_seconds=60)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        # Access "a" to refresh it
        cache.get("a")
        # Now adding "d" should evict "b" (least recently used)
        cache.set("d", 4)
        assert cache.get("a") == 1
        assert cache.get("b") is None
        assert cache.get("c") == 3
        assert cache.get("d") == 4

    def test_ttl_expiration(self):
        cache = TTLLRUCache(maxsize=10, ttl_seconds=1)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        # Wait for expiration
        time.sleep(1.1)
        assert cache.get("key1") is None

    def test_zero_ttl_never_expires(self):
        cache = TTLLRUCache(maxsize=10, ttl_seconds=0)
        cache.set("key1", "value1")
        # With ttl_seconds=0, expires_at is float("inf"), so it never expires
        assert cache.get("key1") == "value1"

    def test_overwrite_existing_key(self):
        cache = TTLLRUCache(maxsize=3, ttl_seconds=60)
        cache.set("a", 1)
        cache.set("a", 2)
        assert cache.get("a") == 2
        # Should still only count as 1 entry
        cache.set("b", 3)
        cache.set("c", 4)
        # All 3 should fit
        assert cache.get("a") == 2
        assert cache.get("b") == 3
        assert cache.get("c") == 4

    def test_maxsize_one(self):
        cache = TTLLRUCache(maxsize=1, ttl_seconds=60)
        cache.set("a", 1)
        assert cache.get("a") == 1
        cache.set("b", 2)
        assert cache.get("a") is None
        assert cache.get("b") == 2


class TestGetQueryCache:
    """Tests for the get_query_cache singleton."""

    def test_returns_cache_when_enabled(self):
        cache = get_query_cache()
        # Should return a TTLLRUCache instance (or None if disabled)
        if cache is not None:
            assert isinstance(cache, TTLLRUCache)

    def test_singleton_behavior(self):
        cache1 = get_query_cache()
        cache2 = get_query_cache()
        if cache1 is not None:
            assert cache1 is cache2


class TestMakeCacheKey:
    """Tests for the make_cache_key helper."""

    def test_simple_key(self):
        key = make_cache_key("query", "en", 3)
        assert key == "query|en|3"

    def test_none_handling(self):
        key = make_cache_key("query", None, 3)
        assert key == "query||3"

    def test_single_part(self):
        key = make_cache_key("hello")
        assert key == "hello"
