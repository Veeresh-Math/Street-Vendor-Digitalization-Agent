"""
Demand Forecasting Module — Formula-based prediction with seasonal adjustments.
"""

import random
from datetime import date as _date, datetime, timedelta


# Simulated product categories and base demands
CATEGORIES = {
    "fruits": {"base": 85, "peak_hours": [7, 8, 17, 18], "weekend_boost": 1.3},
    "vegetables": {"base": 92, "peak_hours": [6, 7, 8, 17, 18, 19], "weekend_boost": 1.2},
    "street_food": {"base": 78, "peak_hours": [12, 13, 19, 20, 21], "weekend_boost": 1.5},
    "textiles": {"base": 45, "peak_hours": [11, 12, 16, 17], "weekend_boost": 1.8},
    "flowers": {"base": 70, "peak_hours": [6, 7, 8, 17, 18], "weekend_boost": 1.6},
    "electronics": {"base": 35, "peak_hours": [11, 12, 15, 16], "weekend_boost": 1.4},
}

# Seasonal multipliers (month -> multiplier)
SEASONAL = {
    1: 1.1,   # New Year / Makar Sankranti
    2: 0.95,  # Post-festival lull
    3: 1.0,
    4: 0.9,   # Summer slowdown
    5: 0.85,  # Peak summer
    6: 0.9,   # Monsoon start
    7: 1.0,   # Monsoon
    8: 1.05,  # Pre-festival
    9: 1.2,   # Ganesh Chaturthi / Navratri
    10: 1.4,  # Diwali peak
    11: 1.15, # Post-Diwali
    12: 1.1,  # Christmas / year-end
}

# Festival demand spikes
FESTIVALS = {
    (10, 15): ("Diwali", 1.8),
    (10, 20): ("Dhanteras", 1.6),
    (9, 25): ("Navratri", 1.5),
    (8, 25): ("Ganesh Chaturthi", 1.5),
    (3, 14): ("Holi", 1.4),
    (1, 14): ("Makar Sankranti", 1.3),
    (12, 25): ("Christmas", 1.3),
    (11, 1): ("Diwali Follow-up", 1.2),
}


def _get_category_params(category: str) -> dict:
    if category == "all" or category not in CATEGORIES:
        return {"base": 65, "peak_hours": [8, 12, 18], "weekend_boost": 1.3}
    return CATEGORIES[category]


def _day_of_week_factor(date: datetime) -> float:
    """Weekend boost."""
    if date.weekday() >= 5:  # Saturday=5, Sunday=6
        return _get_category_params("all").get("weekend_boost", 1.3)
    return 1.0


def _festival_factor(date: datetime) -> float:
    """Check if date falls near a festival."""
    d = date.date() if hasattr(date, 'date') else date
    for (month, day), (name, mult) in FESTIVALS.items():
        fest_date = _date(d.year, month, day)
        distance = abs((d - fest_date).days)
        if distance <= 3:
            return mult
    return 1.0


def get_forecast(category: str = "all", days: int = 7) -> dict:
    """
    Generate a demand forecast for the next N days.
    Returns list of daily predictions with demand index and factors.
    """
    params = _get_category_params(category)
    base = params["base"]
    weekend_boost = params.get("weekend_boost", 1.3)
    today = datetime.now()
    forecast_data = []

    for i in range(days):
        date = today + timedelta(days=i)
        day_factor = weekend_boost if date.weekday() >= 5 else 1.0
        seasonal = SEASONAL.get(date.month, 1.0)
        festival = _festival_factor(date)
        seed = int(date.strftime("%Y%m%d"))
        noise = random.Random(seed).uniform(0.92, 1.08)

        demand = int(base * day_factor * seasonal * festival * noise)
        demand = max(10, min(100, demand))

        factors = []
        if day_factor > 1.0:
            factors.append("Weekend boost")
        if seasonal > 1.1:
            factors.append("Festival season")
        if festival > 1.0:
            factors.append("Nearby festival")
        if date.weekday() < 5:
            factors.append("Weekday")

        forecast_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "day": date.strftime("%A"),
            "demand_index": demand,
            "demand_level": (
                "High" if demand >= 80 else
                "Medium" if demand >= 50 else
                "Low"
            ),
            "factors": factors if factors else ["Normal"],
        })

    # Trend calculation
    demands = [d["demand_index"] for d in forecast_data]
    avg_first = sum(demands[:3]) / 3 if len(demands) >= 3 else demands[0]
    avg_last = sum(demands[-3:]) / 3 if len(demands) >= 3 else demands[-1]
    if avg_last > avg_first * 1.1:
        trend = "Increasing"
    elif avg_last < avg_first * 0.9:
        trend = "Decreasing"
    else:
        trend = "Stable"

    avg_demand = sum(demands) / len(demands)
    summary = (
        f"Average demand index: {int(avg_demand)}/100. "
        f"Trend: {trend}. "
    )
    if any(d["demand_index"] >= 80 for d in forecast_data):
        peak_day = max(forecast_data, key=lambda x: x["demand_index"])
        summary += f"Peak day: {peak_day['day']} ({peak_day['date']}) with index {peak_day['demand_index']}."
    else:
        summary += "No high-demand spikes expected in this period."

    return {
        "category": category,
        "days": days,
        "forecast": forecast_data,
        "trend": trend,
        "summary": summary,
    }
