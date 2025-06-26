class BookingRepository:
    def __init__(self):
        self.reservations = {}

    def save(self, reservation):
        self.reservations[reservation.id] = reservation

    def get_by_id(self, reservation_id: str): 
        return self.reservations.get(reservation_id)

    def get_all(self):
        return list(self.reservations.values())

        
