class StadiumState:
    def __init__(self, name="FIFA World Cup 2026 Arena", total_capacity=80000):
        self.name = name
        self.total_capacity = total_capacity
        self.current_attendance = 0
        self.match_status = "Pre-match Warmup"
        self.match_info = "USA vs England - Group B"
        self.emergency_mode = False
        self.emergency_type = None

    def to_dict(self):
        return {
            'name': self.name,
            'total_capacity': self.total_capacity,
            'current_attendance': self.current_attendance,
            'match_status': self.match_status,
            'match_info': self.match_info,
            'emergency_mode': self.emergency_mode,
            'emergency_type': self.emergency_type
        }
