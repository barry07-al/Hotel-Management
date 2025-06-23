import uuid
from datetime import date
from domain.rooms.entities import RoomType
from domain.booking.value_objects import ReservationStatus

class Reservation:
    def __init__(self, guest_id: str, room_type: RoomType, nights: int, checkin_date: date):
        if nights <= 0:
            raise ValueError("Nights must be a positive integer.")
        
        self.id = str(uuid.uuid4())
        self.guest_id = guest_id
        self.room_type = room_type
        self.nights = nights
        self.checkin_date = checkin_date
        self.status = ReservationStatus.PENDING
        self.total_price = room_type.value * nights

    def confirm(self):
        if self.status != ReservationStatus.PENDING:
            raise ValueError("Only pending reservations can be confirmed.")
        self.status = ReservationStatus.CONFIRMED

    def cancel(self):
        if self.status == ReservationStatus.CANCELED:
            raise ValueError("Reservation is already canceled.")
        self.status = ReservationStatus.CANCELED
