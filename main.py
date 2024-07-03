import requests

file_path = 'C:/Users/nikolais/Documents/python-task/vehicles.csv'
target_url = 'http://127.0.0.1:8000/upload-csv/'

with open(file_path, 'rb') as file_data:
    files = {'file': file_data}
    r = requests.post(target_url, files=files)

print(r.status_code)

# python .\main.py -s C:\Users\nikolais\Documents\python-task\vehicles.csv
# python .\main.py -s C:\Users\nicolai\PycharmProjects\python-task\vehicles.csv
