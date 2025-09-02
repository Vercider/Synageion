import streamlit as st
from controllers.admin_controller import AdminController
from constants import ACTIVE_ROLES

# ----- 3.3 ADMIN-View -----
class AdminView:
    # ---- 3.3.1 Admin-View-Initialisierung ----
    def __init__(self):
        """Initialisierung der AdminView"""
        self.controller = AdminController()

    # ---- 3.3.2 Hauptansicht rendern ----
    def render(self):
        """Rendert das komplette Admin-Dashboard"""
        st.title("🛡️ Administrator Dashboard")
        st.write(f"Willkommen im Admin-Panel, {st.session_state.username}!")

        # Tab-Navigation erstellen
        tab1, tab2, tab3, tab4 = st.tabs([
            "👥 User-Verwaltung", 
            "⏳ Wartende User", 
            "📊 Statistiken",
            "🔧 System"
        ])

        # Tab-Inhalte rendern
        with tab1:
            self._render_user_management()

        with tab2:
            self._render_waiting_users()

        with tab3:
            self._render_statistics()

        with tab4:
            self._render_system_info()

    # ---- 3.3.3 Wartende User anzeigen ----
    def _render_waiting_users(self):
        """Zeigt User mit Rolle 'Wartend' zur Freischaltung"""
        st.subheader("⏳ Wartende User freischalten")

        # Wartende User vom Controller holen
        waiting_users, error = self.controller.get_waiting_users()

        if error:
            st.error(f"Fehler beim Laden wartender User: {error}")
            return
        
        if not waiting_users:
            st.success("🎉 Keine User warten auf Freischaltung!")
            st.info("Alle registrierten User haben bereits eine aktive Rolle.")
            return
        
        # Wartende User anzeigen
        st.warning(f"📋 {len(waiting_users)} User warten auf Freischaltung:")

        # Für jeden wartenden User ein Freischaltungs-Formular
        for user in waiting_users:
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                st.write(f"**👤 {user.username}**")
                st.caption(f"User-ID: {user.user_id}")

            with col2:
                # Rolle-Auswahl für diesen User
                selected_role = st.selectbox(
                    "Neue Rolle zuweisen:",
                    options=ACTIVE_ROLES,
                    key=f"role_select_{user.user_id}",
                    help=f"Wählen Sie eine aktive Rolle für {user.username}"
                )

            with col3:
                # Freischalten-Button
                if st.button(
                    "✅ Freischalten",
                    key=f"activate_{user.user_id}",
                    type="primary"
                ):
                    self._handle_user_activation(user.user_id, user.username, selected_role)

            st.divider()  # Trennung zwischen Usern

    # ---- 3.3.4 User-Freischaltung verarbeiten ----
    def _handle_user_activation(self, user_id, username, new_role):
        """Verarbeitet die Freischaltung eines Users"""

        # Controller aufrufen
        success, message = self.controller.change_user_role(user_id, new_role)

        if success:
            st.success(f"🎉 {username} wurde als '{new_role}' freigeschaltet!")
            st.balloons()
            st.rerun()
        else:
            if isinstance(message, list):
                for error in message:
                    st.error(error)
            else:
                st.error(message)

    # ---- 3.3.5 User-Verwaltung anzeigen ----
    def _render_user_management(self):
        """Zeigt alle User mit Rollen-Management"""
        st.subheader("👥 User-Verwaltung")

        # Alle User vom Controller holen
        all_users, error = self.controller.get_all_users()

        if error:
            st.error(f"Fehler beim Laden der User: {error}")
            return
        
        # Filter-Option
        col1, col2 = st.columns(2)

        with col1:
            # Filter nach Rolle
            filter_role = st.selectbox(
                "Filter nach Rolle:",
                options=["Alle"] + ["Administrator","Einkäufer", "Logistiker", "Vertriebler", "Wartend"],
                help="Zeige User mit bestimmter Rolle"
            )

        with col2:
            # Suchfeld
            search_term = st.text_input(
                "User suchen:",
                placeholder="Benutzername eingeben...",
                help="Suche nach Benutzername"
            )

        # User filtern
        filtered_users = all_users

        # Nach Rollen filtern
        if filter_role != "Alle":
            filtered_users = [user for user in filtered_users if user.role_name == filter_role]

        # Nach Suchbegriff filtern
        if search_term:
            filtered_users = [user for user in filtered_users if search_term.lower() in user.username.lower()]
        
        # Gefilterte User anzeigen
        st.write(f"**Gefundene User: {len(filtered_users)}**")

        if not filtered_users:
            st.info("Keine User entsprechen den Filterkriterien")
            return
        
        # User-Tabelle
        for user in filtered_users:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

                with col1:
                    st.write(f"**👤 {user.username}**")
                    st.caption(f"ID: {user.user_id}")

                with col2:
                    # Aktuelle Rolle anzeigen
                    if user.role_name == "Wartend":
                        st.warning(f"🔄 {user.role_name}")
                    elif user.role_name == "Administrator":
                        st.error(f"🛡️ {user.role_name}")
                    else:
                        st.success(f"✅ {user.role_name}")

                with col3:
                    # Rolle ändern (nur wenn nicht Admin und nicht der eigene Account)
                    if (user.role_name != "Administrator" and user.username != st.session_state.username):
                        new_role = st.selectbox(
                            "Rolle ändern:",
                            options=ACTIVE_ROLES,
                            index=ACTIVE_ROLES.index(user.role_name) if user.role_name in ACTIVE_ROLES else 0,
                            key=f"change_role_{user.user_id}",
                            help=f"Rolle für {user.username} ändern"
                        )

                        if new_role != user.role_name:
                            if st.button(
                                "💾 Ändern",
                                key=f"save_role_{user.user_id}",
                                help="Rolle speichern"
                            ):
                                self._handle_role_change(user.user_id, user.username, new_role)
                
                with col4:
                    # Deaktivieren-Button (nur wenn nicht Admin und nicht der eigene Account)
                    if (user.role_name != "Administrator" and
                        user.username != st.session_state.username and
                        user.role_name != "Wartend"):

                        if st.button(
                            "❌",
                            key=f"deactivate_{user.user_id}",
                            help=f"{user.username} deaktivieren",
                            type="secondary"
                        ):
                            self._handle_user_deactivation(user.user_id, user.username)

                st.divider()

    # ---- 3.3.6 Rollen-Änderung verarbeiten ----
    def _handle_role_change(self, user_id, username, new_role):
        """Verarbeitet Rollen-Änderung eines Users"""
        success, message = self.controller.change_user_role(user_id, new_role)

        if success:
            st.success(f"✅ Rolle von {username} wurde auf '{new_role}' geändert!")
            st.rerun()
        else:
            if isinstance(message, list):
                for error in message:
                    st.error(error)
            else:
                st.error(message)
    
    # ---- 3.3.7 User-Deaktivierung verarbeiten ----
    def _handle_user_deactivation(self, user_id, username):
        """Verarbeitet die Deaktivierung eines Users"""
        success, message = self.controller.deactivate_user(user_id)

        if success:
            st.warning(f"⚠️ {username} wurde deaktiviert!")
            st.rerun()
        else:
            if isinstance(message, list):
                for error in message:
                    st.error(error)
            else:
                st.error(message)
                        
