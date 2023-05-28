from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
import datetime

# connecting to my psql database
DATABASE = PostgresqlDatabase('quoticus')


# Author model
class Author(Model):
    name = CharField()
    quote = TextField()
    source = CharField(max_length=255)
    date = CharField()

    class Meta:
        database = DATABASE
        table_name = 'authors'


# Category model
class Category(Model):
    category_name = CharField(max_length=100)
    author = ForeignKeyField(Author, backref='categories')

    class Meta:
        database = DATABASE
        table_name = 'categories'


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
       


def initialize():
    DATABASE.connect()
    # DATABASE.drop_tables([Author, Category, User])
    author_count = Author.select().count()
    print("number of records in Author table:", author_count)
    DATABASE.create_tables([Author, Category, User], safe=True)
    print("Connected to DB and created tables if they do not already exist")
    DATABASE.close()