from flask import Flask, request, render_template, jsonify

import os
import requests
import jinja2

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
# find recipes in api, # find recipes in database, #call 2 functions find recipes
def find_recipes():
    """"Search for recipes by entering main ingredient(s)"""

    ingredients = request.args.get("ingredients")
    number = request.args.get("num_recipes", 1)

    response = api.search_recipes_by_ingredients(ingredients, number=number)

    data = response.json()
    print(data)
    recipe_title = data[0]['title']
  
    return render_template('recipe-search.html', title=recipe_title, ingredients=ingredients, data=data)


@app.route("/inventory")
def update_inventory():
    """ form with default values for location, able to save timestamp, quantity """

    return render_template('inventory.html')


@app.route("/mealplan")
def show_meal_plan():
    """ display meal plan for certain date """

    return render_template('meal-plan.html', date=date)


@app.route("/recipe/display")
def display_recipe():
    """ display recipe printout via link"""

    return render_template('recipe-display.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')