from flask import Flask, request, render_template, redirect, session, flash
import os

from model import db, connect_to_db, MealPlan, Recipe
from helper import check_mealplan, make_cal_event, cred_dict, create_recipe_list, pick_recipes, create_alt_recipes, convert_dates, mealplan_dates, num_days
from crud import all_recipes, create_db_recipes, mealplan_add_recipe, create_api_recipes

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


@app.route("/", methods=['GET', 'POST'])
def homepage():
    """Show options to view all recipes, all mealplans, or create new mealplan"""

    return render_template('homepage.html')


@app.route("/recipes")
def show_recipes():
    """Show all recipes"""
    recipes = all_recipes()

    return render_template('recipes.html', recipes=recipes)


# @app.route("/mealplans")
# def show_mealplans(user):
#     """Show all mealplans"""
#     mealplans = user.mealplans_r

#     return render_template('mealplans.html', mealplans=mealplans)


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

    authorization_url, state = flow.authorization_url(
                                access_type='offline',
                                include_granted_scopes='true')

    session['state'] = state

    return redirect(authorization_url)


@app.route('/callback')
def callback():
    """Processes response for google calendar authorization"""
    # google making a request to flask server with code attached
    authorization_response = request.url

    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials

    session['credentials'] = cred_dict(credentials)

    flash('Succesfully logged in to Google Calendar!')
    return render_template('search.html')


@app.route("/search")
def search_results():
    """take in date for mealplan, ingredients, and number of recipes
       outputs list of recipes that are associated with mealplan obj
    """
    ingredients = request.args.get("ingredients").split(",")
    num = int(request.args.get("recipes_per_day"))

    start = request.args.get("start_date")
    end = request.args.get("end_date")
    start_date, end_date = convert_dates(start, end)
    days = num_days(start_date, end_date)

    num_recipes = num * days
    mealplans = mealplan_dates(start_date, end_date)
    db_recipes = create_db_recipes(ingredients)
    lists = create_recipe_list(ingredients, num_recipes, db_recipes)
    recipe_list = lists[0]
    alternate_recipes = {}

    # all mealplans will be created from same recipe_list, to avoid duplicate recipes in mealplan cluster
    for mealplan in mealplans:
        mealplan_add_recipe(mealplan, recipe_list)
        print("recipes added to mealplan")
        # mealplan_id = mealplan.id
        alt_recipe = create_alt_recipes(lists, ingredients, num, mealplan)
        alternate_recipes[mealplan.id] = alt_recipe

        print(f"\nthis is the dictionary of id/alt_recipes list: {alternate_recipes}\n")

    return render_template('modify.html',
                           mealplans=mealplans,
                           alternate_recipes=alternate_recipes)


@app.route('/modify', methods=['POST'])
def modify_recipes():
    """remove select recipes and replace with additional db/api recipes"""

    id_remove_recipes = request.form.getlist('remove')
    id_add_recipes = request.form.getlist('add')
    mealplans = request.form.getlist("mealplans")
    session['mealplans'] = mealplans  # need not obj

    remove = []
    for recipe_id in id_remove_recipes:
        recipe = Recipe.query.get(recipe_id)
        remove.append(recipe)

    add = []
    for recipe_id in id_add_recipes:
        recipe = Recipe.query.get(recipe_id)
        add.append(recipe)

    for mealplan in mealplans:
        recipes = mealplan.recipes_r
        print(f"this is the recipes list after removal: {recipes}")

    for recipe in remove:
        recipes.remove(recipe)

    for recipe in add:
        if recipe not in recipes:
            recipes.append(recipe)
        else:
            flash('recipe already in mealplan')

    db.session.commit()

    flash('Recipes removed and added')
    return render_template('events.html', recipes=recipes, mealplan=mealplan)


@app.route('/cal', methods=['POST'])
def make_calendar_event():
    """Add all-day recipe event to user's google calendar with OAUTH"""

    # grabs stored OAuth credentials
    credentials = Credentials(**session['credentials'])

    # google api client to make google calendar event
    cal = build('calendar', API_VERSION, credentials=credentials)
    cal_id = 'tl9a33nl5al9k337lh45f40av8@group.calendar.google.com'
    # print(session)
    # date = session["date"] should just query dates to get mealplan
    # print(session)

    # mealplans = session['mealplans'] #need not obj
    for mealplan in mealplans:
        recipes = mealplan.recipes_r

        for recipe in recipes:
            event = make_cal_event(recipe, date)
            add_event = cal.events().insert(calendarId=cal_id, sendNotifications=True, body=event).execute()

    flash('Recipes added to MealPlan calendar!')

    return render_template('homepage.html')

@app.route("/mealplan/<int:mealplan_id>")
def modify_mealplan(mealplan_id):
    mealplan_id = int(mealplan_id)
    mealplan = MealPlan.query.get(mealplan_id)
    print(mealplan)
    return "hi"
# @app.route("/inventory")
# def update_inventory():
#     """ form with default values for location, able to save timestamp, quantity """

#     return render_template('inventory.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
