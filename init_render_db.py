import os
from app import app, db, Client, TypePrestation
from sqlalchemy import inspect, text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    logger.info("=== DÉBUT INITIALISATION BASE DE DONNÉES ===")
    
    # Vérification de la variable d'environnement
    database_url = os.environ.get('DATABASE_URL')
    logger.info(f"DATABASE_URL: {database_url}")
    
    with app.app_context():
        try:
            # Test de connexion
            logger.info("Test de connexion à la base de données...")
            with db.engine.connect() as connection:
                # Vérifier si on peut exécuter une requête simple
                result = connection.execute(text("SELECT 1")).scalar()
                logger.info(f"Test de connexion réussi: {result == 1}")
            
            # Création des tables
            logger.info("Création des tables...")
            
            # Création manuelle des tables
            with db.engine.connect() as conn:
                # Table client
                logger.info("Création de la table client...")
                conn.execute(text("""
                DROP TABLE IF EXISTS client CASCADE;
                CREATE TABLE client (
                    id SERIAL PRIMARY KEY,
                    nom VARCHAR(100),
                    prenom VARCHAR(100),
                    entreprise VARCHAR(100),
                    montant FLOAT,
                    frequence VARCHAR(50),
                    date_debut DATE,
                    date_fin DATE,
                    actif BOOLEAN DEFAULT TRUE,
                    date_archivage DATE,
                    commentaire TEXT
                );
                """))
                
                # Table type_prestation
                logger.info("Création de la table type_prestation...")
                conn.execute(text("""
                DROP TABLE IF EXISTS type_prestation CASCADE;
                CREATE TABLE type_prestation (
                    id SERIAL PRIMARY KEY,
                    nom VARCHAR(50) UNIQUE NOT NULL
                );
                """))
                
                conn.commit()
                logger.info("✓ Tables créées avec succès")

            # Vérification des tables
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            logger.info(f"Tables disponibles: {tables}")

            # Ajout des types de prestation par défaut
            with db.engine.connect() as conn:
                logger.info("Ajout des types de prestation...")
                types = [
                    ("Mensuel",),
                    ("Trimestriel",),
                    ("Semestriel",),
                    ("Annuel",)
                ]
                conn.execute(text(
                    "INSERT INTO type_prestation (nom) VALUES (:nom)"
                ), [{"nom": type_name} for (type_name,) in types])
                conn.commit()
                logger.info("✓ Types de prestation ajoutés")
            
            logger.info("=== INITIALISATION TERMINÉE AVEC SUCCÈS ===")
            return True

        except Exception as e:
            logger.error(f"✗ ERREUR lors de l'initialisation: {str(e)}")
            if 'db' in locals():
                db.session.rollback()
            raise

if __name__ == '__main__':
    init_db()
