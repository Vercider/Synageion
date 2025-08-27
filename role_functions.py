import streamlit as st
import sqlite3
from permissions import requires_role
from config import DB_NAME

@requires_role("Administrator")
def show_admin_functions():
    st.title("🔑 Administrator Dashboard")
    st.write(f"Willkommen im Administrationsbereich, {st.session_state.username}!")
    
    tab1, tab2 = st.tabs(["👥 Benutzerverwaltung", "📝 System Log"])
    with tab1:
        admin_panel()
    with tab2:
        show_admin_logs()

@requires_role("Logistiker")
def show_logistics_functions():
    st.title("🚚 Logistik Dashboard")
    st.write(f"Willkommen im Logistikmanagement, {st.session_state.username}!")
    
    tab1, tab2, tab3 = st.tabs(["📦 Lagerbestand", "🚛 Lieferungen", "📊 Statistik"])
    with tab1:
        show_inventory()
    with tab2:
        show_deliveries()
    with tab3:
        show_logistics_stats()

@requires_role("Vertriebler")
def show_sales_functions():
    st.title("💼 Vertriebs Dashboard")
    st.write(f"Willkommen im Vertriebsmanagement, {st.session_state.username}!")
    
    tab1, tab2, tab3 = st.tabs(["👥 Kunden", "📊 Verkäufe", "📈 Prognosen"])
    with tab1:
        show_customers()
    with tab2:
        show_sales()
    with tab3:
        show_forecasts()

def add_article(article_number, name, description, min_stock, status="aktiv"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO articles (article_number, name, description, min_stock, status)
            VALUES (?, ?, ?, ?, ?)
        """, (article_number, name, description, min_stock, status))
        conn.commit()
        return True, "Artikel erfolgreich angelegt"
    except sqlite3.IntegrityError:
        return False, "Artikelnummer existiert bereits"
    except sqlite3.Error as e:
        return False, f"Datenbankfehler: {e}"
    finally:
        conn.close()

def get_all_articles():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("SELECT article_number, name, description, min_stock, status FROM articles")
        return c.fetchall()
    except sqlite3.Error:
        return []
    finally:
        conn.close()

@requires_role("Einkäufer")
def show_purchase_functions():
    st.title("🛒 Einkäufer Dashboard")
    st.write(f"Willkommen im Einkaufsmanagement, {st.session_state.username}!")
    
    tab1, tab2 = st.tabs(["📦 Artikelstamm", "➕ Neuer Artikel"])
    
    with tab1:
        st.subheader("Artikelübersicht")
        articles = get_all_articles()
        if articles:
            # Konvertiere die Artikel in ein Dictionary für das DataFrame
            articles_dict = {
                "Artikelnummer": [a[0] for a in articles],
                "Name": [a[1] for a in articles],
                "Beschreibung": [a[2] for a in articles],
                "Mindestbestand": [a[3] for a in articles],
                "Status": [a[4] for a in articles]
            }
            st.dataframe(articles_dict)
        else:
            st.info("Keine Artikel vorhanden")
    
    with tab2:
        st.subheader("Neuen Artikel anlegen")
        with st.form("new_article_form"):
            article_number = st.text_input("Artikelnummer")
            name = st.text_input("Artikelname")
            description = st.text_area("Beschreibung")
            min_stock = st.number_input("Mindestbestand", min_value=0, value=0)
            status = st.selectbox("Status", ["aktiv", "inaktiv"])
            
            submitted = st.form_submit_button("Artikel anlegen")
            if submitted:
                if not article_number or not name:
                    st.error("Artikelnummer und Name sind erforderlich!")
                else:
                    success, message = add_article(
                        article_number, name, description, min_stock, status
                    )
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                        
# Hilfsfunktionen für die einzelnen Bereiche
def show_orders():
    st.subheader("Bestellverwaltung")
    st.info("Hier können Sie Bestellungen verwalten und neue Bestellungen aufgeben.")

def show_suppliers():
    st.subheader("Lieferantenverwaltung")
    st.info("Hier können Sie Lieferanten verwalten und neue Lieferanten anlegen.")

def show_inventory():
    st.subheader("Lagerbestandsverwaltung")
    st.info("Hier sehen Sie den aktuellen Lagerbestand und können Waren ein- und ausbuchen.")

def show_deliveries():
    st.subheader("Lieferungsverwaltung")
    st.info("Hier können Sie Lieferungen planen und verfolgen.")

def show_logistics_stats():
    st.subheader("Logistik-Statistiken")
    st.info("Hier finden Sie Statistiken und Analysen zur Logistik.")

def show_customers():
    st.subheader("Kundenverwaltung")
    st.info("Hier können Sie Kunden verwalten und neue Kunden anlegen.")

def show_sales():
    st.subheader("Verkaufsübersicht")
    st.info("Hier sehen Sie alle Verkäufe und können neue Verkäufe erfassen.")

def show_forecasts():
    st.subheader("Vertriebsprognosen")
    st.info("Hier finden Sie Prognosen und Analysen für den Vertrieb.")

# Admin Hilfsfunktionen
def admin_panel():
    st.subheader("👥 Benutzerverwaltung")
    
    # Beispiel für Benutzerübersicht
    users_data = {
        "Benutzername": ["admin", "einkauf1", "logistik1", "vertrieb1"],
        "Rolle": ["Administrator", "Einkäufer", "Logistiker", "Vertriebler"],
        "Letzter Login": ["2025-08-26", "2025-08-25", "2025-08-26", "2025-08-24"]
    }
    
    st.dataframe(users_data)
    
    # Placeholder für Benutzer hinzufügen
    with st.expander("Neuen Benutzer anlegen"):
        st.text_input("Benutzername")
        st.selectbox("Rolle", ["Administrator", "Einkäufer", "Logistiker", "Vertriebler"])
        st.text_input("Passwort", type="password")
        st.button("Benutzer anlegen")

def show_admin_logs():
    st.subheader("📝 System Log")
    
    # Beispiel für System Logs
    log_data = {
        "Zeitstempel": ["2025-08-26 10:00", "2025-08-26 09:45", "2025-08-26 09:30"],
        "Benutzer": ["admin", "einkauf1", "logistik1"],
        "Aktion": ["Benutzer angelegt", "Login", "Logout"],
        "Details": ["Neuer Benutzer: vertrieb2", "Erfolgreicher Login", "Session beendet"]
    }