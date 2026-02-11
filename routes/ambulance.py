from flask import Blueprint, request, jsonify, render_template, session

ambulance_bp = Blueprint('ambulance', __name__)

@ambulance_bp.route('/find-hospital', methods=['POST'])
def find_hospital():
    """Find nearest hospital based on patient needs"""
    from app import db, config
    
    try:
        data = request.get_json()
        
        # Extract form data
        patient_type = data.get('patient_type')
        emergency_type = data.get('emergency_type')
        needs = {
            'bed': True,  # Always mandatory
            'icu': data.get('need_icu', False),
            'oxygen': data.get('need_oxygen', False),
            'ventilator': data.get('need_ventilator', False)
        }
        
        # Ambulance location (using default from config)
        ambulance_lat = config.DEFAULT_AMBULANCE_LATITUDE
        ambulance_lon = config.DEFAULT_AMBULANCE_LONGITUDE
        
        # Find nearest hospital
        nearest_hospital = db.find_nearest_hospital(ambulance_lat, ambulance_lon, needs)
        
        if not nearest_hospital:
            return jsonify({
                'success': False,
                'message': 'No hospital found with required facilities'
            }), 404
        
        # Create emergency request
        request_id = db.create_emergency_request(
            patient_type, 
            emergency_type, 
            needs, 
            nearest_hospital['id']
        )
        
        if not request_id:
            return jsonify({
                'success': False,
                'message': 'Failed to create emergency request'
            }), 500
        
        # Store request ID in session for status tracking
        session['last_request_id'] = request_id
        
        return jsonify({
            'success': True,
            'message': 'Request sent to nearest hospital',
            'hospital_name': nearest_hospital['name'],
            'distance': nearest_hospital['distance'],
            'request_id': request_id
        }), 200
        
    except Exception as e:
        print(f"Error in find_hospital: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your request'
        }), 500

@ambulance_bp.route('/status')
def view_status():
    """View status page for ambulance staff"""
    return render_template('status.html')

@ambulance_bp.route('/check-status', methods=['POST'])
def check_status():
    """Check status of emergency request"""
    from app import db
    
    try:
        data = request.get_json()
        request_id = data.get('request_id') or session.get('last_request_id')
        
        if not request_id:
            return jsonify({
                'success': False,
                'message': 'No request ID provided'
            }), 400
        
        # Get request status
        request_data = db.get_request_status(request_id)
        
        if not request_data:
            return jsonify({
                'success': False,
                'message': 'Request not found'
            }), 404
        
        return jsonify({
            'success': True,
            'request_id': request_data['id'],
            'status': request_data['status'],
            'hospital_name': request_data['hospital_name'],
            'patient_type': request_data['patient_type'],
            'emergency_type': request_data['emergency_type']
        }), 200
        
    except Exception as e:
        print(f"Error in check_status: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while checking status'
        }), 500
