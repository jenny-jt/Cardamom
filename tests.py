from unittest import TestCase
from server import app
from model import *
from crud import *
from flask import Flask, request, render_template, redirect, session, flash, jsonify

class FlaskTestCaseLoggedIn(TestCase):
    """Flask tests using session with user logged in"""

    def setUp(self):
        """Stuff to do before every test."""
        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        # set secret key because using session
        app.config['SECRET_KEY'] = 'key'
        # Get the Flask test client
        self.client = app.test_client()

        # test to see if things are being stored in session
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """stuff to do after each test"""
        pass

    def test_home(self):  # GET request
        self.client = app.test_client()
        result = self.client.get('/', follow_redirects=True)
        self.assertEqual(result.status_code, 200)


    def test_favorite_color_form(self):  # POST request
        self.client = app.test_client()
        result = self.client.post('/fav-color', data={'color': 'blue'})
        self.assertIn(b'Woah! I like blue, too', result.data)



class FlaskTests(TestCase):
    """Flask tests"""
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")
        # Create tables and add sample data
        db.create_all()
        test_data()   # should i copy my seed_db
    
    def tearDown(self):
        """stuff to do after each test"""
        pass

    def test_mealplans_page(self):  # GET request
        self.client = app.test_client()
        # fake user trying to visit my route
        result = self.client.get('/mealplans')
        # check status code = 200 (success)
        self.assertEqual(result.status_code, 200)


    def test_recipes_page(self):  # GET request
        self.client = app.test_client()
        result = self.client.get('/recipes')
        self.assertEqual(result.status_code, 200)


#########helper methods#########
def login(self, email, password)



if __name__ == '__main__':
    unittest.main()