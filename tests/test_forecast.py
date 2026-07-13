"""
Tests for the demand forecast module.
"""

import pytest
from backend.forecast import get_forecast, CATEGORIES


def test_forecast_default():
    """Test default forecast returns 7 days."""
    result = get_forecast()
    assert result["category"] == "all"
    assert result["days"] == 7
    assert len(result["forecast"]) == 7
    assert result["trend"] in ["Increasing", "Decreasing", "Stable"]
    assert isinstance(result["summary"], str)


def test_forecast_specific_category():
    """Test forecast for a specific category."""
    result = get_forecast(category="fruits", days=5)
    assert result["category"] == "fruits"
    assert result["days"] == 5
    assert len(result["forecast"]) == 5


def test_forecast_all_categories():
    """Test forecast works for all defined categories."""
    for cat in CATEGORIES:
        result = get_forecast(category=cat, days=3)
        assert result["category"] == cat
        assert len(result["forecast"]) == 3


def test_forecast_demand_range():
    """Test demand index is within valid range (10-100)."""
    result = get_forecast(days=14)
    for day in result["forecast"]:
        assert 10 <= day["demand_index"] <= 100
        assert day["demand_level"] in ["High", "Medium", "Low"]
        assert "date" in day
        assert "day" in day
        assert "factors" in day


def test_forecast_unknown_category():
    """Test forecast with unknown category uses defaults."""
    result = get_forecast(category="unknown_category")
    assert result["category"] == "unknown_category"
    assert len(result["forecast"]) == 7
