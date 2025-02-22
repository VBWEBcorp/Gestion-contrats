# Gestion de Contrats

Application de gestion de contrats permettant de gérer et suivre les contrats d'une organisation.

## Fonctionnalités Principales

### 1. Clients Actuels

Structure pour recenser les clients en cours :
- **Nom** (obligatoire)
- **Prénom** (obligatoire)
- **Entreprise** (facultatif)
- **Type(s) de prestation** :
  - Liste avec choix multiples :
    - SEO
    - Dev Web
    - Maintenance Dev Web
    - Maintenance Site Web
    - Site Internet
- **Montant** : en euros (€)
- **Fréquence** : mensuel, annuel
- **Date de début de contrat** : obligatoire
- **Date de fin de contrat** : facultatif

#### Fonctionnalité spécifique
- Transfert automatique vers l'historique à l'échéance du contrat
- Saisie manuelle possible d'anciens contrats

### 2. Historique des Clients

Structure pour archiver les contrats terminés :
- Nom et prénom du client
- Entreprise (facultatif)
- Type(s) de prestation
- Montant facturé (€)
- Fréquence (mensuel, annuel)
- Date de début et de fin de contrat
- Remarque ou commentaire (champ libre)

#### Fonctionnalité spécifique
- Transfert automatique des clients à la date de fin de contrat

### 3. Statistiques

#### Objectif
Suivre et comparer les entrées de chiffre d'affaires (CA) mensuelles.

#### Données affichées
1. CA mensuel à l'instant T
2. Évolution mensuelle du CA
3. Nombre de contrats actifs
4. Répartition des prestations en cours
5. Historique mensuel du CA

## Caractéristiques Techniques

### Modularité
- Champs modulables (types de prestation, fréquences)
- Interface avec accès rapide aux trois onglets
- Export des statistiques (CSV ou autre format)
- Gestion intuitive des données historiques et actuelles

### Design
- Interface épurée en blanc et bleu
- Design responsive avec menu burger pour mobile

## Installation

À venir...

## Utilisation

À venir...
