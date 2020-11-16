from flask import Flask, request, render_template, redirect, session, flash, json
from datetime import datetime
from model import connect_to_db, Ingredient, Recipe, MealPlan
import crud
import os
import jsonpickle
from json import JSONEncoder
from random import choice
import requests
import jinja2

import spoonacular as sp
import google.oauth2.credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from urllib.parse import parse_qs
from oauth2client import file, client, GOOGLE_TOKEN_URI


app = Flask(__name__)
app.secret_key = os.environ['secret_key']

CLIENT_SECRETS_FILE = 'client_secret.json'
API_SERVICE_NAME = 'cal'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']


@app.route("/")
def show_homepage():
    """Show the application's homepage."""
    date = session['date']
    print(f"\nthis is the date from session: {date}\n")
    # events = cal.events().list()

    # return render_template('homepage.html', events=events)
    return render_template('homepage.html')


@app.route('/authorize')
def authorize():
    '''Asks user for authorization to google calendar account'''

    # creates flow instance to manage OAuth grant access, uri configured in API Google console
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
                                         scopes=SCOPES,
                                         redirect_uri='http://localhost:5000/callback')

    # finds authorization url
    authorization_url, state = flow.authorization_url(
                                access_type='offline',
                                include_granted_scopes='true')

    session['state'] = state

    # redirect user to authorization url 
    return redirect(authorization_url)


def credentials_to_dict(credentials):
    """Takes in credentials from OAuth and returns in dictionary format"""

    # Returns dictionary for OAuth process
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


@app.route('/callback')
def callback():
    '''Processes response for google calendar authorization'''

    # creates flow instance to manage OAuth grant access
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
                                         scopes=SCOPES,
                                         redirect_uri='http://localhost:5000/callback')

    authorization_response = request.url

    # fetch tocken for the authorization response
    flow.fetch_token(authorization_response=authorization_response)

    # credentials stored
    credentials = flow.credentials

    session['credentials'] = credentials_to_dict(credentials)

    d = session.get('date')  # is none
    print(f"\nthis is the date string stored in session when called: {d}\n")

    flash('Succesfully logged in to Google Calendar!')
    return render_template('search-form.html')


@app.route("/search")
def search_results():
    """take in date for mealplan, ingredients, and number of recipes, outputs mealplan with attached recipes"""
    ingredients = request.args.get("ingredients").split(",")
    num = int(request.args.get("num_recipes"))
    session['num'] = num
    date = request.args.get("date")
    session['date'] = date

    # make sure there is a mealplan obj
    mealplan = check_mealplan(date)

    # this is the way without using secondary table
    # db_recipes = crud.db_recipe_search(ingredients) 
    db_recipes = crud.db_recipe_r(ingredients)

    if len(db_recipes) < num:
        api_recipe_ids = crud.api_id_search(ingredients, num)
        api_recipes = crud.api_recipes_list(api_recipe_ids)
        recipe_list = make_recipe_list(num, db_recipes, api_recipes)
    else:
        recipe_list = make_recipe_list(num, db_recipes)

    recipes = crud.mealplan_add_recipe(mealplan, recipe_list)

    return render_template('recipe-display.html', recipes=recipes) 


def check_mealplan(date):
    """checks if mealplan exists, otherwise makes a new mealplan object"""
    mealplan = MealPlan.query.filter(MealPlan.date == date).first()

    if not mealplan:
        mealplan = crud.add_mealplan(date)

    return mealplan


def make_recipe_list(number, db_recipes, api_recipes=[]):
    """makes a list of recipes that is the number requested by user"""

    count = 0
    recipe_list = []
    while count < number:
        if db_recipes:
            item = pick_recipes(db_recipes)
            db_recipes.remove(item)
        else:
            item = pick_recipes(api_recipes)
            api_recipes.remove(item)

        recipe_list.append(item)
        count += 1   
    print(f"this is the final recipe list output: {recipe_list}")     

    return recipe_list


def pick_recipes(recipes):
    """takes in list of recipes, picks a random recipe from list"""
    item = choice(recipes)

    return item


# TODO: get request to retrieve meal plan obj (in session) as json blob. 
# user says looks good, add to gcal. This pg will post to make_calendar_event
@app.route('/add-to-cal', methods=['POST'])
def make_calendar_event():
    """Add all-day recipe event to user's google calendar with OAUTH"""
    cal_id = 'tl9a33nl5al9k337lh45f40av8@group.calendar.google.com'
    # checks if credentials not already in session
    if 'credentials' not in session:
        return redirect('/authorize')
    # gets information about recipe to add to calendar

    # grabs stored OAuth credentials
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])

    # google api client to make google calendar event
    cal = build('calendar', API_VERSION, credentials=credentials)

    # session way to retrieve mealplan object
    # mplan = jsonpickle.decode(session['mealplan'])
    # mealplan = json.loads(mplan)
    # print(f"this is the mealplan object from session: {mealplan}")
    d = request.args.get("date")
    print(d)
    # mealplan = check_mealplan(date)

    # mealplan = MealPlan.query.filter(MealPlan.date == date).first()
    # recipes = mealplan.recipes_r
    # print(f"this is the list of recipe objects from mealplan: {recipes}")
    # creates google calendar event for each recipe in mealplan 
    # recipes = [<Recipe name=Creme Brulee ingredients=egg, eggs, heavy whipping cream>, <Recipe name=Hard-Boiled Eggs ingredients=eggs, eggs, hard boiled eggs, hard-boiled eggs, cook: mins, prep: mins, print, save, total: mins>]
    recipes = Recipe.query.filter(Recipe.ingredients.contains("carrot")).distinct()
    print(f"\nrecipe list to make events: {recipes}\n")
    for recipe in recipes:
        event = make_cal_event(recipe, d)
        # adds the calendar event to the google calendar
        add_event = cal.events().insert(calendarId=cal_id, sendNotifications=True, body=event).execute()

    flash('Recipes added to MealPlan calendar!')
    # maybe another button/option to add more meal plan?
    render_template('mealplan.html')


def make_cal_event(recipe, date):
    """Takes in recipe object, turns it into gcal event body with:
    date of event: mealplan date (or random choice of mealplan dates)
    name of event: recipe name 
    description of event: cook time
    source: recipe url
    # recipes = [<Recipe name = 3-Ingredient Bacon Stuffed Mushrooms ingredients = {"button mushrooms", "cooked bacon", "feta cheese"}>, 
    # <Recipe name = Easy Pesto Stuffed Mushrooms ingredients = {"button mushrooms", parmesan, pesto }>]
    """
    # date = "2020-11-13"
    # name = recipe.name
    # url = recipe.url
    # description = "recipe cook time"
    # date = mealplan.date
    print(f"this is the recipe name used to make the cal event: {recipe.name}")
    # dictionary for google event information

    event = {
            'summary': recipe.name,
            'start': {"date": date},
            'end': {"date": date},
            # 'description': description,
            'source': {"url": recipe.url}
            }

    return event


# @app.route("/recipe/display")
# def display_recipe():
#     """ display recipe printout via link"""

#     return render_template('recipe-display.html')


@app.route("/mealplan")
def show_meal_plan(date):
    """ display meal plan for certain dates """

    return render_template('meal-plan.html', date=date)


@app.route("/inventory")
def update_inventory():
    """ form with default values for location, able to save timestamp, quantity """

    return render_template('inventory.html')


# @app.route("/search")
# def show_search_form():
#     """Show form to enter date for mealplan and main ingredient(s) for recipes""" 

#     return render_template('search-form.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
