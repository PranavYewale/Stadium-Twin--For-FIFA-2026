class WaterState:
    def __init__(self):
        self.flow_rate_liters_sec = 12.5
        self.recycled_water_liters = 45000
        self.leak_detection = "No leaks detected"
        self.reserve_tank_level = 94.5 # percentage

    def to_dict(self):
        return {
            'flow_rate_liters_sec': self.flow_rate_liters_sec,
            'recycled_water_liters': self.recycled_water_liters,
            'leak_detection': self.leak_detection,
            'reserve_tank_level': self.reserve_tank_level
        }
