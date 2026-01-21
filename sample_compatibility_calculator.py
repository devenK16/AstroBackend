"""
Sample Compatibility Calculator Module
This shows how to calculate the missing compatibility parameters
"""

# Nakshatra to Varna mapping (27 Nakshatras)
NAKSHATRA_VARNA = {
    "Ashwini": "Brahmin",
    "Bharani": "Kshatriya",
    "Kritika": "Vaishya",
    "Rohini": "Shudra",
    "Mrigashira": "Brahmin",
    "Ardra": "Kshatriya",
    "Punarvasu": "Vaishya",
    "Pushya": "Shudra",
    "Ashlesha": "Brahmin",
    "Magha": "Kshatriya",
    "Purva Phalguni": "Vaishya",
    "Uttara Phalguni": "Shudra",
    "Hasta": "Brahmin",
    "Chitra": "Kshatriya",
    "Swati": "Vaishya",
    "Vishakha": "Shudra",
    "Anuradha": "Brahmin",
    "Jyeshta": "Kshatriya",
    "Mula": "Vaishya",
    "Purva Ashadha": "Shudra",
    "Uttara Ashadha": "Brahmin",
    "Shravana": "Kshatriya",
    "Dhanishta": "Vaishya",
    "Shatabhisha": "Shudra",
    "Purva Bhadrapada": "Brahmin",
    "Uttara Bhadrapada": "Kshatriya",
    "Revati": "Vaishya"
}

# Sign to Vashya mapping
SIGN_VASHYA = {
    "Aries": "Chatuspadha",      # Quadruped
    "Taurus": "Chatuspadha",
    "Gemini": "Nara",             # Human
    "Cancer": "Jalachara",        # Aquatic
    "Leo": "Chatuspadha",
    "Virgo": "Nara",
    "Libra": "Nara",
    "Scorpio": "Keeta",           # Insect
    "Sagittarius": "Chatuspadha",
    "Capricorn": "Chatuspadha",
    "Aquarius": "Nara",
    "Pisces": "Jalachara"
}

# Nakshatra to Yoni mapping (14 pairs)
NAKSHATRA_YONI = {
    "Ashwini": "Horse",
    "Bharani": "Elephant",
    "Kritika": "Sheep",
    "Rohini": "Serpent",
    "Mrigashira": "Serpent",
    "Ardra": "Dog",
    "Punarvasu": "Cat",
    "Pushya": "Goat",
    "Ashlesha": "Cat",
    "Magha": "Rat",
    "Purva Phalguni": "Rat",
    "Uttara Phalguni": "Bull",
    "Hasta": "Buffalo",
    "Chitra": "Tiger",
    "Swati": "Buffalo",
    "Vishakha": "Tiger",
    "Anuradha": "Hare",
    "Jyeshta": "Hare",
    "Mula": "Dog",
    "Purva Ashadha": "Monkey",
    "Uttara Ashadha": "Mongoose",
    "Shravana": "Monkey",
    "Dhanishta": "Lion",
    "Shatabhisha": "Horse",
    "Purva Bhadrapada": "Lion",
    "Uttara Bhadrapada": "Cow",
    "Revati": "Elephant"
}

# Nakshatra to Gan mapping
NAKSHATRA_GAN = {
    "Ashwini": "Deva",
    "Bharani": "Manushya",
    "Kritika": "Rakshasa",
    "Rohini": "Manushya",
    "Mrigashira": "Deva",
    "Ardra": "Manushya",
    "Punarvasu": "Deva",
    "Pushya": "Deva",
    "Ashlesha": "Rakshasa",
    "Magha": "Rakshasa",
    "Purva Phalguni": "Manushya",
    "Uttara Phalguni": "Manushya",
    "Hasta": "Deva",
    "Chitra": "Manushya",
    "Swati": "Deva",
    "Vishakha": "Manushya",
    "Anuradha": "Deva",
    "Jyeshta": "Rakshasa",
    "Mula": "Rakshasa",
    "Purva Ashadha": "Manushya",
    "Uttara Ashadha": "Manushya",
    "Shravana": "Deva",
    "Dhanishta": "Manushya",
    "Shatabhisha": "Rakshasa",
    "Purva Bhadrapada": "Rakshasa",
    "Uttara Bhadrapada": "Rakshasa",
    "Revati": "Deva"
}

# Nakshatra to Nadi mapping
NAKSHATRA_NADI = {
    "Ashwini": "Adi",
    "Bharani": "Madhya",
    "Kritika": "Antya",
    "Rohini": "Antya",
    "Mrigashira": "Madhya",
    "Ardra": "Adi",
    "Punarvasu": "Adi",
    "Pushya": "Madhya",
    "Ashlesha": "Antya",
    "Magha": "Antya",
    "Purva Phalguni": "Madhya",
    "Uttara Phalguni": "Adi",
    "Hasta": "Adi",
    "Chitra": "Madhya",
    "Swati": "Antya",
    "Vishakha": "Antya",
    "Anuradha": "Madhya",
    "Jyeshta": "Adi",
    "Mula": "Adi",
    "Purva Ashadha": "Antya",
    "Uttara Ashadha": "Antya",
    "Shravana": "Adi",
    "Dhanishta": "Madhya",
    "Shatabhisha": "Adi",
    "Purva Bhadrapada": "Antya",
    "Uttara Bhadrapada": "Adi",
    "Revati": "Madhya"
}

# Sign to Tatva (Element) mapping
SIGN_TATVA = {
    "Aries": "Fire",
    "Taurus": "Earth",
    "Gemini": "Air",
    "Cancer": "Water",
    "Leo": "Fire",
    "Virgo": "Earth",
    "Libra": "Air",
    "Scorpio": "Water",
    "Sagittarius": "Fire",
    "Capricorn": "Earth",
    "Aquarius": "Air",
    "Pisces": "Water"
}

# Nakshatra to Paya mapping
NAKSHATRA_PAYA = {
    "Ashwini": "Dhana",      # Gold
    "Bharani": "Mrit",        # Clay
    "Kritika": "Rajat",       # Silver
    "Rohini": "Dhana",
    "Mrigashira": "Mrit",
    "Ardra": "Rajat",
    "Punarvasu": "Loh",       # Iron
    "Pushya": "Dhana",
    "Ashlesha": "Mrit",
    "Magha": "Rajat",
    "Purva Phalguni": "Loh",
    "Uttara Phalguni": "Loh",
    "Hasta": "Dhana",
    "Chitra": "Mrit",
    "Swati": "Rajat",
    "Vishakha": "Loh",
    "Anuradha": "Dhana",
    "Jyeshta": "Mrit",
    "Mula": "Rajat",
    "Purva Ashadha": "Loh",
    "Uttara Ashadha": "Loh",
    "Shravana": "Dhana",
    "Dhanishta": "Mrit",
    "Shatabhisha": "Rajat",
    "Purva Bhadrapada": "Loh",
    "Uttara Bhadrapada": "Mrit",
    "Revati": "Dhana"
}


def calculate_compatibility_details(chart, name: str = ""):
    """
    Calculate all compatibility/matching parameters from the birth chart.
    
    Args:
        chart: VedicBirthChart object from jyotishganit
        name: Person's name (for alphabet extraction)
    
    Returns:
        dict: Dictionary with all compatibility parameters
    """
    # Get Moon's position (Moon is typically the second planet in the list)
    # Find Moon explicitly to be safe
    moon = None
    for planet in chart.d1_chart.planets:
        if planet.celestial_body == "Moon":
            moon = planet
            break
    
    if not moon:
        raise ValueError("Moon position not found in chart")
    
    moon_nakshatra = moon.nakshatra
    moon_sign = moon.sign
    
    # Calculate all parameters
    compatibility = {
        "varna": NAKSHATRA_VARNA.get(moon_nakshatra, "Unknown"),
        "vashya": SIGN_VASHYA.get(moon_sign, "Unknown"),
        "yoni": NAKSHATRA_YONI.get(moon_nakshatra, "Unknown"),
        "gan": NAKSHATRA_GAN.get(moon_nakshatra, "Unknown"),
        "nadi": NAKSHATRA_NADI.get(moon_nakshatra, "Unknown"),
        "tatva": SIGN_TATVA.get(moon_sign, "Unknown"),
        "paya": NAKSHATRA_PAYA.get(moon_nakshatra, "Unknown"),
        "name_alphabet": name[0].upper() if name else ""
    }
    
    return compatibility


def get_sign_lord(sign: str) -> str:
    """
    Get the lord of a zodiac sign.
    
    Args:
        sign: Zodiac sign name
    
    Returns:
        str: Planet name that rules the sign
    """
    SIGN_LORDS = {
        "Aries": "Mars",
        "Taurus": "Venus",
        "Gemini": "Mercury",
        "Cancer": "Moon",
        "Leo": "Sun",
        "Virgo": "Mercury",
        "Libra": "Venus",
        "Scorpio": "Mars",
        "Sagittarius": "Jupiter",
        "Capricorn": "Saturn",
        "Aquarius": "Saturn",
        "Pisces": "Jupiter"
    }
    return SIGN_LORDS.get(sign, "Unknown")


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
    
    # Calculate compatibility details
    compat = calculate_compatibility_details(chart, "John Doe")
    
    print("Compatibility Details:")
    print(f"Varna: {compat['varna']}")
    print(f"Vashya: {compat['vashya']}")
    print(f"Yoni: {compat['yoni']}")
    print(f"Gan: {compat['gan']}")
    print(f"Nadi: {compat['nadi']}")
    print(f"Tatva: {compat['tatva']}")
    print(f"Paya: {compat['paya']}")
    print(f"Name Alphabet: {compat['name_alphabet']}")
