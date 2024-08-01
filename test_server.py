import subprocess
import time
import os
import requests
import pytest

@pytest.fixture(scope="module")
def server_process():
    # Start the server as a subprocess
    process = subprocess.Popen(['uvicorn', 'server:app', '--host', '127.0.0.1', '--port', '8003', '--reload'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)  # Give the server time to start
    yield process
    process.terminate()
    process.wait()

@pytest.fixture
def csv_file_path():
    return "vehicles_fixed.csv"

def test_root_endpoint(server_process):
    # Test the root endpoint
    response = requests.get("http://127.0.0.1:8003")
    assert response.status_code == 200
    assert response.json() == {"message": "Willkommen bei der FastAPI Anwendung. Verfügbare Endpunkte: /upload-csv/"}

def test_upload_csv_endpoint(server_process, csv_file_path):
    # Ensure the CSV file exists
    assert os.path.exists(csv_file_path), f"CSV file not found: {csv_file_path}"

    # Test the /upload-csv/ endpoint
    with open(csv_file_path, 'rb') as f:
        response = requests.post("http://127.0.0.1:8003/upload-csv/", files={'file': f})
        assert response.status_code == 200
        assert response.json() == {"message": "CSV-Datei erfolgreich gelesen und verarbeitet"}

if __name__ == "__main__":
    pytest.main()
