from flask import Flask, render_template
import json  # Import standard json module instead of flask.json
from flask_cors import CORS
from app.routes.auth import auth_bp
from app.routes.articles import articles_bp
from dotenv import load_dotenv
import os
from bson import ObjectId

# Load environment variables
load_dotenv()

# Custom JSON encoder to handle ObjectId
class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static'
)
# Use the custom JSON encoder
app.json_encoder = MongoJSONEncoder
# Disable strict slashes to prevent 308 redirects
app.url_map.strict_slashes = False

# Fix CORS configuration to allow both localhost and 127.0.0.1 and ngrok
# Replace the current CORS configuration
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Set secret key for JWT
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(articles_bp, url_prefix='/api/articles')

# Frontend routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/articles/new')
def create_article():
    return render_template('create_article.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

# Add this route after your other routes
@app.route('/articles/edit/<article_id>')
def edit_article(article_id):
    return render_template('edit_article.html', article_id=article_id)

@app.route('/articles/<article_id>')
def view_article(article_id):
    return render_template('article_detail.html', article_id=article_id)

# Add this route to your app.py file
@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html')

# Add a health check endpoint
@app.route('/api/health')
def health_check():
    return jsonify({"status": "ok", "message": "API is running"}), 200

if __name__ == '__main__':
    app.run(debug=True)