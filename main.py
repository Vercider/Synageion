import streamlit as st
import bcrypt
import sqlite3
from datetime import datetime
from permissions import requires_role, log_admin_action
from constants import DB_NAME, VALID_ROLES, DEFAULT_ROLE

# --- 1.Datenbank-Setup ---
DB_NAME = "users.db"# Benneung der SQLite-Datenbankdatei

#--- 1.1 Funktionen für die USER-Datenbank ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            role TEXT DEFAULT 'Vertriebler',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    """)

    # Admin-Account erstellen, falls nicht vorhanden
    admin_pw = hash_password("admin123")
    c.execute("INSERT OR IGNORE INTO users (username, hashed_password, role) VALUES (?, ?, ?)",
             ("admin", admin_pw, "Administrator"))
    conn.commit()
    conn.close()

#--- 1.2 Funktionen für die USER-Verwaltung ---
def register_user_db(username, hashed_password, role="Vertriebler"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, hashed_password, role) VALUES (?, ?, ?)",
                 (username, hashed_password, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

#--- 1.3 Funktionen für die USER-Authentifizierung ---
def get_user_db(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT hashed_password, role FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result if result else (None, None)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')# Hashen des Passworts

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))# Überprüfung des Passworts gegen den Hash

#--- 1.4 Admin-Funktionen ---
#-- 1.4.1 Benutzerrolle aktualisieren --
@requires_role("Administrator")
def update_user_role(username, new_role):
    if new_role not in VALID_ROLES:
        return False
        
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET role = ? WHERE username = ?", (new_role, username))
        conn.commit()
        log_admin_action(
            st.session_state.username,
            "Rollenänderung",
            f"User: {username} -> {new_role}"
        )
        return True
    except sqlite3.Error as e:
        print(f"Datenbankfehler: {e}")
        return False
    finally:
        conn.close()

#-- 1.4.2 Letzten Login-Zeitstempel aktualisieren --
def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username, role FROM users")
    users = c.fetchall()
    conn.close()
    return users

#---- 2.Hauptseite ----
st.set_page_config(page_title="SYNAGEION", layout="centered")# Seiteneinstellungen

st.title("Willkommen bei Synageion\n Bitte anmelden bzw. registrieren:")#

#---- 3.Datenbank initialisieren ----
init_db()

#---- 4.Session State initialisieren ----
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:  # Neue Zeile
    st.session_state.role = ""

#---- 5.Funktionen für die Formulare ----
#--- 5.1 Login-Formular ---
def login_form():
    st.subheader("Anmelden")
    username = st.text_input("Benutzername", key="login_username")
    password = st.text_input("Passwort", type="password", key="login_password")

    if st.button("Anmelden"):
        try:
            result = get_user_db(username)
            if result:
                hashed_pw_from_db, role = result
                if check_password(password, hashed_pw_from_db):
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    c.execute("""
                        UPDATE users 
                        SET last_login = CURRENT_TIMESTAMP 
                        WHERE username = ?
                    """, (username,))
                    conn.commit()
                    conn.close()
                    
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = role
                    st.success(f"Erfolgreich angemeldet als {username} ({role})!")
                    st.rerun()
                else:
                    st.error("Falsches Passwort!")
            else:
                st.error("Benutzer nicht gefunden!")
        except sqlite3.Error as e:
            st.error(f"Datenbankfehler: {e}")

#--- 5.2 Registrierungsformular ---
def register_form():
    st.subheader("Registrieren")# Registrierungsformular im subheader
    new_username = st.text_input("Neuer Benutzername", key="register_username")# Eingabefeld für den neuen Benutzernamen
    new_password = st.text_input("Neues Passwort", type="password", key="register_password")# Eingabefeld für das neue Passwort
    confirm_password = st.text_input("Passwort bestätigen", type="password", key="confirm_password")# Eingabefeld zur Bestätigung des neuen Passworts

    if st.button("Registrieren"):
        if new_password != confirm_password:# Überprüfung, ob die Passwörter übereinstimmen
            st.error("Passwörter stimmen nicht überein.")
        elif len(new_username) < 4:# Überprüfung der Mindestlänge des Benutzernamens
            st.error("Der Benutzername muss mindestens 4 Zeichen lang sein.")
        elif len(new_password) < 6:# Überprüfung der Mindestlänge des Passworts
            st.error("Das Passwort muss mindestens 6 Zeichen lang sein.")
        else:
            hashed_pw = hash_password(new_password)# Passwort hashen
            if register_user_db(new_username, hashed_pw):# Benutzer in der Datenbank registrieren
                st.success("Registrierung erfolgreich! Sie können sich jetzt anmelden.")
            else:
                st.error("Dieser Benutzername existiert bereits.")

#--- 5.3 Admin-Benutzerverwaltung ---
def admin_panel():
    st.subheader("Benutzerverwaltung")# Admin-Benutzerverwaltungsbereich im subheader
    users = get_all_users()# Alle Benutzer aus der Datenbank abrufen

    for username, current_role in users:
        col1, col2, col3 = st.columns([2, 2, 1])# Spaltenlayout für Benutzerinformationen und Rollenänderung
        with col1:
            st.text(username)
        with col2:
            new_role = st.selectbox(
                "Rolle", 
                ["Administrator", "Einkäufer", "Logistiker", "Vertriebler"],
                index=["Administrator", "Einkäufer", "Logistiker", "Vertriebler"].index(current_role),
                key=f"role_{username}"
            )
        with col3:
            if st.button("Speichern", key=f"update_{username}"):
                if update_user_role(username, new_role):
                    st.success(f"Rolle von {username} zu {new_role} geändert.")
                else:
                    st.error("Fehler beim Aktualisieren der Rolle.")

#---- 6. Hauptlogik ----
if st.session_state.logged_in:
    st.write(f"Hallo {st.session_state.username}! Sie sind angemeldet als {st.session_state.role}.")

    # Admin-Panel nur für Administratoren anzeigen
    if st.session_state.role == "Administrator":
        admin_panel()
    
    # Abmelden-Button
    if st.button("Abmelden"):
        st.session_state.logged_in = False
        st.session_state.username = ""# Session-Status zurücksetzen
        st.session_state.role = ""
        st.info("Sie wurden abgemeldet.")#  Abmeldebestätigung
        st.rerun()

else:
    tab1, tab2 = st.tabs(["Anmelden", "Registrieren"])# Tabs für Anmelden und Registrieren

    with tab1:
        login_form()

    with tab2:
        register_form()