from flask import Blueprint, jsonify, request
from database.models import db, Zone, Alert, Prediction, Sustainability, Recommendation
from datetime import datetime
import random
from services.simulation import SIMULATION_OVERRIDES

api_bp = Blueprint('api', __name__)

# --- GET ENDPOINTS ---

@api_bp.route('/api/dashboard')
def get_dashboard_summary():
    zones = Zone.query.all()
    alerts = Alert.query.filter_by(resolved=False).all()
    recs = Recommendation.query.all()
    
    total_attendance = sum(z.current_crowd for z in zones if z.zone_type.lower() == 'stand')
    total_capacity = sum(z.capacity for z in zones if z.zone_type.lower() == 'stand')
    
    # Calculate average risk
    avg_risk = sum(z.risk_score for z in zones) / max(1, len(zones))
    
    return jsonify({
        'attendance': total_attendance,
        'capacity': total_capacity,
        'occupancy_percentage': round((total_attendance / max(1, total_capacity)) * 100, 1),
        'active_alerts_count': len(alerts),
        'average_risk_score': round(avg_risk, 1),
        'recommendations_count': len(recs)
    })

@api_bp.route('/map')
def get_map_markers():
    zones = Zone.query.all()
    markers = []
    for z in zones:
        markers.append({
            'id': z.id,
            'name': z.name,
            'type': z.zone_type,
            'current_crowd': z.current_crowd,
            'capacity': z.capacity,
            'status': z.status,
            'risk_score': z.risk_score
        })
    return jsonify(markers)

@api_bp.route('/crowd')
def get_crowd_metrics():
    zones = Zone.query.all()
    stands = [z.to_dict() for z in zones if z.zone_type.lower() == 'stand']
    entrances = [z.to_dict() for z in zones if z.zone_type.lower() == 'entrance']
    return jsonify({
        'stands': stands,
        'entrances': entrances,
        'total_stands_crowd': sum(s['current_crowd'] for s in stands)
    })

@api_bp.route('/weather', methods=['GET', 'POST'])
def handle_weather():
    if request.method == 'GET':
        # Return mock weather stats
        return jsonify({
            'temp': 24.5,
            'humidity': 62,
            'condition': 'Partly Cloudy',
            'precipitation_chance': 10
        })
    else:
        # POST to update weather
        data = request.json or {}
        return jsonify({'status': 'weather updated', 'received': data})

@api_bp.route('/traffic', methods=['GET', 'POST'])
def handle_traffic():
    if request.method == 'GET':
        return jsonify({
            'status': 'Elevated Delays',
            'average_speed_mph': 28.5,
            'delay_minutes': 18
        })
    else:
        # POST
        data = request.json or {}
        return jsonify({'status': 'traffic data posted', 'received': data})

@api_bp.route('/predictions')
def get_predictions_api():
    preds = Prediction.query.all()
    return jsonify([p.to_dict() for p in preds])

@api_bp.route('/recommendations')
def get_recommendations_api():
    recs = Recommendation.query.all()
    return jsonify([r.to_dict() for r in recs])

@api_bp.route('/reports')
def get_reports_api():
    # Return list of generated reports (stub)
    return jsonify([
        {
            'name': 'stadium_digital_twin_report.pdf',
            'timestamp': datetime.utcnow().isoformat(),
            'size_bytes': 152000
        }
    ])


# --- POST ENDPOINTS ---

@api_bp.route('/sensor', methods=['POST'])
def post_sensor_data():
    data = request.json or {}
    zone_id = data.get('zone_id')
    metric = data.get('metric') # 'crowd', 'temperature', 'queue_length'
    value = data.get('value')
    
    zone = Zone.query.filter_by(id=zone_id).first()
    if not zone:
        return jsonify({'error': 'Zone not found'}), 404
        
    if metric == 'crowd':
        zone.current_crowd = int(value)
    elif metric == 'temperature':
        zone.temperature = float(value)
    elif metric == 'queue_length':
        zone.queue_length = int(value)
        
    db.session.commit()
    return jsonify({'status': 'success', 'updated_zone': zone.to_dict()})

@api_bp.route('/camera', methods=['POST'])
def post_camera_feed():
    data = request.json or {}
    zone_id = data.get('zone_id')
    incident_type = data.get('incident_type') # e.g. fight, smoke
    message = data.get('message', 'Incident detected')
    level = data.get('level', 'warning')
    
    alert = Alert(
        alert_type=incident_type,
        message=message,
        level=level,
        zone_id=zone_id,
        resolved=False
    )
    db.session.add(alert)
    
    zone = Zone.query.filter_by(id=zone_id).first()
    if zone:
        zone.security_level = 'High' if level == 'warning' else 'Critical'
        zone.status = 'Orange' if level == 'warning' else 'Red'
        
    db.session.commit()
    return jsonify({'status': 'success', 'created_alert': alert.to_dict()})

@api_bp.route('/tickets', methods=['POST'])
def post_tickets_data():
    data = request.json or {}
    gate_id = data.get('gate_id')
    scan_count = data.get('scan_count', 1)
    
    zone = Zone.query.filter_by(id=gate_id).first()
    if not zone:
        return jsonify({'error': 'Gate not found'}), 404
        
    zone.current_crowd += scan_count
    db.session.commit()
    return jsonify({'status': 'success', 'current_crowd': zone.current_crowd})

@api_bp.route('/security', methods=['POST'])
def post_security_incident():
    data = request.json or {}
    msg = data.get('message', 'Security Alarm')
    zone_id = data.get('zone_id')
    level = data.get('level', 'warning')
    
    alert = Alert(
        alert_type='security',
        message=msg,
        level=level,
        zone_id=zone_id,
        resolved=False
    )
    db.session.add(alert)
    db.session.commit()
    return jsonify({'status': 'success', 'alert': alert.to_dict()})

@api_bp.route('/parking', methods=['POST'])
def post_parking_sensor():
    data = request.json or {}
    lot_id = data.get('lot_id')
    occupied = data.get('occupied')
    
    zone = Zone.query.filter_by(id=lot_id).first()
    if not zone:
        return jsonify({'error': 'Parking lot not found'}), 404
        
    zone.current_crowd = occupied
    db.session.commit()
    return jsonify({'status': 'success', 'updated_parking': zone.to_dict()})

@api_bp.route('/emergency', methods=['POST'])
def post_emergency():
    # Direct forward to emergency blueprint trigger or replicate here
    data = request.json or {}
    alert = Alert(
        alert_type=data.get('type', 'Evacuation'),
        message=data.get('message', 'Emergency triggered'),
        level='critical',
        zone_id=data.get('zone_id', 'Global')
    )
    db.session.add(alert)
    db.session.commit()
    return jsonify({'status': 'success', 'emergency_alert': alert.to_dict()})


# --- PUT ENDPOINTS ---

@api_bp.route('/update-zone', methods=['PUT'])
def update_zone_data():
    data = request.json or {}
    zone_id = data.get('zone_id')
    zone = Zone.query.filter_by(id=zone_id).first()
    if not zone:
        return jsonify({'error': 'Zone not found'}), 404
        
    if 'current_crowd' in data:
        zone.current_crowd = int(data['current_crowd'])
    if 'capacity' in data:
        zone.capacity = int(data['capacity'])
    if 'queue_length' in data:
        zone.queue_length = int(data['queue_length'])
    if 'status' in data:
        zone.status = data['status']
        
    db.session.commit()
    return jsonify({'status': 'success', 'updated_zone': zone.to_dict()})

@api_bp.route('/update-gate', methods=['PUT'])
def update_gate_data():
    data = request.json or {}
    gate_id = data.get('gate_id')
    zone = Zone.query.filter_by(id=gate_id).first()
    if not zone or zone.zone_type != 'entrance':
        return jsonify({'error': 'Gate not found or not an entrance type'}), 404
        
    if 'queue_length' in data:
        zone.queue_length = int(data['queue_length'])
    if 'capacity' in data:
        zone.capacity = int(data['capacity'])
        
    db.session.commit()
    return jsonify({'status': 'success', 'updated_gate': zone.to_dict()})


# --- DELETE ENDPOINTS ---

@api_bp.route('/alert', methods=['DELETE'])
def delete_alert():
    alert_id = request.args.get('id')
    if not alert_id:
        return jsonify({'error': 'Missing alert id parameter'}), 400
        
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
        
    db.session.delete(alert)
    db.session.commit()
    return jsonify({'status': 'success', 'deleted_alert_id': alert_id})

# --- SIMULATION OVERRIDES ---

@api_bp.route('/api/simulation/override', methods=['POST'])
def update_simulation_override():
    data = request.json or {}
    
    if 'weather_condition' in data:
        SIMULATION_OVERRIDES['weather_condition'] = data['weather_condition']
    if 'power_cut' in data:
        SIMULATION_OVERRIDES['power_cut'] = bool(data['power_cut'])
        # If power cut is resolved, also resolve the critical alert
        if not data['power_cut']:
            pf_alert = Alert.query.filter_by(alert_type='power_failure', resolved=False).first()
            if pf_alert:
                pf_alert.resolved = True
                
            # Restores grid sustainability status
            sustainability_score = 98.4
            
    if 'crowd_scale' in data:
        new_scale = float(data['crowd_scale'])
        old_scale = SIMULATION_OVERRIDES.get('crowd_scale', 1.0)
        if old_scale <= 0.0:
            old_scale = 1.0
        SIMULATION_OVERRIDES['crowd_scale'] = new_scale
        
        # Scale existing crowds once to reflect instant UI change
        relative_scale = new_scale / old_scale
        zones = Zone.query.all()
        for z in zones:
            z.current_crowd = min(int(z.capacity * 1.3), max(0, int(z.current_crowd * relative_scale)))
            z.queue_length = min(200, max(0, int(z.queue_length * relative_scale)))
    if 'temp_adjust' in data:
        SIMULATION_OVERRIDES['temp_adjust'] = float(data['temp_adjust'])
        
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'overrides': SIMULATION_OVERRIDES
    })

# --- SPECIALIST ASSISTANT ENDPOINTS ---

@api_bp.route('/api/assistant/lost-child', methods=['POST'])
def lost_child_search():
    data = request.json or {}
    name = data.get('name', 'Child')
    color = data.get('color', 'Red')
    last_seen = data.get('last_seen', 'gate_a')
    
    # AI Camera Search simulation: child spotted adjacent to last seen based on crowd flow
    zone_connections = {
        'gate_a': 'stand_lower',
        'gate_b': 'stand_middle',
        'gate_c': 'stand_upper',
        'vip_entrance': 'parking_vip',
        'stand_lower': 'food_court_north',
        'stand_middle': 'food_court_west',
        'stand_upper': 'metro_station',
        'food_court_north': 'gate_a',
        'food_court_west': 'gate_c',
        'parking_east': 'gate_b',
        'parking_west': 'gate_c',
        'parking_vip': 'vip_entrance',
        'metro_station': 'gate_a',
        'bus_stop': 'gate_c'
    }
    
    spotted_zone_id = zone_connections.get(last_seen, 'stand_lower')
    zone = Zone.query.filter_by(id=spotted_zone_id).first() or Zone.query.first()
    
    # Generate alert
    new_alert = Alert(
        alert_type='lost_child',
        message=f"MISSING PERSON: {name} ({color} shirt) spotted near {zone.name}. Volunteers dispatched.",
        level='critical',
        zone_id=zone.id
    )
    db.session.add(new_alert)
    db.session.commit()
    
    return jsonify({
        'spotted_zone': zone.to_dict(),
        'message': f"Grid sweep active. Search cameras spotted matching subject at {zone.name}.",
        'alert_id': new_alert.id
    })

@api_bp.route('/api/assistant/accessibility', methods=['POST'])
def accessibility_assist():
    data = request.json or {}
    source = data.get('source', 'parking_east')
    dest = data.get('destination', 'stand_lower')
    assist_type = data.get('type', 'wheelchair')
    
    routes = {
        'wheelchair': [
            "Enter via East ramp elevator bank E1",
            "Take Lift E1 to concourse level 2",
            "Proceed via step-free corridor toward Sector Lower A"
        ],
        'visually_impaired': [
            "Bleep beacon active on Gate B entry path",
            "Tactile paving guides to concourse Sector B",
            "Proceed 30 meters straight, turn right at concessions."
        ]
    }
    
    selected_route = routes.get(assist_type, routes['wheelchair'])
    elevator_wait = random_element_wait = random.randint(2, 6)
    
    return jsonify({
        'route': selected_route,
        'elevator_wait_min': elevator_wait,
        'restroom_location': 'Parking VIP (Fully Accessible)',
        'seating_block': 'Block Lower 108 (Wheelchair spaces available)'
    })

@api_bp.route('/api/assistant/queue-optimize', methods=['POST'])
def queue_optimize():
    zones = Zone.query.all()
    reassignments = []
    
    food_north = Zone.query.filter_by(id='food_court_north').first()
    food_west = Zone.query.filter_by(id='food_court_west').first()
    
    if food_north and food_north.queue_length > 15:
        food_north.queue_length = max(2, food_north.queue_length - 8)
        reassignments.append("Assigned 3 temporary counters at North Food Court")
        
    if food_west and food_west.queue_length > 15:
        food_west.queue_length = max(2, food_west.queue_length - 6)
        reassignments.append("Reallocated 2 operators to West Food Court checkout lanes")
        
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'actions': reassignments if reassignments else ["Queues optimal. Staff balances within margins."]
    })

@api_bp.route('/api/assistant/sentiment', methods=['GET'])
def sentiment_analysis():
    zones = Zone.query.all()
    avg_risk = sum(z.risk_score for z in zones) / max(1, len(zones))
    happiness = max(45.0, round(96.0 - (avg_risk * 0.4), 1))
    
    hotspots = []
    if avg_risk > 30:
        hotspots.append({'location': 'Metro Station', 'issue': 'Long wait lines'})
    if any(z.queue_length > 15 for z in zones):
        hotspots.append({'location': 'Food Courts', 'issue': 'Food counter bottlenecks'})
        
    if not hotspots:
        hotspots.append({'location': 'None', 'issue': 'Nominal feedback'})
        
    feed = [
        {"user": "@stadiumfan26", "text": "Stands are rocking! USA vs ENG is crazy! #wc2026", "sentiment": "positive"},
        {"user": "@soccerqueen", "text": "Restrooms near Gate C are clean, thanks to sanitation staff!", "sentiment": "positive"},
        {"user": "@transitguy", "text": "Bus lines are packing up outside parking lot east. #stadiumtransit", "sentiment": "negative"}
    ]
    
    return jsonify({
        'happiness_score': happiness,
        'hotspots': hotspots,
        'trending_tags': [
            {'tag': '#restroom-lines', 'count': 4 if avg_risk > 20 else 1},
            {'tag': '#cold-drinks', 'count': 8},
            {'tag': '#matchdayglow', 'count': 23}
        ],
        'feed': feed
    })
