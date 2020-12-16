from unittest import TestCase, main
from server import app
from model import User, MealPlan, Recipe
from crud import add_mealplan, user_by_email
from flask import Flask, request, render_template, redirect, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os


class FlaskTestCaseLoggedIn(TestCase):
    """Flask tests using session without user logged in"""

    def setUp(self):
        """Stuff to do before every test."""
        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        """stuff to do after each test"""
        pass

    def test_home(self):  # GET request
        self.client = app.test_client()
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)

    # def test_authorize(self):
    #     self.client = app.test_client()
    #     return self.client.get('/authorize', follow_redirects=True)

    # def test_recipes_page(self):  # GET request
    #     self.client = app.test_client()
    #     result = self.client.get('/api/recipes')
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('Recipes', result.data)


class FlaskTests(TestCase):
    """Flask tests"""

    def setUp(self):
        # ? how to take out os.system cmds and how much stub data
        # ? how to properly set up testdb
        app.config['TESTING'] = True
        self.client = app.test_client()

        db = SQLAlchemy(app)
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        os.system('createdb testdb')
        # Connect to test database
        connect_to_db(app)
        # Create tables and add sample data
        db.create_all()
        os.system('python3 model.py')
        os.system('python3 seed_database.py')  # ? should i run my model and seed_db to create db
        self.test_user = user_by_email("email@test.com")
        self.test_mealplan = add_mealplan("11-02-2020", self.test_user)
        print(self.test_mealplan)

    def tearDown(self):
        """stuff to do after each test"""
        os.system('dropdb testdb')

    def test_login(self):
        with app.test_client() as c:
            # info i'm "getting" from the front end
            result = c.post('/api/login', json={'name': user.name, 'id': user.id})
            data = result.get_json()
            self.assertEqual(result.status_code, 200)
            # checking to see if output is appropriate
            self.assertIn('name', result.data)

    def test_login_error(self):
        with app.test_client() as c:
            result = c.post('/api/login', json={'no user with this email'})
            data = result.get_json()
            self.assertEqual(result.status_code, 200)
            self.assertIn('no user', result.data)

    def test_new_user(self):  
        with app.test_client() as c:
            # ? do i pass in new user data here
            result = c.post('/api/new_user', json={'name': user.name, 'id': user.id})
            data = result.get_json()
            self.assertEqual(result.status_code, 200)
            self.assertIn('name', result.data)

    def test_new_user_error(self):
        with app.test_client() as c:
            result = c.post('/api/new_user', json={'user with this email already exists'})
            data = result.get_json()
            self.assertEqual(result.status_code, 200)
            self.assertIn('already exists', result.data)

    def test_mealplans_page(self):
        # ? how would i not use a POST request and still have it be JSON
        # ? give user info and test the data that comes out, which is JSON
        with app.test_client() as c:
            result = c.post('/api/mealplans', json={'user['id']': mealplan.id})
            data = result.get_json()
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'mp['id']', result.data)



# class FlaskTestCaseLoggedIn(TestCase):
#     """Flask tests using session with user logged in"""

#     def setUp(self):
#         """Stuff to do before every test."""
#         # Show Flask errors that happen during tests
#         app.config['TESTING'] = True
#         # set secret key because using session
#         app.config['SECRET_KEY'] = 'key'
#         # Get the Flask test client
#         self.client = app.test_client()

#         # test to see if things are being stored in session
#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = 1

#     def tearDown(self):
#         """stuff to do after each test"""
#         pass

#     def test_home(self):  # GET request
#         self.client = app.test_client()
#         result = self.client.get('/', follow_redirects=True)
#         self.assertEqual(result.status_code, 200)

#     def test_favorite_color_form(self):  # POST request
#         self.client = app.test_client()
#         result = self.client.post('/fav-color', data={'color': 'blue'})
#         self.assertIn(b'Woah! I like blue, too', result.data)


if __name__ == '__main__':
    main()
