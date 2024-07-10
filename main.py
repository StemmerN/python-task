import argparse
import logging
import os
import requests
import sys

target_url = 'http://127.0.0.1:8000/upload-csv/'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

parser = argparse.ArgumentParser(description='Skript zum Hochladen einer CSV-Datei.')
parser.add_argument('-p', '--csv-path', type=str, required=True, help='Pfad zur CSV-Datei')
parser.add_argument('-v', '--verbose', action='store_true', help='Erhöhte Ausgabedetails')
args = parser.parse_args()

if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)

file_path = args.csv_path

if not os.path.exists(file_path):
    logging.error('Die Datei existiert nicht.')
    sys.exit(2)     # Statuscode 2 für Datei nicht gefunden

try:
    with open(file_path, 'rb') as file_data:
        files = {'file': file_data}
        logging.info('Beginne mit dem Hochladen der Datei...')
        response = requests.post(target_url, files=files)
        response.raise_for_status()
        logging.info('Datei erfolgreich hochgeladen.')
        logging.debug(f'Status Code: {response.status_code}')
        logging.debug(f'Response: {response.text}')
except requests.exceptions.RequestException as e:
    logging.error(f'Fehler beim Hochladen der Datei: {e}')
    sys.exit(3)     # Statuscode 3 für Netzwerk- o. HTTP Fehler
except Exception as e:
    logging.error(f'Ein unerwarteter Fehler ist aufgetreten: {e}')
    sys.exit(1)     # Stautscode 1 für allg. Fehler



# python .\main.py -p C:\Users\nikolais\Documents\python-task\vehicles.csv
# python .\main.py -p C:\Users\nicolai\PycharmProjects\python-task\vehicles.csv
