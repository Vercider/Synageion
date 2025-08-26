import streamlit as st
from permissions import requires_role

@requires_role("Administrator")
def show_admin_functions():
    st.title("🔑 Administrator Dashboard")
    st.write(f"Willkommen im Administrationsbereich, {st.session_state.username}!")
    
    tab1, tab2 = st.tabs(["👥 Benutzerverwaltung", "📝 System Log"])
    with tab1:
        admin_panel()
    with tab2:
        show_admin_logs()

@requires_role("Einkäufer")
def show_purchase_functions():
    st.title("🛒 Einkäufer Dashboard")
    st.write(f"Willkommen im Einkaufsmanagement, {st.session_state.username}!")
    
    tab1, tab2 = st.tabs(["📦 Bestellungen", "🏢 Lieferanten"])
    with tab1:
        show_orders()
    with tab2:
        show_suppliers()

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