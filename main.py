import requests
import os
import argparse
from flask import Flask, request, jsonify
import uuid

target_url = 'http://127.0.0.1:8000/upload-csv/'

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == 'Test' and password == '123456':
        token = str(uuid.uuid4())
        return jsonify({'login': True, 'token': token})
    else:
        return jsonify({'login': False})


@app.route('/upload-csv/', methods=['POST'])
def upload_csv():
    token = request.headers.get('Authorization')

    # Überprüfung des Token
    if token is None:
        return jsonify({'message': 'Kein Token angegeben'}), 401

    # Datei-Upload
    file = request.files.get('file')
    if file:
        # Verarbeitung der Datei
        return jsonify({'message': 'Datei erfolgreich hochgeladen'}), 200
    else:
        return jsonify({'message': 'Keine Datei angegeben'}), 400


if __name__ == '__main__':
    app.run(debug=True)

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

# Login-Anfrage
login_response = requests.post('http://127.0.0.1:8000/login', json={'username': 'Test', 'password': '123456'})
if login_response.status_code == 200:
    login_data = login_response.json()
    if login_data['login']:
        token = login_data['token']

        # Datei-Upload mit Token
        with open(file_path, 'rb') as file_data:
            files = {'file': file_data}
            headers = {'Authorization': token}
            r = requests.post(target_url, files=files, headers=headers)

        print(r.status_code)
    else:
        print("Login fehlgeschlagen.")
else:
    print("Fehler beim Login.")
