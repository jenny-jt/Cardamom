"""Script to seed db"""

from datetime import datetime
import os
import json
from model import connect_to_db, db, Ingredient, Inventory, Recipe, User
from crud import add_user, add_ingredient, add_recipe, add_mealplan
from server import app
from random import choice

# try to use functions instead of these commands. ? how would i set these up in functions
os.system('dropdb meals')
os.system('createdb meals')

connect_to_db(app)
db.create_all()

ingredients = [{"name": "onion", "location": "fridge"},
               {"name": "egg", "location": "fridge"},
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

recipes = [{"name": "Taiwanese Ground Pork", "ingredients": ["ground pork"], 
            "url":"https://ketchupwithlinda.com/taiwanese-meat-sauce/print/8317/", "cook_time": 20, 
            "image": "https://ketchupwithlinda.com/wp-content/uploads/2019/08/Taiwanese-Meat-Sauce-8.jpg"},
           {"name": "Oyakodon", "ingredients": ["boneless chicken dark meat", "onion", "onions", "egg"], 
            "url": "https://www.seriouseats.com/recipes/2016/08/print/oyakodon-japanese-chicken-and-egg-rice-bowl-recipe.html", 
            "cook_time": 20, "image": "https://www.seriouseats.com/recipes/images/2016/08/20160802-oyakodon-4.jpg"},
           {"name": "Cuban Shredded Beef", "ingredients": ["chuck roast", "onion", "onions"], 
            "url": "https://thegingeredwhisk.com/shredded-cuban-beef-bowl-slow-cooker/", "cook_time": 502, 
            "image": "https://littlespicejar.com/wp-content/uploads/2016/06/Slow-Cooker-Shredded-Cuban-Beef-Ropa-Vieja.jpg"},
           {"name": "Beef Kabob", "ingredients": ["ground beef", "onion", "onions"], 
            "url": "https://persianmama.com/easyrecipe-print/4465-0/", "cook_time": 35,
            "image":"https://persianmama.com/wp-content/uploads/2015/06/Kabob-Koobideh-1.jpg" },
           {"name": "Hainan Chicken", "ingredients": ["chicken thigh", "ginger", "green onion"], 
            "url": "https://www.pressurecookrecipes.com/wprm_print/37694", "cook_time": 55,
            "image": "https://www.pressurecookrecipes.com/wp-content/uploads/2016/06/hainanese-chicken-rice-1400x730.jpg"},
           {"name": "Black Pepper Chicken", "ingredients": ["boneless chicken dark meat"], 
            "url": "https://www.foodandwine.com/recipes/caramelized-black-pepper-chicken?printview", "cook_time": 35,
            "image": "https://imagesvc.meredithcorp.io/v3/jumpstartpure/image?url=https://static.onecms.io/wp-content/uploads/sites/9/2013/12/06/1660653193_5845980217001_5844985129001-vs.jpg&w=1280&h=720&q=90&c=cc"},
           {"name": "Korean Braised Chicken", "ingredients": ["chicken drumstick", "potato", "potatoes", "carrots", "carrot"],
            "url": "https://mykoreankitchen.com/jjimdak/#wprm-recipe-container-9105", "cook_time": 60,
            "image": "https://mykoreankitchen.com/wp-content/uploads/2016/06/1.-Jjimdak-Korean-Braised-Chicken.jpg"},
           {"name": "Coq Au Vin", "ingredients": ["chicken thigh", "onion", "onions", "carrot", "carrots", "bacon"], 
            "url": "https://www.theendlessmeal.com/julia-childs-coq-au-vin/print/25522/", "cook_time": 75,
            "image": "https://images.themodernproper.com/billowy-turkey/production/posts/2018/coq-au-vin-9.jpg?w=1200&auto=compress%2Cformat&fit=crop&fp-x=0.5&fp-y=0.5&crop=focalpoint&s=2bcd42007f2b4b5392aa6111a71d778a"},
           {"name": "Tuscan Butter Salmon", "ingredients": ["salmon", "sundried tomato", "sundried tomatoes", "spinach", 
            "heavy whipping cream", "parmesan cheese"], "url": "https://cafedelites.com/wprm_print/43059", "cook_time": 25,
            "image": "https://cafedelites.com/wp-content/uploads/2017/08/Creamy-Garlic-Butter-Tuscan-Salmon-Trout-IMAGE-35.jpg"},
           {"name": "1-2-3-4-5 Spareribs", "ingredients": ["spareribs"], "url": "https://thewoksoflife.com/wprm_print/34693", "cook_time": 40,
            "image": "https://thewoksoflife.com/wp-content/uploads/2019/10/12345-ribs-12.jpg"},
           {"name": "Oxtail", "ingredients": ["oxtail", "carrot", "carrots", "potato", "potatoes"],
            "url": "https://www.pressurecookrecipes.com/wprm_print/33544", "cook_time": 110,
            "image": "https://www.pressurecookrecipes.com/wp-content/uploads/2019/05/instant-pot-oxtail.jpg"},
           {"name": "Chicken Quinoa Casserole", "ingredients": ["quinoa", "boneless chicken dark meat", "cherry tomato", "cherry tomatoes", "tomato paste"], 
            "url": "https://www.eatyourselfskinny.com/cheesy-caprese-chicken-quinoa-casserole/print/15214/", "cook_time": 35,
            "image": "https://www.eatyourselfskinny.com/wp-content/uploads/2016/09/caprese-quinoa-casserole-3-1096x1644.jpg"},
           {"name": "Green Beans", "ingredients": ["green bean", "green beans"], 
            "url": "https://www.myrecipes.com/recipe/quick-easy-green-beans?printview", "cook_time": 6,
            "image": "https://imagesvc.meredithcorp.io/v3/jumpstartpure/image?url=https://static.onecms.io/wp-content/uploads/sites/19/2015/01/26/429048911_5795418733001_5795413682001-vs.jpg&w=1280&h=720&q=90&c=cc"},
           {"name": "Crispy Persian Rice", "ingredients": ["basmati rice", "butter"], 
            "url": "https://www.halfbakedharvest.com/crispy-persian-rice/", "cook_time": 60,
            "image": "https://www.halfbakedharvest.com/wp-content/uploads/2020/03/Crispy-Persian-Rice-Tahdig-with-Spiced-Golden-Chickpeas-10.jpg"},
           {"name": "Creme Brulee", "ingredients": ["egg", "eggs", "heavy whipping cream"], 
            "url": "https://www.averiecooks.com/the-best-and-the-easiest-classic-creme-brulee/", "cook_time": 120,
            "image": "https://www.averiecooks.com/wp-content/uploads/2014/05/cremebrulee-11.jpg"},
           {"name": "Salted Caramel", "ingredients": ["butter", "heavy whipping cream"], 
            "url": "https://sallysbakingaddiction.com/homemade-salted-caramel-recipe/#tasty-recipes-68127", "cook_time": 10,
            "image": "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/delish-caramel-process-324-1541722452.jpg?resize=980:*"},
           {"name": "Shrimp Scampi", "ingredients": ["butter", "shrimp"],
            "url": "https://www.foodnetwork.com/recipes/tyler-florence/shrimp-scampi-with-linguini-recipe-1942429", "cook_time": 40,
            "image": "https://food.fnr.sndimg.com/content/dam/images/food/fullset/2020/07/16/0/FNM_090120-Classic-Shrimp-Scampi_s4x3.jpg.rend.hgtvcom.826.620.suffix/1594915956100.jpeg"},
           {"name": "Lentil Soup", "ingredients": ["lentils", "diced tomatoes", "curry powder"],
            "url": "https://cookieandkate.com/best-lentil-soup-recipe/print/23764/", "cook_time": 55,
            "image": "https://cookieandkate.com/images/2019/01/best-lentil-soup-recipe-4.jpg"},
           {"name": "Zuppa Toscana", "ingredients": ["italian sausage", "potato", "potatoes", "kale"], 
            "url": "https://www.simplyhappyfoodie.com/instant-pot-zuppa-toscana-sausage-potato-soup/#wprm-recipe-container-2090", 
            "cook_time": 65, "image": "https://www.simplyhappyfoodie.com/wp-content/uploads/2017/09/Instant-Pot-Zuppa-Toscana-sausage-potato-soup-1.jpg"}]
# {"name": "", "ingredients": [], "url": ""},       
# kabob url https://persianmama.com/kabob-koobideh-grilled-minced-meat-kabobs/

users = [{"name": "user", "email": "email@test.com", "password": "pw"},
         {"name": "Bob", "email": "1@test.com", "password": "1"},
         {"name": "Richard", "email": "2@test.com", "password": "2"},
         {"name": "Turtle", "email": "3@test.com", "password": "3"}]

for ingredient in ingredients:
    ingr = add_ingredient(name=ingredient['name'], location=ingredient['location'])
    db.session.add(ingr)
    db.session.commit()

location = ["freezer", "fridge", "pantry"]
# making recipe and secondary table, having ingredients associated with recipes and vice versa
for recipe in recipes:
    ingredients = ", ".join(recipe['ingredients'])
    db_recipe = add_recipe(name=recipe['name'], ingredients=ingredients, url=recipe["url"], cook_time=recipe['cook_time'], image=recipe['image'])
    # create recipe object for each recipe in recipes list
    # print(f'recipe is:\n{db_recipe}\n')
    for ingr in recipe["ingredients"]:
        # for each recipe ingredient, query to see if ingredient in db
        db_ingr = Ingredient.query.filter(Ingredient.name == ingr).first()
        if not db_ingr:
            db_ingr = add_ingredient(name=ingr, location=choice(location))
            db.session.add(db_ingr)
            db.session.commit()
        # if ingredient is not in db, make a new one with a random location
        db_recipe.ingredients_r.append(db_ingr)
        # append ingredient object to ingredient relationship of recipe
    db.session.add(db_recipe)
    db.session.commit()


for user in users:
    user = add_user(name=user['name'], email=user['email'], password=user['password'])
    db.session.add(user)
    db.session.commit()

if __name__ = "__main__":
    ###