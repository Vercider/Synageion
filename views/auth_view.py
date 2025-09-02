import streamlit as st
from controllers.auth_controller import AuthController
from constants import VALID_ROLES, DEFAULT_ROLE, MIN_PASSWORD_LENGTH, MIN_USERNAME_LENGTH

# ----- 3.2 Authentifikations-View -----
class AuthView:
    # --- 3.2.1 Auth-View Initialisierung ---
    def __init__(self):
        """Initialisiert die Auth View"""
        self.controller = AuthController()
    
    # --- 3.2.2 Hauptansicht rendern ---
    def render(self):
        """Rendert Login/Register Tabs"""
        st.title("Willkommen bei Synageion")

        # Tab-Navigation
        tab1, tab2 = st.tabs(["🔑 Anmelden", "📝 Registrieren"])

        with tab1:
            self._render_login_form()

        with tab2:
            self._render_register_form()

    # --- 3.2.3 Login-Formular ---
    def _render_login_form(self):
        """Zeigt Login-Formular"""
        st.subheader("Anmelden")

        with st.form("login_form"):
            username = st.text_input(
                "Benutzername",
                placeholder="Ihr Benutzername",
                help="Geben Sie Ihren Benutzernamen ein"
            )

            password = st.text_input(
                "Passwort",
                type="password",
                placeholder="Ihr Passwort",
                help="Geben Sie Ihr Passwort ein"
            )

            submitted = st.form_submit_button("Anmelden", type="primary")

            if submitted:
                self._handle_login(username, password)

    # --- 3.2.4 Register Formular ---
    def _render_register_form(self):
        """Zeigt Registrierungs-Formular"""
        st.subheader("Neuen Benutzer registrieren")

        # Sicherheitshinweis
        st.info("ℹ️ Nach der Registrierung erhalten Sie zunächst eingeschränkte Rechte. Ein Administrator wird Ihnen die passende Rolle zuweisen.")

        with st.form("register_form"):
            username = st.text_input(
                "Benutzername",
                placeholder="Mindestens 4 Zeichen",
                help=f"Mindestens {MIN_USERNAME_LENGTH} Zeichen lang"
            )

            password = st.text_input(
                "Passwort",
                type="password",
                placeholder="Mindestens 6 Zeichen",
                help=f"Mindestens {MIN_PASSWORD_LENGTH} Zeichen lang"
            )

            confirm_password = st.text_input(
                "Passwort bestätigen",
                type="password",
                placeholder="Passwort wiederholen"
            )
            
            submitted = st.form_submit_button("Registrieren", type="primary")

            if submitted:
                self._handle_register(username, password, confirm_password, DEFAULT_ROLE)

    # --- 3.2.5 Login-Handler ---
    def _handle_login(self, username, password):
        """Verarbeitet Login-Anfrage"""

        # Client-seitige Validierung
        if not username.strip():
            st.error("Benutzername ist erforderlich!")
            return
        
        if not password:
            st.error("Passwort ist erforderlich!")
            return
        
        # Controller aufrufen
        success, role, message = self.controller.login_user(username.strip(), password)

        if success:
            # Session-State setzen
            st.session_state.logged_in = True
            st.session_state.username = username.strip()
            st.session_state.role = role

            st.success(f"Willkommen, {username}!")
            st.balloons()
            st.rerun()
        else:
            st.error(message)

    # --- 3.2.6 Register-Handler ---
    def _handle_register(self, username, password, confirm_password, role):
        """Verarbeitet Registrierungs-Anfrage"""

        # Client-seitige Validierung
        if not username.strip():
            st.error("Benutzername ist erforderlich!")
            return
        
        if len(username.strip()) < MIN_USERNAME_LENGTH:
            st.error(f"Benutzername muss mindestens {MIN_USERNAME_LENGTH} Zeichen lang sein!")
            return

        if not password:
            st.error("Passwort ist erforderlich!")
            return
            
        if len(password) < MIN_PASSWORD_LENGTH:
            st.error(f"Passwort muss mindestens {MIN_PASSWORD_LENGTH} Zeichen lang sein!")
            return

        if password != confirm_password:
            st.error("Passwörter stimmen nicht überein!")
            return
        

        # Controller aufrufen
        success, message = self.controller.register_user(username.strip(), password, role)

        if success:
            st.success(message)
            st.info("🎉 Sie können sich jetzt anmelden! Ihre Rolle wird vom Administrator zugewiesen.")
            st.balloons()
        else:
            st.error(message)