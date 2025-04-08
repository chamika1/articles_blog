from pymongo import MongoClient
from urllib.parse import quote_plus

def get_db():
    username = quote_plus('rasanjanachamika')
    password = quote_plus('WKmH9Zunm5f6@K-')
    connection_string = f'mongodb+srv://{username}:{password}@cluster0.sbzsowq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
    client = MongoClient(connection_string)
    return client['tech_blog']