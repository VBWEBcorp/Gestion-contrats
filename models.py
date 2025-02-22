from extensions import db
from datetime import datetime

class TypePrestation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    entreprise = db.Column(db.String(200))
    montant = db.Column(db.Float, nullable=False)
    frequence = db.Column(db.String(50), nullable=False)  # 'mensuel' ou 'annuel'
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime)
    prestations = db.relationship('TypePrestation', secondary='client_prestation')
    actif = db.Column(db.Boolean, default=True)
    # Champs pour l'historique
    date_archivage = db.Column(db.DateTime)
    commentaire = db.Column(db.Text)

# Table d'association pour la relation many-to-many entre Client et TypePrestation
client_prestation = db.Table('client_prestation',
    db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True),
    db.Column('type_prestation_id', db.Integer, db.ForeignKey('type_prestation.id'), primary_key=True)
)
