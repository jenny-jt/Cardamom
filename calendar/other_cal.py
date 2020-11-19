
from jinja2 import StrictUndefined
import os
from flask import (Flask, jsonify, url_for, render_template, redirect, request, flash, session)
import json
# from flask_debugtoolbar import DebugToolbarExtension
from apiclient.discovery import build
import googleapiclient.discovery
import google.oauth2.credentials
import google_auth_oauthlib.flow
import httplib2
from urllib.parse import parse_qs
from model import *
from server import app

CLIENT_SECRETS_FILE = 'client_secret.json'
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

@app.route('/')
def index():
    '''Displays homepage'''
    return render_template('homepage.html')

@app.route('/authorize')
def authorize():
    '''Asks user for authorization to google calendar account'''

    #creates flow instance to manage OAuth grant access
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

    #uri configured in API Google console
    flow.redirect_uri = 'http://localhost:5000/oauth2callback'

    #finds authorization url
    authorization_url, state = flow.authorization_url(
                                access_type='offline', 
                                include_granted_scopes='true')

    session['state'] = state

    #redirect user through authorization url 
    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    '''Processes response for google calendar authorization'''

    #creates flow instance to manage OAuth grant access
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = 'http://localhost:5000/oauth2callback'

    authorization_response = request.url

    #fetch tocken for the authorization response
    flow.fetch_token(authorization_response=authorization_response)

    #credentials stored
    credentials = flow.credentials

    session['credentials'] = credentials_to_dict(credentials)
    flash('Succesfully logged in to Google Calendar! Try adding again.')
    return redirect('/cal')

@app.route('/cal')
def cal():
    return "yay"


@app.route('/add-to-calendar', methods=['GET'])
def make_calendar_event():
    '''Add all-day recipe event to user's google calendar with OAUTH'''
    #checks if credentials not already in session
    if 'credentials' not in session:
        return redirect('/authorize')
    #gets information about recipe to add to calendar
    # recipes = [<Recipe name = 3-Ingredient Bacon Stuffed Mushrooms ingredients = {"button mushrooms", "cooked bacon", "feta cheese"}>, 
    #     <Recipe name = Easy Pesto Stuffed Mushrooms ingredients = {"button mushrooms", parmesan, pesto }>]
    #grabs stored OAuth credentials
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])

    #client a google api client to make google calendar event
    drive = googleapiclient.discovery.build(
      'calendar', API_VERSION, credentials=credentials)

    #creates google calendar event with session stored moon phase info
    # session['event'] = create_google_calendar_event(recipe.name, recipe.url)
    #adds the calendar event to the google calendar
    event_to_add = drive.events().insert(calendarId='tl9a33nl5al9k337lh45f40av8', sendNotifications=True, body=session['event']).execute()
    flash('Event added to calendar!')
    return redirect('/calendar')


def credentials_to_dict(credentials):
  """Takes in credentials from OAuth and returns in dictionary format"""

  #Returns dictionary for OAuth process
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


def create_google_calendar_event(recipe):
  """Takes recipe object and uses name and url to turn into google calendar event"""

  #dictionary for google event information
  event = {
            'summary': f'{recipe.name}',
            'start': start.date,
            'end': end.date,
            'description': f'{recipe.url}'
        }
  return event


if __name__ == '__main__':
    
    app.debug = False
