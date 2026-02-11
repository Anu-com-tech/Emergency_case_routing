from flask import Blueprint, request, jsonify

hospital_bp = Blueprint('hospital', __name__)

@hospital_bp.route('/pending-requests', methods=['GET'])
def get_pending_requests():
    """Get all pending emergency requests for hospital admin"""
    from app import db
    
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
                'created_at': req['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({
            'success': True,
            'requests': formatted_requests
        }), 200
        
    except Exception as e:
        print(f"Error in get_pending_requests: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching requests'
        }), 500

@hospital_bp.route('/accept-request', methods=['POST'])
def accept_request():
    """Accept an emergency request"""
    from app import db
    
    try:
        data = request.get_json()
        request_id = data.get('request_id')
        
        if not request_id:
            return jsonify({
                'success': False,
                'message': 'Request ID is required'
            }), 400
        
        # Update status to Accepted
        success = db.update_request_status(request_id, 'Accepted')
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Request accepted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to accept request'
            }), 500
            
    except Exception as e:
        print(f"Error in accept_request: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while accepting request'
        }), 500

@hospital_bp.route('/reject-request', methods=['POST'])
def reject_request():
    """Reject an emergency request"""
    from app import db
    
    try:
        data = request.get_json()
        request_id = data.get('request_id')
        
        if not request_id:
            return jsonify({
                'success': False,
                'message': 'Request ID is required'
            }), 400
        
        # Update status to Rejected
        success = db.update_request_status(request_id, 'Rejected')
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Request rejected successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to reject request'
            }), 500
            
    except Exception as e:
        print(f"Error in reject_request: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while rejecting request'
        }), 500
