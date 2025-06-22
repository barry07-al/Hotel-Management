# Hotel Management

## Design Stratégique

### Ubiquitous Language — Concepts métiers et définitions
- **Client** : Personne physique qui crée un compte pour utiliser les services de réservation de l'hôtel.
- **Identifiant client** : Code unique attribué automatiquement au client lors de la création de son compte.
- **Compte client** : Ensemble d'informations personnelles (nom, mail, téléphone) du client.
- **Portefeuille électronique** : Moyen de paiement associé à un client, contenant un solde en euros.
- **Devise** : Monnaie utilisée pour alimenter le portefeuille (Euro, Dollar, Livre, Yen, Franc).
- **Chambre** : Type d’hébergement proposé par l’hôtel (standard, supérieure, suite), avec des caractéristiques et un prix.
- **Reservation** : Action de bloquer une chambre pour une ou plusieurs nuits
- **Paiement partiel** : Premier versement de 50% effectué lors de la réservation.
- **Confirmation** : Paiement de la deuxième moitié pour valider la réservation.
- **Annulation** : Action d’annuler une réservation sans remboursement.

### Bounded Contexts — Schéma des contextes bornés
---------------------             ----------------------------             ---------------------------
|  Gestion Client   | <---------> |   Réservations Hôtel     | <---------> | Gestion Paiements       |
---------------------             ----------------------------             ---------------------------

### Context Map — Relations entre contextes
- **Gestion Client ↔ Réservations Hôtel** : relation de partage de données (le client est utilisé dans la réservation)
- **Réservations Hôtel ↔ Gestion Paiements** : relation de coordination (la réservation déclenche un paiement, et dépend du solde)

### Core / Supporting / Generic Domains
| Domaine           | Type       | Justification                                        |
|-------------------|------------|------------------------------------------------------|
| Réservations Hôtel| Core Domain| Cœur du métier, logique centrale                     |
| Gestion Paiements | Supporting | Nécessaire mais secondaire pour le métier principal  |
| Gestion Client    | Generic    | Composant commun, peu spécifique au métier de l’hôtel|

## Design tactique

### Entities
| Entité           | Attributs principaux       | Identifiant                                        |
|-------------------|------------|------------------------------------------------------|
| Client | nom, email (unique), téléphone, portefeuille | client_id (UUID)                     |
| Portefeuille | solde en euros, historique des transactions | lié à un client_id  |
| Chambre    | type (standard/supérieure/suite), équipements, prix | chambre_id (UUID ou nom de type) |
| Reservation | client, chambres, date de check-in, nombre de nuits, état, montant payé | reservation_id (UUID) |

### Value Objects
| Value Object           | Attributs       | Utilisé par                                        |
|-------------------|------------|------------------------------------------------------|
| Nom | nom | Client                     |
| Email | adresse email | Client  |
| Telephone    | numéro | Client |
| Devise | code devise (EUR, USD, ...) | Portefeuille |
| Montant | valeur et devise | Paiement |
| Date de reservation | date et nombre de nuits | Reservation |
| Statut de reservation | effectué / confirmé/ annulé | Reservation |
