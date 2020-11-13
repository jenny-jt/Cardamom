"""Script to seed db"""

from datetime import datetime
import os
import json
from model import connect_to_db, db, Ingredient, Inventory, Recipe
from crud import add_ingredient, add_recipe, add_mealplan, update_inventory
from server import app    
from random import choice

os.system('dropdb meals')
os.system('createdb meals')

connect_to_db(app)
db.create_all()

ingredients = [{"name": "onion", "location": "fridge"}, #id 1
                {"name": "egg", "location": "fridge"},  #id 2
                {"name": "kimchi", "location": "fridge"},
                {"name": "bacon", "location": "fridge"},
                {"name": "heavy whipping cream", "location": "fridge"},
                {"name": "parmesan cheese", "location": "fridge"},
                {"name": "napa cabbage", "location": "fridge"},
                {"name": "bok choy", "location": "fridge"},
                {"name": "green beans", "location": "fridge"},
                {"name": "cauliflower", "location": "fridge"},
                {"name": "butter", "location": "fridge"},
                {"name": "carrot", "location": "fridge"},
                {"name": "chuck roast", "location": "freezer"},
                {"name": "steak", "location": "freezer"},
                {"name": "ground pork", "location": "freezer"},
                {"name": "ground turkey", "location": "freezer"},
                {"name": "ground beef", "location": "freezer"},
                {"name": "shrimp", "location": "freezer"},
                {"name": "oxtail", "location": "freezer"},
                {"name": "chicken thigh", "location": "freezer"},
                {"name": "chicken drumstick", "location": "freezer"},
                {"name": "boneless chicken dark meat", "location": "freezer"},
                {"name": "edamame", "location": "freezer"},
                {"name": "frozen peas", "location": "freezer"}, 
                {"name": "frozen corn", "location": "freezer"},
                {"name": "sparerib", "location": "freezer"},
                {"name": "salmon", "location": "freezer"},
                {"name": "spinach", "location": "freezer"},
                {"name": "cherry tomato", "location": "pantry"},
                {"name": "sweet potato", "location": "pantry"},
                {"name": "avocado", "location": "pantry"},
                {"name": "pasta", "location": "pantry"},
                {"name": "quinoa", "location": "pantry"},
                {"name": "potato", "location": "pantry"},
                {"name": "basmati rice", "location": "pantry"},
                {"name": "jasmine rice", "location": "pantry"},
                {"name": "coconut milk", "location": "pantry"},
                {"name": "canned tomato", "location": "pantry"},
                {"name": "tomato paste", "location": "pantry"},
                {"name": "sundried tomato", "location": "pantry"},
                {"name": "ginger", "location": "pantry"}]
                # {"name": "", "location": "pantry"},
                # {"name": "", "location": "fridge"},
                # {"name": "", "location": "freezer"},

recipes = [{"name": "Taiwanese Ground Pork", "ingredients": ["ground pork"], "url":"https://ketchupwithlinda.com/taiwanese-meat-sauce/print/8317/"}, #id 1
            {"name": "Oyakodon", "ingredients": ["boneless chicken dark meat", "onion", "onions", "egg"], "url": "https://www.seriouseats.com/recipes/2016/08/print/oyakodon-japanese-chicken-and-egg-rice-bowl-recipe.html"},
            {"name": "Cuban Shredded Beef", "ingredients": ["chuck roast", "onion" "onions"], "url": "https://thegingeredwhisk.com/shredded-cuban-beef-bowl-slow-cooker/"},
            {"name": "Beef Kabob", "ingredients": ["ground beef", "onion", "onions"], "url": "https://persianmama.com/easyrecipe-print/4465-0/"},
            {"name": "Hainan Chicken", "ingredients": ["chicken thigh", "ginger", "green onion"], "url": "https://www.pressurecookrecipes.com/wprm_print/37694"},
            {"name": "Black Pepper Chicken", "ingredients": ["boneless chicken dark meat"], "url": "https://www.foodandwine.com/recipes/caramelized-black-pepper-chicken?printview"},
            {"name": "Korean Braised Chicken", "ingredients": ["chicken drumstick", "potato", "potatoes", "carrots", "carrot"], "url": "https://mykoreankitchen.com/jjimdak/#wprm-recipe-container-9105"},
            {"name": "Coq Au Vin", "ingredients": ["chicken thigh", "onion", "onions", "carrot", "carrots", "bacon"], "url": "https://www.theendlessmeal.com/julia-childs-coq-au-vin/print/25522/"},
            {"name": "Tuscan Butter Salmon", "ingredients": ["salmon", "sundried tomato", "sundried tomatoes", "spinach", "heavy whipping cream", "parmesan cheese"], "url": "https://cafedelites.com/wprm_print/43059"},
            {"name": "1-2-3-4-5 Spareribs", "ingredients": ["spareribs"], "url": "https://thewoksoflife.com/wprm_print/34693"},
            {"name": "Oxtail", "ingredients": ["oxtail", "carrot", "carrots", "potato", "potatoes"], "url": "https://www.pressurecookrecipes.com/wprm_print/33544"},
            {"name": "Chicken Quinoa Casserole", "ingredients": ["quinoa", "boneless chicken dark meat", "cherry tomato", "cherry tomatoes", "tomato paste"], "url": "https://www.eatyourselfskinny.com/cheesy-caprese-chicken-quinoa-casserole/print/15214/"},
            {"name": "Green Beans", "ingredients": ["green bean", "green beans"], "url": "https://www.myrecipes.com/recipe/quick-easy-green-beans?printview"},
            {"name": "Crispy Persian Rice", "ingredients": ["basmati rice", "butter"], "url": "https://www.halfbakedharvest.com/crispy-persian-rice/"},
            {"name": "Creme Brulee", "ingredients": ["egg", "eggs", "heavy whipping cream"], "url": "https://www.averiecooks.com/the-best-and-the-easiest-classic-creme-brulee/"},
            {"name": "Salted Caramel", "ingredients": ["butter", "heavy whipping cream"], "url": "https://sallysbakingaddiction.com/homemade-salted-caramel-recipe/print-recipe/68127/"}]
# {"name": "", "ingredients": [], "url": ""},       
# kabob url https://persianmama.com/kabob-koobideh-grilled-minced-meat-kabobs/

# recipe_ingredients = [{"ingredient_id":1, "recipe_id":[2,3,4,8]}, {"ingredient_id":2, "recipe_id":[2, 15]}, {"ingredient_id":3, "recipe_id":[]}, 
#                         {"ingredient_id":4, "recipe_id":[8]}, {"ingredient_id":5, "recipe_id":[9, 15, 16]}, {"ingredient_id":6, "recipe_id":[9]}, {"ingredient_id":7, "recipe_id":[]},
#                         {"ingredient_id":8, "recipe_id":[]}, {"ingredient_id":9, "recipe_id":[13]}, {"ingredient_id":10, "recipe_id":[]}, {"ingredient_id":11, "recipe_id":[14, 16]}, 
#                         {"ingredient_id":12, "recipe_id":[7,8,11]}, {"ingredient_id":13, "recipe_id":[3]}, {"ingredient_id":14, "recipe_id":[]}, {"ingredient_id":15, "recipe_id":[1]}] #{"ingredient_id":, "recipe_id":[]}, {"ingredient_id":, "recipe_id":[]}, {"ingredient_id":, "recipe_id":[]}, 
#                         # {"ingredient_id":, "recipe_id":[]}, {"ingredient_id":, "recipe_id":[]}, {"ingredient_id":, "recipe_id":[]}, {"ingredient_id":, "recipe_id":[]}, {"ingredient_id":, "recipe_id":[]},
#                         # {"ingredient_id":, "recipe_id":[]}, {"ingredient_id":, "recipe_id":[]}, {"ingredient_id":, "recipe_id":[]}, {"ingredient_id":, "recipe_id":[]}, 
#                         # {"ingredient_id":, "recipe_id":[]}, {"ingredient_id":, "recipe_id":[]}, {"ingredient_id":, "recipe_id":[]}, {"ingredient_id":, "recipe_id":[]},]

for ingredient in ingredients:
    add_ingredient(name=ingredient['name'], location=ingredient['location'])

# for recipe in recipes:
#     ingredients = ", ".join(recipe['ingredients'])
#     add_recipe(name=recipe['name'], ingredients=ingredients, url=recipe["url"])

location = ["freezer", "fridge", "pantry"]

#making secondary table
for recipe in recipes:
    ingredients = ", ".join(recipe['ingredients'])
    db_recipe = add_recipe(name=recipe['name'], ingredients=ingredients, url=recipe["url"])
    #create recipe object for each recipe in recipes list
    # print(f'recipe is:\n{db_recipe}\n')
    for ingr in recipe["ingredients"]:
        #for each recipe ingredient, query to see if ingredient in db
        db_ingr = Ingredient.query.filter(Ingredient.name==ingr).first()
        if not db_ingr:
            db_ingr = add_ingredient(name=ingr, location=choice(location))
        # print(f'ingredient is:\n{db_ingr}\n')
        #if ingredient is not in db, make a new one with a random location
        db_recipe.ingredients_r.append(db_ingr)
        # print(f'list of recipe ingredients:\n{db_recipe.ingredients_r}\n')
        #append ingredient object to ingredient relationship of recipe
    db.session.add(db_recipe)
    db.session.commit()