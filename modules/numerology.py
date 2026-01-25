"""
Numerology Module (Vedic / Harish Johari style)
Computes Radical (Psychic), Destiny, and Name numbers from birth date and full name.
Uses data from data/numerology_data.json. Supports karmic debt numbers 13, 14, 16, 19.
"""

import json
import os
import re

# Letter to number (1-9 cycle): A=1..I=9, J=1..R=9, S=1..Z=8 (Pythagorean / Chaldean style)
_LETTER_VALUES = {}
for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    _LETTER_VALUES[c] = (i % 9) + 1 if (i % 9) != 0 else 9
# Fix: 9th letter I=9, 18th R=9, so 27th would be 9 but we only have 26 letters. Actually A=1,B=2,...,I=9,J=1,...,R=9,S=1,T=2,...,Z=8.
# 0-index: A=0 -> 1, B=1 -> 2, ... I=8 -> 9, J=9 -> 1 (9 mod 9 = 0 -> 9), K=10 -> 1, ... R=17 -> 9 (18%9=0->9), S=18 -> 1, ... Z=25 -> 8 (25%9=7 -> 8). So val = (i % 9) + 1 gives 1-9 for 0-8, but for i=8 we get 9, i=9 we get 1. So (i+1)%9 gives 1 for 0, 2 for 1, ... 9 for 8, 1 for 9. So (i % 9) + 1: i=0->1, i=8->9, i=9->1. Good. i=25->(25%9)+1=7+1=8. So Z=8. Correct.

_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
_NUMEROLOGY_DATA_PATH = os.path.join(_DATA_DIR, 'numerology_data.json')
_numerology_data = None


def _load_data():
    global _numerology_data
    if _numerology_data is None:
        with open(_NUMEROLOGY_DATA_PATH, 'r', encoding='utf-8') as f:
            _numerology_data = json.load(f)
    return _numerology_data


def _reduce_to_digit(n):
    """Reduce a number to a single digit 1-9 by repeated digit sum. 0 stays 0."""
    if n == 0:
        return 0
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def _parse_date(date_str):
    """
    Parse date string YYYY-MM-DD into (year, month, day).
    Returns (year, month, day) or None if invalid.
    """
    if not date_str:
        return None
    parts = re.split(r'[-/]', str(date_str).strip())
    if len(parts) != 3:
        return None
    try:
        y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
        if 1 <= m <= 12 and 1 <= d <= 31 and y > 0:
            return (y, m, d)
    except (ValueError, IndexError):
        pass
    return None


def radical_number(day):
    """
    Radical (Psychic) number = digit sum of day of month (1-31).
    Returns int 1-9.
    """
    return _reduce_to_digit(day) or 9


def destiny_number(day, month, year):
    """
    Destiny number = digit sum of day + month + year.
    Returns (single_digit 1-9, raw_sum). raw_sum is used to detect karmic debt 13, 14, 16, 19.
    """
    raw = sum(int(d) for d in str(day) + str(month) + str(year))
    single = _reduce_to_digit(raw) or 9
    return single, raw


def name_number(full_name):
    """
    Name number from full birth name: sum of letter values (A-Z), reduced to 1-9.
    Non-alphabetic characters are ignored. Uses uppercase.
    """
    if not full_name:
        return 9
    s = 0
    for c in str(full_name).upper():
        if c in _LETTER_VALUES:
            s += _LETTER_VALUES[c]
    return _reduce_to_digit(s) or 9


def favourable_alphabets(radical_value):
    """Return letters whose value equals radical_value (1-9)."""
    return [c for c, v in _LETTER_VALUES.items() if v == radical_value]


def get_karmic_debt(raw_sum):
    """If raw destiny sum is 13, 14, 16, or 19, return that karmic number; else None."""
    if raw_sum in (13, 14, 16, 19):
        return raw_sum
    return None


def get_numerology(name, date_str):
    """
    Build full numerology payload from full name and date string (YYYY-MM-DD).
    
    Returns dict with:
      radical_number, destiny_number, name_number,
      favourable_alphabets, favourable_days, favourable_dates, favourable_colours,
      gemstone, deity, mantra, fast_day, ruling_planet, favourable_numbers, direction,
      radical_summary, destiny_summary, name_summary,
      karmic_debt (optional, present when destiny raw sum is 13, 14, 16, or 19)
    """
    data = _load_data()
    numbers_data = data.get("numbers", {})
    karmic_data = data.get("karmic_debt", {})

    parsed = _parse_date(date_str)
    if not parsed:
        return {
            "error": "Invalid date format. Use YYYY-MM-DD.",
            "radical_number": None,
            "destiny_number": None,
            "name_number": None
        }

    year, month, day = parsed
    rad = radical_number(day)
    dest_single, dest_raw = destiny_number(day, month, year)
    name_num = name_number(name)

    # Use radical number for "favourable" fields (main personality)
    num_key = str(rad)
    info = numbers_data.get(num_key, {})

    favourable_dates = info.get("favourable_dates", [])

    def _ordinal(n):
        if 10 <= n % 100 <= 13:
            return str(n) + "th"
        return str(n) + {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    favourable_dates_display = ", ".join(_ordinal(d) for d in favourable_dates)

    result = {
        "radical_number": rad,
        "destiny_number": dest_single,
        "name_number": name_num,
        "name": name.strip() or None,
        "date_of_birth": date_str,
        "favourable_alphabets": favourable_alphabets(rad),
        "favourable_days": info.get("favourable_days", []),
        "favourable_dates": favourable_dates,
        "favourable_dates_display": favourable_dates_display,
        "favourable_number": info.get("friendly_numbers", [1])[0] if info.get("friendly_numbers") else 1,
        "favourable_numbers": info.get("friendly_numbers", []),
        "direction": info.get("direction", ""),
        "auspicious_colour": ", ".join(info.get("favourable_colours", [])[:3]) if info.get("favourable_colours") else "",
        "favourable_colours": info.get("favourable_colours", []),
        "ruling_planet": info.get("ruling_planet", ""),
        "ruling_planet_vedic": info.get("ruling_planet_vedic", ""),
        "gemstone": info.get("gemstone", ""),
        "deity": info.get("deity", ""),
        "mantra": info.get("mantra") or info.get("mantra_alt", ""),
        "mantra_alt": info.get("mantra_alt"),
        "fast_day": info.get("fast_day", ""),
        "radical_summary": info.get("radical_summary", ""),
        "destiny_summary": numbers_data.get(str(dest_single), {}).get("destiny_summary", ""),
        "name_summary": numbers_data.get(str(name_num), {}).get("name_summary", ""),
    }

    # Karmic debt: when raw sum of destiny is 13, 14, 16, or 19
    karmic_raw = get_karmic_debt(dest_raw)
    if karmic_raw is not None:
        kd = karmic_data.get(str(karmic_raw), {})
        result["karmic_debt"] = {
            "number": karmic_raw,
            "reduces_to": kd.get("reduces_to"),
            "summary": kd.get("summary", ""),
            "lesson": kd.get("lesson", ""),
        }
    else:
        result["karmic_debt"] = None

    return result
