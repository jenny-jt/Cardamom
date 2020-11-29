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

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """stuff to do after each test"""

    def test_index(self):  # GET request
        self.client = app.test_client()
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h1>Test</h1>', result.data)
        self.assertIn(b'<h1>Color Form</h1>', result.data)

    def test_favorite_color_form(self):  # POST request
        self.client = app.test_client()
        result = self.client.post('/fav-color', data={'color': 'blue'})
        self.assertIn(b'Woah! I like blue, too', result.data)

    def test_mealplans_page(self):  # GET request
        self.client = app.test_client()
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h1>Test</h1>', result.data)
        self.assertIn(b'<h1>Color Form</h1>', result.data)

    def test_recipes_page(self):  # GET request
        self.client = app.test_client()
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h1>Test</h1>', result.data)
        self.assertIn(b'<h1>Color Form</h1>', result.data)


class FlaskTests(TestCase):
    """Flask tests"""
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")
        # Create tables and add sample data
        db.create_all()
        test_data()


if __name__ == '__main__':
    unittest.main()