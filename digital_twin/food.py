class FoodCourtState:
    def __init__(self, court_id, name):
        self.court_id = court_id
        self.name = name
        self.queue_length = 0
        self.average_wait_time = 0 # seconds
        self.popular_item = "Hot Dog & Soda"
        self.stock_level = 100.0 # percentage

    def to_dict(self):
        return {
            'court_id': self.court_id,
            'name': self.name,
            'queue_length': self.queue_length,
            'average_wait_time': self.average_wait_time,
            'popular_item': self.popular_item,
            'stock_level': self.stock_level
        }
