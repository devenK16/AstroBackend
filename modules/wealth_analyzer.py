"""
Wealth Analyzer Module
Analyzes D2 (Hora) chart for wealth and finance insights
"""

from .analysis_engine import analyze_chart_section


def analyze_wealth(chart):
    """
    Analyze wealth section using D2 chart.
    
    Args:
        chart: VedicBirthChart object
    
    Returns:
        dict: Wealth analysis with insights, strengths, concerns, and prediction
    """
    return analyze_chart_section(chart, "d2", "wealth")
