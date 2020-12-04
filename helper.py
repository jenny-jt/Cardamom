"""All helper functions"""
from flask import session, jsonify
from model import MealPlan
from random import choice
from crud import add_mealplan, create_api_recipes
from datetime import datetime, timedelta


def create_alt_recipes(master_list, ingredients, mealplan):
    """creates list of alternate recipes"""

    if len(master_list) > 2:
        alt_recipes = master_list[1] + master_list[2]
        print("crud: alt recipes with api", alt_recipes)
    else:
        alt_recipes = master_list[1]
        print("crud: alt recipes without api", alt_recipes)

    if len(alt_recipes) < 3:
        new_api_recipes = create_api_recipes(ingredients, 2)
        for recipe in new_api_recipes:
            if recipe not in mealplan.recipes_r:
                alt_recipes.append(recipe)
        print("crud: alt recipes after new api", alt_recipes)

    return alt_recipes


def create_recipe_list(ingredients, num, db_recipes):
    """takes in num as well as list of recipes from db
       will make api recipe list if needed
       returns recipe list that is num long (picked randomly from db only or db + api)
       also returns leftover db_recipes (lists[1]) and api_recipes (lists[2]) lists
    """
    db_num = len(db_recipes)
    api_num = num - db_num + 7

    if db_num < num:
        api_recipes = create_api_recipes(ingredients, api_num)
        print("*********getting api recipes", api_num)
        master_list = make_recipe_lists(num, db_recipes, api_recipes)
    else:
        master_list = make_recipe_lists(num, db_recipes)

    return master_list  # recipe_list, db_recipes, api_recipes


def check_mealplan(date, user):
    """checks if mealplan exists, otherwise makes a new mealplan object"""
    mealplan = MealPlan.query.filter(MealPlan.date == date).first()

    if not mealplan:
        mealplan = add_mealplan(date, user)

    return mealplan


def convert_dates(start, end):  
    """take in start and end date strings from form, returns date time objects"""

    dt_format = "%Y-%m-%d"

    start_date = datetime.strptime(start, dt_format)
    end_date = datetime.strptime(end, dt_format)

    return start_date, end_date


def convert_date(date):
    """take in dto from mealplan date and converts to string"""

    dt_format = "%B %d, %Y"

    mealplan_date = datetime.strftime(date, dt_format)

    return mealplan_date


def cred_dict(credentials):
    """Takes in credentials from OAuth and returns in dictionary format"""

    # Returns dictionary for OAuth process
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def data_mealplans(mealplans):
    """takes in mealplan list and generates list of mealplan info to jsonify"""
    mealplans_info = []

    for mealplan in mealplans:
        mp = {}
        mp['id'] = mealplan.id
        mp['date'] = mealplan.date.strftime("%A | %b %d, %Y")

        mealplans_info.append(mp)

    return mealplans_info


def data_recipes(recipes):
    """Takes in recipe list and generates list of recipe info to jsonify"""
    recipes_info = []

    for recipe in recipes:
        r = {}
        r['id'] = recipe.id
        r['name'] = recipe.name
        r['image'] = recipe.image
        r['cook_time'] = recipe.cook_time
        r['url'] = recipe.url
        recipes_info.append(r)

    return recipes_info


def data_user(user):
    """takes in user obj, sets session with user id and return jsonified user info"""

    session['user_id'] = user.id
    user_info = {'name': user.name, 'id': user.id}

    return user_info


def make_cal_event(recipe, date):
    """Takes in recipe object, turns it into gcal event body with"""

    cook_time = str(recipe.cook_time)  # might be unnecessary, cooktime is probably a string

    # dictionary for google event information
    event = {
            'summary': recipe.name,
            'start': {"date": date},
            'end': {"date": date},
            'description': f"{cook_time} minutes",
            'source': {"url": recipe.url}
            }

    return event


def make_recipe_lists(num, db_recipes, api_recipes=[]):
    """takes in db and api recipe lists, selects number of them to generate recipe list
       returns recipe list of num +2 extra and leftovers of the db and api lists
    """

    count = 0
    recipe_list = []

    while count < (num+2):
        if db_recipes:
            item = pick_recipes(db_recipes)
            db_recipes.remove(item)
        else:
            item = pick_recipes(api_recipes)
            api_recipes.remove(item)

        recipe_list.append(item)
        count += 1

    return recipe_list, db_recipes, api_recipes


def mealplan_dates(start_date, end_date, user):
    """take in start and end dates from form,
       check if mealplan exists for each date in range
       if not exist, then create new mealplan for each date attached to user
       returns list of mealplans for date range
    """
    mealplans = []
    delta = timedelta(days=1)

    while start_date <= end_date:
        start_date_string = start_date.strftime("%Y-%m-%d")
        mealplan = check_mealplan(start_date_string, user)
        mealplans.append(mealplan)
        start_date += delta

    return mealplans


def num_days(start_date, end_date):
    """take in start and end dates, returns number of days in date range"""

    date_range = end_date - start_date
    print("****date range", date_range)
    x = date_range.days
    print("date range days", x)
    num_days = date_range.days + 1
    print("*****num_days", num_days)

    return num_days


def pick_recipes(recipes):
    """takes in list of recipes, picks a random recipe from list"""
    item = choice(recipes)

    return item


def verify_user(password, user):
    """take in user email and password, and checks if user in db
    returns user id and name if yes, string "no user" if no
    """

    if user.password == password:
        user_info = data_user(user)
        return user_info
    else:
        return ("no user with this email")