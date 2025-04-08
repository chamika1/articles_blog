import json
import traceback
from flask import Blueprint, request, jsonify
from bson import ObjectId, json_util
from app.models.article import Article
from app.utils.auth import token_required
from app.utils.image_upload import upload_to_imagebb
from datetime import datetime  # Add this import

articles_bp = Blueprint('articles', __name__)

# Add this import at the top of the file
from bson.json_util import dumps
import json

# Then modify your get_articles function to use json_util
# Update the route to handle both with and without trailing slashes
@articles_bp.route('/', methods=['GET'])
@articles_bp.route('', methods=['GET'])  # Add this line to handle requests without trailing slash
def get_articles():
    try:
        articles = Article.get_all()
        # Debug log
        print(f"Retrieved {len(articles)} articles from database")
        # Convert ObjectId to string using json_util
        return json.loads(dumps({"articles": articles}))
    except Exception as e:
        print(f"Error in get_articles: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"articles": [], "error": str(e)}), 500

# Also update the get_article function
@articles_bp.route('/<article_id>', methods=['GET'])
def get_article(article_id):
    try:
        # Check if article_id is a valid ObjectId
        if not ObjectId.is_valid(article_id):
            return jsonify({'message': f'Invalid article ID format: {article_id}'}), 400
            
        # Convert string ID to ObjectId
        article = Article.get_by_id(ObjectId(article_id))
        
        if not article:
            return jsonify({'message': 'Article not found!'}), 404
        
        # Convert ObjectId to string using json_util
        return json.loads(json_util.dumps({"article": article}))
    except Exception as e:
        print(f"Error getting article: {str(e)}")
        traceback.print_exc()  # Print full traceback for debugging
        return jsonify({'message': f'Error: {str(e)}'}), 500
    # Remove this line at the end of the get_article function:
    # return jsonify({'article': article}), 200

@articles_bp.route('/', methods=['POST'])
@token_required
def create_article(current_user):
    try:
        data = request.get_json()
        
        if not data or not data.get('title') or not data.get('content'):
            return jsonify({'message': 'Missing required fields'}), 400

        article = {
            'title': data['title'],
            'summary': data.get('summary', ''),
            'content': data['content'],
            'thumbnail_url': data.get('thumbnail_url', ''),
            'author_id': str(current_user['_id']),
            'author_name': current_user['username'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

        result = Article.create(article)
        
        return jsonify({
            'message': 'Article created successfully',
            'article_id': str(result.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@articles_bp.route('/upload-image', methods=['POST'])
@token_required
def upload_image(current_user):
    try:
        # Print debug info
        print(f"Upload request from user: {current_user['username']}")
        
        if 'image' not in request.files:
            return jsonify({'message': 'No image file'}), 400

        image = request.files['image']
        if image.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        # Upload to ImageBB
        image_url = upload_to_imagebb(image)
        if not image_url:
            return jsonify({'message': 'Failed to upload image'}), 500

        return jsonify({'url': image_url}), 200

    except Exception as e:
        print(f"Upload route error: {str(e)}")  # Debug logging
        return jsonify({'message': str(e)}), 500

# Update the update_article and delete_article routes to allow admin operations

@articles_bp.route('/<article_id>', methods=['PUT'])
@token_required
def update_article(current_user, article_id):
    try:
        # Check if article_id is a valid ObjectId
        if not ObjectId.is_valid(article_id):
            return jsonify({'message': f'Invalid article ID format: {article_id}'}), 400
            
        # Convert string ID to ObjectId
        article = Article.get_by_id(ObjectId(article_id))
        
        if not article:
            return jsonify({'message': 'Article not found!'}), 404
        
        # Check if current user is the author or an admin
        is_admin = current_user.get('is_admin', False)
        if str(article['author_id']) != str(current_user['_id']) and not is_admin:
            return jsonify({'message': 'You do not have permission to edit this article!'}), 403
        
        # Get data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided!'}), 400
            
        # Update only the fields that are provided
        update_data = {}
        if 'title' in data:
            update_data['title'] = data['title']
        if 'summary' in data:
            update_data['summary'] = data['summary']
        if 'content' in data:
            update_data['content'] = data['content']
        if 'thumbnail_url' in data and data['thumbnail_url']:
            update_data['thumbnail_url'] = data['thumbnail_url']
        
        # Update the article
        updated_article = Article.update(article_id, update_data)
        
        if not updated_article:
            return jsonify({'message': 'Failed to update article!'}), 500
            
        # Return the updated article
        return json.loads(json_util.dumps({"article": updated_article}))
        
    except Exception as e:
        print(f"Error updating article: {str(e)}")
        traceback.print_exc()
        return jsonify({'message': f'Error: {str(e)}'}), 500

@articles_bp.route('/<article_id>', methods=['DELETE'])
@token_required
def delete_article(current_user, article_id):
    try:
        # Log the received article_id for debugging
        print(f"Received article_id for deletion: {article_id}")
        
        # Handle case where article_id might be '[object Object]'
        if article_id == '[object Object]':
            return jsonify({'message': 'Invalid article ID: received [object Object]'}), 400
        
        # Strip any quotes or extra characters that might be present
        article_id = article_id.strip('"\'')
        
        # Check if article_id is a valid ObjectId
        if not ObjectId.is_valid(article_id):
            return jsonify({'message': f'Invalid article ID format: {article_id}'}), 400
            
        # Convert string ID to ObjectId
        article = Article.get_by_id(ObjectId(article_id))
        
        if not article:
            return jsonify({'message': 'Article not found!'}), 404
        
        # Check if current user is the author or an admin
        is_admin = current_user.get('is_admin', False)
        if str(article['author_id']) != str(current_user['_id']) and not is_admin:
            return jsonify({'message': 'You do not have permission to delete this article!'}), 403
        
        # Delete the article
        if Article.delete(article_id):
            return jsonify({'message': 'Article deleted successfully!'}), 200
        else:
            return jsonify({'message': 'Failed to delete article!'}), 500
            
    except Exception as e:
        print(f"Error deleting article: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': f'Error: {str(e)}'}), 500