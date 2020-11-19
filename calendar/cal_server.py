import datetime
import pickle
from flask import request, render_template, redirect
import os.path
# import arrow
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.oauth2.credentials
from server import app

CLIENT_SECRETS_FILE = "client_secret.json"
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
# If modifying these scopes, delete the file token.pickle.


def build_calendar_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            flow.redirect_uri = 'http://localhost:5000/oauthok'  #needs to be same as googlecloud
            credentials = flow.run_local_server(port=5000)
            # credentials = flow.run_console()

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    
    service = build('calendar', 'v3', credentials=credentials)

    authorization(flow)

    return service


def authorization(flow):
    # print(f'\n\n\n\nauthorization_url={authorization_url} flow.authorization_url()={flow.authorization_url()}\n\n\n\n')
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        include_granted_scopes='true')
        # Enable incremental authorization.
    # print(f'\n\n\n\nauthorization_url={authorization_url} flow.authorization_url()={flow.authorization_url()}\n\n\n\n')
    

@app.route("/test")
def test_oauth():
    return redirect(authorization_url)


@app.route("/oauthok")
def oauthok():
    return "yay"


@app.route('/')
def please_work():
    return 'it\'s a route'


# def token():
#     state = flask.session['state']
# flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#     'client_secret.json',
#     scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'],
#     state=state)
# flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

# authorization_response = flask.request.url
# flow.fetch_token(authorization_response=authorization_response)

# # Store the credentials in the session.
# state = flask.session['state']
# flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#     'client_secret.json',
#     scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'],
#     state=state)
# flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

# authorization_response = flask.request.url
# flow.fetch_token(authorization_response=authorization_response)

# # Store the credentials in the session.
# # ACTION ITEM for developers:
# #     Store user's access and refresh tokens in your data store if
# #     incorporating this code into your real app.
# credentials = flow.credentials
# flask.session['credentials'] = {
#     'token': credentials.token,
#     'refresh_token': credentials.refresh_token,
#     'token_uri': credentials.token_uri,
#     'client_id': credentials.client_id,
#     'client_secret': credentials.client_secret,
#     'scopes': credentials.scopes}


def list_all_calendars(gcal):
    page_token = None
    while True:
        calendar_list = gcal.calendarList().list(pageToken=page_token).execute()
        for cal in calendar_list["items"]:
            print(cal["summary"])
        page_token = calendar_list.get("nextPageToken")
        if not page_token:
            break


# def create_events_from_json(gcal, tl9a33nl5al9k337lh45f40av8):  #tzone = optional
#     events = []

#     for recipe in recipes:
#         body = {
#             'Summary': f"{recipe.name}",
#             'Start': 'start.date', 
#             'End': 'end.date',
#             'Description': f"{recipe.url}",
#             # 'Location': f"{recipe.url}",
#         }
#         recipe = (
#             gcal.events()
#             .insert(
#                 calendarId=tl9a33nl5al9k337lh45f40av8,
#                 body=body,)
#             .execute()
#         )

#         print(recipe)

#         events.append(recipe)

#     return events


    # # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])


if __name__ == '__main__':
    gcal = build_calendar_service()
    gcal.close()
    # events = Event.get_all_from(gcal, TARGET_ID)


    def credentials_to_dict(credentials):
  """Takes in credentials from OAuth and returns in dictionary format"""
  '''Takes in credentials from OAuth and returns in dictionary format'''

  #Returns dictionary for OAuth process
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


def create_google_calendar_event(title, date):
  """Takes title and date of event from FullCalendar to turn into google calendar event"""
  '''Takes title and date of event from FullCalendar to turn into google calendar event'''

  #convert datetime object to string to use for google event
  date = datetime.strptime(date[4:15], "%b %d %Y")
  date = date.strftime("%Y-%m-%d")

  #dictionary for google event information
  event = {'summary': title,
            'start': {'date': date,},
            'end': {'date': date}
        }
  return event
