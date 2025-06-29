import sys
import pytest

from pathlib import Path
from unittest.mock import MagicMock, patch


sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from src.domain.wallet.entities import Wallet
from src.domain.client.entities import Client

from src.application.services import BookingService
from src.domain.client.services import ClientService
from src.application.exceptions import ApplicationError
from src.application.services import HotelApplicationService
from src.domain.client.value_objects import FullName, Email, PhoneNumber


@pytest.fixture(autouse=True)
def mock_persistence():
    with patch("src.application.services.Persistence.load_clients", return_value=[]), \
         patch("src.application.services.Persistence.load_wallets", return_value=[]), \
         patch("src.application.services.Persistence.load_transactions", return_value=[]), \
         patch("src.application.services.Persistence.load_reservations", return_value=[]), \
         patch("src.application.services.Persistence.save_clients"), \
         patch("src.application.services.Persistence.save_wallets"), \
         patch("src.application.services.Persistence.save_transactions"), \
         patch("src.application.services.Persistence.save_reservations"), \
         patch("src.application.services.ClientRepository.save"), \
         patch("src.application.services.WalletRepository.save"):
        yield

@pytest.fixture
def hotel_service():
    service = HotelApplicationService()

    clients_store = {}
    wallets_store = {}

    def save_client(client):
        clients_store[client.id] = client

    def get_client_by_id(client_id):
        res = clients_store.get(client_id)
        if not res:
            raise ApplicationError(f"Client {client_id} not exists.")
        return res

    service.clients.save = MagicMock(side_effect=save_client)
    service.clients.get_by_id = MagicMock(side_effect=get_client_by_id)

    def save_wallet(wallet):
        wallets_store[wallet.client_id] = wallet

    def get_wallet_by_client_id(client_id):
        res = wallets_store.get(client_id)
        if not res:
            raise ApplicationError(f"Wallet not found for client {client_id}.")
        return res

    service.wallets.save = MagicMock(side_effect=save_wallet)
    service.wallets.get_by_client_id = MagicMock(side_effect=get_wallet_by_client_id)

    return service

@pytest.fixture
def client(hotel_service):
    client = Client(FullName("Alpha", "BARRY"), Email("barry@gmail.com"), PhoneNumber("0689123546"))
    hotel_service.clients.save(client)
    return client

@pytest.fixture
def mock_booking_repository():
    return MagicMock()

@pytest.fixture
def booking_service(mock_booking_repository):
    return BookingService(repo=mock_booking_repository)

@pytest.fixture
def wallet(hotel_service, client):
    wallet = Wallet(client.id)
    hotel_service.wallets.save(wallet)
    return wallet

@pytest.fixture
def mock_client_repository():
    return MagicMock()

@pytest.fixture
def client_service(mock_client_repository):
    return ClientService(mock_client_repository)

@pytest.fixture
def client_id():
    return "client-123"

@pytest.fixture
def booking_id():
    return "booking-123"
