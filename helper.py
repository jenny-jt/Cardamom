"""All helper functions"""
from model import MealPlan
from random import choice
from crud import add_mealplan, create_api_recipes
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


def check_mealplan(date):
    """checks if mealplan exists, otherwise makes a new mealplan object"""
    mealplan = MealPlan.query.filter(MealPlan.date == date).first()

    if not mealplan:
        mealplan = add_mealplan(date)

    return mealplan


#######################################
# start_date = 2020-11-18
# end_date = 2020-11-27

# start_date.split("-") --> [2020, 11, 18]
# compare months to make sure youre in the same months
# duration = end_array[-1] - start_array[-1] --> 9 days

# for day in range(duration):
#     current_iso = ' '.join()
#     check_mealplan()

# ex of mealplan.date = Mealplan for: 2020-11-26 00:00:00+00:00
# from datetime import timedelta, date
#####################################################

# def daterange(start_date, end_date):
#     for n in range(int((end_date - start_date).days)):
# #         yield start_date + timedelta(n)

# start_date = date(2013, 1, 1)
# end_date = date(2015, 6, 2)

# for date in daterange(start_date, end_date):
#     checkmealplan(date)

# #     print(single_date.strftime("%Y-%m-%d"))


def create_recipe_list(ingredients, num, db_recipes):
    """takes in num as well as list of recipes from db
       will make api recipe list if needed
       returns recipe list that is num long (picked randomly from db only or db + api)
       also returns leftover db_recipes (lists[1]) and api_recipes (lists[2]) lists
    """
    if len(db_recipes) < num:
        api_recipes = create_api_recipes(ingredients, num)
        lists = make_recipe_list(num, db_recipes, api_recipes)
    else:
        lists = make_recipe_list(num, db_recipes)

    return lists


def make_recipe_list(number, db_recipes, api_recipes=[]):
    """takes in db and api recipe lists, selects number of them to generate recipe list
       also contains the leftovers of the db and api lists
    """

    count = 0
    recipe_list = []
    while count < number:
        if db_recipes:
            item = pick_recipes(db_recipes)
            db_recipes.remove(item)
        else:
            item = pick_recipes(api_recipes)
            api_recipes.remove(item)

        recipe_list.append(item)
        count += 1

    return recipe_list, api_recipes, db_recipes


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


def create_alt_recipes(lists, ingredients, num, mealplan):
    """creates list of alternate recipes"""

    if len(lists) > 2:
        alt_recipes = lists[1] + lists[2]
    else:
        alt_recipes = lists[1]

    if not alt_recipes:
        new_api_recipes = create_api_recipes(ingredients, (num+5))
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


def mealplan_dates(start_date, end_date):
    """take in start and end dates from form,
       check if mealplan exists for each date in range
       if not exist, then create new mealplan for each date
       returns list of mealplans for date range
    """
    mealplans = []
    delta = timedelta(days=1)

    while start_date <= end_date:
        start_date_string = start_date.strftime("%Y-%m-%d")
        print(start_date_string)
        mealplan = check_mealplan(start_date_string)
        mealplans.append(mealplan)
        start_date += delta

    return mealplans
