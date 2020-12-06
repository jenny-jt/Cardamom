from flask import Flask, request, render_template, redirect, session, flash, jsonify
import os

from model import db, connect_to_db, MealPlan
from helper import make_cal_event, cred_dict, convert_date, create_recipe_list, create_alt_recipes, data_mealplans, data_recipes, data_user, convert_dates, mealplan_dates, num_days, verify_user
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


@app.route("/api/login", methods=['POST'])
def login_user():
    """log in user, return either jsonify(user name and id), or no user with this email"""
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = user_by_email(email)
    if user:
        user_verified = verify_user(password, user)
        return jsonify(user_verified)
    else:
        return jsonify("no user with this email")


@app.route("/api/new_user", methods=['POST'])
def new_user():
    """ creates user with entered email and password"""

    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    user = user_by_email(email)

    if user:
        return jsonify('user with this email already exists')
    else:
        user = add_user(name, email, password)
        user_info = data_user(user)
        return jsonify(user_info)


@app.route("/api/mealplans", methods=['POST'])
def user_mealplans():
    """show user's mealplans"""
    data = request.get_json()

    user_id = data['user_id']
    print("****mealplans user id", user_id)
    user = user_by_id(user_id)

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

    date = mealplan.date
    mealplan_date = convert_date(date)
    print("****mealplan date", mealplan_date)

    recipes = mealplan.recipes_r
    recipes_info = data_recipes(recipes)

    altrecipes = mealplan.altrecipes_r
    altrecipes_info = data_recipes(altrecipes)

    mealplan_recipes = {'recipes': recipes_info, 'altrecipes': altrecipes_info, 'date': mealplan_date}

    return jsonify(mealplan_recipes)


@app.route("/api/create", methods=['POST'])
def create():
    """create mealplan(s) for user using dates, ingredients, num_recipes entered
        return jsonified obj with mealplan ids of mealplans list
    """
    data = request.get_json()
    print("****data", data)

    user_id = data['user_id']
    ingredients = data['ingredients']  # string: carrot, egg
    num_recipes = int(data['num_recipes_day'])
    start = data['start_date'][:10]
    end = data['end_date'][:10]

    start_date, end_date = convert_dates(start, end)
    days = num_days(start_date, end_date)
    num = num_recipes * days
    print("**********num", num)

    user = user_by_id(user_id)

    db_recipes = create_db_recipes(ingredients)
    master_list = create_recipe_list(ingredients, num, db_recipes)
    recipe_list = master_list[0]
    print("********recipe list has recipes", len(recipe_list))

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
    print("*******data", data)

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
    mealplan.altrecipes_r = alt_recipes
    db.session.commit()
    print(f"\n updated alternate recipes {mealplan.altrecipes_r}\n")

    for recipe in cal_recipes:
        event = make_cal_event(recipe, date)
        cal.events().insert(calendarId=cal_id, sendNotifications=True, body=event).execute()

    return jsonify('Recipes added to MealPlan calendar!')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=False, host='0.0.0.0')
