import argparse
import logging
import os
import requests
import sys
import csv

# Ziel-URL für den Upload
target_url = 'http://127.0.0.1:8003/upload-csv/'

# Konfiguration des Loggings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def validate_and_preprocess_csv(file_path):
    # überprüft die CSV-Datei
    try:
        inconsistent_rows = []
        adjusted_rows = []

        # Lesen und Überarbeiten der CSV-Datei
        with open(file_path, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            rows = list(reader)

        header = rows[0]
        expected_num_fields = len(header)

        processed_rows = [header]
        for line_number, row in enumerate(rows[1:], start=2):
            if len(row) != expected_num_fields:
                inconsistent_rows.append((line_number, row))
                adjusted_row = row[:expected_num_fields] + [''] * (expected_num_fields - len(row))
                adjusted_rows.append((line_number, adjusted_row))
                row = adjusted_row
            processed_rows.append(row)

        # Überschreiben der Originaldatei mit den überarbeiteten Datei
        with open(file_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(processed_rows)

        logging.info(f'Die CSV-Datei wurde überarbeitet und überschrieben: {file_path}')
        return True, inconsistent_rows, adjusted_rows

    except Exception as e:
        logging.error(f'Fehler bei der Überarbeitung der CSV-Datei: {e}')
        return False, [], []


def upload_csv(file_path, verbose=False):
    # Erhöhte Ausgabedetails aktivieren, wenn das entsprechende Argument gesetzt ist (-v)
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

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
        logging.exception(
            f'HTTP-Fehler beim Hochladen der Datei: {e.response.text if e.response else "Keine Antwort erhalten"}')
        logging.error(f'Fehlerdetails: {e.response.content if e.response else "Keine Antwort erhalten"}')
        logging.error(
            f'Fehlerdetails (JSON): {e.response.json() if e.response and e.response.content else "Keine Antwort erhalten"}')
        sys.exit(3)  # Statuscode 3 für Netzwerk- oder HTTP-Fehler
    except Exception as e:
        logging.exception('Ein unerwarteter Fehler ist aufgetreten')
        sys.exit(1)  # Statuscode 1 für allgemeine Fehler


# Argumentparser für Kommandozeilenargumente
parser = argparse.ArgumentParser(description='Skript zum Überarbeiten und Hochladen einer CSV-Datei.')
parser.add_argument('-p', '--csv-path', type=str, required=True, help='Pfad zur CSV-Datei')
parser.add_argument('-v', '--verbose', action='store_true', help='Erhöhte Ausgabedetails')
args = parser.parse_args()

# Vorverarbeiten der CSV-Datei
success, inconsistent_rows, adjusted_rows = validate_and_preprocess_csv(args.csv_path)

if not success:
    logging.error('Überarbeitung der CSV-Datei fehlgeschlagen. Skript wird beendet.')
    sys.exit(4)  # Statuscode 4 für Überarbeitungsfehler

# Protokolldetails zu inkonsistenten und angepassten Zeilen
if inconsistent_rows:
    logging.info(f'Inconsistent rows: {inconsistent_rows}')
if adjusted_rows:
    logging.info(f'Adjusted rows: {adjusted_rows}')

# Hochladen der überarbeiteten CSV-Datei
upload_csv(args.csv_path, args.verbose)


# python .\main.py -p C:\Users\nikolais\Documents\python-task\vehicles_fixed.csv -v
# python .\main.py -p C:\Users\nicolai\PycharmProjects\python-task\vehicles_fixed.csv -v

