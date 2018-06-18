import google.oauth2.credentials
from google_auth_oauthlib.flow import Flow
from pprint import pprint

CLIENT_SECRETS_FILE = './client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob')

auth_url, _ = flow.authorization_url(prompt='consent')
print('Please go to this URL: {}'.format(auth_url))
code = input('Enter the authorization code: ')

flow.fetch_token(code=code)

session = flow.authorized_session()
print(session.get('https://www.googleapis.com/auth/calendar.readonly').json())
