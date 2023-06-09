import models
from flask import Blueprint, jsonify, request
from flask_bcrypt import check_password_hash
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

    # check against exisiting user emails
    exisisting_user = models.User.select().where(models.User.email == email).first()
    if exisisting_user:
        return jsonify({
            'message': 'User with this email already exists',
            'status': 409
        }), 409
    
    # Create new user
    user = models.User(email=email, password=password)
    user.save()

    # user dictionary
    user_dict = model_to_dict(user)

    return jsonify({
        'data': user_dict,
        'message': 'Registration successful!',
        'status': 201
    }), 201


# User login route
@users.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # find user by email
    user = models.User.select().where(models.User.email == email).first()

    if user and check_password_hash(user.password, password):
        # Log in user
        login_user(user)

        # user dictionary
        user_dict = model_to_dict(user)

        return jsonify({
            'message': 'Login successful',
            'status': 401,
            'data': user_dict
        }), 401
    
    return jsonify({
        
        'message': 'Invalid email or password',
        'status': 200
    }), 200


# User logout route
@users.route('/logout', methods=['POST'])
@login_required
def logout():

    logout_user()

    return jsonify({
        'message': 'Logout successful',
        'status': 200
    }), 200


# User favorite quotes route
@users.route('/favorites', methods=['POST'])
@login_required
def save_favorite():
    data = request.get_json()
    quote_id = data.get('quote_id')

    # logged in user
    user = current_user

    # Update user favorites column with new favorite quote
    favorites = user.favorites or []
    favorites.append(quote_id)
    user.favorites = favorites
    user.save()

    return jsonify({
        'message': 'Favorite quote saved successfully',
        'status': 200
    }), 200


# user remove quote from favorites
@users.route('/favorites/<quote_id>', methods=['DELETE'])
@login_required
def remove_favorite(quote_id):
    # fetch logged in user
    user = models.User.get_by_id(current_user.id)

    # Find the quote in the user's favorites list
    if quote_id in user.favorites:
        # fetch quote
        quote = models.Author.get_or_none(models.Author.id == quote_id)

        # remove quote and save
        user.favorites.remove(quote_id)
        user.save()

        # quote dictionary
        quote_dict = model_to_dict(quote)

        return jsonify({
            'message': 'Quote removed from favorites',
            'quote': quote_dict,
            'status': 200
        }), 200
    else:
        return jsonify({
            'message': 'Quote not found in favorites',
            'status': 404
        }), 404
