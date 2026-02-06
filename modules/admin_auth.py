"""
Admin authentication: password hashing (werkzeug), JWT issue and verify.
"""
import os
from functools import wraps

from werkzeug.security import generate_password_hash, check_password_hash

try:
    import jwt
except ImportError:
    jwt = None


def hash_password(password: str) -> str:
    return generate_password_hash(password, method="pbkdf2:sha256")


def check_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)


def issue_jwt(username: str) -> str:
    if not jwt:
        raise RuntimeError("PyJWT is required for admin auth. pip install PyJWT")
    secret = os.environ.get("JWT_SECRET") or os.environ.get("SECRET_KEY") or "change-me-in-production"
    return jwt.encode(
        {"sub": username, "scope": "admin"},
        secret,
        algorithm="HS256",
    )


def verify_jwt(token: str) -> dict | None:
    if not jwt or not token:
        return None
    secret = os.environ.get("JWT_SECRET") or os.environ.get("SECRET_KEY") or "change-me-in-production"
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        if payload.get("scope") == "admin":
            return payload
    except Exception:
        pass
    return None


def get_bearer_token(request) -> str | None:
    auth = request.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
        return auth[7:].strip()
    return None


def admin_required(f):
    """Decorator: require valid admin JWT. Injects request and payload into view (or use g.current_admin)."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        from flask import g, request, jsonify
        token = get_bearer_token(request)
        payload = verify_jwt(token) if token else None
        if not payload:
            return jsonify({"error": "Unauthorized"}), 401
        g.current_admin = payload
        return f(*args, **kwargs)
    return wrapped
