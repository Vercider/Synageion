from models.article_model import Article

# ----- 2.0 Controller -----
    # ---- 2.1 Einkauf-Controller ----
class PurchaseController:
    def __init__(self):
        """Initialisierung des Einkaufs-Controller"""
        pass
    
    # ---- 2.1.1 Alle Artikel abrufen ----
    def get_all_articles(self):
        """Holt alle Artikel und behandelt Fehler"""

        try:
            articles = Article.get_all()
            return articles, None
        except Exception as e:
            return [], str(e)
        
    # ---- 2.1.2 Neuen Artikel erstellen ----
    def create_article(self, article_data):
        """Erstellt einen neuen Artikel mit Validierung"""
        try:
            article = Article(
                article_number=article_data.get("article_number"),
                name=article_data.get("name"),
                description=article_data.get("description"),
                min_stock=article_data.get("min_stock", 0),
                status=article_data.get("status", "aktiv")
            )

            errors = article.validate()
            if errors:
                return False, errors # Validierungs-Fehler
            
            success = article.save()
            if success:
                return True, "Artikel erfolgreich erstellt"
            else:
                return False, ["Fehler beim Speichern"]
        
        except ValueError as e:
            # Spezifischer Fehler (z.B. doppelte Artikelnummer)
            return False, [str(e)]
            # Allgemeiner Fehler
        except Exception as e:
            return False, [f"Unerwarteter Fehler: {str(e)}"]
        
    # ---- 2.1.3 Artikel aktualisieren ----
    def update_article(self, article_id, article_data):
        """Aktualisiert einen bestehenden Artikel"""
        try:
            # Artikel aus der Datenbank laden
            article = Article.find_by_id(article_id)
            if not article:
                return False, ["Artikel nicht gefunden"]
            
            # Neue Daten setzen
            article.article_number = article_data.get("article_number", article.article_number)
            article.name = article_data.get("name", article.name)
            article.description = article_data.get("description", article.description)
            article.min_stock = article_data.get("min_stock", article.min_stock)
            article.status = article_data.get("status", article.status)

            # Validierung
            errors = article.validate()
            if errors:
                return False, errors
            
            # Speicherung
            success = article.save()
            if success:
                return True, "Artikel erfolgreich aktualisiert"
            else:
                return False, ["Fehler beim Aktualisieren"]
        
        except ValueError as e:
            return False, [str(e)]
        except Exception as e:
            return False, [f"Unerwarteter Fehler: {str(e)}"]
            
    # ---- 2.1.4 Artikel löschen ----
    def delete_article(self, article_id):
        """Löscht einen Artikel (Status auf "inaktiv" setzen)"""
        try:
            article = Article.find_by_id(article_id)
            if not article:
                return False, ["Artikel nicht gefunden"]
            
            article.status = "inaktiv"

            success = article.save()
            if success:
                return True, "Artikel erfolgreich deaktiviert"
            else:
                return False, ["Fehler beim Deaktivieren"]
            
        except Exception as e:
            return False, [f"Unerwarteter Fehler: {str(e)}"]
        
    # ---- 2.1.5 Nur aktive Artikel aufrufen ----
    def get_active_articles(self):
        """Holt nur Artikel mit Status 'aktiv'"""
        try:
            all_articles = Article.get_all()
            active_articles = [article for article in all_articles if article.status == "aktiv"]
            return active_articles, None
        except Exception as e:
            return [], str(e)
            

            
