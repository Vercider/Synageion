import streamlit as st
from controllers.session_controller import SessionController
from views.auth_view import AuthView
from views.admin_view import AdminView
from views.purchase_view import PurchaseView
from views.logistics_view import LogisticsView
from views.sales_view import SalesView
from database_setup import init_db


# ----- HAUPT-Initialisierung -----
# ---- HAUPT-Initialisierungsklasse ----
class Application:
    # --- View- und Controller-Initialisierung über Hauptklasse ---
    def __init__(self):
        self.session_controller = SessionController()
        self.auth_view = AuthView()
        self.views = {
            "Administrator": AdminView(),
            "Einkäufer": PurchaseView(),
            "Logistiker": LogisticsView(),
            "Vertriebler": SalesView()
        }

    # --- Ausführung der Views ---
    def run(self):
        """Hauptschleife der Anwendung"""
        
        # ✅ Session-Timeout prüfen (für eingeloggte User)
        if st.session_state.get('logged_in', False):
            if self.session_controller.check_timeout():
                st.warning("⏰ Ihre Session ist abgelaufen. Bitte melden Sie sich erneut an.")
                st.session_state.clear()
                st.rerun()
        
        # Nicht eingeloggt -> AuthView
        if not st.session_state.get('logged_in', False):
            self.auth_view.render()
            return
        
        # Eingeloggt -> Rollenbasierte View
        role = st.session_state.get('role')
        if role in self.views:
            self.views[role].render()
        elif role == "Wartend":
            self.auth_view.render_waiting_status()

if __name__ == "__main__":
    st.set_page_config(page_title="SYNAGEION", layout="centered")
    init_db()

    app = Application()
    app.run()
