import argparse
import logging
import os
import requests
import sys

# Ziel-URL für den Upload
target_url = 'http://127.0.0.1:8000/upload-csv/'

# Konfiguration des Loggings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Argumentparser für Kommandozeilenargumente
parser = argparse.ArgumentParser(description='Skript zum Hochladen einer CSV-Datei.')
parser.add_argument('-p', '--csv-path', type=str, required=True, help='Pfad zur CSV-Datei')
parser.add_argument('-v', '--verbose', action='store_true', help='Erhöhte Ausgabedetails')
args = parser.parse_args()

# Erhöhte Ausgabedetails aktivieren, wenn das entsprechende Argument gesetzt ist
if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)

file_path = args.csv_path

# Prüfen, ob die Datei existiert
if not os.path.exists(file_path):
    logging.error('Die Datei existiert nicht.')
    sys.exit(2)  # Statuscode 2 für Datei nicht gefunden

try:
    with open(file_path, 'rb') as file_data:
        files = {'file': file_data}
        logging.info('Beginne mit dem Hochladen der Datei...')
        response = requests.post(target_url, files=files)
        response.raise_for_status()  # HTTP-Fehler auslösen, falls Statuscode nicht 200
        logging.info('Datei erfolgreich hochgeladen.')
        logging.debug(f'Status Code: {response.status_code}')
        logging.debug(f'Response: {response.text}')
except requests.exceptions.HTTPError as e:
    logging.exception(f"HTTP-Fehler beim Hochladen der Datei: {e.response.text if e.response else 'Keine Antwort erhalten'}")
    sys.exit(3)  # Statuscode 3 für Netzwerk- oder HTTP-Fehler
except Exception as e:
    logging.exception('Ein unerwarteter Fehler ist aufgetreten')
    sys.exit(1)  # Statuscode 1 für allgemeine Fehler


# python .\main.py -p C:\Users\nikolais\Documents\python-task\vehicles.csv
# python .\main.py -p C:\Users\nicolai\PycharmProjects\python-task\vehicles.csv
