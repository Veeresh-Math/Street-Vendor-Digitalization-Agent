"""
Tests for the QR code and business card generator.
"""

import pytest
import os
from backend.qr_generator import generate_qr, generate_business_card, OUTPUT_DIR


def test_generate_qr():
    """Test QR code generation."""
    url = generate_qr("test@upi", "Test Vendor")
    assert url.startswith("/static/generated/")
    assert url.endswith(".png")
    # Check file exists
    filepath = os.path.join(os.path.dirname(__file__), "..", url.lstrip("/"))
    assert os.path.exists(filepath), f"QR file not found: {filepath}"


def test_generate_business_card():
    """Test business card generation."""
    url = generate_business_card(
        vendor_name="Test Vendor",
        business_type="Food Stall",
        location="Test City",
        upi_id="test@upi",
    )
    assert url.startswith("/static/generated/")
    assert url.endswith(".png")
    filepath = os.path.join(os.path.dirname(__file__), "..", url.lstrip("/"))
    assert os.path.exists(filepath), f"Card file not found: {filepath}"


def test_generate_qr_unique():
    """Test each QR generation creates unique files."""
    url1 = generate_qr("test1@upi", "Vendor 1")
    url2 = generate_qr("test2@upi", "Vendor 2")
    assert url1 != url2


def test_output_dir_exists():
    """Test output directory is created."""
    assert os.path.isdir(OUTPUT_DIR)
