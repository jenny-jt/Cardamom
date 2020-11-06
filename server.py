from flask import Flask, request, render_template, jsonify

import os
import requests

import spoonacular as sp

app = Flask(__name__)
app.secret_key = "SECRET"

# apiKey = os.environ['apiKey']
api = sp.API(os.environ['apiKey'])

@app.route("/")
def show_homepage():
    """Show the application's homepage."""

    return render_template('homepage.html')

@app.route("/search")
def show_search_form():
    """Show search recipes form to enter main ingredient(s)""" 

    return render_template('search-form.html')


@app.route("/recipe/search")
def find_recipes():
    """"Search for recipes by entering main ingredient(s)"""

    ingredients = request.args.get('ingredients')
    number = request.args.get('num_recipes', 1)

    url = 'https://api.spoonacular.com/recipes/findByIngredients'

    response = api.search_recipes_by_ingredients(ingredients, number)
    # response = api.parse_ingredients("3.5 cups King Arthur flour", servings=1)
    data = response.json()

    return render_template('recipe-search.html')


# @app.route("/inventory")
# form with default values for location, able to save timestamp, quantity

# @app.route("/mealplan")
#   """ display meal plan for certain date """


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')