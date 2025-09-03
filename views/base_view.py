import streamlit as st
from controllers.auth_controller import AuthController

# ----- 3.4 Basis-Ansicht -----
class BaseView:
    """Basis-View mit gemeinsamen Funktionen für alle Views"""

    # ---- 3.4.1 BaseView Initialisierung ----
    def __init__(self):
        """Initialisierung mit Auth-Controller für PW-Reset"""
        self.auth_controller = AuthController()

    # ---- 3.4.2 Header der Basis-Ansicht ----
    def render_header(self, title, subtitle=None):
        """Rendert Header OHNE Logout-Button"""
        # Vollbreiter Titel (keine Spalten)
        st.title(title)
        if subtitle:
            st.write(subtitle)
            

    # ---- 3.4.3 Allgemeiner Logout-Handler ----
    def _handle_logout(self):
        """Behandelt Abmeldung für alle Views"""
        st.session_state.clear()
        st.success("Sie wurden erfolgreich abgemeldet!")
        st.rerun()

    # ---- 3.4.4 Benutzer-Informationen handeln ----
    def render_user_info(self):
        """Zeigt Benutzer-Informationen inkl. Session-Info"""
        st.sidebar.write(f"**Angemeldet als:** {st.session_state.get('username', 'Unbekannt')}")
        st.sidebar.write(f"**Rolle:** {st.session_state.get('role', 'Unbekannt')}")
        
        # ✅ Session-Zeit anzeigen (optional)
        if 'login_time' in st.session_state:
            import time
            elapsed = int(time.time() - st.session_state.login_time)
            minutes = elapsed // 60
            st.sidebar.caption(f"⏰ Angemeldet seit: {minutes} Min")
            
            # Warnung bei bald ablaufender Session
            if elapsed > 1500:  # 25 Minuten (5 Min vor Ablauf)
                st.sidebar.warning("⚠️ Session läuft bald ab!")

        if st.sidebar.button("🔑 Passwort ändern", key="change_password_btn"):
            st.session_state.show_password_modal = True

        if st.session_state.get("show_password_modal", False):
            self._render_password_change_modal()
        
        if st.sidebar.button("🚪 Abmelden", key="sidebar_logout"):
            self._handle_logout()

    # ---- 3.4.5 Passwort-Modal rendern ----
    def _render_password_change_modal(self):
        """Zeigt Passwort-Änderungs-Dialog in Sidebar"""

        with st.sidebar.expander("🔑 Passwort ändern", expanded=True):

            with st.form("password_change_form"):
                st.write("**Passwort ändern:**")

                current_password = st.text_input(
                    "Aktuelles Passwort:",
                    type="password",
                    key="current_pwd"
                )

                new_password = st.text_input(
                    "Neues Passwort:",
                    type="password",
                    key="new_pwd",
                    help="Mindestens 6 Zeichen"
                )

                confirm_password = st.text_input(
                    "Passwort bestätigen:",
                    type="password",
                    key="confirm_pwd"
                )

                col1, col2 = st.columns(2)
                
                with col1:
                    submit = st.form_submit_button("💾 Ändern", type="primary")
                with col2:
                    cancel = st.form_submit_button("❌ Abbrechen")

                if submit:
                    self._handle_password_change(
                        current_password,
                        new_password,
                        confirm_password
                    )
                
                if cancel:
                    st.session_state.show_password_modal = False
                    st.rerun()

    # ---- 3.4.6 Passwort-Änderung verarbeiten ----
    def _handle_password_change(self, current_pwd, new_pwd, confirm_pwd):
        """Verarbeitet Passwort-Änderung"""

        username = st.session_state.get("username")

        success, message = self.auth_controller.change_password(
            username, current_pwd, new_pwd, confirm_pwd
        )

        if success:
            st.success(message)
            st.balloons()
            st.session_state.show_password_modal = False
            st.info("💡 Passwort erfolgreich geändert!")
        
        else:
            st.error(message)


