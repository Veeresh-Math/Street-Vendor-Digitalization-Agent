"""Compatibility shim for deployment platforms.

Some platforms auto-detect `app.py` as the entrypoint.
We re-export the FastAPI app from `backend.main` as a top-level `app`
so those platforms work without extra configuration.
"""

from backend.main import app  # noqa: F401

