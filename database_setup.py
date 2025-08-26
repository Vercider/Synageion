import sqlite3
from datetime import datetime

DB_NAME = "users.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
    
        # Rollen-Tabelle
        c.execute('''
            CREATE TABLE IF NOT EXISTS roles (
                role_id INTEGER PRIMARY KEY,
                role_name TEXT UNIQUE NOT NULL
            )
        ''')

        # Berechtigungs-Tabelle
        c.execute('''
            CREATE TABLE IF NOT EXISTS permissions (
                permission_id INTEGER PRIMARY KEY,
                permission_name TEXT UNIQUE NOT NULL
            )
        ''')

        # Benutzer-Tabelle mit Rollenzuweisung
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (role_id) REFERENCES roles(role_id)
            )
        ''')

        # Rollen-Berechtigungen Verknüpfungstabelle
        c.execute('''
            CREATE TABLE IF NOT EXISTS role_permissions (
                role_id INTEGER,
                permission_id INTEGER,
                FOREIGN KEY (role_id) REFERENCES roles(role_id),
                FOREIGN KEY (permission_id) REFERENCES permissions(permission_id),
                PRIMARY KEY (role_id, permission_id)
        ''')

        # Admin-Aktionen Log-Tabelle
        c.execute('''
            CREATE TABLE IF NOT EXISTS admin_logs (
                log_id INTEGER PRIMARY KEY,
                admin_user_id INTEGER,
                action TEXT NOT NULL,
                target TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (admin_user_id) REFERENCES users(user_id)
            )
        ''')

    # Standard-Rollen definieren
        roles = [
            (1, "Adminstrator"),
            (2, "Einkäufer"),
            (3, "Logistiker"),
            (4, "Vertreibler")
    ]
        
        c.executemany('INSERT OR IGNORE INTO roles (role_id, role_name) VALUES (?, ?)', roles)

        conn.commit()
    except sqlite3.Error as e:
        print(f"Datenbankfehler beim Setup: {e}")
        raise
    conn.close()