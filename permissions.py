import sqlite3
from functools import wraps
import streamlit as st

DB_NAME = "users.db"

def requires_role(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not hasattr(st.session_state, "role") or st.session_state.role != required_role:
                st.error(f"Diese Funktion erfordert Rolle: {required_role}")
                return None
            return f(*args, **kwargs)
        return wrapper
    return decorator

def log_admin_action(admin_username: str, action: str, target: str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    try:
        c.execute("""
            INSERT INTO admin_logs (admin_id, action, target)
            SELECT user_id, ?, ? 
            FROM users WHERE username = ?
        """, (action, target, admin_username))
        conn.commit()
    finally:
        conn.close()