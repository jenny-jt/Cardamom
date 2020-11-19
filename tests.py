from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import ***

class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True


    # in crud.py or model.py (connected to db)
    # >> mealplan1 = Mealplan.query.get(1)
    # >> mealplan1.recipes
    # [<recipe 1>, <recipe 2>, <recipe 3>] will need index of recipe with id in order to direct swap
    # >> recipe15 = Recipe.query.get(15)
    # how to find index of recipe with specific ID?  = mealplan1.recipes.index(recipe3)

    # Option 1:
    # >> mealplan1.recipes.pop(2) OR mealplan1.recipes.remove(recipe3)
    # >> mealplan1.recipes.append(recipe15)