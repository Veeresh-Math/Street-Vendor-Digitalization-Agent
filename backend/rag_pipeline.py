"""
RAG Pipeline — Street Vendor Digitalization Agent
Local ChromaDB for search (0 tokens) + IBM Llama for generation (30 tokens max)

Token optimization:
  - Cache-first: return cached answer (0 tokens) if query exists
  - On cache miss: call API with max 30 tokens only
  - Context truncated to 150 chars per doc
  - Embed cache prevents duplicate embed calls
"""

import os
from typing import Optional
import chromadb
from backend.rag_query_cache import get_query_cache, make_cache_key
from chromadb.config import Settings
from backend.ibm_client import embed, embed_query, generate
from backend.knowledge_base import get_all_chunks
from backend.demo_responses import get_demo_response

_cache = get_query_cache()
def _is_demo_mode() -> bool:
    return os.getenv("DEMO_MODE", "false").lower() == "true"

# ── ChromaDB config ──────────────────────────────────────────────────────────
CHROMA_PATH     = os.path.join(os.path.dirname(__file__), "..", "vector_store")
COLLECTION_NAME = "vendor_knowledge"
DEFAULT_TOP_K   = 2
MAX_CONTEXT_CHARS = 150  # truncate each doc to save tokens
MAX_GEN_TOKENS = 30     # max tokens per generation

_chroma_client: Optional[chromadb.PersistentClient] = None
_collection: Optional[chromadb.Collection] = None


def _get_collection() -> chromadb.Collection:
    global _chroma_client, _collection
    if _collection is None:
        _chroma_client = chromadb.PersistentClient(
            path=CHROMA_PATH,
            settings=Settings(anonymized_telemetry=False),
        )
        _collection = _chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


# ── Index Builder ────────────────────────────────────────────────────────────

def build_index(force_rebuild: bool = False, status_cb=None) -> int:
    """Embed docs into ChromaDB (one-time cost). Returns doc count."""
    col    = _get_collection()
    chunks = get_all_chunks()

    existing = col.count()
    if existing >= len(chunks) and not force_rebuild:
        if status_cb:
            status_cb(f"Index ready ({existing} docs).")
        return existing

    if force_rebuild and existing > 0:
        global _collection
        _chroma_client.delete_collection(COLLECTION_NAME)
        _collection = _chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        col = _collection
        # Clear query cache on rebuild to avoid stale answers
        if _cache is not None:
            _cache.clear()

    if status_cb:
        status_cb(f"Embedding {len(chunks)} docs...")

    texts   = [t for t, _ in chunks]
    vectors = embed(texts)

    ids       = [doc["id"] for _, doc in chunks]
    metadatas = [
        {"title": doc["title"], "category": doc["category"],
         "tags": ", ".join(doc.get("tags", [])), "lang": doc.get("language_hint", "en")}
        for _, doc in chunks
    ]

    col.upsert(ids=ids, embeddings=vectors, documents=texts, metadatas=metadatas)
    count = col.count()
    if status_cb:
        status_cb(f"Index built ({count} docs).")
    return count


def is_index_ready() -> bool:
    try:
        return _get_collection().count() > 0
    except Exception:
        return False


def index_doc_count() -> int:
    try:
        return _get_collection().count()
    except Exception:
        return 0


# ── Retrieval ────────────────────────────────────────────────────────────────

def retrieve(query_text: str, top_k: int = DEFAULT_TOP_K) -> list[dict]:
    """Embed query → search ChromaDB → return top-k results."""
    col      = _get_collection()
    q_vector = embed_query(query_text)

    try:
        results = col.query(
            query_embeddings=[q_vector],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
    except Exception as e:
        if "dimension" in str(e).lower() or "embedding" in str(e).lower():
            print(f"[RAG] Dimension mismatch detected — rebuilding index...")
            build_index(force_rebuild=True)
            col = _get_collection()
            results = col.query(
                query_embeddings=[q_vector],
                n_results=top_k,
                include=["documents", "metadatas", "distances"],
            )
        else:
            raise

    hits = []
    for i in range(len(results["ids"][0])):
        dist = results["distances"][0][i]
        hits.append({
            "id":       results["ids"][0][i],
            "title":    results["metadatas"][0][i]["title"],
            "category": results["metadatas"][0][i]["category"],
            "text":     results["documents"][0][i],
            "distance": dist,
            "score":    round(1 - dist, 4),
        })
    return hits


# ── Prompt Builder (optimized for minimal tokens) ────────────────────────────

def _build_prompt(user_query: str, retrieved: list[dict], language: str = "en") -> str:
    lang_instruction = {
        "hi": "Hindi mein jawab dein.",
        "mr": "Marathit jawab dein.",
        "ta": "Tamil-il jawab kodukkunga.",
        "te": "Telugu-lo javabu ivvandi.",
        "kn": "Kannada-nalli uttara kodisi.",
        "gu": "Gujarati-ma javab aapo.",
        "bn": "Bengali-te uttara din.",
        "en": "Reply in simple English.",
    }.get(language, "Reply in simple English.")

    # Truncate each doc to save tokens
    ctx_parts = []
    for i, h in enumerate(retrieved, 1):
        text = h['text'][:MAX_CONTEXT_CHARS]
        ctx_parts.append(f"[{i}] {h['category']}: {text}")
    ctx = "\n".join(ctx_parts)

    lang_name = {"hi":"Hindi","mr":"Marathi","ta":"Tamil","te":"Telugu",
                 "kn":"Kannada","gu":"Gujarati","bn":"Bengali"}.get(language, "English")

    return f"""Street Vendor Agent. {lang_instruction}

Context: {ctx}

Question: {user_query}

Answer briefly (2-3 sentences). Use {lang_name}."""


# ── Main Query Function ──────────────────────────────────────────────────────

def answer(user_query: str, top_k: int = DEFAULT_TOP_K, language: str = "en",
           status_cb=None) -> dict:
    """
    Token-smart RAG pipeline:
      1. Check demo cache → 0 tokens
      2. Check query cache → 0 tokens (API skipped)
      3. Cache miss → embed (15 tokens) + generate (30 tokens) = 45 tokens max
    """
    # ── Demo mode: 0 tokens ──────────────────────────────────────────────
    if _is_demo_mode():
        demo_resp = get_demo_response(user_query, language)
        if demo_resp:
            return {"answer": demo_resp, "retrieved_docs": [], "query": user_query,
                    "gen_model": "demo-cached", "embed_model": "none",
                    "language": language, "top_k": top_k}
        return {"answer": "I can help with UPI, PM SVANidhi, Google Maps, FSSAI. Ask about these!",
                "retrieved_docs": [], "query": user_query,
                "gen_model": "demo-fallback", "embed_model": "none",
                "language": language, "top_k": top_k}

    # ── Query cache check FIRST (0 tokens) ───────────────────────────────
    cache_key = make_cache_key(user_query, language, top_k)
    if _cache is not None:
        cached = _cache.get(cache_key)
        if cached is not None:
            if status_cb:
                status_cb("[CACHE] Hit! 0 tokens used.")
            return {"answer": cached, "retrieved_docs": [], "query": user_query,
                    "gen_model": "cache-hit", "embed_model": "none",
                    "language": language, "top_k": top_k}

    # ── Real mode: need index ────────────────────────────────────────────
    if not is_index_ready():
        if status_cb:
            status_cb("[AUTO] Building index first time...")
        build_index(status_cb=status_cb)

    if status_cb:
        status_cb("[1] Embedding query (15 tokens)...")

    retrieved = retrieve(user_query, top_k=top_k)

    if status_cb:
        status_cb(f"[2] Found {len(retrieved)} docs.")
        for r in retrieved:
            status_cb(f"    [{r['category']}] {r['title']} (score: {r['score']})")

    prompt = _build_prompt(user_query, retrieved, language)

    if status_cb:
        status_cb("[3] Generating with Llama (30 tokens max)...")

    # Use 30 tokens max only
    answer_text = generate(prompt, max_tokens=MAX_GEN_TOKENS)

    # Cache the result
    if _cache is not None:
        _cache.set(cache_key, answer_text)

    return {"answer": answer_text, "retrieved_docs": retrieved, "query": user_query,
            "gen_model": "meta-llama/llama-3-3-70b-instruct",
            "embed_model": "intfloat/multilingual-e5-large",
            "language": language, "top_k": top_k}
