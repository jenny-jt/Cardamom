from flask import Flask, request, render_template, redirect, session, flash
import os

from model import connect_to_db, MealPlan
from helper import check_mealplan, make_cal_event, cred_dict, create_recipe_list
from crud import all_recipes, all_mealplans, db_recipe_r, mealplan_add_recipe

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
    """Show options to view all recipes, all mealplans, or create new mealplan"""

    return render_template('homepage.html')


@app.route("/recipes")
def show_recipes():
    """Show all recipes"""
    recipes = all_recipes()

    return render_template('recipes.html', recipes=recipes)


@app.route("/mealplans")
def show_mealplans():
    """Show all mealplans"""
    mealplans = all_mealplans()

    return render_template('mealplans.html', mealplans=mealplans)


@app.route("/create")
def create_mealplan():
    """check if authorized
    if yes: display form to gather info to create mealplan
    if no: redirect to authorize
    """

    if 'credentials' not in session:
        return redirect('/authorize')

    return render_template('search.html')


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
    return render_template('search.html')


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

    db_recipes = db_recipe_r(ingredients)
    # session['db_recipes'] = db_recipes

    recipe_list = create_recipe_list(ingredients, num, db_recipes)

    recipes = mealplan_add_recipe(mealplan, recipe_list)

    return render_template('cal.html', recipes=recipes, mealplan=mealplan)


# TODO: figure out how to query mealplan obj using date stored in session
    # get mealplan obj using date
    # mealplan = MealPlan.query.get(date)
    # dummy data
    # recipes = Recipe.query.filter(Recipe.ingredients.contains("carrot")).distinct()
@app.route('/cal', methods=['POST'])
def make_calendar_event():
    """Add all-day recipe event to user's google calendar with OAUTH"""

    # grabs stored OAuth credentials
    credentials = Credentials(**session['credentials'])

    # google api client to make google calendar event
    cal = build('calendar', API_VERSION, credentials=credentials)

    cal_id = 'tl9a33nl5al9k337lh45f40av8@group.calendar.google.com'

    date = session["date"]

    # from template hidden form input
    mealplan_id = request.form.get("mealplan_id")

    # get mealplan obj using id
    mealplan = MealPlan.query.get(mealplan_id)
    print(f"this is the mealplan object {mealplan}")

    recipes = mealplan.recipes_r
    print(f"this is the list of recipe objects from mealplan: {recipes}")
    # creates google calendar event for each recipe in mealplan 

    print(f"\nrecipe list to make events: {recipes}\n")
    # no duplicates here
    for recipe in recipes:
        event = make_cal_event(recipe, date)
        # adds the calendar event to the google calendar
        add_event = cal.events().insert(calendarId=cal_id, sendNotifications=True, body=event).execute()

    flash('Recipes added to MealPlan calendar!')

    return render_template('homepage.html')


@app.route('/modify', methods=['POST'])
def modify_recipes():
    """remove select recipes and replace with additional db/api recipes"""
    # db_recipes = session['db_recipes']
    # api_recipes = session['api_recipes']

    # display all recipes associated with MealPlan

    # recipe = selected recipe to remove

    # remove(recipe)

    # select recipe to add to mealplan

    # add recipe

    # display all recipes again and ask for approval


# @app.route("/inventory")
# def update_inventory():
#     """ form with default values for location, able to save timestamp, quantity """

#     return render_template('inventory.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
