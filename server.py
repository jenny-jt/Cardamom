from flask import Flask, request, render_template, jsonify, redirect, session
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
app.secret_key = os.environ['secret_key']

# app = connect_to_db(app)
# app.app_context().push()

# apiKey = os.environ['apiKey']
api = sp.API(os.environ['apiKey'])

weekly_meal_plan = set()

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
    ingredients = str(request.args.get("ingredients"))
    # session['ingredients'] = ingredients
    # re_ingredients = re.sub(r'(\w+)',r'"\1"', ingredients) #need to separate multiple ingredients and also make them single
    # print(re_ingredients)
    number = request.args.get("num_recipes")
    date = request.args.get("date")
    
    # session['number'] = number
    # number = session.setdefault("number", request.args.get("num_recipes"))    
    # mealplan = session.setdefault("mealplan", ***) #will actually modify session and create default if mealplan not found
    # mealplan = session.get("mealplan", ***) #will return the default

    if mealplan.date == date:
        print("mealplan already exists, would you like to view it?")
    else:
        mealplan= crud.add_mealplan(date)
        session['mealplan'] = mealplan

        #check if ingredients match db, then call appropriate functions
    if db_recipe_search(ingredients):
        for item in db_recipe:
            mealplan_add_recipe(item)  #should include this function under MealPlan class in model.py or server? ***
    else: 
        api_recipe_ids = api_recipe_search(ingredients, number)
        for item in api_recipe_ids:
            recipe = recipe_info(item)
            mealplan_add_recipe(recipe)


def db_recipe_search(ingredients):
    """takes in ingredients and num_recipes from form, outputs list of recipes from db"""
    """if not have one recipe that contains all ingredients, loop over list of ingredients and search for ingredients individually"""
    db_recipe = Recipe.query.filter(Recipe.ingredients.contains(ingredients)).all()
    db_recipes = []

    for ingredient in ingredients: 
        db_recipe = Recipe.query.filter(Recipe.ingredients.contains(ingredient)).all()
        db_recipes.append()
    return db_recipes


def api_recipe_search(ingredients, number):
    """"Search for recipes in API by entering main ingredient(s) and number of recipes, returns list of recipe ids"""
    response = api.search_recipes_by_ingredients(ingredients, number)
    data = response.json()
    api_recipe_ids = []

    for i in range(number):
        # recipe_title = data[i]['title']
        api_id = data[i]['id']
        api_recipe_ids.append(api_id)
    print(api_recipe_ids)
    return api_recipe_ids


def recipe_info(recipe_api_id):
    """retrieve recipe info and add recipe to database, returns recipe object. DO I WANT TO GROW DB??"""
    response = api.get_recipe_information(id=recipe_api_id)
    data = response.json()
    # recipe_img = data['image']
    name = data['title']

    recipe_ingredients = []
    for i, item in enumerate(data['extendedIngredients']):
        recipe_ingredients.append(data['extendedIngredients'][i][name])
    print("recipe ingredients:", recipe_ingredients)

    url = data['sourceUrl']

    recipe = crud.add_recipe(name, recipe_ingredients, url)  #make new recipe object, returns recipe object

    return recipe


def mealplan_add_recipe(recipe): 
    """add recipe to mealplan"""
    mealplan.add_recipe_to_mealplan(self, recipe) #how to call function in model.py
    mealplan.recipes_r.append(recipe)  #recipe object returned after adding recipe to db

    print("recipe added to mealplan")


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
    app.run(debug=True, host='0.0.0.0')
    connect_to_db(app)