class ParkingState:
    def __init__(self, lot_id, name, capacity=2000):
        self.lot_id = lot_id
        self.name = name
        self.capacity = capacity
        self.occupied_spaces = 0
        self.status = "Open" # Open, Filling, Full, Closed

    def to_dict(self):
        return {
            'lot_id': self.lot_id,
            'name': self.name,
            'capacity': self.capacity,
            'occupied_spaces': self.occupied_spaces,
            'status': self.status,
            'occupancy_percentage': round((self.occupied_spaces / max(1, self.capacity)) * 100, 1)
        }
