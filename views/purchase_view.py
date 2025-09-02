import streamlit as st
from controllers.purchase_controller import PurchaseController

# ----- 3.0 VIEWS -----
# ---- 3.1 Einkaufs-View ----
class PurchaseView:
    # --- 3.1.1 Einkaufs-View Initialisierung ---
    def __init__(self):
        """Initialisierung der Purchase View"""
        self.controller = PurchaseController()

    # --- 3.1.2 Hauptansicht rendern ---
    def render(self):
        """Rendert das komplette Einkäufer-Dashboard"""
        st.title("🛒 Einkäufer Dashboard")
        st.write(f"Willkommen im Einkaufsmanagement, {st.session_state.username}!")

        tab1, tab2, tab3 = st.tabs(["📦 Artikelübersicht","➕ Neuer Artikel anlegen","✏️ Artikel bearbeiten"])

        with tab1:
            self._render_article_list()

        with tab2:
            self._render_new_article_form()

        with tab3:
            self._render_edit_article_form()

    # --- 3.1.3 Artikelübersicht anzeigen ---
    def _render_article_list(self):
        """Zeigt alle Artikel in einer Tabelle an"""
        st.subheader("Artikelübersicht")

        # Filter für aktive/alle Artikel
        show_inactive = st.checkbox("Inaktive Artikel anzeigen", value=False)

        # Artikel vom Controller holen
        if show_inactive:
            articles, error = self.controller.get_all_articles()
        else:
            articles, error = self.controller.get_active_articles()

        # Fehlerbehandlung
        if error:
            st.error(f"Fehler beim Laden der Artikel: {error}")
            return
        
        # Artikel anzeigen
        if articles:
            # DataFrame für Streamlit erstellen
            articles_dict = {
                "ID": [a.article_id for a in articles],
                "Artikelnummer": [a.article_number for a in articles],
                "Name": [a.name for a in articles],
                "Beschreibung": [a.description for a in articles],
                "Mindestbestand": [a.min_stock for a in articles],
                "Status": [a.status for a in articles]
            }
            st.dataframe(articles_dict, use_container_width=True)
        else:
            st.info("Keine Artikel vorhanden")

    # --- 3.1.4 Neues Artikel Formular ---
    def _render_new_article_form(self):
        """Zeigt Formular zum Erstellen neuer Artikel"""
        st.subheader("Neuen Artikel anlegen")

        # Streamlit Form für bessere UX
        with st.form("new_article_form", clear_on_submit=True):
            # Eingabefelder
            article_number = st.text_input(
                "Artikelnummer *",
                placeholder="z.B. ART0001",
                help="Eindeutige Artikelnummer"
            )

            name = st.text_input(
                "Artikelname *",
                placeholder="z.B. Business Laptop",
                help="Bezeichnung des Artikels"
            )

            description = st.text_area(
                "Beschreibung",
                placeholder="Detaillierte Beschreibung des Artikels...",
                help="Optionale Beschreibung"
            )

            col1, col2 = st.columns(2) # 2 Spalten

            with col1:
                min_stock = st.number_input(
                    "Mindestbestand *",
                    min_value=0,
                    value=0,
                    help="Minimaler Lagerbestand"
                )

            with col2:
                status = st.selectbox(
                    "Status",
                    options=["aktiv","inaktiv"],
                    index=0, # "aktiv" als Standard
                    help="Artikelstatus"
                )

            # Submit Button
            submitted = st.form_submit_button("Artikel anlegen", type="primary")

            # Formular verarbeiten
            if submitted:
                self._handle_new_article_submission(
                    article_number,
                    name,
                    description,
                    min_stock,
                    status
                )

    # --- 3.1.5 Neuer Artikel Verarbeitung ---
    def _handle_new_article_submission(self, article_number, name, description, min_stock, status):
        """Verarbeitet die Eingaben des Neuer-Artikel-Formulars """

        # Client-seitige Validierung
        if not article_number.strip():
            st.error("Artikelnummer ist erforderlich!")
            return

        if not name.strip():
            st.error("Artikelname ist erforderlich!")
            return

        # Daten für Controller vorbereiten
        article_data = {
            "article_number": article_number.strip(),
            "name": name.strip(),
            "description": description.strip() if description else "",
            "min_stock": min_stock,
            "status": status
        }

        # Controller aufrufen
        success, message = self.controller.create_article(article_data)

        # Ergebnis anzeigen
        if success:
            st.success(message)
            st.balloons() # Erfolgs-Animation
            # Seite neu laden um Artikelliste zu aktualisieren
            st.rerun()
        else:
            # Fehlermeldung anzeigen (message ist Liste von Fehlern)
            for error in message:
                st.error(error)

    # --- 3.1.6 Artikel bearbeiten Formular ---
    def _render_edit_article_form(self):
        """Zeigt Formular zum Bearbeiten von Artikeln"""
        st.subheader("Artikel bearbeiten")

        # Artikel auswählen
        articles, error = self.controller.get_all_articles()

        if error:
            st.error(f"Fehler beim Laden der Artikel: {error}")
            return
        
        if not articles:
            st.info("Keine Artikel zum Bearbeiten vorhanden")
            return
        
        # Artikel-Auswahl-Dropdown-Menü
        article_options ={}
        for article in articles:
            display_name = f"{article.article_number} - {article.name} ({article.status})"
            article_options[display_name] = article.article_id

        selected_display = st.selectbox(
            "Artikel auswählen:",
            options=list(article_options.keys()),
            help="Wählen Sie den zu bearbeitenden Artikel"
        )

        if selected_display:
            selected_article_id = article_options[selected_display]
            self._render_edit_form(selected_article_id)

    # --- 3.1.7 Edit-Formular anzeigen ---
    def _render_edit_form(self, article_id):
        """Zeigt das Bearbeitungsformular für einen spezifischen Artikel"""

        # Artikel-Details laden
        article = None
        all_articles, _ = self.controller.get_all_articles()
        for a in all_articles:
            if a.article_id == article_id:
                article = a
                break
        if not article:
            st.error("Artikel nicht gefunden")
            return
        
        # Edit-Formular mit vorausgefüllten Werten
        with st.form(f"edit_article_form_{article_id}"):
            st.write("**Aktuelle Werte:**")

            # Eingabefelder mit aktuellen Werten
            article_number = st.text_input(
                "Artikelnummer *",
                value=article.article_number,
                help="Eindeutige Artikelnummer"
            )

            name = st.text_input(
                "Artikelname *",
                value=article.name,
                help="Bezeichnung des Artikels"
            )

            description = st.text_area(
                "Beschreibung",
                value=article.description or "",
                help="Optionale Beschreibung"
            )

            col1, col2 = st.columns(2)

            with col1:
                min_stock = st.number_input(
                    "Mindestbestand *",
                    min_value=0,
                    value=article.min_stock,
                    help="Minimaler Lagerbestand"
                )

            with col2:
                current_status = article.status
                status_index = 0 if current_status == "aktiv" else 1
                status = st.selectbox(
                    "Status",
                    options=["aktiv", "inaktiv"],
                    index=status_index,
                    help="Artikelstatus"
                )

            # Buttons in Spalten
            col1, col2, col3 = st.columns(3)

            with col1:
                update_submitted = st.form_submit_button(
                    "Änderungen speichern",
                    type="primary"
                )

            with col2:
                delete_submitted = st.form_submit_button(
                    "Artikel deaktivieren",
                    type="secondary"
                )

            # Formular verarbeiten
            if update_submitted:
                self._handle_edit_article_submission(
                    article_id, article_number, name, description, min_stock, status
                )

            if delete_submitted:
                self._handle_delete_article_submission(article_id)

    # --- 3.1.8 Edit-Artikel Verarbeitung ---
    def _handle_edit_article_submission(self, article_id, article_number, name, description, min_stock, status):
        """Verarbeitet die Bearbeitung eines Artikels"""

        # Client-seitige Validierung
        if not article_number.strip():
            st.error("Artikelnummer ist erforderlich!")
            return
        
        if not name.strip():
            st.error("Artikelname ist erforderlich!")
            return
        
        # Daten für Controller vorbereiten
        article_data = {
            "article_number": article_number.strip(),
            "name": name.strip(),
            "description": description.strip() if description else "",
            "min_stock": min_stock,
            "status": status
        }

        # Controller aufrufen
        success, message = self.controller.update_article(article_id, article_data)

        if success:
            st.success(message)
            st.balloons()
            st.rerun()
        else:
            for error in message:
                st.error(error)

    # --- 3.1.9 Delete-Artikel-Verarbeitung ---
    def _handle_delete_article_submission(self, article_id):
        """Verarbeitet die Deaktivierung eines Artikels"""

        # Sicherheitsabfrage
        st.warning("⚠️ Möchten Sie diesen Artikel wirklich deaktivieren?")

        # Controller aufrufen
        success, message = self.controller.delete_article(article_id)

        # Ergebnis anzeigen
        if success:
            st.success(message)
            st.rerun()
        else:
            for error in message:
                st.error(error)