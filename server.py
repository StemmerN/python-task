import typing
import uvicorn
from fastapi import FastAPI
import requests
import urllib.request

app: FastAPI = FastAPI()


@app.get('/')
def read_root():
    return {'get succeeded'}


@app.get('/items/{item_id}')
def read_item(item_id: int, q: typing.Union[str, None] = None):
    return dict(item_id=item_id, q=q)


@app.post('C:/Users/nikolais/Documents/python-task/vehicles.csv')
@app.get('/')
def write_csv():
    return {'post succeeded'}


if '__server__' == __name__:
    uvicorn.run(app, host="127.0.0.1", port=8000)


req = urllib.request.Request('http://127.0.0.1:8000/')
with urllib.request.urlopen(req) as response:
    the_page = response.read()

url = 'https://api.baubuddy.de/index.php/v1/login'
payload = {
    'username': '365',
    'password': '1'
}
headers = {
    'Authorization': 'Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz',
    'Content-Type': 'application/json'
}
response = requests.request('POST', url, json=payload, headers=headers)
print(response.text)