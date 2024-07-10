import logging
from typing import io
import requests
import uvicorn
import pandas as pd
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()


def get_token():
    target_url = 'https://api.baubuddy.de/'
    url = f"{target_url}index.php/login"
    payload = {
        "username": "365",
        "password": "1"
    }
    headers = {
        "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["token"]


@app.post('/upload-csv/')
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        logging.info(f"CSV-Datei erfolgreich gelesen: {df.head()}")

        token = get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        target_url = 'https://api.baubuddy.de/'
        url = f"{target_url}upload_csv"

        response = requests.post(url, files={"file": (file.filename, contents, file.content_type)}, headers=headers)
        response.raise_for_status()

        return JSONResponse(content={"message": "Upload erfolgreich"}, status_code=200)
    except requests.exceptions.RequestException as e:
        logging.error(f"Fehler beim Hochladen der Datei: {e}")
        return JSONResponse(content={"message": "Upload fehlgeschlagen", "error": str(e)}, status_code=500)
    except Exception as e:
        logging.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return JSONResponse(content={"message": "Upload fehlgeschlagen", "error": str(e)}, status_code=500)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
