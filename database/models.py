from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False)  # Admin, Operator, Security, Volunteer, Medical

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Zone(db.Model):
    __tablename__ = 'zones'
    id = db.Column(db.String(64), primary_key=False, unique=True, index=True)
    # We use a string ID like 'gate_a', 'stand_101', 'parking_east', 'metro_station'
    db_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    zone_type = db.Column(db.String(32), nullable=False) # entrance, Stand, parking, transit, amenity, concourse
    current_crowd = db.Column(db.Integer, default=0)
    capacity = db.Column(db.Integer, default=1000)
    queue_length = db.Column(db.Integer, default=0)
    temperature = db.Column(db.Float, default=22.0)
    risk_score = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(16), default='Green')  # Green, Yellow, Orange, Red
    security_level = db.Column(db.String(16), default='Normal')  # Normal, Elevated, High, Critical
    medical_incidents = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'zone_type': self.zone_type,
            'current_crowd': self.current_crowd,
            'capacity': self.capacity,
            'queue_length': self.queue_length,
            'temperature': self.temperature,
            'risk_score': self.risk_score,
            'status': self.status,
            'security_level': self.security_level,
            'medical_incidents': self.medical_incidents,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(64), nullable=False) # fire, fight, stampede, medical, parking, queue, weather
    message = db.Column(db.String(256), nullable=False)
    level = db.Column(db.String(16), default='info') # info, warning, critical
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    resolved = db.Column(db.Boolean, default=False, index=True)
    zone_id = db.Column(db.String(64), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'alert_type': self.alert_type,
            'message': self.message,
            'level': self.level,
            'timestamp': self.timestamp.isoformat() if self.timestamp else datetime.utcnow().isoformat(),
            'resolved': self.resolved,
            'zone_id': self.zone_id
        }

class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    zone_id = db.Column(db.String(64), nullable=False, index=True)
    time_offset = db.Column(db.Integer, nullable=False) # 15, 30, 60 minutes
    predicted_crowd = db.Column(db.Integer, nullable=False)
    predicted_queue = db.Column(db.Integer, nullable=False)
    risk_score = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'zone_id': self.zone_id,
            'time_offset': self.time_offset,
            'predicted_crowd': self.predicted_crowd,
            'predicted_queue': self.predicted_queue,
            'risk_score': self.risk_score,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat() if self.timestamp else datetime.utcnow().isoformat()
        }

class Sustainability(db.Model):
    __tablename__ = 'sustainability'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    energy_kwh = db.Column(db.Float, default=0.0)
    water_liters = db.Column(db.Float, default=0.0)
    waste_kg = db.Column(db.Float, default=0.0)
    carbon_footprint_kg = db.Column(db.Float, default=0.0)
    sustainability_score = db.Column(db.Float, default=100.0)

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else datetime.utcnow().isoformat(),
            'energy_kwh': self.energy_kwh,
            'water_liters': self.water_liters,
            'waste_kg': self.waste_kg,
            'carbon_footprint_kg': self.carbon_footprint_kg,
            'sustainability_score': self.sustainability_score
        }

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.String(16), default='Medium') # Low, Medium, High, Critical
    location = db.Column(db.String(64), nullable=True)
    issue = db.Column(db.String(256), nullable=False)
    recommendation = db.Column(db.Text, nullable=False)
    expected_outcome = db.Column(db.String(256), nullable=True)
    resolved = db.Column(db.Boolean, default=False, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else datetime.utcnow().isoformat(),
            'priority': self.priority,
            'location': self.location,
            'issue': self.issue,
            'recommendation': self.recommendation,
            'expected_outcome': self.expected_outcome,
            'resolved': self.resolved
        }
