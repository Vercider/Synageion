from abc import ABC, abstractmethod
import sqlite3
from config import DB_NAME

# ----- 1.0 DATEN-MODELL ----- 
# ---- 1.1 Hauptklasse des DB-Konnektors ----
class BaseModel(ABC):
    # --- 1.1.1 DB-Zuweisung ---
    def __init__(self):
        self.db_name = DB_NAME

    # --- 1.1.2 DB-Verbindung ---
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    # --- 1.1.3 ABST-Validierung ---
    @abstractmethod
    def validate(self):
        pass

    # --- 1.1.4 ABST-Speicherung ---
    @abstractmethod
    def save(self):
        pass