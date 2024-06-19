from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import uvicorn
from flask import Flask, request, jsonify
import uuid

app = FastAPI()
security = HTTPBasic()
app = Flask(__name__)

users_db = dict(Test=dict(username="Test", password="123456"))


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = users_db.get(credentials.username)
    if user is None or user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


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


@app.get("/login")
def login(user: dict = Depends(get_current_user)):
    return {"username": user["username"], "message": "Login successful"}


@app.post('/upload-csv/')
async def upload_csv(file: UploadFile = File(...)):
    return {"filename": file.filename}


@app.get('/')
def read_root():
    return {'message': 'Welcome to the FastAPI application'}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
