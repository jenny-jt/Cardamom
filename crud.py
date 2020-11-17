"""CRUD operations."""
import os
# from flask_sqlalchemy import SQLAlchemy
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


def all_recipes():
    """output all recipes in database"""
    recipes = Recipe.query.all()

    return recipes


def all_mealplans():
    """output all mealplans in database"""
    mealplans = MealPlan.query.all()

    return mealplans


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


def create_api_recipes(ingredients, num):
    api_ids = api_id_search(ingredients, num)
    api_recipes = api_recipes_list(api_ids)

    return api_recipes


def api_id_search(ingredients, number):
    """"takes in main ingredient(s) and number of recipes,
     returns list (length of number) of unique recipe ids
    """
    # response from API for number of recipes, will extract recipe ids
    response = api.search_recipes_by_ingredients(ingredients, number=number, ranking=1)
    data = response.json()
    api_recipe_ids = set()

    for i in range(number):
        api_id = data[i]['id']
        api_recipe_ids.add(api_id)  # add id to a set
    api_recipe_ids = list(api_recipe_ids)  # turn set of ids into a list

    return api_recipe_ids


# TODO: refactor
def recipe_info(recipe_api_id):
    """take in id of api recipe and retrieve recipe info and add recipe to db, returns recipe object"""
    response = api.get_recipe_information(id=recipe_api_id)
    data = response.json()
    print(f"\nthis is the data response from recipe info: {data}\n")

    # recipe_img = data['image']
    name = str(data['title'])
    cook_time = int(data['readyInMinutes'])
    url = data['sourceUrl']

    recipe_ingredients = set()
    ingr_data = data['extendedIngredients']
    for ingr in ingr_data:
        if ingr["id"]:  # if the ID exists
            print(f"id: {ingr['id']}")
            print(f"name: {ingr['name']}")

    # ingr_data = data['analyzedInstructions'][0]['steps'][0]['ingredients']  # a list of dictionary objects
    print(f"\nthis is the extended ingredient data: {data}\n")

    for i, item in enumerate(ingr_data):
        ingredient_id = ingr_data[i]['id']
        print(f"id: {ingredient_id}")
        ingredient_name = ingr_data[i]['name']
        print(f"name: {ingredient_name}")
        if ingredient_id != "None":
            recipe_ingredients.add(ingredient_name)
    print(f"\nthis is the recipe ingredient data: {recipe_ingredients}\n")
    recipe_ingredients = list(recipe_ingredients)

    # check if recipe already exists in db
    check_db = Recipe.query.filter(Recipe.name == name).first()

    if not check_db:
        ingredients = ", ".join(recipe_ingredients)
        recipe = add_recipe(name=name, ingredients=ingredients, url=url, cook_time=cook_time)

        location = ["freezer", "fridge", "pantry"]

        for ingr in ingredients:
            # for each recipe ingredient, query to see if ingredient in db
            db_ingr = Ingredient.query.filter(Ingredient.name == ingr).first()

            # if ingredient is not in db, make a new one with a random location
            if not db_ingr:
                db_ingr = add_ingredient(name=ingr, location=choice(location))
            # append ingredient object to ingredient relationship of recipe
            recipe.ingredients_r.append(db_ingr)
        # print(f'list of recipe ingredients:\n{db_recipe.ingredients_r}\n')

        db.session.add(recipe)
        db.session.commit()
        print(f"\nnew api recipe added to db: {recipe}\n")
        return recipe

    return check_db


def api_recipes_list(api_recipe_ids):
    """takes in list of recipe ids and outputs list of assoc recipes"""
    api_recipes = []

    for api_id in api_recipe_ids:
        recipe = recipe_info(api_id)
        api_recipes.append(recipe)
    print(f"this is the list of api recipes from crud: {api_recipes}")
    return api_recipes


def mealplan_add_recipe(mealplan, recipes_list):
    """takes in mealplan obj and list of recipes
    adds recipes to mealplan via a method,
    returns list of unique recipes associated with mealplan obj
    """
    for item in recipes_list:
        if item not in mealplan.recipes_r:
            mealplan.add_recipe_to_mealplan(item)
            db.session.commit()

    recipes = mealplan.recipes_r

    print(f"recipe objects associated with mealplan: {recipes}")
    return recipes


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


if __name__ == '__main__':
    from server import app
    connect_to_db(app)