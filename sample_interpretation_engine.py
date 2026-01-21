"""
Sample Interpretation Engine
This shows the structure for generating predictions and interpretations
"""

# Example: Planet-House Meanings for D10 (Career Chart)
D10_PLANET_HOUSE_MEANINGS = {
    "Sun": {
        "1": "Strong leadership qualities, natural authority, recognition in career",
        "2": "Wealth through career, financial stability, good earning capacity",
        "3": "Courage, communication skills, success through writing or media",
        "4": "Career in real estate, agriculture, or property-related fields",
        "5": "Creative career, teaching, speculation, or entertainment industry",
        "6": "Success over competitors, career in service, healthcare, or law",
        "7": "Partnerships in business, career through spouse or partners",
        "8": "Hidden sources of income, career in research or occult sciences",
        "9": "Career aligned with dharma, teaching, philosophy, or long-distance travel",
        "10": "Excellent career prospects, high position, recognition, authority",
        "11": "Gains through career, networking, friends help in profession",
        "12": "Career abroad, foreign connections, or career in spiritual fields"
    },
    "Moon": {
        "1": "Public recognition, career in public service or media",
        "2": "Wealth through business, food industry, or liquid assets",
        "3": "Career in communication, writing, or short-distance travel",
        "4": "Career in real estate, mother-related fields, or comfort-oriented work",
        "5": "Creative career, teaching, or entertainment",
        "6": "Service-oriented career, healthcare, or overcoming obstacles",
        "7": "Career through partnerships, public relations, or hospitality",
        "8": "Hidden career opportunities, research, or transformation",
        "9": "Career in teaching, philosophy, or long-distance travel",
        "10": "Fluctuating career, but good public image",
        "11": "Gains through networking, friends, or social media",
        "12": "Career abroad, spiritual pursuits, or behind-the-scenes work"
    },
    "Mars": {
        "1": "Dynamic leadership, career in military, sports, or engineering",
        "2": "Wealth through courage and action, but may have expenses",
        "3": "Career in communication, writing, or technical fields",
        "4": "Career in real estate, construction, or property",
        "5": "Career in sports, entertainment, or creative fields",
        "6": "Excellent for competitive careers, law, or healthcare",
        "7": "Career through partnerships, but may have conflicts",
        "8": "Career in research, investigation, or transformation",
        "9": "Career in law, philosophy, or long-distance travel",
        "10": "Strong career drive, leadership positions, but may have conflicts",
        "11": "Gains through courage and networking",
        "12": "Career abroad, hidden enemies, or spiritual transformation"
    },
    "Mercury": {
        "1": "Career in communication, writing, or business",
        "2": "Wealth through business, writing, or communication",
        "3": "Excellent for writing, communication, or media careers",
        "4": "Career in education, real estate, or property",
        "5": "Career in teaching, writing, or creative fields",
        "6": "Career in service, healthcare, or technical writing",
        "7": "Career through partnerships, business, or trade",
        "8": "Career in research, investigation, or technical analysis",
        "9": "Career in teaching, philosophy, or long-distance communication",
        "10": "Career in business, communication, or administration",
        "11": "Gains through networking, friends, or communication",
        "12": "Career abroad, writing, or behind-the-scenes communication"
    },
    "Jupiter": {
        "1": "Career in teaching, law, or spiritual fields, high recognition",
        "2": "Wealth through knowledge, teaching, or guidance",
        "3": "Career in writing, teaching, or communication",
        "4": "Career in education, real estate, or property",
        "5": "Career in teaching, philosophy, or creative education",
        "6": "Career in law, teaching, or service",
        "7": "Career through partnerships, especially in education or law",
        "8": "Career in research, philosophy, or transformation",
        "9": "Excellent for teaching, philosophy, or spiritual careers",
        "10": "High position, recognition, career in law, teaching, or administration",
        "11": "Gains through knowledge, networking, or guidance",
        "12": "Career abroad, spiritual pursuits, or teaching"
    },
    "Venus": {
        "1": "Career in arts, beauty, luxury, or entertainment",
        "2": "Wealth through arts, beauty, or luxury businesses",
        "3": "Career in arts, communication, or creative writing",
        "4": "Career in real estate, property, or comfort-oriented fields",
        "5": "Career in arts, entertainment, or creative fields",
        "6": "Career in service, healthcare, or beauty industry",
        "7": "Career through partnerships, especially in arts or business",
        "8": "Career in research, transformation, or hidden arts",
        "9": "Career in arts, philosophy, or long-distance travel",
        "10": "Career in arts, luxury, or entertainment industry",
        "11": "Gains through arts, networking, or luxury businesses",
        "12": "Career abroad, spiritual arts, or behind-the-scenes creative work"
    },
    "Saturn": {
        "1": "Delayed but stable career, career in old age, or government service",
        "2": "Wealth through hard work, but may have delays",
        "3": "Career in communication, but with delays or obstacles",
        "4": "Career in real estate, property, or old structures",
        "5": "Career in teaching or creative fields, but with delays",
        "6": "Career in service, healthcare, or overcoming obstacles",
        "7": "Career through partnerships, but may have delays or obstacles",
        "8": "Career in research, transformation, or long-lasting work",
        "9": "Career in philosophy, teaching, or long-distance travel",
        "10": "Delayed but stable career, government service, or authority",
        "11": "Gains through hard work, networking, or old friends",
        "12": "Career abroad, spiritual pursuits, or isolation"
    },
    "Rahu": {
        "1": "Unconventional career, technology, or foreign connections",
        "2": "Wealth through unconventional means or technology",
        "3": "Career in communication, technology, or media",
        "4": "Career in real estate, property, or unconventional fields",
        "5": "Career in technology, entertainment, or creative fields",
        "6": "Career in service, technology, or overcoming obstacles",
        "7": "Career through partnerships, especially foreign or unconventional",
        "8": "Career in research, technology, or transformation",
        "9": "Career in philosophy, technology, or long-distance travel",
        "10": "Unconventional career, technology, or high position",
        "11": "Gains through networking, technology, or unconventional means",
        "12": "Career abroad, technology, or spiritual transformation"
    },
    "Ketu": {
        "1": "Spiritual career, research, or behind-the-scenes work",
        "2": "Wealth through research, spirituality, or hidden sources",
        "3": "Career in communication, research, or writing",
        "4": "Career in real estate, property, or hidden fields",
        "5": "Career in research, spirituality, or creative fields",
        "6": "Career in service, research, or overcoming obstacles",
        "7": "Career through partnerships, especially spiritual or research",
        "8": "Career in research, transformation, or spiritual fields",
        "9": "Career in philosophy, spirituality, or long-distance travel",
        "10": "Spiritual career, research, or behind-the-scenes authority",
        "11": "Gains through research, spirituality, or networking",
        "12": "Career abroad, spirituality, or complete transformation"
    }
}

# Similar structures needed for D2, D9, D16
# D2_PLANET_HOUSE_MEANINGS = {...}  # Wealth chart
# D9_PLANET_HOUSE_MEANINGS = {...}  # Marriage chart
# D16_PLANET_HOUSE_MEANINGS = {...} # Health chart


def analyze_chart_section(chart, chart_type: str, section_name: str):
    """
    Analyze a specific chart section (D2, D9, D10, D16) and generate insights.
    
    Args:
        chart: VedicBirthChart object
        chart_type: "d2", "d9", "d10", or "d16"
        section_name: "wealth", "marriage", "career", or "health"
    
    Returns:
        dict: Analysis with positive insights, strengths, concerns, and prediction
    """
    # Get the divisional chart
    div_chart = chart.divisional_charts.get(chart_type)
    if not div_chart:
        return None
    
    # Get planet-house meanings based on chart type
    meanings_db = get_meanings_database(chart_type)
    
    # Analyze all planet-house combinations
    placements = []
    for house in div_chart.houses:
        for planet in house.occupants:
            planet_name = planet.celestial_body
            house_num = house.number
            meaning = meanings_db.get(planet_name, {}).get(str(house_num), "")
            
            if meaning:
                score = score_placement(planet_name, house_num, chart_type)
                placements.append({
                    "planet": planet_name,
                    "house": house_num,
                    "meaning": meaning,
                    "score": score
                })
    
    # Sort by score (highest first)
    placements.sort(key=lambda x: x["score"], reverse=True)
    
    # Get top 3-4 positive insights
    positive_insights = placements[:4]
    
    # Get strengths based on chart analysis
    strengths = identify_strengths(placements, chart_type)
    
    # Get concerns (lowest scoring or malefic placements)
    concerns = identify_concerns(placements, chart_type)
    
    # Generate general prediction
    prediction = generate_prediction(placements, chart_type, section_name)
    
    return {
        "positive_insights": positive_insights,
        "strengths": strengths,
        "concerns": concerns,
        "general_prediction": prediction
    }


def get_meanings_database(chart_type: str):
    """Get the appropriate meanings database for chart type."""
    databases = {
        "d2": {},  # D2_PLANET_HOUSE_MEANINGS
        "d9": {},  # D9_PLANET_HOUSE_MEANINGS
        "d10": D10_PLANET_HOUSE_MEANINGS,
        "d16": {}  # D16_PLANET_HOUSE_MEANINGS
    }
    return databases.get(chart_type, {})


def score_placement(planet: str, house: int, chart_type: str) -> float:
    """
    Score a planet-house placement (0-10 scale).
    Higher score = more positive/beneficial.
    """
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
        if house == 10:  # 10th house is career house
            score += 2.0
        if house == 2:  # 2nd house is wealth from career
            score += 1.0
    
    return max(0.0, min(10.0, score))  # Clamp between 0-10


def identify_strengths(placements: list, chart_type: str) -> list:
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
    planet_strengths = {
        "Sun": ["Leadership", "Authority", "Recognition"],
        "Moon": ["Intuition", "Public Relations", "Emotional Intelligence"],
        "Mars": ["Courage", "Action", "Competition"],
        "Mercury": ["Communication", "Business", "Intelligence"],
        "Jupiter": ["Wisdom", "Teaching", "Guidance"],
        "Venus": ["Creativity", "Arts", "Luxury"],
        "Saturn": ["Discipline", "Stability", "Long-term Planning"],
        "Rahu": ["Innovation", "Technology", "Unconventional"],
        "Ketu": ["Research", "Spirituality", "Transformation"]
    }
    
    for planet, _ in top_planets:
        if planet in planet_strengths:
            strengths.extend(planet_strengths[planet])
    
    # Chart-specific strengths
    if chart_type == "d10":
        # Check for strong 10th house
        for p in placements:
            if p["house"] == 10 and p["score"] > 7:
                strengths.append("Career Excellence")
                break
    
    return list(set(strengths))[:4]  # Return top 4 unique strengths


def identify_concerns(placements: list, chart_type: str) -> list:
    """Identify concerns or challenges from chart placements."""
    concerns = []
    
    # Get lowest scoring placements
    low_score_placements = [p for p in placements if p["score"] < 4.0]
    
    # Get malefic planets in difficult houses
    malefics = ["Saturn", "Mars", "Rahu", "Ketu"]
    difficult_houses = [6, 8, 12]
    
    for p in placements:
        if p["planet"] in malefics and p["house"] in difficult_houses:
            concerns.append({
                "planet": p["planet"],
                "house": p["house"],
                "description": generate_concern_description(p, chart_type),
                "severity": "moderate" if p["score"] > 2.0 else "high"
            })
    
    return concerns[:2]  # Return top 2 concerns


def generate_concern_description(placement: dict, chart_type: str) -> str:
    """Generate a constructive concern description."""
    planet = placement["planet"]
    house = placement["house"]
    
    templates = {
        "d10": {
            "Saturn": f"Saturn in {house}th house may bring initial delays or require patience in career development—think careful planning to avoid setbacks.",
            "Mars": f"Mars in {house}th house could indicate conflicts or impulsive decisions—awareness helps channel energy constructively.",
            "Rahu": f"Rahu in {house}th house may bring fluctuations or unconventional challenges—staying grounded helps navigate changes."
        }
    }
    
    chart_templates = templates.get(chart_type, {})
    return chart_templates.get(planet, f"{planet} in {house}th house may require careful attention.")


def generate_prediction(placements: list, chart_type: str, section_name: str) -> str:
    """Generate a general prediction for the section."""
    # Analyze overall chart theme
    avg_score = sum(p["score"] for p in placements) / len(placements) if placements else 5.0
    
    predictions = {
        "d10": {
            "career": "Your financial life is shaped by timing more than luck. When preparation meets opportunity, growth follows naturally. The more aligned your actions are with your strengths, the more stable and rewarding your wealth journey becomes."
        },
        "d2": {
            "wealth": "Your chart paints a promising financial journey: Early efforts build a solid foundation, with peaks in gains post-challenges. Imagine a life of abundance fueled by your intuitive nature—wealth flows when you trust your instincts!"
        }
    }
    
    # Return specific prediction or default
    return predictions.get(chart_type, {}).get(section_name, 
        "Your chart shows a balanced path forward. Focus on your strengths and be aware of areas that need attention.")


# Example usage:
if __name__ == "__main__":
    from jyotishganit import calculate_birth_chart
    from datetime import datetime
    
    # Create a sample chart
    chart = calculate_birth_chart(
        birth_date=datetime(1990, 1, 15, 10, 30),
        latitude=28.6139,
        longitude=77.2090,
        timezone_offset=5.5,
        name="John Doe"
    )
    
    # Analyze career section (D10)
    career_analysis = analyze_chart_section(chart, "d10", "career")
    
    print("Career Analysis:")
    print(f"Positive Insights: {len(career_analysis['positive_insights'])}")
    print(f"Strengths: {career_analysis['strengths']}")
    print(f"Concerns: {len(career_analysis['concerns'])}")
    print(f"Prediction: {career_analysis['general_prediction']}")
