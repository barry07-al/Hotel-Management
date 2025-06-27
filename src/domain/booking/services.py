from datetime import date

from .entities import Booking
from domain.rooms.entities import RoomType
from infrastructure.persistence import Persistence
from application.exceptions import ApplicationError
from domain.booking.repository import BookingRepository

class BookingService:

    def __init__(self, repo: BookingRepository):
        self.repo = repo
        loaded = Persistence.load_reservations()
        for r in loaded:
            self.repo.save(r)

    def create_booking(self, client_id: str, room_type: RoomType, nights: int, checkin_date: date) -> Booking:
        booking = Booking(client_id, room_type, nights, checkin_date)
        self.repo.save(booking)
        self._persist()
        return booking

    def confirm_booking(self, booking_id: str):
        booking = self.repo.get_by_id(booking_id)
        booking.confirm()
        self._persist()

    def cancel_booking(self, booking_id: str, client_id: str):
        booking = self.repo.get_by_id(booking_id)
        if not booking:
            raise ApplicationError(f"Booking {booking_id} not found.")
        booking.cancel(client_id)
        self._persist()

    def _persist(self):
        Persistence.save_reservations(self.repo.get_all())
