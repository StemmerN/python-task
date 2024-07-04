import argparse
import logging
import os
import requests

target_url = 'http://127.0.0.1:8000/upload-csv/'

parser = argparse.ArgumentParser(description='Skript zum Hochladen einer CSV-Datei.')
parser.add_argument('-s', '--csv-path', type=str, required=True, help='Pfad zur CSV-Datei')
args = parser.parse_args()

file_path = args.csv_path

if os.path.exists(file_path):
    logging.info('Die Datei existiert.')
else:
    logging.error('Die Datei existiert nicht.')
    exit()

with open(file_path, 'rb') as file_data:
    files = {'file': file_data}
    r = requests.post(target_url, files=files)

print(r.status_code)

# python .\main.py -s C:\Users\nikolais\Documents\python-task\vehicles.csv
# python .\main.py -s C:\Users\nicolai\PycharmProjects\python-task\vehicles.csv
