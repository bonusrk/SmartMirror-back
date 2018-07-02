from bottle import Bottle, run, get, route, response, request
from googleapiclient import discovery
from oauth2client import file, client, tools
from httplib2 import Http
from pprint import pprint
import datetime
import json

app = Bottle()
CLIENT_SECRETS_FILE = './client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
store = file.Storage('credentials.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)

service = discovery.build('calendar', 'v3', http=creds.authorize(Http()))


def cors(func):
    def wrapper(*args, **kwargs):
        response.set_header("Access-Control-Allow-Origin", "*")
        response.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        response.set_header("Access-Control-Allow-Headers", "Origin, Content-Type")

        # skip the function if it is not needed
        if request.method == 'OPTIONS':
            return

        return func(*args, **kwargs)

    return wrapper


@route('/')
def index():
    return 'Hello world'


@route('/tasks')
@cors
def tasks():
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='fp8pfobln6ppgr53nqa3pp08o8@group.calendar.google.com',
                                          timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return json.dumps(events)


run(debug=True, host='127.0.0.1', port=3000, reloader=True)
