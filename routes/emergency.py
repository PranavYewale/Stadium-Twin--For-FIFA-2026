from flask import Blueprint, request, jsonify
from database.models import db, Alert, Zone

emergency_bp = Blueprint('emergency', __name__)

@emergency_bp.route('/api/emergency/trigger', methods=['POST'])
def trigger_emergency():
    """
    Simulates triggering a stadium-wide critical emergency (Fire, Earthquake, Stampede, etc.)
    """
    data = request.json or {}
    emergency_type = data.get('type', 'General Alarm')
    message = data.get('message', 'Critical situation reported! Evacuate immediately.')
    zone_id = data.get('zone_id', 'Global')
    
    # 1. Create a critical alert in the database
    alert = Alert(
        alert_type=emergency_type,
        message=message,
        level='critical',
        zone_id=zone_id,
        resolved=False
    )
    db.session.add(alert)
    
    # 2. Flag zone security levels
    zones = Zone.query.all()
    for z in zones:
        z.security_level = 'Critical'
        # Evacuation status adjustments
        z.status = 'Red'
        
    db.session.commit()
    
    return jsonify({
        'status': 'Emergency Mode Triggered',
        'type': emergency_type,
        'message': message,
        'zone_id': zone_id
    })

@emergency_bp.route('/api/emergency/resolve', methods=['POST'])
def resolve_emergency():
    """
    Resolves any active critical alerts, returning the stadium to normal operation.
    """
    from services.simulation import SIMULATION_OVERRIDES
    
    critical_alerts = Alert.query.filter_by(level='critical', resolved=False).all()
    for alert in critical_alerts:
        alert.resolved = True
        
    # Reset simulator overrides
    SIMULATION_OVERRIDES['weather_condition'] = None
    SIMULATION_OVERRIDES['power_cut'] = False
    SIMULATION_OVERRIDES['crowd_scale'] = 1.0
    SIMULATION_OVERRIDES['temp_adjust'] = 0.0

    # Reset security levels, temperatures, and default occupancy
    zones = Zone.query.all()
    for z in zones:
        z.security_level = 'Normal'
        z.status = 'Green'
        z.medical_incidents = 0
        z.current_crowd = int(z.capacity * 0.1)
        z.queue_length = 0
        z.temperature = 22.0
        
    db.session.commit()
    
    return jsonify({
        'status': 'Normal Operations Restored',
        'resolved_count': len(critical_alerts)
    })
