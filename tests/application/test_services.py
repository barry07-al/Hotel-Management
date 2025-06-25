import unittest
from unittest.mock import patch, MagicMock
from datetime import date

from src.application.services import HotelApplicationService
from src.domain.wallet.value_objects import Currency
from src.domain.wallet.entities import Wallet
from src.domain.wallet.value_objects import Amount
from src.domain.rooms.entities import RoomType
from src.domain.client.entities import Client
from src.domain.booking.entities import Reservation
from src.domain.client.value_objects import FullName, Email, PhoneNumber


@patch('src.application.services.ClientRepository.save')
@patch('src.application.services.WalletRepository.save')
@patch('src.application.services.Persistence.save_clients')
@patch('src.application.services.Persistence.save_wallets')
@patch('src.application.services.Persistence.save_transactions')
@patch('src.application.services.Persistence.save_reservations')
@patch('src.application.services.Persistence.load_clients', return_value=[])
@patch('src.application.services.Persistence.load_wallets', return_value=[])
@patch('src.application.services.Persistence.load_transactions', return_value=[])
class TestHotelApplicationService(unittest.TestCase):

    def setUp(self):
        self.service = HotelApplicationService()
        self.clients_store = {}
        self.wallets_store = {}

        def client_save(client):
            self.clients_store[client.id] = client

        def client_get_by_id(client_id):
            return self.clients_store.get(client_id)

        self.service.clients.save = MagicMock(side_effect=client_save)
        self.service.clients.get_by_id = MagicMock(side_effect=client_get_by_id)

        def wallet_save(wallet):
            self.wallets_store[wallet.client_id] = wallet

        def wallet_get_by_client_id(client_id):
            return self.wallets_store.get(client_id)

        self.service.wallets.save = MagicMock(side_effect=wallet_save)
        self.service.wallets.get_by_client_id = MagicMock(side_effect=wallet_get_by_client_id)
        self.client = Client(FullName("John", "Doe"), Email("john@example.com"), PhoneNumber("0123456789"))
        self.service.clients.save(self.client)
        self.wallet = Wallet(self.client.id)
        self.service.wallets.save(self.wallet)

    def test_create_account_success(self, *_):
        client = self.service.create_account("Alice", "Smith", "alice@example.com", "9876543210")
        self.assertEqual(client.full_name.first_name, "Alice")
        self.assertEqual(client.full_name.last_name, "Smith")
        self.assertEqual(client.email.value, "alice@example.com")
        self.assertIsNotNone(self.service.wallets.get_by_client_id(client.id))

    
    def test_deposit_money_success(self, *_):
        self.service.deposit_money(self.client.id, 100.0, Currency.EUR)
        wallet = self.service.wallets.get_by_client_id(self.client.id)
        self.assertEqual(wallet.get_balance(), 100.0)

    def test_deposit_money_insufficient_wallet(self, *_):
        with self.assertRaises(Exception) as context:
            self.service.deposit_money("unknown", 50.0, Currency.EUR)
        self.assertIn("Wallet not found", str(context.exception))

    def test_get_balance_success(self, *_):
        self.wallet.deposit(Amount(50.0, Currency.EUR))
        self.service.wallets.save(self.wallet)
        balance = self.service.get_balance(self.client.id)
        self.assertEqual(balance, 50.0)

    def test_get_balance_wallet_not_found(self, *_):
        with self.assertRaises(Exception) as context:
            self.service.get_balance("unknown")
        self.assertIn("Wallet not found", str(context.exception))

    @patch('domain.booking.services.BookingService.create_booking')
    def test_book_room_success(self, mock_create_booking, *_):
        self.wallet.deposit(Amount(500.0, Currency.EUR))
        self.service.wallets.save(self.wallet)

        mock_booking = MagicMock(spec=Reservation)
        mock_booking.total_price = 200.0
        mock_booking.id = "mock_booking_id"
        mock_create_booking.return_value = mock_booking

        booking = self.service.book_room(self.client.id, RoomType.SUPERIOR, 2, date.today())
        self.assertEqual(booking.total_price, 200.0)
        self.assertEqual(self.wallet.get_balance(), 500.0 - 100.0)  # 50% paid

    @patch('domain.booking.services.BookingService.create_booking')
    def test_book_room_insufficient_funds(self, mock_create_booking, *_):
        self.wallet.deposit(Amount(20.0, Currency.EUR))
        self.service.wallets.save(self.wallet)

        mock_booking = MagicMock(spec=Reservation)
        mock_booking.total_price = 100.0
        mock_booking.id = "mock_booking_id"
        mock_create_booking.return_value = mock_booking

        with self.assertRaises(Exception) as context:
            self.service.book_room(self.client.id, RoomType.STANDARD, 1, date.today())
        self.assertIn("Insufficient funds", str(context.exception))

    @patch('domain.booking.services.BookingService.confirm_booking')
    def test_confirm_booking_success(self, mock_confirm_booking, *_):
        self.wallet.deposit(Amount(200.0, Currency.EUR))
        self.service.wallets.save(self.wallet)

        self.service.confirm_booking(self.client.id, "booking123", 100.0)
        self.assertEqual(self.wallet.get_balance(), 150.0)

    def test_confirm_booking_insufficient_funds(self, *_):
        self.wallet.deposit(Amount(10.0, Currency.EUR))
        self.service.wallets.save(self.wallet)

        with self.assertRaises(Exception) as context:
            self.service.confirm_booking(self.client.id, "booking123", 100.0)
        self.assertIn("Insufficient funds", str(context.exception))

    @patch('domain.booking.services.BookingService.cancel_booking')
    def test_cancel_booking_calls_service(self, mock_cancel_booking, *_):
        self.service.cancel_booking("booking456", self.client.id)
        mock_cancel_booking.assert_called_once_with("booking456", self.client.id)

    def test_get_client_by_id_success(self, *_):
        found = self.service.get_client_by_id(self.client.id)
        self.assertEqual(found.id, self.client.id)

    def test_get_client_by_id_not_found(self, *_):
        with self.assertRaises(Exception) as context:
            self.service.get_client_by_id("unknown")
        self.assertIn("Client not found", str(context.exception))
