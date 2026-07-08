import random

def get_traffic_status():
    """
    Simulates traffic congestion index on main access roads (I-95, Route 120, etc.)
    Returns delay minutes and status.
    """
    delay = random.randint(2, 45)
    if delay < 10:
        status = "Green"
    elif delay < 25:
        status = "Yellow"
    elif delay < 40:
        status = "Orange"
    else:
        status = "Red"
        
    return {
        'road_status': status,
        'delay_minutes': delay,
        'average_speed_mph': random.randint(15, 60)
    }
