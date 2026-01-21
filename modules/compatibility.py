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


def calculate_compatibility_details(chart, name: str = ""):
    """
    Calculate all compatibility/matching parameters from the birth chart.
    
    Args:
        chart: VedicBirthChart object from jyotishganit
        name: Person's name (for alphabet extraction)
    
    Returns:
        dict: Dictionary with all compatibility parameters
    """
    # Get Moon's position
    moon = None
    for planet in chart.d1_chart.planets:
        if planet.celestial_body == "Moon":
            moon = planet
            break
    
    if not moon:
        raise ValueError("Moon position not found in chart")
    
    moon_nakshatra = moon.nakshatra
    moon_sign = moon.sign
    
    # Get Sign Lord
    SIGN_LORDS = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
    }
    sign_lord = SIGN_LORDS.get(moon_sign, "Unknown")
    
    # Calculate all parameters
    compatibility = {
        "varna": COMPAT_DATA["nakshatra_varna"].get(moon_nakshatra, "Unknown"),
        "vashya": _get_vashya_type(moon_sign),
        "yoni": COMPAT_DATA["nakshatra_yoni"].get(moon_nakshatra, {}).get("yoni", "Unknown"),
        "gan": COMPAT_DATA["nakshatra_gan"].get(moon_nakshatra, "Unknown"),
        "nadi": COMPAT_DATA["nakshatra_nadi"].get(moon_nakshatra, "Unknown"),
        "tatva": COMPAT_DATA["sign_tatva"].get(moon_sign, "Unknown"),
        "paya": COMPAT_DATA["nakshatra_paya"].get(moon_nakshatra, "Unknown"),
        "name_alphabet": name[0].upper() if name else "",
        "sign": moon_sign,
        "sign_lord": sign_lord,
        "nakshatra": moon_nakshatra,
        "nakshatra_pada": moon.pada if hasattr(moon, 'pada') else None
    }
    
    return compatibility


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
