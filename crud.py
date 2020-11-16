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

def add_recipe(name, ingredients, url, cook_time="n/a"):
    """add recipes with required ingredient(s)"""
    recipe = Recipe(name=name, ingredients=ingredients, url=url, cook_time=cook_time)
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


# this is the way to get db_recipes without secondary table
def db_recipe_search(ingredients):
    """takes in ingredients and num_recipes from form, outputs unique list of recipes from db"""
    """if not have one recipe that contains db_recipe = Recipe.query.filter(Recipe.ingredients.contains(ingredients)).all()all ingredients, loop over list of ingredients and search for ingredients individually"""
    # will make a list (or empty list) for each ingredient
    # want it to make a list containing recipes from search of all ingredients
    db_recipes = []

    for ingredient in ingredients:
        db_recipe = Recipe.query.filter(
            Recipe.ingredients.contains(ingredient)).distinct()
        if db_recipe:
            db_recipes.extend(db_recipe)

    db_recipes = set(db_recipes)
    db_recipes = list(db_recipes)

    return db_recipes


# this utilizes secondary table to generate db_recipes
def db_recipe_r(ingredients):
    """takes list of ingredients from form and outputs unique list of recipes associated with those ingredients"""
    db_recipes = []
    location = ["freezer", "fridge", "pantry"]

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
    # number = session['num']
    response = api.search_recipes_by_ingredients(ingredients, number=number, ranking=1)
    data = response.json()
    api_recipe_ids = set()

    for i in range(num):
        # recipe_title = data[i]['title']
        api_id = data[i]['id']
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


# TODO: may need to add secondary table code here to keep db updated
def recipe_info(recipe_api_id):
    """take in id of api recipe and retrieve recipe info and add recipe to db, returns recipe object"""
    response = api.get_recipe_information(id=recipe_api_id)
    data = response.json()
    print(f"\nthis is the data response from recipe info: {data}\n")

    # recipe_img = data['image']
    name = str(data['title'])
    cook_time = int(data['readyInMinutes'])
    url = data['sourceUrl']

    recipe_ingredients = []
    ingr_data = data['extendedIngredients']
    print(f"\nthis is the recipe ingredient data: {data}\n")

    for i, item in enumerate(ingr_data):
        ingredient_id = ingr_data[i]['id']
        print(f"id: {ingredient_id}")
        ingredient_name = ingr_data[i]['name']
        print(f"name: {ingredient_name}")
        if ingredient_id != "None":
            recipe_ingredients.append(ingredient_name)
    print(f"\nthis is the recipe ingredient data: {recipe_ingredients}\n")

    check_db = Recipe.query.filter(Recipe.name == name).first()

    if not check_db:
        ingredients = ", ".join(recipe_ingredients)
        recipe = add_recipe(name=name, ingredients=ingredients, url=url, cook_time=cook_time)
        print(f"\nnew api recipe added to db: {recipe}\n")
        return recipe

    return check_db


# TODO: check if mealplan obj is accumulating more recipes
def mealplan_add_recipe(mealplan, recipes_list):
    """takes in mealplan obj and list of recipes
    adds recipes to mealplan via a method,
    returns list of recipes associated with mealplan obj
    """
    for item in recipes_list:
        mealplan.add_recipe_to_mealplan(item) 

    recipes = mealplan.recipes_r  #this should keep accumulating more recipes?
    print(f"recipes in mealplan: {recipes} ")
    return recipes

# onion = Ingredient.query.filter_by(name="onion").one()
# print(onion.recipes_r)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
