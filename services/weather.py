import random

def get_current_weather():
    """
    Returns simulated or fetched live weather data.
    """
    conditions = ["Clear", "Partly Cloudy", "Heavy Rain", "Overcast", "Windy"]
    condition = random.choice(conditions)
    temp = round(random.uniform(22.0, 31.0), 1)
    humidity = random.randint(40, 90)
    
    return {
        'temp': temp,
        'condition': condition,
        'humidity': humidity,
        'wind_speed': round(random.uniform(5.0, 25.0), 1)
    }
