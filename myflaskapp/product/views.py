# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, jsonify, request

from myflaskapp.product.models import Product

bp = Blueprint(name='product',  # pylint: disable=invalid-name
               import_name=__name__,
               )

@bp.route('/products/', methods=['GET'])
def get_products():

    ALLOWED_SORT = ['-price', 'price']

    sort = request.args.get('sort')
    if sort and sort not in ALLOWED_SORT:
        return jsonify({'error': 'invalid sort'}), 403

    products = Product.query.filter().order_by(sort)

    filter_str = request.args.get('filter')
    if filter_str:
        products = products.filter(Product.name.ilike(filter_str) | Product.description.ilike(filter_str)).all()

    return jsonify({'data': [product.serialize() for product in products]}), 200
