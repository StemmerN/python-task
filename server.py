import logging
import io
import pandas as pd
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


@app.get("/")
def read_root():
    return {"message": "Willkommen bei der FastAPI Anwendung. Verfügbare Endpunkte: /upload-csv/"}


@app.post('/upload-csv/')
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        logging.debug(f"Dateiinhalt: {contents.decode('utf-8')}")
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        logging.info(f"CSV-Datei erfolgreich gelesen: {df.head()}")
        return JSONResponse(content={"message": "CSV-Datei erfolgreich gelesen und verarbeitet"}, status_code=200)
    except pd.errors.ParserError as e:
        logging.exception("Fehler beim Lesen der CSV-Datei")
        return JSONResponse(content={"message": "Fehler beim Verarbeiten der CSV-Datei", "error": str(e)}, status_code=400)
    except Exception as e:
        logging.exception("Ein unerwarteter Fehler ist aufgetreten")
        return JSONResponse(content={"message": "Upload fehlgeschlagen", "error": str(e)}, status_code=500)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8001)
