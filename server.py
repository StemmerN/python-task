import logging
from fastapi import FastAPI, File, UploadFile
import uvicorn

app = FastAPI()
logger = logging.getLogger("api")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("api.log"),
        logging.StreamHandler()
    ]
)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.post('/upload-csv/')
async def root(file: UploadFile = File(...)):
    logger.info("POST request received for /upload-csv/")
    return {"filename": file.filename}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
