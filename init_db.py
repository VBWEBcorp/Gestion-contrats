import os
from app import app, db, TypePrestation
from models import Client

def init_database():
    print("=== DÉBUT INITIALISATION BASE DE DONNÉES ===")
    
    with app.app_context():
        # Vérifier la connexion à la base de données
        try:
            # Tester la connexion
            db.engine.connect()
            print("✓ Connexion à la base de données réussie")
        except Exception as e:
            print(f"✗ ERREUR de connexion à la base de données: {str(e)}")
            raise

        try:
            # Supprimer toutes les tables existantes
            db.drop_all()
            print("✓ Anciennes tables supprimées")
            
            # Créer toutes les tables
            db.create_all()
            print("✓ Nouvelles tables créées")

            # Ajouter les types de prestation par défaut
            if not TypePrestation.query.first():
                types = [
                    TypePrestation(nom="Mensuel"),
                    TypePrestation(nom="Trimestriel"),
                    TypePrestation(nom="Semestriel"),
                    TypePrestation(nom="Annuel")
                ]
                db.session.add_all(types)
                db.session.commit()
                print("✓ Types de prestation ajoutés")
            
            print("=== INITIALISATION TERMINÉE AVEC SUCCÈS ===")
            return True

        except Exception as e:
            print(f"✗ ERREUR lors de l'initialisation: {str(e)}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    init_database()
