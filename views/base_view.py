import streamlit as st

# ----- 3.4 Basis-Ansicht -----
class BaseView:
    """Basis-View mit gemeinsamen Funktionen für alle Views"""

    # ---- 3.4.1 Header der Basis-Ansicht ----
    def render_header(self, title, subtitle=None):
        """Rendert Header mit Titel und Logout-Button"""
        col1, col2 = st.columns([4, 1])

        with col1:
            st.title(title)
            if subtitle:
                st.write(subtitle)

        with col2:
            if st.button("🚪 Abmelden", key="logout_button", help="Aus der Anwendung abmelden"):
                self._handle_logout()

    # ---- 3.4.2 Allgemeiner Logout-Handler ----
    def _handle_logout(self):
        """Behandelt Abmeldung für alle Views"""
        st.session_state.clear()
        st.success("Sie wurden erfolgreich abgemeldet!")
        st.rerun()

    # ---- 3.4.3 Benutzer-Informationen handeln ----
    def render_user_info(self):
        """Zeigt Benutzer-Informationen"""
        st.sidebar.write(f"**Angemeldet als:** {st.session_state.get('username', 'Unbekannt')}")
        st.sidebar.write(f"**Rolle:** {st.session_state.get('role', 'Unbekannt')}")

        if st.sidebar.button("🚪 Abmelden", key="sidebar_logout"):
            self._handle_logout()
