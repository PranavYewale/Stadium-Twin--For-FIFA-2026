import random

def get_transit_telemetry():
    """
    Simulates metro and bus arrivals at the main transit hubs.
    """
    metro_arrival_in = random.randint(1, 8)
    bus_arrival_in = random.randint(1, 12)
    metro_passenger_count = random.randint(200, 600)
    bus_passenger_count = random.randint(40, 90)
    
    return {
        'metro': {
            'next_arrival_minutes': metro_arrival_in,
            'predicted_passengers': metro_passenger_count,
            'status': "On Time" if metro_arrival_in > 2 else "Arriving"
        },
        'bus': {
            'next_arrival_minutes': bus_arrival_in,
            'predicted_passengers': bus_passenger_count,
            'status': "On Time" if bus_arrival_in > 2 else "Arriving"
        }
    }
