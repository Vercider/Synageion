from models.user_model import User
from constants import ACTIVE_ROLES

# ----- 2.3 ADMIN-Controller -----
# ---- 2.3.1 Admin-Controller Initialisierung ----
class AdminController:
    def __init__(self):
        pass

    # ---- 2.3.2 Alle User abrufen ----
    def get_all_users(self):
        """Holt alle User mit Rollen und behandelt Fehler"""
        try:
            users = User.get_all_with_roles()
            return users, None # Erfolg: User + kein Fehler
        except Exception as e:
            return [], str(e) # Fehler: Leere Liste + Fehlermeldung
        
    # ---- 2.3.3 Wartende User abrufen ----
    def get_waiting_users(self):
        """Holt nur User mit Rolle 'Wartend'"""
        try:
            waiting_users = User.get_waiting_users()
            return waiting_users, None
        except Exception as e:
            return [], str(e)
        
    # ---- 2.3.4 User Rolle ändern ----
    def change_user_role(self, user_id, new_role):
        """Ändert die Rolle eines Users"""
        try:
            if new_role not in ACTIVE_ROLES:
                return False, [f"Ungültige Rolle: {new_role}"]
            
            all_users, error = self.get_all_users()
            if error:
                return False, [f"Fehler beim Laden der User: {error}"]
            
            user = None
            for u in all_users:
                if u.user_id == user_id:
                    user = u
                    break
            
            if not user:
                return False, ["User nicht gefunden"]
            
            old_role = user.role_name
            user.update_role(new_role)

            return True, f"Rolle von '{old_role}' zu '{new_role}' geändert'"
        
        except ValueError as e:
            return False, [str(e)]
        except Exception as e:
            return False, [f"Unerwarteter Fehler: {str(e)}"]
        
    # ---- 2.3.5 User "deaktivieren" ----
    def deactivate_user(self, user_id):
        """Setzt User-Rolle auf 'Wartend' (SOFT-DELETE)"""
        try:
            return self.change_user_role(user_id, "Wartend")
        except Exception as e:
            return False, [f"Fehler beim Deaktivieren: {str(e)}"]

    # ---- 2.3.6 Verfügbare Rollen abrufen ----
    def get_available_roles(self):
        """Gibt alle aktiven Rollen zurück"""
        return ACTIVE_ROLES, None
    
    # ---- 2.3.7 User-Statistiken ----
    def get_user_statistics(self):
        """Erstellt Statistiken über User Verteilung"""
        try:
            all_users, error = self.get_all_users()
            if error:
                return {}, error
            
            # Statistiken berechnen
            stats = {}
            for user in all_users:
                role = user.role_name
                stats[role] = stats.get(role, 0) + 1

            return stats, None
        
        except Exception as e:
            return {}, str(e)