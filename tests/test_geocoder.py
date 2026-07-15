"""
Tests for the geocoder module.
"""

import pytest
from backend.geocoder import geocode


@pytest.mark.asyncio
async def test_geocode_returns_dict():
    """Test geocode returns a dictionary."""
    result = await geocode("Pune, India")
    assert isinstance(result, dict)
    assert "query" in result
    assert "found" in result


@pytest.mark.asyncio
async def test_geocode_india_query():
    """Test geocoding an Indian location."""
    result = await geocode("Mumbai, India")
    assert result["query"] == "Mumbai, India"
    if result["found"]:
        assert result["lat"] is not None
        assert result["lon"] is not None
        assert isinstance(result["lat"], float)
        assert isinstance(result["lon"], float)


@pytest.mark.asyncio
async def test_geocode_empty_result():
    """Test geocode with unresolvable query."""
    result = await geocode("xyznonexistent12345")
    assert result["found"] is False
    assert result["lat"] is None
    assert result["lon"] is None
