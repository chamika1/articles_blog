from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
import jwt
import os
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
            
        if not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'message': 'Missing required fields'}), 400

        # Check if user already exists
        existing_user = User.get_by_email(data['email'])
        if existing_user:
            return jsonify({'message': 'Email already exists'}), 400
            
        # Create new user
        user = User.create(data['username'], data['email'], data['password'])
        
        if user:
            return jsonify({'message': 'Registration successful'}), 201
        else:
            return jsonify({'message': 'Failed to create user'}), 500
            
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing email or password'}), 400
        
        user = User.get_by_email(data['email'])
        
        if not user or not check_password_hash(user['password'], data['password']):
            return jsonify({'message': 'Invalid email or password'}), 401
        
        # Include is_admin in the token payload
        token_payload = {
            'sub': str(user['_id']),
            'email': user['email'],
            'username': user['username'],
            'is_admin': user.get('is_admin', False),
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        
        # Use the JWT_SECRET_KEY from environment variables
        secret_key = os.getenv('JWT_SECRET_KEY')
        token = jwt.encode(token_payload, secret_key, algorithm='HS256')
        
        # Generate avatar URL if not already present
        if 'avatar_url' not in user:
            avatar_styles = [
                'cyberpunk_avatar',
                'futuristic_tech_avatar',
                'digital_human_avatar',
                'neon_profile_avatar',
                'sci_fi_character_avatar',
                'tech_hacker_avatar',
                'virtual_reality_avatar'
            ]
            style_index = sum(ord(c) for c in user['username']) % len(avatar_styles)
            avatar_style = avatar_styles[style_index]
            avatar_url = f"https://image.pollinations.ai/prompt/{avatar_style}_{user['username']}?width=200&height=200&nologo=true"
        else:
            avatar_url = user['avatar_url']
        
        # Remove password from user object before sending to client
        user_data = {
            '_id': str(user['_id']),
            'email': user['email'],
            'username': user['username'],
            'is_admin': user.get('is_admin', False),
            'avatar_url': avatar_url
        }
        
        return jsonify({'token': token, 'user': user_data})
    
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'message': f'Login failed: {str(e)}'}), 500