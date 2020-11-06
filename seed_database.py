from server import app
from model import connect_to_db, db, Ingredient, Inventory, Recipe
from crud import add_ingredient, add_recipe, add_mealplan, update_inventory

app = connect_to_db(app)
app.app_context().push()

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

recipes = [{"name": "Taiwanese Ground Pork", "ingredients": ["ground pork"], "url":"https://ketchupwithlinda.com/taiwanese-meat-sauce/print/8317/"},
            {"name": "Oyakodon", "ingredients": ["boneless chicken dark meat", "onion"], "url": "https://www.seriouseats.com/recipes/2016/08/print/oyakodon-japanese-chicken-and-egg-rice-bowl-recipe.html"},
            {"name": "Cuban Shredded Beef", "ingredients": ["chuck roast", "onion"], "url": "https://thegingeredwhisk.com/shredded-cuban-beef-bowl-slow-cooker/"},
            {"name": "Beef Kabob", "ingredients": ["ground beef", "onion"], "url": "https://persianmama.com/easyrecipe-print/4465-0/"},
            {"name": "Hainan Chicken", "ingredients": ["chicken thigh", "ginger", "green onion"], "url": "https://www.pressurecookrecipes.com/wprm_print/37694"},
            {"name": "Black Pepper Chicken", "ingredients": ["boneless chicken dark meat"], "url": "https://www.foodandwine.com/recipes/caramelized-black-pepper-chicken?printview"},
            {"name": "Korean Braised Chicken", "ingredients": ["chicken drumstick", "potato", "carrot"], "url": "https://mykoreankitchen.com/jjimdak/#wprm-recipe-container-9105"},
            {"name": "Coq Au Vin", "ingredients": ["chicken thigh", "onion", "carrots"], "url": "https://www.theendlessmeal.com/julia-childs-coq-au-vin/print/25522/"},
            {"name": "Tuscan Butter Salmon", "ingredients": ["salmon", "sundried tomato". "spinach", "heavy whipping cream"], "url": "https://cafedelites.com/wprm_print/43059"},
            {"name": "1-2-3-4-5 Spareribs", "ingredients": ["spareribs"], "url": "https://thewoksoflife.com/wprm_print/34693"},
            {"name": "Oxtail", "ingredients": ["oxtail", "carrot", "potato"], "url": "https://www.pressurecookrecipes.com/wprm_print/33544"},
            {"name": "Chicken Quinoa Casserole", "ingredients": ["quinoa", "boneless chicken dark meat", "cherry tomato", "tomato paste"], "url": "https://www.eatyourselfskinny.com/cheesy-caprese-chicken-quinoa-casserole/print/15214/"},
            {"name": "Green Beans", "ingredients": ["green beans"], "url": "https://www.myrecipes.com/recipe/quick-easy-green-beans?printview"},
            {"name": "Crispy Persian Rice", "ingredients": ["basmati rice", "butter"], "url": "https://www.halfbakedharvest.com/crispy-persian-rice/"},
            {"name": "Creme Brulee", "ingredients": ["egg", "heavy whipping cream"], "url": "https://www.averiecooks.com/the-best-and-the-easiest-classic-creme-brulee/"},
            {"name": "Salted Caramel", "ingredients": ["butter", "heavy whipping cream"], "url": "https://sallysbakingaddiction.com/homemade-salted-caramel-recipe/print-recipe/68127/"}]

# {"name": "", "ingredients": [], "url": ""},       
# kabob url https://persianmama.com/kabob-koobideh-grilled-minced-meat-kabobs/

for ingredient in ingredients:
    add_ingredient(name=ingredient["name"], location=ingredient["location"])

for recipe in recipes:
    ingredients = ", ".join(recipe['ingredients'])
    add_recipe(name=recipe['name'], ingredients=ingredients, url=recipe["url"])



