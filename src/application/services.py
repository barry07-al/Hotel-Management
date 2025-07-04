from domain.wallet.entities import Wallet
from domain.rooms.entities import RoomType
from domain.wallet.value_objects import Amount
from domain.client.services import ClientService
from infrastructure.persistence import Persistence
from domain.booking.services import BookingService
from domain.currency.value_objects import Currency
from application.exceptions import ApplicationError
from domain.client.repository import ClientRepository
from domain.wallet.repository import WalletRepository
from domain.payment.entities import PaymentTransaction
from domain.payment.repository import PaymentRepository
from domain.booking.repository import BookingRepository 





from datetime import date

class HotelApplicationService:

    def __init__(self):
        self.clients = ClientRepository()
        self.wallets = WalletRepository()
        self.payments = PaymentRepository()
        self.bookings = BookingRepository()
        
        self.client_service = ClientService(self.clients)
        self.booking_service = BookingService(self.bookings)

        for c in Persistence.load_clients():
            self.clients.save(c)
        for w in Persistence.load_wallets():
            self.wallets.save(w)
        for p in Persistence.load_transactions():
            self.payments.record(p)
    
    def get_client_by_id(self, client_id: str):
        client = self.clients.get_by_id(client_id)
        if not client:
            raise ApplicationError(f"Client {client_id} not exists.")
        return client

    def create_account(self, first: str, last: str, email: str, phone: str):
        client = self.client_service.register_client(first, last, email, phone)
        self.wallets.save(Wallet(client.id))
        self._save_all()
        return client

    def deposit_money(self, client_id: str, value: float, currency: Currency):
        wallet = self.wallets.get_by_client_id(client_id)
        amount = Amount(value, currency)
        wallet.deposit(amount)
        self.wallets.save(wallet)
        self._save_all()

    def get_balance(self, client_id: str) -> float:
        wallet = self.wallets.get_by_client_id(client_id)
        return wallet.get_balance()

    def book_room(self, client_id: str, room_type: RoomType, nights: int, checkin_date: date):
        wallet = self.wallets.get_by_client_id(client_id)
        booking = self.booking_service.create_booking(client_id, room_type, nights, checkin_date)
        upfront = booking.total_price * 0.5

        if wallet.get_balance() < upfront:
            raise ApplicationError("Insufficient funds.")

        wallet.withdraw(upfront)
        self.wallets.save(wallet)

        self.payments.record(PaymentTransaction(upfront, "Booking deposit"))
        self.bookings.save(booking)
        self._save_all()
        return booking

    def confirm_booking(self, client_id: str, booking_id: str):
        wallet = self.wallets.get_by_client_id(client_id)
        booking = self.bookings.get_by_id(booking_id)
        if not booking:
            raise ApplicationError(f"Booking {booking_id} not exists.")
        
        remaining = booking.total_price * 0.5

        if wallet.get_balance() < remaining:
            raise ApplicationError("Insufficient funds to confirm.")

        wallet.withdraw(remaining)
        self.wallets.save(wallet)

        self.payments.record(PaymentTransaction(remaining, "Booking confirmation"))
        self.booking_service.confirm_booking(booking_id)
        self._save_all()

    def cancel_booking(self, booking_id: str, client_id: str):
        self.booking_service.cancel_booking(booking_id, client_id)
        self._save_all()

    def _save_all(self):
        Persistence.save_clients(self.clients.get_all())
        Persistence.save_wallets(self.wallets.get_all())
        Persistence.save_transactions(self.payments.get_all())
        Persistence.save_reservations(self.bookings.get_all())
