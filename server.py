from flask import Flask, request, render_template, redirect, session, flash
import os

from model import db, connect_to_db, MealPlan, Recipe
from helper import make_cal_event, cred_dict, create_recipe_list, create_alt_recipes, convert_dates, mealplan_dates, num_days
from crud import all_recipes, create_db_recipes, add_user, user_by_id, user_by_email, mealplan_add_recipe, mealplan_add_altrecipe, mealplan_by_id

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

app = Flask(__name__)
app.secret_key = os.environ['secret_key']

CLIENT_SECRETS_FILE = 'client_secret.json'
API_SERVICE_NAME = 'cal'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']

flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
                                     scopes=SCOPES,
                                     redirect_uri='http://localhost:5000/callback')



@app.route("/")
def show_login():
    """show log in form"""
    if 'credentials' not in session:
        return redirect('/authorize')

    if 'user_id' in session:
        user_id = session['user_id']
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
            session['user_id'] = user.id
            flash("Logged in successfully")
            return redirect('/menu')
        else:
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

    return render_template('menu.html')


@app.route("/recipes")
def show_recipes():
    """Show all recipes"""
    recipes = all_recipes()

    return render_template('recipes.html', recipes=recipes)


@app.route("/mealplans")
def show_mealplans():
    """Show all mealplans for user"""
    user_id = session['user_id']
    user = user_by_id(user_id)
    mealplans = user.mealplans

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
    authorization_response = request.url

    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = cred_dict(credentials)

    flash('Succesfully logged into Google Calendar!')

    return redirect("/")


@app.route("/search")
def search_results():
    """take in date for mealplan, ingredients, and number of recipes
       outputs list of recipes that are associated with mealplan obj
    """
    ingredients = request.args.get("ingredients").split(",")
    num_recipes = int(request.args.get("recipes_per_day"))

    user_id = session['user_id']
    user = user_by_id(user_id)

    start = request.args.get("start_date")
    session['start'] = start
    end = request.args.get("end_date")
    session['end'] = end

    start_date, end_date = convert_dates(start, end)
    days = num_days(start_date, end_date)
    num = num_recipes * days

    mealplans = mealplan_dates(start_date, end_date, user)
    db_recipes = create_db_recipes(ingredients)
    print("*****db recipes", db_recipes)
    master_list = create_recipe_list(ingredients, num, db_recipes)
    recipe_list = master_list[0]
    print("**** recipe_list", recipe_list)

    for mealplan in mealplans:
        alt_recipe = create_alt_recipes(master_list, ingredients, num, mealplan)
        recipes = mealplan_add_recipe(mealplan, recipe_list, num_recipes)
        altrecipes = mealplan_add_altrecipe(mealplan, alt_recipe)
        print("**** date", mealplan.date)
        print("**** id", mealplan.id)
        print("****recipes in mp", recipes)
        print("****alternative recipes in mp", altrecipes)

    print("********mealplans list", mealplans)

    return render_template("display.html", mealplans=mealplans)


@app.route("/mealplans/<int:mealplan_id>")
def modify_mealplan(mealplan_id):
    """retrieve mealplan obj for each id, render modification form"""

    mealplan_id = int(mealplan_id)
    mealplan = MealPlan.query.get(mealplan_id)
    alt_recipes = mealplan.altrecipes_r  # this line should not be needed, jinja should be able to parse mealplan.altrecipes_r

    return render_template('modify.html', mealplan=mealplan, alt_recipes=alt_recipes)


@app.route('/modify', methods=['POST'])
def modify_recipes():
    """remove select recipes and replace with additional db/api recipes"""

    mealplan_id = request.form.get("mealplan_id")
    mealplan = MealPlan.query.get(mealplan_id)

    recipes = mealplan.recipes_r
    altrecipes = mealplan.altrecipes_r
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
        altrecipes.append(recipe)
        db.session.commit()

    for recipe in add:
        if recipe not in recipes:
            recipes.append(recipe)
            altrecipes.remove(recipe)
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

    # user_id = session["user_id"]
    # user = user_by_id(user_id)

    date = request.form.get("mealplan date")[:10]
    print(date)
    mp_id = int(request.form.get("mealplan id"))
    print("mealplan id", mp_id)

    mealplan = mealplan_by_id(mp_id)
    print("mealplan for cal", mealplan)
    recipes = mealplan.recipes_r

    for recipe in recipes:
        event = make_cal_event(recipe, date)
        cal.events().insert(calendarId=cal_id, sendNotifications=True, body=event).execute()

    flash('Recipes added to MealPlan calendar!')

    return render_template('menu.html')


@app.route('/cal_all', methods=['POST'])
def all_to_cal():
    """Add all-day recipe event to user's google calendar for each recipe in mealplan"""

    # grabs stored OAuth credentials
    credentials = Credentials(**session['credentials'])

    # google api client to make google calendar event
    cal = build('calendar', API_VERSION, credentials=credentials)
    cal_id = 'tl9a33nl5al9k337lh45f40av8@group.calendar.google.com'

    user_id = session["user_id"]
    user = user_by_id(user_id)

    start = session['start']
    end = session['end']
    start_date, end_date = convert_dates(start, end)
    mealplans = mealplan_dates(start_date, end_date, user)

    for mealplan in mealplans:
        recipes = mealplan.recipes_r
        date = str(mealplan.date)[:10]  # might be able to take out string

        for recipe in recipes:
            event = make_cal_event(recipe, date)
            add_event = cal.events().insert(calendarId=cal_id, sendNotifications=True, body=event).execute()

    flash('Recipes added to MealPlan calendar!')

    return render_template('menu.html')

# @app.route("/inventory")
# def update_inventory():
#     """ form with default values for location, able to save timestamp, quantity """

#     return render_template('inventory.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
