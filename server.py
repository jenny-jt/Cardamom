from flask import Flask, request, render_template, jsonify

import os
import requests

import spoonacular as sp

app = Flask(__name__)
app.secret_key = "SECRET"

# apiKey = os.environ['apiKey']
api = sp.API(os.environ['apiKey'])

@app.route("/")
def show_homepage():
    """Show the application's homepage."""

    return render_template('homepage.html')

@app.route("/search")
def show_search_form():
    """Show search recipes form to enter main ingredient(s)""" 

    return render_template('search-form.html')

@app.route("/recipe/search")
    """Search for recipes by entering main ingredient(s)"""

    ingredients = request.args.get('ingredients')
    num_recipes = request.args.get('num_recipes', 1)

    url = 
    return render_template('recipe-search.html')



# @app.route("/inventory")
# #what type of form, able to save timestamp, quantity, location

# @app.route("/mealplan")
#   """ display meal plan for certain date """


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')