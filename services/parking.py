import random

def get_parking_telemetry():
    """
    Simulates parking occupancy counts for East, West, and VIP parking lots.
    """
    return {
        'parking_east': {
            'occupied': random.randint(1200, 1980),
            'capacity': 2000
        },
        'parking_west': {
            'occupied': random.randint(800, 1450),
            'capacity': 1500
        },
        'parking_vip': {
            'occupied': random.randint(180, 248),
            'capacity': 250
        }
    }
