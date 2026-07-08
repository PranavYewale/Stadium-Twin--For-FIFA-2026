import random

def get_food_court_telemetry():
    """
    Simulates queue lengths and inventory levels for North and West food courts.
    """
    return {
        'food_court_north': {
            'queue_length': random.randint(5, 45),
            'wait_time_seconds': random.randint(120, 600),
            'stock_level': max(10, 100 - random.randint(0, 40))
        },
        'food_court_west': {
            'queue_length': random.randint(0, 15),
            'wait_time_seconds': random.randint(0, 200),
            'stock_level': max(30, 100 - random.randint(0, 20))
        }
    }
