# XYZ Hotel Management

Ce projet est une implémentation d’un système de gestion d'hôtel en Python, basé sur les principes de Domain-Driven Design (DDD).

## Design Stratégique

### Ubiquitous Language — Concepts métiers et définitions
- **Client**	Personne effectuant des réservations et ayant un portefeuille.
- **Wallet**	Porte-monnaie numérique associé à un client, servant à payer les réservations.
- **Booking**	Réservation effectuée par un client pour un hébergement.
- **Payment**	Transaction représentant le paiement d’un montant lié à une réservation.
- **Amount**	Valeur monétaire (float + devise).
- **Currency**	Devise utilisée pour une transaction ou un solde de portefeuille.
- **HotelApplicationService**	Service applicatif orchestrant les actions entre bookings, wallets, etc.
- **BookingService**	Service de domaine responsable de la logique de réservation.
- **WalletService**	Service de domaine responsable des opérations monétaires.

### Bounded Contexts — Schéma des contextes bornés
```text
+----------------------+       +-----------------------+        +------------------------+
|   Booking Context    |<----->|     Hotel Context     |<-----> |     Wallet Context     |
+----------------------+       +-----------------------+        +------------------------+
| - Booking            |       | - HotelService        |        | - Wallet               |
| - BookingService     |       | - Orchestration       |        | - WalletService        |
| - BookingRepository  |       |                       |        | - Payments             |
+----------------------+       +-----------------------+        +------------------------+
```

### Context Map — Relations entre contextes

- **Hotel Context ↔ Booking Context : Partnership**
Le contexte "Hotel" dépend de "Booking" pour récupérer les réservations et les confirmer.
- **Hotel Context ↔ Wallet Context : Partnership / Customer-Supplier**
"Hotel" dépend de "Wallet" pour vérifier les soldes et initier des retraits. Le service wallet est "supplier".
- **Booking ↔ Wallet** : indirect — via "HotelService".

### Core / Supporting / Generic Domains

| Domaine           | Type       | Justification                                        |
|-------------------|------------|------------------------------------------------------|
| Booking | Core Domain| Cœur du métier, logique centrale                     |
| Wallet | Supporting | Supporte le domaine principal via les paiements, mais n'est pas central |
| HotelApplicationService    | Supporting    | Service applicatif d’orchestration, sans logique métier propre |
| Payments, Currency    | Generic    | Logique générique (transactions, conversions) réutilisable ailleurs. |

## Design tactique

### Entities

| Entité     | Contexte         | Identité clé         | Description                      |
|------------|------------------|----------------------|----------------------------------|
| Booking    | Booking          | booking_id           | Représente une réservation       |
| Client     | Client           | client_id/email   | Un utilisateur du système        |
| Wallet     | Wallet           | wallet_id | Portefeuille pour les paiements |
| Hotel      | Hotel |             | Lieu associé à une réservation   |
| PaymentTransaction    | Payments (optionnel)|       | Détail d’une transaction         |
| RoomType    | Booking|       | Type de chambre à louer         |

### Value Objects

| Value Object | Utilisé dans     | Description                             |
|--------------|------------------|-----------------------------------------|
| Email        | Client           | Adresse e-mail du client          |
| PhoneNumber  | Client           | Numéro de téléphone du client           |
| FullName     | Client           | Prénom et nom                  |
| BookingStatus  | Booking          | Statut de la reservation    |
| Currency        |  Amount  | Devise     |
| Amount        |  Wallet  | Montant avec devise     |


## Structure du projet
```sh
├── data
│   ├── clients.txt
│   ├── reservations.txt
│   ├── transactions.json
│   └── wallets.json
├── pytest.ini
├── README.md
├── requirements.txt
├── run_cli.py
├── src
│   ├── application
│   │   ├── exceptions.py
│   │   ├── __init__.py
│   │   └── services.py
│   ├── domain
│   │   ├── booking
│   │   │   ├── entities.py
│   │   │   ├── __init__.py
│   │   │   ├── repository.py
│   │   │   ├── services.py
│   │   │   └── value_objects.py
│   │   ├── client
│   │   │   ├── entities.py
│   │   │   ├── __init__.py
│   │   │   ├── repository.py
│   │   │   ├── services.py
│   │   │   └── value_objects.py
│   │   ├── currency
│   │   │   ├── __init__.py
│   │   │   └── value_objects.py
│   │   ├── __init__.py
│   │   ├── payment
│   │   │   ├── entities.py
│   │   │   ├── __init__.py
│   │   │   └── repository.py
│   │   ├── rooms
│   │   │   ├── entities.py
│   │   │   └── __init__.py
│   │   └── wallet
│   │       ├── entities.py
│   │       ├── __init__.py
│   │       ├── repository.py
│   │       ├── services.py
│   │       └── value_objects.py
│   ├── infrastructure
│   │   ├── cli.py
│   │   ├── __init__.py
│   │   └── persistence.py
│   ├── __init__.py
│   └── logger
│       ├── __init__.py
│       └── logger.py
└── tests
    ├── conftest.py
    ├── __init__.py
    ├── test_application_services.py
    ├── test_booking_services.py
    ├── test_client_services.py
    └── test_wallet_services.py

14 directories, 46 files

```
## Cloner le projet
```
git clone git@github.com:barry07-al/Hotel-Management.git
```

## Créer l'environnement et installer les dépendances

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Éxécuter le cli
Éxécuter le fichier run_cli.py à la racine du projet
```sh
python3 run_cli.py
```

## Éxécuter les tests
```sh
pytest -v
```
