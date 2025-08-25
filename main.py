import streamlit as st
import bcrypt
import sqlite3

# --- Datenbank-Setup ---
DB_NAME = "users.db"

def init_db():
    """Stellt eine Verbindung zur Datenbank her und erstellt die Benutzertabelle, falls sie nicht existiert."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            hashed_password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def register_user_db(username, hashed_password):
    """Fügt einen neuen Benutzer in die Datenbank ein."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Benutzername existiert bereits
    finally:
        conn.close()

def get_user_db(username):
    """Ruft einen Benutzer aus der Datenbank ab."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def hash_password(password):
    """Hasht ein Passwort mit bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    """Vergleicht ein Klartext-Passwort mit einem gehashten Passwort."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# --- Hauptseite ---
st.set_page_config(page_title="ERP-Light System", layout="centered")

st.title("Willkommen beim ERP-Light System")

# Initialisiere die Datenbank beim Start der App
init_db()

# Session State initialisieren
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def login_form():
    """Zeigt das Anmeldeformular an und verarbeitet die Logik."""
    st.subheader("Anmelden")
    username = st.text_input("Benutzername", key="login_username")
    password = st.text_input("Passwort", type="password", key="login_password")

    if st.button("Anmelden"):
        hashed_pw_from_db = get_user_db(username)
        if hashed_pw_from_db and check_password(password, hashed_pw_from_db):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Erfolgreich angemeldet als {username}!")
            st.rerun()
        else:
            st.error("Ungültiger Benutzername oder Passwort")

def register_form():
    """Zeigt das Registrierungsformular an und verarbeitet die Logik."""
    st.subheader("Registrieren")
    new_username = st.text_input("Neuer Benutzername", key="register_username")
    new_password = st.text_input("Neues Passwort", type="password", key="register_password")
    confirm_password = st.text_input("Passwort bestätigen", type="password", key="confirm_password")

    if st.button("Registrieren"):
        if new_password != confirm_password:
            st.error("Passwörter stimmen nicht überein.")
        elif len(new_username) < 4:
            st.error("Der Benutzername muss mindestens 4 Zeichen lang sein.")
        elif len(new_password) < 6:
            st.error("Das Passwort muss mindestens 6 Zeichen lang sein.")
        else:
            hashed_pw = hash_password(new_password)
            if register_user_db(new_username, hashed_pw):
                st.success("Registrierung erfolgreich! Sie können sich jetzt anmelden.")
            else:
                st.error("Dieser Benutzername existiert bereits.")

# Hauptlogik der Seite
if st.session_state.logged_in:
    st.write(f"Hallo {st.session_state.username}! Sie sind angemeldet.")
    
    # Abmelden-Button
    if st.button("Abmelden"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.info("Sie wurden abgemeldet.")
        st.rerun()

else:
    tab1, tab2 = st.tabs(["Anmelden", "Registrieren"])

    with tab1:
        login_form()

    with tab2:
        register_form()