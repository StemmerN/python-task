import uvicorn
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Header
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    ]
)

app = FastAPI()
security = HTTPBasic()

users_db = {
    'Test': {'username': 'Test', 'password': '123456'}}
fixed_token = 'TestToken'


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = users_db.get(credentials.username)
    if user is None or user['password'] != credentials.password:
        logging.error('Ungültige Anmeldeinformationen')
        raise HTTPException(status_code=401, detail='Ungültige Anmeldeinformationen')
    logging.info(f'Benutzer {credentials.username} hat sich angemeldet.')
    return user


@app.post('/login')
def login(user: dict = Depends(get_current_user)):
    logging.info('Erfolgreiches Login')
    return {'username': user['username'], 'token': fixed_token, 'login': True}


@app.post('/upload-csv/')
async def upload_csv(file: UploadFile = File(...), token: str = Header(None)):
    if token is None or token != fixed_token:
        logging.error('Ungültiges Token')
        raise HTTPException(status_code=401, detail='Ungültiges Token')

    logging.info(f'Uploading file: {file.filename}')
    return {'filename': file.filename}


@app.get('/')
def read_root():
    logging.info('Rootendpoint aufgerufen')
    return {'message': 'Welcome to the FastAPI application'}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
