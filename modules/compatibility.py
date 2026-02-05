"""
Compatibility Calculator Module
Calculates all compatibility/matching parameters from birth chart
"""

import json
import os

# Load compatibility data
_data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
_compatibility_file = os.path.join(_data_dir, 'compatibility_data.json')

with open(_compatibility_file, 'r', encoding='utf-8') as f:
    COMPAT_DATA = json.load(f)

# Alternate nakshatra spellings from library -> our JSON key (for lookups)
NAKSHATRA_NORMALIZE = {
    "Dhanishtha": "Dhanishta",
    "Uttara Asadha": "Uttara Ashadha",
    "Purva Asadha": "Purva Ashadha",
    "Uttara Ashada": "Uttara Ashadha",
    "Purva Ashada": "Purva Ashadha",
    "Uttara Bhadrapad": "Uttara Bhadrapada",
    "Purva Bhadrapad": "Purva Bhadrapada",
    "Uttar Bhadrapad": "Uttara Bhadrapada",
    "Poorv Bhadrapad": "Purva Bhadrapada",
    "Shatabhishak": "Shatabhisha",
    "Mrigashirsha": "Mrigashira",
    "Mrigasira": "Mrigashira",
    "Mrigshira": "Mrigashira",
    "Chitta": "Chitra",
    "Jyeshtha": "Jyeshta",
    "Krittika": "Kritika",
    "Mool": "Mula",
    "Shravan": "Shravana",
    "Poorv Phalguni": "Purva Phalguni",
    "Uttar Phalguni": "Uttara Phalguni",
    "Poorv Ashadh": "Purva Ashadha",
    "Uttar Ashadh": "Uttara Ashadha",
}


def _normalize_nakshatra(name: str) -> str:
    """Return nakshatra key for use in COMPAT_DATA lookups."""
    if not name:
        return ""
    s = (name or "").strip()
    # Try known alternate spellings first
    out = NAKSHATRA_NORMALIZE.get(s, s)
    # Ensure title-case for lookup (e.g. "UTTARA BHADRAPADA" -> "Uttara Bhadrapada")
    if out and out not in COMPAT_DATA.get("nakshatra_nadi", {}):
        out = " ".join(w.capitalize() for w in out.split())
    return out


def _get_moon_house_from_chart(chart):
    """Get Moon's D1 house number from chart (houses with occupants or planet.house)."""
    d1 = getattr(chart, "d1_chart", None)
    if not d1:
        return None
    # From planet object first
    for p in getattr(d1, "planets", []):
        if getattr(p, "celestial_body", None) == "Moon":
            h = getattr(p, "house", None)
            if h is not None:
                return int(h)
            break
    # Build house map from houses with occupants
    houses = getattr(d1, "houses", None)
    if houses:
        for house in houses:
            hnum = getattr(house, "number", None)
            if hnum is None:
                continue
            for occ in getattr(house, "occupants", []):
                body = getattr(occ, "celestial_body", None) or getattr(occ, "planet", None)
                if body == "Moon":
                    return int(hnum)
    # Fallback: planets with house
    for p in getattr(d1, "planets", []):
        if getattr(p, "celestial_body", None) == "Moon":
            h = getattr(p, "house", None)
            if h is not None:
                return int(h)
            break
    return None


def _moon_from_chart_result(chart_result: dict) -> dict:
    """
    Extract Moon's sign, nakshatra, house, pada from the serialized chart JSON.
    chart_result = result of get_birth_chart_json(chart) (parsed dict).
    Returns dict with keys: sign, nakshatra, house, pada (or None for missing).
    """
    out = {"sign": None, "nakshatra": None, "house": None, "pada": None}
    if not chart_result or not isinstance(chart_result, dict):
        return out
    # Library may use d1Chart with houses[].occupants (no top-level planets list)
    d1 = chart_result.get("d1Chart") or chart_result.get("d1_chart") or {}
    # Collect all planet positions from d1.planets or from houses[].occupants
    candidates = []
    planets = d1.get("planets") or chart_result.get("planets") or []
    if isinstance(planets, list):
        candidates.extend(planets)
    houses = d1.get("houses") or []
    if isinstance(houses, list):
        for house in houses:
            if not isinstance(house, dict):
                continue
            for occ in house.get("occupants") or []:
                if isinstance(occ, dict):
                    candidates.append(occ)
    for p in candidates:
        if not isinstance(p, dict):
            continue
        name = (p.get("celestial_body") or p.get("celestialBody") or p.get("planet") or p.get("name") or "").strip()
        if name.lower() != "moon":
            continue
        out["sign"] = (p.get("sign") or p.get("rashi") or "").strip() or None
        out["nakshatra"] = (p.get("nakshatra") or p.get("nakshatra_name") or "").strip() or None
        h = p.get("house")
        if h is not None:
            try:
                out["house"] = int(h)
            except (TypeError, ValueError):
                pass
        pa = p.get("pada") or p.get("nakshatra_pada")
        if pa is not None:
            try:
                out["pada"] = int(pa)
            except (TypeError, ValueError):
                pass
        break
    return out


def calculate_compatibility_details(chart, name: str = "", chart_result: dict = None):
    """
    Calculate all compatibility/matching parameters from the birth chart.
    Uses chart_result (JSON from get_birth_chart_json) when provided, so values
    match the serialized chart. name is not used for name_alphabet (that comes from nakshatra pada).
    
    Args:
        chart: VedicBirthChart object from jyotishganit
        name: Person's name (unused for compatibility; kept for API signature)
        chart_result: Optional dict from get_birth_chart_json(chart) to read Moon from JSON
    
    Returns:
        dict: Dictionary with all compatibility parameters
    """
    moon_sign = None
    moon_nakshatra_raw = None
    moon_house = None
    moon_pada = None

    # Prefer chart_result (serialized JSON) so we use the same data as the API response
    if chart_result and isinstance(chart_result, dict):
        m = _moon_from_chart_result(chart_result)
        moon_sign = m.get("sign")
        moon_nakshatra_raw = m.get("nakshatra")
        moon_house = m.get("house")
        moon_pada = m.get("pada")

    # Fallback: read from chart object (support multiple attribute names)
    if not moon_sign or not moon_nakshatra_raw:
        moon = None
        d1 = getattr(chart, "d1_chart", None) if chart else None
        if d1:
            for planet in getattr(d1, "planets", []):
                cb = getattr(planet, "celestial_body", None) or getattr(planet, "planet", None) or getattr(planet, "name", None)
                if cb and str(cb).strip().lower() == "moon":
                    moon = planet
                    break
            else:
                moon = None
        else:
            moon = None
        if moon:
            if not moon_sign:
                moon_sign = (getattr(moon, "sign", None) or getattr(moon, "rashi", None) or "").strip()
            if not moon_nakshatra_raw:
                moon_nakshatra_raw = (getattr(moon, "nakshatra", None) or getattr(moon, "nakshatra_name", None) or "").strip()
            if moon_house is None:
                moon_house = getattr(moon, "house", None)
                if moon_house is not None:
                    moon_house = int(moon_house)
            if moon_pada is None:
                moon_pada = getattr(moon, "pada", None) or getattr(moon, "nakshatra_pada", None)
                if moon_pada is not None:
                    moon_pada = int(moon_pada)

        if moon_house is None and chart:
            moon_house = _get_moon_house_from_chart(chart)

    if not moon_sign and not moon_nakshatra_raw:
        raise ValueError("Moon position not found in chart or chart_result")

    moon_nakshatra = _normalize_nakshatra(moon_nakshatra_raw or "") or (moon_nakshatra_raw or "").strip()
    moon_sign = (moon_sign or "").strip()
    if not moon_sign and moon_nakshatra:
        moon_sign = "Unknown"
    if not (1 <= (moon_pada or 0) <= 4):
        moon_pada = 1

    # Get Sign Lord
    SIGN_LORDS = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
    }
    sign_lord = SIGN_LORDS.get(moon_sign, "Unknown")

    # Varna: from Moon sign (Rashi), not nakshatra
    varna = _get_varna_from_sign(moon_sign)

    # Paya: by Janma Nakshatra (Revati/Ashwini/Bharani=Gold; Kritika/Rohini/Mrigashira=Iron; Ardra..Anuradha=Silver; Jyeshtha..Uttara Bhadrapada=Copper)
    paya_key = COMPAT_DATA["nakshatra_paya"].get(moon_nakshatra, "Unknown")
    paya_display = {"Dhana": "Gold", "Rajat": "Silver", "Tamra": "Copper", "Loh": "Iron"}.get(paya_key, paya_key)
    paya = paya_display

    # Name alphabet: only from Janma Nakshatra Pada letters (never from user's name)
    name_alphabet = _get_name_letters_for_nakshatra_pada(moon_nakshatra, moon_pada or 1)

    compatibility = {
        "varna": varna,
        "vashya": _get_vashya_type(moon_sign),
        "yoni": COMPAT_DATA["nakshatra_yoni"].get(moon_nakshatra, {}).get("yoni", "Unknown"),
        "gan": COMPAT_DATA["nakshatra_gan"].get(moon_nakshatra, "Unknown"),
        "nadi": COMPAT_DATA["nakshatra_nadi"].get(moon_nakshatra, "Unknown"),
        "tatva": COMPAT_DATA["sign_tatva"].get(moon_sign, "Unknown"),
        "paya": paya,
        "name_alphabet": name_alphabet,
        "sign": moon_sign,
        "sign_lord": sign_lord,
        "nakshatra": moon_nakshatra,
        "nakshatra_pada": moon_pada
    }

    return compatibility


def _get_varna_from_sign(sign: str) -> str:
    """Varna from Moon sign (Rashi), per classical marriage matching (e.g. Indian Astrology Articles)."""
    if not sign:
        return "Unknown"
    varna_by_sign = {
        "Cancer": "Brahmin", "Scorpio": "Brahmin", "Pisces": "Brahmin",
        "Aries": "Kshatriya", "Leo": "Kshatriya", "Sagittarius": "Kshatriya",
        "Taurus": "Vaishya", "Virgo": "Vaishya", "Capricorn": "Vaishya",
        "Gemini": "Shudra", "Libra": "Shudra", "Aquarius": "Shudra",
    }
    return varna_by_sign.get(sign, "Unknown")


def _get_paya_from_house(house: int) -> str:
    """Paya from Moon's house position: 1,6,11=Gold; 2,5,9=Silver; 3,7,10=Copper (Tamra); 4,8,12=Iron (Loh)."""
    if house in (1, 6, 11):
        return "Dhana"
    if house in (2, 5, 9):
        return "Rajat"
    if house in (3, 7, 10):
        return "Tamra"
    if house in (4, 8, 12):
        return "Loh"
    return "Unknown"


def _get_name_letters_for_nakshatra_pada(nakshatra: str, pada: int) -> str:
    """Favourable name letters (Swar) for the native's Janma Nakshatra Pada, with Roman and Hindi (Devanagari)."""
    letters = COMPAT_DATA.get("nakshatra_pada_letters", {})
    padas = letters.get(nakshatra, [])
    if not padas or not (1 <= pada <= 4):
        return ""
    swar = padas[pada - 1]
    if not swar:
        return ""
    # Data may be "Roman (Devanagari)" or plain "Roman"; return as-is so Hindi shows when present
    return swar


def _get_vashya_type(sign: str) -> str:
    """Get Vashya type from sign."""
    vashya_map = {
        "Aries": "Chatuspadha",
        "Taurus": "Chatuspadha",
        "Gemini": "Nara",
        "Cancer": "Jalachara",
        "Leo": "Chatuspadha",
        "Virgo": "Nara",
        "Libra": "Nara",
        "Scorpio": "Keeta",
        "Sagittarius": "Chatuspadha",
        "Capricorn": "Chatuspadha",
        "Aquarius": "Nara",
        "Pisces": "Jalachara"
    }
    return vashya_map.get(sign, "Unknown")
