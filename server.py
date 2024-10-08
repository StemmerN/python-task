import logging
import io
import pandas as pd
import uvicorn
import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.get('/')
def read_root():
    return {
        'message': 'Welcome to the FastAPI application. Available endpoints: /upload-csv/, /get-vehicles/'
    }


# Retrieve the access token from the Baubuddy API
def get_access_token():
    try:
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
        response.raise_for_status()
        access_token = response.json()['oauth']['access_token']
        return access_token
    except Exception as e:
        logging.exception('Error while fetching the access token')
        raise


def get_active_vehicles(access_token):
    try:
        url = 'https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.exception('Error while fetching active vehicles')
        raise


def get_color_code(access_token, label_ids):
    colors = {}
    for label_id in label_ids:
        try:
            url = f'https://api.baubuddy.de/dev/index.php/v1/labels/{label_id}'
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            colors[label_id] = data['colorCode']
        except Exception as e:
            logging.exception(f'Error fetching the color for Label ID {label_id}')
            colors[label_id] = None
    return colors


@app.post('/upload-csv/')
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        csv_str = contents.decode('utf-8')

        # Read the CSV file header to determine how many fields the file has
        first_line = csv_str.split('\n')[0]
        expected_fields = len(first_line.split(';'))
        logging.info(f'Expected number of fields: {expected_fields}')

        # Debug: Output erroneous lines
        lines = csv_str.split('\n')
        for i, line in enumerate(lines):
            if len(line.split(';')) != expected_fields:
                logging.error(f'Erroneous line {i+1}: {line}')

        csv_data = pd.read_csv(io.StringIO(csv_str), delimiter=';')
        logging.info(f'CSV file successfully read: {csv_data.head()}')

        access_token = get_access_token()
        active_vehicles = get_active_vehicles(access_token)

        # Filter out vehicles without 'hu' field and resolve label colors
        filtered_vehicles = []
        for vehicle in active_vehicles:
            if vehicle.get('hu'):
                label_ids = vehicle.get('labelIds') or []
                vehicle['labelColors'] = get_color_code(access_token, label_ids)
                filtered_vehicles.append(vehicle)

        # Create combined data structure
        combined_data = {
            'csv_data': csv_data.to_dict(orient='records'),
            'vehicle_data': filtered_vehicles
        }

        # Remove duplicates in vehicle data
        combined_data['vehicle_data'] = list({v['labelIds']: v for v in combined_data['vehicle_data']}.values())

        # Convert NaN values in CSV data to None (which is represented as null in JSON)
        combined_data['csv_data'] = [{k: (None if pd.isna(v) else v) for k, v in record.items()} for record in combined_data['csv_data']]

        # Return combined data structure as JSON response
        logging.info(f'Combined data: {combined_data}')
        return JSONResponse(content=combined_data, status_code=200)

    except pd.errors.ParserError as e:
        logging.exception('Error reading the CSV file')
        return JSONResponse(content={'message': 'Error processing the CSV file', 'error': str(e)}, status_code=400)
    except Exception as e:
        logging.exception('An unexpected error occurred')
        return JSONResponse(content={'message': 'Upload failed', 'error': str(e)}, status_code=500)


@app.get('/get-vehicles/')
def get_vehicles():
    try:
        access_token = get_access_token()
        vehicles_data = get_active_vehicles(access_token)
        return JSONResponse(content=vehicles_data, status_code=200)
    except Exception as e:
        logging.exception('Error while fetching vehicle data')
        return JSONResponse(content={'message': 'Error fetching vehicle data', 'error': str(e)}, status_code=500)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8003)


# curl -X GET http://127.0.0.1:8003/get-vehicles/
