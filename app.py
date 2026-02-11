from flask import Flask, render_template
from config import Config
from models.database import Database

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
config = Config()
db = Database(config)

# Connect to database
if not db.connect():
    print("Failed to connect to database!")
    exit(1)

# Import and register blueprints
from routes.ambulance import ambulance_bp
from routes.hospital import hospital_bp

app.register_blueprint(ambulance_bp, url_prefix='/ambulance')
app.register_blueprint(hospital_bp, url_prefix='/hospital')

@app.route('/')
def index():
    """Main page with both panels"""
    return render_template('index.html')

@app.teardown_appcontext
def close_db(error):
    """Close database connection when app context ends"""
    if db and db.connection:
        db.disconnect()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
