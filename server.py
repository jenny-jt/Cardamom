from flask import Flask, request, render_template, redirect, session, flash, jsonify
import os

from model import db, connect_to_db, MealPlan, Recipe
from helper import make_cal_event, cred_dict, create_recipe_list, create_alt_recipes, data_mealplans, data_recipes, data_user, convert_dates, mealplan_dates, num_days, verify_user
from crud import all_recipes, create_db_recipes, add_user, user_by_id, user_by_email, mealplan_add_recipe, mealplan_add_altrecipe, updated_recipes

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


@app.route("/api/login", methods=['POST'])
def login_user():
    """log in user, return either jsonify(user name and id), or "no user with this email"
        if no user, creates user with entered email and password
    """
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = user_by_email(email)
    print("****user", user)

    user_verified = verify_user(password, user)
    print("******verified", user_verified)
    return jsonify(user_verified)


@app.route("/api/new_user", methods=['POST'])
def new_user():
    """ creates user with entered email and password"""

    data = request.get_json()
    email = data['email']
    password = data['password']

    user = add_user(name, email, password)
    user_info = data_user(user)

    return jsonify(user_info)


@app.route("/api/mealplans", methods=['POST'])
def user_mealplans():
    """show user's mealplans"""
    data = request.get_json()
    user_id = data['user_id']
    print(user_id)
    user = user_by_id(user_id)
    print(user)

    mealplans = user.mealplans
    mealplans_info = data_mealplans(mealplans)

    return jsonify(mealplans_info)


@app.route("/api/recipes")
def recipes():
    """show user's mealplans"""
    recipes = all_recipes()

    recipes_info = data_recipes(recipes)

    return jsonify(recipes_info)


@app.route("/api/mealplan/<int:mealplan_id>")
def modify_mp(mealplan_id):
    """retrieve mealplan obj for each id, render modification form"""

    mealplan_id = int(mealplan_id)
    mealplan = MealPlan.query.get(mealplan_id)

    recipes = mealplan.recipes_r
    recipes_info = data_recipes(recipes)

    altrecipes = mealplan.altrecipes_r
    altrecipes_info = data_recipes(altrecipes)

    mealplan_recipes = {'recipes': recipes_info, 'altrecipes': altrecipes_info}

    return jsonify(mealplan_recipes)


@app.route("/api/create", methods=['POST'])
def create():
    """create mealplan(s) for user using dates, ingredients, num_recipes entered
        return jsonified obj with mealplan ids of mealplans list
    """
    data = request.get_json()

    ingredients = data['ingredients']
    num_recipes = int(data['num_recipes_day'])
    start = data['start_date']
    end = data['end_date']

    start_date, end_date = convert_dates(start, end)
    days = num_days(start_date, end_date)
    num = num_recipes * days

    user_id = session['user_id']
    user = user_by_id(user_id)

    db_recipes = create_db_recipes(ingredients)
    master_list = create_recipe_list(ingredients, num, db_recipes)
    recipe_list = master_list[0]

    mealplans = mealplan_dates(start_date, end_date, user)
    mealplans_list = []

    for mealplan in mealplans:
        alt_recipes = create_alt_recipes(master_list, ingredients, mealplan)
        altrecipes = mealplan_add_altrecipe(mealplan, alt_recipes)
        recipes = mealplan_add_recipe(mealplan, recipe_list, num_recipes)

        recipes_info = data_recipes(recipes)
        alt_recipes_info = data_recipes(altrecipes)

        mp = {'id': mealplan.id, 'date': mealplan.date.strftime("%Y-%m-%d"),
              'recipes': recipes_info, 'altrecipes': alt_recipes_info}

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
    altrecipe_ids = data['recipe_ids']

    mealplan = MealPlan.query.get(mealplan_id)
    date = str(mealplan.date)[:10]

    # front end recipe list used to make cal events
    cal_recipes = updated_recipes(recipe_ids)
    mealplan.recipes_r = cal_recipes
    db.session.commit()
    print(f"\n updated mealplan recipes {mealplan.recipes_r}\n")

    alt_recipes = updated_recipes(altrecipe_ids)
    mealplan.altrecipes_r = alt_recipes  # can i do this or do i have to .clear() and then add recipes?
    db.session.commit()
    print(f"\n updated alternate recipes {mealplan.altrecipes_r}\n")

    for recipe in cal_recipes:
        event = make_cal_event(recipe, date)
        cal.events().insert(calendarId=cal_id, sendNotifications=True, body=event).execute()

    return jsonify('Recipes added to MealPlan calendar!')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
