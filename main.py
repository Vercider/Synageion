import streamlit as st
import bcrypt
import sqlite3

# --- 1.Datenbank-Setup ---
DB_NAME = "users.db"# Benneung der SQLite-Datenbankdatei

#--- 1.1 Funktionen für die USER-Datenbank ---
def init_db():
    conn = sqlite3.connect(DB_NAME)# Verbindung zur SQLite-Datenbank herstellen
    c = conn.cursor()# Cursor für Datenbank erstellen
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            hashed_password TEXT NOT NULL
        )
    """)# SQL-Befehle für Erstellung der USER-Tabelle
    conn.commit()# Änderungen speichern
    conn.close()# Verbindung schließen

#--- 1.2 Funktionen für die USER-Verwaltung ---
def register_user_db(username, hashed_password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (username, hashed_password))# Benutzer in die Datenbank einfügen
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Benutzername existiert bereits
    finally:
        conn.close()

#--- 1.3 Funktionen für die USER-Authentifizierung ---
def get_user_db(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))# Abfrage des gehashten Passworts für den gegebenen Benutzernamen 
    result = c.fetchone()# Ergebnis der Abfrage holen
    conn.close()
    return result[0] if result else None# Rückgabe des gehashten Passworts aus dem Tupel oder None, wenn der Benutzer nicht existiert

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')# Hashen des Passworts

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))# Überprüfung des Passworts gegen den Hash

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

#---- 5.Funktionen für die Formulare ----
#--- 5.1 Login-Formular ---
def login_form():
    st.subheader("Anmelden")# Anmeldeformular im subheader
    username = st.text_input("Benutzername", key="login_username")# Eingabefeld für den Benutzernamen
    password = st.text_input("Passwort", type="password", key="login_password")# Eingabefeld für das Passwort

    if st.button("Anmelden"):
        hashed_pw_from_db = get_user_db(username)# Gehashtes Passwort aus der Datenbank abrufen
        if hashed_pw_from_db and check_password(password, hashed_pw_from_db):# Passwort überprüfen
            st.session_state.logged_in = True
            st.session_state.username = username # Session-Status aktualisieren
            st.success(f"Erfolgreich angemeldet als {username}!")
            st.rerun()# Seite neu laden
        else:
            st.error("Ungültiger Benutzername oder Passwort")# Fehlermeldung bei ungültigen Anmeldedaten

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

#---- 6. Hauptlogik ----
if st.session_state.logged_in:
    st.write(f"Hallo {st.session_state.username}! Sie sind angemeldet.")
    
    # Abmelden-Button
    if st.button("Abmelden"):
        st.session_state.logged_in = False
        st.session_state.username = ""# Session-Status zurücksetzen
        st.info("Sie wurden abgemeldet.")#  Abmeldebestätigung
        st.rerun()

else:
    tab1, tab2 = st.tabs(["Anmelden", "Registrieren"])# Tabs für Anmelden und Registrieren

    with tab1:
        login_form()

    with tab2:
        register_form()