from fastapi import FastAPI, File, UploadFile, HTTPException, Header
import os
import argparse
import requests

app = FastAPI()

target_url = 'http://127.0.0.1:8000'
token = 'TestToken'


@app.post('/upload-csv/')
async def upload_csv(file: UploadFile = File(...), token: str = Header(None)):
    if token is None or token != 'TestToken':  # Überprüfung des Tokens
        raise HTTPException(status_code=401, detail='Ungültiges Token')

    if file:
        return {'message': 'Datei erfolgreich hochgeladen'}
    else:
        raise HTTPException(status_code=400, detail='Keine Datei angegeben')


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

with open(file_path, 'rb') as file_data:
    files = {'file': file_data}
    headers = {'Authorization': token}
    response = requests.post(target_url, files=files, headers=headers)

print(response.status_code)
