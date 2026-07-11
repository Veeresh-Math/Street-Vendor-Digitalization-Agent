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
