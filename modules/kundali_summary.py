"""
Kundali Summary Module
Computes Manglik status, Sade Sati (current), and current Dasha for display above charts.
"""

from datetime import datetime

# Zodiac sign order (for Sade Sati: 12th, 1st, 2nd from Moon)
SIGNS_ORDER = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]


def _moon_sign_from_chart(chart):
    """Get natal Moon sign from D1 chart."""
    if not chart or not getattr(chart, "d1_chart", None):
        return None
    for p in getattr(chart.d1_chart, "planets", []):
        cb = getattr(p, "celestial_body", None) or getattr(p, "planet", None)
        if cb and str(cb).strip().lower() == "moon":
            return (getattr(p, "sign", None) or getattr(p, "rashi", None) or "").strip()
    return None


def _saturn_sign_from_chart(chart):
    """Get Saturn sign from a chart (natal or transit)."""
    if not chart or not getattr(chart, "d1_chart", None):
        return None
    for p in getattr(chart.d1_chart, "planets", []):
        cb = getattr(p, "celestial_body", None) or getattr(p, "planet", None)
        if cb and str(cb).strip().lower() == "saturn":
            return (getattr(p, "sign", None) or getattr(p, "rashi", None) or "").strip()
    # Try houses with occupants (from JSON-style structure)
    houses = getattr(chart.d1_chart, "houses", None)
    if houses:
        for house in houses:
            for occ in getattr(house, "occupants", []):
                cb = getattr(occ, "celestial_body", None) or getattr(occ, "planet", None)
                if cb and str(cb).strip().lower() == "saturn":
                    return (getattr(occ, "sign", None) or getattr(occ, "rashi", None) or "").strip()
    return None


def is_sade_sati(moon_sign: str, saturn_sign: str) -> bool:
    """
    Sade Sati = Saturn transiting 12th, 1st, or 2nd house from natal Moon (by sign).
    Returns True if Saturn is in the sign before Moon (12th), Moon sign (1st), or sign after Moon (2nd).
    """
    if not moon_sign or not saturn_sign:
        return False
    try:
        moon_idx = SIGNS_ORDER.index(moon_sign.strip())
    except ValueError:
        return False
    try:
        saturn_idx = SIGNS_ORDER.index(saturn_sign.strip())
    except ValueError:
        return False
    # 12th from Moon = (moon_idx - 1) % 12, 1st = moon_idx, 2nd = (moon_idx + 1) % 12
    twelfth = (moon_idx - 1) % 12
    first = moon_idx
    second = (moon_idx + 1) % 12
    return saturn_idx in (twelfth, first, second)


def get_kundali_summary(chart, yoga_dosha_result=None, dasha_data=None,
                        latitude=None, longitude=None, timezone_offset=5.5,
                        transit_chart_fn=None):
    """
    Compute Manglik status, Sade Sati (present or not), and current Dasha string.

    Args:
        chart: VedicBirthChart (natal)
        yoga_dosha_result: Result from analyze_yoga_dosha(chart) for Manglik
        dasha_data: Result from get_dasha_data(chart) for current dasha
        latitude, longitude, timezone_offset: For computing transit (Sade Sati)
        transit_chart_fn: Optional callable (lat, lon, tz) -> chart for "today".
                          If None, will use jyotishganit.calculate_birth_chart with datetime.now().

    Returns:
        dict: {
          "manglik_status": "Yes" | "No",
          "sade_sati_status": "Present" | "Not present",
          "current_dasha": "Ketu - Saturn" (mahadasha - antardasha),
          "current_dasha_detail": { optional summary fields }
        }
    """
    out = {
        "manglik_status": "No",
        "sade_sati_status": "Not present",
        "current_dasha": None,
        "current_dasha_detail": None
    }

    # ----- Manglik (Mangal Dosha) -----
    if yoga_dosha_result and isinstance(yoga_dosha_result, dict):
        doshas = yoga_dosha_result.get("doshas") or []
        for d in doshas:
            if isinstance(d, dict) and "Mangal" in (d.get("name") or ""):
                out["manglik_status"] = "Yes"
                break

    # ----- Current Dasha -----
    if dasha_data and isinstance(dasha_data, dict):
        summary = dasha_data.get("summary") or {}
        maha = summary.get("current_mahadasha")
        anta = summary.get("current_antardasha")
        if maha:
            out["current_dasha"] = f"{maha} - {anta}" if anta else maha
            out["current_dasha_detail"] = {
                "current_mahadasha": maha,
                "current_antardasha": anta,
                "current_pratyantardasha": summary.get("current_pratyantardasha"),
                "current_mahadasha_start": summary.get("current_mahadasha_start"),
                "current_mahadasha_end": summary.get("current_mahadasha_end"),
                "current_antardasha_start": summary.get("current_antardasha_start"),
                "current_antardasha_end": summary.get("current_antardasha_end"),
            }

    # ----- Sade Sati (Saturn transit 12th, 1st, 2nd from Moon) -----
    moon_sign = _moon_sign_from_chart(chart)
    if not moon_sign:
        return out

    transit_chart = None
    if transit_chart_fn and callable(transit_chart_fn):
        try:
            transit_chart = transit_chart_fn(latitude, longitude, timezone_offset)
        except Exception:
            pass
    if transit_chart is None and latitude is not None and longitude is not None:
        try:
            from jyotishganit import calculate_birth_chart
            now = datetime.utcnow()
            # Use local time for the given timezone
            from datetime import timedelta
            local_now = now + timedelta(hours=float(timezone_offset or 0))
            transit_chart = calculate_birth_chart(
                birth_date=local_now,
                latitude=float(latitude),
                longitude=float(longitude),
                timezone_offset=float(timezone_offset or 5.5),
                name="Transit"
            )
        except Exception:
            pass

    if transit_chart:
        saturn_sign = _saturn_sign_from_chart(transit_chart)
        if saturn_sign and is_sade_sati(moon_sign, saturn_sign):
            out["sade_sati_status"] = "Present"

    return out
