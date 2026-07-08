import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fifa-world-cup-2026-digital-twin-secret-key-999')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "digital_twin.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Gemini API settings
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    
    # Simulation Settings
    SIMULATION_INTERVAL = 3.0  # seconds between updates
