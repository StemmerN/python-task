from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Header
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import uvicorn
import uuid
from datetime import datetime, timedelta
import psycopg2

app = FastAPI()
security = HTTPBasic()

users_db = {'Test': {'username': 'Test', 'password': '123456'}}
tokens = {}


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = users_db.get(credentials.username)
    if user is None or user['password'] != credentials.password:
        raise HTTPException(status_code=401, detail='Ungültige Anmeldeinfromationen')
    return user


def create_token(token: str, user_id: int, expires_at: datetime):
    conn = psycopg2.connect(
        host='127.0.0.1, port=8000',
        database='Token.sql',
        user='Test',
        password='123456',
    )
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO tokens (token, user_id, expires_at) VALUES (%s, %s, %s)',
        (token, user_id, expires_at)
    )
    conn.commit()
    cur.close()
    conn.close()


def validate_token(token: str):
    conn = psycopg2.connect(
        host='127.0.0.1, port=8000',
        database='Token.sql',
        user='Test',
        password='123456',
    )
    cur = conn.cursor()
    cur.execute(
        'SELECT COUNT(*) FROM tokens WHERE token = %s AND expires_at > NOW()',
        (token,)
    )
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count > 0


@app.post('/login')
def login(user: dict = Depends(get_current_user)):
    token = str(uuid.uuid4())  # Token Generierung
    expires_at = datetime.utcnow() + timedelta(minutes=15)
    create_token(token, user_id=1, expires_at=expires_at)

    return {'username': user['username'], 'token': token, 'message': 'Login erfolgreich'}


@app.post('/upload-csv/')
async def upload_csv(file: UploadFile = File(...), token: str = Header(None)):
    if token is None:  # Token wird überprüft
        raise HTTPException(status_code=401, detail='Token fehlt')

    token_data = tokens.get(token)
    if token_data is None:
        raise HTTPException(status_code=401, detail='Token abgelaufen')

    return {'filename': file.filename}


@app.get('/')
def read_root():
    return {'message': 'Welcome to the FastAPI application'}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
