from flask import Flask, request, render_template, redirect, session, flash
import os

from model import connect_to_db, MealPlan
from helper import *
import crud

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

app = Flask(__name__)
app.secret_key = os.environ['secret_key']

CLIENT_SECRETS_FILE = 'client_secret.json'
API_SERVICE_NAME = 'cal'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
# creates flow instance to manage OAuth grant access, uri configured in API Google console
flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
                                     scopes=SCOPES,
                                     redirect_uri='http://localhost:5000/callback')


@app.route("/")
def homepage():
    """Show homepage, ask to authorize"""

    return render_template('homepage.html')


@app.route('/authorize')
def authorize():
    """OAuth"""
    # unpack authorization url and state
    authorization_url, state = flow.authorization_url(
                                access_type='offline',
                                include_granted_scopes='true')

    session['state'] = state

    # redirect user
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    """Processes response for google calendar authorization"""
    # google making a request to flask server with code attached
    authorization_response = request.url

    # fetch tocken for the authorization response
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials

    # store credentials in dict format in session
    session['credentials'] = cred_dict(credentials)

    flash('Succesfully logged in to Google Calendar!')
    return render_template('search-form.html')


@app.route("/search")
def search_results():
    """take in date for mealplan, ingredients, and number of recipes
       outputs list of recipes that are associated with mealplan obj
    """
    ingredients = request.args.get("ingredients").split(",")

    num = int(request.args.get("num_recipes"))
    session['num'] = num

    date = request.args.get("date")
    session['date'] = date

    # make sure there is a mealplan obj
    mealplan = check_mealplan(date)

    db_recipes = crud.db_recipe_r(ingredients)

    if len(db_recipes) < num:
        api_ids = crud.api_id_search(ingredients, num)
        api_recipes = crud.api_recipes_list(api_ids)
        recipe_list = make_recipe_list(num, db_recipes, api_recipes)
    else:
        recipe_list = make_recipe_list(num, db_recipes)

    # list of recipes associated with mealplan obj
    recipes = crud.mealplan_add_recipe(mealplan, recipe_list)

    return render_template('recipes.html', mealplan=mealplan, recipes=recipes)

# TODO: figure out how to query mealplan obj using date stored in session

    # print(f"this is the date that should be saved from session:{date}\n")
    # dummy data
        # recipes = Recipe.query.filter(Recipe.ingredients.contains("carrot")).distinct()
@app.route('/add-to-cal', methods=['POST'])
def make_calendar_event():
    """Add all-day recipe event to user's google calendar with OAUTH"""

    if 'credentials' not in session:
        return redirect('/authorize')

    # grabs stored OAuth credentials
    credentials = Credentials(**session['credentials'])

    # google api client to make google calendar event
    cal = build('calendar', API_VERSION, credentials=credentials)

    cal_id = 'tl9a33nl5al9k337lh45f40av8@group.calendar.google.com'

    # from template hidden form input
    mealplan_id = request.form.get("mealplan_id")

    # get mealplan obj using id
    mealplan = MealPlan.query.get(mealplan_id)
    print(f"this is the mealplan object {mealplan}")
    recipes = mealplan.recipes_r
    print(f"this is the list of recipe objects from mealplan: {recipes}")
    # creates google calendar event for each recipe in mealplan 
    date = session["date"]
    print(f"\nrecipe list to make events: {recipes}\n")
    for recipe in recipes:
        event = make_cal_event(recipe, date)
        # adds the calendar event to the google calendar
        add_event = cal.events().insert(calendarId=cal_id, sendNotifications=True, body=event).execute()

    flash('Recipes added to MealPlan calendar!')
    # maybe another button/option to add more meal plan?
    return render_template('meal-plan.html')


def make_cal_event(recipe, date):
    """Takes in recipe object, turns it into gcal event body with:
    date of event: mealplan date (or random choice of mealplan dates)
    name of event: recipe name 
    description of event: cook time
    source: recipe url
    """
    # date = "2020-11-13"
    # name = recipe.name
    # url = recipe.url
    # description = "recipe cook time"
    # date = mealplan.date
    print(f"this is the recipe name used to make the cal event: {recipe.name}")
    # dictionary for google event information

    # "2020-11-13T15:00:37Z-07:00"
    # date.isoformat()
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
