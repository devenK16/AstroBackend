"""
Dasha Module - Extract Vimshottari Dasha data from jyotishganit chart.
Exposes mahadashas, antardashas, pratyantardashas, current/upcoming periods, and balance.
"""

from datetime import datetime, date


def _serialize_value(v):
    """Convert datetime/date to ISO string; leave other types as-is."""
    if isinstance(v, (datetime, date)):
        return v.isoformat()
    if isinstance(v, dict):
        return {k: _serialize_value(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_serialize_value(x) for x in v]
    return v


def get_dasha_data(chart):
    """
    Extract Vimshottari Dasha data from a jyotishganit VedicBirthChart.
    
    Returns a dict suitable for JSON response with:
      - balance: balance of first mahadasha at birth (years), per planet
      - all: full list of mahadashas, each with start, end, antardashas (and pratyantardashas)
      - current: currently running mahadasha(s) and antardasha(s)
      - upcoming: next mahadasha(s) / antardasha(s)
      - summary: current_mahadasha, current_antardasha, current_pratyantardasha (if easily derivable)
    
    Returns None if chart has no dashas or on error.
    """
    if chart is None or not hasattr(chart, 'dashas'):
        return None
    try:
        dashas = chart.dashas
        raw = dashas.to_dict()
    except Exception:
        return None
    
    # Remove @type if present; ensure all datetimes are strings for JSON
    out = {}
    for key in ('balance', 'all', 'current', 'upcoming'):
        if key in raw:
            out[key] = _serialize_value(raw[key])
    
    # Add a flat summary for frontend convenience: current running period names
    summary = _build_summary(raw)
    if summary:
        out['summary'] = summary
    
    return out


def _build_summary(raw):
    """Build summary with current mahadasha, antardasha, pratyantardasha names and date ranges."""
    summary = {}
    current = raw.get('current') or {}
    maha = current.get('mahadashas') or {}
    # Usually one current mahadasha
    for maha_name, maha_data in maha.items():
        if not isinstance(maha_data, dict):
            continue
        summary['current_mahadasha'] = maha_name
        summary['current_mahadasha_start'] = _serialize_value(maha_data.get('start'))
        summary['current_mahadasha_end'] = _serialize_value(maha_data.get('end'))
        antardashas = maha_data.get('antardashas') or {}
        for ant_name, ant_data in antardashas.items():
            if not isinstance(ant_data, dict):
                continue
            summary['current_antardasha'] = ant_name
            summary['current_antardasha_start'] = _serialize_value(ant_data.get('start'))
            summary['current_antardasha_end'] = _serialize_value(ant_data.get('end'))
            pratyantar = ant_data.get('pratyantardashas') or {}
            for prat_name, prat_data in pratyantar.items():
                if not isinstance(prat_data, dict):
                    continue
                summary['current_pratyantardasha'] = prat_name
                summary['current_pratyantardasha_start'] = _serialize_value(prat_data.get('start'))
                summary['current_pratyantardasha_end'] = _serialize_value(prat_data.get('end'))
                break
        break
    
    balance = raw.get('balance') or {}
    if balance:
        summary['balance_at_birth_years'] = balance
        # First planet in balance is the first mahadasha lord
        first_planet = next(iter(balance.keys()), None)
        if first_planet:
            summary['first_mahadasha_lord'] = first_planet
            summary['first_mahadasha_balance_years'] = balance.get(first_planet)
    
    return summary
