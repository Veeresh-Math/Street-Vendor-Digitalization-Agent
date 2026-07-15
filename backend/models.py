"""
Pydantic models — request / response schemas for FastAPI endpoints
"""

import re
import html

from pydantic import BaseModel, Field, field_validator
from typing import Optional


def _validate_upi(v: str | None) -> str | None:
    if v is None or v.strip() == '':
        return None
    v = v.strip()
    if not re.match(r'^[\w.\-]+@[\w]+$', v):
        raise ValueError(f'Invalid UPI ID format: {v}. Expected format: name@bank')
    return v


def _sanitize_input(v: str) -> str:
    """Strip and escape HTML entities to prevent XSS."""
    v = v.strip()
    v = html.escape(v)
    return v


# ── /api/query ────────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    query    : str            = Field(...,  json_schema_extra={"example": "I sell fruit in Pune's Camp area"})
    language : Optional[str]  = Field("en", json_schema_extra={"example": "en"})   # en/hi/mr/ta/te/kn/gu/bn
    top_k    : Optional[int]  = Field(2,    ge=1, le=5)

    @field_validator('query', mode='before')
    @classmethod
    def sanitize_query(cls, v):
        return _sanitize_input(v) if isinstance(v, str) else v


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
    vendor_name    : str           = Field(...,  json_schema_extra={"example": "Ramesh Fruits"})
    business_type  : str           = Field(...,  json_schema_extra={"example": "Fruit & Vegetable Vendor"})
    location       : str           = Field(...,  json_schema_extra={"example": "Camp, Pune"})
    upi_id         : Optional[str] = Field(None, json_schema_extra={"example": "rameshfruits@upi"})
    language       : Optional[str] = Field("en")
    top_k          : Optional[int] = Field(2, ge=1, le=5)

    @field_validator('upi_id', mode='before')
    @classmethod
    def validate_upi(cls, v):
        return _validate_upi(v)

    @field_validator('vendor_name', 'business_type', 'location', mode='before')
    @classmethod
    def sanitize_fields(cls, v):
        return _sanitize_input(v) if isinstance(v, str) else v


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
    upi_id      : str            = Field(...,  json_schema_extra={"example": "rameshfruits@upi"})
    vendor_name : str            = Field(...,  json_schema_extra={"example": "Ramesh Fruits"})
    location    : Optional[str]  = Field(None, json_schema_extra={"example": "Camp, Pune"})

    @field_validator('upi_id', mode='before')
    @classmethod
    def validate_upi(cls, v):
        return _validate_upi(v)


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
    name          : str           = Field(..., json_schema_extra={"example": "Ramesh Fruits"})
    business_type : str           = Field(..., json_schema_extra={"example": "Fruit & Vegetable Vendor"})
    location      : str           = Field(..., json_schema_extra={"example": "Camp, Pune"})
    city          : Optional[str] = Field(None, json_schema_extra={"example": "Pune"})
    lat           : Optional[float] = Field(None)
    lon           : Optional[float] = Field(None)
    upi_id        : Optional[str] = Field(None)

    @field_validator('name', 'business_type', 'location', 'city', mode='before')
    @classmethod
    def sanitize_fields(cls, v):
        return _sanitize_input(v) if isinstance(v, str) else v


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
