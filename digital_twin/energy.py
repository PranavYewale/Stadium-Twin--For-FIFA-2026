class EnergyState:
    def __init__(self):
        self.grid_load_kwh = 1200.0
        self.solar_generation_kwh = 350.0
        self.battery_storage_kwh = 2400.0
        self.hvac_status = "Optimized"

    def to_dict(self):
        return {
            'grid_load_kwh': self.grid_load_kwh,
            'solar_generation_kwh': self.solar_generation_kwh,
            'battery_storage_kwh': self.battery_storage_kwh,
            'hvac_status': self.hvac_status,
            'net_consumption': max(0.0, self.grid_load_kwh - self.solar_generation_kwh)
        }
