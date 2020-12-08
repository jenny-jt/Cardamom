# Cardamom

Cardamom is a web application that syncs up with your Google Calendar to manage meal planning. Simply input the ingredients you have on hand, or want to use, and Cardamom will generate meals and organize them for you. Modification is easy with a click of a button, and recipe events will be added automatically to your calendar once you approve.

Creating a mealplan:
1. Enter ingredients you would like to use
![Image of ingredients](http://0.0.0.0:5000/static/img/readme_img/ingredients.png)
2. Select number of recipes per day you would like
![Image of num of reicpes](http://0.0.0.0:5000/static/img/readme_img/num_recipes.png)
3. Select range of dates for mealplans to be generated for
![Image of dates](http://0.0.0.0:5000/static/img/readme_img/dates.png)

User is automatically redirected to Mealplans page, displaying all mealplans with the most recently created at the top. Individual meal plan selected by clicking the plate icon on the left of the mealplan with the desired date. The icon will change from white to navy blue on hover.
![Image of selecting meal plan](http://0.0.0.0:5000/static/img/readme_img/mealplan_select.png)

Modification of mealplan is simple, with the click of a button
![Image of modification](http://0.0.0.0:5000/static/img/readme_img/modification.png)

Recipe events are added to Google Calendar with the "Add to Calendar" button
![Image of adding to cal](http://0.0.0.0:5000/static/img/readme_img/add_to_cal.png)

Total cook time and link to recipe included with every calendar event
![Image of cook time and url](http://0.0.0.0:5000/static/img/readme_img/cook_time_url.png)


Tech Stack
Frontend: Javascript, React, React-Bootstrap, HTML, CSS
Backend: Python, Flask, SQLAlchemy, PostgreSQL
APIs: Google Calendar, Spoonacular

Set Up: 
Enter the Calendar ID for the Google Calendar you would like to user for meal planning. This can be a separate MealPlan calendar or your Primary Calendar

Contact
Jenny Tan- https://www.linkedin.com/in/jenny-tan-2020/
