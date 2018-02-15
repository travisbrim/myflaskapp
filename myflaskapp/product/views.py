# -*- coding: utf-8 -*-
"""Product views."""
from flask import Blueprint, jsonify, request

from myflaskapp.extensions import csrf_protect
from myflaskapp.product.models import Product

bp = Blueprint(name='product',  # pylint: disable=invalid-name
               import_name=__name__,
               )


@bp.route('/products/', methods=['GET'])
def retrieve_products():

    ALLOWED_SORT = ['-price', 'price']

    sort = request.args.get('sort')
    if sort and sort not in ALLOWED_SORT:
        return jsonify({'error': 'invalid sort'}), 403

    products = Product.query.filter().order_by(sort)

    filter_str = request.args.get('filter')
    if filter_str:
        # add wildcard characters before and after the filter term
        filter_str = ''.join(['%',filter_str,'%'])
        products = products.filter(Product.name.ilike(filter_str) |
            Product.description.ilike(filter_str))

    data = [product.serialize() for product in products.all()]
    return jsonify({'data': data}), 200


@bp.route('/products/', methods=['POST'])
@csrf_protect.exempt
def create_product():

    if not request.headers['Content-Type'] == 'application/json':
        return jsonify({'error': 'endpoint expects application/json content-type'}), 415

    try:
        product = Product.create(name=request.json.get('name'),
                                 price=request.json.get('price'),
                                 description=request.json.get('description'),
                                 color=request.json.get('color'))
    except:
        return jsonify({'error': 'invalid input data'}), 422
    else:
        return jsonify({'data': product.serialize()}), 201



@bp.route('/products/<id>', methods=['GET'])
def retrieve_product(id):
    product = Product.query.get(id)
    if product:
        return jsonify({'data': product.serialize()}), 200
    else:
        return jsonify({'error': 'resource does not exist'}), 403
