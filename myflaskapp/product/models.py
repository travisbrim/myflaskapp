# -*- coding: utf-8 -*-
"""Product models."""

from myflaskapp.database import Column, Model, SurrogatePK, db

class Product(SurrogatePK, Model):
    """A product"""
    name = Column(db.String(30), nullable=False)
    description = Column(db.String(80))
    price = Column(db.Numeric(), nullable=False)
    color = Column(db.String(20))

    def serialize(self):
        return {
            "name": self.name,
            "description": self.description,
            # TODO: introduces the potential for rounding errors
            "price": float(self.price),
            "color": self.color
        }
