from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from datetime import datetime
import os
from extensions import db
from models import Client, TypePrestation
from sqlalchemy import inspect, text
from apscheduler.schedulers.background import BackgroundScheduler
from tasks import check_expired_contracts
from dateutil.relativedelta import relativedelta
import csv
from openpyxl import Workbook
import io

app = Flask(__name__)

# Configuration de la base de données
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL environment variable is not set!')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'votre_clé_secrète_ici')

db.init_app(app)

def init_db():
    print("Début de l'initialisation de la base de données...")
    with app.app_context():
        try:
            # Créer toutes les tables
            db.create_all()
            print("Tables créées avec succès")

            # Vérifier si les types de prestation existent déjà
            if not TypePrestation.query.first():
                print("Ajout des types de prestation par défaut...")
                types = [
                    TypePrestation(nom="Mensuel"),
                    TypePrestation(nom="Trimestriel"),
                    TypePrestation(nom="Semestriel"),
                    TypePrestation(nom="Annuel")
                ]
                db.session.add_all(types)
                db.session.commit()
                print("Types de prestation ajoutés avec succès")
            else:
                print("Les types de prestation existent déjà")
        except Exception as e:
            print(f"Erreur lors de l'initialisation de la base de données: {str(e)}")
            db.session.rollback()
            raise

# Initialiser le planificateur de tâches
scheduler = BackgroundScheduler()
scheduler.add_job(func=lambda: check_expired_contracts(app), trigger="interval", hours=24)
scheduler.start()

@app.route('/')
def index():
    clients = Client.query.filter_by(actif=True).all()
    types_prestation = TypePrestation.query.all()
    total_mensuel = sum(client.montant for client in clients if client.frequence == 'mensuel')
    total_mensuel += sum(client.montant/12 for client in clients if client.frequence == 'annuel')
    return render_template('clients_actuels.html', 
                         clients=clients,
                         types_prestation=types_prestation,
                         total_mensuel=total_mensuel)

@app.route('/client', methods=['POST'])
def add_client():
    if request.method == 'POST':
        # Vérifier si c'est une mise à jour (PUT simulé)
        if '_method' in request.form and request.form['_method'] == 'PUT':
            client_id = request.form.get('client_id')
            if client_id:
                return update_client(int(client_id))
        
        # Sinon, créer un nouveau client
        client = Client(
            nom=request.form['nom'],
            prenom=request.form['prenom'],
            entreprise=request.form['entreprise'],
            montant=float(request.form['montant']),
            frequence=request.form['frequence'],
            date_debut=datetime.strptime(request.form['date_debut'], '%Y-%m-%d'),
            date_fin=datetime.strptime(request.form['date_fin'], '%Y-%m-%d') if request.form['date_fin'] else None
        )
        
        for prestation_id in request.form.getlist('prestations'):
            prestation = TypePrestation.query.get(int(prestation_id))
            if prestation:
                client.prestations.append(prestation)
        
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('index'))

def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    client.nom = request.form['nom']
    client.prenom = request.form['prenom']
    client.entreprise = request.form['entreprise']
    client.montant = float(request.form['montant'])
    client.frequence = request.form['frequence']
    client.date_debut = datetime.strptime(request.form['date_debut'], '%Y-%m-%d')
    client.date_fin = datetime.strptime(request.form['date_fin'], '%Y-%m-%d') if request.form['date_fin'] else None
    
    # Mettre à jour les prestations
    client.prestations = []
    for prestation_id in request.form.getlist('prestations'):
        prestation = TypePrestation.query.get(int(prestation_id))
        if prestation:
            client.prestations.append(prestation)
    
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/client/<int:client_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_client(client_id):
    client = Client.query.get_or_404(client_id)
    
    if request.method == 'GET':
        return jsonify({
            'nom': client.nom,
            'prenom': client.prenom,
            'entreprise': client.entreprise,
            'montant': client.montant,
            'frequence': client.frequence,
            'date_debut': client.date_debut.strftime('%Y-%m-%d'),
            'date_fin': client.date_fin.strftime('%Y-%m-%d') if client.date_fin else None,
            'prestations': [p.id for p in client.prestations],
            'commentaire': client.commentaire
        })
    
    elif request.method == 'DELETE':
        client.actif = False
        client.date_archivage = datetime.now()
        db.session.commit()
        return jsonify({'success': True})
    
    elif request.method == 'PUT':
        # Mettre à jour les données du client
        client.nom = request.form['nom']
        client.prenom = request.form['prenom']
        client.entreprise = request.form['entreprise']
        client.montant = float(request.form['montant'])
        client.frequence = request.form['frequence']
        client.date_debut = datetime.strptime(request.form['date_debut'], '%Y-%m-%d')
        client.date_fin = datetime.strptime(request.form['date_fin'], '%Y-%m-%d') if request.form['date_fin'] else None
        
        # Mettre à jour les prestations
        client.prestations = []
        for prestation_id in request.form.getlist('prestations'):
            prestation = TypePrestation.query.get(int(prestation_id))
            if prestation:
                client.prestations.append(prestation)
        
        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/client/<int:client_id>/comment', methods=['POST'])
def update_comment(client_id):
    client = Client.query.get_or_404(client_id)
    data = request.get_json()
    
    if not client or client.actif:
        return jsonify({'success': False, 'error': 'Client non trouvé ou non archivé'}), 404
    
    client.commentaire = data.get('commentaire', '')
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/client/<int:client_id>/restore', methods=['POST'])
def restore_client(client_id):
    client = Client.query.get_or_404(client_id)
    
    if not client or client.actif:
        return jsonify({'success': False, 'error': 'Client non trouvé ou déjà actif'}), 404
    
    client.actif = True
    client.date_archivage = None
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/historique')
def historique():
    # Récupérer tous les clients archivés, triés par date d'archivage décroissante
    clients = Client.query.filter_by(actif=False).order_by(Client.date_archivage.desc()).all()
    return render_template('historique.html', clients=clients)

@app.route('/statistiques')
def statistiques():
    # Récupérer les données actuelles
    clients = Client.query.filter_by(actif=True).all()
    
    # Calculer le CA mensuel
    ca_mensuel = sum(client.montant for client in clients if client.frequence == 'mensuel')
    ca_mensuel += sum(client.montant/12 for client in clients if client.frequence == 'annuel')
    
    # Nombre de contrats actifs
    nombre_contrats = len(clients)
    
    # Répartition des prestations
    prestations_count = {}
    for client in clients:
        for prestation in client.prestations:
            prestations_count[prestation.nom] = prestations_count.get(prestation.nom, 0) + 1
    
    prestations_labels = list(prestations_count.keys())
    prestations_data = list(prestations_count.values())
    
    # Données historiques (12 derniers mois)
    today = datetime.now()
    months = []
    ca_data = []
    contrats_data = []
    
    for i in range(11, -1, -1):
        date = today.replace(day=1) - relativedelta(months=i)
        next_month = date + relativedelta(months=1)
        
        # Clients actifs pour ce mois
        month_clients = Client.query.filter(
            db.or_(
                Client.actif == True,
                Client.date_archivage >= next_month
            ),
            db.or_(
                Client.date_fin.is_(None),
                Client.date_fin >= date
            ),
            Client.date_debut <= next_month
        ).all()
        
        # Calculer le CA pour ce mois
        month_ca = sum(c.montant for c in month_clients if c.frequence == 'mensuel')
        month_ca += sum(c.montant/12 for c in month_clients if c.frequence == 'annuel')
        
        months.append(date.strftime('%b %Y'))
        ca_data.append(round(month_ca, 2))
        contrats_data.append(len(month_clients))
    
    return render_template('statistiques.html',
                         ca_mensuel=ca_mensuel,
                         nombre_contrats=nombre_contrats,
                         prestations_labels=prestations_labels,
                         prestations_data=prestations_data,
                         ca_labels=months,
                         ca_data=ca_data,
                         contrats_labels=months,
                         contrats_data=contrats_data,
                         comparison_labels=months)

@app.route('/export-stats')
def export_stats():
    format = request.args.get('format', 'csv')
    
    # Récupérer les données
    clients = Client.query.filter_by(actif=True).all()
    prestations_count = {}
    for client in clients:
        for prestation in client.prestations:
            prestations_count[prestation.nom] = prestations_count.get(prestation.nom, 0) + 1
    
    # Créer le contenu CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # En-têtes
    writer.writerow(['Statistiques de Gestion des Contrats'])
    writer.writerow([])
    writer.writerow(['CA Mensuel', 'Nombre de Contrats Actifs'])
    
    # Données principales
    ca_mensuel = sum(client.montant for client in clients if client.frequence == 'mensuel')
    ca_mensuel += sum(client.montant/12 for client in clients if client.frequence == 'annuel')
    writer.writerow([f'{ca_mensuel:.2f} €', len(clients)])
    
    writer.writerow([])
    writer.writerow(['Répartition des Prestations'])
    writer.writerow(['Type de Prestation', 'Nombre de Contrats'])
    for prestation, count in prestations_count.items():
        writer.writerow([prestation, count])
    
    # Historique mensuel
    writer.writerow([])
    writer.writerow(['Historique Mensuel'])
    writer.writerow(['Mois', 'CA', 'Nombre de Contrats'])
    
    today = datetime.now()
    for i in range(11, -1, -1):
        date = today.replace(day=1) - relativedelta(months=i)
        next_month = date + relativedelta(months=1)
        
        month_clients = Client.query.filter(
            db.or_(
                Client.actif == True,
                Client.date_archivage >= next_month
            ),
            db.or_(
                Client.date_fin.is_(None),
                Client.date_fin >= date
            ),
            Client.date_debut <= next_month
        ).all()
        
        month_ca = sum(c.montant for c in month_clients if c.frequence == 'mensuel')
        month_ca += sum(c.montant/12 for c in month_clients if c.frequence == 'annuel')
        
        writer.writerow([
            date.strftime('%b %Y'),
            f'{month_ca:.2f} €',
            len(month_clients)
        ])
    
    # Préparer la réponse
    output.seek(0)
    if format == 'csv':
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=statistiques.csv'}
        )
    else:  # Excel
        # Convertir CSV en Excel
        workbook = Workbook()
        worksheet = workbook.active
        
        for row in csv.reader(io.StringIO(output.getvalue())):
            worksheet.append(row)
        
        excel_output = io.BytesIO()
        workbook.save(excel_output)
        excel_output.seek(0)
        
        return Response(
            excel_output.getvalue(),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': 'attachment; filename=statistiques.xlsx'}
        )

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
