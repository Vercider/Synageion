import sqlite3
from config import DB_NAME

def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
    
        # Rollen-Tabelle - Hier die Änderung mit DROP TABLE
        c.execute('DROP TABLE IF EXISTS roles')
        c.execute('''
            CREATE TABLE IF NOT EXISTS roles (
                role_id INTEGER PRIMARY KEY,
                role_name TEXT UNIQUE NOT NULL
            )
        ''')

        # Standard-Rollen einfügen - Hier INSERT OR REPLACE statt INSERT OR IGNORE
        roles = [
            (1, "Administrator"),
            (2, "Einkäufer"),
            (3, "Logistiker"),
            (4, "Vertriebler")
        ]
        c.executemany("INSERT OR REPLACE INTO roles (role_id, role_name) VALUES (?, ?)", roles)

        # Benutzer-Tabelle
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                role_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                FOREIGN KEY (role_id) REFERENCES roles(role_id)
            )
        ''')

        # Admin-Logs-Tabelle
        c.execute('''
            CREATE TABLE IF NOT EXISTS admin_logs (
                log_id INTEGER PRIMARY KEY,
                admin_id INTEGER,
                action TEXT NOT NULL,
                target TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (admin_id) REFERENCES users(user_id)
            )
        ''')

        # Artikelstamm - Vereinfachte Version
        c.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                article_id INTEGER PRIMARY KEY,
                article_number TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                min_stock INTEGER DEFAULT 0,
                status TEXT DEFAULT 'aktiv'
            )
        ''')

        # Ein Beispielartikel
        example_article = [
            ('ART001', 'ThinkPad X1 Carbon', 'Business Laptop der Oberklasse', 5, 'aktiv')
        ]
        
        c.executemany("""
            INSERT OR IGNORE INTO articles 
            (article_number, name, description, min_stock, status)
            VALUES (?, ?, ?, ?, ?)
        """, example_article)       

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise e
    finally:
        conn.close()