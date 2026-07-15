"""
IBM watsonx.ai Client
Uses the official ibm-watsonx-ai Python SDK.
Models:
  - Generation : meta-llama/llama-3-3-70b-instruct
  - Embeddings : intfloat/multilingual-e5-large
Region: Sydney (au-syd)
"""

import os
import json
import time
import threading
from datetime import date
from collections import OrderedDict
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.embeddings import Embeddings
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames as EmbedParams

# Load .env from backend/ directory (only for local dev, Render env vars take priority)
_backend_dir = os.path.dirname(os.path.abspath(__file__))
_dotenv_path = os.path.join(_backend_dir, ".env")
if os.path.exists(_dotenv_path):
    load_dotenv(_dotenv_path, override=False)

# ── Token Daily Caps ─────────────────────────────────────────────────────────
DAILY_EMBED_TOKEN_LIMIT = int(os.getenv("DAILY_EMBED_LIMIT", "5000"))
DAILY_GEN_TOKEN_LIMIT   = int(os.getenv("DAILY_GEN_LIMIT", "10000"))

# ── Thread-safe Token Tracking ───────────────────────────────────────────────
_TOKEN_FILE = os.path.join(_backend_dir, ".token_usage.json")
_token_lock = threading.Lock()

def _load_token_usage() -> dict:
    """Load daily token usage from disk. Resets if date changed."""
    today = date.today().isoformat()
    default = {"date": today, "embed_tokens": 0, "gen_tokens": 0,
               "embed_calls": 0, "gen_calls": 0}
    try:
        with open(_TOKEN_FILE, "r") as f:
            data = json.load(f)
        if data.get("date") != today:
            return default
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def _save_token_usage(data: dict):
    with open(_TOKEN_FILE, "w") as f:
        json.dump(data, f)

def _update_token_usage(field: str, increment: int) -> dict:
    """Thread-safe token usage update. Returns updated usage dict."""
    with _token_lock:
        usage = _load_token_usage()
        usage[field] += increment
        _save_token_usage(usage)
        return usage

# ── Embedding Cache (saves IBM API calls for repeated queries) ──────────────
_EMBED_CACHE_MAX = 2000
_embed_cache: OrderedDict[str, list[float]] = OrderedDict()
_embed_cache_lock = threading.Lock()

# ── Credentials (read at runtime, not import time) ─────────────────────────
def _get_env(key: str, default: str = "") -> str:
    """Read env var at runtime (not import-time) so Render env vars are always picked up."""
    return os.getenv(key, default)

# Model IDs
GEN_MODEL_ID   = "meta-llama/llama-3-3-70b-instruct"
EMBED_MODEL_ID = "intfloat/multilingual-e5-large"

# ── SDK Client (singleton) ────────────────────────────────────────────────────
_client: APIClient | None = None

def _get_client() -> APIClient:
    global _client
    if _client is None:
        api_key = _get_env("IBM_API_KEY")
        project_id = _get_env("IBM_PROJECT_ID")
        url = _get_env("IBM_URL", "https://au-syd.ml.cloud.ibm.com")
        if not api_key or not project_id:
            raise ValueError("IBM_API_KEY or IBM_PROJECT_ID not set. Check Render environment variables.")
        creds   = Credentials(url=url, api_key=api_key)
        _client = APIClient(credentials=creds, project_id=project_id)
    return _client


# ── Generation Model ──────────────────────────────────────────────────────────
_gen_model: ModelInference | None = None

def _get_gen_model() -> ModelInference:
    global _gen_model
    if _gen_model is None:
        _gen_model = ModelInference(
            model_id   = GEN_MODEL_ID,
            api_client = _get_client(),
            params     = {
                GenParams.DECODING_METHOD  : "greedy",
                GenParams.MAX_NEW_TOKENS   : 30,
                GenParams.MIN_NEW_TOKENS   : 5,
                GenParams.REPETITION_PENALTY: 1.1,
            },
        )
    return _gen_model


# ── Embedding Model ───────────────────────────────────────────────────────────
_embed_model: Embeddings | None = None

def _get_embed_model() -> Embeddings:
    global _embed_model
    if _embed_model is None:
        _embed_model = Embeddings(
            model_id   = EMBED_MODEL_ID,
            api_client = _get_client(),
            params     = {
                EmbedParams.TRUNCATE_INPUT_TOKENS: 256,
            },
        )
    return _embed_model


# ── Public API ────────────────────────────────────────────────────────────────

def generate(prompt: str, max_tokens: int = 30, retries: int = 3) -> str:
    """Generate text with daily token cap."""
    usage = _load_token_usage()

    if usage["gen_tokens"] >= DAILY_GEN_TOKEN_LIMIT:
        return "I can help with UPI, PM SVANidhi, Google Maps, FSSAI. Please ask about these topics."

    model = _get_gen_model()
    last_err = None
    for attempt in range(retries):
        try:
            response = model.generate_text(
                prompt=prompt,
                params={GenParams.MAX_NEW_TOKENS: max_tokens},
            )
            _update_token_usage("gen_calls", 1)
            _update_token_usage("gen_tokens", max_tokens)
            return response.strip() if isinstance(response, str) else response
        except Exception as e:
            last_err = e
            err_str = str(e).lower()
            if "429" in err_str or "rate" in err_str or "limit" in err_str or "consumption" in err_str:
                wait = 3 * (attempt + 1)
                print(f"[IBM] Rate limited ({attempt+1}/{retries}), retry in {wait}s...")
                time.sleep(wait)
            else:
                raise
    raise last_err


def embed(texts: list[str], retries: int = 3) -> list[list[float]]:
    """Embed texts with daily token cap."""
    usage = _load_token_usage()

    # Estimate actual tokens: ~4 chars per token for multilingual-e5-large
    estimated_tokens = sum(max(1, len(t) // 4) for t in texts)

    if usage["embed_tokens"] + estimated_tokens > DAILY_EMBED_TOKEN_LIMIT:
        print(f"[IBM] Embed budget exceeded ({usage['embed_tokens']}/{DAILY_EMBED_TOKEN_LIMIT}). Skipping.")
        return [[0.0] * 384 for _ in texts]

    model = _get_embed_model()
    last_err = None
    for attempt in range(retries):
        try:
            result = model.embed_documents(texts=texts)
            _update_token_usage("embed_calls", len(texts))
            _update_token_usage("embed_tokens", estimated_tokens)
            return result
        except Exception as e:
            last_err = e
            err_str = str(e).lower()
            if "429" in err_str or "rate" in err_str or "limit" in err_str or "consumption" in err_str:
                wait = 3 * (attempt + 1)
                print(f"[IBM] Embed rate limited ({attempt+1}/{retries}), retry in {wait}s...")
                time.sleep(wait)
            else:
                raise
    raise last_err


def embed_query(text: str) -> list[float]:
    """Embed a single query string. Returns one float vector. Uses cache for repeated queries."""
    cache_key = text.strip().lower()
    with _embed_cache_lock:
        if cache_key in _embed_cache:
            _embed_cache.move_to_end(cache_key)
            return _embed_cache[cache_key]
    vecs = embed([text])
    with _embed_cache_lock:
        _embed_cache[cache_key] = vecs[0]
        if len(_embed_cache) > _EMBED_CACHE_MAX:
            _embed_cache.popitem(last=False)
    return vecs[0]


def health_check() -> dict:
    """Verify IBM Cloud connection and return model info."""
    try:
        client = _get_client()
        return {
            "status"      : "connected",
            "url"         : _get_env("IBM_URL", "https://au-syd.ml.cloud.ibm.com"),
            "project_id"  : _get_env("IBM_PROJECT_ID"),
            "gen_model"   : GEN_MODEL_ID,
            "embed_model" : EMBED_MODEL_ID,
            "vector_store": _get_env("IBM_VECTOR_STORE_ID"),
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def get_token_usage() -> dict:
    """Return persistent daily token usage statistics."""
    usage = _load_token_usage()
    return {
        "embed_calls": usage["embed_calls"],
        "gen_calls": usage["gen_calls"],
        "embed_tokens_today": usage["embed_tokens"],
        "gen_tokens_today": usage["gen_tokens"],
        "embed_cache_size": len(_embed_cache),
        "embed_cache_max": _EMBED_CACHE_MAX,
        "daily_embed_limit": DAILY_EMBED_TOKEN_LIMIT,
        "daily_gen_limit": DAILY_GEN_TOKEN_LIMIT,
    }
