from flask import Flask, request, render_template, redirect, session, flash, jsonify
import os

from model import db, connect_to_db, MealPlan, Recipe
from helper import make_cal_event, cred_dict, create_recipe_list, create_alt_recipes, convert_dates, mealplan_dates, num_days
from crud import all_recipes, create_db_recipes, add_user, user_by_id, user_by_email, mealplan_add_recipe, mealplan_add_altrecipe

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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def show_login(path):
    """show root template"""

    return render_template('root.html')


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
    # might need flow here
    authorization_response = request.url

    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = cred_dict(credentials)

    flash('Succesfully logged in to Google Calendar!')

    return render_template('root.html')


# @app.route("/login", methods=['POST'])
# def login():
#     """ask user to login, if new user, create user and add to db"""

#     email = request.form.get('email')
#     password = request.form.get('password')

#     user = user_by_email(email)

#     if user:
#         if user.password == password:
#             session['user_id'] = user.id
#             flash("Logged in successfully")
#             return redirect('/menu')
#         else:
#             flash('Wrong password! Please try again')
#             return redirect('/')
#     else:
#         flash('Email not in system. Would you like to create a new user?')
#         return redirect('/')


# @app.route("/create_user", methods=['POST'])
# def create_user():
#     """creates user with entered email and pw"""

#     email = request.form.get('email')
#     password = request.form.get('password')

#     user = add_user(email, password)
#     session['user_id'] = user.id

#     flash('Account created!')
#     return redirect('/menu')


# @app.route("/menu")
# def menu():
#     """Show options to view all recipes, all mealplans, or create new mealplan"""

#     return render_template('menu.html')


# @app.route("/recipes")
# def show_recipes():
#     """Show all recipes"""
#     recipes = all_recipes()

#     return render_template('recipes.html', recipes=recipes)


# @app.route("/mealplans")
# def show_mealplans():
#     """Show all mealplans for user"""
#     # mealplans = all_mealplans()

#     user_id = session['user_id']
#     user = user_by_id(user_id)
#     mealplans = user.mealplans
#     print(f"these are users mealplans: {mealplans}")

#     if mealplans:
#         return render_template('mealplans.html', mealplans=mealplans)
#     else:
#         flash('No Meal Plans for you yet. Please create one!')
#         return redirect("/create_mealplan")


# @app.route("/create_mealplan")
# def create_mealplan():
#     """check if authorized for gcal
#     if yes: display form to gather info to create mealplan
#     if no: redirect to authorize
#     """
#     print(f"session in create_mealplan route: {session}")

#     if 'credentials' not in session:
#         return redirect('/authorize')

#     return render_template('search.html')


# @app.route("/search")
# def search_results():
#     """take in date for mealplan, ingredients, and number of recipes
#        outputs list of recipes that are associated with mealplan obj
#     """
#     ingredients = request.args.get("ingredients").split(",")
#     num_recipes = int(request.args.get("recipes_per_day"))

#     user_id = session['user_id']
#     user = user_by_id(user_id)

#     start = request.args.get("start_date")
#     session['start'] = start
#     end = request.args.get("end_date")
#     session['end'] = end

#     start_date, end_date = convert_dates(start, end)
#     days = num_days(start_date, end_date)
#     num = num_recipes * days

#     mealplans = mealplan_dates(start_date, end_date, user)
#     db_recipes = create_db_recipes(ingredients)
#     master_list = create_recipe_list(ingredients, num_recipes, db_recipes)
#     recipe_list = master_list[0]

#     for mealplan in mealplans:
#         alt_recipe = create_alt_recipes(master_list, ingredients, num, mealplan)
#         mealplan_add_recipe(mealplan, recipe_list)
#         mealplan_add_altrecipe(mealplan, alt_recipe)

#     return render_template("display.html", mealplans=mealplans)


# @app.route("/mealplans/<int:mealplan_id>")
# def modify_mealplan(mealplan_id):
#     """retrieve mealplan obj for each id, render modification form"""

#     mealplan_id = int(mealplan_id)
#     mealplan = MealPlan.query.get(mealplan_id)

#     return render_template('modify.html', mealplan=mealplan)


# @app.route('/modify', methods=['POST'])
# def modify_recipes():
#     """remove select recipes and replace with additional db/api recipes"""

#     mealplan_id = request.form.get("mealplan_id")
#     mealplan = MealPlan.query.get(mealplan_id)

#     recipes = mealplan.recipes_r
#     id_remove_recipes = request.form.getlist('remove')
#     id_add_recipes = request.form.getlist('add')

#     remove = []
#     for recipe_id in id_remove_recipes:
#         recipe = Recipe.query.get(recipe_id)
#         remove.append(recipe)

#     add = []
#     for recipe_id in id_add_recipes:
#         recipe = Recipe.query.get(recipe_id)
#         add.append(recipe)

#     for recipe in remove:
#         recipes.remove(recipe)
#         db.session.commit()

#     for recipe in add:
#         if recipe not in recipes:
#             recipes.append(recipe)
#             db.session.commit()
#         else:
#             flash('recipe already in mealplan')

#     flash('Recipes removed and added')
#     return render_template('events.html', recipes=recipes, mealplan=mealplan)


# @app.route('/cal', methods=['POST'])
# def make_calendar_event():
#     """Add all-day recipe event to user's google calendar for each recipe in mealplan"""

#     # grabs stored OAuth credentials
#     credentials = Credentials(**session['credentials'])

#     # google api client to make google calendar event
#     cal = build('calendar', API_VERSION, credentials=credentials)
#     cal_id = 'tl9a33nl5al9k337lh45f40av8@group.calendar.google.com'

#     start = session['start']
#     end = session['end']
#     start_date, end_date = convert_dates(start, end)
#     mealplans = mealplan_dates(start_date, end_date)

#     for mealplan in mealplans:
#         recipes = mealplan.recipes_r
#         date = str(mealplan.date)[:10]

#         for recipe in recipes:
#             event = make_cal_event(recipe, date)
#             add_event = cal.events().insert(calendarId=cal_id, sendNotifications=True, body=event).execute()

#     flash('Recipes added to MealPlan calendar!')

#     return render_template('homepage.html')


@app.route("/api/login", methods=['POST'])
def login_user():
    """log in user"""

    if 'credentials' not in session:
        return redirect('/api/authorize')

    data = request.get_json()

    email = data['email']
    password = data['password']

    user = user_by_email(email)

    if user:
        if user.password == password:
            session['user_id'] = user.id
            return jsonify("User logged in successfully")
        else:
            return jsonify("wrong password")

    return jsonify("no user with this email")


@app.route("/api/mealplans")
def user_mealplans():
    """show user's mealplans"""
    user_id = session['user_id']
    user = user_by_id(user_id)

    mealplans = user.mealplans
    mealplans_info = []

    for mealplan in mealplans:
        mp = {}
        mp['id'] = mealplan.id
        mp['date'] = mealplan.date.strftime("%Y-%m-%d")
        mealplans_info.append(mp)

    return jsonify(mealplans_info)


@app.route("/api/recipes")
def recipes():
    """show user's mealplans"""
    recipes = all_recipes()

    recipes_info = []
    for recipe in recipes:
        r = {}
        r['id'] = recipe.id
        r['name'] = recipe.name
        r['image'] = recipe.image
        r['cook_time'] = recipe.cook_time
        r['url'] = recipe.url
        recipes_info.append(r)

    return jsonify(recipes_info)


@app.route("/api/mealplan/<int:mealplan_id>")
def modify_mp(mealplan_id):
    """retrieve mealplan obj for each id, render modification form"""

    mealplan_id = int(mealplan_id)
    mealplan = MealPlan.query.get(mealplan_id)

    recipes = mealplan.recipes_r
    recipes_info = []

    for recipe in recipes:
        r = {}
        r['id'] = recipe.id
        r['name'] = recipe.name
        r['image'] = recipe.image
        r['cook_time'] = recipe.cook_time
        r['url'] = recipe.url
        recipes_info.append(r)

    alt_recipes = mealplan.altrecipes_r
    alt_recipes_info = []

    for recipe in alt_recipes:
        alt_r = {}
        alt_r['id'] = recipe.id
        alt_r['name'] = recipe.name
        alt_r['image'] = recipe.image
        alt_r['cook_time'] = recipe.cook_time
        alt_r['url'] = recipe.url
        alt_recipes_info.append(alt_r)

    mealplan_recipes = {'recipes': recipes_info, 'alts': alt_recipes_info}

    return jsonify(mealplan_recipes)


@app.route("/api/create", methods=['POST'])
def create():
    """create mealplan(s) for user using dates, ingredients, num_recipes entered
        return jsonified obj with mealplan ids of mealplans list
    """
    data = request.get_json()

    ingredients = data['ingredients']
    print(ingredients)
    num_recipes = int(data['num_recipes_day'])
    (num_recipes)
    start = data['start_date']
    print(start)
    end = data['end_date']
    print(end)

    start_date, end_date = convert_dates(start, end)
    days = num_days(start_date, end_date)
    num = num_recipes * days

    user_id = session['user_id']
    user = user_by_id(user_id)

    db_recipes = create_db_recipes(ingredients)
    master_list = create_recipe_list(ingredients, num_recipes, db_recipes)
    recipe_list = master_list[0]

    mealplans = mealplan_dates(start_date, end_date, user)
    mealplans_list = []

    for mealplan in mealplans:
        alt_recipe = create_alt_recipes(master_list, ingredients, num, mealplan)
        recipes = mealplan_add_recipe(mealplan, recipe_list, num_recipes)  
        # need to convert list of recipe obj to list of recipe name, img, url, cooktime
        recipes_info = []
        for recipe in recipes:
            r = {}
            r['id'] = recipe.id
            r['name'] = recipe.name
            r['image'] = recipe.image
            r['cook_time'] = recipe.cook_time
            r['url'] = recipe.url
            recipes_info.append(r)

        # need to convert list of recipe obj to list of recipe name, img, url, cooktime
        alt_recipes_info = []
        for recipe in alt_recipe:
            alt_r = {}
            alt_r['id'] = recipe.id
            alt_r['name'] = recipe.name
            alt_r['image'] = recipe.image
            alt_r['cook_time'] = recipe.cook_time
            alt_r['url'] = recipe.url
            alt_recipes_info.append(alt_r)

        mp = {'id': mealplan.id, 'date': mealplan.date.strftime("%Y-%m-%d"), 'recipes': recipes_info, 'alt_recipes': alt_recipes_info}
        mealplans_list.append(mp)


    return jsonify(mealplans_list)


@app.route('/api/cal', methods=['POST'])
def calendar_event():
    """Add all-day recipe event to user's google calendar for each recipe in mealplan"""

    # grabs stored OAuth credentials
    credentials = Credentials(**session['credentials'])

    # google api client to make google calendar event
    cal = build('calendar', API_VERSION, credentials=credentials)
    cal_id = 'tl9a33nl5al9k337lh45f40av8@group.calendar.google.com'

    data = request.get_json()

    mealplan_id = data['mealplan_id']
    recipe_ids = data['recipe_ids']
    
    mealplan = MealPlan.query.get(mealplan_id)
    date = str(mealplan.date)[:10]

    cal_recipes = []

    for id in recipe_ids:
        cal_recipe = Recipe.query.get(id)
        cal_recipes.append(cal_recipe)
    print(f"\n this is cal_recipes {cal_recipes}\n")

    for recipe in cal_recipes:
        event = make_cal_event(recipe, date)
        print(event)
        add_event = cal.events().insert(calendarId=cal_id, sendNotifications=True, body=event).execute()

    return ('Recipes added to MealPlan calendar!')


# @app.route("/inventory")
# def update_inventory():
#     """ form with default values for location, able to save timestamp, quantity """

#     return render_template('inventory.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
