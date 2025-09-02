import sqlite3
import bcrypt
import streamlit as st
from config import DB_NAME

# ---- 2.2 Authentifikator-Controller ----
class AuthController:
    # --- 2.2.1 Authentifikator-Initialisierung ---
    def __init__(self):
        pass
    
    # --- 2.2.2 Login-Authentifizierung ---
    def login_user(self, username, password):
        """Überprüfe Login-Daten"""
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()

            c.execute("""
                      SELECT u.hashed_password, r.role_name
                      FROM users u
                      JOIN roles r ON u.role_id = r.role_id
                      WHERE u.username = ?
                      """, (username,))
            
            result = c.fetchone()
            conn.close()

            if result:
                hashed_pw, role = result
                if bcrypt.checkpw(password.encode("utf-8"), hashed_pw):
                    return True, role, "Login erfolgreich"
                else:
                    return False, None, "Falsches Passwort"
            else:
                return False, None, "Benutzer nicht gefunden"
            
        except Exception as e:
            return False, None, f"Fehler: {str(e)}"
    
    # --- 2.2.3 User-Anlage ---
    def register_user(self, username, password, role):
        """Registriert neuen Benutzer"""
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()

            # Passwort-Hash
            hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            c.execute("""
                    INSERT INTO users (username, hashed_password, role_id)
                    SELECT ?, ?, role_id FROM roles WHERE role_name = ?
                    """, (username, hashed_pw, role))
            
            conn.commit()
            conn.close()
            return True, "Registrierung erfolgreich"
        
        except sqlite3.IntegrityError:
            return False, "Benutzername bereits vergeben"
        except Exception as e:
            return False, f"Fehler: {str(e)}"
        
