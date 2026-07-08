import random
from datetime import datetime, timedelta
import numpy as np

# We'll use a fallback in case scikit-learn is not available, though we listed it in requirements.
try:
    from sklearn.linear_model import LinearRegression
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

def forecast_zone_telemetry(zone_id, current_crowd, capacity, current_queue, zone_type, historical_rates=None):
    """
    Simulates AI forecasting for 15, 30, and 60 minutes.
    Uses linear extrapolation over a simple time trend with sigmoid boundaries.
    """
    predictions = []
    
    # Simple simulation parameters depending on zone types
    # Stadium gates spike before match, stands fill up, transit spikes before and after
    now = datetime.utcnow()
    
    # We will compute predictions for 15, 30, and 60 minutes
    for offset in [15, 30, 60]:
        # Simple trend computation
        trend = 0
        if zone_type == 'entrance':
            # Pre-match gates fill up then level off
            # Let's check current crowd relative to capacity
            fill_ratio = current_crowd / max(1, capacity)
            if fill_ratio < 0.7:
                # Still filling
                trend = random.randint(10, 30) * (offset / 15)
            elif fill_ratio < 0.95:
                # Congested, slowing down
                trend = random.randint(2, 10) * (offset / 15)
            else:
                # Over capacity, queue grows
                trend = -random.randint(5, 15) * (offset / 15)
        elif zone_type.lower() == 'stand':
            # Stands fill up steadily
            fill_ratio = current_crowd / max(1, capacity)
            if fill_ratio < 0.95:
                trend = random.randint(15, 45) * (offset / 15)
            else:
                trend = random.randint(-5, 5) * (offset / 15)
        elif zone_type == 'transit':
            # Transit flows in waves
            trend = random.choice([-50, -20, 10, 40, 80]) * (offset / 15)
        elif zone_type == 'amenity':
            # Restrooms/Food courts grow as stand capacity increases
            trend = random.randint(-5, 15) * (offset / 15)
        else:
            trend = random.randint(-10, 20) * (offset / 15)
            
        predicted_crowd = int(current_crowd + trend)
        predicted_crowd = max(0, min(predicted_crowd, int(capacity * 1.3))) # Cap at 130% capacity
        
        # Predicted queue length
        predicted_queue = int(current_queue + (trend * 0.3))
        if predicted_crowd > capacity:
            predicted_queue = max(predicted_queue, int((predicted_crowd - capacity) * 0.5))
        predicted_queue = max(0, predicted_queue)
        
        # Calculate future risk score based on future congestion
        congestion_ratio = predicted_crowd / max(1, capacity)
        future_risk = congestion_ratio * 70.0
        if predicted_queue > 50:
            future_risk += 20.0
        elif predicted_queue > 20:
            future_risk += 10.0
            
        future_risk = min(100.0, max(0.0, future_risk))
        
        # Confidence score (lower for 60m, higher for 15m)
        confidence = max(0.4, 0.95 - (offset / 120.0) - (random.random() * 0.05))
        
        predictions.append({
            'time_offset': offset,
            'predicted_crowd': predicted_crowd,
            'predicted_queue': predicted_queue,
            'risk_score': round(future_risk, 1),
            'confidence': round(confidence, 2)
        })
        
    return predictions

def run_regression_prediction(timestamps, values, offset_minutes):
    """
    Perform a simple linear regression using numpy/scikit-learn.
    Returns the predicted value at offset_minutes.
    """
    if len(values) < 2:
        return values[-1] if values else 0
        
    # Convert timestamps to relative seconds
    t0 = timestamps[0]
    x = np.array([(t - t0).total_seconds() for t in timestamps]).reshape(-1, 1)
    y = np.array(values)
    
    future_time_delta = offset_minutes * 60
    target_x = np.array([[(timestamps[-1] - t0).total_seconds() + future_time_delta]])
    
    if HAS_SKLEARN:
        model = LinearRegression()
        model.fit(x, y)
        prediction = model.predict(target_x)[0]
    else:
        # Fallback to numpy polyfit (degree 1)
        coeffs = np.polyfit(x.flatten(), y, 1)
        prediction = coeffs[0] * target_x[0][0] + coeffs[1]
        
    return prediction
