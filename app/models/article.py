from app.utils.db import get_db
from bson import ObjectId
from datetime import datetime

class Article:
    @staticmethod
    def create(article_data):
        db = get_db()
        return db.articles.insert_one(article_data)

    @staticmethod
    def get_all():
        db = get_db()
        return list(db.articles.find())

    @staticmethod
    def get_by_id(article_id):
        db = get_db()
        # Make sure we're using ObjectId for the query
        return db.articles.find_one({'_id': article_id})

    @staticmethod
    def get_by_author(author_id):
        try:
            db = get_db()
            articles = list(db.articles.find({'author_id': author_id}))
            print(f"Retrieved {len(articles)} articles for author {author_id}")
            return articles
        except Exception as e:
            print(f"Error in Article.get_by_author: {str(e)}")
            import traceback
            traceback.print_exc()
            return []

    @staticmethod
    def update(article_id, update_data):
        db = get_db()
        # Add updated_at timestamp
        update_data['updated_at'] = datetime.utcnow()
        
        result = db.articles.update_one(
            {'_id': ObjectId(article_id)},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            return db.articles.find_one({'_id': ObjectId(article_id)})
        return None
        
    @staticmethod
    def delete(article_id):
        try:
            db = get_db()
            
            # Print the article_id for debugging
            print(f"Deleting article with ID: {article_id}")
            
            # Convert string ID to ObjectId if it's not already
            if isinstance(article_id, str):
                # Handle case where article_id might be '[object Object]'
                if article_id == '[object Object]':
                    print("Error: Received [object Object] as article_id")
                    return False
                    
                # Strip any quotes or extra characters
                article_id = article_id.strip('"\'')
                
                # Verify it's a valid ObjectId
                if not ObjectId.is_valid(article_id):
                    print(f"Error: Invalid ObjectId format: {article_id}")
                    return False
                    
                article_id = ObjectId(article_id)
                
            result = db.articles.delete_one({'_id': article_id})
            deleted = result.deleted_count > 0
            print(f"Delete result: {deleted}")
            return deleted
        except Exception as e:
            print(f"Error in Article.delete: {str(e)}")
            import traceback
            traceback.print_exc()
            return False