from models import Category
from flask import Blueprint, jsonify
from playhouse.shortcuts import model_to_dict


# Blueprint
categories = Blueprint('categories', __name__)


#Route
@categories.route('/', methods=['GET'])
def get_categories():
    categories_query = Category.select()
    category_dict = [model_to_dict(category) for category in categories_query]
    return jsonify({
        'data': category_dict,
        'message': f"Successfully found {len(category_dict)} categories",
        'status': 200
    }), 200