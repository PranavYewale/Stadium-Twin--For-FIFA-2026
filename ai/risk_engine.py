def calculate_zone_risk(current_crowd, capacity, queue_length, medical_incidents, security_level):
    """
    Computes a risk score from 0 to 100 and a color-coded status.
    Risk depends on:
    - Crowd congestion ratio (current_crowd / capacity)
    - Queue lengths (indicates delay & potential stampede risk)
    - Security Level (Normal, Elevated, High, Critical)
    - Medical Incidents count
    """
    # 1. Congestion factor
    congestion = current_crowd / max(1, capacity)
    congestion_score = congestion * 60.0  # Up to 60 points from congestion
    
    # 2. Queue factor
    queue_score = 0.0
    if queue_length > 50:
        queue_score = 20.0
    elif queue_length > 20:
        queue_score = 10.0
    elif queue_length > 5:
        queue_score = 5.0
        
    # 3. Security factor
    sec_scores = {
        'Normal': 0.0,
        'Elevated': 10.0,
        'High': 25.0,
        'Critical': 40.0
    }
    security_score = sec_scores.get(security_level, 0.0)
    
    # 4. Medical incident factor
    medical_score = min(20.0, medical_incidents * 10.0)
    
    # Total score
    total_score = congestion_score + queue_score + security_score + medical_score
    total_score = min(100.0, max(0.0, total_score))
    
    # Color mapping
    if total_score < 30.0:
        status = 'Green'
    elif total_score < 60.0:
        status = 'Yellow'
    elif total_score < 80.0:
        status = 'Orange'
    else:
        status = 'Red'
        
    return round(total_score, 1), status
