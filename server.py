from flask import Flask, request, render_template, jsonify, redirect
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
    """take in ingredients from form and search db for recipe, if not found in db, api request for recipe"""
    ingredients = str(request.args.get("ingredients")) #also want to match with regex single/plural items and output all as single

    # number = request.args.get("num_recipes")

    # re_ingredients = re.sub(r'(\w+)',r'"\1"', ingredients) #need to separate multiple ingredients and also make them single
    # print(re_ingredients)
    
    db_recipe = Recipe.query.filter(Recipe.ingredients.contains(ingredients)).first()

    if db_recipe:
        url = str(db_recipe.url)
    else:
        url= str(find_recipes_api(ingredients))
        
    return redirect(url)


def find_recipes_api(ingredients):
    """"Search for recipes by entering main ingredient(s)"""

    response = api.search_recipes_by_ingredients(ingredients, number=1)

    data = response.json()
    recipe_title = data[0]['title']
    recipe_api_id = data[0]['id']

    source_url = find_recipe_info(recipe_api_id)

    return source_url


def find_recipe_info(recipe_api_id):
    """find all pertinent recipe info to display on recipe card"""

    response = api.get_recipe_information(id=recipe_api_id)
    data = response.json()
    # recipe_title = data[0]['title']
    # recipe_img = data[0]['image']
    # recipe_ingredients = data[0]['ingredients']
    return data['sourceUrl']


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