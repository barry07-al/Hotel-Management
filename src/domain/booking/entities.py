import uuid
from datetime import date
from domain.rooms.entities import RoomType
from domain.booking.value_objects import BookingStatus

class Booking:
    def __init__(self, client_id: str, room_type: RoomType, nights: int, checkin_date: date):
        if nights <= 0:
            raise ValueError("Nights must be a positive integer.")
        
        self.id = str(uuid.uuid4())
        self.client_id = client_id
        self.room_type = room_type
        self.nights = nights
        self.checkin_date = checkin_date
        self.status = BookingStatus.PENDING
        self.total_price = room_type.value * nights

    def confirm(self):
        if self.status != BookingStatus.PENDING:
            raise ValueError("Only pending reservations can be confirmed.")
        self.status = BookingStatus.CONFIRMED

    def cancel(self, client_id: str):
        if client_id != self.client_id:
            raise PermissionError("You are not allowed to cancel this reservation.")
        if self.status == BookingStatus.CANCELED:
            raise ValueError("Reservation is already canceled.")
        if self.status == BookingStatus.CONFIRMED:
            raise ValueError("Confirmed reservations cannot be canceled.")
        self.status = BookingStatus.CANCELED
