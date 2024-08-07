import logging
import io
import pandas as pd
import uvicorn
import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_access_token():
    url = 'https://api.baubuddy.de/index.php/login'
    payload = {
        "username": '365',
        "password": '1'
    }
    headers = {
        'Authorization': 'Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Meldet Fehler bei fehlerhaften Statuscodes
    access_token = response.json()['oauth']['access_token']
    return access_token


def get_active_vehicles(access_token):
    url = 'https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


@app.get('/')
def read_root():
    return {'message': 'Willkommen bei der FastAPI Anwendung. Verfügbare Endpunkte: /upload-csv/, /get-vehicles/'}


@app.post('/upload-csv/')
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        logging.info(f'CSV-Datei erfolgreich gelesen: {df.head()}')

        return JSONResponse(content={'message': 'CSV-Datei erfolgreich gelesen und verarbeitet'}, status_code=200) # Status Code 200 = OK
    except pd.errors.ParserError as e:
        logging.exception('Fehler beim lesen der CSV-Datei')
        return JSONResponse(content={'message': 'Fehler beim verarbeiten der CSV-Datei', 'error': str(e)}, status_code=400) # Status Code 400 = Bad Request
    except Exception as e:
        logging.exception('Ein unerwarteter Fehler ist aufgetreten')
        return JSONResponse(content={'message': 'Upload fehlgeschlagen', 'error': str(e)}, status_code=500) # Status Code 500 = Server Error


@app.get('/get-vehicles/')
def get_vehicles():
    try:
        access_token = get_access_token()
        vehicles_data = get_active_vehicles(access_token)
        return JSONResponse(content=vehicles_data, status_code=200) # Status Code 200 = OK
    except Exception as e:
        logging.exception('Fehler beim Abrufen der Fahrzeugdaten')
        return JSONResponse(content={'message': 'Fehler beim Abrufen der Fahrzeugdaten', 'error': str(e)}, status_code=500) # Status Code 500 = Server Error


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8003)

# uvicorn.run(app, host="127.0.0.1", port=8003)
# curl -X GET http://127.0.0.1:8003/get-vehicles/