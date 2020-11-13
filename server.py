from flask import Flask, request, render_template, jsonify, redirect, session, flash
from datetime import datetime
import re
import json
from model import connect_to_db, Ingredient, Recipe, MealPlan
import crud
import os
from random import choice
import requests
import jinja2

import spoonacular as sp
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from apiclient.discovery import build
import httplib2
from urllib.parse import parse_qs
from oauth2client import file, client, GOOGLE_TOKEN_URI


app = Flask(__name__)
app.secret_key = os.environ['secret_key']

CLIENT_SECRETS_FILE = 'client_secret.json'
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

# gcal = build_calendar_service()

@app.route("/")
def show_homepage():
    """Show the application's homepage."""
    
    # events = gcal.events().list()

    # return render_template('homepage.html', events=events)
    return render_template('homepage.html')

@app.route("/search")
def show_search_form():
    """Show form to enter date for mealplan and main ingredient(s) for recipes""" 

    return render_template('search-form.html')

@app.route("/results/search")
def search_results(): 
    """take in date for mealplan, ingredients, and number of recipes, outputs mealplan with attached recipes"""
    ingredients = request.args.get("ingredients").split(",")
    number = int(request.args.get("num_recipes"))
    date = request.args.get("date")
    location = ["freezer", "fridge", "pantry"]
    
    mealplan = MealPlan.query.filter(MealPlan.date == date).first()

    if not mealplan: 
        mealplan = crud.add_mealplan(date)

    # db_recipes = crud.db_recipe_search(ingredients)
    db_recipes = crud.db_recipe_r(ingredients)

    api_recipe_ids = crud.api_recipe_search(ingredients, number)
    api_recipes = api_recipes_list(api_recipe_ids)
    print(f"this is api recipe list: {api_recipes}")

# should separate this out into post because modified db *******
    count = 0
    while count < number:
        if db_recipes:
            item = pick_recipes(db_recipes)
            db_recipes.remove(item)
        else:
            item = pick_recipes(api_recipes)
            api_recipes.remove(item)
                
        crud.mealplan_add_recipe(mealplan, item)
        count += 1    

    recipes = mealplan.recipes_r

    return render_template('recipe-display.html', recipes=recipes)


def api_recipes_list(api_recipe_ids):
    """takes in list of recipe ids and outputs list of assoc recipes"""
    api_recipes = []

    for api_id in api_recipe_ids:
        recipe = crud.recipe_info(api_id)
        api_recipes.append(recipe)
    print(f"this is the list of recipes from api: {api_recipes}")
    return api_recipes


def pick_recipes(recipes):
    """takes in list of recipes, picks a random recipe from list"""
    item = choice(recipes)

    return item    


@app.route("/inventory")
def update_inventory():
    """ form with default values for location, able to save timestamp, quantity """

    return render_template('inventory.html')


@app.route("/mealplan")
def show_meal_plan():
    """ display meal plan for certain dates """

    return render_template('meal-plan.html', date=date)


@app.route("/recipe/display")
def display_recipe():
    """ display recipe printout via link"""
    
    return render_template('recipe-display.html')


@app.route('/authorize')
def authorize():
    '''Asks user for authorization to google calendar account'''

    #creates flow instance to manage OAuth grant access
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

    #uri configured in API Google console
    flow.redirect_uri = 'http://localhost:5000/oauth2callback'

    #finds authorization url
    authorization_url, state = flow.authorization_url(
                                access_type='offline', 
                                include_granted_scopes='true')
    print('\n{authorization_url}\n')
    session['state'] = state

    #redirect user through authorization url 
    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    '''Processes response for google calendar authorization'''

    #creates flow instance to manage OAuth grant access
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = 'http://localhost:5000/oauth2callback'

    # need to get full URL we are on including all the param1 = token&param2=key
    authorization_response = request.url
                            # = request.build_absolute_uri()

    #fetch tocken for the authorization response
    flow.fetch_token(authorization_response=authorization_response)

    #credentials stored
    credentials = flow.credentials

    session['credentials'] = credentials_to_dict(credentials)
    flash('Succesfully logged in to Google Calendar! Try adding again.')
    return redirect('/cal')


@app.route('/cal')
def cal():
    return "yay"

#TODO: get request to retrieve meal plan as json blob. user says looks good, add to gcal. This pg will post to make_calendar_event
@app.route('/add-to-calendar', methods=['GET'])
def make_calendar_event():
    '''Add all-day recipe event to user's google calendar with OAUTH'''
    
    #checks if credentials not already in session
    if 'credentials' not in session:
        return redirect('/authorize')
    #gets information about recipe to add to calendar
    # recipes = [<Recipe name = 3-Ingredient Bacon Stuffed Mushrooms ingredients = {"button mushrooms", "cooked bacon", "feta cheese"}>, 
    #     <Recipe name = Easy Pesto Stuffed Mushrooms ingredients = {"button mushrooms", parmesan, pesto }>]
    #grabs stored OAuth credentials
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])

    #client a google api client to make google calendar event
    drive = googleapiclient.discovery.build(
      'calendar', API_VERSION, credentials=credentials)

    event = create_google_calendar_event()

    #creates google calendar event with session stored moon phase info
    # session['event'] = create_google_calendar_event(recipe.name, recipe.url)
    #adds the calendar event to the google calendar
    event_to_add = drive.events().insert(calendarId='primary', sendNotifications=True, body=event).execute()
    flash('Event added to calendar!')

    return "success"


def credentials_to_dict(credentials):
  """Takes in credentials from OAuth and returns in dictionary format"""

  #Returns dictionary for OAuth process
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


def create_google_calendar_event():
  """Takes recipe object and uses name and url to turn into google calendar event"""
  name= "recipe_name"
  description="description"

  #dictionary for google event information
  event = {
                'summary': name,
                'start': {"date": "2020-11-13"},
                'end': {"date": "2020-11-13"},
                'description': description
            }
  return event


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
