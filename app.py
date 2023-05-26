from flask import Flask, jsonify
from flask_cors import CORS
import models
from flask_login import LoginManager
from resources.authors import authors

DEBUG = True
PORT = 8000

login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = 'VENIVEDIVICI'

login_manager.init_app(app)

# CORS arguments go here


# Register blueprints with the app
app.register_blueprint(authors, url_prefix='/api/v1/authors')




if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)