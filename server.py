from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Header
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import uvicorn


app = FastAPI()
security = HTTPBasic()

users_db = {'Test': {'username': 'Test', 'password': '123456'}}
token = 'TestToken'


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = users_db.get(credentials.username)
    if user is None or user['password'] != credentials.password:
        raise HTTPException(status_code=401, detail='Ungültige Anmeldeinfromationen')
    return user


@app.post('/login')
def login(user: dict = Depends(get_current_user)):

    return {'username': user['username'], 'token': token, 'message': 'Login erfolgreich'}


@app.post('/upload-csv/')
async def upload_csv(file: UploadFile = File(...)):
    if token is None or token != token:  # Token wird überprüft
        raise HTTPException(status_code=401, detail='Token fehlt')

    return {'filename': file.filename}


@app.get('/')
def read_root():
    return {'message': 'Welcome to the FastAPI application'}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
