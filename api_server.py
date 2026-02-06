"""
Flask REST API Server for Astrology Calculations using jyotishganit
This provides endpoints for your frontend to get birth chart data
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from jyotishganit import calculate_birth_chart, get_birth_chart_json
import traceback
import json
import os

# Import our analysis modules
from modules.compatibility import calculate_compatibility_details
from modules.kundali_summary import get_kundali_summary
from modules.career_analyzer import analyze_career
from modules.wealth_analyzer import analyze_wealth
from modules.health_analyzer import analyze_health
from modules.marriage_analyzer import analyze_marriage
from modules.numerology import get_numerology
from modules.dasha import get_dasha_data
from modules.yoga_dosha_analyzer import analyze_yoga_dosha
from modules.personality_insights import get_personality_insights
from modules import db as orders_db
from modules.orders_services import (
    get_amount_and_title,
    validate_create_payload,
    create_razorpay_order,
    verify_payment_signature,
    order_payload_to_record,
    send_admin_email_for_order,
)
from modules.admin_auth import hash_password, check_password, issue_jwt, verify_jwt, get_bearer_token, admin_required

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# --- Orders & admin: init DB and seed admin on first use ---
orders_db.init_db()
orders_db.seed_admin_if_empty(hash_password)

def parse_datetime(date_str, time_str):
    """Parse date and time strings into datetime object"""
    try:
        # Expected format: "YYYY-MM-DD" and "HH:MM"
        datetime_str = f"{date_str} {time_str}"
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    except Exception as e:
        raise ValueError(f"Invalid date/time format: {e}")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Jyotishganit Astrology API",
        "version": "1.0.0"
    })

@app.route('/api/birth-chart', methods=['POST'])
def get_birth_chart():
    """
    Generate complete birth chart from user details
    
    Expected JSON body:
    {
        "name": "John Doe",
        "date": "1990-01-15",
        "time": "10:30",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": 5.5
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'date', 'time', 'latitude', 'longitude', 'timezone']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400
        
        # Parse datetime
        date_of_birth = parse_datetime(data['date'], data['time'])
        
        # 1. Calculate
        chart = calculate_birth_chart(
            birth_date=date_of_birth,
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            timezone_offset=float(data['timezone']),
            name=data['name']
        )
        
        # 2. Serialize chart data
        json_data = get_birth_chart_json(chart)
        
        # Handle if it returns dict or string
        if isinstance(json_data, str):
            chart_result = json.loads(json_data)
        else:
            chart_result = json_data

        # 3. Calculate compatibility details (use chart_result so we read same Moon data as in response)
        try:
            compatibility = calculate_compatibility_details(chart, data['name'], chart_result=chart_result)
        except Exception as e:
            compatibility = {"error": str(e)}

        # 4. Extract Panchanga data
        panchanga_data = {}
        if 'panchanga' in chart_result:
            panchanga = chart_result['panchanga']
            panchanga_data = {
                "tithi": panchanga.get('tithi') if isinstance(panchanga, dict) else None,
                "nakshatra": panchanga.get('nakshatra') if isinstance(panchanga, dict) else None,
                "nakshatra_pada": None,  # Will extract from Moon if available
                "yoga": panchanga.get('yoga') if isinstance(panchanga, dict) else None,
                "karana": panchanga.get('karana') if isinstance(panchanga, dict) else None,
                "vaara": panchanga.get('vaara') if isinstance(panchanga, dict) else None
            }
        
        # Extract Nakshatra Pada from Moon
        try:
            for planet in chart.d1_chart.planets:
                if planet.celestial_body == "Moon":
                    panchanga_data["nakshatra_pada"] = planet.pada if hasattr(planet, 'pada') else None
                    break
        except:
            pass

        # 5. Extract chart data (D1, D2, D9, D10, D16)
        charts_data = {
            "d1": chart_result.get('d1Chart', {}),
            "d2": chart_result.get('divisionalCharts', {}).get('d2', {}),
            "d9": chart_result.get('divisionalCharts', {}).get('d9', {}),
            "d10": chart_result.get('divisionalCharts', {}).get('d10', {}),
            "d16": chart_result.get('divisionalCharts', {}).get('d16', {})
        }

        # 6. Analyze sections (career, wealth, health, marriage, yoga_dosha, numerology, dasha)
        sections = {}
        try:
            sections["career"] = analyze_career(chart) or {}
            sections["wealth"] = analyze_wealth(chart) or {}
            sections["health"] = analyze_health(chart) or {}
            sections["marriage"] = analyze_marriage(chart) or {}
        except Exception as e:
            sections = {"error": f"Analysis error: {str(e)}"}

        try:
            sections["yoga_dosha"] = analyze_yoga_dosha(chart)
        except Exception as e:
            sections["yoga_dosha"] = {"error": str(e), "yogas": [], "doshas": [], "summary": "Yoga/Dosha analysis unavailable."}

        try:
            sections["personality_insights"] = get_personality_insights(
                chart,
                panchanga=panchanga_data,
                yoga_dosha_result=sections.get("yoga_dosha")
            )
        except Exception as e:
            sections["personality_insights"] = {"error": str(e)}

        try:
            sections["numerology"] = get_numerology(data['name'], data['date'])
        except Exception as e:
            sections["numerology"] = {"error": str(e)}

        try:
            dasha = get_dasha_data(chart)
            sections["dasha"] = dasha if dasha is not None else {"error": "Dasha data not available"}
        except Exception as e:
            sections["dasha"] = {"error": str(e)}

        # Kundali summary: Manglik, Sade Sati, current Dasha (for display above charts)
        try:
            kundali_summary = get_kundali_summary(
                chart,
                yoga_dosha_result=sections.get("yoga_dosha"),
                dasha_data=sections.get("dasha"),
                latitude=float(data.get("latitude")),
                longitude=float(data.get("longitude")),
                timezone_offset=float(data.get("timezone", 5.5))
            )
        except Exception as e:
            kundali_summary = {"manglik_status": "Unknown", "sade_sati_status": "Unknown", "current_dasha": None, "error": str(e)}

        # 7. Build complete response: numerology and dasha ONLY inside sections (never at top level)
        result = {
            "success": True,
            "basic_details": {
                "name": data['name'],
                "dob": data['date'],
                "time": data['time'],
                "place": data.get('place', ''),  # Optional
                "latitude": data['latitude'],
                "longitude": data['longitude'],
                "timezone": data['timezone']
            },
            "charts": charts_data,
            "compatibility": compatibility,
            "panchanga": panchanga_data,
            "kundali_summary": kundali_summary,
            "sections": sections,
            "input": {
                'name': data['name'],
                'date': data['date'],
                'time': data['time'],
                'latitude': data['latitude'],
                'longitude': data['longitude'],
                'timezone': data['timezone']
            }
        }
        # Ensure no top-level dasha/numerology (they must only appear under sections)
        result.pop("dasha", None)
        result.pop("numerology", None)

        return jsonify(result)
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/panchanga', methods=['POST'])
def get_panchanga():
    """
    Get Panchanga details for a specific date/time/location
    
    Expected JSON body:
    {
        "date": "1990-01-15",
        "time": "10:30",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": 5.5
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['date', 'time', 'latitude', 'longitude', 'timezone']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400
        
        # Parse datetime
        date_of_birth = parse_datetime(data['date'], data['time'])
        
        # Parse datetime
        date_of_birth = parse_datetime(data['date'], data['time'])
        
        # 1. Calculate
        chart = calculate_birth_chart(
            birth_date=date_of_birth,
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            timezone_offset=float(data['timezone']),
            name="Panchanga Query"
        )
        
        # 2. Serialize
        json_data = get_birth_chart_json(chart)
        
        if isinstance(json_data, str):
            full_data = json.loads(json_data)
        else:
            full_data = json_data

        result = {"success": True}
        
        # Extract panchanga-related fields if they exist
        panchanga_fields = ['tithi', 'nakshatra', 'yoga', 'karana', 'vaara', 'panchanga']
        for field in panchanga_fields:
            if field in full_data:
                result[field] = full_data[field]
        
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/dasha', methods=['POST'])
def get_dasha():
    """
    Get Vimshottari Dasha periods (Mahadasha, Antardasha, Pratyantardasha).
    
    Expected JSON body:
    {
        "name": "John Doe",
        "date": "1990-01-15",
        "time": "10:30",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": 5.5
    }
    
    Returns:
      - success, basic_details, input
      - dasha: { balance, all, current, upcoming, summary }
        - balance: first mahadasha balance at birth (years per planet)
        - all: full mahadashas with antardashas and pratyantardashas (start/end dates)
        - current: currently running mahadasha/antardasha/pratyantardasha
        - upcoming: next periods
        - summary: current_mahadasha, current_antardasha, current_pratyantardasha, dates, balance_at_birth_years
    """
    try:
        data = request.get_json()
        
        required_fields = ['name', 'date', 'time', 'latitude', 'longitude', 'timezone']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400
        
        date_of_birth = parse_datetime(data['date'], data['time'])
        
        chart = calculate_birth_chart(
            birth_date=date_of_birth,
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            timezone_offset=float(data['timezone']),
            name=data['name']
        )

        dasha = get_dasha_data(chart)
        if dasha is None:
            dasha = {"error": "Dasha data not available"}

        result = {
            "success": True,
            "basic_details": {
                "name": data['name'],
                "dob": data['date'],
                "time": data['time'],
                "place": data.get('place', ''),
                "latitude": data['latitude'],
                "longitude": data['longitude'],
                "timezone": data['timezone']
            },
            "dasha": dasha,
            "input": {
                "name": data['name'],
                "date": data['date'],
                "time": data['time'],
                "latitude": data['latitude'],
                "longitude": data['longitude'],
                "timezone": data['timezone']
            }
        }
        
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


# ---------- Orders & payments (Razorpay test mode) ----------

@app.route('/api/orders/create', methods=['POST'])
def orders_create():
    """Create Razorpay order; return order_id, key_id, amount_paise. Do not save to DB yet."""
    try:
        data = request.get_json() or {}
        ok, err = validate_create_payload(data)
        if not ok:
            return jsonify({"error": err}), 400
        service_id = data["service_id"]
        plan_id = data.get("plan_id") or None
        if service_id == "ask-astrologer" and plan_id not in ("one", "three"):
            return jsonify({"error": "plan_id must be 'one' or 'three' for ask-astrologer"}), 400
        result = get_amount_and_title(service_id, plan_id)
        if not result:
            return jsonify({"error": "Unknown service_id or plan_id"}), 400
        amount_paise, _ = result
        resp = create_razorpay_order(amount_paise)
        orders_db.save_pending_payload(resp["razorpay_order_id"], data)
        return jsonify(resp)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/orders/verify', methods=['POST'])
def orders_verify():
    """Verify Razorpay signature, save order, send admin email."""
    try:
        data = request.get_json() or {}
        rp_id = data.get("razorpay_payment_id")
        ro_id = data.get("razorpay_order_id")
        sig = data.get("razorpay_signature")
        payload = data.get("order_payload")
        if not all([rp_id, ro_id, sig, payload]):
            return jsonify({"error": "razorpay_payment_id, razorpay_order_id, razorpay_signature, order_payload required"}), 400
        if not verify_payment_signature(ro_id, rp_id, sig):
            return jsonify({"error": "Invalid signature"}), 400
        if orders_db.order_exists_by_payment_id(rp_id):
            return jsonify({"success": True, "order_id": ro_id}), 200
        record = order_payload_to_record(payload, ro_id, rp_id)
        orders_db.save_order(record)
        send_admin_email_for_order(record)
        orders_db.delete_pending_payload(ro_id)
        return jsonify({"success": True, "order_id": ro_id})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/webhooks/razorpay', methods=['POST'])
def webhooks_razorpay():
    """Razorpay payment.captured: create order and email admin if not already done."""
    try:
        raw = request.get_data()
        sig = request.headers.get("X-Razorpay-Signature", "")
        secret = os.environ.get("RAZORPAY_WEBHOOK_SECRET", "")
        if secret:
            import hmac
            import hashlib
            expected = hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(expected, sig):
                return jsonify({"error": "Invalid webhook signature"}), 400
        body = request.get_json() or {}
        if body.get("event") != "payment.captured":
            return jsonify({"ok": True}), 200
        payment = (body.get("payload") or {}).get("payment") or {}
        payment = payment.get("entity", payment) if isinstance(payment, dict) else {}
        rp_id = payment.get("id")
        ro_id = payment.get("order_id")
        if not rp_id or not ro_id:
            return jsonify({"ok": True}), 200
        if orders_db.order_exists_by_payment_id(rp_id):
            return jsonify({"ok": True}), 200
        payload = orders_db.get_pending_payload(ro_id)
        if not payload:
            return jsonify({"ok": True}), 200
        record = order_payload_to_record(payload, ro_id, rp_id)
        orders_db.save_order(record)
        send_admin_email_for_order(record)
        orders_db.delete_pending_payload(ro_id)
        return jsonify({"ok": True}), 200
    except Exception:
        return jsonify({"error": "Webhook processing failed"}), 500


# ---------- Admin (JWT required) ----------

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    if not username:
        return jsonify({"error": "username required"}), 401
    user = orders_db.get_admin_by_username(username)
    if not user or not check_password(password, user["password_hash"]):
        return jsonify({"error": "Invalid credentials"}), 401
    token = issue_jwt(username)
    return jsonify({"token": token if isinstance(token, str) else token.decode("utf-8")})


@app.route('/api/admin/orders', methods=['GET'])
@admin_required
def admin_orders_list():
    status = request.args.get("status")
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    limit = min(int(request.args.get("limit", 50) or 50), 100)
    offset = int(request.args.get("offset", 0) or 0)
    rows = orders_db.list_orders(status=status, from_date=from_date, to_date=to_date, limit=limit, offset=offset)
    return jsonify(rows)


@app.route('/api/admin/orders/<int:order_id>', methods=['GET'])
@admin_required
def admin_order_detail(order_id):
    order = orders_db.get_order_by_id(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(dict(order))


@app.route('/api/admin/orders/<int:order_id>', methods=['PATCH'])
@admin_required
def admin_order_patch(order_id):
    data = request.get_json() or {}
    if data.get("status") != "completed":
        return jsonify({"error": "Only status: completed is supported"}), 400
    updated = orders_db.update_order_status(order_id, "completed")
    if not updated:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(dict(updated))


@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def admin_stats():
    return jsonify(orders_db.get_orders_stats())


if __name__ == '__main__':
    # Get port from environment variable (for production) or use 5000 (for local)
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    print("\n" + "="*60)
    print("  JYOTISHGANIT ASTROLOGY API SERVER")
    print("="*60)
    print(f"\nServer starting on http://0.0.0.0:{port}")
    print("\nAvailable endpoints:")
    print("  GET  /api/health           - Health check")
    print("  POST /api/birth-chart      - Get complete birth chart with all analyses")
    print("  POST /api/panchanga        - Get Panchanga details")
    print("  POST /api/dasha            - Get Dasha periods")
    print("  POST /api/orders/create    - Create Razorpay order (test mode)")
    print("  POST /api/orders/verify    - Verify payment & save order")
    print("  POST /api/webhooks/razorpay - Razorpay webhook")
    print("  POST /api/admin/login      - Admin login (JWT)")
    print("  GET  /api/admin/orders     - List orders (auth)")
    print("  GET  /api/admin/orders/<id> - Order detail (auth)")
    print("  PATCH /api/admin/orders/<id> - Mark completed (auth)")
    print("  GET  /api/admin/stats      - Stats (auth)")
    print("\n✨ /api/birth-chart includes:")
    print("  - Compatibility parameters (Varna, Vashya, Yoni, etc.)")
    print("  - Career, Wealth, Health, Marriage analyses (D10, D2, D16, D9)")
    print("  - Numerology (Radical, Destiny, Name numbers)")
    print("  - Dasha (Vimshottari Mahadasha, Antardasha, Pratyantardasha)")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
