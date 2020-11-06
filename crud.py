"""CRUD operations."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import db, connect_to_db

def add_ingredient(name,location):
    """add ingredient"""
    ingredient = Ingredient(name=name, location=location)
    db.session.add(ingredient)
    db.session.commit()

    return ingredient

def add_recipe(name, ingredients):
    """add recipes with required ingredient(s)"""
    recipe = Recipe(name=name, ingredients=ingredients)
    db.session.add(recipe)
    db.session.commit()

    return recipe

def update_inventory(ingredient, bought, use_this_week, in_stock, quantity)
    """update inventory when ingredient bought or used"""

    inventory = Inventory(ingredient=ingredient)
