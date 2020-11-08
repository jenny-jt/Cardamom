from flask import Flask, request, render_template, jsonify
from datetime import datetime
import re
import json
from model import connect_to_db, db, Ingredient, Inventory, Recipe
from crud import add_ingredient, add_recipe, add_mealplan

import os
import requests
import jinja2

import spoonacular as sp

app = Flask(__name__)
app.secret_key = "SECRET"

app = connect_to_db(app)
app.app_context().push()

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
def find_recipe_by_ingredients():
    ingredients = str(request.args.get("ingredients")) #also want to match with regex single/plural items and output all as single
    print(ingredients)

    number = request.args.get("num_recipes")

    # re_ingredients = re.sub(r'(\w+)',r'"\1"', ingredients) #need to separate multiple ingredients and also make them single
    # print(re_ingredients)
    
    db_recipe = Recipe.query.filter(Recipe.ingredients.contains(ingredients)).first()
    print(db_recipe)

    # if db_recipe:
    #     find_recipes_db(db_ingredient)
        # return redirect (db_recipe.url)
    # else:
    #     find_recipes_api(ingredients, number=number)

    return render_template('recipe-search.html', ingredients=ingredients)


# def find_recipes_db(ingredients):
#     """"Search for recipes in db with ingredients"""
#     ingredients = request.args.get("ingredients")

#     recipe = Recipe.query.filter(Recipe.ingredients.contains(ingredients)).first()

#     return render_template('recipe-display.html', url=recipe.url)

# def find_recipes_api(ingredients, number):
#     """"Search for recipes by entering main ingredient(s)"""

#     response = api.search_recipes_by_ingredients(ingredients, number=number)

#     data = response.json()
#     recipe_title = data[0]['title']
  
#     return render_template('recipe-search.html', title=recipe_title, ingredients=ingredients)


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