import models
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from playhouse.shortcuts import model_to_dict

# Blueprint for users
users = Blueprint('users', __name__)


# User Registration route
@users.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try: 
        models.User.create_user(email, password)
        return jsonify({'message': 'Registration successful'}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 409


# User Login route
@users.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = models.User.select().where(models.User.email == email).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Login Successful'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401
    

# User Logout route
@users.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 201