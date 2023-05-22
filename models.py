from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from app import db

# Models

# User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    favorites = db.relationship('Author', secondary='favorites', backref='users')

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

# Author
class Author(db.Model):
    id = db.Column(db.integer, primary_key=True)
    quote = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(255))
    date = db.Column(db.String(50))
    category = db.relationship('Category', backref='authors')
    

# Category
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)