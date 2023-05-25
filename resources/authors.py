from models import Author
from flask import Blueprint, jsonify

from playhouse.shortcuts import model_to_dict


# Blueprint
authors = Blueprint('authors', 'authors')

# Route
@authors.route('/authors', methods=["GET"])
def get_authors():
    authors = Author.select()
    author_dict = [model_to_dict(author)for author in authors]
    return jsonify({'authors': author_dict})