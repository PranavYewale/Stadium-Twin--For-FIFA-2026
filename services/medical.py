import random

def check_medical_incidents():
    """
    Simulates medical incident logs like heat exhaustion, fainting, or minor injuries.
    """
    # 2% chance of a medical event
    if random.random() < 0.02:
        incidents = [
            {"type": "heat", "msg": "Fan exhibiting symptoms of heat exhaustion at Stand 201", "level": "info"},
            {"type": "fall", "msg": "Minor fall incident reported on Concourse level 2 escalator", "level": "info"},
            {"type": "cardiac", "msg": "Chest pain warning reported from Sector 108. Dispatching AED unit", "level": "critical"}
        ]
        return random.choice(incidents)
    return None
