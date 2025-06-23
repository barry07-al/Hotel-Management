import json
import os
from domain.client.entities import Client
from domain.wallet.entities import Wallet
from domain.booking.entities import Reservation
from domain.rooms.entities import RoomType
from domain.payment.entities import PaymentTransaction
from datetime import date
from domain.client.value_objects import FullName, Email, PhoneNumber

DATA_DIR = "data"

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

class Persistence:

    # Reservations
    @staticmethod
    def save_reservations(reservations: list, file_path: str = f"{DATA_DIR}/reservations.txt"):
        ensure_data_dir()
        with open(file_path, "w", encoding="utf-8") as f:
            data = [{
                "id": r.id,
                "guest_id": r.guest_id,
                "room_type": r.room_type.name,
                "nights": r.nights,
                "checkin_date": r.checkin_date.isoformat(),
                "status": r.status,
                "total_price": r.total_price
            } for r in reservations]
            json.dump(data, f, indent=2)

    @staticmethod
    def load_reservations(file_path: str = f"{DATA_DIR}/reservations.txt") -> list:
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            return [
                Reservation(
                    guest_id=d["guest_id"],
                    room_type=RoomType[d["room_type"]],
                    nights=int(d["nights"]),
                    checkin_date=date.fromisoformat(d["checkin_date"])
                ).__setattr__("id", d["id"]) or Reservation(
                    guest_id=d["guest_id"],
                    room_type=RoomType[d["room_type"]],
                    nights=int(d["nights"]),
                    checkin_date=date.fromisoformat(d["checkin_date"])
                ) for d in raw_data
            ]

    @staticmethod
    def save_clients(clients: list, file_path: str = f"{DATA_DIR}/clients.txt"):
        ensure_data_dir()
        with open(file_path, "w", encoding="utf-8") as f:
            data = [{
                "id": c.id,
                "full_name": c.full_name.value,
                "email": c.email.value,
                "phone_number": c.phone_number.value
            } for c in clients]
            json.dump(data, f, indent=2)

    @staticmethod
    def load_clients(file_path: str = f"{DATA_DIR}/clients.txt") -> list:
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            clients = []
            for d in raw_data:
                client = Client(
                    full_name=FullName(*d["full_name"].split(" ")),
                    email=Email(d["email"]),
                    phone_number=PhoneNumber(d["phone_number"])
                )
                client.id = d["id"]
                clients.append(client)
            return clients

    @staticmethod
    def save_wallets(wallets: list, file_path=f"{DATA_DIR}/wallets.json"):
        ensure_data_dir()
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([
                {"user_id": w.user_id, "balance": w.balance}
                for w in wallets
            ], f, indent=2)

    @staticmethod
    def load_wallets(file_path=f"{DATA_DIR}/wallets.json") -> list:
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
            wallets = []
            for w in raw:
                wallet = Wallet(w["user_id"])
                wallet.balance = w["balance"]
                wallets.append(wallet)
            return wallets

    @staticmethod
    def save_transactions(transactions: list[PaymentTransaction], file_path=f"{DATA_DIR}/transactions.json"):
        ensure_data_dir()
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([
                {
                    "amount": t.amount,
                    "description": t.description,
                    "timestamp": t.timestamp
                } for t in transactions
            ], f, indent=2)

    @staticmethod
    def load_transactions(file_path=f"{DATA_DIR}/transactions.json") -> list[PaymentTransaction]:
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            return [
                PaymentTransaction(
                    amount=d["amount"],
                    description=d["description"],
                    timestamp=d["timestamp"]
                ) for d in raw_data
            ]
