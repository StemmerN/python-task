import requests
import os
import argparse

target_url = 'http://127.0.0.1:8000/upload-csv/'

parser = argparse.ArgumentParser(description='Client-Skript zum Hochladen einer CSV-Datei.')
parser.add_argument('-p', '--csv-path', type=str, help='Pfad zur CSV-Datei')
args = parser.parse_args()

if args.csv_path:
    file_path = args.csv_path
else:
    file_path = 'C:/Users/nikolais/Documents/python-task/vehicles.csv'

# Überprüfen ob die Datei existiert
if os.path.exists(file_path):
    print("Die Datei existiert.")
else:
    print("Die Datei existiert nicht.")
    exit()

# Upload der Datei inkl. Datei schließen
with open(file_path, 'rb') as file_data:
    files = {'file': file_data}
    r = requests.post(target_url, files=files)

print(r.status_code)
