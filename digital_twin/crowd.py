class CrowdState:
    def __init__(self):
        self.density_level = "Normal"
        self.average_dwell_time = 45 # minutes
        self.movement_flow_rate = 2.4 # meters/sec
        self.anomalies_detected = 0

    def to_dict(self):
        return {
            'density_level': self.density_level,
            'average_dwell_time': self.average_dwell_time,
            'movement_flow_rate': self.movement_flow_rate,
            'anomalies_detected': self.anomalies_detected
        }
