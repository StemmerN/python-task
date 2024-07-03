from fastapi import FastAPI, File, UploadFile
import uvicorn

app = FastAPI()


@app.post('/upload-csv/')
async def root(file: UploadFile = File(...)):
    return {"filename": file.filename}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
    