from models import Author
from flask import Blueprint, jsonify

from playhouse.shortcuts import model_to_dict


# Blueprint
authors = Blueprint('authors', __name__)

# Route
@authors.route('/', methods=["GET"])
def get_authors():
    authors_query = Author.select()
    print(authors_query)
    author_dict = [model_to_dict(author)for author in authors_query]
    return jsonify({
        'data': author_dict,
        'message': f"Successfully found {len(author_dict)} authors",
        'status': 200
        }), 200