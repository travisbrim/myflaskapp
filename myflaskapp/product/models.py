# -*- coding: utf-8 -*-
"""Product models."""
from decimal import Decimal

from sqlalchemy.orm import validates

from myflaskapp.database import Column, Model, SurrogatePK, db

class Product(SurrogatePK, Model):
    """A product"""
    name = Column(db.String(30), nullable=False)
    description = Column(db.String(80))
    price = Column(db.Numeric(), nullable=False)
    color = Column(db.String(20))

    def __init__(self, name, price, description=None, color=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, description=description,
            price=price, color=color, **kwargs)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            # TODO: introduces the potential for rounding errors
            "price": float(self.price),
            "color": self.color
        }

    @validates('price')
    def validate_price(self, key, price):
        assert Decimal(price) >= 0
        return price
