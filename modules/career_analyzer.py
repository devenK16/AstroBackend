"""
Career Analyzer Module
Analyzes D10 (Dasamsa) chart for career insights
"""

from .analysis_engine import analyze_chart_section


def analyze_career(chart):
    """
    Analyze career section using D10 chart.
    
    Args:
        chart: VedicBirthChart object
    
    Returns:
        dict: Career analysis with insights, strengths, concerns, and prediction
    """
    return analyze_chart_section(chart, "d10", "career")
