from app.utils.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
import random

class User:
    @staticmethod
    def create(username, email, password):
        db = get_db()
        
        # Check if user with this email already exists
        if db.users.find_one({'email': email}):
            return None
        
        # Generate a unique avatar URL based on username
        avatar_styles = [
            'cyberpunk_avatar',
            'futuristic_tech_avatar',
            'digital_human_avatar',
            'neon_profile_avatar',
            'sci_fi_character_avatar',
            'tech_hacker_avatar',
            'virtual_reality_avatar'
        ]
        
        # Use username to consistently select the same style
        style_index = sum(ord(c) for c in username) % len(avatar_styles)
        avatar_style = avatar_styles[style_index]
        avatar_url = f"https://image.pollinations.ai/prompt/{avatar_style}_{username}?width=200&height=200&nologo=true"
            
        # Create new user
        new_user = {
            'username': username,
            'email': email,
            'password': generate_password_hash(password),
            'is_admin': False,  # Default to non-admin
            'avatar_url': avatar_url  # Add avatar URL
        }
        
        result = db.users.insert_one(new_user)
        return result.inserted_id
    
    @staticmethod
    def get_by_email(email):
        db = get_db()
        return db.users.find_one({'email': email})
    
    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        return db.users.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def authenticate(email, password):
        db = get_db()
        user = db.users.find_one({'email': email})
        
        if user and check_password_hash(user['password'], password):
            return user
        return None