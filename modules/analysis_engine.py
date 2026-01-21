"""
Analysis Engine Module
Core engine for generating insights, strengths, concerns, and predictions
"""

import json
import os
import random

# Load data files
_data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

# Load meanings databases
_meanings_files = {
    "d2": os.path.join(_data_dir, 'planet_house_meanings_d2.json'),
    "d9": os.path.join(_data_dir, 'planet_house_meanings_d9.json'),
    "d10": os.path.join(_data_dir, 'planet_house_meanings_d10.json'),
    "d16": os.path.join(_data_dir, 'planet_house_meanings_d16.json')
}

_meanings_cache = {}
for chart_type, file_path in _meanings_files.items():
    with open(file_path, 'r', encoding='utf-8') as f:
        _meanings_cache[chart_type] = json.load(f)

# Load other data
_strength_keywords_file = os.path.join(_data_dir, 'strength_keywords.json')
_concern_templates_file = os.path.join(_data_dir, 'concern_templates.json')
_prediction_templates_file = os.path.join(_data_dir, 'prediction_templates.json')

with open(_strength_keywords_file, 'r', encoding='utf-8') as f:
    STRENGTH_KEYWORDS = json.load(f)

with open(_concern_templates_file, 'r', encoding='utf-8') as f:
    CONCERN_TEMPLATES = json.load(f)

with open(_prediction_templates_file, 'r', encoding='utf-8') as f:
    PREDICTION_TEMPLATES = json.load(f)


def analyze_chart_section(chart, chart_type: str, section_name: str):
    """
    Analyze a specific chart section and generate insights.
    
    Args:
        chart: VedicBirthChart object
        chart_type: "d2", "d9", "d10", or "d16"
        section_name: "wealth", "marriage", "career", or "health"
    
    Returns:
        dict: Analysis with positive insights, strengths, concerns, and prediction
    """
    # Get the divisional chart
    div_charts = chart.divisional_charts
    # Library uses uppercase keys (D2, D9, D10, D16)
    chart_key_upper = chart_type.upper()
    chart_key_lower = chart_type.lower()
    
    # Try uppercase first, then lowercase
    if chart_key_upper in div_charts:
        div_chart = div_charts[chart_key_upper]
    elif chart_key_lower in div_charts:
        div_chart = div_charts[chart_key_lower]
    else:
        return None
    
    # Get meanings database (use lowercase for our cache)
    meanings_db = _meanings_cache.get(chart_key_lower, {})
    if not meanings_db or "meanings" not in meanings_db:
        return None
    
    planet_meanings = meanings_db["meanings"]
    
    # Analyze all planet-house combinations
    placements = []
    for house in div_chart.houses:
        for planet in house.occupants:
            planet_name = planet.celestial_body
            house_num = str(house.number)
            
            if planet_name in planet_meanings and house_num in planet_meanings[planet_name]:
                meaning_data = planet_meanings[planet_name][house_num]
                
                # Handle two formats:
                # 1. Dict with "positive" and "negative" keys (D2, D9, D16)
                # 2. String directly (D10)
                if isinstance(meaning_data, dict):
                    # Format: {"positive": "...", "negative": "..."}
                    positive = meaning_data.get("positive", "")
                    negative = meaning_data.get("negative", "")
                elif isinstance(meaning_data, str):
                    # Format: Just a string (treat as positive)
                    positive = meaning_data
                    negative = ""  # No negative for string format
                else:
                    # Unknown format, skip
                    continue
                
                if positive or negative:
                    score = _score_placement(planet_name, int(house_num), chart_type)
                    placements.append({
                        "planet": planet_name,
                        "house": int(house_num),
                        "positive": positive,
                        "negative": negative,
                        "score": score
                    })
    
    # Sort by score (highest first)
    placements.sort(key=lambda x: x["score"], reverse=True)
    
    # Get top 3-4 positive insights
    positive_insights = []
    for p in placements[:4]:
        if p["positive"]:
            positive_insights.append({
                "planet": p["planet"],
                "house": p["house"],
                "description": p["positive"],
                "score": p["score"]
            })
    
    # Get strengths
    strengths = _identify_strengths(placements, chart_type, section_name)
    
    # Get concerns (1-2)
    concerns = _identify_concerns(placements, chart_type, section_name)
    
    # Generate general prediction
    prediction = _generate_prediction(placements, chart_type, section_name)
    
    return {
        "chart": chart_type,
        "positive_insights": positive_insights,
        "strengths": strengths,
        "concerns": concerns,
        "general_prediction": prediction
    }


def _score_placement(planet: str, house: int, chart_type: str) -> float:
    """Score a planet-house placement (0-10 scale)."""
    score = 5.0  # Base score
    
    # Benefic planets get bonus
    benefics = ["Jupiter", "Venus", "Moon"]
    if planet in benefics:
        score += 1.5
    
    # Malefic planets get penalty
    malefics = ["Saturn", "Mars", "Sun"]
    if planet in malefics:
        score -= 1.0
    
    # Kendra houses (1, 4, 7, 10) are strong
    if house in [1, 4, 7, 10]:
        score += 1.0
    
    # Trikona houses (1, 5, 9) are auspicious
    if house in [1, 5, 9]:
        score += 0.5
    
    # Trik houses (6, 8, 12) are challenging
    if house in [6, 8, 12]:
        score -= 1.5
    
    # Chart-specific adjustments
    if chart_type == "d10":  # Career chart
        if house == 10:
            score += 2.0
        if house == 2:
            score += 1.0
    elif chart_type == "d2":  # Wealth chart
        if house == 2 or house == 11:
            score += 1.5
    elif chart_type == "d9":  # Marriage chart
        if house == 7:
            score += 2.0
    elif chart_type == "d16":  # Health chart
        if house == 1 or house == 6:
            score += 1.0
    
    return max(0.0, min(10.0, score))


def _identify_strengths(placements: list, chart_type: str, section_name: str) -> list:
    """Identify key strengths from chart placements."""
    strengths = []
    
    # Analyze dominant planets
    planet_counts = {}
    for p in placements:
        planet = p["planet"]
        if planet not in planet_counts:
            planet_counts[planet] = 0
        planet_counts[planet] += p["score"]
    
    # Get top planets
    top_planets = sorted(planet_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Map planets to strengths
    planet_keywords = STRENGTH_KEYWORDS.get("planets", {})
    
    for planet, _ in top_planets:
        if planet in planet_keywords:
            # Get section-specific strengths
            section_strengths = planet_keywords[planet].get(section_name, [])
            if section_strengths:
                strengths.extend(section_strengths[:2])
            else:
                # Fall back to general strengths
                general_strengths = planet_keywords[planet].get("general", [])
                strengths.extend(general_strengths[:2])
    
    # Chart-specific strengths
    if chart_type == "d10":
        for p in placements:
            if p["house"] == 10 and p["score"] > 7:
                strengths.append("Career Excellence")
                break
    
    return list(set(strengths))[:4]  # Return top 4 unique strengths


def _identify_concerns(placements: list, chart_type: str, section_name: str) -> list:
    """Identify concerns or challenges from chart placements."""
    concerns = []
    
    # Get lowest scoring placements with negative meanings
    low_score_placements = [p for p in placements if p["score"] < 4.0 and p["negative"]]
    
    # Get malefic planets in difficult houses
    malefics = ["Saturn", "Mars", "Rahu", "Ketu"]
    difficult_houses = [6, 8, 12]
    
    for p in placements:
        if p["planet"] in malefics and p["house"] in difficult_houses and p["negative"]:
            concern_desc = _generate_concern_description(p, chart_type, section_name)
            concerns.append({
                "planet": p["planet"],
                "house": p["house"],
                "description": concern_desc,
                "severity": "moderate" if p["score"] > 2.0 else "high"
            })
    
    # If no concerns found, use low score placements
    if not concerns and low_score_placements:
        for p in low_score_placements[:2]:
            concern_desc = _generate_concern_description(p, chart_type, section_name)
            concerns.append({
                "planet": p["planet"],
                "house": p["house"],
                "description": concern_desc,
                "severity": "moderate"
            })
    
    return concerns[:2]  # Return top 2 concerns


def _generate_concern_description(placement: dict, chart_type: str, section_name: str) -> str:
    """Generate a constructive concern description."""
    planet = placement["planet"]
    house = placement["house"]
    negative_text = placement.get("negative", "")
    
    # Use the negative text from the database, which is already constructively framed
    if negative_text:
        return negative_text
    
    # Fallback to template
    templates = CONCERN_TEMPLATES.get("templates", {}).get(section_name, {})
    planet_templates = CONCERN_TEMPLATES.get("planet_specific", {})
    
    if planet in planet_templates:
        pattern = planet_templates[planet].get("pattern", "")
        return pattern.format(planet=planet, house=house, topic=section_name)
    
    # Generic concern
    return f"{planet} in {house}th house may require careful attention in {section_name} matters."


def _generate_prediction(placements: list, chart_type: str, section_name: str) -> str:
    """Generate a general prediction for the section."""
    # Analyze overall chart theme
    avg_score = sum(p["score"] for p in placements) / len(placements) if placements else 5.0
    
    # Get templates
    templates = PREDICTION_TEMPLATES.get(section_name, {})
    
    if avg_score >= 7.0:
        predictions = templates.get("positive", [])
    else:
        predictions = templates.get("balanced", [])
    
    if predictions:
        return random.choice(predictions)
    
    # Default prediction
    return f"Your {section_name} journey shows a balanced path forward. Focus on your strengths and be aware of areas that need attention."
