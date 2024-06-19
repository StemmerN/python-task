import requests
import os
import argparse
from flask import Flask, request, jsonify

target_url = 'http://127.0.0.1:8000/upload-csv/'
fixed_token = 'TestToken'

parser = argparse.ArgumentParser(description='Client-Skript zum Hochladen einer CSV-Datei.')
parser.add_argument('-p', '--csv-path', type=str, help='Pfad zur CSV-Datei')
args = parser.parse_args()

if args.csv_path:
    file_path = args.csv_path
else:
    file_path = 'C:/Users/nikolais/Documents/python-task/vehicles.csv'

if os.path.exists(file_path):
    print("Die Datei existiert.")
else:
    print("Die Datei existiert nicht.")
    exit()

login_response = requests.post('http://127.0.0.1:8000/login', json={'username': 'Test', 'password': '123456'})
if login_response.status_code == 200:
    login_data = login_response.json()
    if login_data['login']:
        token = fixed_token

        with open(file_path, 'rb') as file_data:
            files = {'file': file_data}
            headers = {'Authorization': token}
            response = requests.post(target_url, files=files, headers=headers)

        print(response.status_code)
    else:
        print('Login fehlgeschlagen.')
else:
    print('Fehler beim Login')
