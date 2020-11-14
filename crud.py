"""CRUD operations."""
import os
from flask_sqlalchemy import SQLAlchemy
from random import choice
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
    """takes in ingredients and num_recipes from form, outputs unique list of recipes from db"""
    """if not have one recipe that contains db_recipe = Recipe.query.filter(Recipe.ingredients.contains(ingredients)).all()all ingredients, loop over list of ingredients and search for ingredients individually"""
    # will make a list (or empty list) for each ingredient
    # want it to make a list containing recipes from search of all ingredients
    db_recipes =[]
  
    for ingredient in ingredients: 
        db_recipe = Recipe.query.filter(
            Recipe.ingredients.contains(ingredient)).distinct()
        if db_recipe:
            db_recipes.extend(db_recipe)
    print(f"\nlist of all db_recipes: {db_recipes}\n")  
    db_recipes = set(db_recipes)
    db_recipes = list(db_recipes)
    print(f"\nlist of all db_recipes: {db_recipes}\n")      

    return db_recipes

def db_recipe_r(ingredients):
    """takes list of ingredients from form and outputs unique list of recipes associated with those ingredients"""
    db_recipes = []

    for ingredient in ingredients:
        ingr = Ingredient.query.filter(Ingredient.name == ingredient).first()
        if not ingr:
            ingr = add_ingredient(name=ingredient, location=choice(location))
        ingr_recipes = ingr.recipes_r
        db_recipes.extend(ingr_recipes)

    db_recipes = set(db_recipes)
    db_recipes = list(db_recipes)

    return db_recipes


def api_id_search(ingredients, number):
    """"takes in main ingredient(s) and number of recipes,
     returns list (length of number) of unique recipe ids
    """
    response = api.search_recipes_by_ingredients(ingredients, number)
    #search API for number of recipes with ingredients
    data = response.json()
    print(f"this is the data response from api: {data}")
    api_recipe_ids = set()

    for i in range(number):
        # recipe_title = data[i]['title']
        api_id = data[i]['id']
        print(f"this is the api id extracted from the api request: {api_id}")
        api_recipe_ids.add(api_id)  # add id to a set
    api_recipe_ids = list(api_recipe_ids)  # turn set of ids into a list
    
    return api_recipe_ids


def api_recipes_list(api_recipe_ids):
    """takes in list of recipe ids and outputs list of assoc recipes"""
    api_recipes = []

    for api_id in api_recipe_ids:
        recipe = recipe_info(api_id)
        api_recipes.append(recipe)
    print(f"this is the list of api recipes from crud: {api_recipes}")
    return api_recipes


#TODO: may need to add secondary table code here to keep db updated
def recipe_info(recipe_api_id):
    """take in id of api recipe and retrieve recipe info and add recipe to db, returns recipe object"""
    response = api.get_recipe_information(id=recipe_api_id)
    data = response.json()
    # recipe_img = data['image']
    name = str(data['title'])
    print(f"this is the name of the api recipe: {name}")
    # cook time = data[‘readyInMinutes’]

    recipe_ingredients = []
    print(f"ingredients from api recipe: {data['extendedIngredients']}")
    for i, item in enumerate(data['extendedIngredients']):
        print(f"data in ingredients list: {data['extendedIngredients'][i]['name']}")
        recipe_ingredients.append(data['extendedIngredients'][i]['name'])

    url = data['sourceUrl']

    check_recipe_db = Recipe.query.filter(Recipe.name == name).first()

    if not check_recipe_db:
        recipe = add_recipe(name, recipe_ingredients, url)  
        return recipe


#TODO: add for loop
def mealplan_add_recipe(mealplan, item): 
    """takes in mealplan and adds recipe to mealplan via a method, returns list of recipes associated with mealplan obj"""

    mealplan.add_recipe_to_mealplan(item) 
    recipes = mealplan.recipes_r

    print("recipes added to mealplan")
    return recipes

# onion = Ingredient.query.filter_by(name="onion").one()
# print(onion.recipes_r)
 
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
