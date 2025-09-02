import streamlit as st
from controllers.session_controller import SessionController
from views.auth_view import AuthView
from views.admin_view import AdminView
from views.purchase_view import PurchaseView
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
            # PLACEHOLDER für weiter Views
        }

    # --- Ausführung der Views ---
    def run(self):
        # Prüfung des Timeouts
        if self.session_controller.check_timeout():
            return
        
        # Nicht eingeloggt -> AuthView
        if not st.session_state.get("logged_in", False):
            self.auth_view.render()
            return
        
        # Eingeloggt -> Rollenbasierte View
        role = st.session_state.get("role")
        if role in self.views:
            self.views[role].render()
        elif role == "Wartend":
            self.auth_view.render_waiting_status()

if __name__ == "__main__":
    st.set_page_config(page_title="SYNAGEION", layout="centered")
    init_db()

    app = Application()
    app.run()
