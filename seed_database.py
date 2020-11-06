from server import app
from model import connect_to_db, db, Ingredient, Inventory, Recipe, Ingredient_Recipe, Recipe

dropdb
createdb

ingredients = [{"name": "onion", "location": "fridge"}, 
                {"name": "egg", "location": "fridge"},
                {"name": "kimchi", "location": "fridge"},
                {"name": "bacon", "location": "fridge"},
                {"name": "heavy whipping cream", "location": "fridge"},
                {"name": "parmesan cheese", "location": "fridge"},
                {"name": "napa cabbage", "location": "fridge"},
                {"name": "bok choy", "location": "fridge"},
                {"name": "", "location": "fridge"},
                {"name": "chuck roast", "location": "freezer"},
                {"name": "steak", "location": "freezer"},
                {"name": "ground pork", "location": "freezer"},
                {"name": "ground turkey", "location": "freezer"},
                {"name": "ground beef", "location": "freezer"},
                {"name": "shrimp", "location": "freezer"},
                {"name": "oxtail", "location": "freezer"},
                {"name": "chicken thigh", "location": "freezer"},
                {"name": "boneless chicken dark meat", "location": "freezer"},
                {"name": "", "location": "freezer"},
                {"name": "", "location": "freezer"}, 
                {"name": "sparerib", "location": "freezer"},
                {"name": "cherry tomato", "location": "pantry"},
                {"name": "sweet potato", "location": "pantry"},
                {"name": "avocado", "location": "pantry"},
                {"name": "pasta", "location": "pantry"},
                {"name": "coconut milk", "location": "pantry"},
                {"name": "", "location": "pantry"},
                {"name": "", "location": "fridge"},
                {"name": "", "location": "freezer"}]

for ingredient in ingredients:
   Ingredient(name=ingredient['name'], ...).save()