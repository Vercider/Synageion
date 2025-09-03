import sqlite3
import bcrypt
import streamlit as st
from config import DB_NAME
from constants import MIN_PASSWORD_LENGTH

# ---- 2.2 Authentifikator-Controller ----
class AuthController:
    # --- 2.2.1 Authentifikator-Initialisierung ---
    def __init__(self):
        pass
    
    # --- 2.2.2 Login-Authentifizierung ---
    def login_user(self, username, password):
        """Benutzer anmelden"""
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
                    # ✅ Login-Zeit für Session-Timeout setzen
                    import time
                    st.session_state.login_time = time.time()  # ← HINZUFÜGEN
                    
                    return True, role, "Login erfolgreich!"
                else:
                    return False, None, "Falsches Passwort"
            else:
                return False, None, "Benutzer nicht gefunden"
            
        except Exception as e:
            return False, None, f"Fehler beim Login: {str(e)}"
    
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
        
    # --- 2.2.4 Passwort-Reset für alle Rollen ---
    def change_password(self, username, old_password, new_password, confirm_password):
        """Passwort für eingeloggten User ändern"""
        try:
            # Validierung
            if not all([old_password, new_password, confirm_password]):
                return False, "Alle Felder sind erforderlich"
            
            if new_password != confirm_password:
                return False, "Neue Passwörter stimmen nicht überein"
            
            if len(new_password) < MIN_PASSWORD_LENGTH:
                return False, f"Passwort muss mindestens {MIN_PASSWORD_LENGTH} Zeichen haben"
            
            # Altes Passwort mit SQL prüfen
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()

            # Aktuelles Passwort abrufen
            c.execute("""
                    SELECT hashed_password, user_id
                    FROM users
                    WHERE username = ?
                    """, (username,))
            
            result = c.fetchone()

            if not result:
                conn.close()
                return False, "Benutzer nicht gefunden"
                
            current_hash, user_id = result

            # Altes Passwort prüfen
            if not bcrypt.checkpw(old_password.encode("utf-8"), current_hash):
                conn.close()
                return False, "Aktuelles Passwort ist falsch"
            
            # Neues Passwort hashen und speichern
            new_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

            c.execute("""
                    UPDATE users
                    SET hashed_password = ?
                    WHERE user_id = ?
                    """, (new_hash, user_id))
            
            conn.commit()
            conn.close()

            return True, "Passwort erfolgreich geändert!"
        
        except Exception as e:
            if "conn" in locals():
                conn.close()
            return False, f"Fehler beim Passwort-Wechsel: {str(e)}"
            

