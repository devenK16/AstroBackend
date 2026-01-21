"""
Health Analyzer Module
Analyzes D16 (Shodasamsa) chart for health and wellness insights
"""

from .analysis_engine import analyze_chart_section


def analyze_health(chart):
    """
    Analyze health section using D16 chart.
    
    Args:
        chart: VedicBirthChart object
    
    Returns:
        dict: Health analysis with insights, strengths, concerns, and prediction
    """
    return analyze_chart_section(chart, "d16", "health")
