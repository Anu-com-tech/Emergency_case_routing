from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

ambulance_router = APIRouter()

# Pydantic models for request validation
class PatientNeeds(BaseModel):
    bed: bool = True
    icu: bool = False
    oxygen: bool = False
    ventilator: bool = False

class EmergencyRequest(BaseModel):
    patient_type: str
    emergency_type: str
    needs: PatientNeeds

class RequestStatusCheck(BaseModel):
    request_id: int

# Global reference to database (will be set by app)
db = None

def set_db(database):
    """Set database instance from main app"""
    global db
    db = database

@ambulance_router.post("/find-hospital")
async def find_hospital(emergency_req: EmergencyRequest):
    """Find nearest hospital based on patient needs"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    try:
        # Get ambulance location from config
        from config import Config
        config = Config()
        ambulance_lat = config.DEFAULT_AMBULANCE_LATITUDE
        ambulance_lon = config.DEFAULT_AMBULANCE_LONGITUDE
        
        # Find nearest hospital
        nearest_hospital = db.find_nearest_hospital(
            ambulance_lat, 
            ambulance_lon, 
            emergency_req.needs.dict()
        )
        
        if not nearest_hospital:
            raise HTTPException(
                status_code=404, 
                detail="No hospital found with required facilities"
            )
        
        # Create emergency request
        request_id = db.create_emergency_request(
            emergency_req.patient_type,
            emergency_req.emergency_type,
            emergency_req.needs.dict(),
            nearest_hospital['id']
        )
        
        if not request_id:
            raise HTTPException(
                status_code=500, 
                detail="Failed to create emergency request"
            )
        
        return {
            "success": True,
            "message": "Request sent to nearest hospital",
            "hospital_name": nearest_hospital['name'],
            "distance": nearest_hospital['distance'],
            "request_id": request_id,
            "hospital_id": nearest_hospital['id']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in find_hospital: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while processing your request"
        )

@ambulance_router.post("/check-status")
async def check_status(status_check: RequestStatusCheck):
    """Check status of emergency request"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    try:
        request_data = db.get_request_status(status_check.request_id)
        
        if not request_data:
            raise HTTPException(
                status_code=404, 
                detail="Request not found"
            )
        
        return {
            "success": True,
            "request_id": request_data['id'],
            "status": request_data['status'],
            "hospital_name": request_data['hospital_name'],
            "patient_type": request_data['patient_type'],
            "emergency_type": request_data['emergency_type'],
            "created_at": request_data['created_at'].isoformat() if hasattr(request_data['created_at'], 'isoformat') else str(request_data['created_at'])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in check_status: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while checking status"
        )

@ambulance_router.get("/stats")
async def get_stats():
    """Get ambulance dashboard statistics"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    try:
        pending_requests = db.get_pending_requests()
        hospitals = db.get_all_hospitals()
        
        return {
            "success": True,
            "total_hospitals": len(hospitals),
            "pending_count": len([r for r in pending_requests if r['status'] == 'Pending']),
            "accepted_count": len([r for r in pending_requests if r['status'] == 'Accepted']),
            "response_time": "~2min"
        }
    except Exception as e:
        print(f"Error in get_stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch statistics")
