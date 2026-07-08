import os
from flask import Flask
from flask_socketio import SocketIO
from config import Config
from database.models import db, User
from sockets.websocket import StadiumNamespace
from services.simulation import initialize_database_zones, run_simulation_loop
from routes.dashboard import dashboard_bp
from routes.prediction import prediction_bp
from routes.emergency import emergency_bp
from routes.analytics import analytics_bp
from routes.api import api_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
db.init_app(app)

# Initialize SocketIO
# We use simple threading or gevent as the async mode depending on installation
socketio = SocketIO(app, cors_allowed_origins="*")

# Register Blueprints
app.register_blueprint(dashboard_bp)
app.register_blueprint(prediction_bp)
app.register_blueprint(emergency_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(api_bp)

# Register Websocket Namespaces
socketio.on_namespace(StadiumNamespace('/'))

def setup_app():
    """
    Initializes database tables, seeds default data, and starts the background simulation thread.
    """
    with app.app_context():
        db.create_all()
        
        # Seed test admin account if not existing
        admin_exists = User.query.filter_by(username='admin').first()
        if not admin_exists:
            print("Seeding default demo users...")
            roles = ['Admin', 'Operator', 'Security', 'Volunteer', 'Medical']
            for role in roles:
                u = User(username=role.lower(), role=role)
                u.set_password('worldcup2026')
                db.session.add(u)
            db.session.commit()
            print("Seeding completed. Credentials: username='admin', password='worldcup2026'")
            
        # Seed Zones
        initialize_database_zones(app)

    # Start simulation loop in SocketIO background task
    socketio.start_background_task(run_simulation_loop, app, socketio)

# Execute setup
setup_app()

if __name__ == '__main__':
    # Host on all interfaces for network access, port 5000
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
