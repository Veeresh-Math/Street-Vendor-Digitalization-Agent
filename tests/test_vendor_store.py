"""
Tests for the vendor store module.
"""

import pytest
import os
import json
from backend.vendor_store import register_vendor, get_all_vendors, get_vendor_stats


@pytest.fixture(autouse=True)
def clean_vendors():
    """Clean vendor data before each test."""
    from backend import vendor_store
    vendor_store._vendors = []
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    vendors_file = os.path.join(data_dir, "vendors.json")
    if os.path.exists(vendors_file):
        os.remove(vendors_file)
    yield
    if os.path.exists(vendors_file):
        os.remove(vendors_file)


def test_register_vendor():
    """Test vendor registration."""
    vendor = register_vendor(
        name="Test Vendor",
        business_type="Test Business",
        location="Test City",
        city="Test City",
        lat=20.0,
        lon=78.0,
        upi_id="test@upi",
    )
    assert vendor["name"] == "Test Vendor"
    assert vendor["business_type"] == "Test Business"
    assert vendor["city"] == "Test City"
    assert vendor["lat"] == 20.0
    assert vendor["lon"] == 78.0
    assert vendor["upi_id"] == "test@upi"
    assert "id" in vendor
    assert "registered_at" in vendor


def test_get_all_vendors():
    """Test listing all vendors."""
    register_vendor("V1", "B1", "L1")
    register_vendor("V2", "B2", "L2")
    vendors = get_all_vendors()
    assert len(vendors) == 2
    assert vendors[0]["name"] == "V1"
    assert vendors[1]["name"] == "V2"


def test_get_vendor_stats():
    """Test vendor analytics stats."""
    register_vendor("V1", "Food", "Pune", "Pune", upi_id="v1@upi")
    register_vendor("V2", "Textile", "Mumbai", "Mumbai")
    register_vendor("V3", "Food", "Pune", "Pune", upi_id="v3@upi")

    stats = get_vendor_stats()
    assert stats["total_vendors"] == 3
    assert stats["vendors_with_upi"] == 2
    assert stats["city_counts"]["Pune"] == 2
    assert stats["city_counts"]["Mumbai"] == 1
    assert stats["business_counts"]["Food"] == 2
    assert stats["business_counts"]["Textile"] == 1


def test_register_vendor_minimal():
    """Test vendor registration with minimal fields."""
    vendor = register_vendor("Minimal", "Type", "Location")
    assert vendor["name"] == "Minimal"
    assert vendor["city"] is None
    assert vendor["lat"] is None
    assert vendor["upi_id"] is None
