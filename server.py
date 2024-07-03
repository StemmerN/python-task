import requests
import uvicorn
import pandas as pd
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

target_url = 'https://api.baubuddy.de/'

url = "https://api.baubuddy.de/index.php/login"
payload = {
    "username": "365",
    "password": "1"
}
headers = {
    "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
    "Content-Type": "application/json"
}
response = requests.request("POST", url, json=payload, headers=headers)
print(response.text)


@app.post('/upload-csv/')
async def root(file: UploadFile = File(...)):
    contents = await file.read()

    df = pd.read_csv(contents)

    return {"filename": file.filename}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
