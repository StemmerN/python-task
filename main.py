import argparse
import logging
import os
import sys
import requests
import pandas as pd
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import PatternFill

# Ziel-URL für den Upload
target_url = 'http://127.0.0.1:8003/upload-csv/'

# Konfiguration des Loggings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
            return response.json()  # JSON-Antwort zurückgeben
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


def process_and_save_to_excel(response_data, keys, colored, excel_saving_path=None):
    # Excel-Workbook erstellen
    wb = Workbook()
    ws = wb.active

    # Header setzen
    headers = ['rnr'] + keys
    ws.append(headers)

    # Daten einfügen
    for vehicle in response_data['vehicle_data']:
        row = [vehicle.get('rnr', '')]
        for key in keys:
            row.append(vehicle.get(key, ''))
        ws.append(row)

        # Farbige Hervorhebung der Zeilen basierend auf `hu`
        if colored and ws.max_row > 1:  # Sicherstellen, dass Zeilen vorhanden sind
            hu_date = vehicle.get('hu')
            if hu_date:
                hu_date = datetime.strptime(hu_date, '%Y-%m-%d')
                now = datetime.now()
                diff_months = (now.year - hu_date.year) * 12 + now.month - hu_date.month
                if diff_months <= 3:
                    fill = PatternFill(start_color="007500", end_color="007500", fill_type="solid")
                elif diff_months <= 12:
                    fill = PatternFill(start_color="FFA500", end_color="FFA500", fill_type="solid")
                else:
                    fill = PatternFill(start_color="b30000", end_color="b30000", fill_type="solid")

                for cell in ws[ws.max_row]:  # Hier sicherstellen, dass auf die korrekte Zeile zugegriffen wird
                    cell.fill = fill

    # Speichern der Datei
    current_date = datetime.now().date().isoformat()
    file_name = f'vehicles_{current_date}.xlsx'

    # Falls ein Speicherort angegeben werden soll, alternativ wird weiterhin im aktuellen Verzeichnis gespeichert.
    if excel_saving_path:
        file_name = os.path.join(excel_saving_path, file_name)

    wb.save(file_name)
    logging.info(f'Datei {file_name} wurde erfolgreich erstellt.')


# Argumentparser für Kommandozeilenargumente
parser = argparse.ArgumentParser(description='Skript zum Hochladen einer CSV-Datei und Verarbeitung der API-Antwort.')
parser.add_argument('-p', '--csv-path', type=str, required=True, help='Pfad zur CSV-Datei')
parser.add_argument('-k', '--keys', nargs='+', required=True, help='Schlüssel für zusätzliche Spalten')
parser.add_argument('-c', '--colored', action='store_true', default=True, help='Zeilen farblich hervorheben')
parser.add_argument('-e', '--excel-saving-path', type=str, help='Optionaler Speicherort für die Excel-Datei')
parser.add_argument('-v', '--verbose', action='store_true', help='Erhöhte Ausgabedetails')
args = parser.parse_args()

# CSV-Datei hochladen und Response verarbeiten
response_data = upload_csv(args.csv_path, args.verbose)
process_and_save_to_excel(response_data, args.keys, args.colored, args.excel_saving_path)

# python .\main.py -p C:/Users/nikolais/Documents/python-task/vehicles.csv -k rnr labelIds hu -c -v
# python .\main.py -p C:\Users\nicolai\PycharmProjects\python-task\vehicles.csv -k rnr labelIds hu -c -v
