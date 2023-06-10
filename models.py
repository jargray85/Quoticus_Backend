from peewee import *
import os
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.postgres_ext import ArrayField
import datetime

# connecting to my psql database
# DATABASE = PostgresqlDatabase('quoticus')
DATABASE_URL = os.environ.get('DATABASE_URL')


# Author model
class Author(Model):
    name = CharField()
    quote = TextField()
    source = CharField(max_length=255)
    date = CharField()

    class Meta:
        database = DATABASE_URL
        table_name = 'authors'


# Category model
class Category(Model):
    category_name = CharField(max_length=100)
    author = ForeignKeyField(Author, backref='categories')

    class Meta:
        database = DATABASE_URL
        table_name = 'categories'


# User model
class User(Model, UserMixin):
    email = CharField(unique=True, max_length=120)
    password = CharField(max_length=255)
    favorites = ArrayField(default=[])

    class Meta:
        database = DATABASE_URL
        table_name = 'users'
       

    # def __init__(self, email, password):
    #     super().__init__()
    #     self.email = email
    #     self.password = generate_password_hash(password)
    #     self.favorites = ""

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @staticmethod
    def get_by_id(user_id):
        return User.get(User.id == user_id)


    # def add_favorite(self, author_id):
        # come back to this

    # def remove_favorite(self, author_id):
        # come back to this
       


def initialize():
    DATABASE_URL.connect()
    # DATABASE.drop_tables([Author, Category, User])
    author_count = Author.select().count()
    print("number of records in Author table:", author_count)
    DATABASE_URL.create_tables([Author, Category, User], safe=True)
    print("Connected to DB and created tables if they do not already exist")
    DATABASE_URL.close()