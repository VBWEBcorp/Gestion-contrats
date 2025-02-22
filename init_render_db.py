from app import app, db, Client, TypePrestation
from sqlalchemy import inspect

def init_db():
    print("=== DÉBUT INITIALISATION BASE DE DONNÉES ===")
    with app.app_context():
        try:
            # Vérifier la connexion
            connection = db.engine.connect()
            print("✓ Connexion à la base de données établie")
            connection.close()

            # Créer les tables
            db.create_all()
            print("✓ Tables créées avec succès")

            # Vérifier les tables créées
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Tables disponibles: {tables}")

            # Ajouter les types de prestation par défaut si la table est vide
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
            else:
                print("✓ Types de prestation déjà existants")
            
            print("=== INITIALISATION TERMINÉE AVEC SUCCÈS ===")
            return True

        except Exception as e:
            print(f"✗ ERREUR lors de l'initialisation: {str(e)}")
            if 'db' in locals():
                db.session.rollback()
            raise

if __name__ == '__main__':
    init_db()
