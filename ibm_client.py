"""
IBM watsonx.ai Client
Handles IAM token, embeddings (granite-embedding-278m-multilingual),
and text generation (granite-4-h-small).
"""

import requests
import os
from datetime import datetime, timedelta

# ── IBM Cloud Configuration ──────────────────────────────────────────────────
IBM_API_KEY   = os.getenv("IBM_API_KEY",   "36yHNYbA0YjOeTsl1xGDXQ_5e-KcvJm7-7OQQWzZuolv")
IBM_PROJECT_ID= os.getenv("IBM_PROJECT_ID","59f569dc-3371-40a4-a6dc-0d6242c0745e")
IBM_ENDPOINT  = os.getenv("IBM_ENDPOINT",  "https://us-south.ml.cloud.ibm.com")
IBM_VERSION   = "2024-05-01"

GEN_MODEL   = "ibm/granite-4-h-small"
EMBED_MODEL = "ibm/granite-embedding-278m-multilingual"

IAM_URL = "https://iam.cloud.ibm.com/identity/token"

# ── Token Cache ───────────────────────────────────────────────────────────────
_token_cache = {"token": None, "expires_at": datetime.min}


def get_iam_token() -> str:
    """Fetch (or return cached) IBM IAM Bearer token."""
    global _token_cache
    if _token_cache["token"] and datetime.utcnow() < _token_cache["expires_at"]:
        return _token_cache["token"]

    resp = requests.post(
        IAM_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": IBM_API_KEY,
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    _token_cache["token"]      = data["access_token"]
    _token_cache["expires_at"] = datetime.utcnow() + timedelta(seconds=data.get("expires_in", 3600) - 120)
    return _token_cache["token"]


def get_embedding(text: str) -> list[float]:
    """
    Embed a text string using granite-embedding-278m-multilingual.
    Returns a float vector (list).
    """
    token = get_iam_token()
    resp  = requests.post(
        f"{IBM_ENDPOINT}/ml/v1/text/embeddings?version={IBM_VERSION}",
        headers={
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {token}",
        },
        json={
            "model_id":   EMBED_MODEL,
            "inputs":     [text],
            "project_id": IBM_PROJECT_ID,
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["results"][0]["embedding"]


def generate_text(prompt: str, max_tokens: int = 500) -> str:
    """
    Generate a response using granite-4-h-small.
    Returns the generated text string.
    """
    token = get_iam_token()
    resp  = requests.post(
        f"{IBM_ENDPOINT}/ml/v1/text/generation?version={IBM_VERSION}",
        headers={
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {token}",
        },
        json={
            "model_id": GEN_MODEL,
            "input":    prompt,
            "parameters": {
                "decoding_method":  "greedy",
                "max_new_tokens":   max_tokens,
                "min_new_tokens":   60,
                "repetition_penalty": 1.1,
            },
            "project_id": IBM_PROJECT_ID,
        },
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["results"][0]["generated_text"].strip()
