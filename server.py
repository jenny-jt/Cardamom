from flask import Flask, request, render_template, redirect, session, flash
import os

from model import db, connect_to_db, MealPlan, Recipe
from helper import check_mealplan, make_cal_event, cred_dict, create_recipe_list, pick_recipes, create_alt_recipes, convert_dates, mealplan_dates, num_days
from crud import all_recipes, all_mealplans, create_db_recipes, add_user, user_by_id, user_by_email, mealplan_add_recipe, mealplan_add_altrecipe, create_api_recipes

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
def show_login():
    """show log in form"""

    if 'user_id' in session:
        user_id = session['user_id']
    else:
        session['user_id'] = '' 

    if session['user_id']:
        flash(f'User {user_id} logged in!')
        return redirect('/menu')

    return render_template('login.html')


@app.route("/login", methods=['POST'])
def login():
    """ask user to login, if new user, create user and add to db"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = user_by_email(email)

    if user:
        if user.password == password:
            print(session)
            session['user_id'] = user.id
            print(session)
            print(user)
            print(f"this is the user id after setting session{session['user_id']}")
            return redirect('/menu')
        else:
            session['user_id'] = ''
            flash('Wrong password! Please try again')
            return redirect('/')
    else:
        flash('Email not in system. Would you like to create a new user?')
        return redirect('/')


@app.route("/create_user", methods=['POST'])
def create_user():
    """creates user with entered email and pw"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = add_user(email, password)
    session['user_id'] = user.id

    flash('Account created!')
    return redirect('/menu')


@app.route("/menu")
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
    """Show all mealplans for user"""
    # mealplans = all_mealplans()

    # user_id = 1
    user_id = session['user_id']
    user = user_by_id(user_id)
    mealplans = user.mealplans
    print(f"these are users mealplans: {mealplans}")

    if mealplans:
        return render_template('mealplans.html', mealplans=mealplans)
    else:
        flash('No Meal Plans for you yet. Please create one!')
        return redirect("/create_mealplan")


@app.route("/create_mealplan")
def create_mealplan():
    """check if authorized for gcal
    if yes: display form to gather info to create mealplan
    if no: redirect to authorize
    """
    print(session)

    if 'credentials' not in session:
        return redirect('/authorize')

    return render_template('search.html')


@app.route('/authorize')
def authorize():
    """OAuth"""

    authorization_url, state = flow.authorization_url(
                                access_type='offline',
                                include_granted_scopes='true')
    print(session)
    session['state'] = state
    print(session)

    return redirect(authorization_url)


@app.route('/callback')
def callback():
    """Processes response for google calendar authorization"""
    print(session)
    # google making a request to flask server with code attached
    authorization_response = request.url

    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    print(session)
    session['credentials'] = cred_dict(credentials)
    print(session)
    flash('Succesfully logged in to Google Calendar!')

    return render_template('search.html')


@app.route("/search")
def search_results():
    """take in date for mealplan, ingredients, and number of recipes
       outputs list of recipes that are associated with mealplan obj
    """
    ingredients = request.args.get("ingredients").split(",")
    num_recipes = int(request.args.get("recipes_per_day"))

    # user_id = 1
    print(f"\nthis is the session at beginning: {session}")
    user_id = session['user_id']
    print(f"\nthis is the user id from session: {session}\n")
    user = user_by_id(user_id)
    print(user)

    start = request.args.get("start_date")
    print(f"session before adding start: {session}")
    session['start'] = start
    print(f"session after adding start: {session}")
    end = request.args.get("end_date")
    session['end'] = end
    print(f"session before adding end: {session}")

    start_date, end_date = convert_dates(start, end)
    days = num_days(start_date, end_date)
    num = num_recipes * days

    mealplans = mealplan_dates(start_date, end_date, user)
    db_recipes = create_db_recipes(ingredients)
    master_list = create_recipe_list(ingredients, num_recipes, db_recipes)
    recipe_list = master_list[0]

    for mealplan in mealplans:
        alt_recipe = create_alt_recipes(master_list, ingredients, num, mealplan)
        mealplan_add_recipe(mealplan, recipe_list)
        altrecipes = mealplan_add_altrecipe(mealplan, alt_recipe)

        print(f"\n alternative recipes for mp {altrecipes}\n")

    return render_template("display.html", mealplans=mealplans)


@app.route("/mealplans/<int:mealplan_id>")
def modify_mealplan(mealplan_id):
    """retrieve mealplan obj for each id, render modification form"""

    mealplan_id = int(mealplan_id)
    mealplan = MealPlan.query.get(mealplan_id)

    return render_template('modify.html', mealplan=mealplan)


@app.route('/modify', methods=['POST'])
def modify_recipes():
    """remove select recipes and replace with additional db/api recipes"""

    mealplan_id = request.form.get("mealplan_id")
    mealplan = MealPlan.query.get(mealplan_id)

    recipes = mealplan.recipes_r
    id_remove_recipes = request.form.getlist('remove')
    id_add_recipes = request.form.getlist('add')

    remove = []
    for recipe_id in id_remove_recipes:
        recipe = Recipe.query.get(recipe_id)
        remove.append(recipe)

    add = []
    for recipe_id in id_add_recipes:
        recipe = Recipe.query.get(recipe_id)
        add.append(recipe)

    for recipe in remove:
        recipes.remove(recipe)
        db.session.commit()

    for recipe in add:
        if recipe not in recipes:
            recipes.append(recipe)
            db.session.commit()
        else:
            flash('recipe already in mealplan')

    print(f"this is the recipes list after removal: {recipes}")

    flash('Recipes removed and added')
    return render_template('events.html', recipes=recipes, mealplan=mealplan)


@app.route('/cal', methods=['POST'])
def make_calendar_event():
    """Add all-day recipe event to user's google calendar for each recipe in mealplan"""

    # grabs stored OAuth credentials
    credentials = Credentials(**session['credentials'])

    # google api client to make google calendar event
    cal = build('calendar', API_VERSION, credentials=credentials)
    cal_id = 'tl9a33nl5al9k337lh45f40av8@group.calendar.google.com'

    start = session['start']
    end = session['end']
    start_date, end_date = convert_dates(start, end)
    mealplans = mealplan_dates(start_date, end_date)

    for mealplan in mealplans:
        recipes = mealplan.recipes_r
        date = str(mealplan.date)

        for recipe in recipes:
            event = make_cal_event(recipe, date)
            add_event = cal.events().insert(calendarId=cal_id, sendNotifications=True, body=event).execute()

    flash('Recipes added to MealPlan calendar!')

    return render_template('homepage.html')



# @app.route("/inventory")
# def update_inventory():
#     """ form with default values for location, able to save timestamp, quantity """

#     return render_template('inventory.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
