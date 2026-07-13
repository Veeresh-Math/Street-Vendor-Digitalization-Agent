"""
Vendor Store — In-memory vendor registry with JSON persistence.
"""

import os
import json
import uuid
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
VENDORS_FILE = os.path.join(DATA_DIR, "vendors.json")

_vendors: list[dict] = []
_loaded = False


def _load():
    global _vendors, _loaded
    if _loaded:
        return
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(VENDORS_FILE):
        with open(VENDORS_FILE, "r", encoding="utf-8") as f:
            _vendors = json.load(f)
    else:
        _vendors = _seed_vendors()
        _save()
    _loaded = True


def _save():
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(VENDORS_FILE, "w", encoding="utf-8") as f:
        json.dump(_vendors, f, ensure_ascii=False, indent=2)


def _seed_vendors() -> list[dict]:
    """Pre-populate with sample vendors for demo purposes."""
    seeds = [
        {"name": "Ramesh Fruits", "business_type": "Fruit & Vegetable Vendor", "location": "Camp, Pune", "city": "Pune", "lat": 18.5074, "lon": 73.8893, "upi_id": "rameshfruits@upi"},
        {"name": "Lakshmi Idli House", "business_type": "South Indian Food Stall", "location": "T. Nagar, Chennai", "city": "Chennai", "lat": 13.0418, "lon": 80.2341, "upi_id": "lakshmiidli@paytm"},
        {"name": "Suresh Textiles", "business_type": "Saree & Clothing Vendor", "location": "Dharavi, Mumbai", "city": "Mumbai", "lat": 19.0438, "lon": 72.8534, "upi_id": "sureshtextiles@gpay"},
        {"name": "Anita Flower Stall", "business_type": "Flower Vendor", "location": "KR Market, Bangalore", "city": "Bangalore", "lat": 12.9592, "lon": 77.5747, "upi_id": "anitaflowers@bhim"},
        {"name": "Mahesh Chaat Corner", "business_type": "Street Food Stall", "location": "Chandni Chowk, Delhi", "city": "Delhi", "lat": 28.6507, "lon": 77.2334, "upi_id": "maheshchaat@phonepe"},
        {"name": "Priya Fashion Hub", "business_type": "Textile & Accessories", "location": "Ring Road, Surat", "city": "Surat", "lat": 21.1702, "lon": 72.8311, "upi_id": "priyafashion@upi"},
        {"name": "Ganesh Vegetables", "business_type": "Vegetable Vendor", "location": "FC Road, Pune", "city": "Pune", "lat": 18.5167, "lon": 73.8413, "upi_id": "ganeshveg@paytm"},
        {"name": "Fatima Biryani", "business_type": "Biryani & Rice Stall", "location": "Sowcarpet, Chennai", "city": "Chennai", "lat": 13.0604, "lon": 80.2760, "upi_id": "fatimabiryani@gpay"},
        {"name": "Krishna Electronics", "business_type": "Electronics Repair Shop", "location": "Lajpat Nagar, Delhi", "city": "Delhi", "lat": 28.5679, "lon": 77.2405, "upi_id": "krishnaelec@upi"},
        {"name": "Meena Chat Center", "business_type": "Chaat & Snacks", "location": "Deccan Gymkhana, Pune", "city": "Pune", "lat": 18.5134, "lon": 73.8393, "upi_id": "meenachaat@phonepe"},
    ]
    vendors = []
    for s in seeds:
        vendors.append({
            "id": str(uuid.uuid4())[:8],
            **s,
            "registered_at": datetime.now().isoformat(),
        })
    return vendors


def register_vendor(
    name: str,
    business_type: str,
    location: str,
    city: str = None,
    lat: float = None,
    lon: float = None,
    upi_id: str = None,
) -> dict:
    """Register a new vendor and return the vendor dict."""
    _load()
    vendor = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "business_type": business_type,
        "location": location,
        "city": city,
        "lat": lat,
        "lon": lon,
        "upi_id": upi_id,
        "registered_at": datetime.now().isoformat(),
    }
    _vendors.append(vendor)
    _save()
    return vendor


def get_all_vendors() -> list[dict]:
    """Return all registered vendors."""
    _load()
    return _vendors


def get_vendor_stats() -> dict:
    """Return analytics summary of all vendors."""
    _load()
    total = len(_vendors)
    with_upi = sum(1 for v in _vendors if v.get("upi_id"))
    city_counts = {}
    business_counts = {}
    for v in _vendors:
        city = v.get("city") or "Unknown"
        city_counts[city] = city_counts.get(city, 0) + 1
        bt = v.get("business_type") or "Other"
        business_counts[bt] = business_counts.get(bt, 0) + 1

    recent = sorted(_vendors, key=lambda x: x.get("registered_at", ""), reverse=True)[:5]
    return {
        "total_vendors": total,
        "vendors_with_upi": with_upi,
        "city_counts": city_counts,
        "business_counts": business_counts,
        "recent_vendors": recent,
    }
