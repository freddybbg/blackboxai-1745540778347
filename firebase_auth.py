import firebase_admin
from firebase_admin import auth, credentials
from flask import request, jsonify
from functools import wraps

# Initialize Firebase Admin SDK
cred = credentials.Certificate('path/to/your/firebase-service-account.json')
firebase_admin.initialize_app(cred)

def verify_firebase_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        return None

def firebase_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return jsonify({'message': 'Authorization header missing'}), 401
        
        parts = auth_header.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            return jsonify({'message': 'Invalid authorization header'}), 401
        
        token = parts[1]
        decoded_token = verify_firebase_token(token)
        if not decoded_token:
            return jsonify({'message': 'Invalid or expired token'}), 401
        
        request.user = decoded_token
        return f(*args, **kwargs)
    return decorated_function
