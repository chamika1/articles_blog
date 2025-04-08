import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

def create_token(user_id):
    payload = {
        'user_id': str(user_id),
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, os.getenv('SECRET_KEY', 'your-secret-key'), algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY', 'your-secret-key'), algorithms=['HS256'])
        return payload['user_id']
    except:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Print token for debugging
            print(f"Received token: {token[:10]}...")
            
            # Decode the token
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
            
            # Get user from database
            from app.models.user import User
            from bson import ObjectId
            
            user_id = payload['sub']
            current_user = User.get_by_id(ObjectId(user_id))
            
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
                
            # Pass the current user to the route function
            return f(current_user, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError as e:
            print(f"Invalid token error: {str(e)}")
            return jsonify({'message': 'Invalid token!'}), 401
        except Exception as e:
            print(f"Token validation error: {str(e)}")
            return jsonify({'message': f'Token validation error: {str(e)}'}), 401
            
    return decorated