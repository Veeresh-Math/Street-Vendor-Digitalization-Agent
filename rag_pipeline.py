"""
RAG Pipeline for Street Vendor Digitalization Agent
Steps:
  1. Build vector index from knowledge base using granite-embedding-278m-multilingual
  2. Embed user query
  3. Cosine similarity search → retrieve top-k relevant documents
  4. Build augmented prompt with retrieved context
  5. Generate final answer using granite-4-h-small
"""

import numpy as np
from ibm_client import get_embedding, generate_text
from knowledge_base import get_all_text_chunks

# ── Vector Index (built at startup) ──────────────────────────────────────────
_index: list[dict] = []   # [{text, embedding, doc}, ...]
_index_built = False


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    a_arr = np.array(a, dtype=np.float32)
    b_arr = np.array(b, dtype=np.float32)
    norm_a = np.linalg.norm(a_arr)
    norm_b = np.linalg.norm(b_arr)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a_arr, b_arr) / (norm_a * norm_b))


def build_index(status_callback=None) -> None:
    """
    Embed all knowledge base documents and store vectors.
    Call once at app startup. Uses granite-embedding-278m-multilingual.
    """
    global _index, _index_built
    _index = []
    chunks = get_all_text_chunks()
    total  = len(chunks)

    for i, (text, doc) in enumerate(chunks):
        if status_callback:
            status_callback(f"Embedding document {i+1}/{total}: {doc['title'][:50]}...")
        embedding = get_embedding(text)
        _index.append({
            "text":      text,
            "embedding": embedding,
            "doc":       doc,
        })

    _index_built = True
    if status_callback:
        status_callback(f"✅ Vector index built — {total} documents embedded.")


def retrieve(query: str, top_k: int = 3) -> list[dict]:
    """
    Embed the query and return top-k most relevant documents.
    Returns list of dicts with doc metadata and similarity score.
    """
    global _index
    if not _index:
        raise RuntimeError("Vector index not built. Call build_index() first.")

    query_vec = get_embedding(query)
    scored = []
    for item in _index:
        sim = _cosine_similarity(query_vec, item["embedding"])
        scored.append({"sim": sim, "doc": item["doc"], "text": item["text"]})

    scored.sort(key=lambda x: x["sim"], reverse=True)
    return scored[:top_k]


def build_rag_prompt(user_query: str, retrieved_docs: list[dict]) -> str:
    """
    Build the final prompt for granite-4-h-small by injecting retrieved context.
    """
    context_parts = []
    for i, result in enumerate(retrieved_docs, 1):
        doc = result["doc"]
        context_parts.append(
            f"[Document {i}] Category: {doc['category']}\n"
            f"Title: {doc['title']}\n"
            f"Content: {doc['content']}\n"
        )
    context_str = "\n".join(context_parts)

    prompt = f"""You are the Street Vendor Digitalization Agent, an AI assistant powered by IBM watsonx.ai (Edunet Internship Project). 
You help Indian street vendors and hawkers go digital by providing practical, actionable guidance.

Use ONLY the information from the documents below to answer the vendor's query. 
Be specific, friendly, and provide step-by-step guidance. Respond in English (or the same language as the query).

--- RETRIEVED DOCUMENTS ---
{context_str}
--- END OF DOCUMENTS ---

Vendor Query: "{user_query}"

Provide a structured, helpful response with:
✅ Relevant government schemes with application steps and links
✅ Digital payment/UPI setup steps (specific apps and instructions)  
✅ Online listing platforms relevant to their business
✅ Local SEO and visibility tips for their location
✅ Customer engagement and promotional ideas

Response:"""
    return prompt


def answer_query(user_query: str, top_k: int = 3, status_callback=None) -> dict:
    """
    Full RAG pipeline:
      1. Retrieve top-k relevant docs using granite-embedding-278m-multilingual
      2. Build augmented prompt
      3. Generate answer using granite-4-h-small
    
    Returns dict with answer, retrieved_docs, and metadata.
    """
    if status_callback:
        status_callback("🔍 Embedding your query with granite-embedding-278m-multilingual...")

    # Step 1: Retrieve relevant documents
    retrieved = retrieve(user_query, top_k=top_k)

    if status_callback:
        status_callback(f"📄 Retrieved {len(retrieved)} relevant documents from knowledge base...")
        for r in retrieved:
            status_callback(f"   → [{r['doc']['category']}] {r['doc']['title']} (score: {r['sim']:.3f})")

    # Step 2: Build prompt with context
    prompt = build_rag_prompt(user_query, retrieved)

    if status_callback:
        status_callback("🤖 Generating answer with granite-4-h-small...")

    # Step 3: Generate answer
    answer = generate_text(prompt, max_tokens=500)

    return {
        "answer":         answer,
        "retrieved_docs": retrieved,
        "query":          user_query,
        "model_gen":      "ibm/granite-4-h-small",
        "model_embed":    "ibm/granite-embedding-278m-multilingual",
    }


def is_index_ready() -> bool:
    return _index_built and len(_index) > 0
