import requests

file_path = 'C:/Users/nikolais/Documents/python-task/vehicles.csv'
target_url = 'http://127.0.0.1:8000/'
target_file = open(file_path, 'rb')

r = requests.post(target_url, files={'vehicles.csv': target_file})
print(r.status_code)
