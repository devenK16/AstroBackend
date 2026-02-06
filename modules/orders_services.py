"""
Orders and payments: service prices (backend source of truth), Razorpay create/verify, email to admin.
Uses Razorpay TEST keys (rzp_test_*).
"""
import os
import uuid
from datetime import datetime

# Backend is source of truth: (service_id, plan_id) -> (amount_paise, service_title)
# plan_id is None for report services
SERVICE_PRICES = [
    ("detailed-horoscope", None, 179900, "Detailed Horoscope Report"),
    ("2026-analysis", None, 129900, "2026 Year Analysis"),
    ("numerology", None, 119900, "Numerology"),
    ("career", None, 139900, "Career Report"),
    ("marriage", None, 139900, "Marriage Report"),
    ("doshas", None, 109900, "Yogas & Dosha"),
    ("health", None, 139900, "Health & Wellness"),
    ("wealth", None, 139900, "Wealth & Finance"),
    ("ask-astrologer", "one", 24900, "Ask Astrologer (1 question)"),
    ("ask-astrologer", "three", 55900, "Ask Astrologer (3 questions)"),
]


def get_amount_and_title(service_id: str, plan_id: str | None) -> tuple[int, str] | None:
    for sid, pid, amount, title in SERVICE_PRICES:
        if sid == service_id and (pid == plan_id or (pid is None and plan_id in (None, ""))):
            return amount, title
    return None


def validate_create_payload(data: dict) -> tuple[bool, str]:
    """Returns (ok, error_message)."""
    if not data.get("service_id"):
        return False, "service_id is required"
    if not data.get("customer") or not isinstance(data["customer"], dict):
        return False, "customer object is required"
    c = data["customer"]
    if not c.get("name") or not c.get("email") or not c.get("mobile"):
        return False, "customer must have name, email, mobile"
    if not data.get("birth_details") or not isinstance(data["birth_details"], dict):
        return False, "birth_details object is required"
    b = data["birth_details"]
    for k in ("date_of_birth", "time_of_birth", "place_of_birth", "latitude", "longitude", "gender"):
        if k not in b:
            return False, f"birth_details must include {k}"
    if data.get("service_id") == "ask-astrologer":
        if data.get("plan_id") not in ("one", "three"):
            return False, "plan_id must be 'one' or 'three' for ask-astrologer"
        if not (data.get("questions") or "").strip():
            return False, "questions are required for ask-astrologer"
    else:
        if data.get("plan_id") not in (None, ""):
            data["plan_id"] = None
    return True, ""


def create_razorpay_order(amount_paise: int, receipt_prefix: str = "order_"):
    """Create order in Razorpay (test mode). Returns dict with order_id, key_id, amount_paise, currency."""
    import razorpay
    key_id = os.environ.get("RAZORPAY_KEY_ID", "")
    key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "")
    if not key_id or not key_secret:
        raise RuntimeError("RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET must be set")
    client = razorpay.Client(auth=(key_id, key_secret))
    receipt = receipt_prefix + str(uuid.uuid4()).replace("-", "")[:16]
    order = client.order.create(
        data={
            "amount": amount_paise,
            "currency": "INR",
            "receipt": receipt,
        }
    )
    return {
        "order_id": order["id"],
        "razorpay_order_id": order["id"],
        "key_id": key_id,
        "amount_paise": amount_paise,
        "currency": "INR",
    }


def verify_payment_signature(razorpay_order_id: str, razorpay_payment_id: str, razorpay_signature: str) -> bool:
    import razorpay
    key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "")
    if not key_secret:
        return False
    client = razorpay.Client(auth=(os.environ.get("RAZORPAY_KEY_ID", ""), key_secret))
    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        })
        return True
    except Exception:
        return False


def order_payload_to_record(order_payload: dict, razorpay_order_id: str, razorpay_payment_id: str) -> dict:
    """Build flat record for orders table from order_payload + payment ids."""
    amount, title = get_amount_and_title(
        order_payload["service_id"],
        order_payload.get("plan_id") or None,
    )
    if not amount:
        raise ValueError("Unknown service_id/plan_id")
    c = order_payload["customer"]
    b = order_payload["birth_details"]
    return {
        "razorpay_order_id": razorpay_order_id,
        "razorpay_payment_id": razorpay_payment_id,
        "service_id": order_payload["service_id"],
        "plan_id": order_payload.get("plan_id"),
        "service_title": title,
        "amount_paise": amount,
        "customer_name": c["name"],
        "customer_email": c["email"],
        "customer_mobile": c["mobile"],
        "date_of_birth": b.get("date_of_birth"),
        "time_of_birth": b.get("time_of_birth"),
        "place_of_birth": b.get("place_of_birth"),
        "latitude": b.get("latitude"),
        "longitude": b.get("longitude"),
        "gender": b.get("gender"),
        "questions": order_payload.get("questions"),
    }


def send_admin_email_for_order(record: dict):
    """Send one email to ADMIN_EMAIL with full order details (for forwarding to astrologer)."""
    admin_email = os.environ.get("ADMIN_EMAIL")
    if not admin_email:
        return  # skip if not configured
    amount_inr = record["amount_paise"] / 100
    body = f"""New order – Jyotimay

Order ref: {record.get('razorpay_order_id', '')}
Service: {record.get('service_title', '')}
Plan: {record.get('plan_id') or '-'}
Amount: INR {amount_inr:.2f}

Customer:
  Name: {record.get('customer_name', '')}
  Email: {record.get('customer_email', '')}
  Mobile: {record.get('customer_mobile', '')}

Birth details:
  DOB: {record.get('date_of_birth', '')}
  TOB: {record.get('time_of_birth', '')}
  Place: {record.get('place_of_birth', '')}
  Gender: {record.get('gender', '')}

"""
    if record.get("questions"):
        body += f"Questions:\n{record['questions']}\n"
    body += "\n---\nForward this to the astrologer as needed."

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    host = os.environ.get("SMTP_HOST", "")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER", "")
    password = os.environ.get("SMTP_PASSWORD", "")
    if not host or not user or not password:
        return  # skip sending if SMTP not configured
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Jyotimay order: {record.get('service_title', '')} – {record.get('customer_name', '')}"
    msg["From"] = user
    msg["To"] = admin_email
    msg.attach(MIMEText(body, "plain"))
    with smtplib.SMTP(host, port) as s:
        s.starttls()
        s.login(user, password)
        s.sendmail(user, [admin_email], msg.as_string())
