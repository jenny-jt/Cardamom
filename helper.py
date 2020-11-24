"""All helper functions"""
from model import MealPlan
from random import choice
from crud import create_api_recipes, check_mealplan
from datetime import datetime, timedelta


def cred_dict(credentials):
    """Takes in credentials from OAuth and returns in dictionary format"""

    # Returns dictionary for OAuth process
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def create_recipe_list(ingredients, num, db_recipes):
    """takes in num as well as list of recipes from db
       will make api recipe list if needed
       returns recipe list that is num long (picked randomly from db only or db + api)
       also returns leftover db_recipes (lists[1]) and api_recipes (lists[2]) lists
    """
    db_num = len(db_recipes)
    api_num = num - db_num + 3

    if len(db_recipes) < num:
        api_recipes = create_api_recipes(ingredients, api_num)
        master_list = make_recipe_lists(num, db_recipes, api_recipes)
    else:
        master_list = make_recipe_lists(num, db_recipes)

    return master_list  # recipe_list, db_recipes, api_recipes


def make_recipe_lists(num, db_recipes, api_recipes=[]):
    """takes in db and api recipe lists, selects number of them to generate recipe list
       also contains the leftovers of the db and api lists
    """

    count = 0
    recipe_list = []

    while count < num:
        if db_recipes:
            item = pick_recipes(db_recipes)
            db_recipes.remove(item)
        else:
            item = pick_recipes(api_recipes)
            api_recipes.remove(item)

        recipe_list.append(item)
        count += 1

    return recipe_list, db_recipes, api_recipes


def pick_recipes(recipes):
    """takes in list of recipes, picks a random recipe from list"""
    item = choice(recipes)

    return item


def make_cal_event(recipe, date):
    """Takes in recipe object, turns it into gcal event body with"""
    cook_time = str(recipe.cook_time)

    # dictionary for google event information
    event = {
            'summary': recipe.name,
            'start': {"date": date},
            'end': {"date": date},
            'description': f"{cook_time} minutes",
            'source': {"url": recipe.url}
            }

    return event


def create_alt_recipes(master_list, ingredients, num_recipes, mealplan):
    """creates list of alternate recipes"""

    if len(master_list) > 2:
        alt_recipes = master_list[1] + master_list[2]
    else:
        alt_recipes = master_list[1]

    if len(alt_recipes) < 2:
        new_api_recipes = create_api_recipes(ingredients, 3)
        for recipe in new_api_recipes:
            if recipe not in mealplan.recipes_r:
                alt_recipes.append(recipe)

    return alt_recipes


def convert_dates(start, end):  
    """take in start and end date strings from form, returns date time objects"""

    dt_format = "%Y-%m-%d"

    start_date = datetime.strptime(start, dt_format)
    end_date = datetime.strptime(end, dt_format)

    return start_date, end_date


def num_days(start_date, end_date):
    """take in start and end dates, returns number of days in date range"""

    date_range = end_date - start_date

    num_days = date_range.days

    return num_days


def mealplan_dates(start_date, end_date, user):
    """take in start and end dates from form,
       check if mealplan exists for each date in range
       if not exist, then create new mealplan for each date
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


# def newflow(var):
#     """returns new flow instance to manage OAuth grant access, 
#        uri configured in API Google console
#        var is my session info that I want to keep after oauth
#     """
#     var = str(var)
#     new_url = 'http://localhost:5000/callback'+var

#     flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
#                                          scopes=SCOPES,
#                                          redirect_uri=new_url)

#     return flow
