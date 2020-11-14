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
from googleapiclient.discovery import build
from urllib.parse import parse_qs
from oauth2client import file, client, GOOGLE_TOKEN_URI


app = Flask(__name__)
app.secret_key = os.environ['secret_key']

CLIENT_SECRETS_FILE = 'client_secret.json'
API_SERVICE_NAME = 'cal'
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
    
    #make sure there is a mealplan obj
    check_mealplan(date)

    # this is the way without using secondary table
    # db_recipes = crud.db_recipe_search(ingredients) 
    db_recipes = crud.db_recipe_r(ingredients)
    
    if len(db_recipes) < number:
        api_recipe_ids = crud.api_id_search(ingredients, number)
        api_recipes = crud.api_recipes_list(api_recipe_ids)
    print(f"this is api recipe list: {api_recipes}")    

    return render_template('recipe-display.html', recipes=recipe_list)


def check_mealplan(date):
    """checks if mealplan exists, otherwise makes a new mealplan object"""
    mealplan = MealPlan.query.filter(MealPlan.date == date).first()

    if not mealplan:
        mealplan = crud.add_mealplan(date)
        
    return mealplan


def make_recipe_list(number, db_recipes, api_recipes):
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


@app.route("/mealplan")
def show_meal_plan(date):
    """ display meal plan for certain dates """

    return render_template('meal-plan.html', date=date)


@app.route('/authorize')
def authorize():
    '''Asks user for authorization to google calendar account'''

    # creates flow instance to manage OAuth grant access
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

    # uri configured in API Google console
    flow.redirect_uri = 'http://localhost:5000/oauth2callback'

    # finds authorization url
    authorization_url, state = flow.authorization_url(
                                access_type='offline', 
                                include_granted_scopes='true')
    print('\n{authorization_url}\n')
    session['state'] = state

    # redirect user through authorization url 
    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    '''Processes response for google calendar authorization'''

    # creates flow instance to manage OAuth grant access
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = 'http://localhost:5000/oauth2callback'

    # need to get full URL we are on including all the param1 = token&param2=key
    authorization_response = request.url
                            # = request.build_absolute_uri()

    # fetch tocken for the authorization response
    flow.fetch_token(authorization_response=authorization_response)

    # credentials stored
    credentials = flow.credentials

    session['credentials'] = credentials_to_dict(credentials)

    flash('Succesfully logged in to Google Calendar!')
    return render_template('meal-plan.html')


#TODO: get request to retrieve meal plan as json blob. user says looks good, add to gcal. This pg will post to make_calendar_event
@app.route('/add-to-calendar', methods=['GET'])
def make_calendar_event():
    '''Add all-day recipe event to user's google calendar with OAUTH'''
    
    # checks if credentials not already in session
    if 'credentials' not in session:
        return redirect('/authorize')
    # gets information about recipe to add to calendar
    # recipes = [<Recipe name = 3-Ingredient Bacon Stuffed Mushrooms ingredients = {"button mushrooms", "cooked bacon", "feta cheese"}>, 
    #     <Recipe name = Easy Pesto Stuffed Mushrooms ingredients = {"button mushrooms", parmesan, pesto }>]
    # grabs stored OAuth credentials
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])

    # client a google api client to make google calendar event
    cal = build('calendar', API_VERSION, credentials=credentials)

    event = create_google_calendar_event()

    # creates google calendar event
    session['event'] = create_cal_event(mealplan)

    # adds the calendar event to the google calendar
    add_event = cal.events().insert(calendarId='tl9a33nl5al9k337lh45f40av8@group.calendar.google.com', sendNotifications=True, body=event).execute()

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
    """Takes in mealplan object, turns all the associated recipe objects into gcal events
    date of event: mealplan date (or random choice of mealplan dates)
    name of event: recipe name 
    description of event: cook time
    source: recipe url
    """
#   for recipe in mealplan.recipes_r:
#       name = recipe.name
#       url = recipe.url
#       description = "recipe cook time"
    name = "name"
    description = ""
    # url = ""

    # dictionary for google event information
    event = {
                'summary': name,
                'start': {"date": "2020-11-13"},
                'end': {"date": "2020-11-13"},
                'description': description,
                # 'source': {"url": url}
            }
    return event


@app.route("/recipe/display")
def display_recipe():
    """ display recipe printout via link"""
    
    return render_template('recipe-display.html')


@app.route("/inventory")
def update_inventory():
    """ form with default values for location, able to save timestamp, quantity """

    return render_template('inventory.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
