import requests

login_url = 'https://api.baubuddy.de/index.php/v1/login'
headers = {'principal': 'default_test', 'Authorization': 'Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz'}
login_data = {'username': '365', 'password': '1'}
login_response = requests.post(
    login_url,
    headers=headers,
    json=login_data,
)

json_response = login_response.json()
if login_response.status_code != 200 or 'oauth' not in json_response:
    print(
        f'Failure: {login_response.status_code} {login_response.text}',
    )
    exit(1)
else:
    token_info = json_response['oauth']

repost = requests.get('http://127.0.0.1:8000/')

url = 'http://127.0.0.1:8000/'
files = {'file': ('vehicles.csv', 'rb')}

r = requests.get(url, files=files)
var = r.text

headers: dict[str, str] = {'Authorization': 'Bearer', 'json_response': 'access_token'}
print(files)

file_data = open('vehicles.csv')

r = requests.get(url, files={'vehicles.csv': file_data})

print(r.status_code)
