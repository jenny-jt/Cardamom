# Cardamom
# <img src=">

Cardamom is a web application that syncs up with your Google Calendar to manage meal planning. Simply input the ingredients you have on hand, or want to use, and Cardamom will generate meals and organize them for you. Modification is easy with a click of a button, and recipe events will be added automatically to your calendar once you approve.

## Contents
* [Tech Stack](#tech-stack)
* [Installation](#installation)
* [Features](#features)
* [About the Developer](#about-the-developer)

## <a name="tech-stack"></a>Tech Stack
__Front end:__ React, JavaScript, HTML5, CSS, React-Bootstrap<br/>
__Back end:__ Python, Flask, PostgreSQL, SQLAlchemy<br/>
__APIs:__ Google Calendar, Spoonacular<br/>

## <a name="features"></a>Features

#### Creating a mealplan:
1. Enter ingredients you would like to use
![Image of ingredients](http://0.0.0.0:5000/static/img/readme_img/ingredients.png)
2. Select number of recipes per day you would like
![Image of num of recipes](demo/num_recipes.png)
3. Select range of dates for mealplans to be generated for
![Image of dates](http://0.0.0.0:5000/static/img/readme_img/dates.png)

#### View a meal plan
User is automatically redirected to Mealplans page, displaying all mealplans with the most recently created at the top. Individual meal plan selected by clicking the plate icon on the left of the mealplan with the desired date. The icon will change from white to navy blue on hover.
![Image of selecting meal plan](http://0.0.0.0:5000/static/img/readme_img/mealplan_select.png)

#### Modify a meal plan
Modification of mealplan is simple, with the click of a button
![Image of modification](http://0.0.0.0:5000/static/img/readme_img/modification.png)

#### Adding to Google Calendar
Recipe events are added to Google Calendar with the "Add to Calendar" button
![Image of adding to cal](http://0.0.0.0:5000/static/img/readme_img/add_to_cal.png)

Total cook time and link to recipe included with every calendar event
![Image of cook time and url](http://0.0.0.0:5000/static/img/readme_img/cook_time_url.png)

## <a name="installation"></a>Installation
To run Cardamom on your local machine, follow the steps below:

Install PostgreSQL (Mac OSX)

Clone or fork this repo:
```
https://github.com/jenny-jt/Cardamom/tree/edit-React
```

Create secrets.sh file inside your Cardamom directory, making sure to update
the secret key below:
```
touch secrets.sh
echo 'export SECRET_KEY = "(insert your secret key here)"' > secrets.sh
source secrets.sh
```

Enter the Calendar ID in the api/cal server endpoint for the Google Calendar you would like to user for meal planning. This can be a separate MealPlan calendar or your Primary Calendar
```
cal_id = '(insert your calendar ID here)'
```

Create and activate a virtual environment inside your Cardamom directory:
```
virtualenv env
source env/bin/activate
```

Install the dependencies:
```
pip install -r requirements.txt
```

Set up the database:
```
createdb cardamom
python3 seed.py
```

Run the app:
```
python3 server.py
```

You can now navigate to 'localhost:5000' to access Cardamom.

## <a name="about-the-developer"></a>About the Developer
Jenny Tan is a software engineer located in the San Francisco Bay Area. Previously, she worked as en optometrist, and started her coding adventure during COVID-19. She built Cardamom, her first web app, to make pandemic life easier. Cardamom takes the guesswork out of mealtimes by generating recipes using ingredients already on hand.

Contact
Jenny Tan- https://www.linkedin.com/in/jenny-tan-2020/