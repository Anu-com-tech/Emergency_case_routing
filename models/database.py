import mysql.connector
from mysql.connector import Error
import math

class Database:
    """Database connection and operations manager"""
    
    def __init__(self, config):
        """Initialize database connection"""
        self.config = config
        self.connection = None
        
    def connect(self):
        """Create database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.config.MYSQL_HOST,
                user=self.config.MYSQL_USER,
                password=self.config.MYSQL_PASSWORD,
                database=self.config.MYSQL_DB,
                port=self.config.MYSQL_PORT
            )
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two coordinates using Haversine formula"""
        R = 6371  # Earth's radius in kilometers
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat / 2) ** 2 + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance
    
    def find_nearest_hospital(self, ambulance_lat, ambulance_lon, needs):
        """Find nearest hospital with required facilities"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Build query based on needs
            query = """
                SELECT * FROM hospitals 
                WHERE available_beds > 0
            """
            
            if needs.get('icu'):
                query += " AND available_icu > 0"
            if needs.get('oxygen'):
                query += " AND available_oxygen > 0"
            if needs.get('ventilator'):
                query += " AND available_ventilator > 0"
            
            cursor.execute(query)
            hospitals = cursor.fetchall()
            
            if not hospitals:
                return None
            
            # Calculate distances and find nearest
            nearest_hospital = None
            min_distance = float('inf')
            
            for hospital in hospitals:
                distance = self.calculate_distance(
                    ambulance_lat, ambulance_lon,
                    float(hospital['latitude']), float(hospital['longitude'])
                )
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_hospital = hospital
                    nearest_hospital['distance'] = round(distance, 2)
            
            cursor.close()
            return nearest_hospital
            
        except Error as e:
            print(f"Error finding nearest hospital: {e}")
            return None
    
    def create_emergency_request(self, patient_type, emergency_type, needs, hospital_id):
        """Create new emergency request"""
        try:
            cursor = self.connection.cursor()
            
            query = """
                INSERT INTO emergency_requests 
                (patient_type, emergency_type, need_bed, need_icu, need_oxygen, need_ventilator, hospital_id, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'Pending')
            """
            
            values = (
                patient_type,
                emergency_type,
                True,  # Bed is always mandatory
                needs.get('icu', False),
                needs.get('oxygen', False),
                needs.get('ventilator', False),
                hospital_id
            )
            
            cursor.execute(query, values)
            self.connection.commit()
            request_id = cursor.lastrowid
            cursor.close()
            
            return request_id
            
        except Error as e:
            print(f"Error creating emergency request: {e}")
            self.connection.rollback()
            return None
    
    def get_pending_requests(self):
        """Get all pending emergency requests"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
                SELECT er.*, h.name as hospital_name
                FROM emergency_requests er
                JOIN hospitals h ON er.hospital_id = h.id
                WHERE er.status = 'Pending'
                ORDER BY er.created_at DESC
            """
            
            cursor.execute(query)
            requests = cursor.fetchall()
            cursor.close()
            
            return requests
            
        except Error as e:
            print(f"Error fetching pending requests: {e}")
            return []
    
    def get_request_status(self, request_id):
        """Get status of a specific request"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
                SELECT er.*, h.name as hospital_name
                FROM emergency_requests er
                JOIN hospitals h ON er.hospital_id = h.id
                WHERE er.id = %s
            """
            
            cursor.execute(query, (request_id,))
            request = cursor.fetchone()
            cursor.close()
            
            return request
            
        except Error as e:
            print(f"Error fetching request status: {e}")
            return None
    
    def update_request_status(self, request_id, status):
        """Update request status (Accept/Reject)"""
        try:
            cursor = self.connection.cursor()
            
            query = "UPDATE emergency_requests SET status = %s WHERE id = %s"
            cursor.execute(query, (status, request_id))
            self.connection.commit()
            cursor.close()
            
            return True
            
        except Error as e:
            print(f"Error updating request status: {e}")
            self.connection.rollback()
            return False
    
    def get_all_hospitals(self):
        """Get all hospitals"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM hospitals")
            hospitals = cursor.fetchall()
            cursor.close()
            return hospitals
        except Error as e:
            print(f"Error fetching hospitals: {e}")
            return []


