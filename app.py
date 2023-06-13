from flask import Flask, jsonify
from flask_cors import CORS
import models
from flask_login import LoginManager
from resources.authors import authors
from resources.categories import categories
from resources.users import users
import psycopg2
import os

DEBUG = True
PORT = 8000

login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = 'VENIVEDIVICI'

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return models.User.get_by_id(user_id)

database_url = os.environ.get('DATABASE_URL')

database = psycopg2.connect(database_url)

app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SQLALCHEMY_DATABASE_URI'] = database


# CORS arguments go here
CORS(app, resources={r'/api/v1/*': {'origins': 'https://quoticus.netlify.app'}}, supports_credentials=True)
# CORS(app)
# CORS(app, resources={r'/*': {'origins': ['http://localhost:3000', 'https://quoticus.netlify.app']}}, supports_credentials=True)
# CORS(authors, origins='http://localhost:3000', supports_credentials=True)
# CORS(categories, origins='http://localhost:3000', supports_credentials=True)
# CORS(users, origins='http://localhost:3000', supports_credentials=True)
# @app.after_request
# def set_cors_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000' 
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
#     response.headers['Access-Control-Allow-Credentials'] = 'true'
#     return response

# Register blueprints with the app
app.register_blueprint(authors, url_prefix='/api/v1/authors')
app.register_blueprint(categories, url_prefix='/api/v1/categories')
app.register_blueprint(users, url_prefix='/api/v1/users')



if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)