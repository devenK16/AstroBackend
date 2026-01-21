"""
Comprehensive Exploration Script for jyotishganit Library
This script tests and demonstrates ALL features available in the library
"""

import json
from datetime import datetime
from jyotishganit import calculate_birth_chart, get_birth_chart_json, Person

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def explore_birth_chart_basic():
    """Test basic birth chart creation and properties"""
    print_section("1. BASIC BIRTH CHART CREATION")
    
    # Sample birth data - You can modify this
    name = "Test Person"
    birth_datetime = datetime(1990, 1, 15, 10, 30)  # Jan 15, 1990, 10:30 AM
    latitude = 28.6139   # Delhi, India
    longitude = 77.2090
    timezone_offset = 5.5  # IST (UTC+5:30) - MUST BE NUMERIC
    
    print(f"Creating birth chart for:")
    print(f"  Name: {name}")
    print(f"  DOB: {birth_datetime}")
    print(f"  Location: Lat {latitude}, Lon {longitude}")
    print(f"  Timezone: UTC+{timezone_offset}\n")
    
    try:
        # Use the helper function to calculate birth chart
        chart = calculate_birth_chart(
            birth_date=birth_datetime,
            latitude=latitude,
            longitude=longitude,
            timezone_offset=timezone_offset,
            name=name
        )
        
        print("✓ Birth chart created successfully!")
        print(f"\nChart object type: {type(chart)}")
        print(f"Chart class name: {chart.__class__.__name__}")
        
        # Get all public attributes
        public_attrs = [attr for attr in dir(chart) if not attr.startswith('_')]
        print(f"\nAvailable attributes ({len(public_attrs)} total):")
        for attr in public_attrs:
            print(f"  - {attr}")
        
        return chart
    except Exception as e:
        print(f"✗ Error creating birth chart: {e}")
        import traceback
        traceback.print_exc()
        return None

def explore_chart_attributes(chart):
    """Explore all attributes of the chart object"""
    print_section("2. CHART ATTRIBUTES & DATA")
    
    if not chart:
        print("No chart available")
        return
    
    try:
        # List of common attributes to check
        attrs_to_check = [
            'person', 'd1_chart', 'divisional_charts', 'ayanamsa',
            'ashtakavarga', 'dashas'
        ]
        
        for attr_name in attrs_to_check:
            if hasattr(chart, attr_name):
                print(f"✓ Found attribute: {attr_name}")
                attr = getattr(chart, attr_name)
                print(f"  Type: {type(attr).__name__}")
                
                # Try to show some details
                if hasattr(attr, '__dict__'):
                    sub_attrs = [a for a in dir(attr) if not a.startswith('_')]
                    if sub_attrs:
                        print(f"  Sub-attributes: {', '.join(sub_attrs[:10])}")
                        if len(sub_attrs) > 10:
                            print(f"  ... and {len(sub_attrs) - 10} more")
                print()
                
    except Exception as e:
        print(f"✗ Error exploring chart attributes: {e}")
        import traceback
        traceback.print_exc()

def explore_person_object(chart):
    """Explore the Person object within the chart"""
    print_section("3. PERSON OBJECT")
    
    if not chart or not hasattr(chart, 'person'):
        print("No person object available")
        return
    
    try:
        person = chart.person
        print(f"Person object type: {type(person).__name__}")
        
        # Get all public attributes
        public_attrs = [attr for attr in dir(person) if not attr.startswith('_')]
        print(f"\nPerson attributes ({len(public_attrs)} total):")
        
        for attr_name in public_attrs:
            try:
                attr = getattr(person, attr_name)
                if not callable(attr):
                    print(f"  {attr_name}: {attr}")
            except Exception as e:
                print(f"  {attr_name}: <Error: {e}>")
                
    except Exception as e:
        print(f"✗ Error exploring person object: {e}")

def explore_d1_chart(chart):
    """Explore the D1 (Rasi) chart"""
    print_section("4. D1 CHART (RASI/BIRTH CHART)")
    
    if not chart or not hasattr(chart, 'd1_chart'):
        print("No D1 chart available")
        return
    
    try:
        d1 = chart.d1_chart
        print(f"D1 Chart type: {type(d1).__name__}")
        
        # Get all public attributes
        public_attrs = [attr for attr in dir(d1) if not attr.startswith('_')]
        print(f"\nD1 Chart attributes ({len(public_attrs)} total):")
        
        for attr_name in public_attrs:
            try:
                attr = getattr(d1, attr_name)
                if callable(attr):
                    print(f"  METHOD: {attr_name}()")
                else:
                    attr_str = str(attr)
                    if len(attr_str) > 100:
                        print(f"  {attr_name}: {attr_str[:100]}...")
                    else:
                        print(f"  {attr_name}: {attr_str}")
            except Exception as e:
                print(f"  {attr_name}: <Error: {e}>")
                
    except Exception as e:
        print(f"✗ Error exploring D1 chart: {e}")

def explore_divisional_charts(chart):
    """Explore divisional charts (D1-D60)"""
    print_section("5. DIVISIONAL CHARTS (VARGAS)")
    
    if not chart or not hasattr(chart, 'divisional_charts'):
        print("No divisional charts available")
        return
    
    try:
        div_charts = chart.divisional_charts
        print(f"Divisional Charts type: {type(div_charts).__name__}")
        
        # Get all public attributes
        public_attrs = [attr for attr in dir(div_charts) if not attr.startswith('_')]
        print(f"\nDivisional Charts attributes ({len(public_attrs)} total):")
        
        # Common divisional charts
        common_charts = ['d1', 'd2', 'd3', 'd4', 'd7', 'd9', 'd10', 'd12', 
                        'd16', 'd20', 'd24', 'd27', 'd30', 'd40', 'd45', 'd60']
        
        print("\nChecking for common divisional charts:")
        for chart_name in common_charts:
            if hasattr(div_charts, chart_name):
                chart_obj = getattr(div_charts, chart_name)
                print(f"  ✓ {chart_name.upper()}: {type(chart_obj).__name__}")
            else:
                print(f"  ✗ {chart_name.upper()}: Not found")
                
    except Exception as e:
        print(f"✗ Error exploring divisional charts: {e}")

def explore_ashtakavarga(chart):
    """Explore Ashtakavarga calculations"""
    print_section("6. ASHTAKAVARGA")
    
    if not chart or not hasattr(chart, 'ashtakavarga'):
        print("No ashtakavarga available")
        return
    
    try:
        ashtakavarga = chart.ashtakavarga
        print(f"Ashtakavarga type: {type(ashtakavarga).__name__}")
        
        # Get all public attributes
        public_attrs = [attr for attr in dir(ashtakavarga) if not attr.startswith('_')]
        print(f"\nAshtakavarga attributes ({len(public_attrs)} total):")
        
        for attr_name in public_attrs[:20]:  # Show first 20
            try:
                attr = getattr(ashtakavarga, attr_name)
                if callable(attr):
                    print(f"  METHOD: {attr_name}()")
                else:
                    print(f"  {attr_name}: {type(attr).__name__}")
            except Exception as e:
                print(f"  {attr_name}: <Error: {e}>")
                
    except Exception as e:
        print(f"✗ Error exploring ashtakavarga: {e}")

def explore_dashas(chart):
    """Explore Vimshottari Dasha system"""
    print_section("7. DASHAS (VIMSHOTTARI DASHA SYSTEM)")
    
    if not chart or not hasattr(chart, 'dashas'):
        print("No dashas available")
        return
    
    try:
        dashas = chart.dashas
        print(f"Dashas type: {type(dashas).__name__}")
        
        # Get all public attributes
        public_attrs = [attr for attr in dir(dashas) if not attr.startswith('_')]
        print(f"\nDashas attributes ({len(public_attrs)} total):")
        
        for attr_name in public_attrs:
            try:
                attr = getattr(dashas, attr_name)
                if callable(attr):
                    print(f"  METHOD: {attr_name}()")
                else:
                    attr_str = str(attr)
                    if len(attr_str) > 150:
                        print(f"  {attr_name}: {attr_str[:150]}...")
                    else:
                        print(f"  {attr_name}: {attr_str}")
            except Exception as e:
                print(f"  {attr_name}: <Error: {e}>")
                
    except Exception as e:
        print(f"✗ Error exploring dashas: {e}")

def explore_json_output(chart):
    """Explore JSON output capability"""
    print_section("8. JSON OUTPUT")
    
    if not chart:
        print("No chart available")
        return
    
    try:
        print("Testing get_birth_chart_json function...")
        
        # Use the helper function
        json_output = get_birth_chart_json(
            birth_date=datetime(1990, 1, 15, 10, 30),
            latitude=28.6139,
            longitude=77.2090,
            timezone_offset=5.5,
            name="Test Person"
        )
        
        print(f"✓ JSON output generated!")
        print(f"  Type: {type(json_output)}")
        print(f"  Length: {len(json_output)} characters")
        
        # Try to parse it
        try:
            parsed = json.loads(json_output)
            print(f"\n✓ Valid JSON!")
            print(f"  Top-level keys: {list(parsed.keys())}")
            
            # Show a preview
            print(f"\nJSON Preview (first 500 characters):")
            print(json_output[:500] + "...")
            
            # Save to file
            with open('sample_birth_chart.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(parsed, indent=2))
            print(f"\n✓ Full JSON saved to: sample_birth_chart.json")
            
        except json.JSONDecodeError as e:
            print(f"✗ Invalid JSON: {e}")
            
    except Exception as e:
        print(f"✗ Error exploring JSON output: {e}")
        import traceback
        traceback.print_exc()

def explore_all_methods(obj, obj_name="Object"):
    """List and try all available methods on an object"""
    print_section(f"9. ALL METHODS & ATTRIBUTES - {obj_name}")
    
    if not obj:
        print(f"No {obj_name} available")
        return
    
    try:
        print(f"Exploring all public methods and attributes of {obj_name}:\n")
        
        # Get all attributes that don't start with underscore
        public_attrs = [attr for attr in dir(obj) if not attr.startswith('_')]
        
        print(f"Total public attributes/methods: {len(public_attrs)}\n")
        
        methods = []
        attributes = []
        
        for attr_name in public_attrs:
            try:
                attr = getattr(obj, attr_name)
                if callable(attr):
                    methods.append(attr_name)
                else:
                    attributes.append((attr_name, attr))
            except Exception as e:
                print(f"  Error accessing {attr_name}: {e}")
        
        print(f"METHODS ({len(methods)} total):")
        for method_name in methods:
            print(f"  - {method_name}()")
        
        print(f"\nATTRIBUTES ({len(attributes)} total):")
        for attr_name, attr_value in attributes[:30]:  # Show first 30
            try:
                value_str = str(attr_value)
                if len(value_str) > 80:
                    print(f"  - {attr_name}: {value_str[:80]}...")
                else:
                    print(f"  - {attr_name}: {value_str}")
            except:
                print(f"  - {attr_name}: <{type(attr_value).__name__}>")
        
        if len(attributes) > 30:
            print(f"  ... and {len(attributes) - 30} more attributes")
                    
    except Exception as e:
        print(f"✗ Error exploring all methods: {e}")

def main():
    """Main exploration function"""
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  JYOTISHGANIT LIBRARY - COMPREHENSIVE EXPLORATION".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    # Create birth chart
    chart = explore_birth_chart_basic()
    
    if chart:
        # Explore all features
        explore_chart_attributes(chart)
        explore_person_object(chart)
        explore_d1_chart(chart)
        explore_divisional_charts(chart)
        explore_ashtakavarga(chart)
        explore_dashas(chart)
        explore_json_output(chart)
        explore_all_methods(chart, "VedicBirthChart")
        
        print_section("EXPLORATION COMPLETE")
        print("✓ All features have been tested!")
        print("\nGenerated files:")
        print("  - sample_birth_chart.json (Complete birth chart in JSON format)")
        print("\nNext steps:")
        print("  1. Review the output above to see what features are available")
        print("  2. Check sample_birth_chart.json for the complete data structure")
        print("  3. Test the API server with: python api_server.py")
        print("  4. Read TESTING_GUIDE.md for step-by-step testing instructions")
    else:
        print("\n✗ Could not create birth chart. Please check the library installation.")
        print("  Try: pip install jyotishganit")

if __name__ == "__main__":
    main()
