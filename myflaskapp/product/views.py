# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint

from myflaskapp.product.models import Product

bp = Blueprint(name='product',  # pylint: disable=invalid-name
               import_name=__name__,
               )
