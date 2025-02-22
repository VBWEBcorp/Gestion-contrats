// Fonction pour éditer un client
function editClient(clientId) {
    fetch(`/client/${clientId}`)
        .then(response => response.json())
        .then(data => {
            const modal = new bootstrap.Modal(document.getElementById('addClientModal'));
            // Remplir le formulaire avec les données du client
            document.querySelector('[name="nom"]').value = data.nom;
            document.querySelector('[name="prenom"]').value = data.prenom;
            document.querySelector('[name="entreprise"]').value = data.entreprise || '';
            document.querySelector('[name="montant"]').value = data.montant;
            document.querySelector('[name="frequence"]').value = data.frequence;
            document.querySelector('[name="date_debut"]').value = data.date_debut;
            if (data.date_fin) {
                document.querySelector('[name="date_fin"]').value = data.date_fin;
            }
            
            // Cocher les prestations
            document.querySelectorAll('[name="prestations"]').forEach(checkbox => {
                checkbox.checked = data.prestations.includes(parseInt(checkbox.value));
            });
            
            // Modifier le titre du modal
            document.querySelector('.modal-title').textContent = 'Modifier le client';
            
            // Ajouter l'ID du client au formulaire
            document.getElementById('clientForm').dataset.clientId = clientId;
            
            modal.show();
        });
}

// Fonction pour supprimer un client
function deleteClient(clientId) {
    if (confirm('Êtes-vous sûr de vouloir archiver ce client ?')) {
        fetch(`/client/${clientId}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        });
    }
}

// Fonction pour ajouter un commentaire
function ajouterCommentaire(clientId) {
    const modal = new bootstrap.Modal(document.getElementById('commentaireEditModal'));
    document.getElementById('commentaireForm').dataset.clientId = clientId;
    document.querySelector('#commentaireEditModal .modal-title').textContent = 'Ajouter un commentaire';
    document.querySelector('#commentaireForm [name="commentaire"]').value = '';
    modal.show();
}

// Fonction pour modifier un commentaire
function modifierCommentaire(clientId) {
    fetch(`/client/${clientId}`)
        .then(response => response.json())
        .then(data => {
            const modal = new bootstrap.Modal(document.getElementById('commentaireEditModal'));
            document.getElementById('commentaireForm').dataset.clientId = clientId;
            document.querySelector('#commentaireEditModal .modal-title').textContent = 'Modifier le commentaire';
            document.querySelector('#commentaireForm [name="commentaire"]').value = data.commentaire || '';
            modal.show();
        });
}

// Gestionnaire de soumission du formulaire client
document.getElementById('clientForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const clientId = this.dataset.clientId;
    
    fetch(clientId ? `/client/${clientId}` : '/client', {
        method: clientId ? 'PUT' : 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        }
    });
});

// Gestionnaire de soumission du formulaire commentaire
document.getElementById('commentaireForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const clientId = this.dataset.clientId;
    
    fetch(`/client/${clientId}`, {
        method: 'PUT',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        }
    });
});
