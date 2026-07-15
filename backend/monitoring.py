"""
Structured logging / monitoring hooks for SVDA.
Additive only — does not alter any API responses.

Usage:
    from backend.monitoring import RequestLogger
    logger = RequestLogger()
    # In middleware or endpoint:
    logger.log_request("POST", "/api/query", status_code=200, latency_ms=342.5)
"""

import os
import time
import logging
from dataclasses import dataclass, field
from collections import deque
from typing import Optional


# ── Configuration ─────────────────────────────────────────────────────────────

LOG_LEVEL = os.getenv("SVDA_LOG_LEVEL", "INFO").upper()
MONITORING_ENABLED = os.getenv("SVDA_MONITORING_ENABLED", "true").lower() in {"1", "true", "yes"}


# ── Logger Setup ──────────────────────────────────────────────────────────────

def get_logger(name: str = "svda.monitoring") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = logging.Formatter(
            "[%(asctime)s] %(levelname)s %(name)s — %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
    return logger


# ── Request Log Entry ─────────────────────────────────────────────────────────

@dataclass
class RequestLogEntry:
    method: str
    path: str
    status_code: int
    latency_ms: float
    timestamp: float = field(default_factory=time.time)
    detail: Optional[str] = None


class RequestLogger:
    """In-memory circular buffer of recent request logs + stats."""

    def __init__(self, max_entries: int = 500):
        self._entries: deque[RequestLogEntry] = deque(maxlen=max_entries)
        self._logger = get_logger()
        self._total_requests = 0
        self._total_errors = 0
        self._total_latency_ms = 0.0

    def log_request(
        self,
        method: str,
        path: str,
        status_code: int,
        latency_ms: float,
        detail: Optional[str] = None,
    ) -> None:
        if not MONITORING_ENABLED:
            return

        entry = RequestLogEntry(
            method=method,
            path=path,
            status_code=status_code,
            latency_ms=round(latency_ms, 2),
            detail=detail,
        )
        self._entries.append(entry)
        self._total_requests += 1
        self._total_latency_ms += latency_ms
        if status_code >= 400:
            self._total_errors += 1

        level = logging.WARNING if status_code >= 400 else logging.INFO
        self._logger.log(
            level,
            "%s %s -> %d (%.1fms)%s",
            method,
            path,
            status_code,
            latency_ms,
            f" -- {detail}" if detail else "",
        )

    def get_stats(self) -> dict:
        avg_latency = (
            self._total_latency_ms / self._total_requests
            if self._total_requests > 0
            else 0.0
        )
        return {
            "total_requests": self._total_requests,
            "total_errors": self._total_errors,
            "avg_latency_ms": round(avg_latency, 2),
            "recent_entries": len(self._entries),
        }

    def get_recent(self, n: int = 20) -> list[dict]:
        entries = list(self._entries)[-n:]
        return [
            {
                "method": e.method,
                "path": e.path,
                "status_code": e.status_code,
                "latency_ms": e.latency_ms,
                "timestamp": e.timestamp,
                "detail": e.detail,
            }
            for e in entries
        ]


# ── Module-level singleton ────────────────────────────────────────────────────
request_logger = RequestLogger()
