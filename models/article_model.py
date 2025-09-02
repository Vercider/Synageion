from models.base_model import BaseModel
import sqlite3
from config import DB_NAME

# ---- 1.2 Artikel-DB-Klasse ---- 
class Article(BaseModel):
    # --- 1.2.1 Artikel-DB Konnektor über BaseModel ---
    def __init__(self,
                 article_id=None,
                 article_number=None,
                 name=None,
                 description=None,
                 min_stock=0,
                 status="aktiv"):
        super().__init__()
        self.article_id = article_id
        self.article_number = article_number
        self.name = name
        self.description = description
        self.min_stock = min_stock
        self.status = status

     # --- 1.2.2 Artikel-DB Validierung ---   
    def validate(self):
        """Überprüft, ob die Artikeldaten gültig sind"""
        errors = []
        if not self.article_number:
            errors.append("Artikelnummer ist erforderlich")
        if not self.name:
            errors.append("Artikelname ist erforderlich")
        if self.min_stock < 0:
            errors.append("Mindestbestand muss >= 0 sein")
        return errors
    
    # --- 1.2.3 Artikel-DB Speicherung ---
    def save(self):
        """Speicher den Artikel in der Datenbank"""
        conn = self.get_connection()
        c = conn.cursor()

        try:
            if self.article_id:
                c.execute("""
                          UPDATE articles
                          SET article_number=?, name=?, description=?, min_stock=?, status=?
                          WHERE article_id=?
                          """, 
                          (self.article_number,
                            self.name,
                            self.description,
                            self.min_stock,
                            self.status,
                            self.article_id))
            else:
                c.execute("""
                        INSERT INTO articles (article_number, name, description, min_stock, status)
                        VALUES (?,?,?,?,?)
                        """,
                        (self.article_number,
                        self.name,
                        self.description,
                        self.min_stock,
                        self.status))
                self.article_id = c.lastrowid
            conn.commit()
            return True
            
        except sqlite3.IntegrityError:
            raise ValueError("Artikelnummer existiert bereits")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # --- 1.2.4 Alle Artikel aus DB laden ---
    @classmethod
    def get_all(cls):
        """Alle Artikel aus DB laden"""
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        try:
            c.execute("""
                    SELECT article_id, article_number, name, description, min_stock, status
                    FROM articles
                    """)
            results = c.fetchall()

            articles = []
            for result in results:
                article = cls()
                (article.article_id,
                 article.article_number,
                 article.name,
                 article.description,
                 article.min_stock,
                 article.status) = result
                articles.append(article)

            return articles
        finally:
            conn.close()

    # --- 1.2.5 Artikel nach Artikel-ID finden ---
    @classmethod
    def find_by_id(cls, article_id):
        """Sucht einen Artikel anhand ihrer ID"""
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        try:
            c.execute("""
                    SELECT article_id, article_number, name, description, min_stock, status
                    FROM articles
                    WHERE article_id = ?
                    """, (article_id,)) # Komma wichtig für Tupel!
            result = c.fetchone()

            if result:
                article = cls()
                (article.article_id,
                 article.article_number,
                 article.name,
                 article.description,
                 article.min_stock,
                 article.status) = result
                return article
            
            return None
        finally:
            conn.close()

