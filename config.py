import os

class Config:
    """Application configuration class"""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # MySQL Database Configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'  # Change this to your MySQL username
    MYSQL_PASSWORD = 'Anushika@6002'  # Change this to your MySQL password
    MYSQL_DB = 'emergency_routing_db'
    MYSQL_PORT = 3306
    
    # Application Settings
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    
    # Ambulance location (default - can be changed)
    DEFAULT_AMBULANCE_LATITUDE = 11.0168
    DEFAULT_AMBULANCE_LONGITUDE = 76.9558