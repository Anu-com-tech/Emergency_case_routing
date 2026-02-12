from fastapi import APIRouter, HTTPException

hospitals_router = APIRouter()

# Global reference to database (will be set by app)
db = None

def set_db(database):
    """Set database instance from main app"""
    global db
    db = database

@hospitals_router.get("/")
async def get_all_hospitals():
    """Get list of all hospitals"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    try:
        hospitals = db.get_all_hospitals()
        
        formatted_hospitals = []
        for hospital in hospitals:
            formatted_hospitals.append({
                'id': hospital['id'],
                'name': hospital['name'],
                'latitude': float(hospital['latitude']),
                'longitude': float(hospital['longitude']),
                'available_beds': hospital.get('available_beds', 0),
                'available_icu': hospital.get('available_icu', 0),
                'available_oxygen': hospital.get('available_oxygen', 0),
                'available_ventilator': hospital.get('available_ventilator', 0)
            })
        
        return {
            "success": True,
            "hospitals": formatted_hospitals
        }
    except Exception as e:
        print(f"Error in get_all_hospitals: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch hospitals")
