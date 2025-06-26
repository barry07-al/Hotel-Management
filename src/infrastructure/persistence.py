import json
import os
from domain.client.entities import Client
from domain.wallet.entities import Wallet
from domain.booking.entities import Booking
from domain.booking.value_objects import BookingStatus
from domain.rooms.entities import RoomType
from domain.payment.entities import PaymentTransaction
from datetime import datetime
from domain.client.value_objects import FullName, Email, PhoneNumber

DATA_DIR = "data"

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def read_json_file(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)

class Persistence:

    @staticmethod
    def save_reservations(reservations: list, file_path: str = f"{DATA_DIR}/reservations.txt"):
        ensure_data_dir()
        with open(file_path, "w", encoding="utf-8") as f:
            data = [{
                "id": r.id,
                "client_id": r.client_id,
                "room_type": r.room_type.name,
                "nights": r.nights,
                "checkin_date": r.checkin_date.isoformat(),
                "status": r.status.name,
                "total_price": r.total_price
            } for r in reservations]
            json.dump(data, f, indent=2)

    @staticmethod
    def load_reservations(file_path: str = f"{DATA_DIR}/reservations.txt") -> list:
        raw_data = read_json_file(file_path)
        reservations = []
        for d in raw_data:
            r = Booking(
                client_id=d["client_id"],
                room_type=RoomType[d["room_type"]],
                nights=int(d["nights"]),
                checkin_date=datetime.fromisoformat(d["checkin_date"])
            )
            r.id = d["id"]
            r.status = BookingStatus[d["status"]]
            r.total_price = float(d["total_price"])
            reservations.append(r)
        return reservations

    @staticmethod
    def save_clients(clients: list, file_path: str = f"{DATA_DIR}/clients.txt"):
        ensure_data_dir()
        with open(file_path, "w", encoding="utf-8") as f:
            data = [
                {
                    "id": c.id,
                    "full_name": c.full_name.value,
                    "email": c.email.value,
                    "phone_number": c.phone_number.value
                }
                for c in clients
            ]
            json.dump(data, f, indent=2)

    @staticmethod
    def load_clients(file_path: str = f"{DATA_DIR}/clients.txt") -> list:
        raw_data = read_json_file(file_path)
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
            json.dump(
                [{"client_id": w.client_id, "balance": w.balance} for w in wallets], f, indent=2)

    @staticmethod
    def load_wallets(file_path=f"{DATA_DIR}/wallets.json") -> list:
        raw = read_json_file(file_path)
        wallets = []
        for w in raw:
            wallet = Wallet(w["client_id"])
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
                    "timestamp": t.timestamp.isoformat()
                } for t in transactions
            ], f, indent=2)

    @staticmethod
    def load_transactions(file_path=f"{DATA_DIR}/transactions.json") -> list[PaymentTransaction]:
        raw_data = read_json_file(file_path)
        return [
            PaymentTransaction(
                amount=d["amount"],
                description=d["description"]
            ) for d in raw_data
        ]
