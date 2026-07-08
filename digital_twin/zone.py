class ZoneState:
    def __init__(self, zone_id, name, zone_type, capacity=5000):
        self.zone_id = zone_id
        self.name = name
        self.zone_type = zone_type # stand, concourse, parking, transit, amenity
        self.capacity = capacity
        self.current_crowd = 0
        self.risk_score = 0.0
        self.status = "Green"
        self.temperature = 22.0

    def to_dict(self):
        return {
            'zone_id': self.zone_id,
            'name': self.name,
            'zone_type': self.zone_type,
            'capacity': self.capacity,
            'current_crowd': self.current_crowd,
            'risk_score': self.risk_score,
            'status': self.status,
            'temperature': self.temperature
        }
