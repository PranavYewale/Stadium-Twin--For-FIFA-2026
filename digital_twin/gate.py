class GateState:
    def __init__(self, gate_id, name, capacity=1000):
        self.gate_id = gate_id
        self.name = name
        self.capacity = capacity
        self.current_crowd = 0
        self.queue_length = 0
        self.status = "Green"
        self.scanned_tickets_count = 0

    def to_dict(self):
        return {
            'gate_id': self.gate_id,
            'name': self.name,
            'capacity': self.capacity,
            'current_crowd': self.current_crowd,
            'queue_length': self.queue_length,
            'status': self.status,
            'scanned_tickets_count': self.scanned_tickets_count
        }
