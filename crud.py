"""CRUD operations."""
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import db, connect_to_db, Ingredient, Inventory, Recipe, MealPlan
import spoonacular as sp

api = sp.API(os.environ['apiKey'])

def add_ingredient(name,location):
    """add ingredient"""
    ingredient = Ingredient(name=name, location=location)
    db.session.add(ingredient)
    db.session.commit()

    return ingredient

def add_recipe(name, ingredients, url):
    """add recipes with required ingredient(s)"""
    recipe = Recipe(name=name, ingredients=ingredients, url=url)
    db.session.add(recipe)
    db.session.commit()

    return recipe


def add_mealplan(date):
    """add meal plan with date"""
    mealplan = MealPlan(date=date)
    db.session.add(mealplan)
    db.session.commit()

    return mealplan


def update_inventory(ingredient, bought, use_this_week, in_stock, quantity):
    """update inventory when ingredient bought or used"""

    inventory = Inventory(ingredient_r=ingredient, bought=bought, use_this_week=use_this_week, in_stock=in_stock, quantity=quantity)
    
    db.session.add(inventory)
    db.session.commit()

    return inventory

def db_recipe_search(ingredients):
    """takes in ingredients and num_recipes from form, outputs list of recipes from db"""
    """if not have one recipe that contains db_recipe = Recipe.query.filter(Recipe.ingredients.contains(ingredients)).all()all ingredients, loop over list of ingredients and search for ingredients individually"""
    # will make a list (or empty list) for each ingredient
    # want it to make a list containing recipes from search of all ingredients
    db_recipes =[]
  
    for ingredient in ingredients: 
        db_recipe = Recipe.query.filter(Recipe.ingredients.contains(ingredient)).distinct().all()
        print("for ingredient loop in db_recipe_search:", db_recipe)
        if db_recipe:
            db_recipes.extend(db_recipe)
    print(db_recipes)        
    return db_recipes


def api_recipe_search(ingredients, number):
    """"takes in main ingredient(s) and number of recipes, returns list of recipe ids that match"""
    response = api.search_recipes_by_ingredients(ingredients, number)
    data = response.json()
    api_recipe_ids = []

    for i in range(number):
        # recipe_title = data[i]['title']
        api_id = data[i]['id']
        api_recipe_ids.append(api_id)

    return api_recipe_ids


def recipe_info(recipe_api_id):
    """retrieve recipe info and add recipe to database, returns recipe object. DO I WANT TO GROW DB??"""
    response = api.get_recipe_information(id=recipe_api_id)
    data = response.json()
    # recipe_img = data['image']
    name = data['title']
    # cook time = data[‘readyInMinutes’]

    recipe_ingredients = []
    for i, item in enumerate(data['extendedIngredients']):
        recipe_ingredients.append(data['extendedIngredients'][i]['name'])

    url = data['sourceUrl']

    check_recipe_db = Recipe.query.filter(Recipe.name == name).first()

    if not check_recipe_db:
        recipe = add_recipe(name, recipe_ingredients, url)  
        return recipe


def mealplan_add_recipe(mealplan, recipe): 
    """add recipe to mealplan"""
    mealplan.add_recipe_to_mealplan(recipe) 

    print("recipe added to mealplan")

 
if __name__ == '__main__':
    from server import app
    connect_to_db(app)