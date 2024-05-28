from fastapi import FastAPI, File, UploadFile
from typing_extensions import Annotated

app = FastAPI()


@app.post('/upload file/')
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
