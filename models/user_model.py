from models.base_model import BaseModel
import sqlite3
from config import DB_NAME


# ----- 1.4 USER-Daten-Modell -----
# ---- 1.4.1 User-Klassen-Initialisierung ----
class User(BaseModel):
    def __init__(self, user_id=None, username=None, hashed_password=None, role_id= None, role_name=None):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.hashed_password = hashed_password
        self.role_id = role_id
        self.role_name = role_name

    # ---- 1.4.2 User-Validierung ----
    def validate(self):
        """Validiert User-Daten"""
        errors = []
        if not self.username:
            errors.append("Benutzername ist erforderlich!")
        if not self.role_id:
            errors.append("Rolle ist erforderlich!")
        return errors

    # ---- 1.4.3 User-Daten-Änderung ----
    def save(self):
        """Speichert User-Änderungen(erstmal Nur Rollenänderung)"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("""
                    UPDATE users SET role_id = ? WHERE user_id = ?
                    """, (self.role_id, self.user_id))
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # ---- 1.4.4 Generierung aller User samt Rollen aus DB ----
    @classmethod
    def get_all_with_roles(cls):
        """Lädt alle User mit Rollen-Namen"""
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        try:
            c.execute("""
                    SELECT u.user_id, u.username, u.hashed_password, u.role_id, r.role_name
                    FROM users u
                    JOIN roles r ON u.role_id = r.role_id
                    ORDER BY u.username
                    """)
            results = c.fetchall()

            users = []
            for result in results:
                user = cls()
                (user.user_id, user.username, user.hashed_password,
                user.role_id, user.role_name) = result
                users.append(user)
            return users
        finally:
            conn.close()

    # ---- 1.4.5 Generierung aller User mit Rolle "Wartend" aus DB ----
    @classmethod
    def get_waiting_users(cls):
        """Lädt nur User mit der Rolle 'wartend'"""
        all_users = cls.get_all_with_roles()
        return [user for user in all_users if user.role_name == "Wartend"]

    # ---- 1.4.6 Änderung der Rolle eines Users ---- 
    def update_role(self, new_role_name):
        """Ändert die Rolle eines Users"""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            # Hole role_id für role_name
            c.execute("SELECT role_id FROM roles WHERE role_name = ?", (new_role_name,))
            result = c.fetchone()

            if not result:
                raise ValueError(f"Rolle '{new_role_name}' nicht gefunden")
            
            new_role_id = result[0]

            # Update user role
            c.execute("""
                    UPDATE users SET role_id = ? WHERE user_id = ?
                    """, (new_role_id, self.user_id))
            
            conn.commit()

            # Update object
            self.role_id = new_role_id
            self.role_name = new_role_name

            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()