import pytest
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from unittest.mock import MagicMock

from src.domain.wallet.entities import Wallet
from src.domain.client.entities import Client
from src.application.services import HotelApplicationService
from src.domain.client.value_objects import FullName, Email, PhoneNumber


@pytest.fixture
def client():
    return Client(FullName("John", "Doe"), Email("john@example.com"), PhoneNumber("0123456789"))

@pytest.fixture
def wallet(client):
    wallet = Wallet(client.id)
    return wallet

@pytest.fixture
def hotel_service():
    service = HotelApplicationService()

    clients_store = {}
    wallets_store = {}

    def save_client(client):
        clients_store[client.id] = client

    def get_client(client_id):
        return clients_store.get(client_id)

    service.clients.save = MagicMock(side_effect=save_client)
    service.clients.get_by_id = MagicMock(side_effect=get_client)

    def save_wallet(wallet):
        wallets_store[wallet.client_id] = wallet

    def get_wallet(client_id):
        return wallets_store.get(client_id)

    service.wallets.save = MagicMock(side_effect=save_wallet)
    service.wallets.get_by_client_id = MagicMock(side_effect=get_wallet)
    return service
