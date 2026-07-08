class SeatState:
    def __init__(self, total_seats=80000):
        self.total_seats = total_seats
        self.occupied_seats = 0
        self.vip_seats_occupied = 0
        self.accessible_seats_occupied = 0

    def to_dict(self):
        return {
            'total_seats': self.total_seats,
            'occupied_seats': self.occupied_seats,
            'vip_seats_occupied': self.vip_seats_occupied,
            'accessible_seats_occupied': self.accessible_seats_occupied
        }
