"""
Geocoder — OpenStreetMap Nominatim (free, no API key needed)
Resolves vendor location strings to lat/lng + locality details.
"""

import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS       = {"User-Agent": "StreetVendorDigitalizationAgent/1.0"}


def geocode(query: str) -> dict:
    """
    Geocode a free-text location query using Nominatim.
    Returns dict with lat, lon, display_name, city, locality, state, found.
    """
    try:
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

        # Extract meaningful locality name
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
