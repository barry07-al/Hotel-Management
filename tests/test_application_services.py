import pytest
from unittest.mock import MagicMock, patch
from datetime import date

from src.application.services import HotelApplicationService
from src.domain.wallet.value_objects import Currency, Amount
from src.domain.wallet.entities import Wallet
from src.domain.rooms.entities import RoomType
from src.domain.client.entities import Client
from src.domain.booking.entities import Booking
from src.domain.client.value_objects import FullName, Email, PhoneNumber


@pytest.fixture(autouse=True)
def mock_persistence():
    with patch("src.application.services.Persistence.load_clients", return_value=[]), \
         patch("src.application.services.Persistence.load_wallets", return_value=[]), \
         patch("src.application.services.Persistence.load_transactions", return_value=[]), \
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
        return clients_store.get(client_id)

    service.clients.save = MagicMock(side_effect=save_client)
    service.clients.get_by_id = MagicMock(side_effect=get_client_by_id)

    def save_wallet(wallet):
        wallets_store[wallet.client_id] = wallet

    def get_wallet_by_client_id(client_id):
        return wallets_store.get(client_id)

    service.wallets.save = MagicMock(side_effect=save_wallet)
    service.wallets.get_by_client_id = MagicMock(side_effect=get_wallet_by_client_id)

    return service

@pytest.fixture
def client(hotel_service):
    client = Client(FullName("John", "Doe"), Email("john@example.com"), PhoneNumber("0123456789"))
    hotel_service.clients.save(client)
    return client

@pytest.fixture
def wallet(hotel_service, client):
    wallet = Wallet(client.id)
    hotel_service.wallets.save(wallet)
    return wallet

def test_create_account_success(hotel_service):
    client = hotel_service.create_account("Alice", "Smith", "alice@example.com", "9876543210")
    assert client.full_name.first_name == "Alice"
    assert client.email.value == "alice@example.com"
    assert hotel_service.wallets.get_by_client_id(client.id) is not None

def test_deposit_money_success(hotel_service, client, wallet):
    hotel_service.deposit_money(client.id, 100.0, Currency.EUR)
    w = hotel_service.wallets.get_by_client_id(client.id)
    assert w.get_balance() == 100.0

def test_deposit_money_insufficient_wallet(hotel_service):
    with pytest.raises(Exception, match="Wallet not found"):
        hotel_service.deposit_money("unknown", 50.0, Currency.EUR)

def test_get_balance_success(hotel_service, client, wallet):
    wallet.deposit(Amount(50.0, Currency.EUR))
    hotel_service.wallets.save(wallet)
    balance = hotel_service.get_balance(client.id)
    assert balance == 50.0

def test_get_balance_wallet_not_found(hotel_service):
    with pytest.raises(Exception, match="Wallet not found"):
        hotel_service.get_balance("unknown")

@patch("src.application.services.BookingService.create_booking")
def test_book_room_success(mock_create_booking, hotel_service, client, wallet):
    wallet.deposit(Amount(500.0, Currency.EUR))
    hotel_service.wallets.save(wallet)

    mock_booking = MagicMock(spec=Booking)
    mock_booking.total_price = 200.0
    mock_booking.id = "mock_booking_id"
    mock_create_booking.return_value = mock_booking

    booking = hotel_service.book_room(client.id, RoomType.SUPERIOR, 2, date.today())

    assert booking.total_price == 200.0
    assert wallet.get_balance() == 400.0

@patch("src.application.services.BookingService.create_booking")
def test_book_room_insufficient_funds(mock_create_booking, hotel_service, client, wallet):
    wallet.deposit(Amount(20.0, Currency.EUR))
    hotel_service.wallets.save(wallet)

    mock_booking = MagicMock(spec=Booking)
    mock_booking.total_price = 100.0
    mock_booking.id = "mock_booking_id"
    mock_create_booking.return_value = mock_booking

    with pytest.raises(Exception, match="Insufficient funds"):
        hotel_service.book_room(client.id, RoomType.STANDARD, 1, date.today())

@patch("src.application.services.BookingService.confirm_booking")
def test_confirm_booking_success(mock_confirm_booking, hotel_service, client, wallet):
    wallet.deposit(Amount(200.0, Currency.EUR))
    hotel_service.wallets.save(wallet)

    mock_booking = MagicMock()
    mock_booking.total_price = 50
    hotel_service.bookings.get_by_id = MagicMock(return_value=mock_booking)

    hotel_service.confirm_booking(client.id, "booking123")
    assert wallet.get_balance() == 175

def test_confirm_booking_insufficient_funds(hotel_service, client, wallet):
    wallet.deposit(Amount(10.0, Currency.EUR))
    hotel_service.wallets.save(wallet)

    mock_booking = MagicMock()
    mock_booking.total_price = 50
    hotel_service.bookings.get_by_id = MagicMock(return_value=mock_booking)

    with pytest.raises(Exception, match="Insufficient funds"):
        hotel_service.confirm_booking(client.id, "booking123")


@patch("src.application.services.BookingService.cancel_booking")
def test_cancel_booking_calls_service(mock_cancel_booking, hotel_service, client):
    hotel_service.cancel_booking("booking456", client.id)
    mock_cancel_booking.assert_called_once_with("booking456", client.id)


def test_get_client_by_id_success(hotel_service, client):
    found = hotel_service.get_client_by_id(client.id)
    assert found.id == client.id


def test_get_client_by_id_not_found(hotel_service):
    with pytest.raises(Exception, match="Client not found"):
        hotel_service.get_client_by_id("unknown")
