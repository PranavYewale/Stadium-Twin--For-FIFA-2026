import random

def check_security_logs():
    """
    Simulates security alerts like blocked exits, intrusions, or suspicious behaviour.
    """
    # 3% chance of a new alert
    if random.random() < 0.03:
        incidents = [
            {"type": "intrusion", "msg": "Intrusion alarm triggered in Sector B perimeter wall", "level": "warning"},
            {"type": "blocked_exit", "msg": "Exit 104 is currently blocked by stacked transit crates", "level": "warning"},
            {"type": "crowd_rush", "msg": "Crowd surge reported near ticket scanner terminal A2", "level": "critical"}
        ]
        return random.choice(incidents)
    return None
