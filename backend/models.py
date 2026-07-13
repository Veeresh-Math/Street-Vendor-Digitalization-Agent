"""
Pydantic models — request / response schemas for FastAPI endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional


# ── /api/query ────────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    query    : str            = Field(...,  example="I sell fruit in Pune's Camp area")
    language : Optional[str]  = Field("en", example="en")   # en/hi/mr/ta/te/kn/gu/bn
    top_k    : Optional[int]  = Field(3,    ge=1, le=5)


class RetrievedDoc(BaseModel):
    id       : str
    title    : str
    category : str
    score    : float


class QueryResponse(BaseModel):
    answer          : str
    retrieved_docs  : list[RetrievedDoc]
    query           : str
    language        : str
    gen_model       : str
    embed_model     : str


# ── /api/generate-kit ─────────────────────────────────────────────────────────

class KitRequest(BaseModel):
    vendor_name    : str           = Field(...,  example="Ramesh Fruits")
    business_type  : str           = Field(...,  example="Fruit & Vegetable Vendor")
    location       : str           = Field(...,  example="Camp, Pune")
    upi_id         : Optional[str] = Field(None, example="rameshfruits@upi")
    language       : Optional[str] = Field("en")
    top_k          : Optional[int] = Field(3, ge=1, le=5)


class KitResponse(BaseModel):
    vendor_name   : str
    business_type : str
    location      : str
    upi_id        : Optional[str]
    answer        : str
    qr_url        : Optional[str]   # /static/generated/<filename>.png
    retrieved_docs: list[RetrievedDoc]
    gen_model     : str
    embed_model   : str


# ── /api/qr ───────────────────────────────────────────────────────────────────

class QRRequest(BaseModel):
    upi_id      : str            = Field(...,  example="rameshfruits@upi")
    vendor_name : str            = Field(...,  example="Ramesh Fruits")
    location    : Optional[str]  = Field(None, example="Camp, Pune")


class QRResponse(BaseModel):
    qr_url      : str            # URL path to the generated PNG
    upi_id      : str
    vendor_name : str


# ── /api/geocode ──────────────────────────────────────────────────────────────

class GeocodeResponse(BaseModel):
    query        : str
    display_name : Optional[str]
    lat          : Optional[float]
    lon          : Optional[float]
    city         : Optional[str]
    locality     : Optional[str]
    state        : Optional[str]
    found        : bool


# ── /api/health ───────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status       : str
    ibm_status   : str
    index_ready  : bool
    doc_count    : int
    gen_model    : str
    embed_model  : str
    chroma_path  : str


# ── /api/vendors ──────────────────────────────────────────────────────────────

class VendorRegisterRequest(BaseModel):
    name          : str           = Field(..., example="Ramesh Fruits")
    business_type : str           = Field(..., example="Fruit & Vegetable Vendor")
    location      : str           = Field(..., example="Camp, Pune")
    city          : Optional[str] = Field(None, example="Pune")
    lat           : Optional[float] = Field(None)
    lon           : Optional[float] = Field(None)
    upi_id        : Optional[str] = Field(None)


class VendorResponse(BaseModel):
    id            : str
    name          : str
    business_type : str
    location      : str
    city          : Optional[str]
    lat           : Optional[float]
    lon           : Optional[float]
    upi_id        : Optional[str]
    registered_at : str


# ── /api/analytics ────────────────────────────────────────────────────────────

class AnalyticsResponse(BaseModel):
    total_vendors    : int
    vendors_with_upi : int
    city_counts      : dict
    business_counts  : dict
    recent_vendors   : list[dict]


# ── /api/forecast ─────────────────────────────────────────────────────────────

class ForecastResponse(BaseModel):
    category   : str
    days       : int
    forecast   : list[dict]
    trend      : str
    summary    : str


# ── /api/scheme-check ─────────────────────────────────────────────────────────

class SchemeCheckRequest(BaseModel):
    has_cov       : bool = Field(False, description="Has Certificate of Vending")
    has_lor       : bool = Field(False, description="Has Letter of Recommendation")
    is_food_vendor: bool = Field(False, description="Sells food items")
    city          : Optional[str] = Field(None)


class SchemeCheckResponse(BaseModel):
    eligible          : bool
    loan_amount       : str
    schemes           : list[dict]
    next_steps        : list[str]
    documents_needed  : list[str]
