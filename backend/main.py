"""
FastAPI main — Street Vendor Digitalization Agent
Serves all API endpoints AND the frontend static files.

Run:
    uvicorn backend.main:app --reload --port 8000

Routes:
    GET  /               → frontend/index.html  (landing page)
    GET  /agent          → frontend/agent.html  (live AI chat tool)
    POST /api/query      → RAG query → answer + retrieved docs
    POST /api/generate-kit → full digital kit for a vendor
    POST /api/qr         → generate QR + business card PNG
    GET  /api/geocode    → OpenStreetMap Nominatim lookup
    POST /api/build-index→ (re)build ChromaDB vector index
    GET  /api/health     → IBM connection + index status
"""

import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

# Force UTF-8 output on Windows to avoid emoji encoding errors
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from backend.models import (
    QueryRequest, QueryResponse, RetrievedDoc,
    KitRequest, KitResponse,
    QRRequest, QRResponse,
    GeocodeResponse, HealthResponse,
)
from backend.rag_pipeline import build_index, answer, is_index_ready, index_doc_count
from backend.qr_generator import generate_qr, generate_business_card
from backend.geocoder import geocode
from backend.ibm_client import health_check

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
STATIC_DIR   = os.path.join(BASE_DIR, "static")
os.makedirs(os.path.join(STATIC_DIR, "generated"), exist_ok=True)

# ── Startup: auto-build index if empty ────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    if not is_index_ready():
        print("[STARTUP] Building ChromaDB vector index on startup...")
        try:
            count = build_index()
            print(f"[STARTUP] Index ready -- {count} documents embedded.")
        except Exception as e:
            print(f"[STARTUP] Index build failed: {e}. Run POST /api/build-index to retry.")
    else:
        print(f"[STARTUP] ChromaDB index already ready ({index_doc_count()} docs).")
    yield


app = FastAPI(
    title       = "Street Vendor Digitalization Agent",
    description = "AICTE-IBM SkillsBuild Internship 2026 — Problem Statement No. 29",
    version     = "1.0.0",
    lifespan    = lifespan,
)

# ── Static files ──────────────────────────────────────────────────────────────
app.mount("/static",   StaticFiles(directory=STATIC_DIR),   name="static")
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Frontend page routes ───────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def landing():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/agent", include_in_schema=False)
async def agent():
    return FileResponse(os.path.join(FRONTEND_DIR, "agent.html"))


# ── API: Health ────────────────────────────────────────────────────────────────
@app.get("/api/health", response_model=HealthResponse, tags=["System"])
async def health():
    ibm  = health_check()
    return HealthResponse(
        status      = "ok",
        ibm_status  = ibm["status"],
        index_ready = is_index_ready(),
        doc_count   = index_doc_count(),
        gen_model   = "ibm/granite-4-h-small",
        embed_model = "ibm/granite-embedding-278m-multilingual",
        chroma_path = os.path.join(BASE_DIR, "vector_store"),
    )


# ── API: Build Index ───────────────────────────────────────────────────────────
@app.post("/api/build-index", tags=["System"])
async def api_build_index(background_tasks: BackgroundTasks, force: bool = False):
    """Trigger (re)build of the ChromaDB vector index in the background."""
    log = []
    background_tasks.add_task(build_index, force_rebuild=force, status_cb=log.append)
    return {"message": "Index build started in background.", "force_rebuild": force}


# ── API: Query (core RAG) ──────────────────────────────────────────────────────
@app.post("/api/query", response_model=QueryResponse, tags=["Agent"])
async def api_query(req: QueryRequest):
    """
    RAG query: embed → retrieve from ChromaDB → generate with granite-4-h-small.
    """
    if not is_index_ready():
        raise HTTPException(
            status_code=503,
            detail="Vector index not ready. Call POST /api/build-index first.",
        )
    try:
        result = answer(req.query, top_k=req.top_k, language=req.language)
        docs   = [
            RetrievedDoc(
                id=d["id"], title=d["title"],
                category=d["category"], score=d["score"],
            )
            for d in result["retrieved_docs"]
        ]
        return QueryResponse(
            answer         = result["answer"],
            retrieved_docs = docs,
            query          = result["query"],
            language       = result["language"],
            gen_model      = result["gen_model"],
            embed_model    = result["embed_model"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── API: Generate Kit ──────────────────────────────────────────────────────────
@app.post("/api/generate-kit", response_model=KitResponse, tags=["Agent"])
async def api_generate_kit(req: KitRequest):
    """
    Full digital kit: profile + UPI guide + schemes + SEO tips + QR business card.
    """
    if not is_index_ready():
        raise HTTPException(status_code=503, detail="Vector index not ready.")

    # Build a rich query from the structured vendor info
    enriched_query = (
        f"I am {req.vendor_name}, a {req.business_type} located at {req.location}. "
        f"My UPI ID is {req.upi_id or 'not set yet'}. "
        f"How do I go digital? What schemes am I eligible for? "
        f"Which platforms should I list on? What are my local SEO tips?"
    )

    try:
        result = answer(enriched_query, top_k=req.top_k, language=req.language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Generate business card if UPI ID provided
    qr_url = None
    if req.upi_id:
        try:
            qr_url = generate_business_card(
                vendor_name   = req.vendor_name,
                business_type = req.business_type,
                location      = req.location,
                upi_id        = req.upi_id,
            )
        except Exception:
            qr_url = None   # non-fatal

    docs = [
        RetrievedDoc(
            id=d["id"], title=d["title"],
            category=d["category"], score=d["score"],
        )
        for d in result["retrieved_docs"]
    ]

    return KitResponse(
        vendor_name    = req.vendor_name,
        business_type  = req.business_type,
        location       = req.location,
        upi_id         = req.upi_id,
        answer         = result["answer"],
        qr_url         = qr_url,
        retrieved_docs = docs,
        gen_model      = "ibm/granite-4-h-small",
        embed_model    = "ibm/granite-embedding-278m-multilingual",
    )


# ── API: QR Code ───────────────────────────────────────────────────────────────
@app.post("/api/qr", response_model=QRResponse, tags=["Tools"])
async def api_qr(req: QRRequest):
    """Generate a styled UPI QR code PNG and return its URL."""
    try:
        url = generate_qr(req.upi_id, req.vendor_name)
        return QRResponse(qr_url=url, upi_id=req.upi_id, vendor_name=req.vendor_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── API: Geocode ───────────────────────────────────────────────────────────────
@app.get("/api/geocode", response_model=GeocodeResponse, tags=["Tools"])
async def api_geocode(q: str):
    """Geocode a location string using OpenStreetMap Nominatim (free, no key)."""
    result = geocode(q)
    return GeocodeResponse(**{k: v for k, v in result.items() if k != "error"})
