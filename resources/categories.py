from models import Category, Author
from flask import Blueprint, jsonify
from playhouse.shortcuts import model_to_dict


# Blueprint
categories = Blueprint('categories', __name__)


#Route (for all categories)
@categories.route('/', methods=['GET'])
def get_categories():
    categories_query = Category.select(Category.category_name).distinct()
    category_dict = [model_to_dict(category) for category in categories_query]
    return jsonify({
        'data': category_dict,
        'message': f"Successfully found {len(category_dict)} categories",
        'status': 200
    }), 200


# Route for a specific category
@categories.route('/<category_name>/quotes', methods=["GET"])
def get_category(category_name):
    try:
        # fetch category by category.id
        category = Category.get(Category.category_name == category_name)

        # fetch all authors associated with the category
        authors = Author.select().join(Category).where(Category.category_name == category_name)

        # Convert authors to dictionaries
        author_dict = [model_to_dict(author) for author in authors]

        return jsonify({
            'category_name': category.category_name,
            'authors': author_dict,
            'status': 200
        }), 200
    except Category.DoesNotExist:
        return jsonify({
            'data': {},
            'message': f"Category with name '{category_name}' does not exist.",
            'status': 404
        }), 404