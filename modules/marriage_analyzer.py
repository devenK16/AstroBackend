"""
Marriage Analyzer Module
Analyzes D9 (Navamsa) chart for marriage and relationship insights
"""

from .analysis_engine import analyze_chart_section


def analyze_marriage(chart):
    """
    Analyze marriage section using D9 chart.
    
    Args:
        chart: VedicBirthChart object
    
    Returns:
        dict: Marriage analysis with insights, strengths, concerns, and prediction
    """
    return analyze_chart_section(chart, "d9", "marriage")
