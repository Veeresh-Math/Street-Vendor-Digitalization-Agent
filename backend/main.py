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
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

# Force UTF-8 output on Windows to avoid emoji encoding errors
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Load .env from backend/ directory
_backend_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_backend_dir, ".env"))

from backend.models import (
    QueryRequest, QueryResponse, RetrievedDoc,
    KitRequest, KitResponse,
    QRRequest, QRResponse,
    GeocodeResponse, HealthResponse,
    VendorRegisterRequest, VendorResponse,
    AnalyticsResponse, ForecastResponse,
    SchemeCheckRequest, SchemeCheckResponse,
)
from backend.rag_pipeline import build_index, answer, is_index_ready, index_doc_count
from backend.qr_generator import generate_qr, generate_business_card
from backend.geocoder import geocode
from backend.ibm_client import health_check, get_token_usage
from backend.vendor_store import register_vendor, get_all_vendors, get_vendor_stats
from backend.forecast import get_forecast
from backend.scheme_checker import check_eligibility
from backend.knowledge_base import get_all_documents
from backend.monitoring import request_logger

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
STATIC_DIR   = os.path.join(BASE_DIR, "static")
os.makedirs(os.path.join(STATIC_DIR, "generated"), exist_ok=True)

# ── Startup: auto-build index if empty ────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Check if DEMO_MODE is enabled — skip all IBM API calls
    demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    if demo_mode:
        print("[STARTUP] DEMO_MODE enabled — skipping index build and IBM pre-warm (0 tokens).")
    else:
        if not is_index_ready():
            print("[STARTUP] Building ChromaDB vector index on startup...")
            try:
                count = build_index()
                print(f"[STARTUP] Index ready -- {count} documents embedded.")
            except Exception as e:
                print(f"[STARTUP] Index build failed: {e}. Run POST /api/build-index to retry.")
        else:
            print(f"[STARTUP] ChromaDB index already ready ({index_doc_count()} docs).")
        # Pre-warm IBM connection so first user request is fast
        try:
            from backend.ibm_client import _get_gen_model, _get_embed_model
            _get_gen_model()
            _get_embed_model()
            print("[STARTUP] IBM models pre-warmed.")
        except Exception as e:
            print(f"[STARTUP] IBM pre-warm skipped: {e}")
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

# Compatibility: the frontend currently references assets from root
# (e.g. /js/kit.js, /service-worker.js, /manifest.json).
# Map these root paths to their corresponding files inside /frontend.
app.mount("/css",  StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")),  name="css")
app.mount("/js",   StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")),   name="js")

# Root-level web app assets referenced by the frontend (service worker + PWA manifest)
@app.get("/service-worker.js", include_in_schema=False)
async def service_worker_js():
    return FileResponse(os.path.join(FRONTEND_DIR, "service-worker.js"), media_type="application/javascript")

@app.get("/manifest.json", include_in_schema=False)
async def manifest_json():
    return FileResponse(os.path.join(FRONTEND_DIR, "manifest.json"), media_type="application/manifest+json")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Security Headers Middleware ────────────────────────────────────────────────
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


# ── Rate Limiting Middleware ───────────────────────────────────────────────────
import time as _time
from collections import defaultdict

_rate_limit_store: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 30  # per window per IP

@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    now = _time.time()
    
    # Clean old entries
    _rate_limit_store[client_ip] = [
        t for t in _rate_limit_store[client_ip] if now - t < RATE_LIMIT_WINDOW
    ]
    
    if len(_rate_limit_store[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=429,
            detail="Too many requests. Please try again later."
        )
    
    _rate_limit_store[client_ip].append(now)
    response = await call_next(request)
    return response


# ── Request Logging Middleware ─────────────────────────────────────────────────
@app.middleware("http")
async def log_requests(request, call_next):
    import time as _time
    start = _time.time()
    response = await call_next(request)
    latency_ms = (_time.time() - start) * 1000
    request_logger.log_request(
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        latency_ms=latency_ms,
    )
    return response

# ── Frontend page routes ───────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def landing():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# Some frontend/service-worker paths may request these explicitly.
@app.get("/index.html", include_in_schema=False)
async def index_html():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/agent", include_in_schema=False)
async def agent():
    return FileResponse(os.path.join(FRONTEND_DIR, "agent.html"), media_type="text/html")

@app.get("/agent.html", include_in_schema=False)
async def agent_html():
    return FileResponse(os.path.join(FRONTEND_DIR, "agent.html"), media_type="text/html")


@app.get("/dashboard", include_in_schema=False)
async def dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "dashboard.html"), media_type="text/html")

@app.get("/dashboard.html", include_in_schema=False)
async def dashboard_html():
    return FileResponse(os.path.join(FRONTEND_DIR, "dashboard.html"), media_type="text/html")



# ── API: Health ────────────────────────────────────────────────────────────────
@app.get("/api/health", response_model=HealthResponse, tags=["System"])
async def health():
    demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    # In demo mode, skip IBM connection entirely
    if demo_mode:
        ibm_status = "demo-mode"
    else:
        ibm = health_check()
        ibm_status = ibm["status"]
    # In demo mode, report index as ready (we don't need it)
    index_ready = True if demo_mode else is_index_ready()
    return HealthResponse(
        status      = "ok",
        ibm_status  = ibm_status,
        index_ready = index_ready,
        doc_count   = len(get_all_documents()) if demo_mode else index_doc_count(),
        gen_model   = "demo-cached" if demo_mode else "meta-llama/llama-3-3-70b-instruct",
        embed_model = "none" if demo_mode else "intfloat/multilingual-e5-large",
        chroma_path = os.path.join(BASE_DIR, "vector_store"),
    )


# ── API: Ping (keep-alive, no IBM call, instant response) ─────────────────────
@app.get("/api/ping", tags=["System"])
async def ping():
    return {"status": "ok"}


# ── API: Monitoring Stats ────────────────────────────────────────────────────
@app.get("/api/monitoring/stats", tags=["System"])
async def monitoring_stats():
    """Return request logging statistics (additive, no response changes)."""
    return request_logger.get_stats()


@app.get("/api/monitoring/recent", tags=["System"])
async def monitoring_recent(n: int = 20):
    """Return the last N request log entries."""
    return request_logger.get_recent(n=n)


@app.get("/api/monitoring/tokens", tags=["System"])
async def monitoring_tokens():
    """Return IBM token usage statistics."""
    return get_token_usage()


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
    RAG query: embed → retrieve from ChromaDB → generate with llama-3-3-70b-instruct.
    In DEMO_MODE, uses pre-cached responses (0 tokens).
    """
    # In demo mode, skip index check — demo responses don't need the index
    demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    if not demo_mode and not is_index_ready():
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
    In DEMO_MODE, uses pre-cached responses (0 tokens).
    """
    # In demo mode, skip index check
    demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    if not demo_mode and not is_index_ready():
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

    qr_url = None
    if req.upi_id:
        try:
            qr_url = generate_business_card(
                vendor_name   = req.vendor_name,
                business_type = req.business_type,
                location      = req.location,
                upi_id        = req.upi_id,
            )
        except Exception as e:
            print(f"[QR] Business card generation failed: {e}")
            import traceback; traceback.print_exc()
            qr_url = None

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
        gen_model      = "demo-cached" if demo_mode else "meta-llama/llama-3-3-70b-instruct",
        embed_model    = "none" if demo_mode else "intfloat/multilingual-e5-large",
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
    result = await geocode(q)
    return GeocodeResponse(**{k: v for k, v in result.items() if k != "error"})


# ── API: Vendor Registration ──────────────────────────────────────────────────
@app.post("/api/vendors", response_model=VendorResponse, tags=["Vendors"])
async def api_register_vendor(req: VendorRegisterRequest):
    """Register a new vendor in the local store."""
    vendor = register_vendor(
        name=req.name,
        business_type=req.business_type,
        location=req.location,
        city=req.city,
        lat=req.lat,
        lon=req.lon,
        upi_id=req.upi_id,
    )
    return VendorResponse(**vendor)


@app.get("/api/vendors", tags=["Vendors"])
async def api_list_vendors(city: str = None, business_type: str = None):
    """List all registered vendors, with optional city/type filtering."""
    vendors = get_all_vendors()
    if city:
        vendors = [v for v in vendors if (v.get("city") or "").lower() == city.lower()]
    if business_type:
        vendors = [v for v in vendors if (v.get("business_type") or "").lower() == business_type.lower()]
    return vendors


# ── API: Dashboard Analytics ──────────────────────────────────────────────────
@app.get("/api/analytics", response_model=AnalyticsResponse, tags=["Analytics"])
async def api_analytics():
    """Get dashboard analytics data."""
    stats = get_vendor_stats()
    return AnalyticsResponse(**stats)


# ── API: Demand Forecast ─────────────────────────────────────────────────────
@app.get("/api/forecast", response_model=ForecastResponse, tags=["Analytics"])
async def api_forecast(category: str = "all", days: int = 7):
    """Get demand forecast for a product category."""
    days = max(1, min(days, 30))
    result = get_forecast(category=category, days=days)
    return ForecastResponse(**result)


# ── API: Scheme Eligibility Check ────────────────────────────────────────────
@app.post("/api/scheme-check", response_model=SchemeCheckResponse, tags=["Schemes"])
async def api_scheme_check(req: SchemeCheckRequest):
    """Check PM SVANidhi eligibility based on vendor profile."""
    result = check_eligibility(
        has_cov=req.has_cov,
        has_lor=req.has_lor,
        is_food_vendor=req.is_food_vendor,
        city=req.city,
    )
    return SchemeCheckResponse(**result)


# ── API: List Government Schemes ─────────────────────────────────────────────
@app.get("/api/schemes", response_model=list[dict], tags=["Schemes"])
async def api_list_schemes():
    """Return all available government schemes."""
    return [
        {"name": "PM SVANidhi", "description": "Working capital loan for street vendors", "amount": "Up to Rs.50,000", "portal": "pmsvanidhi.mohua.gov.in", "helpline": "1800-11-1979"},
        {"name": "MSME Udyam Registration", "description": "Free MSME registration for priority sector benefits", "amount": "Free forever", "portal": "udyamregistration.gov.in", "helpline": "1800-111-956"},
        {"name": "Mudra Yojana (Shishu/Kishore)", "description": "Collateral-free business loans", "amount": "Up to Rs.5 lakh", "portal": "mudra.org.in", "helpline": "1800-180-1111"},
        {"name": "e-Shram Card", "description": "Universal social security for unorganised workers", "amount": "Free + Rs.2 lakh insurance", "portal": "eshram.gov.in", "helpline": "14434"},
        {"name": "FSSAI License", "description": "Food safety registration for food vendors", "amount": "Rs.100-2000/year", "portal": "foscos.fssai.gov.in", "helpline": "1800-112-100"},
        {"name": "Digital India", "description": "Government digital literacy and services", "amount": "Various benefits", "portal": "digitalindia.gov.in", "helpline": "1800-111-800"},
    ]


# ── API: List Supported Cities ───────────────────────────────────────────────
@app.get("/api/cities", response_model=list[dict], tags=["Cities"])
async def api_list_cities():
    """Return supported cities with vendor counts."""
    vendors = get_all_vendors()
    city_counts = {}
    for v in vendors:
        c = v.get("city", "Unknown")
        city_counts[c] = city_counts.get(c, 0) + 1
    cities_data = [
        {"name": "Pune", "state": "Maharashtra", "vendors": city_counts.get("Pune", 0)},
        {"name": "Mumbai", "state": "Maharashtra", "vendors": city_counts.get("Mumbai", 0)},
        {"name": "Chennai", "state": "Tamil Nadu", "vendors": city_counts.get("Chennai", 0)},
        {"name": "Bangalore", "state": "Karnataka", "vendors": city_counts.get("Bangalore", 0)},
        {"name": "Surat", "state": "Gujarat", "vendors": city_counts.get("Surat", 0)},
        {"name": "Delhi", "state": "Delhi", "vendors": city_counts.get("Delhi", 0)},
    ]
    return cities_data


# ── API: Personalized Recommendations ────────────────────────────────────────
@app.get("/api/recommendations", response_model=list[dict], tags=["Agent"])
async def api_recommendations():
    """Return personalized recommendations for vendors."""
    vendors = get_all_vendors()
    stats = get_vendor_stats()
    recs = []
    if stats.get("total", 0) == 0:
        recs.append({"title": "Register as a Vendor", "description": "Register on our platform to get started with digital tools.", "priority": "high", "icon": "user-plus"})
    if stats.get("vendors_with_upi", 0) < stats.get("total", 1):
        recs.append({"title": "Set Up UPI Payments", "description": "Accept digital payments to grow your business by 30%.", "priority": "high", "icon": "credit-card"})
    if stats.get("total_cities", 0) < 3:
        recs.append({"title": "Expand to New Cities", "description": "List your business on Google Maps for wider reach.", "priority": "medium", "icon": "map-pin"})
    recs.extend([
        {"title": "Apply for PM SVANidhi", "description": "Get a collateral-free loan of up to Rs.50,000.", "priority": "medium", "icon": "landmark"},
        {"title": "Create a Google Business Profile", "description": "Show up in local search results and get more customers.", "priority": "medium", "icon": "search"},
        {"title": "Join WhatsApp Business", "description": "Connect with customers directly through WhatsApp.", "priority": "low", "icon": "message-circle"},
    ])
    return recs[:6]
