"""
Knowledge Updater Worker — Scheduled refresh of the ChromaDB vector index.

This worker runs independently of the main FastAPI app and can be triggered
via cron, systemd timer, or manually. It does NOT affect the runtime application.

Usage:
    python -m backend.knowledge_updater.worker [--force] [--interval 3600]

The worker will:
1. Check if the knowledge base has changed since the last index build
2. Re-embed any new/updated documents
3. Rebuild the ChromaDB vector index if needed
4. Log the results

Configuration via environment variables:
    SVDA_UPDATE_INTERVAL  — Seconds between checks (default: 3600)
    SVDA_UPDATE_ENABLED   — Enable/disable the worker (default: false)
    SVDA_LOG_LEVEL        — Logging level (default: INFO)
"""

import os
import sys
import time
import signal
import logging
from datetime import datetime, timezone

# Ensure the project root is on the path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

from backend.monitoring import get_logger

logger = get_logger("svda.knowledge_updater")

# ── Configuration ─────────────────────────────────────────────────────────────

UPDATE_INTERVAL = int(os.getenv("SVDA_UPDATE_INTERVAL", "3600"))
UPDATE_ENABLED = os.getenv("SVDA_UPDATE_ENABLED", "false").lower() in {"1", "true", "yes"}
LAST_UPDATE_FILE = os.path.join(BASE_DIR, "data", "last_knowledge_update.txt")

# ── Graceful Shutdown ────────────────────────────────────────────────────────

_running = True


def _signal_handler(signum, frame):
    global _running
    logger.info("Shutdown signal received. Stopping worker...")
    _running = False


signal.signal(signal.SIGINT, _signal_handler)
signal.signal(signal.SIGTERM, _signal_handler)


# ── Core Logic ────────────────────────────────────────────────────────────────

def _get_last_update_time() -> float:
    """Return the last update timestamp, or 0 if never updated."""
    if os.path.exists(LAST_UPDATE_FILE):
        try:
            with open(LAST_UPDATE_FILE, "r") as f:
                return float(f.read().strip())
        except (ValueError, IOError):
            return 0.0
    return 0.0


def _save_last_update_time(ts: float) -> None:
    """Save the last update timestamp."""
    os.makedirs(os.path.dirname(LAST_UPDATE_FILE), exist_ok=True)
    with open(LAST_UPDATE_FILE, "w") as f:
        f.write(str(ts))


def _knowledge_base_changed() -> bool:
    """Check if any knowledge base files were modified since the last update."""
    last_update = _get_last_update_time()
    kb_path = os.path.join(BASE_DIR, "backend", "knowledge_base.py")
    try:
        mtime = os.path.getmtime(kb_path)
        return mtime > last_update
    except OSError:
        return False


def run_update(force: bool = False) -> dict:
    """
    Check for changes and rebuild the index if needed.
    Returns a status dict.
    """
    from backend.rag_pipeline import build_index, is_index_ready, index_doc_count

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": "none",
        "doc_count": 0,
        "success": True,
        "message": "",
    }

    try:
        if not force and not _knowledge_base_changed():
            result["message"] = "No changes detected. Skipping rebuild."
            result["doc_count"] = index_doc_count()
            return result

        logger.info("Knowledge base changed or force rebuild requested. Rebuilding index...")
        count = build_index(force_rebuild=force)
        _save_last_update_time(time.time())

        result["action"] = "rebuilt"
        result["doc_count"] = count
        result["message"] = f"Index rebuilt successfully with {count} documents."
        logger.info(result["message"])

    except Exception as e:
        result["success"] = False
        result["message"] = f"Update failed: {e}"
        logger.error(result["message"])

    return result


def run_worker(interval: int = UPDATE_INTERVAL) -> None:
    """Run the worker loop, checking for updates every `interval` seconds."""
    logger.info(
        "Knowledge Updater Worker started. interval=%ds, enabled=%s",
        interval,
        UPDATE_ENABLED,
    )

    if not UPDATE_ENABLED:
        logger.info("Worker is disabled (SVDA_UPDATE_ENABLED=false). Exiting.")
        return

    while _running:
        try:
            result = run_update()
            logger.info("Update check: %s", result["message"])
        except Exception as e:
            logger.error("Worker error: %s", e)

        # Sleep in small increments so we can respond to shutdown signals
        for _ in range(interval):
            if not _running:
                break
            time.sleep(1)

    logger.info("Knowledge Updater Worker stopped.")


# ── CLI Entry Point ───────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description="SVDA Knowledge Updater Worker")
    parser.add_argument("--force", action="store_true", help="Force rebuild even if no changes detected")
    parser.add_argument("--interval", type=int, default=UPDATE_INTERVAL, help="Check interval in seconds")
    parser.add_argument("--once", action="store_true", help="Run a single update check and exit")
    args = parser.parse_args()

    if args.once:
        result = run_update(force=args.force)
        print(result["message"])
        sys.exit(0 if result["success"] else 1)
    else:
        run_worker(interval=args.interval)


if __name__ == "__main__":
    main()
