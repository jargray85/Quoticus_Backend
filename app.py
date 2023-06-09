from flask import Flask, jsonify
from flask_cors import CORS
import models
from flask_login import LoginManager
from resources.authors import authors
from resources.categories import categories
from resources.users import users

DEBUG = True
PORT = 8000

login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = 'VENIVEDIVICI'

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return models.User.get_by_id(user_id)

# CORS arguments go here
CORS(app)
@app.after_request
def set_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Replace * with your frontend URL for production
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# Register blueprints with the app
app.register_blueprint(authors, url_prefix='/api/v1/authors')
app.register_blueprint(categories, url_prefix='/api/v1/categories')
app.register_blueprint(users, url_prefix='/api/v1/users')



if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)