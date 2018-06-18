from bottle import Bottle, run
from pprint import pprint
import json
import requests

with open('client_secret.json') as file:
    data = json.load(file)


pprint(data["installed"])
app = Bottle()


@app.get('/')
def test():
    req = requests.get('https://yandex.ru')
    print(req)
    return 'Hello'


run(debug=True, host='localhost', port=3000, reloader=True)
