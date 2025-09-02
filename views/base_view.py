import streamlit as st

# ----- 3.4 Basis-Ansicht -----
class BaseView:
    """Basis-View mit gemeinsamen Funktionen für alle Views"""

    # ---- 3.4.1 Header der Basis-Ansicht ----
    def render_header(self, title, subtitle=None):
        """Rendert Header OHNE Logout-Button"""
        # Vollbreiter Titel (keine Spalten)
        st.title(title)
        if subtitle:
            st.write(subtitle)
            

    # ---- 3.4.2 Allgemeiner Logout-Handler ----
    def _handle_logout(self):
        """Behandelt Abmeldung für alle Views"""
        st.session_state.clear()
        st.success("Sie wurden erfolgreich abgemeldet!")
        st.rerun()

    # ---- 3.4.3 Benutzer-Informationen handeln ----
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
        
        if st.sidebar.button("🚪 Abmelden", key="sidebar_logout"):
            self._handle_logout()
