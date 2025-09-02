import streamlit as st
from views.base_view import BaseView

# ----- 3.6 VERTRIEBS-VIEW -----
class SalesView(BaseView):
    # ---- 3.6.1 Vertriebs-View Initialisierung ----
    def __init__(self):
        """Initialisierung der Sales View"""
        # self.controller = SalesController()
        pass
    
    # ---- 3.6.2 Hauptansicht rendern ----
    def render(self):
        """Rendert das komplette Vertriebler-Dashboard"""

        # Header mit Logout
        self.render_header("💼 Vertrieb - Kundenmanagement",
                           f"Willkommen, {st.session_state.username}!")
        
        # Sidebar mit Logout
        self.render_user_info()

        # Tab-Navigation
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Kundenaufträge",
            "👥 Kundenstamm",
            "📊 Verkaufsstatistik",
            "🎯 Angebote"
        ])

        with tab1:
            self._render_customer_orders()

        with tab2:
            self._render_customer_management()

        with tab3:
            self._render_sales_statistics()

        with tab4:
            self._render_quotations()

    # ---- 3.6.3 Kundenaufträge ----
    def _render_customer_orders(self):
        st.subheader("📋 Kundenaufträge")

        # Placeholder für Aufträge-Funktionalität
        st.info("🚧 **Kommende Funktionen:**")
        st.write("- 📝 Neue Kundenaufträge erstellen")
        st.write("- 📋 Aufträge verwalten und bearbeiten")
        st.write("- 🚚 Lieferstatus verfolgen")
        st.write("- 💰 Rechnungsausstellung")
        st.write("- 📊 Auftrags-Pipeline")

        # Demo-Auftrags-Interface
        with st.expander("🔮 Vorschau: Neuer Kundenauftrag"):
            col1, col2 = st.columns(2)

            with col1:
                st.selectbox("Kunde", ["Müller GmbH", "Schmidt AG", "Weber & Co"], disabled=True)
                st.date_input("Auftragsdatum", disabled=True)
                st.selectbox("Artikel", ["Laptop Dell XPS", "Monitor Samsung", "Drucker HP", "Tablet iPad"], disabled=True)

            with col2:
                st.number_input("Menge", min_value=1, disabled=True)
                st.number_input("Einzelpreis (€)", disabled=True)
                st.selectbox("Liefertermin", ["Sofort", "1 Woche", "2 Wochen"], disabled=True)

            st.text_area("Bemerkungen", disabled=True)
            st.button("Auftrag erstellen", disabled=True, help="Wird mit SalesController implementiert")

        # Demo-Auftragsliste
        with st.expander("🔮 Vorschau: Aktuelle Aufträge"):
            demo_orders = {
                "Auftrag-Nr": ["SO-2024-001", "SO-2024-002", "SO-2024-003", "SO-2024-004"],
                "Kunde": ["Müller GmbH", "Schmidt AG", "Weber & Co", "Klein KG"],
                "Artikel": ["Laptop Dell XPS", "Monitor Samsung" , "Drucker HP", "Tablet iPad"],
                "Wert": ["€2.450", "€890", "€1.200", "€650"],
                "Status": ["Offen", "In Bearbeitung", "Geliefert", "Rechnung erstellt"]
            }
            st.dataframe(demo_orders, use_container_width=True)

    # ---- 3.6.4 Kundenstamm ----
    def _render_customer_management(self):
        """Kundenstamm verwalten"""
        st.subheader("👥 Kundenstamm")

        st.info("🚧 **Kommende Funktionen:**")
        st.write("- 👤 Neue Kunden anlegen")
        st.write("- ✏️ Kundendaten bearbeiten")
        st.write("- 📞 Kontakthistorie verwalten")
        st.write("- 💰 Umsatzhistorie anzeigen")
        st.write("- 🏷️ Kundenklassifizierung (A/B/C)")

        # Demo-Kunde anlegen
        with st.expander("🔮 Vorschau: Neuen Kunden anlegen"):
            col1, col2 = st.columns(2)

            with col1:
                st.text_input("Firmenname", disabled=True)
                st.time_input("Ansprechpartner", disabled=True)
                st.time_input("E-Mail", disabled=True)
                st.time_input("Telefon", disabled=True)

            with col2:
                st.text_input("Straße", disabled=True)
                st.text_input("PLZ", disabled=True)
                st.text_input("Ort", disabled=True)
                st.selectbox("Kundenklasse", ["A-Kunde", "B-Kunde", "C-Kunde"], disabled=True)

            st.button("Kunden anlegen", disabled=True)

        # Demo-Kundenliste
        with st.expander("🔮 Vorschau: Kundenliste"):
            demo_customers = {
                "Kunde-Nr": ["K-001", "K-002", "K-003", "K-004"],
                "Firmenname": ["Müller GmbH", "Schmidt AG", "Weber & Co", "Klein KG"],
                "Ansprechpartner": ["Hans Müller", "Anna Schmidt", "Tom Weber", "Lisa Klein"],
                "Umsatz (YTD)": ["€45.600", "€23.400", "€78.900", "€12.300"],
                "Klasse": ["A-Kunde", "B-Kunde", "A-Kunde", "C-Kunde"]
            }
            st.dataframe(demo_customers, use_container_width=True)

            st.write("**Kundenaktion (Demo):**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("📝 Kunde bearbeiten", disabled=True)
            with col2:
                st.button("📞 Kontakt hinzufügen", disabled=True)
            with col3:
                st.button("📊 Umsatz anzeigen", disabled=True)

    # ---- 3.6.5 Verkaufsstatistik ----
    def _render_sales_statistics(self):
        """Verkaufsstatistiken und KPIs anzeigen"""
        st.subheader("📊 Verkaufsstatistik")

        st.info("🚧 **Kommende Funktionen:**")
        st.write("- 💰 Umsatz-Dashboard")
        st.write("- 📈 Verkaufstrends analysieren")
        st.write("- 🎯 Zielerreichung verfolgen")
        st.write("- 👥 Kunden-Rankings")
        st.write("- 📦 Produkt-Performance")

        # Demo-KPIs
        with st.expander("🔮 Vorschau: Verkaufs-Dashboard"):
            st.write("**Aktuelle Periode (Demo-Daten):**")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Umsatz (Monat)", "€156.789", "+€12.456")
            with col2:
                st.metric("Aufträge", "47", "+8")
            with col3:
                st.metric("Neukunden", "6", "+2")
            with col4:
                st.metric("Zielerreichung", "87%", "+5%")

            # Demo-Chart
            st.write("**Umsatzentwicklung (Demo-Daten):**")
            chart_data = {
                "Monat": ["Jan", "Feb", "Mar", "Apr", "Mai"],
                "Umsatz": [145000, 167000, 134000, 189000, 156000],
                "Ziel": [150000, 150000, 150000, 150000, 150000]
            }
            st.line_chart(chart_data, x="Monat")

            # Top-Kunden
            st.write("**Top-Kunden (Demo):**")
            top_customers = {
                "Rang": [1, 2, 3, 4, 5],
                "Kunde": ["Weber & Co", "Müller GmbH", "Schmidt AG", "Klein AG", "Groß Industries"],
                "Umsatz": ["€78.900", "€45.600", "€23.400", "€12.300", "€8.900"]
            }
            st.dataframe(top_customers, use_container_width=True)

    # ---- 3.6.6 Angebote ----
    def _render_quotations(self):
        """Angebote erstellen und verwalten"""
        st.subheader("🎯 Angebote")

        st.info("🚧 **Kommende Funktionen:**")
        st.write("- 📝 Angebote erstellen")
        st.write("- 📧 Angebote versenden")
        st.write("- 📊 Angebots-Erfolgsquote")
        st.write("- ⏰ Nachfass-Erinnerungen")
        st.write("- 💰 Preiskalkulation")

        # Demo-Angebot erstellen
        with st.expander("🔮 Vorschau: Neues Angebot"):
            col1, col2 = st.columns(2)

            with col1:
                st.selectbox("Kunde", ["Müller GmbH", "Schmidt AG", "Interessent XY"], disabled=True)
                st.text_input("Angebot-Titel", disabled=True)
                st.date_input("Gültig bis", disabled=True)

            with col2:
                st.selectbox("Artikel-Paket", ["Office-Paket", "IT-Grundausstattung"], disabled=True)
                st.number_input("Rabatt (%)", disabled=True)
                st.selectbox("Zahlungsbedingungen", ["30 Tage", "Sofort", "14 Tage"], disabled=True)

            st.text_area("Angebots-Text", disabled=True)
            st.button("Angebot erstellen", disabled=True)

        # Demo-Angebotsliste
        with st.expander("🔮 Vorschau: Offene Angebote"):
            demo_quotes = {
                "Angebot-Nr": ["AN-2024-001", "AN-2024-002", "AN-2024-003"],
                "Kunde": ["Müller GmbH", "Interessent ABC", "Schmidt AG"],
                "Titel": ["Office-Ausstattung", "IT-Modernisierung", "Drucker-Upgrade"],
                "Wert": ["€5.600", "€12.400", "€2.300"],
                "Status": ["Offen", "Nachgefasst", "Angenommen"]
            }
            st.dataframe(demo_quotes, use_container_width=True)

            st.write("**Angebots-Aktionen (Demo):**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.button("📧 Versenden", disabled=True)
            with col2:
                st.button("📞 Nachfassen", disabled=True)
            with col3:
                st.button("✏️ Bearbeiten", disabled=True)
            with col4:
                st.button("✅ Abschließen", disabled=True)
                           
