"""
Tests for the QR code and business card generator.
"""

import pytest
from backend.qr_generator import generate_qr, generate_business_card


def test_generate_qr():
    """Test QR code generation returns a valid data URI."""
    uri = generate_qr("test@upi", "Test Vendor")
    assert uri.startswith("data:image/png;base64,")
    assert len(uri) > 100


def test_generate_business_card():
    """Test business card generation returns a valid data URI."""
    uri = generate_business_card(
        vendor_name="Test Vendor",
        business_type="Food Stall",
        location="Test City",
        upi_id="test@upi",
    )
    assert uri.startswith("data:image/png;base64,")
    assert len(uri) > 1000


def test_generate_qr_unique():
    """Test each QR generation creates unique data URIs."""
    uri1 = generate_qr("test1@upi", "Vendor 1")
    uri2 = generate_qr("test2@upi", "Vendor 2")
    assert uri1 != uri2


def test_generate_qr_different_vendors():
    """Test same UPI different vendor names produce different URIs."""
    uri1 = generate_qr("same@upi", "Vendor A")
    uri2 = generate_qr("same@upi", "Vendor B")
    assert uri1 != uri2
