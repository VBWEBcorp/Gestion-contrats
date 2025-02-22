from datetime import datetime
from models import Client
from extensions import db

def check_expired_contracts(app):
    """Vérifie et archive les contrats expirés"""
    with app.app_context():
        today = datetime.now().date()
        # Recherche des contrats actifs avec une date de fin passée
        expired_contracts = Client.query.filter(
            Client.date_fin.isnot(None),
            Client.date_fin < today,
            Client.actif == True
        ).all()

        for client in expired_contracts:
            client.actif = False
            client.date_archivage = datetime.now()
        
        db.session.commit()
        return len(expired_contracts)
