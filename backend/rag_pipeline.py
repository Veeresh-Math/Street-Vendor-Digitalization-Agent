"""
RAG Pipeline — Street Vendor Digitalization Agent
ChromaDB (local persistent) + ibm/granite-embedding-278m-multilingual + ibm/granite-4-h-small

Flow:
  build_index()  → embed all knowledge base docs → store in ChromaDB collection
  query()        → embed user query → cosine search → top-k docs → augmented prompt → generate
"""

import os
from typing import Optional
import chromadb
from chromadb.config import Settings
from backend.ibm_client import embed, embed_query, generate
from backend.knowledge_base import get_all_chunks, get_all_documents

# ── ChromaDB config ───────────────────────────────────────────────────────────
CHROMA_PATH       = os.path.join(os.path.dirname(__file__), "..", "vector_store")
COLLECTION_NAME   = "vendor_knowledge"
DEFAULT_TOP_K     = 3

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


# ── Index Builder ─────────────────────────────────────────────────────────────

def build_index(force_rebuild: bool = False, status_cb=None) -> int:
    """
    Embed all knowledge base documents and upsert into ChromaDB.
    Skips already-embedded docs unless force_rebuild=True.
    Returns number of documents in collection after build.
    """
    col   = _get_collection()
    chunks = get_all_chunks()   # [(text_to_embed, doc_metadata), ...]

    # Check existing count
    existing = col.count()
    if existing >= len(chunks) and not force_rebuild:
        if status_cb:
            status_cb(f"✅ Index already up to date ({existing} docs). Skipping rebuild.")
        return existing

    if force_rebuild and existing > 0:
        # Delete and recreate collection
        global _collection
        _chroma_client.delete_collection(COLLECTION_NAME)
        _collection = _chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        col = _collection

    if status_cb:
        status_cb(f"[EMBED] Embedding {len(chunks)} documents with granite-embedding-278m-multilingual...")

    # Batch embed (IBM SDK accepts list)
    texts    = [t for t, _ in chunks]
    vectors  = embed(texts)      # list[list[float]]

    ids       = [doc["id"]      for _, doc in chunks]
    metadatas = [
        {
            "title"    : doc["title"],
            "category" : doc["category"],
            "tags"     : ", ".join(doc.get("tags", [])),
            "lang"     : doc.get("language_hint", "en"),
        }
        for _, doc in chunks
    ]
    documents_text = [t for t, _ in chunks]

    col.upsert(
        ids        = ids,
        embeddings = vectors,
        documents  = documents_text,
        metadatas  = metadatas,
    )

    count = col.count()
    if status_cb:
        status_cb(f"[DONE] Vector index built -- {count} documents stored in ChromaDB.")
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


# ── Retrieval ─────────────────────────────────────────────────────────────────

def retrieve(query_text: str, top_k: int = DEFAULT_TOP_K) -> list[dict]:
    """
    Embed query → cosine search in ChromaDB → return top-k results.
    Returns list of:
      { "id", "title", "category", "text", "distance", "score" }
    """
    col       = _get_collection()
    q_vector  = embed_query(query_text)   # single vector from IBM

    results = col.query(
        query_embeddings = [q_vector],
        n_results        = top_k,
        include          = ["documents", "metadatas", "distances"],
    )

    hits = []
    for i in range(len(results["ids"][0])):
        dist = results["distances"][0][i]
        hits.append({
            "id"       : results["ids"][0][i],
            "title"    : results["metadatas"][0][i]["title"],
            "category" : results["metadatas"][0][i]["category"],
            "text"     : results["documents"][0][i],
            "distance" : dist,
            "score"    : round(1 - dist, 4),  # cosine similarity = 1 - cosine distance
        })
    return hits


# ── Prompt Builder ────────────────────────────────────────────────────────────

def _build_prompt(user_query: str, retrieved: list[dict], language: str = "en") -> str:
    lang_instruction = {
        "hi": "Respond in Hindi (Devanagari script). Use simple, conversational Hindi.",
        "mr": "Respond in Marathi (Devanagari script). Use simple, conversational Marathi.",
        "ta": "Respond in Tamil script. Use simple Tamil.",
        "te": "Respond in Telugu script. Use simple Telugu.",
        "kn": "Respond in Kannada script. Use simple Kannada.",
        "gu": "Respond in Gujarati script. Use simple Gujarati.",
        "bn": "Respond in Bengali script. Use simple Bengali.",
        "en": "Respond in clear, simple English.",
    }.get(language, "Respond in clear, simple English.")

    context_blocks = []
    for i, hit in enumerate(retrieved, 1):
        context_blocks.append(
            f"[Document {i}] {hit['category']} - {hit['title']}\n{hit['text']}"
        )
    context_str = "\n\n".join(context_blocks)

    prompt = f"""You are the Street Vendor Digitalization Agent, an AI assistant for the AICTE-IBM SkillsBuild Internship 2026 (Problem Statement No. 29).
Your mission: help Indian street vendors and hawkers become digitally visible and grow their business.
{lang_instruction}

Use ONLY the information from the documents below. Do not invent schemes, links, or phone numbers.

--- RETRIEVED KNOWLEDGE ---
{context_str}
--- END OF KNOWLEDGE ---

Vendor's query: "{user_query}"

Provide a structured, friendly, actionable response with these sections (use only what is relevant):
[1] Digital Payment Setup (UPI / QR steps)
[2] Online Listing Platforms (specific apps for their business type)
[3] Government Schemes (eligibility + application steps + helpline)
[4] Local SEO Tips (specific to their city/locality)
[5] Customer Engagement Ideas (WhatsApp, festivals, loyalty)
[6] Next Steps (top 3 immediate actions)

Keep it practical and specific. Mention exact app names, portal URLs, and helpline numbers from the documents.

Response:"""
    return prompt


# ── Main Query Function ───────────────────────────────────────────────────────

def answer(
    user_query : str,
    top_k      : int = DEFAULT_TOP_K,
    language   : str = "en",
    status_cb  = None,
) -> dict:
    """
    Full RAG pipeline:
      1. Embed query with granite-embedding-278m-multilingual
      2. Retrieve top-k docs from ChromaDB
      3. Build augmented prompt
      4. Generate answer with granite-4-h-small
    Returns full result dict for API response.
    """
    if not is_index_ready():
        raise RuntimeError("Vector index is empty. Call build_index() first.")

    if status_cb:
        status_cb("[STEP 1] Embedding query with granite-embedding-278m-multilingual...")

    retrieved = retrieve(user_query, top_k=top_k)

    if status_cb:
        status_cb(f"[STEP 2] Retrieved {len(retrieved)} documents.")
        for r in retrieved:
            status_cb(f"   -> [{r['category']}] {r['title']} (score: {r['score']})")
        status_cb("[STEP 3] Generating response with granite-4-h-small...")

    prompt      = _build_prompt(user_query, retrieved, language)
    answer_text = generate(prompt, max_tokens=600)

    return {
        "answer"         : answer_text,
        "retrieved_docs" : retrieved,
        "query"          : user_query,
        "language"       : language,
        "gen_model"      : "ibm/granite-4-h-small",
        "embed_model"    : "ibm/granite-embedding-278m-multilingual",
        "top_k"          : top_k,
    }
