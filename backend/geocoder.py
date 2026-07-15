"""
Geocoder — OpenStreetMap Nominatim (free, no API key needed)
"""

import time
import asyncio
import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS       = {"User-Agent": "StreetVendorDigitalizationAgent/1.0"}
_last_request_time = 0


def _geocode_sync(query: str) -> dict:
    """Synchronous geocode using Nominatim (called in thread)."""
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < 1.0:
        time.sleep(1.0 - elapsed)

    try:
        _last_request_time = time.time()
        resp = requests.get(
            NOMINATIM_URL,
            params={
                "q"              : f"{query}, India",
                "format"         : "json",
                "addressdetails" : 1,
                "limit"          : 1,
                "countrycodes"   : "in",
            },
            headers = HEADERS,
            timeout = 8,
        )
        resp.raise_for_status()
        data = resp.json()

        if not data:
            return _empty(query)

        result  = data[0]
        address = result.get("address", {})

        locality = (
            address.get("suburb")
            or address.get("neighbourhood")
            or address.get("quarter")
            or address.get("town")
            or address.get("village")
            or ""
        )
        city = (
            address.get("city")
            or address.get("town")
            or address.get("municipality")
            or ""
        )
        state = address.get("state", "")

        return {
            "query"        : query,
            "display_name" : result.get("display_name", ""),
            "lat"          : float(result.get("lat", 0)),
            "lon"          : float(result.get("lon", 0)),
            "city"         : city,
            "locality"     : locality,
            "state"        : state,
            "found"        : True,
        }

    except Exception as e:
        return {**_empty(query), "error": str(e)}


def _empty(query: str) -> dict:
    return {
        "query"        : query,
        "display_name" : None,
        "lat"          : None,
        "lon"          : None,
        "city"         : None,
        "locality"     : None,
        "state"        : None,
        "found"        : False,
    }


_geocode_cache: dict = {}
_CACHE_MAX = 200


async def geocode(query: str) -> dict:
    """Async geocode — runs blocking I/O in thread, caches results."""
    q = query.strip().lower()
    if q in _geocode_cache:
        return _geocode_cache[q]
    result = await asyncio.to_thread(_geocode_sync, query)
    if len(_geocode_cache) < _CACHE_MAX:
        _geocode_cache[q] = result
    return result
