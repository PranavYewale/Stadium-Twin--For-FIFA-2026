import time
import random
from datetime import datetime, timedelta
from database.models import db, Zone, Alert, Prediction, Sustainability, Recommendation
from ai.prediction_engine import forecast_zone_telemetry
from ai.risk_engine import calculate_zone_risk
from ai.gemini import generate_gemini_recommendation
import services.camera as camera
import services.weather as weather
import services.traffic as traffic
import services.transport as transport
import services.foodcourt as foodcourt
import services.iot as iot
import services.tickets as tickets
import services.security as security
import services.medical as medical
import services.parking as parking

DEFAULT_ZONES = [
    # id, name, type, capacity
    ('gate_a', 'Gate A (North)', 'entrance', 8000),
    ('gate_b', 'Gate B (East)', 'entrance', 12000),
    ('gate_c', 'Gate C (West)', 'entrance', 10000),
    ('vip_entrance', 'VIP Club Entrance', 'entrance', 2000),
    ('stand_lower', 'Lower Tier Stands', 'stand', 35000),
    ('stand_middle', 'Mid Tier Stands', 'stand', 25000),
    ('stand_upper', 'Upper Tier Stands', 'stand', 20000),
    ('food_court_north', 'North Food Court', 'amenity', 3000),
    ('food_court_west', 'West Food Court', 'amenity', 2000),
    ('parking_east', 'Parking Lot East', 'parking', 4000),
    ('parking_west', 'Parking Lot West', 'parking', 3000),
    ('parking_vip', 'VIP Parking Lot', 'parking', 500),
    ('metro_station', 'Metro Transit Hub', 'transit', 15000),
    ('bus_stop', 'Stadium Bus Terminal', 'transit', 5000)
]

# Simulation override states
SIMULATION_OVERRIDES = {
    'weather_condition': None,  # 'Clear', 'Heavy Rain', 'Heatwave'
    'power_cut': False,         # True/False
    'crowd_scale': 1.0,         # multiplier
    'temp_adjust': 0.0          # offset
}

def initialize_database_zones(app):
    """
    Seeds the database with default stadium zone structures.
    """
    with app.app_context():
        # Check if zones already exist
        if Zone.query.first() is not None:
            return
            
        print("Initializing digital twin stadium zones...")
        for zid, name, ztype, cap in DEFAULT_ZONES:
            zone = Zone(
                id=zid,
                name=name,
                zone_type=ztype,
                capacity=cap,
                current_crowd=int(cap * 0.1), # Start with 10% occupancy
                queue_length=0,
                temperature=22.0,
                risk_score=0.0,
                status='Green',
                security_level='Normal',
                medical_incidents=0
            )
            db.session.add(zone)
        db.session.commit()
        print("Digital twin stadium initialized successfully.")

def run_simulation_loop(app, socketio):
    """
    Main simulator runner designed to run inside a SocketIO background thread.
    """
    print("Background stadium simulation started...")
    
    # Store dynamic state variables for matching arrival curve
    # Simulation starts at match warmup, slowly progresses towards match kickoff
    tick_count = 0
    
    while True:
        try:
            # Run simulation step every 3 seconds
            time.sleep(3.0)
            tick_count += 1
            
            with app.app_context():
                zones = Zone.query.all()
                if not zones:
                    continue
                
                # Fetch fresh values from external simulation modules
                weather_info = weather.get_current_weather()
                if SIMULATION_OVERRIDES['weather_condition']:
                    weather_info['condition'] = SIMULATION_OVERRIDES['weather_condition']
                    if SIMULATION_OVERRIDES['weather_condition'] == 'Heatwave':
                        weather_info['temp'] = 39.5
                if SIMULATION_OVERRIDES['temp_adjust'] != 0.0:
                    weather_info['temp'] += SIMULATION_OVERRIDES['temp_adjust']
                    
                traffic_info = traffic.get_traffic_status()
                transit_info = transport.get_transit_telemetry()
                fc_info = foodcourt.get_food_court_telemetry()
                t_scan = tickets.get_ticket_scan_metrics()
                p_occupancy = parking.get_parking_telemetry()
                
                # Calculate total attendance
                total_attendance = 0
                for zone in zones:
                    if zone.zone_type == 'stand':
                        total_attendance += zone.current_crowd
                
                iot_info = iot.get_iot_telemetry(total_attendance)
                if SIMULATION_OVERRIDES['power_cut']:
                    iot_info['energy_kwh'] = 0.0
                    iot_info['hvac_load_pct'] = 0.0
                    iot_info['carbon_footprint_kg'] = 0.0
                    
                    # Ensure power cut alert exists
                    active_pc = Alert.query.filter_by(alert_type='power_failure', resolved=False).first()
                    if not active_pc:
                        db.session.add(Alert(
                            alert_type='power_failure',
                            message='CRITICAL: Main grid power outage reported! Back-up generators active.',
                            level='critical',
                            zone_id='Global'
                        ))
                
                # Check for critical triggers (emergency flag)
                # If emergency_mode is active in db (can be set by UI), we force evacuations
                emergency_active = False
                active_critical_alert = Alert.query.filter_by(level='critical', resolved=False).first()
                if active_critical_alert:
                    emergency_active = True
                
                # 1. Update each zone
                updated_zones = []
                for zone in zones:
                    # Modify crowd and metrics depending on simulation mode
                    if emergency_active:
                        # Evacuate: move crowd out of stands/amenities towards exit gates/transit
                        if zone.zone_type in ['stand', 'amenity']:
                            reduction = int(zone.current_crowd * 0.15)
                            zone.current_crowd = max(0, zone.current_crowd - reduction)
                        elif zone.zone_type == 'entrance': # Used as exits during evacuation
                            # Surge exit crowd
                            addition = int(zone.capacity * 0.08)
                            zone.current_crowd = min(int(zone.capacity * 1.4), zone.current_crowd + addition)
                            zone.queue_length = max(0, zone.queue_length + int(addition * 0.2))
                        elif zone.zone_type == 'transit':
                            addition = int(zone.capacity * 0.1)
                            zone.current_crowd = min(zone.capacity, zone.current_crowd + addition)
                    else:
                        # Normal Simulation Pattern: slowly filling up stands
                        # Crowd comes in from transit/parking -> passes gates -> stand
                        if zone.id == 'gate_a':
                            # Scan entry
                            zone.current_crowd = int(zone.current_crowd * 0.95 + t_scan['gate_a_scans'])
                            zone.queue_length = max(0, int(zone.queue_length + (t_scan['gate_a_scans'] * 0.2) - random.randint(1, 5)))
                        elif zone.id == 'gate_b':
                            zone.current_crowd = int(zone.current_crowd * 0.95 + t_scan['gate_b_scans'])
                            zone.queue_length = max(0, int(zone.queue_length + (t_scan['gate_b_scans'] * 0.2) - random.randint(2, 6)))
                        elif zone.id == 'gate_c':
                            zone.current_crowd = int(zone.current_crowd * 0.95 + t_scan['gate_c_scans'])
                            zone.queue_length = max(0, int(zone.queue_length + (t_scan['gate_c_scans'] * 0.2) - random.randint(1, 4)))
                        elif zone.id == 'vip_entrance':
                            zone.current_crowd = int(zone.current_crowd * 0.9 + t_scan['vip_scans'])
                            zone.queue_length = max(0, int(zone.queue_length + (t_scan['vip_scans'] * 0.1) - random.randint(1, 2)))
                        elif zone.id == 'stand_lower':
                            # Flow in from gates
                            zone.current_crowd = min(zone.capacity, zone.current_crowd + random.randint(10, 40))
                        elif zone.id == 'stand_middle':
                            zone.current_crowd = min(zone.capacity, zone.current_crowd + random.randint(5, 30))
                        elif zone.id == 'stand_upper':
                            zone.current_crowd = min(zone.capacity, zone.current_crowd + random.randint(2, 20))
                        elif zone.id == 'food_court_north':
                            zone.queue_length = fc_info['food_court_north']['queue_length']
                            zone.current_crowd = int(zone.queue_length * 2.5)
                        elif zone.id == 'food_court_west':
                            zone.queue_length = fc_info['food_court_west']['queue_length']
                            zone.current_crowd = int(zone.queue_length * 2.5)
                        elif zone.id == 'parking_east':
                            zone.current_crowd = p_occupancy['parking_east']['occupied']
                        elif zone.id == 'parking_west':
                            zone.current_crowd = p_occupancy['parking_west']['occupied']
                        elif zone.id == 'parking_vip':
                            zone.current_crowd = p_occupancy['parking_vip']['occupied']
                        elif zone.id == 'metro_station':
                            zone.current_crowd = max(0, zone.current_crowd + transit_info['metro']['predicted_passengers'] - random.randint(100, 300))
                        elif zone.id == 'bus_stop':
                            zone.current_crowd = max(0, zone.current_crowd + transit_info['bus']['predicted_passengers'] - random.randint(30, 80))
                    # Update temperature and other standard variables
                    zone.temperature = round(weather_info['temp'] + random.uniform(-0.5, 1.2), 1)
                    
                    # Randomly increment medical incidents if rolls align
                    med_roll = medical.check_medical_incidents()
                    if med_roll and random.random() < 0.05:
                        zone.medical_incidents += 1
                        # Create alert
                        new_alert = Alert(
                            alert_type='medical',
                            message=f"{med_roll['msg']} at {zone.name}",
                            level=med_roll['level'],
                            zone_id=zone.id
                        )
                        db.session.add(new_alert)
                        
                    # CV analysis on cameras
                    cv_roll = camera.process_cctv_cv(zone.id)
                    if cv_roll['detected']:
                        new_alert = Alert(
                            alert_type=cv_roll['anomaly_type'],
                            message=cv_roll['message'],
                            level=cv_roll['level'],
                            zone_id=zone.id
                        )
                        db.session.add(new_alert)
                        # Elevate security levels
                        if cv_roll['level'] == 'critical':
                            zone.security_level = 'Critical'
                        elif cv_roll['level'] == 'warning':
                            zone.security_level = 'High'
                            
                    # Recalculate Risk & Status
                    risk, status = calculate_zone_risk(
                        zone.current_crowd,
                        zone.capacity,
                        zone.queue_length,
                        zone.medical_incidents,
                        zone.security_level
                    )
                    zone.risk_score = risk
                    zone.status = status
                    
                    updated_zones.append(zone.to_dict())
                    
                # 2. Run Predictions for all zones (Every 10 seconds or every simulation cycle)
                # Clear past predictions
                db.session.query(Prediction).delete()
                
                prediction_dicts = []
                for zone in zones:
                    forecasts = forecast_zone_telemetry(
                        zone.id, zone.current_crowd, zone.capacity, zone.queue_length, zone.zone_type
                    )
                    for f in forecasts:
                        pred = Prediction(
                            zone_id=zone.id,
                            time_offset=f['time_offset'],
                            predicted_crowd=f['predicted_crowd'],
                            predicted_queue=f['predicted_queue'],
                            risk_score=f['risk_score'],
                            confidence=f['confidence']
                        )
                        db.session.add(pred)
                        prediction_dicts.append(pred.to_dict())
                        
                # 3. Update Sustainability Metrics
                sus = Sustainability(
                    energy_kwh=iot_info['energy_kwh'],
                    water_liters=iot_info['water_liters_sec'] * 3.0, # aggregate flow over tick
                    waste_kg=total_attendance * 0.005, # ~5g of waste per person per 3 seconds
                    carbon_footprint_kg=iot_info['carbon_footprint_kg'],
                    sustainability_score=max(50.0, 100.0 - (iot_info['energy_kwh']/2000.0 * 20.0) - (iot_info['water_liters_sec']/30.0 * 10.0))
                )
                db.session.add(sus)
                
                # Limit size of sustainability history (keep last 50)
                sus_count = Sustainability.query.count()
                if sus_count > 50:
                    oldest_sus = Sustainability.query.order_by(Sustainability.timestamp.asc()).first()
                    db.session.delete(oldest_sus)
                
                db.session.commit()
                
                # 4. Run Gemini AI Decision Engine (every 3 ticks / ~10 seconds to throttle calls)
                if tick_count % 3 == 0 or tick_count == 1:
                    # Gather active alerts
                    alerts = Alert.query.filter_by(resolved=False).all()
                    alerts_list = [a.to_dict() for a in alerts]
                    
                    # Generate recommendations
                    ai_rec_data = generate_gemini_recommendation(
                        updated_zones,
                        prediction_dicts[:30], # Limit to avoid huge prompt
                        alerts_list,
                        weather_info
                    )
                    
                    # Clear past recommendation history (to prevent bloat, keep last 10)
                    db.session.query(Recommendation).filter_by(resolved=False).delete()
                    
                    # Add new ones
                    for action in ai_rec_data.get('priority_actions', []):
                        rec = Recommendation(
                            priority=action.get('priority', 'Medium'),
                            location=action.get('location'),
                            issue=ai_rec_data.get('analysis', 'Risk assessment flagged'),
                            recommendation=action.get('description', ''),
                            expected_outcome=action.get('expected_outcome')
                        )
                        db.session.add(rec)
                    db.session.commit()
                    
                    # Broadcast the new AI analysis and announcement
                    socketio.emit('ai_recommendation', {
                        'analysis': ai_rec_data.get('analysis'),
                        'announcement': ai_rec_data.get('public_announcement'),
                        'actions': ai_rec_data.get('priority_actions')
                    })
                    
                # 5. Broadcast global status to WebSockets
                active_alerts = [a.to_dict() for a in Alert.query.filter_by(resolved=False).all()]
                latest_sus = Sustainability.query.order_by(Sustainability.timestamp.desc()).first()
                
                socketio.emit('stadium_update', {
                    'zones': updated_zones,
                    'weather': weather_info,
                    'traffic': traffic_info,
                    'transit': transit_info,
                    'sustainability': latest_sus.to_dict() if latest_sus else {},
                    'alerts': active_alerts,
                    'attendance': total_attendance,
                    'match_info': {
                        'status': 'Second Half' if tick_count > 60 else 'First Half',
                        'teams': 'USA vs England',
                        'score': f"{random.randint(0,2)} - {random.randint(0,2)}"
                    }
                })
                
        except Exception as e:
            print(f"Error in simulation loop: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(5.0)
