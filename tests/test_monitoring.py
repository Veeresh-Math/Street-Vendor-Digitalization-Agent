"""
Tests for the monitoring module.
"""

import pytest
from backend.monitoring import RequestLogger, get_logger, request_logger


class TestRequestLogger:
    """Tests for the RequestLogger class."""

    def test_log_request(self):
        logger = RequestLogger()
        logger.log_request("GET", "/api/health", status_code=200, latency_ms=15.3)
        stats = logger.get_stats()
        assert stats["total_requests"] == 1
        assert stats["total_errors"] == 0
        assert stats["avg_latency_ms"] > 0

    def test_log_error_request(self):
        logger = RequestLogger()
        logger.log_request("POST", "/api/query", status_code=500, latency_ms=100.0)
        stats = logger.get_stats()
        assert stats["total_requests"] == 1
        assert stats["total_errors"] == 1

    def test_get_recent(self):
        logger = RequestLogger()
        for i in range(5):
            logger.log_request("GET", f"/api/test/{i}", status_code=200, latency_ms=10.0)
        recent = logger.get_recent(n=3)
        assert len(recent) == 3
        assert recent[0]["path"] == "/api/test/2"
        assert recent[2]["path"] == "/api/test/4"

    def test_max_entries_limit(self):
        logger = RequestLogger(max_entries=3)
        for i in range(5):
            logger.log_request("GET", f"/api/{i}", status_code=200, latency_ms=1.0)
        stats = logger.get_stats()
        assert stats["recent_entries"] == 3

    def test_avg_latency_calculation(self):
        logger = RequestLogger()
        logger.log_request("GET", "/a", status_code=200, latency_ms=100.0)
        logger.log_request("GET", "/b", status_code=200, latency_ms=200.0)
        stats = logger.get_stats()
        assert stats["avg_latency_ms"] == 150.0


class TestGetLogger:
    """Tests for the get_logger helper."""

    def test_returns_logger(self):
        import logging
        logger = get_logger("test")
        assert isinstance(logger, logging.Logger)

    def test_logger_name(self):
        logger = get_logger("my_test")
        assert logger.name == "my_test"


class TestModuleSingleton:
    """Tests for the module-level request_logger singleton."""

    def test_singleton_exists(self):
        assert isinstance(request_logger, RequestLogger)
