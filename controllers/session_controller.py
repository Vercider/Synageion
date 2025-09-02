import streamlit as st

class SessionController:
    def check_timeout(self):
        """Prüft Session-Timeout nach 30 Minuten"""
        if 'login_time' not in st.session_state:
            return False
        
        import time
        elapsed = time.time() - st.session_state.login_time
        return elapsed > 1800  # 30 Minuten