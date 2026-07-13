"""
IBM watsonx.ai Client
Uses the official ibm-watsonx-ai Python SDK.
Models:
  - Generation : ibm/granite-4-h-small
  - Embeddings : ibm/granite-embedding-278m-multilingual
"""

import os
import time
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.embeddings import Embeddings
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames as EmbedParams

load_dotenv()

# ── Credentials ───────────────────────────────────────────────────────────────
IBM_API_KEY    = os.getenv("IBM_API_KEY",    "")
IBM_PROJECT_ID = os.getenv("IBM_PROJECT_ID", "")
IBM_URL        = os.getenv("IBM_URL",        "https://us-south.ml.cloud.ibm.com")

# Model IDs — mandatory per problem statement
GEN_MODEL_ID   = "ibm/granite-4-h-small"
EMBED_MODEL_ID = "ibm/granite-embedding-278m-multilingual"

# ── SDK Client (singleton) ────────────────────────────────────────────────────
_client: APIClient | None = None

def _get_client() -> APIClient:
    global _client
    if _client is None:
        creds   = Credentials(url=IBM_URL, api_key=IBM_API_KEY)
        _client = APIClient(credentials=creds, project_id=IBM_PROJECT_ID)
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
                GenParams.MAX_NEW_TOKENS   : 600,
                GenParams.MIN_NEW_TOKENS   : 60,
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
                EmbedParams.TRUNCATE_INPUT_TOKENS: 512,
            },
        )
    return _embed_model


# ── Public API ────────────────────────────────────────────────────────────────

def generate(prompt: str, max_tokens: int = 600, retries: int = 3) -> str:
    """
    Generate text using ibm/granite-4-h-small with retry on rate limit.
    Returns the generated string.
    """
    model = _get_gen_model()
    last_err = None
    for attempt in range(retries):
        try:
            response = model.generate_text(
                prompt = prompt,
                params = {
                    GenParams.MAX_NEW_TOKENS: max_tokens,
                },
            )
            return response.strip() if isinstance(response, str) else response
        except Exception as e:
            last_err = e
            err_str = str(e).lower()
            if "429" in err_str or "rate" in err_str or "limit" in err_str or "consumption" in err_str:
                wait = 3 * (attempt + 1)
                print(f"[IBM] Rate limited (attempt {attempt+1}/{retries}), retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise
    raise last_err


def embed(texts: list[str], retries: int = 3) -> list[list[float]]:
    """
    Embed a list of texts using ibm/granite-embedding-278m-multilingual with retry.
    Returns list of float vectors.
    """
    model  = _get_embed_model()
    last_err = None
    for attempt in range(retries):
        try:
            result = model.embed_documents(texts=texts)
            return result
        except Exception as e:
            last_err = e
            err_str = str(e).lower()
            if "429" in err_str or "rate" in err_str or "limit" in err_str or "consumption" in err_str:
                wait = 3 * (attempt + 1)
                print(f"[IBM] Embed rate limited (attempt {attempt+1}/{retries}), retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise
    raise last_err


def embed_query(text: str) -> list[float]:
    """Embed a single query string. Returns one float vector."""
    vecs = embed([text])
    return vecs[0]


def health_check() -> dict:
    """Verify IBM Cloud connection and return model info."""
    try:
        client = _get_client()
        return {
            "status"      : "connected",
            "url"         : IBM_URL,
            "project_id"  : IBM_PROJECT_ID,
            "gen_model"   : GEN_MODEL_ID,
            "embed_model" : EMBED_MODEL_ID,
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}
