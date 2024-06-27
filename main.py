import requests
import os
import argparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('client.log'),
        logging.StreamHandler()
    ]
)

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

logging.info('Starte Login-Prozess.')
login_response = requests.post('http://127.0.0.1:8000/login',
                               json={'username': 'Test', 'password': '123456', 'token': 'TestToken'}, )
if login_response.status_code == 200:
    login_data = login_response.json()
    if login_data['login']:
        token = login_data['token']
        logging.info('Login erfolgreich.')

        logging.info('Starte Upload der Datei.')
        with open(file_path, 'rb') as file_data:
            files = {'file': file_data}
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.post(target_url, files=files, headers=headers)
            logging.info(f'Upload abgeschlossen. Statuscode: {response.status_code}')
    else:
        logging.error('Login fehlgeschlagen.')
        print(login_response)

else:
    logging.error('Fehler beim Login')
    print(login_response)

# python .\main.py -s C:\Users\nikolais\Documents\python-task\vehicles.csv
# python .\main.py -s C:\Users\nicolai\PycharmProjects\python-task\vehicles.csv
