import os
import secrets

class Config:
    # Use dynamic cryptographically secure secret key if environment doesn't specify one
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "digital_twin.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session Cookie Security flags
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Gemini API settings
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    
    # Force Offline Fallback Mode (highly recommended for free hosts like PythonAnywhere)
    OFFLINE_MODE = os.environ.get('OFFLINE_MODE', 'False').lower() in ('true', '1', 'yes') or 'pythonanywhere' in os.environ.get('PYTHONANYWHERE_DOMAIN', '').lower()
    
    # Simulation Settings
    SIMULATION_INTERVAL = 3.0  # seconds between updates
