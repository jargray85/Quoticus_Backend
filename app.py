from flask import Flask, jsonify, request
from flask_cors import CORS
import models
import os
from flask_login import LoginManager
from resources.authors import authors
from resources.categories import categories
from resources.users import users



DEBUG = False
PORT = int(os.environ.get('PORT', 8000))

login_manager = LoginManager()

app = Flask(__name__)

# Test Route for http://localhost:8000
@app.route('/')
def home():
    return "Hello, this is the home page!"

# SECRET KEY
app.secret_key = 'VENIVEDIVICI'

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return models.User.get_by_id(user_id)


# CORS arguments go here
cors = CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "https://main--quoticus.netlify.app"],
        "supports_credentials": True
    }
})

# Register blueprints with the app
app.register_blueprint(authors, url_prefix='/api/v1/authors')
app.register_blueprint(categories, url_prefix='/api/v1/categories')
app.register_blueprint(users, url_prefix='/api/v1/users')

# Handling OPTIONS requests
@app.before_request
def handle_options_request():
    if request.method == 'OPTIONS':
        # Handle OPTIONS request
        response = jsonify()
        response.status_code = 200 
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)