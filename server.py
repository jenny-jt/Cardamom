from flask import Flask, request, render_template, jsonify, redirect, session
from datetime import datetime
import re
import json
from model import connect_to_db, MealPlan
import crud
import os

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
    date = request.args.get("date")
    
    mealplan = MealPlan.query.filter(MealPlan.date == date).first()
    print("mealplan query result", mealplan)

    if not mealplan: 
        mealplan = crud.add_mealplan(date)

    while number > 0: 
        print(number)
        db_recipes = crud.db_recipe_search(ingredients)
        print("initial query of db with ingredients:", db_recipes)
        if len(db_recipes) > 1:
            for item in db_recipes:
                crud.mealplan_add_recipe(mealplan, item) 
                print("db recipe item:", item)
                number -= 1     
        else: 
            api_recipes = crud.api_recipe_search(ingredients, number)
            for item in api_recipes:
                recipe = crud.recipe_info(item)
                print("api recipe id:", item)
                crud.mealplan_add_recipe(mealplan, recipe)
                number -= 1

    print("after creating mealplan", mealplan.recipes_r)

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
