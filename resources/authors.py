from models import Author
from flask import Blueprint, jsonify
from playhouse.shortcuts import model_to_dict


# Blueprint
authors = Blueprint('authors', __name__)

# Route for all authors
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

# Route for quotes by author
@authors.route('/<author_name>/quotes')
def get_author_quotes(author_name):
    try:
        # Find author by name
        author = Author.get(Author.name == author_name)

        # get all quotes by the author
        quotes = [author.quote for author in Author.select().where(Author.name == author_name)]

        return jsonify({
            'author_name': author.name,
            'quotes': quotes,
            'status': 200
        }), 200
    
    except Author.DoesNotExist:
        return jsonify({
            'data': {},
            'message': f"Author with name {author_name} does not exist.",
            'status': 404
        }), 404