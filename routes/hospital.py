from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

hospital_router = APIRouter()

class RequestAction(BaseModel):
    request_id: int

# Global reference to database (will be set by app)
db = None

def set_db(database):
    """Set database instance from main app"""
    global db
    db = database

@hospital_router.get("/pending-requests")
async def get_pending_requests():
    """Get all pending emergency requests for hospital admin"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    try:
        pending_requests = db.get_pending_requests()
        
        # Format the response
        formatted_requests = []
        for req in pending_requests:
            formatted_requests.append({
                'id': req['id'],
                'patient_type': req['patient_type'],
                'emergency_type': req['emergency_type'],
                'need_bed': req['need_bed'],
                'need_icu': req['need_icu'],
                'need_oxygen': req['need_oxygen'],
                'need_ventilator': req['need_ventilator'],
                'hospital_name': req['hospital_name'],
                'status': req['status'],
                'created_at': req['created_at'].isoformat() if hasattr(req['created_at'], 'isoformat') else str(req['created_at'])
            })
        
        return {
            "success": True,
            "requests": formatted_requests
        }
        
    except Exception as e:
        print(f"Error in get_pending_requests: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while fetching requests"
        )

@hospital_router.post("/accept-request")
async def accept_request(action: RequestAction):
    """Accept an emergency request"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    try:
        if not action.request_id:
            raise HTTPException(status_code=400, detail="Request ID is required")
        
        # Update status to Accepted
        success = db.update_request_status(action.request_id, 'Accepted')
        
        if success:
            return {
                "success": True,
                "message": "Request accepted successfully"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to accept request")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in accept_request: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while accepting request"
        )

@hospital_router.post("/reject-request")
async def reject_request(action: RequestAction):
    """Reject an emergency request"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    try:
        if not action.request_id:
            raise HTTPException(status_code=400, detail="Request ID is required")
        
        # Update status to Rejected
        success = db.update_request_status(action.request_id, 'Rejected')
        
        if success:
            return {
                "success": True,
                "message": "Request rejected successfully"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to reject request")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in reject_request: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while rejecting request"
        )
