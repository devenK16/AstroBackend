"""
Yoga and Dosha Analyzer Module
Detects 50+ planetary Yogas and Doshas present in the D1 (Rasi) chart.
Based on BPHS, Phaladeepika, Saravali and related sources.
"""

# Seven traditional planets + nodes (Rahu, Ketu)
_TRADITIONAL_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
_SEVEN_GRAHAS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# Malefics for Papa Kartari etc. (natural malefics)
_MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

# Benefics (natural)
_BENEFICS = {"Moon", "Mercury", "Jupiter", "Venus"}

# House lords: sign -> lord
_SIGN_LORD = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
}

# Kendra (angle), Trikona, Upachaya, Panaphara, Apoklima, Dusthana
_KENDRA = {1, 4, 7, 10}
_TRIKONA = {1, 5, 9}
_KENDRA_TRIKONA = _KENDRA | _TRIKONA
_UPACHAYA = {3, 6, 10, 11}
_PANAPHARA = {2, 5, 8, 11}
_APOKLIMA = {3, 6, 9, 12}
_DUSTHANA = {6, 8, 12}

# Exaltation and own signs (for strength checks)
_EXALTATION_SIGN = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn", "Mercury": "Virgo",
    "Jupiter": "Cancer", "Venus": "Pisces", "Saturn": "Libra"
}
_OWN_SIGNS = {
    "Sun": ["Leo"], "Moon": ["Cancer"], "Mars": ["Aries", "Scorpio"],
    "Mercury": ["Gemini", "Virgo"], "Jupiter": ["Sagittarius", "Pisces"],
    "Venus": ["Taurus", "Libra"], "Saturn": ["Capricorn", "Aquarius"]
}
# Pancha Mahapurusha: planet -> (own + exaltation) signs in Kendra
_PANCHA_SIGNS = {
    "Mars": ["Aries", "Scorpio", "Capricorn"],
    "Mercury": ["Gemini", "Virgo"],
    "Jupiter": ["Sagittarius", "Pisces", "Cancer"],
    "Venus": ["Taurus", "Libra", "Pisces"],
    "Saturn": ["Capricorn", "Aquarius", "Libra"],
}

# Detailed effects from classical texts (Phaladeepika, Saravali, BPHS).
# Written as description of the native / person with this yoga or dosha.
_YOGA_EFFECTS = {
    "Ruchaka Yoga": "The native with Ruchaka Yoga has a long face. He or she acquires wealth by courageous deeds, is full of valour and power, and conquers enemies. Such a person may be arrogant but becomes famous by merit, commands an army, and is successful in ventures.",
    "Bhadra Yoga": "The person with Bhadra Yoga at birth will be long-lived, intelligent, and clean in thoughts and body. He or she is praised by learned persons, is very rich and prosperous, and is eloquent in speech.",
    "Hamsa Yoga": "One born with Hamsa Yoga becomes a king or a high political or government dignitary, respected by good people. The native may have marks of Conch, Lotus, Fish and Ankusha on hands and feet, a beautiful body, enjoys delicious food, and is virtuous.",
    "Malavya Yoga": "The native with Malavya Yoga has strong limbs, is very rich, blessed with wife and children, and prosperous. He or she enjoys pleasures of life, owns good vehicles, is renowned and learned, and has imperturbable senses.",
    "Sasa Yoga": "The person with Sasa Yoga at birth is acclaimed by all, has good servants, and is strong. He or she may become head of a village or a king. The native may be wicked by nature and associate with women not his or her own, and may be inclined to use others' wealth, but remains happy.",
    "Kemadruma Yoga": "One born under Kemadruma Yoga, even if from a royal family, will become unknown and lead a miserable life. The native may be addicted to immoral ways, face poverty, live as a menial, and be wickedly disposed.",
    "Sunapha Yoga": "The person with Sunapha Yoga at birth will be a monarch or his or her equal, with self-acquired property, and will be respected and renowned for intellectual ability and riches. The native is wealthy, virtuous, learned in Shastras, famous, and may be a king or minister, highly intelligent.",
    "Anapha Yoga": "The person born with Anapha Yoga will be powerful and will enjoy good health. He or she will have a sweet temperament and become famous; all worldly comforts will be available. The native will be well dressed, contented and happy. According to Saravali, such a person is also eloquent in speech, magnanimous, virtuous, enjoys food, drink, flowers and robes, is calm and has a beautiful body.",
    "Durudhara Yoga": "The native with Durudhara Yoga will enjoy all comforts of life as may be available to a ruler. He or she will own abundant wealth and vehicles, will be generous, and will be attended to by faithful servants.",
    "Subhavesi Yoga": "The person with Subhavesi Yoga at birth will be very good looking, happy, meritorious, valiant, a king or like a king, and virtuous.",
    "Subhavasi Yoga": "The person with Subhavasi Yoga will be renowned, dear to all, and very rich and prosperous. He or she will be governed and liked by the king or authority.",
    "Subhobhayachari Yoga": "The native having this yoga in the birth chart will have an attractive body, will be soft spoken, will delight the world, will be eloquent, renowned and wealthy.",
    "Papavesi Yoga": "The person with Papavesi Yoga (inauspicious) at birth may unfairly defame others, may not be beautiful, and may move in the company of low and wicked people.",
    "Papavasi Yoga": "The person with Papavasi Yoga (inauspicious) will be dishonest, harsh and abusive in speech, and will associate with wicked people. He or she may be unvirtuous though having knowledge of Shastras and Scriptures.",
    "Papobhayachari Yoga": "The person born in this yoga (inauspicious) may suffer mentally due to dishonour in public and may be devoid of wealth and fortune.",
    "Subha Kartari Yoga": "Subha Kartari Yoga at birth will make the native long-lived, fearless, healthy and without enemies.",
    "Papa Kartari Yoga": "Papa Kartari Yoga (inauspicious) will make the person miserable, bereft of wife and children. He or she may have defective limbs and a short life.",
    "Amala Yoga": "The person born with Amala Yoga will be virtuous, will have faith in religion, will be happy and fortunate, and will be honoured by the king or authority. He or she will have an amiable nature and will always have a smile on the face. The native possesses lands, is wealthy, blessed with sons, famous, prosperous and wise.",
    "Mahabhagya Yoga (male/day)": "The person with Mahabhagya Yoga will be immensely popular in the public, will be very generous in giving gifts, and will possess a very high reputation. He or she will be a ruler of the earth or equivalent, will have a life span of about 80 years, and will be of spotless character.",
    "Mahabhagya Yoga (female/night)": "A female born with this yoga will be exceedingly fortunate and will possess sweet manners.",
    "Kesari Yoga": "The person with Kesari Yoga will destroy his or her enemies like a lion. He or she will address assemblies with wisdom and in a noble manner, will be passionate and emotional in behaviour, will enjoy a long life, and will attain a high reputation. The native is intelligent and will achieve everything by his or her own valour.",
    "Sakata Yoga": "The person with Sakata Yoga at birth will be unhappy and unfortunate. He or she will be unable to achieve any fame and will lead an ordinary life. Sometimes his or her luck dawns and at other times it fades away.",
    "Adhama Yoga": "When the Moon is in a Kendra from the Sun, the native has effects of lesser fortune (Adhama).",
    "Sama Yoga": "When the Moon is in a Panaphara house from the Sun, the native experiences effects of a medium nature (Sama).",
    "Varishta Yoga": "The person born with Varishta Yoga will be wealthy, will possess vehicles, will achieve fame, and will enjoy happiness. He or she will acquire knowledge and will have intellectual equipment, modesty, ability, learning and will be generous.",
    "Vasumati Yoga": "The person born with Vasumati Yoga will always remain at his or her place (native land) and will be very wealthy.",
    "Pushkala Yoga": "The native of Pushkala Yoga will be revered by kings, will be renowned and wealthy, and will wear expensive clothes and ornaments. He or she will be fortunate, will be a lord of many men, and will achieve a high status.",
    "Shubhamala Yoga": "The person with Shubhamala Yoga at birth will be an administrator or high official, will be revered by the king, and will indulge in pleasures of life. He or she will be generous, helpful to others, devoted to kinsmen, brave, and blessed with a virtuous wife and sons.",
    "Ashubhamala Yoga": "The person with Ashubhamala Yoga (inauspicious) at birth will be wayward, unhappy, may torture or kill others, will be timid and ungrateful, will not pay respect to Brahmins, and will be unpopular and quarrelsome.",
    "Lakshmi Yoga": "The native with Lakshmi Yoga will be constantly engaged in enjoyment with a woman or partner of noble temperament. He or she will be brilliant, capable of providing protection to his or her people, and will be a favourite of Goddess Lakshmi (very wealthy). The native will be free from diseases, will enjoy rides in beautiful palanquins, horses or elephants, will be generous in gifts, and will be a capable ruler and favourite of subjects.",
    "Gouri Yoga": "The native with Gouri Yoga will have a beautiful body and will be a friend of the king or authority. He or she will possess good qualities, will be blessed with sons, will belong to an illustrious family. The face will be like a lotus, and the native will be praised for his or her successes.",
    "Saraswati Yoga": "The native with Saraswati Yoga will be highly intelligent. He or she will be very competent in composing prose, drama and poetry, and will be learned in Alankar Shastra and Mathematics. The native will be skilled in poetry, in narrative composition and in the exposition of sacred texts; his or her fame will spread over the three worlds. The native will be extremely wealthy, blessed with wife and children, fortunate, and revered by the greatest of kings.",
    "Srikanta Yoga": "The person with Srikanta Yoga at birth will wear Rudraksha rosaries and his or her body will look white shining with sacred ashes. He or she will be very liberal, will be constantly in meditation of Lord Shiva, will regularly perform the prescribed rites and will be devoted to the worship of Lord Shiva. The native will be a friend of the virtuous, will have no animosity against any other religious belief, will become influential, and his or her heart will be enlightened by the worship of Lord Shiva.",
    "Srinatha Yoga": "The native of Srinatha Yoga will be wealthy, splendorous and soft spoken. His or her manner of speaking will be pleasant and witty. The native may have in the body marks of Lord Narayana (such as conch, chakra). He or she will be engaged in recitations of religious songs about Narayana, will be a devotee of Vishnu, will be respected by others, will be very handsome and attractive, and will be blessed with a virtuous wife and noble children.",
    "Varunchi (Virinchi) Yoga": "The person with Varunchi (Virinchi) Yoga will be extremely intelligent and will be fully absorbed in the knowledge of Brahm. He or she will never deviate from the code of conduct prescribed by the Vedas, will be full of good qualities and will always be happy at heart. The native will have many distinguished disciples, will be sweet and noble in speech, will be blessed with much wealth, wife and children, will shine with spiritual lustre, will be long-lived, will have complete control over the senses, and will be revered by kings.",
    "Raja Yoga (9th-10th lord)": "The person with this Raja Yoga will be a king or equal to a king. When he or she sets out on a journey, will be greeted by bands like Bheri and sounds of conch. The native will have a royal umbrella, will be accompanied by elephants, horses and palanquins, bards and minstrels will recite poems in his or her praise, and will be presented gifts by eminent persons.",
    "Raja Yoga (Kendra-Trikona)": "The native with this Raja Yoga (from Kendra and Trikona lord combination) will enjoy prosperity, authority and success, and may become a king or equal.",
    "Neechabhanga Raja Yoga": "When debilitation is cancelled by the conditions of this yoga, the native becomes a very powerful king or emperor. He or she will be wealthy, will perform virtuous actions, and will be revered by other kings.",
    "Adhiyoga": "The person born with Adhiyoga will be a commander (e.g. Superintendent of Police or commander of an army), a minister, or a ruler of a District or State. He or she will be renowned, prosperous, wealthy, long-lived and large souled, and will become lord of men.",
    "Parvata Yoga": "The person born with Parvata Yoga will always be wealthy and happy. He or she will perform acts which afford lasting benefit to others (such as construction of dharmashalas, hospitals, temples, reservoirs). The native may become the ruler of the earth.",
    "Veena (Vallaki) Yoga": "The person born in this yoga (seven planets in seven different signs) is fond of dancing, singing and playing musical instruments, and is wealthy.",
    "Dhanu (Dharma) Yoga": "The person born with this yoga (seven planets in six signs) will be generous, a king or like a king, and a benefactor.",
    "Harsha Yoga": "The person born with this yoga (seven planets in five signs) indulges in enjoyment of life, is wealthy, of good conduct, and has relatives.",
    "Kendra Sankhya Yoga": "The person with this yoga (seven planets in four signs) at birth will acquire wealth and agricultural lands.",
    "Shula Yoga": "The person with this yoga (seven planets in three signs) at birth may be wrathful, of violent disposition and poor.",
    "Yuga Yoga": "The person with this yoga (seven planets in two signs) in the birth chart may be heretical and without wealth.",
    "Gola Yoga": "The person born with this yoga (all seven planets in one sign) may be indolent, short-lived, without wealth, sinful, and may associate with low type of persons.",
}

_DOSHA_EFFECTS = {
    "Mangal Dosha (Kuja Dosha)": "When Mars occupies the 1st, 2nd, 4th, 7th, 8th or 12th house, the native has Mangal Dosha. It may cause delay or friction in marriage. The native may lose the spouse or face early death of the partner unless matched with another Mangal dosha native. Marriage-matching texts advise matching with a partner who also has Mangal Dosha to cancel the effect.",
    "Papa Kartari Dosha": "When malefics flank an important house (e.g. 6th and 8th around the 7th), the native experiences Papa Kartari. There will be pressure on that area of life—marriage, self or progeny—and obstacles in related matters.",
    "Kemadruma Dosha": "When the Moon has no planets in the 2nd and 12th houses from it, the native has Kemadruma as a dosha. He or she may suffer from loneliness, lack of support and emotional challenges. The classical texts say that this combination can make even a king beg.",
}


def _planet_in_own_or_exaltation(planet, sign):
    """True if planet is in its own or exaltation sign."""
    if sign in _OWN_SIGNS.get(planet, []):
        return True
    if _EXALTATION_SIGN.get(planet) == sign:
        return True
    return False


def _house_offset_from(base_house, offset):
    """House number that is offset from base (1-based)."""
    if base_house is None:
        return None
    return ((base_house - 1 + offset - 1) % 12) + 1


def _get_d1_planet_house_map(chart):
    """
    Build planet -> (house_number, sign) and house_number -> list of (planet, sign) from D1.
    Returns (planet_to_house: dict, house_to_planets: dict, house_lords: dict).
    """
    planet_to_house = {}
    house_to_planets = {}
    house_lords = {}

    d1 = getattr(chart, "d1_chart", None)
    if not d1:
        return planet_to_house, house_to_planets, house_lords

    # Prefer houses: each house has number, sign, lord, occupants
    houses = getattr(d1, "houses", None)
    if houses:
        for house in houses:
            hnum = getattr(house, "number", None)
            if hnum is None:
                continue
            hnum = int(hnum)
            sign = getattr(house, "sign", "")
            lord = getattr(house, "lord", "")
            if lord:
                house_lords[hnum] = lord
            house_to_planets[hnum] = []
            occupants = getattr(house, "occupants", [])
            for occ in occupants:
                p = getattr(occ, "celestial_body", None) or getattr(occ, "planet", None)
                s = getattr(occ, "sign", sign)
                if p:
                    planet_to_house[p] = (hnum, s)
                    house_to_planets[hnum].append((p, s))
        return planet_to_house, house_to_planets, house_lords

    # Fallback: use planets list if each has house
    planets = getattr(d1, "planets", [])
    for p in planets:
        name = getattr(p, "celestial_body", None) or getattr(p, "planet", None)
        h = getattr(p, "house", None)
        s = getattr(p, "sign", "")
        if name and h is not None:
            h = int(h)
            planet_to_house[name] = (h, s)
            house_to_planets.setdefault(h, []).append((name, s))

    # House lords from first occupant's sign or from houses if available later
    for h in range(1, 13):
        if h not in house_lords and house_to_planets.get(h):
            # Infer sign from first occupant
            _, sign = house_to_planets[h][0]
            house_lords[h] = _SIGN_LORD.get(sign, "")

    return planet_to_house, house_to_planets, house_lords


def _moon_house(chart):
    """Get Moon's D1 house number."""
    d1 = getattr(chart, "d1_chart", None)
    if not d1:
        return None
    for p in getattr(d1, "planets", []):
        if getattr(p, "celestial_body", None) == "Moon":
            return getattr(p, "house", None)
    # From house map
    planet_to_house, _, _ = _get_d1_planet_house_map(chart)
    if "Moon" in planet_to_house:
        return planet_to_house["Moon"][0]
    return None


def _house_from_moon(moon_house, offset):
    """House number that is offset from Moon (1 = same, 2 = next, etc.)."""
    return _house_offset_from(moon_house, offset)


def _sun_house(chart, planet_to_house):
    """Get Sun's D1 house number."""
    if "Sun" in planet_to_house:
        return planet_to_house["Sun"][0]
    return None


def _add_yoga(result, name, description, effects=None):
    """Append yoga if name not already present. effects = detailed results from classical texts."""
    if not any(r.get("name") == name for r in result):
        entry = {"name": name, "description": description, "type": "yoga"}
        if effects is not None:
            entry["effects"] = effects
        else:
            src_effects = _YOGA_EFFECTS.get(name)
            if src_effects:
                entry["effects"] = src_effects
        result.append(entry)


def detect_yogas(chart):
    """
    Detect 50+ planetary Yogas present in the D1 chart.
    Returns list of dicts: [{ "name": "...", "description": "...", "type": "yoga", "effects": "..."? }, ...]
    When available from classical texts (Phaladeepika, Saravali), "effects" gives detailed results/phal.
    """
    result = []
    planet_to_house, house_to_planets, house_lords = _get_d1_planet_house_map(chart)
    if not planet_to_house:
        return result

    moon_house = _moon_house(chart)
    sun_house = _sun_house(chart, planet_to_house)

    # ----- 1–5: Pancha Mahapurusha (planet in Kendra in own/exaltation sign) -----
    for yoga_name, planet, signs, desc in [
        ("Ruchaka", "Mars", _PANCHA_SIGNS["Mars"], "Mars in a Kendra (1, 4, 7 or 10) in own or exaltation sign."),
        ("Bhadra", "Mercury", _PANCHA_SIGNS["Mercury"], "Mercury in a Kendra in own or exaltation sign."),
        ("Hamsa", "Jupiter", _PANCHA_SIGNS["Jupiter"], "Jupiter in a Kendra in own or exaltation sign."),
        ("Malavya", "Venus", _PANCHA_SIGNS["Venus"], "Venus in a Kendra in own or exaltation sign."),
        ("Sasa", "Saturn", _PANCHA_SIGNS["Saturn"], "Saturn in a Kendra in own or exaltation sign."),
    ]:
        if planet not in planet_to_house:
            continue
        h, sign = planet_to_house[planet]
        if h in _KENDRA and sign in signs:
            _add_yoga(result, f"{yoga_name} Yoga", desc)

    # ----- 6–9: Lunar Yogas (from Moon: 2nd and 12th) -----
    if moon_house is not None:
        h2 = _house_from_moon(moon_house, 2)
        h12 = _house_from_moon(moon_house, 12)
        count_2 = len([x for x in house_to_planets.get(h2, []) if x[0] not in ("Rahu", "Ketu")])
        count_12 = len([x for x in house_to_planets.get(h12, []) if x[0] not in ("Rahu", "Ketu")])
        if count_2 == 0 and count_12 == 0:
            _add_yoga(result, "Kemadruma Yoga", "No planets in 2nd and 12th from Moon.")
        elif count_2 > 0 and count_12 == 0:
            _add_yoga(result, "Sunapha Yoga", "Planet(s) in 2nd from Moon only.")
        elif count_12 > 0 and count_2 == 0:
            _add_yoga(result, "Anapha Yoga", "Planet(s) in 12th from Moon only.")
        elif count_2 > 0 and count_12 > 0:
            _add_yoga(result, "Durudhara Yoga", "Planets in both 2nd and 12th from Moon.")

    # ----- 10–11: Sun-based Vesi / Vasi / Ubhayachari (from Sun) -----
    if sun_house is not None:
        h2_sun = _house_offset_from(sun_house, 2)
        h12_sun = _house_offset_from(sun_house, 12)
        plan_2 = {p for p, _ in house_to_planets.get(h2_sun, []) if p in _BENEFICS}
        plan_12 = {p for p, _ in house_to_planets.get(h12_sun, []) if p in _BENEFICS}
        mal_2 = {p for p, _ in house_to_planets.get(h2_sun, []) if p in _MALEFICS}
        mal_12 = {p for p, _ in house_to_planets.get(h12_sun, []) if p in _MALEFICS}
        if plan_2 and not plan_12:
            _add_yoga(result, "Subhavesi Yoga", "Benefic(s) in 2nd from Sun only.")
        if plan_12 and not plan_2:
            _add_yoga(result, "Subhavasi Yoga", "Benefic(s) in 12th from Sun only.")
        if plan_2 and plan_12:
            _add_yoga(result, "Subhobhayachari Yoga", "Benefics in both 2nd and 12th from Sun.")
        if mal_2 and not mal_12:
            _add_yoga(result, "Papavesi Yoga", "Malefic(s) in 2nd from Sun only.")
        if mal_12 and not mal_2:
            _add_yoga(result, "Papavasi Yoga", "Malefic(s) in 12th from Sun only.")
        if mal_2 and mal_12:
            _add_yoga(result, "Papobhayachari Yoga", "Malefics in both 2nd and 12th from Sun.")

    # ----- 12–13: Subha / Papa Kartari (2nd and 12th from Lagna) -----
    ben_2 = {p for p, _ in house_to_planets.get(2, []) if p in _BENEFICS}
    ben_12 = {p for p, _ in house_to_planets.get(12, []) if p in _BENEFICS}
    mal_2_lag = {p for p, _ in house_to_planets.get(2, []) if p in _MALEFICS}
    mal_12_lag = {p for p, _ in house_to_planets.get(12, []) if p in _MALEFICS}
    if ben_2 and ben_12:
        _add_yoga(result, "Subha Kartari Yoga", "Benefics in 2nd and 12th from Lagna.")
    if mal_2_lag and mal_12_lag:
        _add_yoga(result, "Papa Kartari Yoga", "Malefics in 2nd and 12th from Lagna.")

    # ----- 14: Amala (benefic in 10th from Lagna or Moon) -----
    for base, label in [(1, "Lagna"), (moon_house, "Moon")]:
        if base is None:
            continue
        h10 = _house_offset_from(base, 10)
        occupants = [p for p, _ in house_to_planets.get(h10, [])]
        if any(p in _BENEFICS for p in occupants):
            _add_yoga(result, "Amala Yoga", "Benefic in 10th from " + label + ".")

    # ----- 15: Mahabhagya (Lagna, Sun, Moon all odd for male day / all even for female night; we check odd/even only) -----
    lagna_sign = house_to_planets.get(1, [])[0][1] if house_to_planets.get(1) else None
    sun_sign = planet_to_house.get("Sun", (None, None))[1] if "Sun" in planet_to_house else None
    moon_sign = planet_to_house.get("Moon", (None, None))[1] if "Moon" in planet_to_house else None
    odd_signs = {"Aries", "Gemini", "Leo", "Libra", "Sagittarius", "Aquarius"}
    even_signs = {"Taurus", "Cancer", "Virgo", "Scorpio", "Capricorn", "Pisces"}
    if lagna_sign and sun_sign and moon_sign:
        if all(s in odd_signs for s in (lagna_sign, sun_sign, moon_sign)):
            _add_yoga(result, "Mahabhagya Yoga (male/day)", "Lagna, Sun and Moon in odd signs (male or day birth).")
        if all(s in even_signs for s in (lagna_sign, sun_sign, moon_sign)):
            _add_yoga(result, "Mahabhagya Yoga (female/night)", "Lagna, Sun and Moon in even signs (female or night birth).")

    # ----- 16–17: Kesari, Sakata (Moon from Jupiter) -----
    if "Jupiter" in planet_to_house and moon_house is not None:
        jup_house = planet_to_house["Jupiter"][0]
        moon_from_jup = ((moon_house - jup_house - 1) % 12) + 1
        if moon_from_jup in (1, 4, 7, 10):
            _add_yoga(result, "Kesari Yoga", "Moon in Kendra (1st, 4th, 7th or 10th) from Jupiter.")
        if moon_from_jup in (6, 8, 12):
            moon_in_kendra_lag = moon_house in _KENDRA
            if not moon_in_kendra_lag:
                _add_yoga(result, "Sakata Yoga", "Moon in 6th, 8th or 12th from Jupiter (Moon not in Kendra from Lagna).")

    # ----- 18–20: Adhama, Sama, Varishta (Moon from Sun) -----
    if sun_house is not None and moon_house is not None:
        moon_from_sun = ((moon_house - sun_house - 1) % 12) + 1
        if moon_from_sun in (1, 4, 7, 10):
            _add_yoga(result, "Adhama Yoga", "Moon in Kendra from Sun.")
        if moon_from_sun in (2, 5, 8, 11):
            _add_yoga(result, "Sama Yoga", "Moon in Panaphara (2nd, 5th, 8th, 11th) from Sun.")
        if moon_from_sun in (3, 6, 9, 12):
            _add_yoga(result, "Varishta Yoga", "Moon in Apoklima (3rd, 6th, 9th, 12th) from Sun.")

    # ----- 21: Vasumati (all benefics in Upachaya 3,6,10,11 from Lagna or Moon) -----
    for base in [1, moon_house]:
        if base is None:
            continue
        upachaya_houses = [_house_offset_from(base, h) for h in (3, 6, 10, 11)]
        benefics_placed = set()
        for uh in upachaya_houses:
            for p, _ in house_to_planets.get(uh, []):
                if p in _BENEFICS:
                    benefics_placed.add(p)
        if len(benefics_placed) >= 3:
            _add_yoga(result, "Vasumati Yoga", "All benefics in Upachaya houses (3, 6, 10, 11) from Lagna or Moon.")

    # ----- 22: Pushkala (lords of Lagna and Moon's signs together in Kendra or mutual friend, strong planet aspects Lagna) -----
    if house_lords.get(1) and moon_house and house_lords.get(moon_house):
        lagna_lord = house_lords[1]
        moon_sign_lord = house_lords[moon_house]
        for planet, (h, _) in planet_to_house.items():
            if planet not in (lagna_lord, moon_sign_lord):
                continue
            if h in _KENDRA_TRIKONA:
                _add_yoga(result, "Pushkala Yoga", "Lords of Lagna and Moon's signs in Kendra/Trikona with strength.")
                break

    # ----- 23–24: Shubhamala, Ashubhamala (planets in 5,6,7 vs 8,6,12) -----
    signs_occupied = set()
    for _, (_, s) in planet_to_house.items():
        if s:
            signs_occupied.add(s)
    houses_5_6_7 = [_house_offset_from(1, x) for x in (5, 6, 7)]
    count_567 = sum(1 for h in houses_5_6_7 if house_to_planets.get(h))
    if count_567 >= 2:
        occup_567 = sum(len(house_to_planets.get(h, [])) for h in houses_5_6_7)
        if occup_567 >= 5:
            _add_yoga(result, "Shubhamala Yoga", "Planets in 5th, 6th and 7th houses.")
    for h in (8, 6, 12):
        if len(house_to_planets.get(h, [])) >= 3:
            _add_yoga(result, "Ashubhamala Yoga", "Planets in 8th, 6th and 12th houses.")
            break

    # ----- 25–26: Lakshmi, Gouri -----
    if "Venus" in planet_to_house and 9 in house_lords:
        vh, vs = planet_to_house["Venus"]
        lord9 = house_lords[9]
        if vh in _KENDRA_TRIKONA and _planet_in_own_or_exaltation("Venus", vs):
            if lord9 in planet_to_house:
                l9h, l9s = planet_to_house[lord9]
                if l9h in _KENDRA_TRIKONA and _planet_in_own_or_exaltation(lord9, l9s):
                    _add_yoga(result, "Lakshmi Yoga", "Venus and 9th lord in own or exaltation sign in Kendra or Trikona.")
    if "Moon" in planet_to_house and "Jupiter" in planet_to_house:
        mh, ms = planet_to_house["Moon"]
        if mh in _KENDRA_TRIKONA and _planet_in_own_or_exaltation("Moon", ms):
            _add_yoga(result, "Gouri Yoga", "Moon in own or exaltation sign in Kendra or Trikona (Jupiter strong).")

    # ----- 27: Saraswati (Mercury, Jupiter, Venus in Kendra/Trikona or in 2nd with Jupiter strong) -----
    me_jup_ven = ["Mercury", "Jupiter", "Venus"]
    in_kt = [p for p in me_jup_ven if p in planet_to_house and planet_to_house[p][0] in _KENDRA_TRIKONA]
    in_2 = [p for p in me_jup_ven if p in planet_to_house and planet_to_house[p][0] == 2]
    if len(in_kt) >= 3:
        _add_yoga(result, "Saraswati Yoga", "Mercury, Jupiter and Venus in Kendra or Trikona.")
    elif len(in_kt) >= 2 and "Jupiter" in planet_to_house:
        jh, js = planet_to_house["Jupiter"]
        if _planet_in_own_or_exaltation("Jupiter", js) and (2 in (planet_to_house.get(p, (None,))[0] for p in me_jup_ven if p in planet_to_house)):
            _add_yoga(result, "Saraswati Yoga", "Mercury, Jupiter, Venus in Kendra/Trikona or 2nd house, with Jupiter in own or exaltation sign.")

    # ----- 28–30: Srikanta, Srinatha, Varunchi (Virinchi) -----
    if house_lords.get(1) and "Sun" in planet_to_house and "Moon" in planet_to_house:
        lord1 = house_lords[1]
        l1h, l1s = planet_to_house.get(lord1, (None, None))
        sun_h, sun_s = planet_to_house["Sun"]
        moon_h, moon_s = planet_to_house["Moon"]
        if l1h and l1h in _KENDRA_TRIKONA and sun_h in _KENDRA_TRIKONA and moon_h in _KENDRA_TRIKONA:
            if _planet_in_own_or_exaltation(lord1, l1s) or _planet_in_own_or_exaltation("Sun", sun_s) or _planet_in_own_or_exaltation("Moon", moon_s):
                _add_yoga(result, "Srikanta Yoga", "Lagna lord, Sun and Moon in exaltation, own or friend's sign in Kendra or Trikona.")
    if 9 in house_lords and "Venus" in planet_to_house and "Mercury" in planet_to_house:
        lord9 = house_lords[9]
        vh, vs = planet_to_house["Venus"]
        mh, ms = planet_to_house["Mercury"]
        if vh in _KENDRA_TRIKONA and mh in _KENDRA_TRIKONA:
            if lord9 in planet_to_house:
                l9h, l9s = planet_to_house[lord9]
                if l9h in _KENDRA_TRIKONA and (_planet_in_own_or_exaltation("Venus", vs) or _planet_in_own_or_exaltation(lord9, l9s) or _planet_in_own_or_exaltation("Mercury", ms)):
                    _add_yoga(result, "Srinatha Yoga", "Venus, 9th lord and Mercury in exaltation or own sign in Kendra or Trikona.")
    if 5 in house_lords and "Jupiter" in planet_to_house and "Saturn" in planet_to_house:
        lord5 = house_lords[5]
        jh, js = planet_to_house["Jupiter"]
        sh, ss = planet_to_house["Saturn"]
        if jh in _KENDRA_TRIKONA and sh in _KENDRA_TRIKONA and lord5 in planet_to_house:
            l5h, l5s = planet_to_house[lord5]
            if l5h in _KENDRA_TRIKONA and (_planet_in_own_or_exaltation("Jupiter", js) or _planet_in_own_or_exaltation("Saturn", ss) or _planet_in_own_or_exaltation(lord5, l5s)):
                _add_yoga(result, "Varunchi (Virinchi) Yoga", "Jupiter, 5th lord and Saturn in exaltation or own sign in Kendra or Trikona.")

    # ----- 31–33: Parivartana (Maha, Dainya, Kahala) -----
    for (a, b), yoga_type, formation in [
        ((1, 2), "Maha", "Lords of houses 1 and 2 exchange places."),
        ((1, 4), "Maha", "Lords of houses 1 and 4 exchange places."),
        ((1, 5), "Maha", "Lords of houses 1 and 5 exchange places."),
        ((1, 7), "Maha", "Lords of houses 1 and 7 exchange places."),
        ((1, 9), "Maha", "Lords of houses 1 and 9 exchange places."),
        ((1, 10), "Maha", "Lords of houses 1 and 10 exchange places."),
        ((9, 10), "Maha", "Lords of houses 9 and 10 exchange places."),
        ((1, 3), "Kahala", "Lords of houses 1 and 3 exchange places."),
        ((6, 8), "Dainya", "Lords of houses 6 and 8 exchange places."),
        ((6, 12), "Dainya", "Lords of houses 6 and 12 exchange places."),
        ((8, 12), "Dainya", "Lords of houses 8 and 12 exchange places."),
    ]:
        if a not in house_lords or b not in house_lords:
            continue
        lord_a, lord_b = house_lords[a], house_lords[b]
        if lord_a not in planet_to_house or lord_b not in planet_to_house:
            continue
        if planet_to_house[lord_a][0] == b and planet_to_house[lord_b][0] == a:
            if yoga_type == "Maha":
                _add_yoga(result, "Parivartana (Maha) Yoga", formation)
            elif yoga_type == "Kahala":
                _add_yoga(result, "Kahala (Parivartana) Yoga", formation)
            else:
                _add_yoga(result, "Parivartana (Dainya) Yoga", formation)

    # ----- 34: Raja Yoga (9th-10th lord conjunction) -----
    if 9 in house_lords and 10 in house_lords:
        lord9, lord10 = house_lords[9], house_lords[10]
        if lord9 in planet_to_house and lord10 in planet_to_house:
            h9, h10 = planet_to_house[lord9][0], planet_to_house[lord10][0]
            if h9 == h10 and h9 in _KENDRA_TRIKONA:
                _add_yoga(result, "Raja Yoga (9th-10th lord)", "Lords of 9th and 10th in conjunction in a Kendra or Trikona house.")

    # ----- 35: Raja Yoga (Kendra lord in Trikona or Trikona lord in Kendra) -----
    kendra_lords = {house_lords[h] for h in _KENDRA if h in house_lords and house_lords[h]}
    trikona_lords = {house_lords[h] for h in _TRIKONA if h in house_lords and house_lords[h]}
    for planet, (h, _) in planet_to_house.items():
        if planet not in _TRADITIONAL_PLANETS:
            continue
        if (planet in kendra_lords and h in _TRIKONA) or (planet in trikona_lords and h in _KENDRA):
            _add_yoga(result, "Raja Yoga (Kendra-Trikona)", "A Kendra lord in a Trikona house, or a Trikona lord in a Kendra house.")
            break

    # ----- 36: Shankha (Kendra and Trikona lords together) -----
    for planet, (h, _) in planet_to_house.items():
        if planet in kendra_lords and planet in trikona_lords and h in _KENDRA_TRIKONA:
            _add_yoga(result, "Shankha Yoga", "Same planet as lord of a Kendra and of a Trikona, placed together in a Kendra or Trikona house.")
            break

    # ----- 37–43: Sankhya / planetary distribution (Veena, Dhanu, Harsha, etc.) -----
    seven_in = set()
    for p in _SEVEN_GRAHAS:
        if p in planet_to_house:
            seven_in.add(planet_to_house[p][0])
    n_signs = len(seven_in)
    if n_signs == 7:
        _add_yoga(result, "Veena (Vallaki) Yoga", "Seven planets in seven different signs.")
    elif n_signs == 6:
        _add_yoga(result, "Dhanu (Dharma) Yoga", "Seven planets in six signs.")
    elif n_signs == 5:
        _add_yoga(result, "Harsha Yoga", "Seven planets in five signs.")
    elif n_signs == 4:
        _add_yoga(result, "Kendra Sankhya Yoga", "Seven planets in four signs.")
    elif n_signs == 3:
        _add_yoga(result, "Shula Yoga", "Seven planets in three signs.")
    elif n_signs == 2:
        _add_yoga(result, "Yuga Yoga", "Seven planets in two signs; heretical, without wealth. (Inauspicious)")
    elif n_signs == 1:
        _add_yoga(result, "Gola Yoga", "All seven planets in one sign.")

    # ----- 44: Adhiyoga (Mercury, Jupiter, Venus in 6,7,8 from Lagna or Moon) -----
    for base in [1, moon_house]:
        if base is None:
            continue
        h6 = _house_offset_from(base, 6)
        h7 = _house_offset_from(base, 7)
        h8 = _house_offset_from(base, 8)
        occup = set()
        for h in (h6, h7, h8):
            for p, _ in house_to_planets.get(h, []):
                if p in ("Mercury", "Jupiter", "Venus"):
                    occup.add(p)
        if len(occup) >= 3:
            _add_yoga(result, "Adhiyoga", "Mercury, Jupiter and Venus occupy 6th, 7th and 8th houses from Lagna or Moon.")
            break

    # ----- 45–56: House-lord strength yogas (Chamar, Dhenu, Shaurya, Jaladhi, Chhatra, Astra, Kama, Asura, Bhagya, Khyati, Parijata, Musala 12th) -----
    def _house_lord_strong(house_num):
        if house_num not in house_lords:
            return False
        lord = house_lords[house_num]
        if lord not in planet_to_house:
            return False
        h, s = planet_to_house[lord]
        if h not in _KENDRA_TRIKONA:
            return False
        return _planet_in_own_or_exaltation(lord, s)

    house_yogas = [
        (1, "Chamara Yoga", "Lagna occupied or aspected by benefics and Lagna lord in own or exaltation sign in Kendra or Trikona."),
        (2, "Dhenu Yoga", "2nd house occupied or aspected by benefic and 2nd lord in own or exaltation sign in Kendra or Trikona."),
        (3, "Shaurya Yoga", "3rd house with benefic and 3rd lord in own or exaltation sign in Kendra or Trikona."),
        (4, "Jaladhi Yoga", "4th house similarly disposed and 4th lord in own or exaltation in Kendra or Trikona."),
        (5, "Chhatra Yoga", "5th house similarly disposed and 5th lord in own or exaltation in Kendra or Trikona."),
        (6, "Astra Yoga (6th)", "6th house occupied or aspected by benefic and 6th lord in own or exaltation in Kendra or Trikona."),
        (7, "Kama Yoga", "7th house similarly disposed and 7th lord in own or exaltation in Kendra or Trikona."),
        (8, "Asura Yoga", "8th house with benefic and 8th lord in own or exaltation in Kendra or Trikona."),
        (9, "Bhagya Yoga", "9th house similarly disposed and 9th lord in own or exaltation in Kendra or Trikona."),
        (10, "Khyati Yoga", "10th house similarly disposed and 10th lord in own or exaltation in Kendra or Trikona."),
        (11, "Parijata Yoga", "11th house similarly disposed and 11th lord in own or exaltation in Kendra or Trikona."),
        (12, "Musala (12th) Yoga", "12th house with benefic and 12th lord in own or exaltation in Kendra or Trikona."),
    ]
    for hnum, yname, ydesc in house_yogas:
        if _house_lord_strong(hnum):
            # Check benefic on house for 1,2,3,4,5, etc. (simplified: any benefic in that house or aspecting)
            occupants = house_to_planets.get(hnum, [])
            has_benefic = any(p in _BENEFICS for p, _ in occupants)
            if hnum in (1, 2, 3, 4, 5, 9, 10, 11) and (has_benefic or hnum == 1):
                _add_yoga(result, yname, ydesc)
            elif hnum in (6, 7, 8, 12):
                _add_yoga(result, yname, ydesc)

    # ----- 57–61: Vipareeta / Dusthana lord yogas (Harsha, Sarala, Vimala) -----
    if 6 in house_lords and 8 in house_lords and 12 in house_lords:
        L6, L8, L12 = house_lords[6], house_lords[8], house_lords[12]
        for lor in (L6, L8, L12):
            if lor not in planet_to_house:
                continue
            ih = planet_to_house[lor][0]
            if ih == 6:
                _add_yoga(result, "Harsha (Vipareeta) Yoga", "6th lord in 6th house (Vipareeta Raja).")
            if ih == 8:
                _add_yoga(result, "Sarala (Vipareeta) Yoga", "6th, 8th or 12th lord in 8th house (Vipareeta Raja).")
            if ih == 12:
                _add_yoga(result, "Vimala (Vipareeta) Yoga", "Lord of 6th, 8th or 12th in 12th house (Vipareeta Raja).")
            break

    # ----- 62: Neechabhanga Raja (planet in debilitation, lord of debilitation or exaltation lord in Kendra from Lagna/Moon) -----
    debilitation_sign = {"Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer", "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo", "Saturn": "Aries"}
    exalt_lord = {"Sun": "Mars", "Moon": "Venus", "Mars": "Moon", "Mercury": "Jupiter", "Jupiter": "Moon", "Venus": "Mercury", "Saturn": "Venus"}
    for planet, deb_sign in debilitation_sign.items():
        if planet not in planet_to_house:
            continue
        h, sign = planet_to_house[planet]
        if sign != deb_sign:
            continue
        deb_lord = _SIGN_LORD.get(deb_sign)
        if deb_lord and deb_lord in planet_to_house:
            dh = planet_to_house[deb_lord][0]
            kendra_from_moon = {_house_offset_from(moon_house, k) for k in (1, 4, 7, 10)} if moon_house else set()
            if dh in _KENDRA or dh in kendra_from_moon:
                _add_yoga(result, "Neechabhanga Raja Yoga", "Planet in debilitation and lord of debilitation sign in Kendra from Lagna or Moon.")
                break
        exc_l = exalt_lord.get(planet)
        if exc_l and exc_l in planet_to_house:
            eh = planet_to_house[exc_l][0]
            kendra_from_moon = {_house_offset_from(moon_house, k) for k in (1, 4, 7, 10)} if moon_house else set()
            if eh in _KENDRA or eh in kendra_from_moon:
                _add_yoga(result, "Neechabhanga Raja Yoga", "Planet in debilitation and exaltation lord of that planet in Kendra from Lagna or Moon.")
                break

    # ----- 63: Parvata (lord of sign where Lagna lord is, in exaltation/own in Kendra/Trikona) -----
    if 1 in house_lords:
        L1 = house_lords[1]
        if L1 in planet_to_house:
            h1, s1 = planet_to_house[L1]
            sign_lord = _SIGN_LORD.get(s1)
            if sign_lord and sign_lord in planet_to_house:
                sh, ss = planet_to_house[sign_lord]
                if sh in _KENDRA_TRIKONA and _planet_in_own_or_exaltation(sign_lord, ss):
                    _add_yoga(result, "Parvata Yoga", "Lord of the sign where Lagna lord is placed, itself in exaltation or own sign in Kendra or Trikona.")

    # ----- Nabhasa: Rajju, Musala, Nala (seven planets in movable/fixed/dual) -----
    signs_by_nature = {"movable": ["Aries", "Cancer", "Libra", "Capricorn"],
                       "fixed": ["Taurus", "Leo", "Scorpio", "Aquarius"],
                       "dual": ["Gemini", "Virgo", "Sagittarius", "Pisces"]}
    nature_of = {}
    for nat, signs in signs_by_nature.items():
        for s in signs:
            nature_of[s] = nat
    sign_natures = [nature_of.get(s, "") for p, (_, s) in planet_to_house.items() if p in _SEVEN_GRAHAS and s]
    if len(sign_natures) >= 5:
        if all(n == "movable" for n in sign_natures):
            _add_yoga(result, "Rajju Yoga", "All seven planets in movable signs.")
        elif all(n == "fixed" for n in sign_natures):
            _add_yoga(result, "Musala (Nabhasa) Yoga", "All seven planets in fixed signs.")
        elif all(n == "dual" for n in sign_natures):
            _add_yoga(result, "Nala Yoga", "All seven planets in dual signs.")

    return result


def detect_doshas(chart):
    """
    Detect Doshas (afflictions) present in the D1 chart.
    Returns list of dicts: [{ "name": "...", "description": "...", "severity": "low|moderate|high", "type": "dosha" }, ...]
    """
    result = []
    planet_to_house, house_to_planets, house_lords = _get_d1_planet_house_map(chart)
    if not planet_to_house:
        return result

    # ----- Mangal (Kuja) Dosha: Mars in 1, 2, 4, 7, 8, 12 -----
    mangal_houses = {1, 2, 4, 7, 8, 12}
    if "Mars" in planet_to_house:
        h, sign = planet_to_house["Mars"]
        if h in mangal_houses:
            entry = {
                "name": "Mangal Dosha (Kuja Dosha)",
                "description": f"Mars in house {h}.",
                "severity": "moderate" if h in (2, 12) else "high",
                "type": "dosha"
            }
            if "Mangal Dosha (Kuja Dosha)" in _DOSHA_EFFECTS:
                entry["effects"] = _DOSHA_EFFECTS["Mangal Dosha (Kuja Dosha)"]
            result.append(entry)

    # ----- Papa Kartari: malefics flanking a house (e.g. 6th and 8th around 7th) -----
    for target in [7, 1, 5]:  # 7th = marriage, 1st = self, 5th = progeny
        left = ((target - 1 - 1) % 12) + 1   # house before target (e.g. 6 for 7th)
        right = (target % 12) + 1             # house after target (e.g. 8 for 7th)
        left_planets = {p for p, _ in house_to_planets.get(left, [])}
        right_planets = {p for p, _ in house_to_planets.get(right, [])}
        mal_left = left_planets & _MALEFICS
        mal_right = right_planets & _MALEFICS
        if mal_left and mal_right:
            entry = {
                "name": "Papa Kartari Dosha",
                "description": f"Malefics in houses on both sides of house {target} (e.g. 6th and 8th around 7th).",
                "severity": "moderate",
                "type": "dosha"
            }
            if "Papa Kartari Dosha" in _DOSHA_EFFECTS:
                entry["effects"] = _DOSHA_EFFECTS["Papa Kartari Dosha"]
            result.append(entry)
            break

    # ----- Kemadruma as dosha (affliction angle; same condition as Kemadruma Yoga) -----
    moon_house = _moon_house(chart)
    if moon_house is not None:
        h2 = _house_from_moon(moon_house, 2)
        h12 = _house_from_moon(moon_house, 12)
        if len(house_to_planets.get(h2, [])) == 0 and len(house_to_planets.get(h12, [])) == 0:
            # Add once as dosha (affliction); yoga list already has Kemadruma Yoga
            if not any(d.get("name") == "Kemadruma Dosha" for d in result):
                entry = {
                    "name": "Kemadruma Dosha",
                    "description": "Moon without any planet in 2nd and 12th houses from it.",
                    "severity": "moderate",
                    "type": "dosha"
                }
                if "Kemadruma Dosha" in _DOSHA_EFFECTS:
                    entry["effects"] = _DOSHA_EFFECTS["Kemadruma Dosha"]
                result.append(entry)

    return result


def analyze_yoga_dosha(chart):
    """
    Analyze D1 chart for Yogas and Doshas. Returns a single dict for sections.
    
    Args:
        chart: VedicBirthChart object
    
    Returns:
        dict: { "yogas": [...], "doshas": [...], "summary": "...", "chart": "d1" }.
        Each yoga/dosha may include "effects" (detailed results from classical sources) when available.
    """
    yogas = detect_yogas(chart)
    doshas = detect_doshas(chart)

    # Remove duplicate Kemadruma if added both as yoga and dosha (keep in yogas and in doshas for different angle)
    summary_parts = []
    if yogas:
        summary_parts.append(f"{len(yogas)} yoga(s) present")
    if doshas:
        summary_parts.append(f"{len(doshas)} dosha(s) present")
    summary = "; ".join(summary_parts) if summary_parts else "No significant yogas or doshas detected."

    return {
        "chart": "d1",
        "yogas": yogas,
        "doshas": doshas,
        "summary": summary,
    }
