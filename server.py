from flask import Flask, request, render_template, jsonify, redirect, session
from datetime import datetime
import re
import json
from model import connect_to_db, MealPlan
import crud
import os
import random
import requests
import jinja2

import spoonacular as sp

app = Flask(__name__)
app.secret_key = os.environ['secret_key']

@app.route("/")
def show_homepage():
    """Show the application's homepage."""

    return render_template('homepage.html')

@app.route("/search")
def show_search_form():
    """Show form to enter date for mealplan and main ingredient(s) for recipes""" 

    return render_template('search-form.html')

@app.route("/results/search")
def search_results(): 
    """take in date for mealplan, ingredients, and number of recipes, outputs mealplan and recipes"""
    ingredients = request.args.get("ingredients").split(",")
    number = int(request.args.get("num_recipes"))
    print(number)
    date = request.args.get("date")
    
    mealplan = MealPlan.query.filter(MealPlan.date == date).first()
    print("mealplan query result", mealplan) #confused why this always returns something

    if not mealplan: 
        mealplan = crud.add_mealplan(date)

    db_recipes = crud.db_recipe_search(ingredients)
    
    api_recipe_ids = crud.api_recipe_search(ingredients, number)
    api_recipes = api_recipes_list(api_recipe_ids)

    count = 0
    while count < number:
        if db_recipes:
            item = pick_db_recipes(db_recipes)
            crud.mealplan_add_recipe(mealplan, item)
            count += 1
        else:
            item = pick_db_recipes(api_recipes)
            crud.mealplan_add_recipe(mealplan, item)
            count += 1

    recipes = mealplan.recipes_r
    print(recipes)

    return render_template('recipe-display.html', recipes=recipes)

def api_recipes_list(api_recipe_ids):
    """takes in list of recipe ids and outputs list of assoc recipes"""
    api_recipes = []

    for id in api_recipe_ids:
        recipe = crud.recipe_info(id)
        api_recipes.append(recipe)
    
    return api_recipes

def pick_db_recipes(db_recipes):
    """takes in list of db_recipes, adds random recipes from that list to meal plan and increases count"""
    item = random.choice(db_recipes)

    return item    


def pick_api_recipes(api_recipes):
    """takes in list of api_recipes, adds recipes to mealplan and increases count"""
    item = random.choice(api_recipes)
    
    return item  


def db_ingredient():
    """turn form inputs into singular form"""
    

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
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
