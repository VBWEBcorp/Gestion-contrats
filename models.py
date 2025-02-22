from extensions import db
from datetime import datetime

class TypePrestation(db.Model):
    __tablename__ = 'type_prestation'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)

class Client(db.Model):
    __tablename__ = 'client'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    entreprise = db.Column(db.String(100))
    montant = db.Column(db.Float)
    frequence = db.Column(db.String(50))
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    actif = db.Column(db.Boolean, default=True)
    date_archivage = db.Column(db.Date)
    commentaire = db.Column(db.Text)

# Table d'association pour la relation many-to-many entre Client et TypePrestation
client_prestation = db.Table('client_prestation',
    db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True),
    db.Column('type_prestation_id', db.Integer, db.ForeignKey('type_prestation.id'), primary_key=True)
)
