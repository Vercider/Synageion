import os
import sqlite3
import bcrypt
import streamlit as st
from datetime import datetime, timedelta
from functools import wraps
from config import DB_NAME, ADMIN_USERNAME, ADMIN_PASSWORD
from logger import setup_logger
from database_setup import init_db as setup_db
from permissions import requires_role, log_admin_action
from constants import VALID_ROLES, DEFAULT_ROLE
from role_functions import (
    show_admin_functions, 
    show_purchase_functions,
    show_logistics_functions,
    show_sales_functions
)

# Logger initialisieren
logger = setup_logger()

# --- 1.Datenbank-Setup ---
DB_NAME = "users.db"# Benneung der SQLite-Datenbankdatei

#--- 1.1 Funktionen für die USER-Datenbank ---
def init_db():
    setup_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    if ADMIN_PASSWORD and ADMIN_USERNAME:
        admin_pw = hash_password(ADMIN_PASSWORD)
        c.execute("""
            INSERT OR IGNORE INTO users (username, hashed_password, role_id) 
            VALUES (?, ?, (SELECT role_id FROM roles WHERE role_name = 'Administrator'))
        """, (ADMIN_USERNAME, admin_pw))
        conn.commit()
    conn.close()

#--- 1.2 Funktionen für die USER-Verwaltung ---
def register_user_db(username, hashed_password, role=DEFAULT_ROLE):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO users (username, hashed_password, role_id)
            SELECT ?, ?, role_id 
            FROM roles 
            WHERE role_name = ?
        """, (username, hashed_password, role))
        conn.commit()
        logger.info(f"Neuer Benutzer registriert: {username} mit Rolle {role}")
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"Registrierung fehlgeschlagen - Benutzername existiert bereits: {username}")
        return False
    except sqlite3.Error as e:
        logger.error(f"Datenbankfehler bei Registrierung: {e}")
        return False
    finally:
        conn.close()

# Session-Management mit timedelta
SESSION_TIMEOUT = timedelta(minutes=30)

def check_session_timeout():
    if 'last_activity' in st.session_state:
        if datetime.now() - st.session_state.last_activity > SESSION_TIMEOUT:
            st.session_state.clear()
            return True
    st.session_state.last_activity = datetime.now()
    return False

#--- 1.3 Funktionen für die USER-Authentifizierung ---
def get_user_db(username):
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
    return result if result else (None, None)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

#--- 1.4 Admin-Funktionen ---
#-- 1.4.1 Benutzerrolle aktualisieren --
@requires_role("Administrator")
def update_user_role(username, new_role):
    if new_role not in VALID_ROLES:
        return False
        
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("""
            UPDATE users 
            SET role_id = (SELECT role_id FROM roles WHERE role_name = ?) 
            WHERE username = ?
        """, (new_role, username))
        conn.commit()
        log_admin_action(
            st.session_state.username,
            "Rollenänderung",
            f"User: {username} -> {new_role}"
        )
        return True
    except sqlite3.Error as e:
        logger.error(f"Datenbankfehler: {e}")
        return False
    finally:
        conn.close()

#-- 1.4.2 Letzten Login-Zeitstempel aktualisieren --
def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("""
            SELECT u.username, r.role_name
            FROM users u
            JOIN roles r ON u.role_id = r.role_id
        """)
        users = c.fetchall()
        return users
    except sqlite3.Error as e:
        logger.error(f"Error fetching users: {e}")
        return []
    finally:
        conn.close()

def show_dashboard():
    st.sidebar.title(f"👤 {st.session_state.username}")
    st.sidebar.text(f"Rolle: {st.session_state.role}")
    
    if st.session_state.logged_in:
        if st.session_state.role == "Administrator":
            show_admin_functions()
        elif st.session_state.role == "Einkäufer":
            show_purchase_functions()
        elif st.session_state.role == "Logistiker":
            show_logistics_functions()
        elif st.session_state.role == "Vertriebler":
            show_sales_functions()

#---- 2.Hauptseite ----
st.set_page_config(page_title="SYNAGEION", layout="centered")# Seiteneinstellungen

st.title("Willkommen bei Synageion\n Bitte anmelden bzw. registrieren:")

#---- 3.Datenbank initialisieren ----
init_db()

#---- 4.Session State initialisieren ----
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None

if "last_activity" not in st.session_state:
    st.session_state.last_activity = datetime.now()

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
@requires_role("Administrator")
def admin_panel():
    st.subheader("Admin-Panel - Benutzerverwaltung")
    
    users = get_all_users()
    
    st.write("Benutzerrollen ändern:")
    for username, current_role in users:  # Jetzt werden genau 2 Werte entpackt
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Benutzer: {username}")
        with col2:
            new_role = st.selectbox(
                f"Rolle für {username}",
                options=VALID_ROLES,
                index=VALID_ROLES.index(current_role),
                key=f"role_{username}"
            )
            if new_role != current_role:
                if st.button(f"Rolle ändern für {username}"):
                    update_user_role(username, new_role)
                    log_admin_action(st.session_state.username, 
                                   "role_change", 
                                   f"{username}: {current_role} -> {new_role}")
                    st.success(f"Rolle für {username} zu {new_role} geändert!")
                    st.rerun()
                    
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