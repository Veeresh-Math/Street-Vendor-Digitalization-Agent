"""
Tests for the PM SVANidhi scheme eligibility checker.
"""

import pytest
from backend.scheme_checker import check_eligibility


def test_eligible_with_cov():
    """Test eligibility with Certificate of Vending."""
    result = check_eligibility(has_cov=True)
    assert result["eligible"] is True
    assert "Rs.10,000" in result["loan_amount"]
    assert len(result["schemes"]) >= 3
    assert len(result["next_steps"]) > 0
    assert len(result["documents_needed"]) > 0


def test_eligible_with_lor():
    """Test eligibility with Letter of Recommendation."""
    result = check_eligibility(has_lor=True)
    assert result["eligible"] is True
    assert "Rs.10,000" in result["loan_amount"]


def test_not_eligible():
    """Test when vendor has no CoV or LoR."""
    result = check_eligibility(has_cov=False, has_lor=False)
    assert result["eligible"] is False
    assert "need CoV/LoR" in result["loan_amount"]


def test_food_vendor_gets_fssai():
    """Test food vendors get FSSAI scheme."""
    result = check_eligibility(has_cov=True, is_food_vendor=True)
    scheme_names = [s["name"] for s in result["schemes"]]
    assert "FSSAI Basic Registration" in scheme_names
    assert "FSSAI Basic Registration (Rs.100/year)" in result["documents_needed"]


def test_non_food_vendor_no_fssai():
    """Test non-food vendors don't get FSSAI."""
    result = check_eligibility(has_cov=True, is_food_vendor=False)
    scheme_names = [s["name"] for s in result["schemes"]]
    assert "FSSAI Basic Registration" not in scheme_names


def test_always_has_udyam():
    """Test MSME Udyam is always available."""
    result = check_eligibility()
    scheme_names = [s["name"] for s in result["schemes"]]
    assert "MSME Udyam Registration" in scheme_names


def test_always_has_eshram():
    """Test e-Shram is always available."""
    result = check_eligibility()
    scheme_names = [s["name"] for s in result["schemes"]]
    assert "e-Shram Card" in scheme_names


def test_always_has_mudra():
    """Test Mudra Yojana is always available."""
    result = check_eligibility()
    scheme_names = [s["name"] for s in result["schemes"]]
    assert "Mudra Yojana (Shishu)" in scheme_names


def test_documents_for_food_vendor():
    """Test food vendors have FSSAI in documents."""
    result = check_eligibility(is_food_vendor=True)
    assert any("FSSAI" in d for d in result["documents_needed"])
