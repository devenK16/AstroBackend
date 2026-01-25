"""
Personality Insights Module
Derives personality, natural strengths, negative traits, and "how the world sees you"
from the D1 (Rasi) chart, based on Lagna, Moon nakshatra, planet strengths, and classical sources.
"""

import json
import os

_data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
with open(os.path.join(_data_dir, 'personality_insights_data.json'), 'r', encoding='utf-8') as f:
    _INSIGHTS_DATA = json.load(f)

_SIGN_LORD = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
}
_EXALTATION_SIGN = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn", "Mercury": "Virgo",
    "Jupiter": "Cancer", "Venus": "Pisces", "Saturn": "Libra"
}
_OWN_SIGNS = {
    "Sun": ["Leo"], "Moon": ["Cancer"], "Mars": ["Aries", "Scorpio"],
    "Mercury": ["Gemini", "Virgo"], "Jupiter": ["Sagittarius", "Pisces"],
    "Venus": ["Taurus", "Libra"], "Saturn": ["Capricorn", "Aquarius"]
}
_DEBILITATION_SIGN = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer", "Mercury": "Pisces",
    "Jupiter": "Capricorn", "Venus": "Virgo", "Saturn": "Aries"
}
_SEVEN_GRAHAS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_KENDRA_TRIKONA = {1, 4, 5, 7, 9, 10}
_DUSTHANA = {6, 8, 12}


def _ordinal(n):
    """Return ordinal string for house number: 1 -> '1st', 2 -> '2nd', etc."""
    if n == 1:
        return "1st"
    if n == 2:
        return "2nd"
    if n == 3:
        return "3rd"
    if 4 <= n <= 12:
        return f"{n}th"
    return str(n)


def _get_d1_map(chart):
    """Build planet -> (house, sign), house -> [(planet, sign)], house_lords, lagna_sign."""
    planet_to_house = {}
    house_to_planets = {}
    house_lords = {}
    lagna_sign = None

    d1 = getattr(chart, "d1_chart", None)
    if not d1:
        return planet_to_house, house_to_planets, house_lords, lagna_sign

    houses = getattr(d1, "houses", None)
    if houses:
        for house in houses:
            hnum = getattr(house, "number", None)
            if hnum is None:
                continue
            hnum = int(hnum)
            sign = getattr(house, "sign", "") or ""
            lord = getattr(house, "lord", "")
            if lord:
                house_lords[hnum] = lord
            if hnum == 1:
                lagna_sign = sign
            house_to_planets[hnum] = []
            for occ in getattr(house, "occupants", []):
                p = getattr(occ, "celestial_body", None) or getattr(occ, "planet", None)
                s = getattr(occ, "sign", sign) or sign
                if p:
                    planet_to_house[p] = (hnum, s)
                    house_to_planets[hnum].append((p, s))
        return planet_to_house, house_to_planets, house_lords, lagna_sign

    # Fallback: planets list
    for p in getattr(d1, "planets", []):
        name = getattr(p, "celestial_body", None) or getattr(p, "planet", None)
        h = getattr(p, "house", None)
        s = getattr(p, "sign", "") or ""
        if name and h is not None:
            h = int(h)
            planet_to_house[name] = (h, s)
            house_to_planets.setdefault(h, []).append((name, s))
            if h == 1 and lagna_sign is None:
                lagna_sign = s
    for h in range(1, 13):
        if h not in house_lords and house_to_planets.get(h):
            _, sig = house_to_planets[h][0]
            house_lords[h] = _SIGN_LORD.get(sig, "")
        if h == 1 and lagna_sign is None and house_to_planets.get(h):
            _, lagna_sign = house_to_planets[1][0]

    return planet_to_house, house_to_planets, house_lords, lagna_sign


def _get_moon_nakshatra_from_chart(chart):
    """Get Moon's nakshatra and sign from D1 planets."""
    d1 = getattr(chart, "d1_chart", None)
    if not d1:
        return None, None
    for p in getattr(d1, "planets", []):
        if getattr(p, "celestial_body", None) == "Moon":
            naks = getattr(p, "nakshatra", None) or getattr(p, "nakshatra_name", None)
            sign = getattr(p, "sign", None)
            return (naks or "").strip(), (sign or "").strip()
    return None, None


def _planet_strong(planet, house, sign):
    """True if planet has positional or dignitary strength (own/exalt or in Kendra/Trikona)."""
    if planet not in _SEVEN_GRAHAS:
        return False
    if sign in _OWN_SIGNS.get(planet, []) or _EXALTATION_SIGN.get(planet) == sign:
        return True
    if house in _KENDRA_TRIKONA:
        return True
    return False


def _planet_weak(planet, house, sign):
    """True if planet is in dusthana or debilitation."""
    if planet not in _SEVEN_GRAHAS:
        return False
    if house in _DUSTHANA:
        return True
    if _DEBILITATION_SIGN.get(planet) == sign:
        return True
    return False


def get_personality_insights(chart, panchanga=None, yoga_dosha_result=None):
    """
    Build personality, natural strengths, negative traits, and how the world sees you from the chart.

    Args:
        chart: VedicBirthChart from jyotishganit
        panchanga: Optional dict with keys like nakshatra, nakshatra_pada (overrides Moon nakshatra if present)
        yoga_dosha_result: Optional dict from analyze_yoga_dosha (doshas list) to factor into negative traits

    Returns:
        dict with:
          - personality: str (based on Lagna + Moon nakshatra)
          - lagna_sign: str
          - moon_nakshatra: str
          - moon_sign: str
          - natural_strengths: list of { planet, meaning }
          - negative_traits: list of str
          - how_the_world_sees_you: str
    """
    out = {
        "personality": "",
        "lagna_sign": None,
        "moon_sign": None,
        "moon_nakshatra": None,
        "natural_strengths": [],
        "negative_traits": [],
        "how_the_world_sees_you": ""
    }

    planet_to_house, house_to_planets, house_lords, lagna_sign = _get_d1_map(chart)
    moon_nakshatra, moon_sign = _get_moon_nakshatra_from_chart(chart)
    if panchanga and panchanga.get("nakshatra"):
        moon_nakshatra = moon_nakshatra or panchanga["nakshatra"]

    out["lagna_sign"] = lagna_sign
    out["moon_sign"] = moon_sign
    out["moon_nakshatra"] = moon_nakshatra

    # ---- Strong planets in the kundali (planet, house, sign, meaning); always at least 2 ----
    house_meanings = _INSIGHTS_DATA.get("planet_house_meanings_d1", {})
    # House priority for fallback (1=best): 1,10,5,9,4,7,2,11,3,6,8,12
    _HOUSE_PRIORITY = (1, 10, 5, 9, 4, 7, 2, 11, 3, 6, 8, 12)
    strong_planets_list = []
    for planet in _SEVEN_GRAHAS:
        if planet not in planet_to_house:
            continue
        h, sign = planet_to_house[planet]
        if not _planet_strong(planet, h, sign):
            continue
        meaning = (house_meanings.get(planet) or {}).get(str(h))
        if not meaning:
            meaning = f"{planet} in the {_ordinal(h)} house in {sign} gives strength in matters of that house and supports your chart when well placed."
        strong_planets_list.append({
            "planet": planet,
            "house": h,
            "sign": sign,
            "meaning": meaning
        })
    # Ensure at least 2 strong planets: add next-best by house priority if needed
    added_planets = {p["planet"] for p in strong_planets_list}
    if len(strong_planets_list) < 2:
        candidates = []
        for planet in _SEVEN_GRAHAS:
            if planet in added_planets or planet not in planet_to_house:
                continue
            h, sign = planet_to_house[planet]
            try:
                rank = _HOUSE_PRIORITY.index(h)
            except ValueError:
                rank = 99
            candidates.append((rank, planet, h, sign))
        candidates.sort(key=lambda x: x[0])
        for _, planet, h, sign in candidates:
            if len(strong_planets_list) >= 2:
                break
            meaning = (house_meanings.get(planet) or {}).get(str(h))
            if not meaning:
                meaning = f"{planet} in the {_ordinal(h)} house in {sign} influences matters of that house and contributes to your chart."
            strong_planets_list.append({"planet": planet, "house": h, "sign": sign, "meaning": meaning})
            added_planets.add(planet)
    out["strong_planets_in_houses"] = strong_planets_list

    # ---- Personality: Lagna + Nakshatra (descriptive paragraph, 3-4+ sentences) ----
    sign_traits = _INSIGHTS_DATA.get("sign_personality", {})
    naks_traits = _INSIGHTS_DATA.get("nakshatra_personality", {})
    parts = []
    if lagna_sign and lagna_sign in sign_traits:
        parts.append(sign_traits[lagna_sign])
    if moon_nakshatra and moon_nakshatra in naks_traits:
        parts.append(naks_traits[moon_nakshatra])
    if parts:
        out["personality"] = " ".join(parts)
    else:
        out["personality"] = f"Your chart is ruled by Lagna sign {lagna_sign or 'unknown'} and Moon nakshatra {moon_nakshatra or 'unknown'}. These shape your core personality and emotional nature according to classical Vedic astrology."

    # ---- Natural strengths: always 3-4 descriptive traits (full sentences) ----
    strength_meanings = _INSIGHTS_DATA.get("planet_strength_meaning", {})
    sign_pos = _INSIGHTS_DATA.get("sign_positive_traits", {})
    naks_pos = _INSIGHTS_DATA.get("nakshatra_positive_traits", {})
    positive_pool = []
    seen_planet = set()
    for planet in _SEVEN_GRAHAS:
        if planet not in planet_to_house:
            continue
        h, sign = planet_to_house[planet]
        if _planet_strong(planet, h, sign) and planet not in seen_planet:
            seen_planet.add(planet)
            meaning = strength_meanings.get(planet)
            if meaning:
                positive_pool.append({"planet": planet, "meaning": meaning})
    if not positive_pool:
        for p in ("Jupiter", "Venus", "Mercury", "Moon", "Sun"):
            if p in planet_to_house and p not in seen_planet:
                h, sign = planet_to_house[p]
                if h in _KENDRA_TRIKONA:
                    seen_planet.add(p)
                    meaning = strength_meanings.get(p)
                    if meaning:
                        positive_pool.append({"planet": p, "meaning": meaning})
                    if len(positive_pool) >= 4:
                        break
    for sent in sign_pos.get(lagna_sign or "", [])[:2]:
        positive_pool.append({"planet": f"Lagna ({lagna_sign})", "meaning": sent})
    for sent in naks_pos.get(moon_nakshatra or "", [])[:2]:
        positive_pool.append({"planet": f"Moon ({moon_nakshatra})", "meaning": sent})
    out["natural_strengths"] = positive_pool[:4]

    # ---- Negative traits: always exactly 2 descriptive traits (full sentences) ----
    weakness_meanings = _INSIGHTS_DATA.get("planet_weakness_meaning", {})
    neg_house = _INSIGHTS_DATA.get("negative_trait_house", {})
    sign_neg = _INSIGHTS_DATA.get("sign_negative_traits", {})
    naks_neg = _INSIGHTS_DATA.get("nakshatra_negative_traits", {})
    default_neg = _INSIGHTS_DATA.get("default_negative_traits", [])
    negative_pool = []
    for planet in _SEVEN_GRAHAS:
        if planet not in planet_to_house:
            continue
        h, sign = planet_to_house[planet]
        if _planet_weak(planet, h, sign):
            meaning = weakness_meanings.get(planet)
            if meaning:
                negative_pool.append(meaning)
            if str(h) in neg_house:
                negative_pool.append(neg_house[str(h)])
    if yoga_dosha_result and isinstance(yoga_dosha_result.get("doshas"), list):
        for d in yoga_dosha_result["doshas"]:
            name = d.get("name", "")
            if name and "Kemadruma" in name:
                negative_pool.append("According to the classics, Kemadruma (Moon without planets in 2nd and 12th from it) can bring emotional loneliness, lack of support, and a tendency to feel unknown or unsupported even in crowds.")
            elif name and "Papa Kartari" in name:
                negative_pool.append("Papa Kartari indicates pressure on important areas of life—such as marriage, self, or progeny—because malefics flank a key house; obstacles and delays in that sphere may be experienced.")
            elif name and "Mangal" in name:
                negative_pool.append("Mangal Dosha (Mars in 1st, 2nd, 4th, 7th, 8th or 12th) is traditionally associated with delay or friction in marriage and partnership unless the partner's chart also has the dosha or suitable remedial measures are considered.")
    for sent in sign_neg.get(lagna_sign or "", [])[:2]:
        negative_pool.append(sent)
    for sent in naks_neg.get(moon_nakshatra or "", [])[:2]:
        negative_pool.append(sent)
    for sent in default_neg:
        negative_pool.append(sent)
    seen_neg = []
    for s in negative_pool:
        if s not in seen_neg:
            seen_neg.append(s)
    out["negative_traits"] = seen_neg[:2]

    # ---- How the world sees you: descriptive 2-3 sentences (10th lord + Lagna element) ----
    tenth_lord = house_lords.get(10) if house_lords else None
    world_by_lord = _INSIGHTS_DATA.get("world_sees_by_tenth_lord", {})
    sign_element = _INSIGHTS_DATA.get("sign_element", {})
    world_by_element = _INSIGHTS_DATA.get("world_sees_by_lagna_element", {})
    world_parts = []
    if tenth_lord and tenth_lord in world_by_lord:
        world_parts.append(world_by_lord[tenth_lord])
    elem = sign_element.get(lagna_sign, "") if lagna_sign else ""
    if elem and elem in world_by_element:
        world_parts.append(world_by_element[elem])
    if "Sun" in planet_to_house and planet_to_house["Sun"][0] == 10:
        world_parts.append("You are often in the limelight and seen as someone with authority or visibility.")
    if world_parts:
        out["how_the_world_sees_you"] = " ".join(world_parts)
    else:
        out["how_the_world_sees_you"] = f"Others tend to see you through your 10th house of career and public image and through your rising sign ({lagna_sign or 'Lagna'}). You leave an impression of someone with a distinct presence and a clear professional or social role."

    return out
