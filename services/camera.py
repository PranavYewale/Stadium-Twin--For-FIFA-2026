import random

def process_cctv_cv(zone_id):
    """
    Simulates CV computer vision analytics (YOLO / OpenCV) on a camera feed.
    Detects crowd density, running, falling, fights, fire/smoke, or abandoned bags.
    """
    # Small chance of triggering an incident
    trigger_roll = random.random()
    
    if trigger_roll < 0.02:
        anomalies = [
            ("fight", "Physical altercation detected in stand section", "warning"),
            ("abandoned_bag", "Unattended package identified near transit point", "warning"),
            ("smoke", "Visual smoke indicator near concession area", "critical"),
            ("stampede_risk", "High density crowd movement pattern detected", "critical")
        ]
        anomaly, msg, level = random.choice(anomalies)
        return {
            'detected': True,
            'anomaly_type': anomaly,
            'message': msg,
            'level': level
        }
        
    return {'detected': False}
