"""
SQLite database for orders and admin users.
Schema: orders, admin_users, pending_order_payloads (for webhook).
"""
import os
import sqlite3
import json
from contextlib import contextmanager

# Default path: instance/orders.db (create instance if needed)
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DATABASE_PATH = os.environ.get('DATABASE_PATH') or os.path.join(INSTANCE_DIR, 'orders.db')


def get_db_path():
    return DATABASE_PATH


@contextmanager
def get_db():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Create tables if they do not exist. Call on app startup."""
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                razorpay_order_id TEXT UNIQUE NOT NULL,
                razorpay_payment_id TEXT UNIQUE,
                service_id TEXT NOT NULL,
                plan_id TEXT,
                service_title TEXT NOT NULL,
                amount_paise INTEGER NOT NULL,
                customer_name TEXT NOT NULL,
                customer_email TEXT NOT NULL,
                customer_mobile TEXT NOT NULL,
                date_of_birth TEXT,
                time_of_birth TEXT,
                place_of_birth TEXT,
                latitude REAL,
                longitude REAL,
                gender TEXT,
                questions TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                completed_at TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
            CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);

            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS pending_order_payloads (
                razorpay_order_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
        """)


def save_pending_payload(razorpay_order_id: str, payload: dict):
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO pending_order_payloads (razorpay_order_id, payload, created_at) VALUES (?, ?, datetime('now'))",
            (razorpay_order_id, json.dumps(payload))
        )


def get_pending_payload(razorpay_order_id: str):
    with get_db() as conn:
        row = conn.execute(
            "SELECT payload FROM pending_order_payloads WHERE razorpay_order_id = ?",
            (razorpay_order_id,)
        ).fetchone()
    if not row:
        return None
    return json.loads(row[0])


def delete_pending_payload(razorpay_order_id: str):
    with get_db() as conn:
        conn.execute("DELETE FROM pending_order_payloads WHERE razorpay_order_id = ?", (razorpay_order_id,))


def order_exists_by_payment_id(razorpay_payment_id: str) -> bool:
    with get_db() as conn:
        row = conn.execute(
            "SELECT 1 FROM orders WHERE razorpay_payment_id = ?",
            (razorpay_payment_id,)
        ).fetchone()
    return row is not None


def save_order(record: dict):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO orders (
                razorpay_order_id, razorpay_payment_id, service_id, plan_id, service_title,
                amount_paise, customer_name, customer_email, customer_mobile,
                date_of_birth, time_of_birth, place_of_birth, latitude, longitude, gender,
                questions, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', datetime('now'))
        """, (
            record["razorpay_order_id"],
            record.get("razorpay_payment_id"),
            record["service_id"],
            record.get("plan_id"),
            record["service_title"],
            record["amount_paise"],
            record["customer_name"],
            record["customer_email"],
            record["customer_mobile"],
            record.get("date_of_birth"),
            record.get("time_of_birth"),
            record.get("place_of_birth"),
            record.get("latitude"),
            record.get("longitude"),
            record.get("gender"),
            record.get("questions"),
        ))
        return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def list_orders(status=None, from_date=None, to_date=None, limit=50, offset=0):
    with get_db() as conn:
        q = "SELECT id, razorpay_order_id, service_title, customer_name, customer_email, amount_paise, status, created_at FROM orders WHERE 1=1"
        params = []
        if status:
            q += " AND status = ?"
            params.append(status)
        if from_date:
            q += " AND date(created_at) >= date(?)"
            params.append(from_date)
        if to_date:
            q += " AND date(created_at) <= date(?)"
            params.append(to_date)
        q += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        rows = conn.execute(q, params).fetchall()
    return [dict(r) for r in rows]


def get_order_by_id(order_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    return dict(row) if row else None


def update_order_status(order_id: int, status: str):
    with get_db() as conn:
        conn.execute(
            "UPDATE orders SET status = ?, completed_at = datetime('now') WHERE id = ?",
            (status, order_id)
        )
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    return dict(row) if row else None


def get_orders_stats():
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        pending = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'pending'").fetchone()[0]
        completed = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'completed'").fetchone()[0]
        revenue = conn.execute("SELECT COALESCE(SUM(amount_paise), 0) FROM orders").fetchone()[0]
        last_7 = conn.execute(
            "SELECT COUNT(*) FROM orders WHERE created_at >= datetime('now', '-7 days')"
        ).fetchone()[0]
        last_30 = conn.execute(
            "SELECT COUNT(*) FROM orders WHERE created_at >= datetime('now', '-30 days')"
        ).fetchone()[0]
    return {
        "total_orders": total,
        "pending_orders": pending,
        "completed_orders": completed,
        "total_revenue_paise": revenue,
        "orders_last_7_days": last_7,
        "orders_last_30_days": last_30,
    }


def get_admin_by_username(username: str):
    with get_db() as conn:
        row = conn.execute("SELECT id, username, password_hash FROM admin_users WHERE username = ?", (username,)).fetchone()
    return dict(row) if row else None


def seed_admin_if_empty(password_hash_fn):
    """Create one admin user if admin_users is empty. password_hash_fn(username, password) -> hash."""
    with get_db() as conn:
        n = conn.execute("SELECT COUNT(*) FROM admin_users").fetchone()[0]
        if n > 0:
            return
        username = os.environ.get("ADMIN_USERNAME", "admin")
        password = os.environ.get("ADMIN_PASSWORD", "admin_change_me")
        h = password_hash_fn(password)
        conn.execute("INSERT INTO admin_users (username, password_hash) VALUES (?, ?)", (username, h))
