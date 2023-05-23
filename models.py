from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
import datetime

# connecting to my psql database
DATABASE = PostgresqlDatabase('quoticus')

# User model
class User(Model, UserMixin):
    email = CharField(unique=True, max_length=120)
    password = CharField(max_length=255)
    favorites = TextField(default="[]")

    class Meta:
        database = DATABASE
       

    def __init__(self, email, password):
        super().__init__()
        self.email = email
        self.password = generate_password_hash(password)
        self.favorites = ""

    # def add_favorite(self, author_id):
        # come back to this

    # def remove_favorite(self, author_id):
        # come back to this

# Category model
class Category(Model):
    name = CharField(max_length=100)

    class Meta:
        database = DATABASE
        

# Author model
class Author(Model):
    quote = TextField()
    source = CharField(max_length=255)
    date = TextField()

    class Meta:
        database = DATABASE
        


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Author, Category, User], safe=True)
    print("Connected to DB and created tables if they do not already exist")
    DATABASE.close()