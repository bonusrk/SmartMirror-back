from bottle import Bottle, run, get, post
from googleapiclient import discovery
from oauth2client import file, client, tools
from httplib2 import Http
from pprint import pprint
import datetime

session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.auto': True,
}

app = Bottle()
CLIENT_SECRETS_FILE = './client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
store = file.Storage('credentials.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
    # auth_url, _ = flow.authorization_url(prompt='consent')
    # print('Please go to this URL: {}'.format(auth_url))
    # code = input('Enter the authorization code: ')
    # flow.fetch_token(code=code)

service = discovery.build('calendar', 'v3', http=creds.authorize(Http()))


@get('/')
def index():
    return 'Hello world'


@get('/calendar')
def calendar():
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='fp8pfobln6ppgr53nqa3pp08o8@group.calendar.google.com',
                                          timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return 'No upcoming events found.'
    for event in events:
        pprint(event)
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    return events[0]['summary']


run(debug=True, host='localhost', port=3000, reloader=True)
