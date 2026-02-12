import os

class Config:
    """Application configuration class"""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # MySQL Database Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'Anushika@6002'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'emergency_routing_db'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)
    
    # Application Settings
    DEBUG = os.environ.get('DEBUG') or True
    TEMPLATES_AUTO_RELOAD = True
    
    # Ambulance location (default - Coimbatore, Tamil Nadu, India)
    DEFAULT_AMBULANCE_LATITUDE = float(os.environ.get('DEFAULT_AMBULANCE_LATITUDE') or 11.0168)
    DEFAULT_AMBULANCE_LONGITUDE = float(os.environ.get('DEFAULT_AMBULANCE_LONGITUDE') or 76.9558)
    
    # API Settings
    API_TITLE = "Emergency Routing System API"
    API_VERSION = "1.0.0"
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
